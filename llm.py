import os
import re
from google import genai

# System prompt defining the AI's persona
SYSTEM_PROMPT = (
    "Sei J.A.R.V.I.S., un'intelligenza artificiale avanzata al servizio di Tony Stark (l'utente). "
    "Rispondi in ITALIANO con tono formale, efficiente, educato e leggermente 'british'. "
    "Rivolgiti all'utente chiamandolo 'Signore'. Sii conciso e preciso. Massimo 3-4 frasi..."
)

# Pre-compile regex patterns for better performance
MARKDOWN_CHARS_PATTERN = re.compile(r'[*_`#>|]')
WHITESPACE_PATTERN = re.compile(r'\s+')

def _clean_for_tts(text: str) -> str:
    """
    Cleans text for Text-to-Speech (TTS) processing.
    Removes markdown characters and normalizes whitespace.
    """
    # Remove common markdown characters
    text = MARKDOWN_CHARS_PATTERN.sub(" ", text)
    # Compact multiple spaces into one
    text = WHITESPACE_PATTERN.sub(" ", text)
    return text.strip()

class Chat:
    """
    Manages the chat interaction with the LLM (Gemini).
    Handles message history, summarization, and visual intent detection.
    """
    def __init__(self):
        """
        Initializes the Chat instance, setting up the Gemini client
        and chat history parameters.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Environment variable GEMINI_API_KEY not found.")
        
        self.client = genai.Client(api_key=api_key)
        self.history = []
        self.summary = ""
        self.max_history = 10

    def _summarize_history(self):
        """
        Summarizes the conversation history to save context window space.
        The summary replaces the detailed history to keep the context concise.
        """
        if not self.history:
            return

        history_text = "\n".join([f"{role}: {msg}" for role, msg in self.history])
        prompt = (
            f"Summarize the following conversation concisely, keeping key points and important context for future interactions. "
            f"Previous summary: {self.summary}\n\n"
            f"Recent conversation:\n{history_text}"
        )
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        self.summary = response.text or ""
        self.history = []

    def send_message(self, user_input: str) -> str:
        """
        Sends a message to the LLM and returns the response.
        Manages history and context, summarizing old conversations if needed.
        
        Args:
            user_input (str): The user's message.
            
        Returns:
            str: The LLM's cleaned response.
        """
        # Summarize history if it exceeds the limit
        if len(self.history) >= self.max_history:
            self._summarize_history()

        self.history.append(("Utente", user_input)) # Add user input to history
        
        # Build the full prompt with context and history
        history_text = "\n".join([f"{role}: {msg}" for role, msg in self.history])
        context = ""
        if self.summary:
            context += f"Previous Summary: {self.summary}\n\n"
        
        full_prompt = f"{SYSTEM_PROMPT}\n\n{context}Recent History:\n{history_text}\n\nUtente: {user_input}"

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        raw_text = response.text or ""
        cleaned_text = _clean_for_tts(raw_text)
        
        self.history.append(("Assistente", cleaned_text)) # Add assistant response to history
        
        return cleaned_text

    def check_visual_intent(self, user_input: str) -> bool:
        """
        Determines if the user's input requires the use of the camera.
        
        Args:
            user_input (str): The user's message.
            
        Returns:
            bool: True if visual context is needed, False otherwise.
        """
        prompt = (
            f"Analyze the following user phrase and respond ONLY with 'YES' if it requires seeing something, "
            f"or 'NO' otherwise. Examples YES: 'What do you see?', 'Describe this', 'What am I holding?'. "
            f"Examples NO: 'What time is it?', 'Tell me a story', 'Who is the president?'.\n\n"
            f"Phrase: {user_input}"
        )
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        text = response.text or ""
        return "YES" in text.upper().strip() or "SI" in text.upper().strip()