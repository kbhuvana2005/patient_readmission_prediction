import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Paper, Typography, TextField, Button } from "@mui/material";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = () => {
    navigate("/patient-details");
  };

  return (
    <Box
      sx={{
        height: "100svh",         // <--- use small viewport height unit
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        bgcolor: "#f5f5f5",
        px: 2,
      }}
    >
      <Paper
        elevation={3}
        sx={{
          width: "100%",
          maxWidth: 400,
          p: 4,
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        <Typography variant="h5" gutterBottom>
          Hospital Staff Login
        </Typography>

        <TextField
          fullWidth
          label="Email"
          name="email"
          value={form.email}
          onChange={handleChange}
          type="email"
          variant="outlined"
        />

        <TextField
          fullWidth
          label="Password"
          name="password"
          value={form.password}
          onChange={handleChange}
          type="password"
          variant="outlined"
        />

        <Button
          variant="contained"
          fullWidth
          onClick={handleLogin}
          sx={{ mt: 2 }}
        >
          Login
        </Button>
      </Paper>
    </Box>
  );
}
