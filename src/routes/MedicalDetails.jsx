import React, { useState, useMemo } from "react";
import { useLocation } from "react-router-dom";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  MenuItem,
  Stack,
  Card,
  CardContent,
  Divider,
  Chip,
  Alert
} from "@mui/material";
import { predictReadmission } from "../services/predictionService";

export default function MedicalDetails() {
  const location = useLocation();
  const patientData = location.state?.patientData || {};

  const [form, setForm] = useState({
    abnormal_blood_test_result: "",
    hb_level: "",
    sugar_level: "",
    previous_admissions: "",
    chronic_disease_count: "",
    major_illness: "",
    bmi: "",
    history_of_sugar: "",
    length_of_stay: "",
    icu_stay: ""
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sentForReview, setSentForReview] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  /** ---------- Validation ---------- */
  const isFormValid = useMemo(() => {
    const requiredFields = [
      "abnormal_blood_test_result",
      "hb_level",
      "sugar_level",
      "previous_admissions",
      "bmi",
      "length_of_stay"
    ];

    return requiredFields.every(
      (field) => form[field] !== "" && form[field] !== null
    );
  }, [form]);

  /** ---------- Prediction ---------- */
  const handlePredict = async () => {
    setLoading(true);
    setSentForReview(false);
    try {
      const result = await predictReadmission({
        ...patientData,
        ...form
      });
      setPrediction(result);
    } catch (err) {
      console.error("Prediction failed:", err);
    }
    setLoading(false);
  };

  /** ---------- Risk logic ---------- */
  const getRiskLabel = (confidence) => {
    if (confidence > 0.85)
      return { label: "High Risk", color: "error" };
    if (confidence >= 0.75)
      return { label: "Medium Risk", color: "warning" };
    return { label: "Low Risk", color: "success" };
  };

  /** ---------- Review simulation ---------- */
  const handleSendForReview = () => {
    setSentForReview(true);
  };

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f5f5f5" }}>
      {/* Page Header */}
      <Box sx={{ bgcolor: "#1976d2", py: 2.5, px: 3 }}>
        <Typography variant="h4" sx={{ color: "#fff", fontWeight: 500 }}>
          Readmission Prediction
        </Typography>
      </Box>

      <Box sx={{ display: "flex", justifyContent: "center", px: 2, py: 4 }}>
        <Paper elevation={3} sx={{ width: "100%", maxWidth: 650, p: 4 }}>
          <Stack spacing={3}>
            {/* Medical History */}
            <Typography variant="h6" sx={{ color: "#1976d2" }}>
              Medical History
            </Typography>

            <TextField
              fullWidth
              label="Previous Admissions"
              name="previous_admissions"
              type="number"
              value={form.previous_admissions}
              onChange={handleChange}
            />

            <TextField
              fullWidth
              label="Chronic Disease Count"
              name="chronic_disease_count"
              type="number"
              value={form.chronic_disease_count}
              onChange={handleChange}
            />

            <TextField
              fullWidth
              label="Major Illness"
              name="major_illness"
              value={form.major_illness}
              onChange={handleChange}
            />

            <TextField
              fullWidth
              select
              label="History of Sugar"
              name="history_of_sugar"
              value={form.history_of_sugar}
              onChange={handleChange}
            >
              <MenuItem value="Yes">Yes</MenuItem>
              <MenuItem value="No">No</MenuItem>
            </TextField>

            <Divider />

            {/* Current Medical Record */}
            <Typography variant="h6" sx={{ color: "#1976d2" }}>
              Current Medical Record
            </Typography>

            <TextField
              fullWidth
              select
              label="Abnormal Blood Test Result"
              name="abnormal_blood_test_result"
              value={form.abnormal_blood_test_result}
              onChange={handleChange}
              required
            >
              <MenuItem value="Yes">Yes</MenuItem>
              <MenuItem value="No">No</MenuItem>
            </TextField>

            <TextField
              fullWidth
              label="HB Level"
              name="hb_level"
              type="number"
              value={form.hb_level}
              onChange={handleChange}
              required
            />

            <TextField
              fullWidth
              label="Sugar Level"
              name="sugar_level"
              type="number"
              value={form.sugar_level}
              onChange={handleChange}
              required
            />

            <TextField
              fullWidth
              label="BMI"
              name="bmi"
              type="number"
              value={form.bmi}
              onChange={handleChange}
              required
            />

            <TextField
              fullWidth
              label="Length of Stay (days)"
              name="length_of_stay"
              type="number"
              value={form.length_of_stay}
              onChange={handleChange}
              required
            />

            <TextField
              fullWidth
              label="ICU Stay (days)"
              name="icu_stay"
              type="number"
              value={form.icu_stay}
              onChange={handleChange}
            />

            {/* Predict Button */}
            <Button
              variant="contained"
              fullWidth
              disabled={!isFormValid || loading}
              onClick={handlePredict}
            >
              {loading ? "Predicting..." : "Predict Readmission"}
            </Button>

            {/* Result */}
            {prediction && (
              <Card sx={{ bgcolor: "#e3f2fd" }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Prediction Result
                  </Typography>

                  <Typography>
                    Will Readmit: <b>{prediction.predicted}</b>
                  </Typography>

                  <Typography sx={{ mb: 2 }}>
                    Confidence: <b>{prediction.confidence}</b>
                  </Typography>

                  {/* Risk Label – full width, subtle rounding */}
                  <Chip
                    label={getRiskLabel(prediction.confidence).label}
                    color={getRiskLabel(prediction.confidence).color}
                    sx={{
                      width: "100%",
                      borderRadius: 1,
                      fontSize: "1rem",
                      py: 2
                    }}
                  />

                  {/* Send for review */}
                  <Button
                    variant="outlined"
                    fullWidth
                    sx={{ mt: 2 }}
                    onClick={handleSendForReview}
                  >
                    Send for Doctor Review
                  </Button>

                  {sentForReview && (
                    <Alert severity="success" sx={{ mt: 2 }}>
                      Patient data and prediction sent for doctor review.
                    </Alert>
                  )}
                </CardContent>
              </Card>
            )}
          </Stack>
        </Paper>
      </Box>
    </Box>
  );
}
