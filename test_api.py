import requests
import json

url = 'http://localhost:5000/api/predict-location'
data = {'lat': 28.6139, 'lon': 77.2090}  # Minto Bridge

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
