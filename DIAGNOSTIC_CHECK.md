# Garage Response Recording - Diagnostic Check

**Date:** December 2, 2025  
**Purpose:** Systematically check all three possible failure points

---

## Issue 1: New Backend Code Not Deployed on Render

### What to Check

1. **Go to Render Dashboard**
   - Open your backend service (Garagefy API)
   - Click on **Deploys** tab

2. **Check the Latest Deploy**
   - Look at the most recent deployment
   - Check the **Commit** column
   - You should see one of these recent commits:
     ```
     Fix garage response VIN extraction - search body for request ID
     Improve VIN extraction logging and fallback patterns
     Add diagnostic guide for garage response recording issue
     ```

3. **Check the Branch**
   - Look for **Branch** information
   - It should show either:
     - `main` (if you merged fresh-garagefy to main)
     - `fresh-garagefy` (if Render is configured to deploy this branch)

### What This Means

**If you see the recent commits:**
- ✅ The fix IS deployed
- Move to Issue 2

**If you see OLD commits (from before Dec 2):**
- ❌ The fix is NOT deployed
- **Action:** Either:
  - Option A: Merge `fresh-garagefy` into `main` branch locally and push
  - Option B: Change Render to deploy from `fresh-garagefy` branch

### How to Deploy

**Option A: Merge to main (Recommended)**
```bash
git checkout main
git merge fresh-garagefy
git push origin main
```
Then Render will auto-deploy within 1-2 minutes.

**Option B: Configure Render to use fresh-garagefy**
1. Go to Render Dashboard → Your backend service
2. Click **Settings**
3. Find **Branch** setting
4. Change from `main` to `fresh-garagefy`
5. Save
6. Render will redeploy automatically

---

## Issue 2: Email Monitor Not Processing Inbox

### What to Check

**A. Verify Email Credentials in Render**

1. Go to Render Dashboard → Your backend service
2. Click **Environment** tab
3. Verify these variables are set:
   ```
   EMAIL_ADDRESS = info@garagefy.app
   EMAIL_PASSWORD = [should be set]
   MS_CLIENT_ID = [should be set]
   MS_CLIENT_SECRET = [should be set]
   MS_TENANT_ID = [should be set]
   IMAP_SERVER = outlook.office365.com
   IMAP_PORT = 993
   ```

**B. Check Render Logs for Email Monitor Errors**

1. Go to Render Dashboard → Your backend service
2. Click **Logs** tab
3. Search for these keywords:
   ```
   EmailMonitorService
   check_and_process_new_emails
   OAuth2 token
   Failed to connect to inbox
   IMAP
   ```

**C. Look for These Log Patterns**

**Good (Email monitor is working):**
```
[SCHEDULED] Starting email check at 2025-12-02 10:00:00
Found X emails from today to check
Processing email from garage@example.com: Re: Repair Quote Request
Successfully saved NEW email to Airtable from garage@example.com
```

**Bad (Email monitor not running):**
```
[SCHEDULED] Email check failed: [error message]
Failed to acquire token: [error]
Failed to connect to inbox: [error]
Error checking emails: [error]
```

### What This Means

**If you see "Starting email check" messages:**
- ✅ Email monitor IS running
- Move to Issue 3

**If you see error messages:**
- ❌ Email monitor has a problem
- Check the error message:
  - `Failed to acquire token` → OAuth2 credentials wrong
  - `Failed to connect to inbox` → IMAP credentials wrong
  - `Connection timeout` → Network issue

### How to Fix

**If OAuth2 token error:**
1. Verify `MS_CLIENT_ID`, `MS_CLIENT_SECRET`, `MS_TENANT_ID` in Render
2. Regenerate tokens in Azure AD if needed

**If IMAP connection error:**
1. Verify `EMAIL_ADDRESS` and `EMAIL_PASSWORD` are correct
2. Verify `IMAP_SERVER` = `outlook.office365.com`
3. Verify `IMAP_PORT` = `993`

---

## Issue 3: Baserow Call Failing (Wrong Table ID / API Error)

### What to Check

**A. Verify Baserow Environment Variables in Render**

1. Go to Render Dashboard → Your backend service
2. Click **Environment** tab
3. Verify these variables are set:
   ```
   BASEROW_API_TOKEN = [should be set]
   BASEROW_DATABASE_ID = [should be set]
   BASEROW_TABLE_CUSTOMER_DETAILS = [should be set]
   BASEROW_TABLE_FIX_IT = [should be set]
   BASEROW_TABLE_RECEIVED_EMAIL = [should be set]
   ```

**B. Verify Table IDs Are Correct**

1. Go to Baserow
2. Open your database
3. For each table, click on the table name
4. Look at the URL: `https://baserow.io/database/[DB_ID]/table/[TABLE_ID]`
5. Extract the TABLE_ID and verify it matches your environment variables

**Example:**
```
URL: https://baserow.io/database/12345/table/67890
TABLE_ID = 67890
```

**C. Check Render Logs for Baserow Errors**

1. Go to Render Dashboard → Your backend service
2. Click **Logs** tab
3. Search for these keywords:
   ```
   Baserow API error
   store_received_email
   Invalid Recevied email table ID
   Field error
   Baserow URL
   ```

**D. Look for These Log Patterns**

**Good (Baserow working):**
```
DEBUG: Using table ID 67890 for Recevied email table
DEBUG: Storing email with payload: {...}
Stored email from garage@example.com for VIN TESTVIN123456789
```

**Bad (Baserow error):**
```
Invalid Recevied email table ID: 0
Baserow API error (400): Invalid table ID
Baserow API error (401): Unauthorized
Field error [field_6389838]: This field does not exist
```

### What This Means

**If you see "Stored email" messages:**
- ✅ Baserow IS working
- ✅ All three issues are resolved

**If you see "Invalid table ID: 0":**
- ❌ `BASEROW_TABLE_RECEIVED_EMAIL` is not set or is 0
- **Action:** Set the correct table ID in Render environment variables

**If you see "Field does not exist":**
- ❌ Field IDs are wrong
- **Action:** Verify field IDs in Baserow match the code

**If you see "Unauthorized":**
- ❌ `BASEROW_API_TOKEN` is wrong or expired
- **Action:** Regenerate token in Baserow

---

## Quick Diagnostic Checklist

### Step 1: Deployment Check
- [ ] Go to Render Deploys tab
- [ ] Verify latest commit is from Dec 2 (fresh-garagefy fixes)
- [ ] If not, merge fresh-garagefy to main and push

### Step 2: Email Monitor Check
- [ ] Go to Render Logs
- [ ] Search for "Starting email check"
- [ ] If found, email monitor is running ✅
- [ ] If not found, check for OAuth2/IMAP errors

### Step 3: Baserow Check
- [ ] Go to Render Logs
- [ ] Search for "Stored email"
- [ ] If found, Baserow is working ✅
- [ ] If not found, check for Baserow API errors

### Step 4: Verify in Baserow
- [ ] Go to Baserow
- [ ] Open "Recevied email" table
- [ ] Check if new records appear after garage response
- [ ] Verify VIN field is populated

---

## Test Scenario

Once you've verified all three issues:

1. **Submit a test request** with VIN: `TESTVIN1234567890A`
2. **Wait for quote email** to be sent to garage
3. **Reply from garage** with a simple response
4. **Wait 1-2 minutes** for email monitoring
5. **Check Baserow** for new record in "Recevied email" table
6. **Verify VIN** is populated in the record

---

## Expected Results

### After Fix Deployment

**Render Logs should show:**
```
[SCHEDULED] Starting email check at 2025-12-02 10:05:00
Found 1 emails from today to check
Processing email from garage@example.com: Re: Repair Quote Request - VIN: TESTVIN1234567890A
Extracted request ID from body: req_1764594858259_r42e3r4ym
Found request ID req_1764594858259_r42e3r4ym, matched to VIN: TESTVIN1234567890A
DEBUG: Using table ID 67890 for Recevied email table
DEBUG: Storing email with payload: {
  "field_6389838": "garage@example.com",
  "field_6389839": "Re: Repair Quote Request - VIN: TESTVIN1234567890A",
  "field_6389840": "I can fix this for 500 euros.",
  "field_6389841": "2025-12-02T10:05:00+00:00",
  "field_6389842": "TESTVIN1234567890A"
}
Stored email from garage@example.com for VIN TESTVIN1234567890A
Successfully saved NEW email to Airtable from garage@example.com
```

**Baserow "Recevied email" table should show:**
```
Email: garage@example.com
Subject: Re: Repair Quote Request - VIN: TESTVIN1234567890A
Body: I can fix this for 500 euros.
Received At: 2025-12-02T10:05:00+00:00
VIN: TESTVIN1234567890A
```

---

## Troubleshooting

### Problem: No new records in Baserow

**Check in this order:**
1. Is the fix deployed? (Check Render Deploys)
2. Is email monitor running? (Check Render Logs for "Starting email check")
3. Is Baserow API working? (Check Render Logs for "Stored email")
4. Are environment variables set? (Check Render Environment)

### Problem: Records appear but VIN is empty

**Causes:**
1. VIN extraction failed (check logs for "Could not extract VIN")
2. Request ID extraction failed (check logs for "Extracted request ID")
3. VIN lookup failed (check logs for "Could not find VIN for request ID")

**Fix:**
- Ensure garage response email includes the original quoted email with VIN
- Ensure original quote request email includes VIN in subject or body

### Problem: Baserow API error

**Check:**
1. Is `BASEROW_TABLE_RECEIVED_EMAIL` set to correct table ID?
2. Are field IDs correct? (field_6389838, field_6389839, etc.)
3. Is `BASEROW_API_TOKEN` valid?

---

**Status:** Diagnostic checklist created  
**Next Action:** Run through the checklist and report findings
