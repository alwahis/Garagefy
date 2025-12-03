# Diagnosis: No Records in "Recevied email" Table

**Issue:** Garage responses are not appearing in Baserow "Recevied email" table  
**Table ID:** 755538  
**Database ID:** 328778

---

## Step 1: Check Render Logs

Go to **Render Dashboard → Garagefy API → Logs** and look for these patterns:

### Pattern 1: Email Monitor Running?

**Look for:**
```
[SCHEDULED] Starting email check at [TIME]
Found X emails from today to check
```

**If you see this:** Email monitor IS running ✅  
**If you DON'T see this:** Email monitor is NOT running ❌

---

### Pattern 2: Emails Being Fetched?

**Look for:**
```
Processing email from [GARAGE_EMAIL]: [SUBJECT]
```

**If you see this:** Emails ARE being fetched ✅  
**If you DON'T see this:** No emails found or connection failed ❌

---

### Pattern 3: VIN Extraction?

**Look for:**
```
Extracted VIN from email text: [VIN]
```

**If you see this:** VIN extraction IS working ✅  
**If you see:** `Could not extract VIN from email` ❌

---

### Pattern 4: Baserow Write?

**Look for:**
```
Stored email from [GARAGE] for VIN [VIN]
```

**If you see this:** Record WAS written to Baserow ✅  
**If you see:** `Baserow API error` ❌

---

## Step 2: Likely Causes

Based on what you see in logs, here are the most likely causes:

### Cause A: Email Monitor Not Running

**Symptoms:**
- No `[SCHEDULED] Starting email check` in logs
- No `Found X emails` messages

**Why:**
- Scheduler not started
- OAuth2 token acquisition failed
- IMAP connection failed

**Check:**
1. Look for: `Scheduler started successfully`
2. Look for: `Failed to acquire token` or `Failed to connect to inbox`
3. Check Render environment variables:
   - `MS_CLIENT_ID`
   - `MS_CLIENT_SECRET`
   - `MS_TENANT_ID`
   - `EMAIL_ADDRESS`
   - `EMAIL_PASSWORD` (if using basic auth)

---

### Cause B: Emails Not Being Found

**Symptoms:**
- `[SCHEDULED] Starting email check` appears
- But `Found 0 emails from today to check`

**Why:**
- No emails in inbox
- Email search filter not working
- Emails are old (older than 24 hours)

**Check:**
1. Manually check info@garagefy.app inbox
2. Verify garage has actually sent a reply
3. Check email timestamp is recent

---

### Cause C: VIN Not Being Extracted

**Symptoms:**
- `Processing email from [GARAGE]` appears
- But no `Extracted VIN` message
- Instead: `Could not extract VIN from email`

**Why:**
- Email doesn't contain VIN
- VIN format is invalid
- Request ID lookup failed

**Check:**
1. Verify garage response includes VIN in subject or body
2. Verify VIN is 17 characters (valid format)
3. Check request ID extraction worked

---

### Cause D: Baserow Write Failing

**Symptoms:**
- `Extracted VIN` message appears
- But no `Stored email` message
- Instead: `Baserow API error`

**Why:**
- Table ID is wrong
- API token is invalid/expired
- Field IDs are wrong
- Duplicate detection skipped the record

**Check:**
1. Verify table ID: 755538
2. Verify API token in Render
3. Check field IDs in code
4. Check if VIN already exists (duplicate)

---

## Step 3: Quick Diagnostic Commands

### Check 1: Is Email Monitor Scheduler Running?

Look in Render logs for:
```
app.services.scheduler_service - INFO - Scheduler started successfully
```

If not found, the scheduler didn't start.

---

### Check 2: How Many Emails Are Being Found?

Look for:
```
Found X emails from today to check
```

- If X = 0: No emails in inbox
- If X > 0: Emails found, check if they're being processed

---

### Check 3: Are Emails Being Processed?

Look for:
```
Processing email from [EMAIL]: [SUBJECT]
```

Count how many times this appears. Should match the number of emails found.

---

### Check 4: Are VINs Being Extracted?

Look for:
```
Extracted VIN from email text: [VIN]
```

If you see this, VIN extraction is working.

---

### Check 5: Are Records Being Stored?

Look for:
```
Stored email from [GARAGE] for VIN [VIN]
```

If you see this, the record WAS written to Baserow.

---

## Step 4: Manual Test

### Test 1: Send a Test Email

1. From any email account, send to: `info@garagefy.app`
2. Subject: `Re: Repair Quote Request - VIN: TESTVIN1234567890A`
3. Body: `I can fix this for 500 euros`
4. Wait 1-2 minutes
5. Check Render logs for processing

### Test 2: Check Baserow Directly

1. Go to Baserow
2. Database: 328778
3. Table: 755538 (Recevied email)
4. Sort by "Created" (newest first)
5. Look for your test email

### Test 3: Run Test Script on Render

1. Go to Render Shell
2. Run: `python test_write_to_baserow.py`
3. Check output for: `[SUCCESS] Record created`
4. Go to Baserow and verify record appears

---

## Step 5: What to Report

When you check the logs, tell me:

1. **Is email monitor running?**
   - Yes / No
   - If yes, what time did it start?

2. **How many emails are being found?**
   - 0 / 1 / 2 / etc.

3. **Are emails being processed?**
   - Yes / No
   - If yes, what's the garage email address?

4. **Is VIN being extracted?**
   - Yes / No
   - If yes, what VIN?

5. **Is Baserow write succeeding?**
   - Yes / No
   - If no, what's the error?

6. **Any error messages?**
   - Copy/paste the error

---

## Common Issues and Fixes

### Issue: "Invalid Recevied email table ID: 0"

**Cause:** `BASEROW_TABLE_RECEIVED_EMAIL` is not set or is 0

**Fix:** Set in Render environment:
```
BASEROW_TABLE_RECEIVED_EMAIL = 755538
```

---

### Issue: "Baserow API error (401): Unauthorized"

**Cause:** API token is invalid or expired

**Fix:** 
1. Go to Baserow
2. Generate a new API token
3. Update in Render environment: `BASEROW_API_TOKEN`

---

### Issue: "Failed to acquire token"

**Cause:** OAuth2 credentials are wrong

**Fix:** Verify in Render environment:
```
MS_CLIENT_ID = [correct value]
MS_CLIENT_SECRET = [correct value]
MS_TENANT_ID = [correct value]
```

---

### Issue: "Found 0 emails from today"

**Cause:** No emails in inbox or search filter not working

**Fix:**
1. Check info@garagefy.app inbox manually
2. Verify garage actually sent a reply
3. Check email timestamp is recent

---

## Next Steps

1. **Check Render logs** for the patterns above
2. **Report what you find** (use the checklist in Step 5)
3. **I'll diagnose** based on your findings
4. **We'll fix** the specific issue

---

**Status:** Awaiting log analysis  
**Action Required:** Check Render logs and report findings
