// src/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "https://task-tracker-backend-271k.onrender.com", // Deployed FastAPI backend
});


// Attach token if available
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export default API;
