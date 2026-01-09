import streamlit as st
import requests

API_QUIZ = "http://127.0.0.1:8000/generate_quiz"

st.set_page_config(page_title="Quiz", layout="wide")

st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Accueil"):
    st.switch_page("home.py")
if st.sidebar.button("💬 Chat & IDE"):
    st.switch_page("pages/chat.py")

st.title("Quiz basé sur tutoriel")

if "last_tutorial" not in st.session_state or not st.session_state.last_tutorial:
    st.warning("Aucun tutoriel n’a été généré. Retourne dans le Chat.")
    st.stop()

# ------------------------------------------------------------
# Génération / Récupération du quiz
# ------------------------------------------------------------
# On stocke le quiz dans session_state pour qu'il ne disparaisse pas au clic
if "generated_quiz" not in st.session_state:
    with st.spinner("Génération du quiz par l'IA..."):
        res = requests.post(API_QUIZ, json={"tutorial_text": st.session_state.last_tutorial})
        st.session_state.generated_quiz = res.json().get("quiz", {})

quiz = st.session_state.generated_quiz

if not quiz or "questions" not in quiz:
    st.error("Erreur lors de la génération du quiz. Réessaie.")
    if st.button("Réessayer"):
        del st.session_state.generated_quiz
        st.rerun()
    st.stop()

st.subheader(quiz.get("quiz_title", "Quiz"))

# ------------------------------------------------------------
# Affichage questions dans un Formulaire
# ------------------------------------------------------------
with st.form("quiz_form"):
    user_responses = []
    for i, q in enumerate(quiz["questions"]):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        # On récupère l'index de la réponse choisie
        res = st.radio("Choisir :", q["options"], key=f"q_{i}")
        user_responses.append(res)
    
    submitted = st.form_submit_button("Valider mes réponses")

# ------------------------------------------------------------
# Score
# ------------------------------------------------------------
if submitted:
    score = 0
    for i, q in enumerate(quiz["questions"]):
        actual_answer_text = q["options"][q["answer"]]
        if user_responses[i] == actual_answer_text:
            score += 1
            st.success(f"Question {i+1} : Correct !")
        else:
            st.error(f"Question {i+1} : Faux (La réponse était : {actual_answer_text})")
            
    st.divider()
    st.subheader(f"Score final : {score} / {len(quiz['questions'])}")
    
    if score == len(quiz["questions"]):
        st.balloons()