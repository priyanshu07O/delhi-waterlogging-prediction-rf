import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import xgboost as xgb
import os

def train_and_save_models():
    print("="*60)
    print("  TRAINING ENSEMBLE MODELS (RF + XGBoost)")
    print("="*60)

    # 1. Setup Directories
    base_dir = Path(__file__).parent
    data_path = base_dir / 'data' / 'processed' / 'training_data.csv'
    models_dir = base_dir / 'models' / 'saved_models'
    models_dir.mkdir(parents=True, exist_ok=True)

    # 2. Load or Create Data
    if data_path.exists():
        print(f"Loading real data from {data_path}...")
        df = pd.read_csv(data_path)
        # Assuming 'waterlogged' is the target and others are features
        X = df.drop('waterlogged', axis=1).select_dtypes(include=[np.number])
        y = df['waterlogged']
    else:
        print("Warning: 'training_data.csv' not found.")
        print("Generating SYNTHETIC data for demonstration/initialization...")
        
        # Generate robust synthetic data for waterlogging
        np.random.seed(42)
        n_samples = 2000
        
        data = {
            'rainfall_current': np.random.gamma(shape=2, scale=10, size=n_samples), # Skewed rainfall
            'rainfall_3h': np.random.gamma(shape=3, scale=15, size=n_samples),
            'elevation': np.random.normal(210, 10, n_samples),
            'dist_drain': np.random.uniform(0, 5000, n_samples),
            'humidity': np.random.uniform(30, 95, n_samples)
        }
        X = pd.DataFrame(data)
        
        # Logic: High rain + Low elevation + Far from drain = Waterlogging (1)
        risk_score = (
            (X['rainfall_current'] / 20) * 0.4 + 
            (X['rainfall_3h'] / 30) * 0.3 + 
            ((250 - X['elevation']) / 50) * 0.3 +
            (X['dist_drain'] / 5000) * 0.1
        )
        y = (risk_score > 1.2).astype(int)
        
        # Save feature names for the predictor to use later
        feature_names = list(X.columns)
        print(f"Features used: {feature_names}")

    # 3. Preprocessing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Train Random Forest
    print("\nTraining Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    rf_acc = accuracy_score(y_test, rf_model.predict(X_test_scaled))
    print(f" - Random Forest Accuracy: {rf_acc:.4f}")

    # 5. Train XGBoost
    print("\nTraining XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    xgb_model.fit(X_train_scaled, y_train)
    xgb_acc = accuracy_score(y_test, xgb_model.predict(X_test_scaled))
    print(f" - XGBoost Accuracy: {xgb_acc:.4f}")

    # 6. Save Everything
    print("\nSaving models to 'models/saved_models/'...")
    
    joblib.dump(rf_model, models_dir / 'rf_model.pkl')
    print(f" [Saved] rf_model.pkl")
    
    joblib.dump(xgb_model, models_dir / 'xgb_model.pkl')
    print(f" [Saved] xgb_model.pkl")
    
    joblib.dump(scaler, models_dir / 'scaler.pkl')
    print(f" [Saved] scaler.pkl")
    
    joblib.dump(list(X.columns), models_dir / 'feature_names.pkl')
    print(f" [Saved] feature_names.pkl")

    print("\nDONE! You can now run main.py")

if __name__ == "__main__":
    try:
        train_and_save_models()
    except ImportError as e:
        print(f"\nERROR: Missing Library. {e}")
        print("Please run: pip install xgboost scikit-learn pandas joblib")