# Patient Readmission Prediction

A machine learning system to predict 30-day hospital readmissions using clinical data.

## Overview

This project helps healthcare providers identify patients at high risk of readmission within 30 days. It uses a Random Forest model trained on EMR data with clinically meaningful features.

## Project Structure

```
patient_readmission_prediction/
├── dataset/                    # Raw EMR data files
├── cleaned_data/               # Processed data
├── src-cleaning/               # Jupyter notebooks
│   ├── data-cleaning.ipynb    # Data preprocessing
│   └── model-training.ipynb   # Model training with balanced dataset
├── models/                     # Trained model files
└── ui/                         # Streamlit web application
    └── app.py
```

## How to Use

### 1. Clean Data
```bash
jupyter notebook src-cleaning/data-cleaning.ipynb
```

### 2. Train Model
```bash
jupyter notebook src-cleaning/model-training.ipynb
```

### 3. Run Web UI
```bash
cd ui
./run.sh
```
Access at: `http://localhost:8501`

## Model Features (10 Clinical Predictors)

1. **LengthOfStay** - Hospital stay duration
2. **PreviousAdmissions** - Admission history
3. **PatientAge** - Age-related risk
4. **PatientGender** - Gender-specific conditions
5. **DiagnosisChapter** - ICD-10 diagnosis category
6. **NumLabs** - Lab test intensity
7. **Hemoglobin** - Anemia indicator (g/dL)
8. **Glucose** - Diabetes control (mg/dL)
9. **Creatinine** - Kidney function (mg/dL)
10. **WBC Count** - Infection marker (k/cumm)

## Key Improvements

- Uses individual lab values (not averaged)
- Balanced dataset (131 readmitted + 200 healthy cases)
- Only clinically relevant features
- Professional web interface for predictions
- ✅ Converts categorical variables using Label Encoding
- ✅ Aggregates lab data per admission
- ✅ Creates time-based features (days to next admission)

### Model Features
- ✅ Random Forest with 100 trees
- ✅ Balanced class weights to handle imbalanced data
- ✅ Stratified train-test split
- ✅ Comprehensive evaluation metrics

### Visualizations
- 📊 Confusion Matrix
- 📈 ROC Curve
- 🎯 Feature Importance Bar Chart
- 📉 Patient Demographics Analysis

## 🛠️ Technologies Used

- **Python 3.8+** - Programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning library
- **Matplotlib & Seaborn** - Data visualization
- **Jupyter Notebook** - Interactive development environment

## 📊 Results

The model successfully identifies patients at risk of readmission with:
- High precision to minimize false positives
- Good recall to capture most readmission cases
- Robust ROC-AUC score indicating strong discriminative ability
Training Details:
```
Dataset: Balanced with 131 readmitted + 200 healthy cases
Total Training Records: ~331 cases
Readmission Rate: ~40% (balanced)
Features: 10 clinically meaningful predictors
Model: Random Forest with 100 trees
```

### Key Improvements from v1.0:
- ✅ Removed non-medical features (poverty, race, marital status)
- ✅ Replaced meaningless "average lab value" with specific labs
- ✅ Balanced dataset for better prediction accuracy
- ✅ Industry-standard professional UI with Plotly charts
- ✅ Medical-grade risk stratification (High/Moderate/Low)ting Set: 7,229 records (20%)
```
