# Patient Readmission Prediction System

A machine learning system to predict whether the discharging patient will be readmitted or not.

## Project Structure

```

v5/
├── frontend/         # React client
├── backend/          # Node.js API server
├── model_service/    # FastAPI ML service
└── README.md

```

## How to use

### 1. Running the ML API

cd model_service
python -m venv venv
venv\Scripts\activate        # Windows

pip install -r requirements.txt
uvicorn main:app --reload

### 2. Backend

cd backend
npm install
node server.js

### 3. Frontend

cd frontend
npm install
npm start

### You need all three terminals running simultaneously

