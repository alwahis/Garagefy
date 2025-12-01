# Garage Responses Not Recording in Baserow - Diagnostic Guide

**Date:** December 1, 2025  
**Issue:** Garage responses are not being recorded in the "Recevied email" table

---

## Problem Analysis

From the backend logs, we can see:
1. ✅ Emails ARE being received and processed
2. ✅ Emails ARE being stored in Baserow
3. ❌ BUT: VIN field is empty/None, so responses can't be matched to customer requests

**Key Log Entry:**
```
2025-12-01 14:42:42,476 - WARNING - No VIN provided, cannot check for duplicates
2025-12-01 14:42:43,687 - INFO - ✅ Stored email from Wayak for VIN None
```

---

## Root Cause

The VIN extraction is failing or returning None. This happens when:

1. **Request ID not found** - Email subject doesn't contain reference ID
2. **VIN regex not matching** - Email body doesn't contain a valid 17-character VIN
3. **VIN label pattern not matching** - "VIN:" label not found in email

---

## Solution: Check Garage Response Email Format

### What the system expects:

The system looks for VIN in this order:

**Option 1: Via Request ID (Preferred)**
```
Email Subject: Re: Repair Quote Request - Ref: req_1764594858259_r42e3r4ym
↓
System extracts: req_1764594858259_r42e3r4ym
↓
Looks up VIN in "Customer details" table by matching timestamp
```

**Option 2: Via VIN in Email Body (Fallback)**
```
Email Body contains:
"VIN: TESTVIN123"
or
"VIN TESTVIN123"
or just
"TESTVIN123" (17 alphanumeric characters)
```

---

## Verification Steps

### Step 1: Check Recent Garage Response Emails

1. Go to your email inbox (info@garagefy.app)
2. Look at the most recent garage response email
3. Check:
   - **Subject line** - Does it contain "Ref: req_XXXXX"?
   - **Body** - Does it contain the VIN?

### Step 2: Check Backend Logs

Look for these log entries when a garage responds:

**Good (VIN extracted):**
```
✅ Extracted VIN from email text: TESTVIN123
```

**Bad (VIN not extracted):**
```
⚠️ Could not extract VIN from email. Subject: Re: Repair Quote Request...
```

### Step 3: Verify Baserow Records

1. Go to Baserow
2. Open "Recevied email" table
3. Check the latest records:
   - **Email column** - Should have garage email ✓
   - **Subject column** - Should have email subject ✓
   - **Body column** - Should have email body ✓
   - **VIN column** - Should NOT be empty ✗ (THIS IS THE PROBLEM)

---

## Why VIN Extraction Might Fail

### Issue 1: Email Subject Format

**If garage responds with:**
```
Subject: Re: Repair Quote Request - VIN: TESTVIN123
```

**System expects:**
```
Subject: Re: Repair Quote Request - Ref: req_1764594858259_r42e3r4ym
```

**Fix:** The original quote request email must include the reference ID in the subject.

### Issue 2: VIN Not in Email Body

**If garage response is just:**
```
"No" or "I will fix it for 400 euros"
```

**System needs:**
```
"I will fix it for 400 euros. VIN: TESTVIN123"
or
"TESTVIN123 - I will fix it for 400 euros"
```

**Fix:** Ensure the VIN appears somewhere in the email body.

### Issue 3: Invalid VIN Format

**Valid VIN:** 17 alphanumeric characters (no I, O, Q)
```
TESTVIN123456789 ✓
TESTVIN12345678  ✗ (only 16 chars)
TESTVIN123456789Q ✗ (contains Q)
```

---

## How to Fix

### For Immediate Testing

When sending a test email from a garage, include:

**Option A: In Subject**
```
Subject: Re: Repair Quote Request - Ref: req_1764594858259_r42e3r4ym
```

**Option B: In Body**
```
I can fix this vehicle for 500 euros.

VIN: TESTVIN123456789
```

### For Production

1. **Ensure customer request emails include reference ID:**
   - Check `backend/app/api/endpoints/service_requests.py`
   - Verify the email template includes: `Reference ID: req_XXXXX`

2. **Ensure garage responses include VIN:**
   - The original quote request email must mention the VIN
   - Garage's reply will include the original email (with VIN)
   - System will extract VIN from the quoted text

---

## Testing the Fix

### Step 1: Send a Test Request

1. Go to frontend form
2. Fill out with:
   - Name: Test User
   - Email: test@example.com
   - Car Brand: BMW
   - VIN: **TESTVIN123456789** (exactly 17 chars)
   - Notes: Test repair

3. Submit form
4. Check Baserow "Customer details" table for new record

### Step 2: Simulate Garage Response

1. Send an email to info@garagefy.app from a garage email
2. **Subject:** `Re: Repair Quote Request - Ref: req_XXXXX` (use the ref from the request)
3. **Body:**
```
I can fix this for 500 euros.

On [date], Garagefy wrote:
> Vehicle Brand: BMW
> VIN: TESTVIN123456789
> Damage: Test repair
```

### Step 3: Verify Recording

1. Wait 1-2 minutes for email monitoring to run
2. Check Baserow "Recevied email" table
3. Should see new record with:
   - Email: garage email
   - Subject: Re: Repair Quote Request...
   - Body: repair quote
   - **VIN: TESTVIN123456789** ← This should NOT be empty

---

## Debugging Commands

### Check Backend Logs in Real-Time

```bash
# SSH into Render backend
# View live logs
tail -f /var/log/app.log | grep -i "vin\|extract\|email"
```

### Manual VIN Extraction Test

```python
import re

def extract_vin(text):
    # Pattern 1: Standard VIN
    vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'
    matches = re.findall(vin_pattern, text.upper())
    if matches:
        return matches[0]
    
    # Pattern 2: VIN label
    vin_label_pattern = r'(?:VIN|Vin|vin)[\s:]*([A-HJ-NPR-Z0-9]{17})'
    label_matches = re.findall(vin_label_pattern, text.upper())
    if label_matches:
        return label_matches[0]
    
    return None

# Test
email_body = "I will fix it for 400 euros. VIN: TESTVIN123456789"
vin = extract_vin(email_body)
print(f"Extracted VIN: {vin}")  # Should print: TESTVIN123456789
```

---

## Expected Behavior After Fix

1. Garage sends response email
2. Email monitoring service runs (every 1 minute)
3. System extracts VIN from email
4. Record is stored in "Recevied email" table WITH VIN
5. Customer response service matches responses to customer requests
6. Customer receives compiled quotes email

---

## Checklist

- [ ] Verify garage response emails include VIN or reference ID
- [ ] Check Baserow "Recevied email" table for VIN values
- [ ] Review backend logs for VIN extraction messages
- [ ] Test with a sample garage response email
- [ ] Confirm VIN appears in "Recevied email" table after response
- [ ] Verify customer receives compiled quotes email

---

## Next Steps

1. **Immediate:** Check a recent garage response email format
2. **Verify:** Look at Baserow records to see if VIN is empty
3. **Test:** Send a test garage response with explicit VIN
4. **Monitor:** Watch backend logs for VIN extraction
5. **Confirm:** Check if record appears in "Recevied email" table with VIN

---

**Status:** Diagnostic guide created  
**Action Required:** Verify garage response email format and check Baserow records
