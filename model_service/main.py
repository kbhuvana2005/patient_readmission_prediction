from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI()

# Load model artifacts
BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "random_forest_readmission_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "label_encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)

with open(os.path.join(BASE_DIR, "feature_names.pkl"), "rb") as f:
    feature_names = pickle.load(f)


class PatientInput(BaseModel):
    LengthOfStay: int
    PreviousAdmissions: int
    PatientAge: int
    PatientGender: str
    DiagnosisChapter: str
    NumLabs: int
    hemoglobin_avg: float
    glucose_avg: float
    creatinine_avg: float
    wbc_avg: float


@app.post("/predict")
def predict(data: PatientInput):
    try:
        df = pd.DataFrame([data.dict()])

        print("Incoming data:", df)

        for col in ['PatientGender', 'DiagnosisChapter']:
            if col in encoders:
                print(f"Encoding {col}:", df[col].values)
                df[col] = encoders[col].transform(df[col])

        print("After encoding:", df)

        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0]

        return {
            "prediction": int(prediction),
            "readmission_probability": float(proba[1] * 100),
            "not_readmitted_probability": float(proba[0] * 100),
            "confidence": float(max(proba) * 100)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
