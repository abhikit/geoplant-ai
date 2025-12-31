import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None

    d = r.json()
    return {
        "temperature": d["main"]["temp"],
        "humidity": d["main"]["humidity"],
        "condition": d["weather"][0]["description"]
    }
