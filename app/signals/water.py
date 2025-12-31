def infer_water_stress(temp, humidity):
    if temp > 35 and humidity < 30:
        return "High water stress"
    if humidity > 80:
        return "Risk of overwatering"
    return "Normal conditions"
