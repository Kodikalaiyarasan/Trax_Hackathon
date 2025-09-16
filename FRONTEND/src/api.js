import axios from "axios";

// 👇 change this if backend is deployed elsewhere
const API_BASE = "http://localhost:8000";

export async function uploadSchedule(file) {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${API_BASE}/schedule/upload_csv`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export async function ingestRealtime(data) {
  return axios.post(`${API_BASE}/realtime/ingest`, data);
}

export async function setPriority(train_number, priority) {
  return axios.post(`${API_BASE}/realtime/priority`, { train_number, priority });
}

export async function getRecommendations() {
  const res = await axios.post(`${API_BASE}/ai/optimize`, {});
  return res.data;
}

export async function getPredictions() {
  const res = await axios.get(`${API_BASE}/ai/predictions`);
  return res.data;
}
