# CodeTutorAI 

**CodeTutorAI** est une application intelligente conçue pour assister les apprenants en programmation.  
Elle permet de générer des **explications pédagogiques**, des **exemples de code** et des **tutoriels étape par étape** à partir de simples questions posées par l’utilisateur.

Le projet repose sur une architecture moderne combinant un **backend API** et une **interface frontend interactive**, offrant une expérience d’apprentissage fluide et efficace.

---

## Objectifs du projet

- Faciliter l’apprentissage de la programmation
- Fournir des explications claires et structurées
- Aider les débutants comme les utilisateurs avancés
- Centraliser l’aide pédagogique via une intelligence artificielle

---

## Fonctionnalités principales

- Génération intelligente d’explications de code
- Tutoriels détaillés étape par étape
- Exemples pratiques pour plusieurs langages
- Interface utilisateur simple et interactive
- Communication fluide entre le frontend et le backend

---

## 🛠️ Technologies utilisées

- **Python**
- **FastAPI** – Backend API
- **Uvicorn** – Serveur ASGI
- **Streamlit** – Interface utilisateur
- **IA / NLP** – Génération des réponses

---

## Démarrage de l’application

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/IlhamBouatioui15/CodeTutorAI.git
cd CodeTutorAI
```

### Étape 2 : Créer et activer l’environnement virtuel
**Sous Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Sous Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 4 : Lancer le backend (FastAPI)
```bash
uvicorn back:app --reload
```


### Étape 5 : Lancer le frontend (Streamlit)

Ouvrir un nouveau terminal, activer l’environnement virtuel puis exécuter :

```bash
streamlit run app/home.py
```

L’application s’ouvrira automatiquement dans le navigateur.

## Utilisation

Accéder à l’interface Streamlit

Poser une question de programmation

Recevoir une explication détaillée

Tester et apprendre de manière interactive

## Améliorations futures

Support multilingue

Éditeur de code intégré

Historique des conversations

Authentification des utilisateurs
