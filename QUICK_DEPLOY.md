# ⚡ Quick Deploy to Render - 5 Minutes

## 🎯 What You Need

From your `backend/.env` file, copy these values:
- AIRTABLE_API_KEY
- MS_CLIENT_ID
- MS_CLIENT_SECRET
- MS_TENANT_ID
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET

## 🚀 Deploy Steps

### 1. Go to Render
👉 https://render.com → Sign up with GitHub

### 2. Create Web Service
- Click "New +" → "Web Service"
- Connect repository: **alwahis/Garagefy**
- Branch: **clean-garagefy**

### 3. Render Auto-Detects Settings ✅
(from render.yaml - no manual config needed!)

### 4. Add Environment Variables
Click "Advanced" and add:

```
AIRTABLE_API_KEY=<paste-from-env>
AIRTABLE_BASE_ID=appaZpcXMlL5JqJBc
MS_CLIENT_ID=<paste-from-env>
MS_CLIENT_SECRET=<paste-from-env>
MS_TENANT_ID=<paste-from-env>
EMAIL_ADDRESS=info@garagefy.app
CLOUDINARY_CLOUD_NAME=dteblwsuu
CLOUDINARY_API_KEY=<paste-from-env>
CLOUDINARY_API_SECRET=<paste-from-env>
```

### 5. Deploy
Click "Create Web Service" → Wait 3-5 minutes

### 6. Get Your URL
Copy the URL: `https://garagefy-backend.onrender.com`

### 7. Update Netlify
👉 https://app.netlify.com/sites/garagefy-app-8zts3/settings/deploys

Add variable:
- Key: `REACT_APP_API_URL`
- Value: `https://garagefy-backend.onrender.com`

Then: Deploys → Trigger deploy

### 8. Test
Visit: https://garagefy.app ✅

## ⏱️ Total Time: ~5 minutes

## 📝 Notes

- Free tier spins down after 15 min (30s cold start)
- Auto-deploys on git push
- Logs available in Render dashboard

---

**Full guide:** See RENDER_DEPLOYMENT.md
