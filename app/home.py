import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Tuteur IA - Apprendre le Code", page_icon="🐍", layout="wide")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    /* Import de polices */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient de fond pour le header */
    .main-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 60px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Style des cartes de fonctionnalités */
    .feature-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
        height: 100%;
        border: 1px solid #f0f2f6;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .icon-circle {
        width: 60px;
        height: 60px;
        background: #f0f7ff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        font-size: 30px;
    }

    /* Section "Comment ça marche" */
    .step-box {
        border-left: 4px solid #4facfe;
        padding-left: 20px;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER / HERO SECTION ---
st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 10px;">L'apprentissage du code réinventé par l'IA </h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Apprenez, pratiquez et testez vos compétences sur une plateforme unique et interactive.</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION AVANTAGES (3 Colonnes) ---
st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Nos piliers d'apprentissage</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-circle">🤖</div>
            <h3>Tuteur Intelligent</h3>
            <p>Un chatbot spécialisé qui génère des tutoriels sur mesure selon votre niveau et vos besoins spécifiques.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-circle">💻</div>
            <h3>IDE Intégré</h3>
            <p>Plus besoin d'installer d'outils complexes. Écrivez et testez votre code directement dans votre navigateur.</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="icon-circle">📝</div>
            <h3>Quiz Dynamiques</h3>
            <p>Validez vos connaissances avec des quiz générés par IA et suivez votre progression en temps réel.</p>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# --- SECTION "FONCTIONNEMENT" ---
col_text, col_img = st.columns([1, 1])

with col_text:
    st.markdown("## Comment ça fonctionne ?")
    st.markdown("""
    <div class="step-box">
        <h4>1. Choisissez votre sujet</h4>
        <p>Discutez avec l'IA pour définir ce que vous voulez apprendre (Python, Javascript, C, Algo...).</p>
    </div>
    <div class="step-box">
        <h4>2. Pratiquez en direct</h4>
        <p>Utilisez l'IDE pour appliquer les concepts du tutoriel immédiatement.</p>
    </div>
    <div class="step-box">
        <h4>3. Évaluez-vous</h4>
        <p>Générez un quiz basé sur votre session pour ancrer vos connaissances.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Commencer l'aventure"):
        st.balloons()
        st.info("Utilisez la barre latérale pour naviguer entre les outils !")

with col_img:
    # Ici, tu peux mettre une image d'illustration ou un composant visuel
    st.image("https://illustrations.popsy.co/amber/coding.svg", use_container_width=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.8rem; border-top: 1px solid #eee; padding-top: 20px;">
        Propulsé par Streamlit & Intelligence Artificielle • 2026 Tuteur IA
    </div>
    """, unsafe_allow_html=True)