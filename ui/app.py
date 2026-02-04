"""
Patient Readmission Prediction - Web UI
A Streamlit-based web application for predicting 30-day hospital readmission risk
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Patient Readmission Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        padding-bottom: 30px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    .high-risk {
        background-color: #ffcccc;
        border: 2px solid #ff0000;
    }
    .low-risk {
        background-color: #ccffcc;
        border: 2px solid #00cc00;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load model and encoders
@st.cache_resource
def load_model_artifacts():
    """Load the trained model, encoders, and feature names"""
    try:
        models_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        
        # Load model
        with open(os.path.join(models_path, 'random_forest_readmission_model.pkl'), 'rb') as f:
            model = pickle.load(f)
        
        # Load label encoders
        with open(os.path.join(models_path, 'label_encoders.pkl'), 'rb') as f:
            encoders = pickle.load(f)
        
        # Load feature names
        with open(os.path.join(models_path, 'feature_names.pkl'), 'rb') as f:
            feature_names = pickle.load(f)
        
        return model, encoders, feature_names
    except Exception as e:
        st.error(f"Error loading model artifacts: {str(e)}")
        return None, None, None

# Initialize model
model, encoders, feature_names = load_model_artifacts()

# Header
st.markdown('<div class="main-header">🏥 Patient Readmission Risk Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Predict the likelihood of patient readmission within 30 days</div>', unsafe_allow_html=True)

# Sidebar - Information
with st.sidebar:
    st.header("ℹ️ About")
    st.info(
        """
        This application uses a Random Forest machine learning model 
        to predict the risk of hospital readmission within 30 days.
        
        **Model Performance:**
        - Accuracy: ~72%
        - ROC-AUC: ~0.72
        - Trained on 36,000+ hospital admissions
        
        **Required Information:**
        - Patient demographics
        - Current admission details
        - Diagnosis information
        - Laboratory test results
        """
    )
    
    st.header("📊 Model Features")
    st.write("""
    The model considers:
    - Length of hospital stay
    - Previous admission history
    - Patient demographics
    - Diagnosis category
    - Lab test results
    """)

# Check if model loaded successfully
if model is None:
    st.error("⚠️ Failed to load the model. Please ensure model files are in the 'models' directory.")
    st.stop()

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Patient Details", "🔮 Prediction Results", "📈 Model Information"])

with tab1:
    st.header("Enter Patient Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏥 Admission Details")
        
        admission_date = st.date_input(
            "Admission Date",
            value=datetime.now() - timedelta(days=3),
            max_value=datetime.now()
        )
        
        discharge_date = st.date_input(
            "Discharge Date",
            value=datetime.now(),
            min_value=admission_date,
            max_value=datetime.now()
        )
        
        # Calculate length of stay
        length_of_stay = (discharge_date - admission_date).days
        if length_of_stay < 0:
            length_of_stay = 0
        
        st.metric("Length of Stay (days)", length_of_stay)
        
        previous_admissions = st.number_input(
            "Number of Previous Admissions",
            min_value=0,
            max_value=50,
            value=0,
            help="Total number of previous hospital admissions"
        )
    
    with col2:
        st.subheader("👤 Patient Demographics")
        
        gender = st.selectbox(
            "Gender",
            options=["Male", "Female", "Other"],
            help="Patient's gender"
        )
        
        race = st.selectbox(
            "Race/Ethnicity",
            options=[
                "Caucasian",
                "African American",
                "Hispanic",
                "Asian",
                "Native American",
                "Other",
                "Unknown"
            ]
        )
        
        marital_status = st.selectbox(
            "Marital Status",
            options=["Single", "Married", "Divorced", "Widowed", "Separated", "Unknown"]
        )
        
        language = st.selectbox(
            "Primary Language",
            options=["English", "Spanish", "Chinese", "Other", "Unknown"]
        )
        
        poverty_percentage = st.slider(
            "Population Below Poverty (%)",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
            step=0.5,
            help="Percentage of population below poverty line in patient's area"
        )
    
    with col3:
        st.subheader("🔬 Clinical Information")
        
        diagnosis_chapter = st.selectbox(
            "Primary Diagnosis Chapter (ICD)",
            options=[
                "I - Infectious diseases",
                "II - Neoplasms",
                "III - Blood/immune disorders",
                "IV - Endocrine/nutritional/metabolic",
                "V - Mental disorders",
                "VI - Nervous system",
                "VII - Eye disorders",
                "VIII - Ear disorders",
                "IX - Circulatory system",
                "X - Respiratory system",
                "XI - Digestive system",
                "XII - Skin disorders",
                "XIII - Musculoskeletal system",
                "XIV - Genitourinary system",
                "XV - Pregnancy/childbirth",
                "XVI - Perinatal conditions",
                "XVII - Congenital abnormalities",
                "XVIII - Symptoms/signs/abnormal findings",
                "XIX - Injury/poisoning",
                "XX - External causes",
                "XXI - Health status factors"
            ],
            help="Primary diagnosis category based on ICD classification"
        )
        
        num_labs = st.number_input(
            "Number of Lab Tests",
            min_value=0,
            max_value=500,
            value=10,
            help="Total number of laboratory tests performed during admission"
        )
        
        avg_lab_value = st.number_input(
            "Average Lab Value",
            min_value=0.0,
            max_value=1000.0,
            value=100.0,
            step=1.0,
            help="Average of all lab test results (normalized)"
        )
    
    # Prediction button
    st.markdown("---")
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        predict_button = st.button("🔮 Predict Readmission Risk", type="primary", use_container_width=True)

with tab2:
    if predict_button:
        # Prepare input data
        try:
            # Create input dataframe
            input_data = pd.DataFrame({
                'LengthOfStay': [length_of_stay],
                'PreviousAdmissions': [previous_admissions],
                'PatientGender': [gender],
                'PatientRace': [race],
                'PatientMaritalStatus': [marital_status],
                'PatientLanguage': [language],
                'PatientPopulationPercentageBelowPoverty': [poverty_percentage],
                'DiagnosisChapter': [diagnosis_chapter],
                'NumLabs': [num_labs],
                'AvgLabValue': [avg_lab_value]
            })
            
            # Encode categorical variables
            categorical_cols = ['PatientGender', 'PatientRace', 'PatientMaritalStatus', 
                              'PatientLanguage', 'DiagnosisChapter']
            
            for col in categorical_cols:
                if col in encoders:
                    try:
                        # Handle unknown categories
                        input_data[col] = encoders[col].transform(input_data[col].astype(str))
                    except:
                        # If category not in encoder, use most common (0)
                        input_data[col] = 0
                        st.warning(f"Unknown value for {col}, using default encoding")
            
            # Make prediction
            prediction = model.predict(input_data)[0]
            prediction_proba = model.predict_proba(input_data)[0]
            
            # Display results
            st.header("Prediction Results")
            
            # Risk assessment
            readmission_probability = prediction_proba[1] * 100
            
            if prediction == 1:
                st.markdown(f'''
                    <div class="prediction-box high-risk">
                        <h2>⚠️ HIGH RISK</h2>
                        <h1>{readmission_probability:.1f}%</h1>
                        <p style="font-size: 1.2rem;">Probability of readmission within 30 days</p>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.error("""
                    **⚠️ Patient at High Risk of Readmission**
                    
                    Consider the following interventions:
                    - Enhanced discharge planning
                    - Close follow-up appointments
                    - Home health services
                    - Medication reconciliation
                    - Patient education on warning signs
                    - Social work consultation
                """)
            else:
                st.markdown(f'''
                    <div class="prediction-box low-risk">
                        <h2>✅ LOW RISK</h2>
                        <h1>{readmission_probability:.1f}%</h1>
                        <p style="font-size: 1.2rem;">Probability of readmission within 30 days</p>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.success("""
                    **✅ Patient at Low Risk of Readmission**
                    
                    Standard discharge recommendations:
                    - Routine follow-up care
                    - Standard discharge instructions
                    - Prescription management
                    - Primary care physician contact
                """)
            
            # Detailed metrics
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f'''
                    <div class="metric-card">
                        <h3>Not Readmitted</h3>
                        <h2>{prediction_proba[0]*100:.1f}%</h2>
                    </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                    <div class="metric-card">
                        <h3>Readmitted</h3>
                        <h2>{prediction_proba[1]*100:.1f}%</h2>
                    </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                risk_level = "High" if prediction == 1 else "Low"
                st.markdown(f'''
                    <div class="metric-card">
                        <h3>Risk Level</h3>
                        <h2>{risk_level}</h2>
                    </div>
                ''', unsafe_allow_html=True)
            
            # Feature importance for this prediction
            st.markdown("---")
            st.subheader("📊 Key Factors Contributing to Risk")
            
            # Get feature importances from model
            feature_importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            st.bar_chart(feature_importance.set_index('Feature')['Importance'])
            
            # Patient summary
            st.markdown("---")
            st.subheader("📋 Patient Summary")
            
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.write("**Admission Information:**")
                st.write(f"- Length of Stay: {length_of_stay} days")
                st.write(f"- Previous Admissions: {previous_admissions}")
                st.write(f"- Admission Date: {admission_date}")
                st.write(f"- Discharge Date: {discharge_date}")
            
            with summary_col2:
                st.write("**Clinical Information:**")
                st.write(f"- Number of Labs: {num_labs}")
                st.write(f"- Average Lab Value: {avg_lab_value:.2f}")
                st.write(f"- Primary Diagnosis: {diagnosis_chapter}")
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.exception(e)
    else:
        st.info("👈 Please fill in the patient details in the 'Patient Details' tab and click 'Predict Readmission Risk'")

with tab3:
    st.header("📈 Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Details")
        st.write("""
        **Algorithm:** Random Forest Classifier
        
        **Model Configuration:**
        - Number of trees: 100
        - Max depth: 10
        - Class weight: Balanced
        - Random state: 42
        
        **Training Dataset:**
        - Total admissions: 36,143
        - Total patients: 10,002
        - Training split: 80%
        - Testing split: 20%
        """)
    
    with col2:
        st.subheader("Performance Metrics")
        st.write("""
        **Test Set Performance:**
        - Accuracy: ~72%
        - Precision: ~40%
        - Recall: ~72%
        - F1-Score: ~51%
        - ROC-AUC: ~0.72
        
        **Note:** The model is optimized to identify high-risk patients,
        which may result in some false positives to minimize missed cases.
        """)
    
    st.markdown("---")
    st.subheader("Features Used by the Model")
    
    features_df = pd.DataFrame({
        'Feature': [
            'Length of Stay',
            'Previous Admissions',
            'Patient Gender',
            'Patient Race',
            'Marital Status',
            'Primary Language',
            'Population Below Poverty',
            'Diagnosis Chapter',
            'Number of Lab Tests',
            'Average Lab Value'
        ],
        'Description': [
            'Number of days in hospital',
            'Number of prior hospital admissions',
            'Patient\'s gender',
            'Patient\'s race/ethnicity',
            'Patient\'s marital status',
            'Patient\'s primary language',
            'Socioeconomic indicator (%)',
            'Primary diagnosis category (ICD)',
            'Total lab tests performed',
            'Average of all lab results'
        ],
        'Type': [
            'Numeric',
            'Numeric',
            'Categorical',
            'Categorical',
            'Categorical',
            'Categorical',
            'Numeric',
            'Categorical',
            'Numeric',
            'Numeric'
        ]
    })
    
    st.dataframe(features_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("⚠️ Disclaimer")
    st.warning("""
    This prediction tool is designed to assist healthcare professionals in identifying 
    patients at higher risk of readmission. It should not be used as the sole basis 
    for clinical decision-making. Always consider the complete clinical context and 
    use professional judgment when making patient care decisions.
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>Patient Readmission Prediction System | Powered by Machine Learning</p>
        <p>© 2026 | Built with Streamlit and Scikit-learn</p>
    </div>
""", unsafe_allow_html=True)
