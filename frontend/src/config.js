// Configuration file for the application

// API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8099';

// Endpoints
const ENDPOINTS = {
    HEALTH: '/health',
    DIAGNOSE: '/api/diagnose',
    CAR_DATA: '/api/car-data',
    GARAGES: '/api/garages',
    TEST: '/api/test',
    USED_CAR_CHECK: '/api/used-car/check',
    USED_CAR_OPTIONS: '/api/used-car/options'
};

const config = {
    API_BASE_URL,
    ENDPOINTS
};

export default config;
