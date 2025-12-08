from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai # On remplace OpenAI par Google GenAI
import os

# ---------------------------------------
# CONFIGURATION GOOGLE GEMINI
# ---------------------------------------
# Obtenez votre clé sur : https://aistudio.google.com/app/apikey
GOOGLE_API_KEY = "AIzaSyC4l1ci82Ov-AQuZ-dV-_Sx9VhtBfj_TZY"

genai.configure(api_key=GOOGLE_API_KEY)

# Nom du modèle (utilisez 'gemini-1.5-flash' ou 'gemini-1.5-pro' actuellement)
# Si Gemini 3 sort, changez simplement ce nom (ex: "gemini-3.0-pro")
MODEL_NAME = "gemini-flash-latest"

# Configuration du modèle avec l'instruction système
system_instruction = "Tu es un assistant expert en programmation. Tu crées des tutoriels clairs, structurés et pédagogiques avec des exemples de code concrets et bien commentés."

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=system_instruction
)

# ---------------------------------------
# FASTAPI
# ---------------------------------------
app = FastAPI(title="Chat IA Tutoriels (Google Gemini)", version="2.0")

def generate_response(prompt_text, max_tokens=2000, temperature=0.2):
    try:
        # Configuration de la génération
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
        )

        # Appel à l'API Gemini
        response = model.generate_content(
            prompt_text,
            generation_config=generation_config
        )
        
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération Gemini : {str(e)}"

# ---------------------------------------
# Embeddings + FAISS (Inchangé)
# ---------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store = FAISS.from_texts(
    ["Bienvenue ! Pose-moi une question pour obtenir un tutoriel de programmation."],
    embeddings
)
retriever = vector_store.as_retriever()

# ---------------------------------------
# PromptTemplate
# ---------------------------------------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Contexte: {context}\n\n"
        "Question: {question}\n\n"
        "Donne un tutoriel clair et structuré avec des exemples de code concrets.\n"
    )
)

# ---------------------------------------
# Schéma API
# ---------------------------------------
class ChatRequest(BaseModel):
    message: str

# ---------------------------------------
# Endpoint /chat
# ---------------------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = req.message

    # Note: Ajouter la question au store à chaque fois peut polluer le contexte
    # mais je garde votre logique originale.
    vector_store.add_texts([user_msg])
    
    docs = retriever.invoke(user_msg)
    context_text = "\n".join([d.page_content for d in docs])

    final_prompt = prompt.format(context=context_text, question=user_msg)

    # Appel Gemini API
    answer = generate_response(final_prompt)

    return {"response": answer}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "provider": "Google Gemini",
        "note": "Modèle multimodal performant"
    }

# ---------------------------------------
# Mode Console
# ---------------------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print(f"🚀 MODE CONSOLE : Google {MODEL_NAME}")
    print("="*60)
    print("📝 Clé API : https://aistudio.google.com/app/apikey")
    print("💡 Tape 'quit' pour arrêter.\n")

    while True:
        user_input = input("Vous : ")

        if user_input.lower() in ["quit", "exit"]:
            print("Fin du chat.")
            break

        # Ajouter dans FAISS
        vector_store.add_texts([user_input])

        # Récupération du contexte
        docs = retriever.invoke(user_input)
        context_text = "\n".join([d.page_content for d in docs])

        # Prompt final
        full_prompt = prompt.format(context=context_text, question=user_input)

        # Génération via Gemini
        print("\n⏳ Génération en cours...")
        response = generate_response(full_prompt)

        print("\nAssistant :", response, "\n")