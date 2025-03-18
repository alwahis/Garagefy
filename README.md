# Garagefy - AI-Powered Car Diagnostic System

Garagefy is an intelligent car diagnostic system that uses AI models to analyze car issues and provide accurate diagnostics based on manufacturer service manuals and expert knowledge.

## Features
- AI-powered car diagnostics using DeepSeek AI
- Technical diagnosis based on manufacturer service manuals and documentation
- Detailed diagnostic reports including:
  - Severity assessment
  - Problem analysis with likely causes
  - Diagnostic steps with required tools
  - Repair recommendations
  - Safety implications
  - Technical references to service manuals
- Location-based garage finder
- Comprehensive car brand and model database
- User-friendly interface built with React and Chakra UI

## Quick Start
To run the application locally, use the provided start script:

```bash
# Make the script executable
chmod +x start_local.sh

# Run the application
./start_local.sh
```

This will start both the backend and frontend servers in a tmux session.

## Manual Setup
If you prefer to set up and run components individually:

### Backend
```bash
# Setup Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the backend
python main.py
```

### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the frontend
npm start
```

## API Usage
The backend provides various API endpoints:

- Car diagnostics: `POST /api/diagnose`
- Garage finder: `GET /api/garages`
- Car data: `GET /api/brands`, `GET /api/models/{brand}`, `GET /api/years/{brand}/{model}`

## Dependencies
- Python 3.8+
- Node.js 14+
- Various AI APIs (configured in .env file)

## License
MIT License
