import os
from google import genai

# Carica la chiave API dal nome dalla variabile d'ambiente corretta
api_key = os.getenv("GEMINI_API_KEY") 

if not api_key:
    raise ValueError("Variabile d'ambiente GEMINI_API_KEY non trovata.")


client = genai.Client(api_key=api_key) # Inizializza il client con la chiave API

def generate_text(prompt: str) -> str:
    response = client.models.generate_content( #manda una richiesta di generazione di contenuti
        model="gemini-2.5-flash", 
        contents=prompt
    )

    # Ensure we always return a string; fallback to empty string if None
    return response.text or ""