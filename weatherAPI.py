import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_coordinates(city, api_key):
    """Obtenir latitude et longitude d'une ville."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(geo_url)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"Erreur : Impossible de trouver les coordonnées pour la ville '{city}'.")
    return data[0]["lat"], data[0]["lon"]

def get_weather(lat, lon, api_key):
    """Obtenir la météo via OneCall API."""
    # Teste avec OneCall 2.5 si 3.0 ne fonctionne pas
    weather_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=fr"
    response = requests.get(weather_url)
    response.raise_for_status()
    data = response.json()

    # Extraire les données principales
    current_temp = data["current"]["temp"]
    description = data["current"]["weather"][0]["description"]
    print(f"Actuellement, il fait {current_temp}°C avec {description}.")

def main():
    api_key = os.getenv("WEATHERAPI")
    if not api_key:
        print("Erreur : Clé API introuvable.")
        return

    try:
        city = input("Entrez le nom de la ville : ")
        lat, lon = get_coordinates(city, api_key)
        get_weather(lat, lon, api_key)
    except ValueError as ve:
        print(ve)
    except requests.exceptions.HTTPError as e:
        print(f"Erreur API : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
