import streamlit as st
import requests
from streamlit_monaco_editor import st_monaco

# --- CONFIGURATION ---
st.set_page_config(page_title="Tuteur IA - Code & Chat", page_icon="🐍", layout="wide")

API_CHAT = "http://127.0.0.1:8000/chat"
API_EXEC = "http://127.0.0.1:8000/execute"

# --- STYLE CSS (Inspiré de l'accueil) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header stylisé plus compact */
    .chat-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Conteneur pour l'IDE et le Chat */
    .stColumn > div {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }

    /* Style du bouton Run */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
    }
    
    /* Style spécifique pour la zone de résultat */
    .result-box {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_tutorial" not in st.session_state:
    st.session_state.last_tutorial = ""

# --- HEADER ---
st.markdown("""
    <div class="chat-header">
        <h2 style="margin:0;">💻 Espace de Travail Interactif</h2>
        <p style="margin:0; opacity:0.9;">Apprenez avec l'IA et testez votre code en temps réel</p>
    </div>
    """, unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
col_ide, col_chat = st.columns([1, 1.4], gap="large")

# ------------------------------------------------------------
# SECTION IDE (GAUCHE)
# ------------------------------------------------------------
with col_ide:
    st.markdown("### 🛠️ IDE Multilangage")
    
    LANGAGES = {
        "Python": "python",
        "JavaScript": "javascript",
        "C": "c",
        "Java": "java",
        "Go": "go",
        "Ruby": "ruby",
        "PHP": "php",
    }
    
    langage = st.selectbox("Langage de programmation", list(LANGAGES.keys()))
    
    code_default = {
        "Python": "print('Hello Python!')",
        "JavaScript": "console.log('Hello JS!')",
        "C": "#include <stdio.h>\nint main() {\n    printf(\"Hello C!\");\n    return 0;\n}",
        "Java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello Java!\");\n    }\n}",
        "Go": "package main\nimport \"fmt\"\nfunc main() {\n    fmt.Println(\"Hello Go!\")\n}",
        "Ruby": "puts 'Hello Ruby!'",
        "PHP": "<?php echo 'Hello PHP!'; ?>"
    }

    # Editor Monaco
    code = st_monaco(
        value=code_default[langage],
        language=LANGAGES[langage],
        theme="vs-dark",
        height="400px"
    )

    if st.button("Exécuter le code", type="primary"):
        with st.spinner("Exécution..."):
            try:
                res = requests.post(API_EXEC, json={
                    "language": langage.lower(),
                    "code": code
                })
                if res.status_code == 200:
                    st.markdown(" **Résultat :**")
                    output = res.json().get("output", "Aucune sortie")
                    st.code(output, language=LANGAGES[langage])
                else:
                    st.error("Erreur lors de l'exécution.")
            except Exception as e:
                st.error(f"Erreur API : {e}")


# ------------------------------------------------------------
# SECTION CHATBOT (DROITE)
# ------------------------------------------------------------
with col_chat:
    st.markdown('<div class="column-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Tuteur IA")
    
    # LE CONTENEUR SCROLLABLE : 
    # C'est ici que tout se passe. On fixe la hauteur (ex: 550px).
    # Seul ce bloc défilera si le tutoriel est long.
    chat_container = st.container(height=550)

    with chat_container:
        # Affichage de tous les messages (y compris le long tutoriel)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # L'input reste en bas, à l'intérieur du cadre blanc mais hors du container scrollable
    if prompt := st.chat_input("Posez votre question (ex: Tutoriel Python débutant)"):
        # 1. Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Afficher immédiatement dans le container
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            # 3. Appel API et affichage de la réponse (Tutoriel)
            with st.chat_message("assistant"):
                with st.spinner("Le tuteur rédige votre tutoriel..."):
                    try:
                        res = requests.post(API_CHAT, json={"message": prompt})
                        if res.status_code == 200:
                            ai_response = res.json()["response"]
                            st.markdown(ai_response) # Le tutoriel s'affiche ici
                            
                            # Sauvegarde
                            st.session_state.last_tutorial = ai_response
                            st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        else:
                            st.error("Erreur technique.")
                    except Exception as e:
                        st.error(f"Erreur de connexion : {e}")
        
        # Petit hack pour forcer le scroll vers le bas après la réponse
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# ACTION FOOTER : GÉNÉRATION DU QUIZ
# ------------------------------------------------------------
st.write("---")
col_info, col_btn = st.columns([2, 1])

with col_info:
    if st.session_state.last_tutorial:
        st.success("Un tutoriel est prêt ! Vous pouvez maintenant tester vos connaissances.")
    else:
        st.info("Posez une question pour générer un tutoriel et débloquer le quiz.")

with col_btn:
    if st.button("Passer au Quiz de Validation", use_container_width=True):
        if not st.session_state.last_tutorial:
            st.warning("Veuillez d'abord générer un tutoriel avec le chatbot.")
        else:
            # Nettoyage de l'ancien quiz pour forcer la regénération sur la page Quiz
            if "generated_quiz" in st.session_state:
                del st.session_state.generated_quiz
            
            st.switch_page("pages/quiz.py")