import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyC4l1ci82Ov-AQuZ-dV-_Sx9VhtBfj_TZY"  # Remettez votre clé ici
genai.configure(api_key=GOOGLE_API_KEY)

print("Recherche des modèles disponibles...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Erreur de connexion : {e}")