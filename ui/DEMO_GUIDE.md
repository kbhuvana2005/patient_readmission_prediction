# 🏥 Patient Readmission Prediction - Web UI

## Quick Start Guide

### Starting the Application

**Option 1: Using the Launch Script (Recommended)**
```bash
cd ui
./run.sh
```

**Option 2: Manual Setup**
```bash
cd ui

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

---

## 🎯 Example Patient Scenarios for Testing

### Scenario 1: High Risk Patient
**Patient Profile**: Elderly patient with multiple comorbidities

| Field | Value |
|-------|-------|
| **Admission Details** |
| Admission Date | 7 days ago |
| Discharge Date | Today |
| Previous Admissions | 5 |
| **Demographics** |
| Gender | Male |
| Race | Caucasian |
| Marital Status | Widowed |
| Language | English |
| Poverty % | 25.0 |
| **Clinical** |
| Diagnosis | IX - Circulatory system |
| Number of Labs | 45 |
| Average Lab Value | 150.0 |

**Expected Result**: HIGH RISK (60-80% probability)

---

### Scenario 2: Low Risk Patient
**Patient Profile**: Young patient, minor condition

| Field | Value |
|-------|-------|
| **Admission Details** |
| Admission Date | 2 days ago |
| Discharge Date | Today |
| Previous Admissions | 0 |
| **Demographics** |
| Gender | Female |
| Race | Caucasian |
| Marital Status | Single |
| Language | English |
| Poverty % | 10.0 |
| **Clinical** |
| Diagnosis | XIII - Musculoskeletal system |
| Number of Labs | 5 |
| Average Lab Value | 95.0 |

**Expected Result**: LOW RISK (20-40% probability)

---

### Scenario 3: Moderate Risk Patient
**Patient Profile**: Middle-aged with chronic condition

| Field | Value |
|-------|-------|
| **Admission Details** |
| Admission Date | 4 days ago |
| Discharge Date | Today |
| Previous Admissions | 2 |
| **Demographics** |
| Gender | Male |
| Race | African American |
| Marital Status | Married |
| Language | English |
| Poverty % | 18.0 |
| **Clinical** |
| Diagnosis | IV - Endocrine/nutritional/metabolic |
| Number of Labs | 20 |
| Average Lab Value | 120.0 |

**Expected Result**: MODERATE RISK (45-55% probability)

---

## 📱 Application Features

### Tab 1: Patient Details
- **Admission Information**: Dates, length of stay, history
- **Demographics**: Gender, race, language, socioeconomic factors
- **Clinical Data**: Diagnosis category, lab results
- **Auto-calculated fields**: Length of stay

### Tab 2: Prediction Results
- **Risk Level**: High/Low risk indicator
- **Probability Score**: Percentage likelihood of readmission
- **Clinical Recommendations**: Actionable next steps
- **Feature Importance**: Which factors contribute most
- **Patient Summary**: Complete overview

### Tab 3: Model Information
- **Model Details**: Algorithm, configuration, training data
- **Performance Metrics**: Accuracy, precision, recall, etc.
- **Feature Descriptions**: What each input means
- **Disclaimer**: Important usage notes

---

## 🎨 UI Highlights

✅ **Color-coded Risk Indicators**
- 🔴 Red for high risk
- 🟢 Green for low risk

✅ **Real-time Predictions**
- Instant results after clicking predict

✅ **Professional Medical Theme**
- Clean, healthcare-appropriate design

✅ **Responsive Layout**
- Works on desktop and tablet

---

## 🔧 Troubleshooting

### Model Not Found Error
```
Error loading model artifacts
```
**Fix**: Ensure you've run the training notebook first:
```bash
jupyter notebook src-cleaning/test-model-training.ipynb
```

### Port Already in Use
```
Address already in use
```
**Fix**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```
ModuleNotFoundError: No module named 'streamlit'
```
**Fix**: Install requirements:
```bash
pip install -r requirements.txt
```

---

## 📸 Screenshots

The UI includes:
- 📝 **Clean Input Forms** with validation
- 🎯 **Large Risk Indicators** easy to read
- 📊 **Visual Charts** for feature importance
- 💡 **Clinical Guidance** for each prediction
- 📈 **Performance Metrics** for transparency

---

## 🔐 Privacy & Security Notes

⚠️ **Important**: This is a demonstration application. For production use:
- [ ] Implement user authentication
- [ ] Add HIPAA-compliant logging
- [ ] Use encrypted connections (HTTPS)
- [ ] Implement audit trails
- [ ] Add data validation and sanitization
- [ ] Follow healthcare data privacy regulations

---

## 📞 Need Help?

1. Check the main [README.md](../README.md)
2. Review the [UI README](ui/README.md)
3. Ensure model files exist in `models/` directory
4. Verify all dependencies are installed

---

## 🚀 Next Steps

After testing the UI:
1. ✅ Try different patient scenarios
2. ✅ Review feature importance rankings
3. ✅ Compare predictions with actual risk factors
4. ✅ Customize the UI for your needs
5. ✅ Add additional features or visualizations

---

**Built with ❤️ using Streamlit, Scikit-learn, and Python**
