from Speech import speak
from Listen import main as rt
from Listen import setup_mic
from llm import generate_text

def main():
    setup_mic()
    speak("How can i help ya mare?")
    while True:
        user_input = rt()
        if user_input is None:
            continue

        if "esci" in user_input or "chiudi" in user_input:
            speak("Ok, chiudo l'assistente. A presto!")
            break

        risposta = generate_text(user_input)
        print(f"[ASSISTENTE]: {risposta}")
        speak(risposta)

if __name__ == "__main__":
    main()