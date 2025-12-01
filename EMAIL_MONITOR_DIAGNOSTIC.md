# Email Monitoring System Diagnostic
**Date:** December 1, 2025  
**Issue:** Garage responses not being saved to Baserow

---

## System Flow

```
1. Garage sends email to info@garagefy.app
   ↓
2. Email Monitor checks inbox (every 1 minute)
   ↓
3. Email Monitor extracts:
   - From email (garage email)
   - Subject
   - Body
   - VIN (from subject or body)
   ↓
4. Email Monitor calls store_received_email()
   ↓
5. store_received_email() saves to Baserow "Recevied email" table
   ↓
6. Customer Response Service checks for responses
   ↓
7. When all garages respond or 2 business days pass, customer gets compiled quotes
```

---

## Potential Issues

### Issue 1: Email Monitor Not Running
**Check:**
- Go to Render logs
- Look for `[SCHEDULED] Starting email check` messages
- If not present, scheduler didn't start

**Fix:**
- Check if backend started successfully
- Verify no errors in startup logs

### Issue 2: VIN Not Being Extracted
**Check:**
- Look for log messages like:
  - `Found request ID req_XXXXX, matched to VIN: ABC123`
  - `Extracted VIN from email text: ABC123`
  - `No VIN provided, cannot check for duplicates`

**Fix:**
- Ensure email subject contains VIN or request ID
- Email subject should be like: `Repair Quote Request - VIN: ABC123`
- Or email should contain request ID like: `Ref: req_1760691162901_aod9uhj2e`

### Issue 3: Table ID Not Set
**Check:**
- Look for error: `Invalid Recevied email table ID: 0`

**Fix:**
- Set `BASEROW_TABLE_RECEIVED_EMAIL` environment variable on Render
- Value should be the table ID from Baserow URL

### Issue 4: Field IDs Wrong
**Check:**
- Look for error: `Field error [field_XXXXX]`

**Fix:**
- Verify field IDs in Baserow match the code:
  - `field_6389838` = Email
  - `field_6389839` = Subject
  - `field_6389840` = Body
  - `field_6389841` = Received At
  - `field_6389842` = VIN

### Issue 5: Email Not Being Received
**Check:**
- Check Microsoft 365 inbox directly
- Verify emails are arriving

**Fix:**
- Check OAuth2 credentials
- Verify email address is correct
- Check IMAP settings

---

## How to Debug

### Step 1: Check Render Logs
```
Go to Render Dashboard → Your Service → Logs
Look for these patterns:
```

**Success Pattern:**
```
[SCHEDULED] Starting email check at 2025-12-01 14:30:00
Processing email from garage@example.com: Repair Quote Request - VIN: ABC123
Found request ID req_1760691162901_aod9uhj2e, matched to VIN: ABC123
[OK] Stored email from garage@example.com for VIN ABC123
[SCHEDULED] Email check completed: 1 emails processed
```

**Failure Pattern:**
```
[SCHEDULED] Starting email check at 2025-12-01 14:30:00
[SCHEDULED] Email check failed: Failed to connect to inbox
```

### Step 2: Check Email Monitor Logs
Look for:
- Connection errors (OAuth2, IMAP)
- Email processing errors
- VIN extraction failures
- Storage errors

### Step 3: Verify Baserow Configuration
```bash
# Run locally (requires .env):
python check_table_ids.py

# Should show:
[OK] BASEROW_TABLE_RECEIVED_EMAIL: 328781 (valid)
```

### Step 4: Test Email Storage Directly
```bash
# Run locally (requires .env):
python test_garage_response_storage.py
```

---

## Email Subject Format

The email subject should contain either:

**Option 1: Request ID**
```
Repair Quote Request - Ref: req_1760691162901_aod9uhj2e
```

**Option 2: VIN**
```
Repair Quote Request - VIN: ABC123DEF456GHI789
```

**Option 3: Both (Recommended)**
```
Repair Quote Request - VIN: ABC123DEF456GHI789 - Ref: req_1760691162901_aod9uhj2e
```

---

## VIN Extraction

The system tries to extract VIN in this order:

1. **From Request ID** - Looks up VIN in Customer details table using request ID
2. **From Email Text** - Uses regex to find 17-character VIN pattern
3. **Fallback** - If no VIN found, email is still saved but won't be matched to customer

---

## Common Errors

### Error: "Failed to connect to inbox"
**Cause:** OAuth2 or password authentication failed  
**Fix:**
- Verify `MS_CLIENT_ID`, `MS_CLIENT_SECRET`, `MS_TENANT_ID` are set
- Or verify `EMAIL_PASSWORD` is set
- Check credentials are correct

### Error: "Invalid Recevied email table ID: 0"
**Cause:** `BASEROW_TABLE_RECEIVED_EMAIL` not set  
**Fix:**
- Get table ID from Baserow URL
- Set on Render environment variables
- Redeploy

### Error: "Field error [field_6389838]"
**Cause:** Field ID doesn't exist in your Baserow instance  
**Fix:**
- Check actual field IDs in Baserow
- Update field IDs in `baserow_service.py`

### Error: "No VIN provided, cannot check for duplicates"
**Cause:** VIN not extracted from email  
**Fix:**
- Ensure email subject contains VIN or request ID
- Check email body contains VIN

---

## Testing the System

### Test 1: Send a Test Email
1. Send email to `info@garagefy.app` from a garage
2. Subject: `Repair Quote Request - VIN: TEST123456789ABCDE`
3. Body: `We can fix your car for 500 EUR`
4. Wait 1-2 minutes
5. Check Baserow "Recevied email" table

### Test 2: Check Logs
1. Go to Render logs
2. Look for email processing messages
3. Verify no errors

### Test 3: Verify Record
1. Go to Baserow
2. Open "Recevied email" table
3. Look for new record with:
   - Email: garage email
   - Subject: email subject
   - Body: email body
   - VIN: extracted VIN

---

## Next Steps

1. **Check Render logs** for email processing messages
2. **Verify environment variables** are set correctly
3. **Send a test email** with VIN in subject
4. **Monitor logs** for processing
5. **Check Baserow** for new record

---

**Status:** Diagnostic guide created  
**Last Updated:** December 1, 2025
