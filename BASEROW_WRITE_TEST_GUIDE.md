# Baserow Write Test Guide

**Date:** December 2, 2025  
**Purpose:** Verify that garage responses are being written to Baserow "Recevied email" table

---

## Configuration Status

✅ **Verified Working:**

```
Baserow Service Configuration:
  Base URL: https://api.baserow.io
  Database ID: 328778
  Table IDs:
    Customer details: 755537
    Fix it: 755536
    Recevied email: 755538 ✅
  
API Connection: ✅ Working (successfully fetched 36 customer records)
```

---

## How to Test Writing to Baserow

### Option 1: Run Test Script on Render (Recommended)

The test script `test_write_to_baserow.py` is ready to run on Render where environment variables are set.

**Steps:**

1. **Deploy the test script to Render:**
   ```bash
   git add test_write_to_baserow.py
   git commit -m "Add test script for Baserow write"
   git push origin main
   ```

2. **Run it on Render:**
   - Go to Render Dashboard
   - Your Garagefy API service
   - Click "Shell" tab
   - Run: `python test_write_to_baserow.py`

3. **Check the output:**
   - If successful, you'll see: `[SUCCESS] Record created with ID: [number]`
   - If failed, you'll see the error message

4. **Verify in Baserow:**
   - Go to Baserow
   - Open database 328778
   - Open table 755538 (Recevied email)
   - Look for a record with:
     - Email: `test.garage@example.com`
     - VIN: `TESTVIN1234567890A`

---

### Option 2: Manual Test via API

If you want to test directly via API:

**Endpoint:**
```
POST https://api.baserow.io/api/database/rows/table/755538/
```

**Headers:**
```
Authorization: Token [YOUR_BASEROW_API_TOKEN]
Content-Type: application/json
```

**Payload:**
```json
{
  "field_6389838": "test.garage@example.com",
  "field_6389839": "Re: Repair Quote Request - VIN: TESTVIN1234567890A",
  "field_6389840": "I can fix this vehicle for 500 euros.",
  "field_6389841": "2025-12-02T11:00:00+00:00",
  "field_6389842": "TESTVIN1234567890A"
}
```

**Field Mappings:**
- `field_6389838` = Email
- `field_6389839` = Subject
- `field_6389840` = Body
- `field_6389841` = Received At
- `field_6389842` = VIN

---

## What Should Happen

### When Email Monitor Processes a Garage Response

1. **Email arrives** at info@garagefy.app
2. **Email monitor** (runs every 1 minute):
   - Connects to inbox
   - Fetches emails from today
   - Extracts: from_email, subject, body, received_at
   - Extracts: request_id (from subject or body)
   - Extracts: VIN (from email text or via request ID lookup)
   - Calls: `baserow_service.store_received_email(email_data, vin)`

3. **Baserow service** stores the record:
   - Validates table ID (755538)
   - Checks for duplicates by VIN
   - Creates payload with field IDs
   - POSTs to Baserow API
   - Returns success/error

4. **Record appears** in "Recevied email" table:
   - Email: garage email address
   - Subject: Re: Repair Quote Request...
   - Body: garage response
   - VIN: extracted VIN ✅
   - Received At: timestamp

---

## Troubleshooting

### Problem: No records appear in Baserow

**Check these in order:**

1. **Is the email monitor running?**
   - Check Render Logs for: `[SCHEDULED] Starting email check`
   - If not, check scheduler is started

2. **Are emails being fetched?**
   - Check Render Logs for: `Found X emails from today`
   - If not, check OAuth2 credentials

3. **Is VIN being extracted?**
   - Check Render Logs for: `Extracted VIN from email text`
   - If not, check email format includes VIN

4. **Is Baserow call succeeding?**
   - Check Render Logs for: `Stored email from [garage]`
   - If not, check table ID and API token

5. **Are you looking at the right table?**
   - Database ID: 328778
   - Table ID: 755538
   - Table name: "Recevied email" (with typo)

### Problem: Records appear but VIN is empty

**Causes:**
1. VIN extraction failed (no VIN in email)
2. Request ID lookup failed (wrong request ID format)
3. Duplicate detection skipped the record

**Solution:**
- Ensure garage response includes the original quoted email with VIN
- Ensure original quote request includes VIN in subject or body

### Problem: Duplicate records not being created

**This is expected behavior:**
- System checks for existing records with same VIN
- If found, skips creating a duplicate
- Only the first response for a VIN creates a new row

**To test multiple responses:**
- Use different VINs for each test
- Example: TESTVIN1111111111A, TESTVIN2222222222B, etc.

---

## Expected Render Logs

### Successful Email Processing

```
2025-12-02 11:00:00,000 - app.services.scheduler_service - INFO - [SCHEDULED] Starting email check
2025-12-02 11:00:01,000 - app.services.email_monitor_service - INFO - Connecting to outlook.office365.com:993
2025-12-02 11:00:02,000 - app.services.email_monitor_service - INFO - Successfully connected to inbox using OAuth2: info@garagefy.app
2025-12-02 11:00:03,000 - app.services.email_monitor_service - INFO - Found 1 emails from today to check
2025-12-02 11:00:04,000 - app.services.email_monitor_service - INFO - Processing email from garage@example.com: Re: Repair Quote Request
2025-12-02 11:00:05,000 - app.services.email_monitor_service - INFO - 🔍 DEBUG: Extracted request ID from body: req_1764659386879_uv5m3bh19
2025-12-02 11:00:06,000 - app.services.email_monitor_service - INFO - ✅ Extracted VIN from email text: TESTVIN1234567890A
2025-12-02 11:00:07,000 - app.services.baserow_service - INFO - 🔍 DEBUG: Using table ID 755538 for Recevied email table
2025-12-02 11:00:08,000 - app.services.baserow_service - INFO - 🔍 DEBUG: Storing email with payload: {...}
2025-12-02 11:00:09,000 - app.services.baserow_service - INFO - ✅ Stored email from garage@example.com for VIN TESTVIN1234567890A
2025-12-02 11:00:10,000 - app.services.email_monitor_service - INFO - Successfully saved NEW email to Airtable from garage@example.com
```

### Error Logs to Look For

```
# OAuth2 error
"Failed to acquire token: [error]"

# IMAP connection error
"Failed to connect to inbox: [error]"

# Baserow error
"Baserow API error (400): [error]"
"Invalid Recevied email table ID: 0"

# VIN extraction error
"Could not extract VIN from email"
```

---

## Next Steps

1. **Run the test script** on Render to verify write capability
2. **Check Baserow** for the test record
3. **Send a real garage response** and verify it appears in Baserow
4. **Monitor Render logs** for any errors
5. **Verify customer response service** sends compiled quotes

---

## Files Created

- `test_baserow_write.py` - Test script to write a record
- `check_baserow_config.py` - Check Baserow configuration
- `test_write_to_baserow.py` - Simplified test for Render

---

**Status:** ✅ Ready to test  
**Next Action:** Run test script on Render and verify record appears in Baserow
