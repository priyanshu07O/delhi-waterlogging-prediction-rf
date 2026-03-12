"""
Delhi Water Logging Prediction System - Main Entry Point
Simple CLI interface for predicting waterlogging risks
"""

import sys
from pathlib import Path

# Configure UTF-8 encoding for Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except:
    pass

# Add project root to path
sys.path.append(str(Path(__file__).parent))

import yaml
from prediction.real_time_predictor import RealTimePredictor
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime


def print_header(predictor=None):
    """Print application header"""
    print("\n" + "="*70)
    print("  DELHI WATER LOGGING PREDICTION SYSTEM")
    print("="*70)
    print("  Real-time AI-powered waterlogging risk prediction")
    print(f"  Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if predictor and predictor.get_model_update_time():
        print(f"  Model Last Updated: {predictor.get_model_update_time().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_high_risk_areas(predictor, config):
    """Generate and display high-risk areas"""
    print("Analyzing Delhi for waterlogging risks...")
    print("Generating predictions...\n")
    
    # Generate predictions for grid sample
    predictions_df = predictor.predict_grid(sample_size=200)
    
    # Filter high and medium risk areas
    high_risk = predictions_df[predictions_df['risk_level'] == 'HIGH'].sort_values('probability', ascending=False)
    medium_risk = predictions_df[predictions_df['risk_level'] == 'MEDIUM'].sort_values('probability', ascending=False)
    
    # Display HIGH RISK areas
    print("\n" + "="*70)
    print("  HIGH RISK AREAS (>70% probability)")
    print("="*70)
    
    if len(high_risk) > 0:
        print(f"\n{'No.':<5} {'Area Name':<30} {'Latitude':<10} {'Longitude':<10} {'Rain(mm)':<10} {'Risk %':<8}")
        print("-"*85)
        
        geolocator = Nominatim(user_agent="delhi_waterlogging_predictor")
        
        for idx, (_, row) in enumerate(high_risk.iterrows(), 1):
            # Try to find matching known location
            area_name = f"Zone {idx}"
            found_known = False
            for loc in config['prediction']['known_locations']:
                if abs(row['lat'] - loc['lat']) < 0.01 and abs(row['lon'] - loc['lon']) < 0.01:
                    area_name = loc['name']
                    found_known = True
                    break
            
            # If not a known location, reverse geocode
            if not found_known:
                try:
                    location = geolocator.reverse(f"{row['lat']}, {row['lon']}", timeout=2)
                    if location and 'address' in location.raw:
                        address = location.raw['address']
                        # Try to get specific parts of the address
                        area_parts = []
                        if 'suburb' in address: area_parts.append(address['suburb'])
                        if 'neighbourhood' in address: area_parts.append(address['neighbourhood'])
                        if 'road' in address: area_parts.append(address['road'])
                        
                        if area_parts:
                            area_name = ", ".join(area_parts[:2])  # Take first 2 parts
                        elif 'city_district' in address:
                             area_name = address['city_district']
                except (GeocoderTimedOut, GeocoderServiceError):
                    pass
            
            # Truncate area name if too long
            if len(area_name) > 28:
                area_name = area_name[:25] + "..."

            print(f"{idx:<5} {area_name:<30} {row['lat']:<10.4f} {row['lon']:<10.4f} {row['rainfall']:<10.1f} {row['probability']*100:<8.1f}")
    else:
        print("\n  No high-risk areas detected at this time.")
    
    # Display MEDIUM RISK areas
    if len(medium_risk) > 0:
        print("\n" + "="*85)
        print("  MEDIUM RISK AREAS (40-70% probability)")
        print("="*85)
        print(f"\n{'No.':<5} {'Area Name':<30} {'Latitude':<10} {'Longitude':<10} {'Rain(mm)':<10} {'Risk %':<8}")
        print("-"*85)
        
        for idx, (_, row) in enumerate(medium_risk.head(10).iterrows(), 1):
            area_name = f"Zone M{idx}"
            for loc in config['prediction']['known_locations']:
                if abs(row['lat'] - loc['lat']) < 0.01 and abs(row['lon'] - loc['lon']) < 0.01:
                    area_name = loc['name']
                    break
            
            print(f"{idx:<5} {area_name:<30} {row['lat']:<10.4f} {row['lon']:<10.4f} {row['rainfall']:<10.1f} {row['probability']*100:<8.1f}")
    
    # Summary statistics
    total = len(predictions_df)
    high_count = len(high_risk)
    medium_count = len(medium_risk)
    low_count = total - high_count - medium_count
    
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    print(f"  Total locations analyzed: {total}")
    print(f"  High Risk:   {high_count} locations")
    print(f"  Medium Risk: {medium_count} locations")
    print(f"  Low Risk:    {low_count} locations")
    print("="*70 + "\n")


def search_location(predictor, config):
    """Interactive location search"""
    print("\n" + "="*70)
    print("  SEARCH FOR SPECIFIC LOCATION")
    print("="*70)
    
    # Show known locations
    print("\nKnown locations you can search:")
    for idx, loc in enumerate(config['prediction']['known_locations'][:10], 1):
        print(f"  {idx}. {loc['name']}")
    
    print("\nEnter location name (or 'back' to return): ", end='')
    query = input().strip()
    
    if query.lower() == 'back':
        return
    
    # Search in known locations
    found = False
    for loc in config['prediction']['known_locations']:
        if query.lower() in loc['name'].lower():
            print(f"\nSearching for: {loc['name']}...")
            result = predictor.predict_location(loc['lat'], loc['lon'])
            
            # Fetch forecast
            forecast = predictor.fetch_weather_forecast(loc['lat'], loc['lon'])
            
            print("\n" + "-"*70)
            print(f"  Location: {loc['name']}")
            print(f"  Coordinates: {loc['lat']:.4f}°N, {loc['lon']:.4f}°E")
            print(f"  Current Rainfall: {result['rainfall']:.1f} mm")
            print(f"  Waterlogging Probability: {result['probability']*100:.1f}%")
            print(f"  Risk Level: {result['risk_level']}")
            
            # Display forecast
            if forecast:
                print("\n  Rainfall Forecast (Next 12 hours):")
                for i, fc in enumerate(forecast, 1):
                    print(f"    {fc['time']}: {fc['rain']:.1f} mm")
            
            print("-"*70)
            found = True
            break
    
    if not found:
        print(f"\n  Location '{query}' not found in database.")
        print("  Try searching for: Minto Bridge, IP Estate, Pul Prahladpur, etc.")


def main():
    """Main application loop"""
    try:
        # Load configuration
        config_path = Path('config/config.yaml')
        if not config_path.exists():
            print("ERROR: Configuration file not found!")
            print(f"Expected: {config_path.absolute()}")
            return 1
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check if model exists
        model_path = Path('models/saved_models/ensemble_model.pkl')
        if not model_path.exists():
            print("\nERROR: Trained model not found!")
            print("Please run the training pipeline first:")
            print("  python data/feature_engineering.py")
            print("  python models/model_trainer.py")
            return 1
        
        # Initialize predictor
        print("\nInitializing prediction system...")
        predictor = RealTimePredictor(config_path)
        print("[OK] System ready!\n")
        
        while True:
            print_header(predictor)
            
            print("Options:")
            print("  1. Show High-Risk Areas")
            print("  2. Search Specific Location")
            print("  3. Exit")
            print("\nEnter your choice (1-3): ", end='')
            
            choice = input().strip()
            
            if choice == '1':
                print_high_risk_areas(predictor, config)
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                search_location(predictor, config)
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                print("\nThank you for using Delhi Water Logging Prediction System!")
                print("Stay safe during monsoon season!\n")
                break
            
            else:
                print("\nInvalid choice. Please enter 1, 2, or 3.")
                input("Press Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user. Goodbye!")
        return 0
    except FileNotFoundError as e:
        print(f"\n\nERROR: Required file not found: {e}")
        print("\nPlease ensure all data files are present:")
        print("  - data/raw/delhi_grid.csv")
        print("  - data/raw/elevation/grid_elevations.csv")
        print("  - models/saved_models/ensemble_model.pkl")
        return 1
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
