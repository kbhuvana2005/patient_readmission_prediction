import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./routes/Login.jsx";
import PatientDetails from "./routes/PatientDetails.jsx";
import MedicalDetails from "./routes/MedicalDetails.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/patient-details" element={<PatientDetails />} />
        <Route path="/medical-details" element={<MedicalDetails />} />
      </Routes>
    </BrowserRouter>
  );
}
