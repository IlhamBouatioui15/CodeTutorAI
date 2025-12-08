import streamlit as st
import requests
from streamlit_monaco_editor import st_monaco
import io
import sys

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="Tuteur IA", page_icon="🐍", layout="wide")

API_CHAT = "http://127.0.0.1:8000/chat"
API_EXEC = "http://127.0.0.1:8000/execute"

st.title("🤖 Tuteur IA — Coding")

# -------------------------------------------------------------------
# SESSION
# -------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------------------------
# LAYOUT
# -------------------------------------------------------------------
col_ide, col_chat = st.columns([1, 1.6])

# -------------------------------------------------------------------
# LANGAGES PRIS EN CHARGE
# -------------------------------------------------------------------
LANGAGES = {
    "Python": "python",
    "JavaScript": "javascript",
    "C": "c",
    "C++": "cpp",
    "Java": "java",
    "Go": "go",
    "Ruby": "ruby",
    "PHP": "php",
    "Swift": "swift"
}

# ===================================================================
# IDE COLONNE
# ===================================================================
with col_ide:
    st.subheader("IDE Multilangage")

    langage = st.selectbox("Choisir un langage :", list(LANGAGES.keys()))
    monaco_lang = LANGAGES[langage]

    code_default = {
        "Python": "print('Hello Python!')",
        "JavaScript": "console.log('Hello JS!')",
        "C": "#include <stdio.h>\nint main(){ printf(\"Hello C!\"); return 0; }",
        "C++": "#include <iostream>\nint main(){ std::cout << \"Hello C++!\"; return 0; }",
        "Java": "class Main{ public static void main(String[] args){ System.out.println(\"Hello Java!\"); }}",
        "Go": "package main\nimport \"fmt\"\nfunc main(){ fmt.Println(\"Hello Go!\") }",
        "Ruby": "puts 'Hello Ruby!'",
        "PHP": "<?php echo 'Hello PHP!'; ?>",
        "Swift": "print(\"Hello Swift!\")"
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

# ===================================================================
# CHATBOT COLONNE (avec input fixe en bas)
# ===================================================================
with col_chat:
    st.subheader("Chatbot Coding")

    # Affichage de l'historique
    chat_box = st.empty()
    with chat_box.container():
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input utilisateur (fixé en bas)
    st.markdown("<div style='position:sticky; bottom:0; background-color:white; padding-top:10px;'></div>", unsafe_allow_html=True)
    if prompt := st.chat_input("Pose ta question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Appel API FastAPI
        with st.chat_message("assistant"):
            with st.spinner("En cours..."):
                try:
                    response = requests.post(API_CHAT, json={"message": prompt})
                    if response.status_code == 200:
                        ai = response.json()["response"]
                    else:
                        ai = f"Erreur API : {response.text}"
                except Exception:
                    ai = "❌ Impossible de contacter le serveur FastAPI."
                st.markdown(ai)
                st.session_state.messages.append({"role": "assistant", "content": ai})
