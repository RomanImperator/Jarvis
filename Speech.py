import edge_tts
import os
import pygame
import tempfile
import time
import asyncio

# Edge TTS Voice Configuration
VOICE = 'it-IT-MarcelloMultilingualNeural'

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

async def _generate_speech(text: str, output_file: str):
    """
    Generates speech audio using Edge TTS asynchronously.
    
    Args:
        text (str): Text to convert to speech.
        output_file (str): Path to save the audio file.
    """
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def speak(text: str):
    """
    Converts text to speech and plays it immediately.
    Handles temporary file creation and cleanup.
    
    Args:
        text (str): The text to speak.
    """
    temp_file = None
    try:
        # Create a temporary file for the audio
        fd, temp_file = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)  # Close the file descriptor immediately

        # Generate audio
        asyncio.run(_generate_speech(text, temp_file))
        
        # Play audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play() 
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Stop and unload to release the file lock
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    except PermissionError as e:
        print(f"[ERROR] Permission denied in TTS: {e}")
    except Exception as e:
        print(f"[ERROR] TTS Error: {e}")
    finally:
        # Ensure temporary file is always deleted
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as cleanup_error:
                print(f"[WARNING] Could not delete temp file {temp_file}: {cleanup_error}")