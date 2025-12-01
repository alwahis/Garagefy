# IMMEDIATE ACTION REQUIRED - Frontend Connection Fix

## Problem
Frontend cannot connect to backend. Error: "No response from server. Please check your connection."

## Root Cause
The environment variable `REACT_APP_API_URL` is not set in Netlify, so the frontend defaults to `http://localhost:8099` which doesn't exist in production.

---

## IMMEDIATE FIX (5 minutes)

### Step 1: Go to Netlify Dashboard
1. Open https://app.netlify.com
2. Log in to your account
3. Select your Garagefy frontend site

### Step 2: Set Environment Variable
1. Click **Site Settings** (top menu)
2. Click **Build & Deploy** (left sidebar)
3. Click **Environment** (left sidebar)
4. Click **Edit variables**
5. Add new variable:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://garagefy-1.onrender.com`
6. Click **Save**

### Step 3: Rebuild Frontend
1. Go back to your site
2. Click **Deploys** (top menu)
3. Click **Trigger deploy** (dropdown button)
4. Click **Deploy site**
5. Wait for build to complete (usually 2-3 minutes)
6. You should see "Published" status

### Step 4: Test
1. Go to your frontend URL
2. Fill out the service request form
3. Submit
4. Should see success message (no error)

---

## Why This Works

**Before Fix:**
```
Frontend tries to connect to: http://localhost:8099
Result: Connection refused (no server at that address)
Error: "No response from server"
```

**After Fix:**
```
Frontend connects to: https://garagefy-1.onrender.com
Result: Backend responds successfully
Success: Form submitted, customer record created
```

---

## Verification

After rebuild completes, verify:

1. **Frontend loads** - Go to your Netlify URL
2. **Form displays** - Service request form should be visible
3. **Submit works** - Fill form and submit
4. **Success message** - Should see "Your service request has been submitted successfully"
5. **Check Baserow** - New customer record should appear in "Customer details" table

---

## If You Need Help

The issue is 100% the missing environment variable. Once you set it in Netlify and rebuild, it will work.

**What was changed:**
- Nothing in the code
- Just need to set one environment variable in Netlify

**Why it wasn't set before:**
- The netlify.toml file has it for production context, but Netlify also needs it in the dashboard
- The dashboard setting takes precedence

---

## Timeline

- **Now:** Set environment variable in Netlify (2 minutes)
- **Next:** Trigger rebuild (1 minute)
- **Wait:** Build completes (2-3 minutes)
- **Then:** Test form submission (1 minute)
- **Total:** ~7 minutes

---

## Questions?

If the rebuild fails or you get an error:
1. Check the Netlify build logs for error messages
2. Verify the environment variable was saved correctly
3. Make sure the value is exactly: `https://garagefy-1.onrender.com`

---

**Status:** Action required by user  
**Estimated Fix Time:** 5-10 minutes
