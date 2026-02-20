const express = require("express");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const axios = require("axios");

require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 5000;
const SECRET = "supersecretkey";

// Dummy hospital staff account
const USER = {
  email: "admin@hospital.com",
  password: "password123"
};

// Login route
app.post("/api/login", (req, res) => {
  const { email, password } = req.body;

  if (email === USER.email && password === USER.password) {
    const token = jwt.sign({ email }, SECRET, { expiresIn: "1h" });
    return res.json({ token });
  }

  return res.status(401).json({ message: "Invalid credentials" });
});

// Token middleware
function verifyToken(req, res, next) {
  const header = req.headers.authorization;

  if (!header) return res.status(403).json({ message: "No token provided" });

  const token = header.split(" ")[1];

  jwt.verify(token, SECRET, (err, decoded) => {
    if (err) return res.status(401).json({ message: "Invalid token" });
    req.user = decoded;
    next();
  });
}

// Secure prediction route
app.post("/api/predict", async (req, res) => {
  console.log("Received request at /api/predict");
  console.log("Body:", req.body);

  try {
    const response = await axios.post(
      "http://localhost:8000/predict",
      req.body,
      { headers: { "Content-Type": "application/json" } }
    );

    console.log("Response from FastAPI:", response.data);
    res.json(response.data);

  } catch (error) {
    console.log("ERROR FROM FASTAPI:");
    console.log(error.response?.data || error.message);
    res.status(500).json({ error: error.response?.data || error.message });
  }
});



app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
