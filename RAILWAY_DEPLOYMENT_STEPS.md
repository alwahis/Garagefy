# Railway Backend Deployment - Step by Step

## ✅ Preparation Complete

I've already created the necessary files:
- `backend/railway.json` - Railway configuration
- `backend/Procfile` - Start command
- `backend/runtime.txt` - Python version

## 🚀 Deployment Steps

### Step 1: Login to Railway (In Progress)

A browser window should have opened. Please:
1. Login with your GitHub account
2. Authorize Railway
3. Come back to the terminal

### Step 2: Initialize Railway Project

After login completes, run:
```bash
cd backend
/Users/mudhafar.hamid/.npm-global/bin/railway init
```

Choose:
- Create a new project: **Yes**
- Project name: **garagefy-backend**

### Step 3: Deploy

```bash
/Users/mudhafar.hamid/.npm-global/bin/railway up
```

This will:
- Upload your backend code
- Install dependencies from requirements.txt
- Start the FastAPI server

### Step 4: Add Environment Variables

Go to Railway dashboard: https://railway.app/dashboard

Click on your project → Variables tab → Add these:

```
AIRTABLE_API_KEY=<from your backend/.env>
AIRTABLE_BASE_ID=appaZpcXMlL5JqJBc
MS_CLIENT_ID=<from your backend/.env>
MS_CLIENT_SECRET=<from your backend/.env>
MS_TENANT_ID=<from your backend/.env>
EMAIL_ADDRESS=info@garagefy.app
CLOUDINARY_CLOUD_NAME=dteblwsuu
CLOUDINARY_API_KEY=<from your backend/.env>
CLOUDINARY_API_SECRET=<from your backend/.env>
```

### Step 5: Generate Domain

```bash
/Users/mudhafar.hamid/.npm-global/bin/railway domain
```

This will give you a URL like: `https://garagefy-backend-production.up.railway.app`

### Step 6: Test Backend

Visit: `https://your-backend-url.railway.app/health`

Should return: `{"status":"healthy"}`

### Step 7: Update Frontend

1. Go to Netlify: https://app.netlify.com/sites/garagefy-app-8zts3/settings/deploys
2. Click "Environment variables"
3. Add new variable:
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-backend-url.railway.app` (from step 5)
4. Click "Deploys" → "Trigger deploy" → "Deploy site"

### Step 8: Verify

Visit https://garagefy.app and test submitting a quote request!

## 🔧 Troubleshooting

### If deployment fails:

Check logs:
```bash
/Users/mudhafar.hamid/.npm-global/bin/railway logs
```

### If environment variables are missing:

Railway dashboard → Your project → Variables → Add missing ones

### If CORS errors:

The backend is already configured to allow garagefy.app in the CORS origins.

## 📝 Quick Commands Reference

```bash
# Check deployment status
/Users/mudhafar.hamid/.npm-global/bin/railway status

# View logs
/Users/mudhafar.hamid/.npm-global/bin/railway logs

# Redeploy
cd backend
/Users/mudhafar.hamid/.npm-global/bin/railway up

# Open Railway dashboard
/Users/mudhafar.hamid/.npm-global/bin/railway open
```

## ⚡ After Deployment

Your full stack will be:
- Frontend: https://garagefy.app (Netlify)
- Backend: https://your-backend.railway.app (Railway)
- Database: Airtable (Cloud)
- Images: Cloudinary (Cloud)
- Email: Microsoft Graph API (Cloud)

All services will be connected and working! 🎉
