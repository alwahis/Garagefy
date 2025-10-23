# Backend Deployment Guide

## Current Status
✅ Frontend deployed to: https://garagefy.app
❌ Backend needs to be deployed

## Option 1: Deploy Backend to Railway (Recommended)

Railway offers free tier and is easy to set up for Python FastAPI apps.

### Steps:

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize Railway project:**
   ```bash
   cd backend
   railway init
   ```

4. **Add environment variables:**
   ```bash
   railway variables set AIRTABLE_API_KEY="your-key"
   railway variables set AIRTABLE_BASE_ID="appaZpcXMlL5JqJBc"
   railway variables set MS_CLIENT_ID="your-client-id"
   railway variables set MS_CLIENT_SECRET="your-secret"
   railway variables set MS_TENANT_ID="your-tenant-id"
   railway variables set EMAIL_ADDRESS="info@garagefy.app"
   railway variables set CLOUDINARY_CLOUD_NAME="dteblwsuu"
   railway variables set CLOUDINARY_API_KEY="your-key"
   railway variables set CLOUDINARY_API_SECRET="your-secret"
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

6. **Get your backend URL:**
   ```bash
   railway domain
   ```
   This will give you a URL like: `https://your-app.railway.app`

7. **Update Netlify environment variable:**
   - Go to: https://app.netlify.com/sites/garagefy-app-8zts3/settings/deploys
   - Add environment variable: `REACT_APP_API_URL` = `https://your-app.railway.app`
   - Redeploy frontend

## Option 2: Deploy Backend to Render

1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables from backend/.env
6. Deploy
7. Update Netlify with the Render URL

## Option 3: Deploy Backend to Heroku

1. Install Heroku CLI
2. Create Procfile in backend/:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   cd backend
   heroku create garagefy-api
   heroku config:set AIRTABLE_API_KEY="your-key"
   # ... set all other env vars
   git push heroku main
   ```

## After Backend Deployment

1. Get your backend URL (e.g., `https://garagefy-api.railway.app`)
2. Update Netlify environment variable:
   - Site: https://app.netlify.com/sites/garagefy-app-8zts3/settings/deploys
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.com`
3. Redeploy frontend on Netlify

## Testing

Once deployed, test:
- Frontend: https://garagefy.app
- Backend health: https://your-backend-url.com/health
- Should return: `{"status":"healthy"}`

## CORS Configuration

Make sure your backend allows requests from garagefy.app. In `backend/app/main.py`, the origins list should include:
```python
origins = [
    "https://garagefy.app",
    "https://www.garagefy.app",
    "http://localhost:3000",  # for local development
]
```
