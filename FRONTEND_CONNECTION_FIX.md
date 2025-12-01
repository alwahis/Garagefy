# Frontend Connection Error - Fix Guide
**Date:** December 1, 2025  
**Error:** "No response from server. Please check your connection."

---

## Problem

The frontend is unable to connect to the backend API. The error occurs when submitting a service request form.

---

## Root Cause

The frontend environment variable `REACT_APP_API_URL` is not being set correctly during the Netlify build process. The frontend defaults to `http://localhost:8099` which doesn't exist in production.

---

## Solution

### Step 1: Set Environment Variable in Netlify

1. Go to Netlify Dashboard
2. Select your Garagefy frontend site
3. Go to **Site Settings → Build & Deploy → Environment**
4. Add new environment variable:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://garagefy-1.onrender.com`

### Step 2: Trigger a Rebuild

1. Go to **Deploys** tab
2. Click **Trigger deploy → Deploy site**
3. Wait for build to complete (usually 2-3 minutes)

### Step 3: Verify the Fix

1. Go to your Garagefy frontend URL
2. Fill out the service request form
3. Submit
4. Should see success message (no "No response from server" error)

---

## How It Works

**Frontend Configuration Flow:**
```
1. Build time: Netlify reads REACT_APP_API_URL env var
2. Build time: Value is embedded in the built JavaScript
3. Runtime: Frontend uses embedded value to connect to backend
4. Runtime: Requests go to https://garagefy-1.onrender.com/api/service-requests
```

**Current Configuration:**
```javascript
// frontend/src/config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8099';
```

**In netlify.toml:**
```toml
[context.production.environment]
  REACT_APP_API_URL = "https://garagefy-1.onrender.com"
```

---

## Verification Checklist

- [ ] Environment variable set in Netlify dashboard
- [ ] Frontend rebuilt (check Deploys tab)
- [ ] Build completed successfully (no errors)
- [ ] Can access frontend URL
- [ ] Can fill out service request form
- [ ] Form submission succeeds (no error toast)
- [ ] Success message appears
- [ ] Check Render logs for incoming request

---

## If Still Not Working

### Check 1: Verify Backend is Running
```bash
curl https://garagefy-1.onrender.com/health
```
Should return: `{"status":"healthy"}`

### Check 2: Check Browser Console
1. Open frontend in browser
2. Press F12 to open Developer Tools
3. Go to **Console** tab
4. Submit form
5. Look for error messages
6. Check **Network** tab to see if request was made

### Check 3: Check CORS Headers
The backend has CORS configured for:
- `https://garagefy.app`
- `https://www.garagefy.app`
- `http://localhost:3000`

If your frontend is on a different domain, add it to the CORS list in `backend/app/main.py`

### Check 4: Verify Form Data
Check that all required fields are filled:
- Name ✓
- Email ✓
- Car Brand ✓
- VIN ✓
- Consent checkbox ✓

---

## Common Issues

### Issue 1: "No response from server"
**Cause:** Frontend can't reach backend  
**Fix:** Set `REACT_APP_API_URL` environment variable in Netlify

### Issue 2: CORS Error
**Cause:** Frontend domain not in backend CORS list  
**Fix:** Add frontend domain to CORS origins in `backend/app/main.py`

### Issue 3: 404 Error
**Cause:** Endpoint doesn't exist  
**Fix:** Verify backend has `/api/service-requests` endpoint

### Issue 4: 500 Error
**Cause:** Backend error processing request  
**Fix:** Check Render logs for error details

---

## Environment Variables Summary

**Frontend (Netlify):**
- `REACT_APP_API_URL` = `https://garagefy-1.onrender.com`

**Backend (Render):**
- `BASEROW_API_TOKEN` = your token
- `BASEROW_DATABASE_ID` = your db id
- `BASEROW_TABLE_RECEIVED_EMAIL` = your table id
- `CLOUDINARY_CLOUD_NAME` = your cloud name
- `CLOUDINARY_API_KEY` = your api key
- `CLOUDINARY_API_SECRET` = your api secret
- `MS_CLIENT_ID` = your client id
- `MS_CLIENT_SECRET` = your client secret
- `MS_TENANT_ID` = your tenant id
- `EMAIL_ADDRESS` = info@garagefy.app
- `EMAIL_PASSWORD` = your password (or use OAuth2)

---

## Testing the Connection

### Test 1: Direct API Call
```bash
curl -X POST https://garagefy-1.onrender.com/api/service-requests \
  -F "name=Test User" \
  -F "email=test@example.com" \
  -F "carBrand=BMW" \
  -F "vin=TEST123456789ABCDE"
```

### Test 2: Browser Console
```javascript
fetch('https://garagefy-1.onrender.com/health')
  .then(r => r.json())
  .then(d => console.log(d))
  .catch(e => console.error(e))
```

### Test 3: Form Submission
1. Open frontend
2. Fill form with test data
3. Submit
4. Check browser console for logs
5. Check Render logs for backend processing

---

## Next Steps

1. Set `REACT_APP_API_URL` in Netlify environment variables
2. Trigger rebuild
3. Wait for build to complete
4. Test form submission
5. Verify success message appears
6. Check Baserow for new customer record

---

**Status:** Fix guide created  
**Action Required:** Set environment variable in Netlify and rebuild
