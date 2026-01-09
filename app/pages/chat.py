import streamlit as st
import requests
from streamlit_monaco_editor import st_monaco

API_CHAT = "http://127.0.0.1:8000/chat"
API_EXEC = "http://127.0.0.1:8000/execute"
API_QUIZ = "http://127.0.0.1:8000/generate_quiz"

st.set_page_config(page_title="Chat & IDE", layout="wide")

# ------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Accueil"):
    st.switch_page("home.py")
if st.sidebar.button("📝 Quiz"):
    st.switch_page("pages/quiz.py")

st.title("Chatbot + IDE")

# SESSION
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_tutorial" not in st.session_state:
    st.session_state.last_tutorial = ""


# ------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------
col_ide, col_chat = st.columns([1, 1.6])

# ------------------------------------------------------------
# IDE
# ------------------------------------------------------------
with col_ide:
    st.subheader("IDE Multilangage")

    LANGAGES = {
        "Python": "python",
        "JavaScript": "javascript",
        "C": "c",
        "Java": "java",
        "Go": "go",
        "Ruby": "ruby",
        "PHP": "php",
    }

    langage = st.selectbox("Choisir un langage :", list(LANGAGES.keys()))
    monaco_lang = LANGAGES[langage]

    code_default = {
        "Python": "print('Hello Python!')",
        "JavaScript": "console.log('Hello JS!')",
        "C": "#include <stdio.h>\nint main(){ printf(\"Hello C!\"); return 0; }",
        "Java": "class Main{ public static void main(String[] args){ System.out.println(\"Hello Java!\"); }}",
        "Go": "package main\nimport \"fmt\"\nfunc main(){ fmt.Println(\"Hello Go!\") }",
        "Ruby": "puts 'Hello Ruby!'",
        "PHP": "<?php echo 'Hello PHP!'; ?>"
    }

    code = st_monaco(
        value=code_default[langage],
        language=monaco_lang,
        theme="vs-dark",
        height="350px"
    )

    if st.button("▶️ Run", type="primary"):
        try:
            res = requests.post(API_EXEC, json={
                "language": langage.lower(),
                "code": code
            })
            if res.status_code == 200:
                st.subheader("Résultat :")
                st.code(res.json().get("output", ""))
            else:
                st.error(f"Erreur API : {res.text}")
        except Exception as e:
            st.error(f"Erreur de communication : {e}")


# ------------------------------------------------------------
# CHATBOT
# ------------------------------------------------------------
with col_chat:
    st.subheader("Chat")

    chat_box = st.empty()
    with chat_box.container():
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Pose ta question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            res = requests.post(API_CHAT, json={"message": prompt})
            ai = res.json()["response"]
            st.session_state.last_tutorial = ai
            st.session_state.messages.append({"role": "assistant", "content": ai})
            st.markdown(ai)


# ------------------------------------------------------------
# Bouton pour aller au quiz
# ------------------------------------------------------------
st.write("---")
if st.button("🎯 Générer un Quiz à partir du tutoriel"):
    if not st.session_state.last_tutorial:
        st.warning("Aucun tutoriel trouvé.")
    else:
        # On enregistre simplement le texte puis on change de page
        st.sidebar.success("Quiz généré, direction la page Quiz !")
        st.switch_page("pages/quiz.py")
        st.write("---")

