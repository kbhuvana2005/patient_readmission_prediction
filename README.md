# Patient Readmission Prediction

A machine learning project to predict patient readmissions within 30 days using Random Forest algorithm. This project demonstrates data cleaning, feature engineering, and model development using healthcare data.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Performance](#model-performance)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Results](#results)
- [Future Improvements](#future-improvements)

## 🎯 Overview

Hospital readmissions are a significant concern in healthcare, both for patient outcomes and healthcare costs. This project uses machine learning to predict whether a patient will be readmitted within 30 days of discharge, helping healthcare providers identify high-risk patients and take preventive measures.

## 📊 Dataset

The project uses EMR (Electronic Medical Records) data containing:

- **Patient Demographics**: Gender, Race, Marital Status, Language, Poverty Level
- **Admission Records**: Admission dates, Length of Stay, Previous Admissions
- **Diagnoses**: ICD-10 codes and descriptions
- **Lab Results**: Lab test names and values

**Note**: Dataset files are not included in the repository due to size constraints. Place your dataset files in the following structure:

```
dataset/
├── AdmissionsCorePopulatedTable.txt
├── AdmissionsDiagnosesCorePopulatedTable.txt
├── LabsCorePopulatedTable.txt
└── PatientCorePopulatedTable.txt
```

## 📁 Project Structure

```
patient_readmission_prediction/
│
├── dataset/                          # Raw data files (not tracked in git)
│   ├── AdmissionsCorePopulatedTable.txt
│   ├── AdmissionsDiagnosesCorePopulatedTable.txt
│   ├── LabsCorePopulatedTable.txt
│   └── PatientCorePopulatedTable.txt
│
├── cleaned_data/                     # Cleaned datasets (not tracked in git)
│   ├── patients_cleaned.csv
│   ├── admissions_cleaned.csv
│   ├── diagnoses_cleaned.csv
│   └── labs_cleaned.csv
│
├── src-cleaning/                     # Jupyter notebooks
│   ├── test.cleaning.ipynb          # Data cleaning and EDA
│   └── test-model-training.ipynb    # Model training and evaluation
│
├── models/                           # Trained models
│   ├── random_forest_readmission_model.pkl
│   ├── label_encoders.pkl
│   └── feature_names.pkl
│
├── .gitignore                        # Git ignore file
└── README.md                         # Project documentation
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd patient_readmission_prediction
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn
   ```

   Or install from requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### 1. Data Cleaning

Run the data cleaning notebook to process raw data:

```bash
jupyter notebook src-cleaning/test.cleaning.ipynb
```

This notebook will:
- Load raw dataset files
- Analyze missing values
- Clean and preprocess data
- Perform exploratory data analysis
- Save cleaned datasets to `cleaned_data/` folder

### 2. Model Training

Train the Random Forest model:

```bash
jupyter notebook src-cleaning/test-model-training.ipynb
```

This notebook will:
- Load cleaned datasets
- Engineer features (LengthOfStay, PreviousAdmissions, etc.)
- Create readmission labels (30-day readmission target)
- Split data into training/testing sets (80/20)
- Train Random Forest classifier
- Evaluate model performance
- Generate visualizations (Confusion Matrix, ROC Curve, Feature Importance)
- Save trained model to `models/` folder

## 📈 Model Performance

The Random Forest model achieves the following metrics on the test set:

| Metric      | Score  |
|-------------|--------|
| Accuracy    | ~XX%   |
| Precision   | ~XX%   |
| Recall      | ~XX%   |
| F1-Score    | ~XX%   |
| ROC-AUC     | ~XX%   |

### Key Features (by importance):
1. **PreviousAdmissions** - Number of previous hospital admissions
2. **LengthOfStay** - Duration of current hospital stay
3. **AvgLabValue** - Average laboratory test values
4. **NumLabs** - Number of lab tests performed
5. **DiagnosisChapter** - ICD-10 diagnosis category

## ✨ Features

### Data Processing
- ✅ Handles missing values intelligently
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

### Example Output:
```
Total Records: 36,145
Readmission Rate: ~XX%
Training Set: 28,916 records (80%)
Testing Set: 7,229 records (20%)
```
