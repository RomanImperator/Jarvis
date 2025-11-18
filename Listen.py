import speech_recognition as sr 
from Speech import speak

r = sr.Recognizer() #crea un riconoscitore di parlato
mic = sr.Microphone() #usa il microfono di default del sistema

def setup_mic(): #Calibra il microfono per il rumore di fondo
    with mic as source:
        print("Calibro il rumore di fondo...")
        r.adjust_for_ambient_noise(source, duration=0.5)  #type: ignore

def listen_until_pause(pause_seconds=1.0, timeout=10) -> str | None:
    """
    Ascolta dal microfono finché non rileva circa 'pause_seconds'
    secondi di silenzio. 'timeout' è il tempo massimo per iniziare
    a parlare (dopo aver avviato l'ascolto).
    """

    with mic as source:
        print("Sto ascoltando, parla pure...")

        # Quanto silenzio deve passare prima di considerare finita la frase
        r.pause_threshold = pause_seconds
        # Quanto silenzio minimo ignora all'inizio / tra parole non significative
        r.non_speaking_duration = 0.6

        try:
            # phrase_time_limit=None -> niente limite fisso sulla durata
            audio = r.listen(
                source,
                timeout=timeout,          # quanto tempo hai per INIZIARE a parlare
                phrase_time_limit=None    # puoi parlare finché non fai 0.6s di silenzio
            )
        except sr.WaitTimeoutError:
            print("Non hai iniziato a parlare in tempo.")
            return None

    # Una volta che listen() ritorna, proviamo a riconoscere il parlato
    try:
        text = r.recognize_google(audio, language="it-IT") #type: ignore
        print(f"[TU]: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Non ho capito cosa hai detto.")
        speak("Non ho capito, puoi ripetere?")  # da fare dire all'assistente in futuro
        return None
    except sr.RequestError as e:
        print("Errore di connessione al servizio di riconoscimento:", e)
        speak("Ho problemi a connettermi per il riconoscimento vocale.")  # da fare dire all'assistente in futuro
        return None


def main() -> str | None:
    while True:
        user_input = input("\nPremi INVIO per parlare, oppure q + INVIO per uscire: ")
        if user_input.lower() == "q":
            return "__quit__"

        # Ascolta finché non fai 3 secondi di silenzio
        text = listen_until_pause()

        if text is None:
            continue

        return text


if __name__ == "__main__":
    main()