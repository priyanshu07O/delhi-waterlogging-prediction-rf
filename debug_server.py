import requests

try:
    # Test homepage
    resp = requests.get('http://localhost:5000/')
    print(f"Homepage: {resp.status_code}")
    
    # Test API again
    resp = requests.post('http://localhost:5000/api/predict-location', json={'lat': 28.6, 'lon': 77.2})
    print(f"API: {resp.status_code}")
    print(resp.text[:200])
except Exception as e:
    print(f"Error: {e}")
