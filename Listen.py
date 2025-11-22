import speech_recognition as sr 
from Speech import speak

r = sr.Recognizer() #crea un riconoscitore di parlato
mic = sr.Microphone() #usa il microfono di default del sistema

def setup_mic(): #Calibra il microfono per il rumore di fondo
    with mic as source:
        print("Calibro il rumore di fondo...")
        r.adjust_for_ambient_noise(source, duration=0.5)  #type: ignore

def listen_until_pause(pause_seconds=1.5, timeout=None) -> str | None:
    """
    Ascolta dal microfono finché non rileva circa 'pause_seconds'
    secondi di silenzio. 'timeout' è il tempo massimo per iniziare
    a parlare (dopo aver avviato l'ascolto).
    """

    with mic as source:
        print("Sto ascoltando, parla pure...")

        r.pause_threshold = pause_seconds #Quanto silenzio deve passare prima di considerare finita la frase
        r.non_speaking_duration = 0.6 #Quanto silenzio minimo ignora all'inizio / tra parole non significative

        try:
            audio = r.listen(
                source,
                timeout=timeout,
                phrase_time_limit=None
            )
        except sr.WaitTimeoutError:
            return None

    try:
        text = r.recognize_google(audio, language="it-IT") #type: ignore
        print(f"[TU]: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Errore di connessione al servizio di riconoscimento:", e)
        return None


def main() -> str | None:
    while True:
        text = listen_until_pause(timeout=5)

        if text is None:
            continue

        if "jarvis" or "jarvi" or "delemain" in text:
            return text
        else:
            print(f"Ignorato (manca wake word 'Jarvis'): {text}")


#PER DEBUG:
# if __name__ == "__main__":
#     setup_mic() # Assicuriamoci di calibrare se lanciato direttamente
#     while True:
#         print(main())