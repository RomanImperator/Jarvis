from gtts import gTTS
import os
import pygame
import tempfile
import time

language = 'it'
pygame.mixer.init() # Inizializza il mixer di pygame per la riproduzione audio

def speak(text: str):
    temp_file = None
    try:
        fd, temp_file = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)  # Chiudi il file descriptor

        tts = gTTS(text=text, lang=language)
        tts.save(temp_file)
        
        pygame.mixer.music.load(temp_file) # carica il file temporaneo
        pygame.mixer.music.play() 
        
        while pygame.mixer.music.get_busy(): # aspetta che finisca la riproduzione
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()  # scarica il file dalla memoria
        os.remove(temp_file)  # elimina il file temporaneo

    except PermissionError as e:
        print(f"PermissionError nella sintesi vocale: {e}")
    except Exception as e:
        print(f"Errore nella sintesi vocale: {e}")