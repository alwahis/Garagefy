# 🚀 Deploy Backend to Render - Complete Guide

## ✅ Prerequisites Complete

- ✅ `render.yaml` configured
- ✅ Backend code ready
- ✅ GitHub repo up to date

## 📋 Step-by-Step Deployment

### Step 1: Sign Up / Login to Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account (alwahis)
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub repository:
   - Search for: **Garagefy**
   - Click "Connect" next to alwahis/Garagefy

### Step 3: Configure the Service

Render will auto-detect the `render.yaml` file, but verify these settings:

**Basic Settings:**
- **Name:** `garagefy-backend`
- **Region:** Frankfurt (or closest to Luxembourg)
- **Branch:** `clean-garagefy` (or `main`)
- **Root Directory:** `backend`

**Build & Deploy:**
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **Free** plan

### Step 4: Add Environment Variables

Click "Advanced" → "Add Environment Variable" and add these:

```
AIRTABLE_API_KEY=<your-key-from-backend/.env>
AIRTABLE_BASE_ID=appaZpcXMlL5JqJBc
MS_CLIENT_ID=<your-client-id>
MS_CLIENT_SECRET=<your-secret>
MS_TENANT_ID=<your-tenant-id>
EMAIL_ADDRESS=info@garagefy.app
CLOUDINARY_CLOUD_NAME=dteblwsuu
CLOUDINARY_API_KEY=<your-key>
CLOUDINARY_API_SECRET=<your-secret>
```

**Important:** Copy these values from your `backend/.env` file!

### Step 5: Create Web Service

1. Click "Create Web Service"
2. Wait for deployment (takes 2-5 minutes)
3. Watch the build logs for any errors

### Step 6: Get Your Backend URL

Once deployed, you'll see your service URL at the top:
```
https://garagefy-backend.onrender.com
```

**Test it:** Visit `https://garagefy-backend.onrender.com/health`

Should return: `{"status":"healthy"}`

### Step 7: Update Frontend (Netlify)

1. Go to Netlify dashboard: https://app.netlify.com/sites/garagefy-app-8zts3/settings/deploys
2. Click "Environment variables"
3. Click "Add a variable"
4. Add:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://garagefy-backend.onrender.com`
5. Click "Save"
6. Go to "Deploys" tab
7. Click "Trigger deploy" → "Deploy site"

### Step 8: Verify Everything Works

1. Visit https://garagefy.app
2. Try submitting a quote request
3. Check if it works without errors!

## 🔧 Troubleshooting

### If Build Fails:

**Check logs in Render dashboard:**
- Look for missing dependencies
- Check Python version compatibility
- Verify requirements.txt is correct

**Common fixes:**
```bash
# Update requirements.txt if needed
cd backend
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### If Health Check Fails:

1. Check if `/health` endpoint exists in your code
2. Verify the start command is correct
3. Check environment variables are set

### If CORS Errors:

Your backend is already configured to allow `https://garagefy.app` in CORS origins (we did this earlier).

### Cold Starts (Free Plan):

⚠️ **Important:** Free tier spins down after 15 minutes of inactivity
- First request after inactivity: ~30 seconds delay
- Subsequent requests: Fast
- This is normal for free tier!

**Solutions:**
1. Upgrade to paid plan ($7/month) for always-on
2. Use a service like UptimeRobot to ping your API every 14 minutes
3. Accept the cold start delay (most users won't notice)

## 📊 Monitoring

### View Logs:
1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. See real-time logs

### Metrics:
- CPU usage
- Memory usage
- Request count
- Response times

## 🔄 Auto-Deploy

Render automatically deploys when you push to GitHub!

```bash
# Make changes
git add .
git commit -m "Update backend"
git push

# Render will automatically deploy the changes
```

## 💰 Pricing

**Free Plan:**
- ✅ 750 hours/month (enough for 1 service 24/7)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after 15 min inactivity

**Paid Plan ($7/month):**
- ✅ Always on (no cold starts)
- ✅ More resources
- ✅ Better performance

## ✅ Final Architecture

After deployment:

```
┌─────────────────────────────────────┐
│         garagefy.app                │
│      (Netlify - Frontend)           │
└──────────────┬──────────────────────┘
               │
               │ API Calls
               ↓
┌─────────────────────────────────────┐
│  garagefy-backend.onrender.com      │
│      (Render - Backend API)         │
└──────────────┬──────────────────────┘
               │
               ├─────────────┬─────────────┐
               ↓             ↓             ↓
         ┌─────────┐   ┌──────────┐  ┌──────────┐
         │Airtable │   │Cloudinary│  │Microsoft │
         │   DB    │   │  Images  │  │  Email   │
         └─────────┘   └──────────┘  └──────────┘
```

## 🎉 Success!

Once all steps are complete:
- ✅ Backend deployed to Render
- ✅ Frontend updated with backend URL
- ✅ Full application working at https://garagefy.app

## 📞 Need Help?

If you encounter issues:
1. Check Render logs
2. Verify all environment variables are set
3. Test backend health endpoint
4. Check browser console for errors

---

**Ready to deploy? Follow the steps above!** 🚀
