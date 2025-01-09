import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';  // Default API URL

export const api = axios.create({
    baseURL: `${API_URL}/api/v1`,  // Add /api to the baseURL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
); 