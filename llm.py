import os
import re
from google import genai

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

class Chat:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Variabile d'ambiente GEMINI_API_KEY non trovata.")
        
        self.client = genai.Client(api_key=api_key)
        self.history = []
        self.summary = ""
        self.max_history = 10

    def _summarize_history(self):
        if not self.history:
            return

        history_text = "\n".join([f"{role}: {msg}" for role, msg in self.history])
        prompt = (
            f"Riassumi la seguente conversazione in modo conciso, mantenendo i punti chiave e il contesto importante per le future interazioni. "
            f"Precedente riassunto: {self.summary}\n\n"
            f"Conversazione recente:\n{history_text}"
        )
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        self.summary = response.text or ""
        self.history = []

    def send_message(self, user_input: str) -> str:
        if len(self.history) >= self.max_history:
            self._summarize_history()

        self.history.append(("Utente", user_input)) # Aggiunge la conversazione al history
        
        history_text = "\n".join([f"{role}: {msg}" for role, msg in self.history])
        context = ""
        if self.summary:
            context += f"Riassunto precedente: {self.summary}\n\n"
        
        full_prompt = f"{SYSTEM_PROMPT}\n\n{context}Storia recente:\n{history_text}\n\nUtente: {user_input}"

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        raw_text = response.text or ""
        cleaned_text = _clean_for_tts(raw_text)
        
        self.history.append(("Assistente", cleaned_text)) # Aggiunge la conversazione al history
        
        return cleaned_text