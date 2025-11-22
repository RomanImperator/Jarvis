from Speech import speak
from Listen import main as rt
from Listen import setup_mic
from llm import Chat
from Video import Camera
from Vision import Vision

def main():
    setup_mic()
    chat = Chat()
    
    try:
        vision = Vision()
        camera = Camera()
        print("Sistema visivo pronto.")
    except Exception as e:
        print(f"Errore inizializzazione video: {e}")
        vision = None
        camera = None

    speak("In cosa posso essere utile Mare?")
    
    while True:
        user_input = rt() #crea un loop per ascoltare il utente
        if user_input is None:
            continue

        if "esci" in user_input or "quit" in user_input:
            speak("Ok, chiudo l'assistente. A presto!")
            if camera:
                camera.release()
            break

        # Controllo Intento Visivo
        if vision and camera and chat.check_visual_intent(user_input):
            print("[INFO] Rilevata richiesta visiva. Catturo immagine...")
            speak("Dammmi un secondo che guardo...")
            frame = camera.capture_frame()
            
            if frame:
                description = vision.describe(frame)
                print(f"[VISION]: {description}")
                # Arricchiamo il prompt per l'LLM
                user_input += f"\n\n[NOTA DI SISTEMA]: L'utente ti ha chiesto di guardare. Ecco cosa vede la telecamera: {description}"
            else:
                speak("Non riesco ad accedere alla telecamera.")

        risposta = chat.send_message(user_input)
        print(f"[ASSISTENTE]: {risposta}")
        speak(risposta)

if __name__ == "__main__":
    main()