import axios from 'axios';

// Create axios instance with default config
export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1', // Default to localhost if not set
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor for authentication if needed
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle specific error cases here
        if (error.response?.status === 401) {
            // Handle unauthorized access
            localStorage.removeItem('token');
        }
        return Promise.reject(error);
    }
);