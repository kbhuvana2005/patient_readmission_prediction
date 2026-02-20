import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const diagnosisOptions = [
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
];

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [dob, setDob] = useState("");
  const [admissionDate, setAdmissionDate] = useState("");
  const [dischargeDate, setDischargeDate] = useState("");

  const [formData, setFormData] = useState({
    LengthOfStay: "",
    PreviousAdmissions: "",
    PatientAge: "",
    PatientGender: "",
    DiagnosisChapter: "",
    NumLabs: "",
    hemoglobin_avg: "",
    glucose_avg: "",
    creatinine_avg: "",
    wbc_avg: ""
  });

  const [result, setResult] = useState(null);

  const calculateAge = (dob) => {
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) age--;
    return age;
  };

  const calculateLOS = (admit, discharge) => {
    const a = new Date(admit);
    const d = new Date(discharge);
    const diff = (d - a) / (1000 * 60 * 60 * 24);
    return diff >= 0 ? diff : 0;
  };

  useEffect(() => {
    if (dob) {
      setFormData((prev) => ({
        ...prev,
        PatientAge: calculateAge(dob)
      }));
    }
  }, [dob]);

  useEffect(() => {
    if (admissionDate && dischargeDate) {
      setFormData((prev) => ({
        ...prev,
        LengthOfStay: calculateLOS(admissionDate, dischargeDate)
      }));
    }
  }, [admissionDate, dischargeDate]);

  const login = async () => {
    try {
      const res = await axios.post("http://localhost:5000/api/login", {
        email,
        password
      });
      localStorage.setItem("token", res.data.token);
      setToken(res.data.token);
    } catch {
      alert("Login failed");
    }
  };

  const predict = async () => {
    try {
      const diagnosisMap = {
        "I - Infectious diseases": "A",
        "II - Neoplasms": "B",
        "III - Blood/immune disorders": "C",
        "IV - Endocrine/nutritional/metabolic": "D",
        "V - Mental disorders": "E",
        "VI - Nervous system": "F",
        "VII - Eye disorders": "G",
        "VIII - Ear disorders": "H",
        "IX - Circulatory system": "I",
        "X - Respiratory system": "J",
        "XI - Digestive system": "K",
        "XII - Skin disorders": "M",
        "XIII - Musculoskeletal system": "N",
        "XIV - Genitourinary system": "O",
        "XV - Pregnancy/childbirth": "P",
        "XVI - Perinatal conditions": "Q",
        "XVII - Congenital abnormalities": "R",
        "XVIII - Symptoms/signs": "T",
        "XIX - Injury/poisoning": "Z"
      };

      // Ensure all numeric fields are numbers and empty fields become 0
      const payload = {
        ...formData,
        LengthOfStay: Number(formData.LengthOfStay) || 0,
        PreviousAdmissions: Number(formData.PreviousAdmissions) || 0,
        PatientAge: Number(formData.PatientAge) || 0,
        NumLabs: Number(formData.NumLabs) || 0,
        hemoglobin_avg: Number(formData.hemoglobin_avg) || 0,
        glucose_avg: Number(formData.glucose_avg) || 0,
        creatinine_avg: Number(formData.creatinine_avg) || 0,
        wbc_avg: Number(formData.wbc_avg) || 0,
        DiagnosisChapter: diagnosisMap[formData.DiagnosisChapter] || ""
      };

      const res = await axios.post(
        "http://localhost:5000/api/predict",
        payload
      );
      setResult(res.data);

    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Prediction failed");
    }
  };

  const [errors, setErrors] = useState({});

  const validateLabs = (name, value) => {
    let message = "";

    const val = Number(value);

    if (name === "hemoglobin_avg") {
      if (val < 0 || val > 30) message = "Out of physiological range";
    }

    if (name === "glucose_avg") {
      if (val < 0 || val > 800) message = "Out of physiological range";
    }

    if (name === "creatinine_avg") {
      if (val < 0 || val > 30) message = "Out of physiological range";
    }

    if (name === "wbc_avg") {
      if (val < 0 || val > 50000) message = "Out of physiological range";
    }

    return message;
  };

  if (!token) {
    return (
      <div className="container">
        <h2>Login</h2>
        <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button onClick={login}>Login</button>
      </div>
    );
  }

  return (
    <div className="page">
    <h1>Patient Readmission Prediction</h1>

    <div className="grid">

      {/* Personal Details */}
      <div className="card">
        <h3>Personal Details</h3>

        <label>Date of Birth</label>
        <input type="date" onChange={(e) => setDob(e.target.value)} />

        <label>Age</label>
        <input value={formData.PatientAge || ""} readOnly />

        <label>Gender</label>
        <select onChange={(e) => setFormData({ ...formData, PatientGender: e.target.value })}>
          <option value="">Select</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>

      {/* Admission Details */}
      <div className="card">
        <h3>Admission Details</h3>

        <label>Admission Date</label>
        <input type="date" onChange={(e) => setAdmissionDate(e.target.value)} />

        <label>Discharge Date</label>
        <input type="date" onChange={(e) => setDischargeDate(e.target.value)} />

        <label>Length of Stay (days)</label>
        <input value={formData.LengthOfStay || ""} readOnly />

        <label>Previous Admissions</label>
        <input type="number" onChange={(e) => setFormData({ ...formData, PreviousAdmissions: Number(e.target.value) })} />

        <label>Diagnosis Chapter</label>
        <select
          value={formData.DiagnosisChapter}
          onChange={(e) => setFormData({ ...formData, DiagnosisChapter: e.target.value })}
        >
          <option value="">Select Chapter</option>
          {diagnosisOptions.map((option, index) => (
            <option key={index} value={option}>{option}</option>
          ))}
        </select>
      </div>

      {/* Lab Parameters */}
      <div className="card">
        <h3>Lab Parameters</h3>

        {["hemoglobin_avg","glucose_avg","creatinine_avg","wbc_avg"].map((lab) => (
          <div key={lab}>
            <label>{lab.replace("_avg","").replace("_"," ").toUpperCase()}</label>
            <input
              type="number"
              className={errors[lab] ? "input-error" : ""}
              onChange={(e) => {
                const value = e.target.value ? Number(e.target.value) : 0;
                setFormData({ ...formData, [lab]: value });

                const errorMsg = validateLabs(lab, value);
                setErrors(prev => ({ ...prev, [lab]: errorMsg }));
              }}
            />
            {errors[lab] && <div className="error-text">{errors[lab]}</div>}
          </div>
        ))}
      </div>

    </div>

    <div className="predict-section">
      <button onClick={predict}>Predict</button>
    </div>

    {result && (
      <div className="modal-overlay">
        <div className="modal-card">
          <button className="close-btn" onClick={() => setResult(null)}>×</button>
          <h3>Prediction Result</h3>
          <div className="result-row">
            <span>Readmission Risk:</span>
            <span>{result.readmission_probability.toFixed(1)}%</span>
          </div>
          <div className="result-row">
            <span>Not Readmitted Probability:</span>
            <span>{result.not_readmitted_probability.toFixed(1)}%</span>
          </div>
          <div className="result-row">
            <span>Prediction:</span>
            <span>{result.prediction === 1 ? "Readmitted" : "Not Readmitted"}</span>
          </div>
          <div className="result-row">
            <span>Confidence:</span>
            <span>{result.confidence.toFixed(1)}%</span>
          </div>

          {/* Dummy medical workflow button */}
          <button
            className="doctor-btn"
            onClick={() => alert("This would send the result for doctor review")}
          >
            Send to Doctor for Review
          </button>
        </div>
      </div>
    )}
  </div>
  );
}

export default App;
