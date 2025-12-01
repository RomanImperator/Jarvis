import speech_recognition as sr 
from Speech import speak

# Initialize recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

def setup_mic():
    """
    Calibrates the microphone for ambient noise.
    This helps in better speech recognition accuracy.
    """
    with mic as source:
        print("[SYSTEM] Calibrating background noise...")
        r.adjust_for_ambient_noise(source, duration=0.5)

def listen_until_pause(pause_seconds=1.5, timeout=None) -> str | None:
    """
    Listens for speech input until a pause is detected.
    
    Args:
        pause_seconds (float): Duration of silence to consider the phrase complete.
        timeout (int): Maximum time to wait for speech to start.
        
    Returns:
        str | None: The recognized text in lowercase, or None if no speech detected/error.
    """
    with mic as source:
        print("[SYSTEM] Listening...")

        # Configure silence thresholds
        r.pause_threshold = pause_seconds 
        r.non_speaking_duration = 0.6 

        try:
            audio = r.listen(
                source,
                timeout=timeout,
                phrase_time_limit=None
            )
        except sr.WaitTimeoutError:
            return None

    try:
        # Recognize speech using Google Web Speech API (Italian)
        text = r.recognize_google(audio, language="it-IT")
        print(f"[YOU]: {text}")
        return text.lower()
    except sr.UnknownValueError:
        # Speech was unintelligible
        return None
    except sr.RequestError as e:
        print(f"[ERROR] Speech recognition service error: {e}")
        return None


def listen_continuous() -> str | None:
    """
    Continuously listens for the wake word or valid commands.
    Filters out noise and irrelevant speech.
    
    Returns:
        str | None: The valid command text if wake word is detected.
    """
    while True:
        text = listen_until_pause()

        if text is None:
            continue

        # Check for wake words or specific keywords
        # Note: 'delemain' seems to be a custom wake word or misinterpretation of 'jarvis'
        if "jarvis" in text or "jarvi" in text or "delemain" in text:
            return text
        else:
            print(f"[IGNORED] Missing wake word: {text}")


# DEBUG:
# if __name__ == "__main__":
#     setup_mic() 
#     while True:
#         print(listen_continuous())