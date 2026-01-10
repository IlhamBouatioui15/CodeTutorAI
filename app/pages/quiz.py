import streamlit as st
import requests

# Configuration de l'API
API_QUIZ = "http://127.0.0.1:8000/generate_quiz"

st.set_page_config(page_title="Quiz IA", page_icon="📝", layout="wide")

# Style CSS pour rester dans le thème moderne
st.markdown("""
    <style>
    .quiz-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4facfe;
        margin-bottom: 20px;
    }
    .stRadio > label { font-weight: bold; color: #1f1f1f; }
    </style>
    """, unsafe_allow_html=True)

st.title(" Auto-Évaluation par IA")

# 1. Vérification de la présence d'un tutoriel
if "last_tutorial" not in st.session_state or not st.session_state.last_tutorial:
    st.warning("⚠️ Aucun tutoriel n'a été trouvé. Veuillez d'abord générer un tutoriel dans le Chatbot.")
    if st.button("Aller au Chatbot"):
        st.switch_page("pages/chatbot.py") # Ajuste le chemin selon ta structure
    st.stop()

# 2. Logique de génération/régénération du quiz
# On vérifie si le tutoriel actuel est différent de celui qui a servi au dernier quiz
if "current_quiz_source" not in st.session_state:
    st.session_state.current_quiz_source = None

# Si le tutoriel a changé ou si aucun quiz n'existe encore
if st.session_state.current_quiz_source != st.session_state.last_tutorial:
    st.info("🔄 Un nouveau tutoriel a été détecté. Préparez-vous pour votre quiz !")
    
    if st.button("Générer le quiz pour ce tutoriel"):
        with st.spinner("L'IA analyse le tutoriel pour créer des questions..."):
            try:
                res = requests.post(API_QUIZ, json={"tutorial_text": st.session_state.last_tutorial})
                if res.status_code == 200:
                    st.session_state.generated_quiz = res.json().get("quiz", {})
                    st.session_state.current_quiz_source = st.session_state.last_tutorial
                    st.rerun()
                else:
                    st.error("Erreur serveur lors de la génération du quiz.")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
    st.stop()

# 3. Affichage du quiz si disponible
if "generated_quiz" in st.session_state:
    quiz = st.session_state.generated_quiz
    
    st.markdown(f"###  Sujet : {quiz.get('quiz_title', 'Évaluation de programmation')}")
    st.write("Répondez aux questions ci-dessous pour valider vos acquis.")

    with st.form("quiz_form"):
        user_responses = []
        for i, q in enumerate(quiz.get("questions", [])):
            st.markdown(f"""<div class="quiz-container">
                <p style='font-size:1.1rem;'><b>Question {i+1}:</b> {q['question']}</p>
            </div>""", unsafe_allow_html=True)
            
            res = st.radio("Sélectionnez votre réponse :", q["options"], key=f"q_{i}")
            user_responses.append(res)
        
        submitted = st.form_submit_button("Soumettre mes réponses")

    # 4. Calcul du Score
    if submitted:
        score = 0
        questions = quiz.get("questions", [])
        
        for i, q in enumerate(questions):
            # L'index de la bonne réponse est dans q['answer']
            correct_index = q['answer']
            correct_text = q['options'][correct_index]
            
            if user_responses[i] == correct_text:
                score += 1
                st.success(f"✅ Question {i+1} : Correct !")
            else:
                st.error(f"❌ Question {i+1} : Faux. La réponse était : **{correct_text}**")
        
        # Affichage final
        st.divider()
        final_score_pct = (score / len(questions)) * 100
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("Votre Score", f"{score} / {len(questions)}", f"{final_score_pct}%")
        
        with col2:
            if final_score_pct >= 70:
                st.balloons()
                st.success("Félicitations ! Vous avez bien assimilé le cours. 🏆")
            else:
                st.warning("Encore un peu d'effort ! Relisez le tutoriel dans le Chatbot. 📚")