import gtts
import os

language = 'it'
def speak(text: str):
    try:
        tts = gtts.gTTS(text=text, lang=language)
        temp_file = "temp_speech.mp3"
        tts.save(temp_file)
        os.system(f"start {temp_file}")
    except Exception as e:
        print(f"Errore nella sintesi vocale: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)