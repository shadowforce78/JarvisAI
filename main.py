import speech_recognition as sr
import pyttsx3

def talk(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parle, j'écoute 👂...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='fr-FR')
            return command.lower()
        except sr.UnknownValueError:
            return "Je n'ai pas compris."

while True:
    command = listen()
    if "quitter" in command or "au revoir" in command:
        talk("Bye bye !")
        break
    elif "heure" in command:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        talk(f"Il est {now}")
    else:
        talk("Je ne sais pas encore faire ça.")
