# Patient Readmission Prediction - Web UI

A user-friendly web application for predicting 30-day hospital readmission risk using machine learning.

## 🌟 Features

- **Interactive Web Interface**: Easy-to-use form for entering patient details
- **Real-time Predictions**: Instant readmission risk assessment
- **Visual Analytics**: Clear visualization of prediction results and confidence levels
- **Risk Stratification**: Automated classification into high/low risk categories
- **Clinical Recommendations**: Actionable insights based on risk level
- **Feature Importance**: Understanding which factors contribute most to the prediction

## 📋 Requirements

- Python 3.8 or higher
- Trained model files (located in `../models/`)
  - `random_forest_readmission_model.pkl`
  - `label_encoders.pkl`
  - `feature_names.pkl`

## 🚀 Installation

1. **Navigate to the UI directory**:
   ```bash
   cd ui
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Starting the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.

### Using the Application

1. **Enter Patient Details**:
   - Fill in the admission details (dates, previous admissions)
   - Provide patient demographics (gender, race, marital status, etc.)
   - Enter clinical information (diagnosis, lab results)

2. **Get Prediction**:
   - Click the "Predict Readmission Risk" button
   - View the prediction results in the "Prediction Results" tab

3. **Review Results**:
   - Risk level (High/Low)
   - Probability percentage
   - Clinical recommendations
   - Feature importance analysis

## 📊 Input Fields

### Admission Details
- **Admission Date**: Date of hospital admission
- **Discharge Date**: Date of hospital discharge
- **Previous Admissions**: Number of prior hospital admissions

### Patient Demographics
- **Gender**: Male, Female, or Other
- **Race/Ethnicity**: Patient's racial/ethnic background
- **Marital Status**: Single, Married, Divorced, etc.
- **Primary Language**: Patient's primary language
- **Population Below Poverty**: Socioeconomic indicator

### Clinical Information
- **Diagnosis Chapter**: Primary diagnosis category (ICD classification)
- **Number of Lab Tests**: Total lab tests performed
- **Average Lab Value**: Average of all lab test results

## 🎯 Model Performance

- **Accuracy**: ~72%
- **ROC-AUC**: ~0.72
- **Trained on**: 36,143 hospital admissions
- **Features**: 10 clinical and demographic variables

## 🏗️ Application Structure

```
ui/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Custom Styling
The application includes custom CSS for:
- Color-coded risk indicators (red for high risk, green for low risk)
- Responsive layout
- Professional medical theme

### Model Integration
The app automatically loads model artifacts from the parent `models/` directory:
- Random Forest model
- Label encoders for categorical variables
- Feature names for consistency

## 📱 Tabs Overview

### 1. Patient Details
- Input form for all required patient information
- Real-time validation
- Calculated fields (e.g., length of stay)

### 2. Prediction Results
- Risk level indicator
- Probability scores
- Clinical recommendations
- Feature importance chart
- Patient summary

### 3. Model Information
- Model details and configuration
- Performance metrics
- Feature descriptions
- Disclaimer and usage guidelines

## ⚠️ Important Notes

- **Clinical Use**: This tool assists healthcare professionals but should not replace clinical judgment
- **Data Privacy**: Ensure patient data is handled according to HIPAA and local regulations
- **Model Updates**: Regularly retrain the model with new data for optimal performance
- **Unknown Categories**: The app handles unknown categorical values gracefully

## 🐛 Troubleshooting

### Model Not Found
```
Error loading model artifacts
```
**Solution**: Ensure the `models/` directory exists in the parent folder and contains all required `.pkl` files.

### Dependency Issues
```
ImportError: No module named 'streamlit'
```
**Solution**: Install all dependencies using `pip install -r requirements.txt`

### Port Already in Use
```
Address already in use
```
**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

## 🔄 Future Enhancements

- [ ] Batch prediction for multiple patients
- [ ] Export prediction reports as PDF
- [ ] Integration with EHR systems
- [ ] Historical trend analysis
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Real-time model performance monitoring

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main project README
3. Ensure all model files are properly trained and saved

## 📄 License

This application is part of the Patient Readmission Prediction project.

---

**Built with ❤️ using Streamlit and Scikit-learn**
