@echo off
REM Patient Readmission Prediction - UI Launch Script (Windows)

echo ======================================
echo Patient Readmission Prediction Web UI
echo ======================================
echo.

REM Navigate to UI directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo Dependencies installed
echo.

REM Check if model files exist
if not exist "..\models\random_forest_readmission_model.pkl" (
    echo.
    echo WARNING: Model files not found!
    echo Please ensure you have trained the model first by running:
    echo   ..\src-cleaning\test-model-training.ipynb
    echo.
    pause
)

REM Launch Streamlit app
echo.
echo Launching web application...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo ======================================
echo.

streamlit run app.py
