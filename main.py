from Speech import speak
from Listen import listen_continuous, setup_mic
from llm import Chat
from Video import Camera
from Vision import Vision

def main():
    """
    Main function to run the Jarvis assistant.
    Handles initialization, voice interaction loop, and visual intent processing.
    """
    # Initialize microphone for background noise
    setup_mic()
    
    # Initialize the LLM Chat interface
    chat = Chat()
    
    # Initialize Vision capabilities (Camera and Vision model)
    try:
        vision = Vision()
        camera = Camera()
        print("[SYSTEM] Vision system ready.")
    except Exception as e:
        print(f"[ERROR] Vision initialization failed: {e}")
        vision = None
        camera = None

    # Greeting
    speak("In cosa posso essere utile Mare?")
    
    # Main Interaction Loop
    while True:
        # Listen for user input (blocking until a phrase is detected)
        user_input = listen_continuous()
        
        # If no valid input detected, continue listening
        if user_input is None:
            continue

        # Exit command check
        if "esci" in user_input or "quit" in user_input:
            speak("Ok, chiudo l'assistente. A presto!")
            if camera:
                camera.release()
            break

        # Visual Intent Check
        # If the user asks to see something, capture an image and describe it
        if vision and camera and chat.check_visual_intent(user_input):
            print("[INFO] Visual request detected. Capturing image...")
            speak("Dammi un secondo che guardo...")
            
            frame = camera.capture_frame()
            
            if frame:
                description = vision.describe(frame)
                print(f"[VISION]: {description}")
                
                # Enrich the prompt for the LLM with the visual description
                # Note: We append this system note to the user's input so the LLM knows what it 'sees'
                user_input += f"\n\n[SYSTEM NOTE]: The user asked you to look. Here is what the camera sees: {description}"
            else:
                speak("Non riesco ad accedere alla telecamera.")

        # Generate and speak response
        response = chat.send_message(user_input)
        print(f"[ASSISTANT]: {response}")
        speak(response)

if __name__ == "__main__":
    main()