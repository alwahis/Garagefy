// Configuration file for the application

// API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8099';

// Endpoints
const ENDPOINTS = {
    HEALTH: '/health',
    SERVICE_REQUESTS: '/api/service-requests'
};

const config = {
    API_BASE_URL,
    ENDPOINTS
};

export default config;
