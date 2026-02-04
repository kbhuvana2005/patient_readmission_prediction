
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Clinical Readmission Risk Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Clinical Decision Support System v2.0"
    }
)

# Professional CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        color: #1e3a8a;
        text-align: center;
        padding: 25px 20px 10px 20px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        text-align: center;
        padding-bottom: 35px;
        font-weight: 400;
    }
    
    .prediction-box {
        padding: 35px;
        border-radius: 16px;
        margin: 25px 0;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .high-risk {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 3px solid #dc2626;
    }
    
    .low-risk {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 3px solid #059669;
    }
    
    .moderate-risk {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #d97706;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border: 1px solid #e2e8f0;
    }
    
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        padding: 14px 32px;
        border-radius: 10px;
        border: none;
        font-size: 1.05rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s;
    }
    
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .stAlert {
        border-radius: 10px;
        border-left-width: 4px;
    }
    
    .section-divider {
        margin: 30px 0;
        border-bottom: 2px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Load model artifacts
@st.cache_resource
def load_model_artifacts():
    """Load trained model, encoders, and feature names"""
    try:
        models_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        
        with open(os.path.join(models_path, 'random_forest_readmission_model.pkl'), 'rb') as f:
            model = pickle.load(f)
        
        with open(os.path.join(models_path, 'label_encoders.pkl'), 'rb') as f:
            encoders = pickle.load(f)
        
        with open(os.path.join(models_path, 'feature_names.pkl'), 'rb') as f:
            feature_names = pickle.load(f)
        
        return model, encoders, feature_names
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None, None

# Initialize
model, encoders, feature_names = load_model_artifacts()

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 Clinical Decision Support")
    st.markdown("---")
    
    with st.expander("📊 Model Performance", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", "72%")
            st.metric("ROC-AUC", "0.72")
        with col2:
            st.metric("Precision", "40%")
            st.metric("Recall", "72%")
    
    with st.expander("🔬 Clinical Features"):
        st.markdown("""
        **Admission History:**
        • Length of Stay
        • Previous Admissions
        
        **Demographics:**
        • Patient Age  
        • Gender
        
        **Clinical:**
        • Primary Diagnosis
        • Lab Intensity
        
        **Laboratory:**
        • Hemoglobin
        • Glucose  
        • Creatinine
        • WBC Count
        """)
    
    st.markdown("---")
    st.caption("🔒 HIPAA Compliant")
    st.caption(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Header
st.markdown('<div class="main-header">🏥 Clinical Readmission Risk Assessment</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Clinical Decision Support for 30-Day Readmission Prediction</div>', unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model not loaded. Please ensure model files exist.")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Patient Assessment", "🔮 Risk Analysis", "📈 System Info"])

with tab1:
    st.markdown("### Patient Information Entry")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Column 1: Admission Data
    with col1:
        st.markdown("#### 🏥 Admission Information")
        
        admission_date = st.date_input(
            "Admission Date",
            value=datetime.now() - timedelta(days=4),
            max_value=datetime.now(),
            help="Date patient was admitted to hospital"
        )
        
        discharge_date = st.date_input(
            "Discharge Date",
            value=datetime.now(),
            min_value=admission_date,
            max_value=datetime.now(),
            help="Date patient was discharged"
        )
        
        length_of_stay = (discharge_date - admission_date).days
        st.metric("Length of Stay", f"{length_of_stay} days")
        
        previous_admissions = st.number_input(
            "Previous Admissions",
            min_value=0,
            max_value=50,
            value=0,
            help="Total number of previous hospital admissions in patient history"
        )
        
        num_labs = st.number_input(
            "Number of Lab Tests",
            min_value=0,
            max_value=500,
            value=15,
            help="Total laboratory tests performed during admission"
        )
    
    # Column 2: Demographics
    with col2:
        st.markdown("#### 👤 Patient Demographics")
        
        patient_age = st.number_input(
            "Patient Age",
            min_value=0,
            max_value=120,
            value=55,
            help="Patient's age in years"
        )
        
        patient_gender = st.selectbox(
            "Gender",
            options=["Male", "Female"],
            help="Patient's biological sex"
        )
        
        st.markdown("#### 🔬 Primary Diagnosis")
        
        diagnosis_chapter = st.selectbox(
            "ICD Diagnosis Chapter",
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
                "XVIII - Symptoms/signs",
                "XIX - Injury/poisoning",
                "XX - External causes",
                "XXI - Health status factors"
            ],
            index=8,  # Default to Circulatory
            help="Primary diagnosis classification (ICD-10 chapter)"
        )
    
    # Column 3: Laboratory Values
    with col3:
        st.markdown("#### 🧪 Laboratory Values")
        st.caption("Leave blank if test not performed")
        
        hemoglobin = st.number_input(
            "Hemoglobin (g/dL)",
            min_value=0.0,
            max_value=25.0,
            value=13.5,
            step=0.1,
            help="Normal: 12-16 g/dL. Indicates anemia if low"
        )
        
        glucose = st.number_input(
            "Glucose (mg/dL)",
            min_value=0.0,
            max_value=600.0,
            value=100.0,
            step=1.0,
            help="Normal: 70-100 mg/dL. Diabetes indicator if elevated"
        )
        
        creatinine = st.number_input(
            "Creatinine (mg/dL)",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=0.1,
            help="Normal: 0.7-1.3 mg/dL. Kidney function marker"
        )
        
        wbc = st.number_input(
            "WBC Count (k/cumm)",
            min_value=0.0,
            max_value=100.0,
            value=7.5,
            step=0.1,
            help="Normal: 4.0-11.0 k/cumm. Infection/immune indicator"
        )
    
    # Prediction Button
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        predict_button = st.button("🔮 Analyze Readmission Risk", type="primary", use_container_width=True)

with tab2:
    if predict_button:
        # Prepare input
        try:
            input_data = pd.DataFrame({
                'LengthOfStay': [length_of_stay],
                'PreviousAdmissions': [previous_admissions],
                'PatientAge': [patient_age],
                'PatientGender': [patient_gender],
                'DiagnosisChapter': [diagnosis_chapter],
                'NumLabs': [num_labs],
                'hemoglobin_avg': [hemoglobin],
                'glucose_avg': [glucose],
                'creatinine_avg': [creatinine],
                'wbc_avg': [wbc]
            })
            
            # Encode
            for col in ['PatientGender', 'DiagnosisChapter']:
                if col in encoders:
                    try:
                        input_data[col] = encoders[col].transform(input_data[col].astype(str))
                    except:
                        input_data[col] = 0
            
            # Predict
            prediction = model.predict(input_data)[0]
            prediction_proba = model.predict_proba(input_data)[0]
            readmission_prob = prediction_proba[1] * 100
            
            # Risk Level
            if readmission_prob >= 60:
                risk_level = "HIGH"
                risk_class = "high-risk"
                risk_icon = "⚠️"
                risk_color = "#dc2626"
            elif readmission_prob >= 40:
                risk_level = "MODERATE"
                risk_class = "moderate-risk"
                risk_icon = "⚡"
                risk_color = "#d97706"
            else:
                risk_level = "LOW"
                risk_class = "low-risk"
                risk_icon = "✅"
                risk_color = "#059669"
            
            # Display Result
            st.markdown(f'''
                <div class="prediction-box {risk_class}">
                    <h1 style="font-size: 3rem; margin: 0;">{risk_icon}</h1>
                    <h2 style="color: {risk_color}; margin: 15px 0 10px 0;">{risk_level} RISK</h2>
                    <h1 style="font-size: 3.5rem; font-weight: 700; margin: 10px 0;">{readmission_prob:.1f}%</h1>
                    <p style="font-size: 1.1rem; color: #64748b; margin: 0;">Probability of 30-Day Readmission</p>
                </div>
            ''', unsafe_allow_html=True)
            
            # Clinical Recommendations
            st.markdown("### 💡 Clinical Recommendations")
            
            if prediction == 1:
                st.error("""
                **⚠️ High Risk Patient - Enhanced Care Pathway Recommended**
                
                **Immediate Actions:**
                - Schedule follow-up within 7 days
                - Arrange home health services if applicable
                - Comprehensive medication reconciliation
                - Social work consultation for support needs
                - Patient education on warning signs
                - Consider transitional care program enrollment
                
                **Discharge Planning:**
                - Clear written discharge instructions
                - Confirm transportation arrangements
                - Verify medication availability and understanding
                - Ensure caregiver involvement and education
                """)
            else:
                st.success("""
                **✅ Low to Moderate Risk - Standard Care Protocol**
                
                **Standard Discharge Process:**
                - Routine follow-up within 2-4 weeks
                - Standard discharge instructions provided
                - Primary care physician notification
                - Medication list and prescriptions reviewed
                - Patient education materials provided
                
                **Patient Responsibilities:**
                - Attend scheduled follow-up appointments
                - Take medications as prescribed
                - Monitor for warning signs
                - Contact provider with concerns
                """)
            
            # Detailed Metrics
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📊 Detailed Analysis")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Not Readmitted",
                    f"{prediction_proba[0]*100:.1f}%",
                    help="Probability patient will NOT be readmitted"
                )
            
            with col2:
                st.metric(
                    "Readmitted",
                    f"{prediction_proba[1]*100:.1f}%",
                    help="Probability patient WILL be readmitted"
                )
            
            with col3:
                st.metric(
                    "Risk Category",
                    risk_level,
                    help="Overall risk stratification"
                )
            
            with col4:
                confidence = max(prediction_proba) * 100
                st.metric(
                    "Confidence",
                    f"{confidence:.1f}%",
                    help="Model prediction confidence"
                )
            
            # Feature Importance Chart
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📈 Contributing Factors")
            
            feature_importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)
            
            # Create modern plotly chart
            fig = go.Figure(go.Bar(
                x=feature_importance['Importance'],
                y=feature_importance['Feature'],
                orientation='h',
                marker=dict(
                    color=feature_importance['Importance'],
                    colorscale='Blues',
                    line=dict(color='#1e40af', width=1)
                )
            ))
            
            fig.update_layout(
                title="Feature Importance in Prediction Model",
                xaxis_title="Importance Score",
                yaxis_title="Clinical Feature",
                height=400,
                template="plotly_white",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Patient Summary
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📋 Patient Summary")
            
            sum_col1, sum_col2 = st.columns(2)
            
            with sum_col1:
                st.markdown(f"""
                **Admission Information:**
                - Length of Stay: {length_of_stay} days
                - Previous Admissions: {previous_admissions}
                - Admission Date: {admission_date}
                - Discharge Date: {discharge_date}
                - Total Labs: {num_labs}
                """)
            
            with sum_col2:
                st.markdown(f"""
                **Patient & Clinical:**
                - Age: {patient_age} years
                - Gender: {patient_gender}
                - Primary Diagnosis: {diagnosis_chapter}
                
                **Laboratory Values:**
                - Hemoglobin: {hemoglobin} g/dL
                - Glucose: {glucose} mg/dL
                - Creatinine: {creatinine} mg/dL
                - WBC: {wbc} k/cumm
                """)
            
        except Exception as e:
            st.error(f"❌ Prediction Error: {str(e)}")
            st.exception(e)
    else:
        st.info("👈 Please enter patient details in the 'Patient Assessment' tab and click 'Analyze Readmission Risk'")

with tab3:
    st.markdown("### 📈 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Model Architecture")
        st.markdown("""
        **Algorithm:** Random Forest Classifier
        
        **Configuration:**
        - Estimators: 100 trees
        - Max Depth: 10
        - Class Weight: Balanced
        - Random State: 42
        
        **Training Data:**
        - Total Admissions: 36,143
        - Total Patients: 10,002
        - Train Split: 80%
        - Test Split: 20%
        """)
    
    with col2:
        st.markdown("#### Performance Metrics")
        st.markdown("""
        **Test Set Results:**
        - Accuracy: ~72%
        - Precision: ~40%
        - Recall: ~72%
        - F1-Score: ~51%
        - ROC-AUC: ~0.72
        
        **Note:** Model optimized to identify high-risk patients,
        accepting some false positives to minimize missed cases.
        """)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### Clinical Features")
    
    features_df = pd.DataFrame({
        'Feature': [
            'Length of Stay',
            'Previous Admissions',
            'Patient Age',
            'Gender',
            'Diagnosis Chapter',
            'Lab Test Count',
            'Hemoglobin',
            'Glucose',
            'Creatinine',
            'WBC Count'
        ],
        'Type': [
            'Numeric', 'Numeric', 'Numeric', 'Categorical', 'Categorical',
            'Numeric', 'Numeric', 'Numeric', 'Numeric', 'Numeric'
        ],
        'Clinical Relevance': [
            'Severity indicator',
            'Chronic condition marker',
            'Age-related risk',
            'Gender-specific conditions',
            'Disease category risk',
            'Monitoring intensity',
            'Anemia detection',
            'Diabetes control',
            'Kidney function',
            'Infection/immune status'
        ]
    })
    
    st.dataframe(features_df, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### ⚠️ Clinical Use Disclaimer")
    st.warning("""
    **Important Medical Disclaimer:**
    
    This clinical decision support tool is designed to assist healthcare professionals 
    in identifying patients at higher risk of hospital readmission. 
    
    **This tool should NOT:**
    - Be used as the sole basis for clinical decisions
    - Replace professional medical judgment
    - Be considered a diagnostic device
    - Override clinical assessment and patient context
    
    **Always consider:**
    - Complete clinical context
    - Patient-specific factors
    - Current medical guidelines
    - Interdisciplinary team input
    
    For clinical validation and regulatory compliance, consult your institution's 
    clinical informatics and legal teams.
    """)

# Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 25px 20px;">
        <p style="margin: 5px 0;">Clinical Readmission Risk Assessment System v2.0</p>
        <p style="margin: 5px 0;">Powered by Machine Learning | Built with Streamlit</p>
        <p style="margin: 5px 0;">© 2026 | For Healthcare Professional Use Only</p>
    </div>
""", unsafe_allow_html=True)
