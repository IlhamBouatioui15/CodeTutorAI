import io
import subprocess
import sys
import tempfile
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

import requests

load_dotenv()
# --- CONFIGURATION GEMINI ---
# Remplace par ta vraie clé

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-flash-latest"
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=(
        "Tu es un tuteur IA spécialisé EXCLUSIVEMENT en programmation et informatique. "
        "CONSIGNE DE SÉCURITÉ CRUCIALE : Si la question de l'utilisateur ne concerne pas la programmation, "
        "le développement logiciel, l'algorithmique ou l'informatique, tu dois refuser de répondre. "
        "Dans ce cas, utilise exactement cette phrase : 'Désolé, je suis un tuteur spécialisé uniquement en programmation. "
        "Je ne peux pas répondre à cette question ou demande hors de mon domaine d'expertise.'\n\n"
        
        "Si la demande concerne la programmation, ta mission est de produire des TUTORIELS COMPLETS, STRUCTURÉS et PROGRESSIFS "
        "en 3 niveaux :\n"
        "1) Débutant : explication simple, analogies, notions fondamentales.\n"
        "2) Intermédiaire : exemples pratiques, exercices guidés, erreurs courantes.\n"
        "3) Avancé : architecture, bonnes pratiques, optimisation.\n\n"
        "Tu écris dans un style clair et pédagogique."
    )
)
# --- FASTAPI ---
app = FastAPI(title="Backend Chat IA")

class ChatRequest(BaseModel):
    message: str
class CodeRequest(BaseModel):
    language: str
    code: str

# --- Charger les textes depuis le JSON ---
with open("geeks_texts.json", "r", encoding="utf-8") as f:
    all_texts = json.load(f)

# --- RAG (FAISS) ---
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(all_texts, embeddings)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})


prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "ÉVALUATION DU SUJET :\n"
        "La question suivante porte-t-elle sur la programmation ou l'informatique ?\n"
        "QUESTION UTILISATEUR : {question}\n\n"
        
        "=== INSTRUCTIONS ===\n"
        "1. SI LE SUJET N'EST PAS LA PROGRAMMATION : Réponds uniquement que tu es un tuteur de programmation et refuse la demande.\n"
        "2. SI LE SUJET EST LA PROGRAMMATION : Utilise le CONTEXTE DOCUMENTAIRE RAG ci-dessous (si pertinent) et génère un TUTORIEL COMPLET.\n\n"
        
        "CONTEXT DOCUMENTAIRE RAG :\n{context}\n\n"
        
        "STRUCTURE DU TUTORIEL (Si applicable) :\n"
        "1. Contexte général et but du tutoriel\n"
        "2. Niveau Débutant : bases + exemples simples\n"
        "3. Niveau Intermédiaire : exercices + mini-projet guidé\n"
        "4. Niveau Avancé : concepts experts + optimisation\n"
        "5. Résumé + exercices finaux\n\n"
        
        "=== RÉPONSE ===\n"
    )
)


def generate_gemini(text):
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return f"Erreur API : {str(e)}"

@app.post("/chat")

def chat_endpoint(req: ChatRequest):
    user_msg = req.message
    
    # RAG : On ajoute la question et on cherche le contexte
    docs = retriever.invoke(user_msg)
    context_text = "\n".join([d.page_content for d in docs])
    
    final_prompt = prompt_template.format(context=context_text, question=user_msg)
    
    # Génération
    response_text = generate_gemini(final_prompt)
    
    return {"response": response_text}


# Tu peux garder un mapping, mais avec les noms de langage Piston
LANGUAGE_MAP = {
    "python": "python",
    "javascript": "javascript",
    "c": "c",
    "java": "java",
    "go": "go",
    "ruby": "ruby",
    "php": "php"
}


@app.post("/execute")
def execute_code(req: CodeRequest):

    language = req.language.lower()

    if language not in ["python", "javascript", "java", "c", "go", "ruby", "php"]:
        return {"output": f"Langage {req.language} non supporté."}

    payload = {
        "language": language,
        "version": "*",  # Piston choisit automatiquement la version la plus récente
        "files": [
            {
                "content": req.code
            }
        ],
        "stdin": ""
    }

    try:
        response = requests.post(
            "https://emkc.org/api/v2/piston/execute",
            json=payload
        )

        if response.status_code != 200:
            return {"output": f"Erreur Piston : {response.status_code} - {response.text}"}

        result = response.json()

        output = result.get("run", {}).get("output", "")

        if not output:
            output = "Aucun résultat."

        return {"output": output.strip()}

    except Exception as e:
        return {"output": f"Erreur API Piston : {e}"}


class QuizRequest(BaseModel):
    tutorial_text: str  # texte du tutoriel à partir duquel générer le quiz


@app.post("/generate_quiz")
def generate_quiz(req: QuizRequest):
    prompt = f"""
    Génère un quiz de 10 questions à choix multiples à partir de ce tutoriel :
    {req.tutorial_text}
    Réponds UNIQUEMENT au format JSON suivant :
    {{
        "quiz_title": "Quiz sur le tutoriel",
        "questions": [
            {{
                "question": "...",
                "options": ["...","...","...","..."],
                "answer": 0
            }}
        ]
    }}
    """
    try:
        response = model.generate_content(prompt)
        # NETTOYAGE : Enlève les balises ```json si Gemini les ajoute
        raw_text = response.text.strip().replace("```json", "").replace("```", "")
        quiz_json = json.loads(raw_text)
        return {"quiz": quiz_json}
    except Exception as e:
        print(f"Erreur : {e}")
        return {"quiz": {}, "error": str(e)}