import requests

def resolve_location(city=None, lat=None, lon=None):
    if city:
        # Forward geocoding
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "GeoPlantAI"}
        )
        data = r.json()[0]
        return {
            "city": city,
            "lat": float(data["lat"]),
            "lon": float(data["lon"])
        }

    if lat is not None and lon is not None:
        # Reverse geocoding
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "GeoPlantAI"}
        )
        data = r.json()
        return {
            "city": data.get("address", {}).get("city", "Unknown"),
            "lat": float(lat),
            "lon": float(lon)
        }

    raise ValueError("Location not provided")
