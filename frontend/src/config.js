const config = {
    API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8099',
    ENDPOINTS: {
        HEALTH: '/health',
        DIAGNOSE: '/api/diagnose',
        CAR_DATA: '/api/car-data',
        GARAGES: '/api/garages',
        TEST: '/api/test'
    }
};

export default config;
