import requests
import json
import time

# Wait for server to be ready
time.sleep(2)

print("\n=== Testing /api/current-risks ===")
try:
    resp = requests.get('http://localhost:5000/api/current-risks')
    data = resp.json()
    features = data['features']
    print(f"Total features: {len(features)}")
    
    low_risk = [f for f in features if f['properties']['risk_level'] == 'LOW']
    print(f"Low risk features: {len(low_risk)}")
    if len(low_risk) > 0:
        print("Sample low risk:", json.dumps(low_risk[0]['properties'], indent=2))
    else:
        print("WARNING: No low risk features found!")
        
except Exception as e:
    print(f"Error testing current-risks: {e}")

print("\n=== Testing /api/predict-location (Click Simulation) ===")
try:
    # Test a random point
    payload = {'lat': 28.7, 'lon': 77.1}
    resp = requests.post('http://localhost:5000/api/predict-location', json=payload)
    print(f"Status: {resp.status_code}")
    print("Response:", json.dumps(resp.json(), indent=2))
except Exception as e:
    print(f"Error testing predict-location: {e}")
