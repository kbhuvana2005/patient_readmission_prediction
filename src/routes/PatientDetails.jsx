import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  MenuItem,
  Grid
} from "@mui/material";

export default function PatientDetails() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    age: "",
    sex: "",
    dob: "",
    address: "",
    email_id: "",
    phone_no: "",
    guardian_name: "",
    guardian_phone_no: "",
    guardian_relation: ""
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validate = () => {
    const newErrors = {};

    if (!form.name) newErrors.name = "Name is required";
    if (!form.age || form.age <= 0) newErrors.age = "Valid age required";
    if (!form.sex) newErrors.sex = "Select sex";
    if (!form.dob) newErrors.dob = "DOB required";
    if (!form.phone_no || form.phone_no.length !== 10)
      newErrors.phone_no = "Enter valid 10-digit phone number";
    if (form.email_id && !/\S+@\S+\.\S+/.test(form.email_id))
      newErrors.email_id = "Invalid email";

    if (!form.guardian_name) newErrors.guardian_name = "Guardian name required";
    if (!form.guardian_relation)
      newErrors.guardian_relation = "Relation required";
    if (!form.guardian_phone_no || form.guardian_phone_no.length !== 10)
      newErrors.guardian_phone_no = "Valid phone required";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (!validate()) return;
    navigate("/medical-details", { state: { patientData: form } });
  };

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f5f5f5" }}>
      {/* Page header */}
      <Box sx={{ bgcolor: "#1976d2", py: 2, px: 3 }}>
        <Typography variant="h4" sx={{ color: "#fff" }}>
          Patient Details
        </Typography>
      </Box>

      <Box sx={{ display: "flex", justifyContent: "center", px: 2, py: 4 }}>
        <Paper sx={{ width: "100%", maxWidth: 900, p: 4 }}>
          <Grid container spacing={4}>
            {/* Patient column */}
            <Grid item xs={12} md={6}>
              <Typography
                variant="h6"
                sx={{ color: "#1976d2", mb: 2 }}
              >
                Patient Information
              </Typography>

              <TextField fullWidth label="Name" name="name" value={form.name} onChange={handleChange} error={!!errors.name} helperText={errors.name} sx={{ mb: 2 }} />
              <TextField fullWidth label="Age" name="age" type="number" value={form.age} onChange={handleChange} error={!!errors.age} helperText={errors.age} sx={{ mb: 2 }} />
              <TextField fullWidth select label="Sex" name="sex" value={form.sex} onChange={handleChange} error={!!errors.sex} helperText={errors.sex} sx={{ mb: 2 }}>
                <MenuItem value="Male">Male</MenuItem>
                <MenuItem value="Female">Female</MenuItem>
                <MenuItem value="Other">Other</MenuItem>
              </TextField>
              <TextField fullWidth type="date" label="Date of Birth" name="dob" InputLabelProps={{ shrink: true }} value={form.dob} onChange={handleChange} error={!!errors.dob} helperText={errors.dob} sx={{ mb: 2 }} />
              <TextField fullWidth label="Address" name="address" value={form.address} onChange={handleChange} sx={{ mb: 2 }} />
              <TextField fullWidth label="Email ID" name="email_id" value={form.email_id} onChange={handleChange} error={!!errors.email_id} helperText={errors.email_id} sx={{ mb: 2 }} />
              <TextField fullWidth label="Phone No" name="phone_no" value={form.phone_no} onChange={handleChange} error={!!errors.phone_no} helperText={errors.phone_no} />
            </Grid>

            {/* Guardian column */}
            <Grid item xs={12} md={6}>
              <Typography
                variant="h6"
                sx={{ color: "#1976d2", mb: 2 }}
              >
                Guardian Information
              </Typography>

              <TextField fullWidth label="Guardian Name" name="guardian_name" value={form.guardian_name} onChange={handleChange} error={!!errors.guardian_name} helperText={errors.guardian_name} sx={{ mb: 2 }} />
              <TextField fullWidth label="Relation to Patient" name="guardian_relation" value={form.guardian_relation} onChange={handleChange} error={!!errors.guardian_relation} helperText={errors.guardian_relation} sx={{ mb: 2 }} />
              <TextField fullWidth label="Guardian Phone No" name="guardian_phone_no" value={form.guardian_phone_no} onChange={handleChange} error={!!errors.guardian_phone_no} helperText={errors.guardian_phone_no} />
            </Grid>
          </Grid>

          <Box mt={4}>
            <Button variant="contained" fullWidth onClick={handleNext}>
              Next: Medical Details
            </Button>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
}
