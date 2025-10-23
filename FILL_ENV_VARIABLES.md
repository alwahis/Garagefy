# 🔑 Fill in Your Environment Variables

## ⚠️ IMPORTANT: You need to add your actual API keys!

I've updated `backend/.env` with placeholders. You need to replace these with your actual values:

### 📝 What You Need to Fill In:

Open `backend/.env` and replace these placeholders:

#### 1. Airtable API Key
```
AIRTABLE_API_KEY=YOUR_AIRTABLE_API_KEY_HERE
```
**Where to find it:**
- Go to: https://airtable.com/account
- Click "Generate API key"
- Copy and paste it

#### 2. Microsoft Graph API Credentials
```
MS_CLIENT_ID=YOUR_MS_CLIENT_ID_HERE
MS_CLIENT_SECRET=YOUR_MS_CLIENT_SECRET_HERE
MS_TENANT_ID=YOUR_MS_TENANT_ID_HERE
```
**Where to find it:**
- Azure Portal: https://portal.azure.com
- App Registrations → Your app
- Copy Client ID, Client Secret, and Tenant ID

#### 3. Cloudinary Credentials
```
CLOUDINARY_API_KEY=YOUR_CLOUDINARY_API_KEY_HERE
CLOUDINARY_API_SECRET=YOUR_CLOUDINARY_API_SECRET_HERE
```
**Where to find it:**
- Cloudinary Dashboard: https://cloudinary.com/console
- Account Details section
- Copy API Key and API Secret

---

## ✅ Already Set (No Changes Needed):

These are already correct:
- ✅ `AIRTABLE_BASE_ID=appaZpcXMlL5JqJBc`
- ✅ `EMAIL_ADDRESS=info@garagefy.app`
- ✅ `CLOUDINARY_CLOUD_NAME=dteblwsuu`
- ✅ `DEEPSEEK_API_KEY=sk-92c7ef09798c44499cc632be29c479b9`

---

## 🚀 After Filling In:

Once you've added all the real values to `backend/.env`, you'll use these same values in Render:

### For Render Deployment:

When you create the web service on Render, add these environment variables:

```
AIRTABLE_API_KEY = <value from backend/.env>
AIRTABLE_BASE_ID = appaZpcXMlL5JqJBc
MS_CLIENT_ID = <value from backend/.env>
MS_CLIENT_SECRET = <value from backend/.env>
MS_TENANT_ID = <value from backend/.env>
EMAIL_ADDRESS = info@garagefy.app
CLOUDINARY_CLOUD_NAME = dteblwsuu
CLOUDINARY_API_KEY = <value from backend/.env>
CLOUDINARY_API_SECRET = <value from backend/.env>
```

---

## 🔍 How to Check if You Have the Right Values:

### Test Locally First:

1. Fill in `backend/.env` with real values
2. Run the backend:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8099
   ```
3. Visit: http://localhost:8099/health
4. Should return: `{"status":"healthy"}`

If it works locally, the same values will work on Render!

---

## ⚠️ Security Note:

- ✅ `backend/.env` is in `.gitignore` (won't be pushed to GitHub)
- ✅ Never commit API keys to GitHub
- ✅ Only add them to Render dashboard manually

---

**Need help finding any of these values? Let me know which one!**
