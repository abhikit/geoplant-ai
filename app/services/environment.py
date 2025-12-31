from app.signals.weather import get_weather
from app.signals.air_quality import get_air_quality
from app.signals.soil import get_soil_profile
from app.signals.water import infer_water_stress

def get_environmental_context(lat, lon):
    weather = get_weather(lat, lon)
    air = get_air_quality(lat, lon)
    soil = get_soil_profile(lat, lon)

    water_stress = (
        infer_water_stress(weather["temperature"], weather["humidity"])
        if weather else "Unknown"
    )

    return {
        "weather": weather,
        "air_quality": air,
        "soil": soil,
        "water_stress": water_stress
    }
