from Speech import speak
from Listen import main as rt
from Listen import setup_mic
from llm import Chat

def main():
    setup_mic()
    chat = Chat()
    speak("In cosa posso essere utile Mare?")
    while True:
        user_input = rt()
        if user_input is None:
            continue

        if "esci" in user_input or "quit" in user_input:
            speak("Ok, chiudo l'assistente. A presto!")
            break

        risposta = chat.send_message(user_input)
        print(f"[ASSISTENTE]: {risposta}")
        speak(risposta)

if __name__ == "__main__":
    main()