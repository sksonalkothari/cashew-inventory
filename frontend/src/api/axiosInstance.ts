import axios from "axios";
import { BASE_URL } from "../constants/apiRoutes";
import { getToken, clearToken } from "./auth";
import { toast } from "react-toastify";

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Inject token into every request
axiosInstance.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

// Handle expired session globally
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      toast.error("Session expired, please login again");
      clearToken(); // remove token from storage
      // 👇 Let ProtectedRoute handle redirect automatically
      window.location.href = "/auth/login";
      return Promise.resolve(); // 👈 prevent throwing into ErrorBoundary
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
