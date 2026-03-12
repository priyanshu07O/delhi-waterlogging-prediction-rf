# Delhi Waterlogging Prediction System - Complete Guide

## 📋 Table of Contents
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Training the Model](#training-the-model)
- [Running the System](#running-the-system)
  - [Terminal Version](#terminal-version)
  - [Web Interface](#web-interface)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB free space
- **Internet**: Required for initial setup and weather data

---

## 📦 Installation

### Step 1: Verify Python Installation
Open Command Prompt and check Python version:
```cmd
python --version
```
If Python is not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Navigate to Project Directory
```cmd
cd C:\Users\Priyanshu\Desktop\ML_project
```

### Step 3: Install Dependencies
```cmd
pip install -r requirements.txt
```

This will install all required packages:
- pandas
- numpy
- scikit-learn
- Flask
- requests
- PyYAML
- and more...

---

## 🎓 Training the Model

### Complete Training Process (From Scratch)

#### Step 1: Generate Training Data
This creates synthetic training data with diverse rainfall scenarios:
```cmd
python data\feature_engineering.py
```

**What it does:**
- Loads waterlogging incidents
- Matches with weather data
- Creates positive samples (waterlogged areas)
- Generates negative samples with varied rainfall
- Extracts features (rainfall, elevation, location, temporal)
- Saves to `data\processed\training_data.csv`

**Expected output:**
```
=== Creating Training Dataset ===
Generating POSITIVE samples (waterlogged)...
  Generated 128 positive samples
  Rainfall stats: mean=12.08mm, median=12.49mm

Generating NEGATIVE samples (non-waterlogged)...
  Generated 154 negative samples
  Rainfall stats: mean=3.66mm, median=3.11mm

[OK] Training dataset created
```

#### Step 2: Train the Model
This trains the Random Forest and Gradient Boosting ensemble:
```cmd
python models\model_trainer.py
```

**What it does:**
- Loads training data
- Splits into train/test sets (80/20)
- Trains Random Forest classifier
- Trains Gradient Boosting classifier
- Combines into ensemble model
- Evaluates performance
- Saves model files to `models\saved_models\`

**Expected output:**
```
============================================================
WATER LOGGING PREDICTION - MODEL TRAINING
============================================================
Loading training data...
[OK] Loaded 282 samples with 20 features

Training Hybrid Ensemble...
Accuracy: 0.9649
AUC-ROC: 1.0000

[OK] Model saved to models\saved_models\ensemble_model.pkl
[OK] MODEL TRAINING COMPLETE
```

**Model files created:**
- `ensemble_model.pkl` - Trained model
- `scaler.pkl` - Feature scaler
- `feature_names.pkl` - Feature list

---

## 🚀 Running the System

### Option 1: Terminal Version (Command Line Interface)

Run the interactive terminal application:
```cmd
python main.py
```

**Features:**
- Interactive menu-driven interface
- Predict waterlogging for specific coordinates
- Predict for known vulnerable areas
- Predict for entire Delhi grid
- Export results to CSV

**Usage Example:**
```
=== DELHI WATERLOGGING PREDICTION SYSTEM ===

1. Predict for specific location (lat, lon)
2. Predict for known vulnerable areas
3. Predict for Delhi grid (sample)
4. Exit

Enter choice: 1
Enter latitude: 28.6139
Enter longitude: 77.2090

Prediction: HIGH RISK
Probability: 74.1%
Rainfall: 2.0mm
```

**To exit:** Press `4` or `Ctrl+C`

---

### Option 2: Web Interface (Interactive Map)

#### Step 1: Start the Web Server
```cmd
python web\app.py
```

**Expected output:**
```
Loading trained model...
[OK] Model loaded successfully
Loading static data...
[OK] Loaded 3752 grid points
Starting web server on 0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

#### Step 2: Open in Browser
Open your web browser and navigate to:
```
http://localhost:5000
```

Or use the local network IP shown in the terminal (e.g., `http://10.234.114.12:5000`)

#### Step 3: Using the Web Interface

**Features:**
1. **Interactive Map**
   - View Delhi map with risk markers
   - Red = High risk (>70%)
   - Yellow = Medium risk (40-70%)
   - Green = Low risk (<40%)

2. **Hover Functionality**
   - Move cursor to see coordinates
   - Hover over markers to see probability instantly

3. **Click to Predict**
   - Click anywhere on map for detailed prediction
   - Shows: Risk level, probability, rainfall, coordinates

4. **High-Risk Areas Panel**
   - Lists top high-risk locations
   - Click to zoom to area

5. **Statistics Panel**
   - Total locations analyzed
   - Count by risk level
   - Last update time

6. **Search Functionality**
   - Search known locations (e.g., "Minto Bridge")
   - View predictions for searched areas

**To stop the server:** Press `Ctrl+C` in the terminal (may need to press twice)

**Browser Hard Refresh:** If changes don't show, press `Ctrl+Shift+R`

---

## 📁 Project Structure

```
ML_project/
├── config/
│   └── config.yaml              # Configuration file
├── data/
│   ├── raw/                     # Raw data files
│   │   ├── incidents/           # Waterlogging incidents
│   │   ├── weather/             # Historical weather data
│   │   └── elevation/           # Elevation data
│   ├── processed/               # Generated training data
│   └── feature_engineering.py   # Data generation script
├── models/
│   ├── saved_models/            # Trained model files
│   │   ├── ensemble_model.pkl
│   │   ├── scaler.pkl
│   │   └── feature_names.pkl
│   └── model_trainer.py         # Training script
├── prediction/
│   └── real_time_predictor.py   # Prediction engine
├── web/
│   ├── app.py                   # Flask web server
│   ├── templates/
│   │   └── index.html           # Web interface
│   └── static/
│       ├── js/main.js           # Frontend logic
│       └── css/style.css        # Styling
├── main.py                      # Terminal interface
├── requirements.txt             # Python dependencies
└── Readme_new.md               # This file
```

---

## 🔧 Troubleshooting

### Model Not Found Error
**Problem:** `FileNotFoundError: Model file not found`

**Solution:** Train the model first:
```cmd
python data\feature_engineering.py
python models\model_trainer.py
```

---

### Web Server Won't Start
**Problem:** `Address already in use` or port 5000 occupied

**Solution 1:** Kill existing Python processes:
```cmd
taskkill /F /IM python.exe
```

**Solution 2:** Change port in `config\config.yaml`:
```yaml
web:
  port: 5001  # Change to different port
```

---

### Import Errors
**Problem:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:** Reinstall dependencies:
```cmd
pip install -r requirements.txt --upgrade
```

---

### Hover Tooltips Not Working
**Problem:** Map doesn't show tooltips on hover

**Solution:**
1. Stop server with `Ctrl+C`
2. Restart: `python web\app.py`
3. Hard refresh browser: `Ctrl+Shift+R`

---

### Low Accuracy or Poor Predictions
**Problem:** Model predictions seem incorrect

**Solution:** Retrain with fresh data:
```cmd
python data\feature_engineering.py
python models\model_trainer.py
```

---

### API Request Timeout
**Problem:** "Analyzing location..." hangs forever

**Solution:** Check server logs for errors. Restart server:
```cmd
# Stop with Ctrl+C
python web\app.py
```

---

## 📊 Understanding the Output

### Risk Levels
- **HIGH RISK (>70%)**: Waterlogging very likely, avoid area
- **MEDIUM RISK (40-70%)**: Moderate chance, exercise caution
- **LOW RISK (<40%)**: Safe conditions

### Key Features Affecting Predictions
1. **Rainfall** - Current and cumulative rainfall
2. **Location** - Proximity to known vulnerable areas
3. **Elevation** - Low-lying areas at higher risk
4. **Season** - Monsoon months (June-September) increase risk

---

## 🔄 Retraining the Model

To retrain with updated or corrected data:

```cmd
# Step 1: Regenerate training data
python data\feature_engineering.py

# Step 2: Train new model
python models\model_trainer.py
```

The new model will automatically replace the old one.

---

## 🆘 Quick Reference

### Quick Start (First Time)
```cmd
cd C:\Users\Priyanshu\Desktop\ML_project
pip install -r requirements.txt
python data\feature_engineering.py
python models\model_trainer.py
python main.py
```

### Quick Start Web Interface
```cmd
cd C:\Users\Priyanshu\Desktop\ML_project
python web\app.py
# Open http://localhost:5000
```

### Retrain Model
```cmd
python data\feature_engineering.py
python models\model_trainer.py
```

---

## 📝 Notes

- **API Key**: The system uses OpenWeatherMap API. Ensure API key is configured in `config\config.yaml`
- **Data Updates**: Weather data is fetched in real-time for predictions
- **Offline Mode**: Terminal predictions work offline if model is trained
- **Performance**: Web interface handles 1000 concurrent predictions efficiently

---

## 👨‍💻 Development

### Model Improvements
- Training data: `data\feature_engineering.py`
- Model architecture: `models\model_trainer.py`
- Prediction logic: `prediction\real_time_predictor.py`

### Web Interface Customization
- Frontend: `web\static\js\main.js`
- Styling: `web\static\css\style.css`
- Backend: `web\app.py`

---

**Last Updated:** 2025-11-26
**Version:** 2.0
**Author:** ML Project Team
