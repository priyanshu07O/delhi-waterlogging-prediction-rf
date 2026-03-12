from prediction.real_time_predictor import RealTimePredictor
from pathlib import Path

p = RealTimePredictor(Path('config/config.yaml'))
weather = p.fetch_current_weather(28.6139, 77.2090)

print("Current Weather Data:")
print(f"  Rainfall (1h): {weather['rain_1h']} mm")
print(f"  Rainfall (3h): {weather['rain_3h']} mm")
print(f"  Temperature: {weather['temp']}°C")
print(f"  Humidity: {weather['humidity']}%")
print(f"  Pressure: {weather['pressure']} hPa")

print("\nTesting prediction for Minto Bridge:")
result = p.predict_location(28.6139, 77.2090)
print(f"  Probability: {result['probability']*100:.1f}%")
print(f"  Risk Level: {result['risk_level']}")
