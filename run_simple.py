import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

print("="*60)
print("TESTING MAIN.PY")
print("="*60)

try:
    print("Step 1: Importing modules...")
    from pathlib import Path
    import yaml
    
    print("Step 2: Loading config...")
    config_path = Path('config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    print(f"  API Key present: {bool(config['api_keys']['openweathermap'])}")
    
    print("Step 3: Checking directories...")
    from models.model_trainer import HybridModelTrainer
    
    model_dir = Path('models/saved_models')
    model_file = model_dir / 'ensemble_model.pkl'
    print(f"  Model file exists: {model_file.exists()}")
    
    if not model_file.exists():
        print("\nStep 4: Training model (this will take 2-3 minutes)...")
        config_path_full = Path('config/config.yaml')
        trainer = HybridModelTrainer(config_path_full)
        results = trainer.train_and_evaluate()
        print(f"\nModel training complete!")
        print(f"  Accuracy: {results['accuracy']:.3f}")
    else:
        print("\n  Model already exists, skipping training")
    
    print("\nStep 5: Starting web server...")
    print("  Server will start on http://localhost:5000")
    print("  Open your browser to that URL")
    print("  Press Ctrl+C to stop the server")
    print("="*60)
    
    from web.app import app
    app.run(host='0.0.0.0', port=5000, debug=False)
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user")
except Exception as e:
    print(f"\n\nERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
