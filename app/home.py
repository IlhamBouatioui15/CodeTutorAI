import streamlit as st

st.set_page_config(page_title="Tuteur IA", page_icon="🐍", layout="wide")

st.title("Bienvenue dans Tuteur IA 👋")

st.sidebar.title("Navigation")
if st.sidebar.button("💬 Chat & IDE"):
    st.switch_page("pages/chat.py")

st.write("""
Cette application contient :
- Un chatbot générateur de **tutoriels**
- Un mini **IDE**
- Une page dédiée pour **générer et répondre à des quiz**
""")

