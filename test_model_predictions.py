"""
Test what the model predicts WITHOUT the rainfall override
"""
from pathlib import Path
import numpy as np
from prediction.real_time_predictor import RealTimePredictor

config_path = Path('config/config.yaml')
predictor = RealTimePredictor(config_path)

print('\n' + '='*70)
print('TESTING MODEL PREDICTIONS WITHOUT RAINFALL OVERRIDE')
print('='*70)

# Test with 0 rainfall
weather_data_zero = {'temp': 25, 'humidity': 60, 'pressure': 1010, 'rain_1h': 0}
features_dict = predictor.extract_features_for_location(28.6139, 77.2090, weather_data_zero)
feature_array = np.array([[features_dict[fname] for fname in predictor.feature_names]])
feature_scaled = predictor.scaler.transform(feature_array)
probability_zero = predictor.model.predict_proba(feature_scaled)[0, 1]

print(f'\n[Test 1] Minto Bridge with 0mm rainfall:')
print(f'  Rainfall: {weather_data_zero["rain_1h"]} mm')
print(f'  Model raw prediction: {probability_zero:.4f} ({probability_zero*100:.1f}%)')

# Test with 5mm rainfall
weather_data_5mm = {'temp': 25, 'humidity': 80, 'pressure': 1005, 'rain_1h': 5}
features_dict = predictor.extract_features_for_location(28.6139, 77.2090, weather_data_5mm)
feature_array = np.array([[features_dict[fname] for fname in predictor.feature_names]])
feature_scaled = predictor.scaler.transform(feature_array)
probability_5mm = predictor.model.predict_proba(feature_scaled)[0, 1]

print(f'\n[Test 2] Minto Bridge with 5mm rainfall:')
print(f'  Rainfall: {weather_data_5mm["rain_1h"]} mm')
print(f'  Model raw prediction: {probability_5mm:.4f} ({probability_5mm*100:.1f}%)')

# Test with 15mm rainfall
weather_data_15mm = {'temp': 25, 'humidity': 90, 'pressure': 1000, 'rain_1h': 15}
features_dict = predictor.extract_features_for_location(28.6139, 77.2090, weather_data_15mm)
feature_array = np.array([[features_dict[fname] for fname in predictor.feature_names]])
feature_scaled = predictor.scaler.transform(feature_array)
probability_15mm = predictor.model.predict_proba(feature_scaled)[0, 1]

print(f'\n[Test 3] Minto Bridge with 15mm rainfall:')
print(f'  Rainfall: {weather_data_15mm["rain_1h"]} mm')
print(f'  Model raw prediction: {probability_15mm:.4f} ({probability_15mm*100:.1f}%)')

print('\n' + '='*70)
print('KEY FEATURES FOR 0mm RAIN TEST:')
print('='*70)
features_dict = predictor.extract_features_for_location(28.6139, 77.2090, weather_data_zero)
for fname in predictor.feature_names:
    print(f'  {fname:.<35} {features_dict[fname]}')

print('\n' + '='*70)
