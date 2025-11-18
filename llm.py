import os
import re
from google import genai

# Carica la chiave API dalle variabili d'ambiente
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Variabile d'ambiente GEMINI_API_KEY non trovata.")

client = genai.Client(api_key=api_key) # Inizializza il client Gemini AI

SYSTEM_PROMPT = (
    "Sei un assistente vocale che risponde in ITALIANO. "
    "Rispondi in modo breve e colloquiale, massimo 4-6 frasi. "
    "NON usare markdown, elenchi puntati, titoli, emoji o codice. "
    "Restituisci solo testo semplice, pronto per essere letto ad alta voce."
)

def _clean_for_tts(text: str) -> str:
    """Rimuove i caratteri tipici del markdown e spazi strani."""
    # elimina caratteri markdown più comuni
    text = re.sub(r'[*_`#>|]', " ", text)
    # compatta gli spazi
    text = re.sub(r'\s+', " ", text)
    return text.strip()

def generate_text(prompt: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\nUtente: {prompt}"
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    raw_text = response.text or ""
    return _clean_for_tts(raw_text)