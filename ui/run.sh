#!/bin/bash

# Patient Readmission Prediction - UI Launch Script

echo "======================================"
echo "Patient Readmission Prediction Web UI"
echo "======================================"
echo ""

# Navigate to UI directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if model files exist
if [ ! -f "../models/random_forest_readmission_model.pkl" ]; then
    echo ""
    echo "⚠️  WARNING: Model files not found!"
    echo "Please ensure you have trained the model first by running:"
    echo "  ../src-cleaning/test-model-training.ipynb"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Launch Streamlit app
echo ""
echo "Launching web application..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo "======================================"
echo ""

streamlit run app.py
