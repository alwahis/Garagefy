// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8099';

export default API_BASE_URL;
