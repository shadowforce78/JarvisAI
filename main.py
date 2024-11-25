import speech_recognition as sr
import pyttsx3
from weatherAPI import get_weather, get_coordinates
import os
import requests

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
    elif "météo" in command:
        api_key = os.getenv("WEATHERAPI")
        if not api_key:
            talk("Erreur : Clé API introuvable.")
            continue

        try:
            words = command.split()
            if "météo" in words:
                city_index = words.index("météo") + 2
                city = " ".join(words[city_index:])
            if not city:
                talk("Je n'ai pas compris le nom de la ville.")
                continue
            lat, lon = get_coordinates(city, api_key)
            talk(get_weather(lat, lon, api_key, city))
        except ValueError as ve:
            talk(ve)
        except requests.exceptions.HTTPError as e:
            talk(f"Erreur API : {e}")
        except Exception as e:
            talk(f"Erreur inattendue : {e}")
    else:
        talk("Je ne sais pas encore faire ça.")
