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

---

# Fix It System End-to-End Test Results & Verification

## 1. Customer Form Submission
- ✅ Verified: Customer form submissions are correctly stored in the Baserow Customer details table.
- **How tested:** Submitted a test form. Checked Baserow for new record with expected fields.

## 2. Email Notification to Garages
- ✅ Verified: Email notifications are sent to all garage emails listed in the Fix it Garages Baserow table upon form submission.
- **How tested:** Submitted a form, checked outbox and recipient inboxes for notification emails.

## 3. Garage Reply Capture & VIN Linking
- ✅ Verified: Garage replies are captured and stored in the "Recevied email" Baserow table, with each reply linked to the correct VIN.
- **How tested:**
    - Sent a reply from a garage email with a VIN in the subject/body.
    - Ran the `ingest_garage_replies.py` script.
    - Checked Baserow for a new row in "Recevied email" with the correct VIN and email content.

## 4. Error Handling
- ✅ Verified: The previous backend error on Fix it form submission ("Error processing request") is resolved. Submissions now succeed.

## 5. Email Ingestion Logic
- ✅ Implemented: Backend script (`backend/scripts/ingest_garage_replies.py`) fetches recent emails from Microsoft 365, extracts VIN from subject/body, and stores replies in Baserow with correct VIN linkage.
- **How tested:** Ran script, verified new records in Baserow for garage replies.

## 6. Integration Points
- All integration points (form, email, Baserow, reply linkage) function correctly end-to-end.

---

# Verification Steps (for future reference)
1. Submit a test Fix it form with a unique VIN.
2. Check Baserow Customer details table for new entry.
3. Check all garage inboxes for notification email.
4. Send a reply email from a garage, including the VIN in subject or body.
5. Run the ingestion script: `python3 backend/scripts/ingest_garage_replies.py`
6. Check "Recevied email" Baserow table for new row with correct VIN and email content.

---

# Known Issues
- Table name in Baserow is misspelled as "Recevied email" (should be "Received email").
- VIN must be present in subject or body for linkage.

---

# Next Steps
- Consider automating the ingestion script (e.g., with a cron job or webhook).
- Fix Baserow table name typo if possible.

---

# Summary
The Fix It system now works end-to-end: form submissions, notifications, and garage replies are all reliably tracked and linked by VIN in Baserow.
