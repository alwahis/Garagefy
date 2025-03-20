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

## Environment Variables
The application uses environment variables for configuration. A template file `.env.example` is provided.

1. Copy the example file to create your own `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholder values with your actual API keys and configuration:
   - `GOOGLE_API_KEY`: Required for geocoding and maps functionality
   - `DEEPSEEK_API_KEY`: Used for AI-powered diagnostics
   - `OPENAI_API_KEY`: Alternative AI provider

**IMPORTANT: Never commit your `.env` file to version control. It contains sensitive information.**

## Security

- API keys and sensitive credentials should be stored in the `.env` file
- The `.env` file is excluded from version control via `.gitignore`
- Always rotate API keys if you suspect they have been compromised
- Use environment-specific settings for development, testing, and production

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
