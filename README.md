# delhi-waterlogging-prediction-rf
Dynamic waterlogging prediction system for Delhi using a Hybrid Random Forest model and live weather APIs.
# Real-Time Waterlogging Prediction System

## Overview
This project features a dynamic, real-time prediction system developed to forecast localized waterlogging probabilities for Delhi. It was built by integrating historical climate data with live environmental metrics to create a highly accurate, predictive geographical model.

## Key Features
* **Live Data Fusion:** Fetches live weather metrics dynamically via API and fuses them with historical climate datasets for the target region.
* **Predictive Modeling:** Deploys a hybrid Random Forest model to analyze these complex environmental inputs and output real-time waterlogging probabilities.

## Tech Stack
* **Language:** Python
* **Machine Learning:** scikit-learn (Random Forest Classifier)
* **Data Processing:** Pandas, API Integration (REST)

## Configuration & Execution
1. Clone the repository and install requirements.
2. **Environment Variables:** Rename `.env.example` to `.env` and insert your weather API key.
   ```text
   WEATHER_API_KEY=your_api_key_here
