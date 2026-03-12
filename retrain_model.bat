@echo off
echo ===================================================
echo   DELHI WATERLOGGING MODEL - RETRAINING PIPELINE
echo ===================================================
echo.

echo 1. Generating Training Data (Real Historical Events)...
python data/generate_training_data.py
if %errorlevel% neq 0 goto error
echo [OK] Data Generated.
echo.

echo 2. Running Feature Engineering...
python data/feature_engineering.py
if %errorlevel% neq 0 goto error
echo [OK] Features Extracted.
echo.

echo 3. Training Ensemble Model...
python models/model_trainer.py
if %errorlevel% neq 0 goto error
echo [OK] Model Trained Successfully!
echo.

echo ===================================================
echo   RETRAINING COMPLETE!
echo ===================================================
pause
exit /b 0

:error
echo.
echo [ERROR] Pipeline failed! Check the errors above.
pause
exit /b 1
