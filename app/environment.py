import requests
from app.utils.logger import logger

def get_environment(lat: float, lon: float, api_key: str):
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    air_url = "https://api.openweathermap.org/data/2.5/air_pollution"

    weather = requests.get(
        weather_url,
        params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    ).json()

    air = requests.get(
        air_url,
        params={"lat": lat, "lon": lon, "appid": api_key}
    ).json()

    temperature = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    pm25 = air["list"][0]["components"]["pm2_5"]

    aqi = int(pm25 * 4)  # approximate real AQI

    logger.info({
        "event": "environment_fetched",
        "temperature": temperature,
        "humidity": humidity,
        "pm25": pm25,
        "aqi": aqi
    })

    return {
        "temperature": temperature,
        "humidity": humidity,
        "aqi": aqi
    }
