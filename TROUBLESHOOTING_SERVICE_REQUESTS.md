# Troubleshooting Service Request Errors
**Error:** `ERROR_REQUEST_BODY_VALIDATION` when submitting Fix-It forms

---

## Quick Diagnosis

### Step 1: Check the Backend Logs
```bash
tail -f backend/logs/garagefy.log | grep -E "Field error|Baserow API error|Payload"
```

Look for messages like:
- `Field error [field_XXXXX]: ...` - Specific field validation error
- `Baserow API error: ...` - General API error
- `Payload being sent: ...` - The exact data being sent

### Step 2: Identify the Problem Field
The error message should tell you which field is invalid. Common issues:

| Field | Issue | Solution |
|-------|-------|----------|
| `field_6389835` (Image) | Invalid format | See Image Field Fix below |
| `field_6389834` (Date) | Invalid date format | Use ISO format |
| `field_6389828` (Name) | Empty or missing | Ensure name is provided |
| `field_6389830` (Email) | Invalid email | Ensure valid email format |

---

## Common Issues & Fixes

### Issue 1: Image Field Validation Error

**Symptoms:**
```
Field error [field_6389835]: Invalid image format
```

**Root Cause:**
The Image field might be:
- A File field (expects file uploads, not URLs)
- A URL field (expects just the URL string)
- Expecting a specific format

**Solution:**

Option A - Omit the Image field if it's not needed:
```python
# Don't include the Image field if there are no images
if formatted_images:
    payload['field_6389835'] = formatted_images
```

Option B - Send just the URL string instead of an object:
```python
# Try sending just the URL string
if formatted_images:
    payload['field_6389835'] = [img['url'] for img in formatted_images]
```

Option C - Check the field type in Baserow:
1. Go to Baserow
2. Open Customer details table
3. Click on Image field settings
4. Check the field type (File, URL, Link, etc.)
5. Adjust the format accordingly

**Status:** Already fixed in the latest code update.

---

### Issue 2: Date/Time Field Format Error

**Symptoms:**
```
Field error [field_6389834]: Invalid datetime format
```

**Root Cause:**
Baserow might expect a specific date format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)

**Solution:**
```python
# Use simple date format instead of ISO with timezone
from datetime import datetime

# Instead of:
payload['field_6389834'] = datetime.now(timezone.utc).isoformat()

# Try:
payload['field_6389834'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
```

**Status:** Fallback handling added in the latest code update.

---

### Issue 3: Empty Required Field

**Symptoms:**
```
Field error [field_6389828]: This field is required
```

**Root Cause:**
A required field (Name or Email) is empty or missing

**Solution:**
1. Check the form submission - ensure name and email are provided
2. Verify the frontend is sending the data correctly
3. Check the backend logs for the actual data being received

```bash
# Check what data is being received
tail -f backend/logs/garagefy.log | grep "Request details"
```

---

### Issue 4: Invalid Email Format

**Symptoms:**
```
Field error [field_6389830]: Invalid email address
```

**Root Cause:**
The email field contains an invalid email address

**Solution:**
1. Validate email on the frontend before submission
2. Add email validation in the backend:

```python
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# In create_customer method:
if not is_valid_email(data.get('Email')):
    return {'success': False, 'error': 'Invalid email format', 'record_id': None}
```

---

## Debugging Workflow

### Step 1: Enable Detailed Logging
```python
# In backend/app/services/baserow_service.py
self.logger.info(f"🔍 DEBUG: Payload being sent: {json.dumps(payload, indent=2)}")
```

### Step 2: Test with Minimal Data
```bash
# Test with just required fields
curl -X POST http://localhost:8099/api/service-requests \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "carBrand=BMW" \
  -F "vin=VIN123456"
```

### Step 3: Add Fields One by One
```bash
# Add phone
curl -X POST http://localhost:8099/api/service-requests \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=+352 123 456" \
  -F "carBrand=BMW" \
  -F "vin=VIN123456"

# Add license plate
curl -X POST http://localhost:8099/api/service-requests \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=+352 123 456" \
  -F "carBrand=BMW" \
  -F "vin=VIN123456" \
  -F "licensePlate=ABC-123"

# Add notes
curl -X POST http://localhost:8099/api/service-requests \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=+352 123 456" \
  -F "carBrand=BMW" \
  -F "vin=VIN123456" \
  -F "licensePlate=ABC-123" \
  -F "notes=Front bumper damage"

# Add images
curl -X POST http://localhost:8099/api/service-requests \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=+352 123 456" \
  -F "carBrand=BMW" \
  -F "vin=VIN123456" \
  -F "licensePlate=ABC-123" \
  -F "notes=Front bumper damage" \
  -F "images=@/path/to/image.jpg"
```

### Step 4: Check Baserow Directly
```bash
# Use the debug script to test Baserow API directly
python debug_baserow_fields.py
```

---

## Field Mapping Reference

**Customer details table fields:**

| Field ID | Name | Type | Required | Notes |
|----------|------|------|----------|-------|
| field_6389828 | Name | Text | Yes | Customer name |
| field_6389829 | Phone | Phone | No | Phone number |
| field_6389830 | Email | Email | Yes | Email address |
| field_6389831 | VIN | Text | No | Vehicle VIN |
| field_6389832 | Notes | Long text | No | Damage description |
| field_6389833 | Brand | Text | No | Car brand |
| field_6389834 | Date and Time | DateTime | No | Submission timestamp |
| field_6389835 | Image | File | No | Damage images |
| field_6389836 | Sent Emails | Text | No | Email tracking |
| field_6389837 | Plate Number | Text | No | License plate |

---

## Verification Checklist

- [ ] Backend is running: `python backend/run.py`
- [ ] Environment variables are set (check `.env` file)
- [ ] Baserow API token is valid
- [ ] Baserow database ID is correct
- [ ] Baserow table IDs are correct
- [ ] Cloudinary credentials are set (if using images)
- [ ] Frontend is sending correct field names
- [ ] Email format is valid
- [ ] Name is not empty
- [ ] Images are valid URLs (if provided)

---

## Getting Help

### Check These Files
1. `backend/logs/garagefy.log` - Application logs
2. `backend/logs/requests.log` - Request logs
3. `BASEROW_VALIDATION_FIX.md` - Detailed fix documentation
4. `debug_baserow_fields.py` - Debugging script

### Run Diagnostics
```bash
# Check Baserow connectivity
python debug_baserow_fields.py

# Check backend health
curl http://localhost:8099/health

# Check API documentation
curl http://localhost:8099/docs
```

### Enable Debug Mode
```python
# In backend/app/main.py
logger.setLevel(logging.DEBUG)
```

---

## Summary

The `ERROR_REQUEST_BODY_VALIDATION` error indicates that one or more fields in the request payload don't match Baserow's expected format. Use the debugging steps above to identify which field is causing the issue, then apply the appropriate fix.

**Key Points:**
1. Check the logs for field-specific error messages
2. Test with minimal data first
3. Add fields one by one to identify the problem
4. Use the debug script to verify Baserow configuration
5. Refer to the field mapping table for correct field IDs

---

**Last Updated:** December 1, 2025
