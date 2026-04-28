import axios from 'axios';

const LOCAL_API_URL = 'http://localhost:5000/api';
const DEFAULT_PRODUCTION_API_URL = 'https://careertrust-backend.onrender.com/api';

const resolveApiBaseUrl = () => {
  const runtimeConfigUrl =
    typeof window !== 'undefined' && window.__CAREER_TRUST_API_URL__
      ? window.__CAREER_TRUST_API_URL__
      : '';

  const envUrl = process.env.REACT_APP_API_URL || runtimeConfigUrl;
  if (envUrl) {
    return envUrl.replace(/\/$/, '');
  }

  if (typeof window !== 'undefined') {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return LOCAL_API_URL;
    }

    return DEFAULT_PRODUCTION_API_URL;
  }

  return DEFAULT_PRODUCTION_API_URL;
};

const API_BASE_URL = resolveApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use((config) => {
  // Let the browser set the multipart boundary for file uploads.
  if (typeof FormData !== 'undefined' && config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle expired/invalid sessions globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    const message = (
      error?.response?.data?.msg ||
      error?.response?.data?.error ||
      ''
    ).toLowerCase();

    const isAuthFailure =
      status === 401 ||
      message.includes('token') ||
      message.includes('authorization') ||
      message.includes('jwt');

    if (isAuthFailure) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;
