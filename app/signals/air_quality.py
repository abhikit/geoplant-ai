import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# -----------------------------
# PM2.5 → AQI calculation
# -----------------------------
def calculate_aqi_pm25(pm25):
    breakpoints = [
        (0.0, 12.0, 0, 50, "Good"),
        (12.1, 35.4, 51, 100, "Moderate"),
        (35.5, 55.4, 101, 150, "Unhealthy for Sensitive Groups"),
        (55.5, 150.4, 151, 200, "Unhealthy"),
        (150.5, 250.4, 201, 300, "Very Unhealthy"),
        (250.5, 500.4, 301, 500, "Hazardous"),
    ]

    for bp_low, bp_high, aqi_low, aqi_high, category in breakpoints:
        if bp_low <= pm25 <= bp_high:
            aqi = ((aqi_high - aqi_low) / (bp_high - bp_low)) * (pm25 - bp_low) + aqi_low
            return int(round(aqi)), category

    return None, "Unknown"


def get_air_quality(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    components = data["list"][0]["components"]

    pm25 = components.get("pm2_5")
    pm10 = components.get("pm10")

    aqi_value, category = calculate_aqi_pm25(pm25)

    return {
        "aqi": aqi_value,                 # REAL AQI (0–500)
        "category": category,
        "pm2_5": pm25,
        "pm10": pm10
    }
