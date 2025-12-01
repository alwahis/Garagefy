# Baserow API Validation Error Fix
**Date:** December 1, 2025  
**Error:** `ERROR_REQUEST_BODY_VALIDATION` when creating service requests

---

## Problem

When submitting a service request through the Fix-It form, the backend returns:
```
Error processing service request: 500: Failed to create service request: 
Error creating customer: Baserow API error: ERROR_REQUEST_BODY_VALIDATION.
```

This error indicates that the request payload being sent to Baserow contains invalid data for one or more fields.

---

## Root Cause Analysis

The issue is likely in the **Image field** handling. The Baserow API has specific requirements for how image data should be formatted:

### What Was Being Sent (Incorrect)
```json
{
  "field_6389835": [
    {"url": "https://cloudinary.com/image.jpg"}
  ]
}
```

### What Baserow Expects (Correct)
Baserow's file/image field has specific validation requirements. The field may expect:
1. Just the URL string (not wrapped in an object)
2. A specific object format with additional metadata
3. Empty list if no images
4. The field to be omitted entirely if empty

---

## Changes Made

### 1. Improved Image Field Formatting
**File:** `backend/app/services/baserow_service.py` (lines 233-256)

Enhanced the image field handling to:
- Convert various image formats to proper Baserow format
- Handle both string URLs and dictionary objects
- Add detailed logging for debugging
- Validate image data before sending

```python
# Handle images - field_6389835
# Baserow Image field expects a list of objects with 'name' and 'url' keys
if data.get('Image'):
    images = data['Image']
    if not isinstance(images, list):
        images = [images]
    
    # Convert to proper Baserow format
    formatted_images = []
    for img in images:
        if isinstance(img, dict):
            # If it's already a dict with 'url', keep it as is
            if 'url' in img:
                formatted_images.append(img)
            # If it's a dict with other keys, extract URL
            elif 'link' in img:
                formatted_images.append({'url': img['link']})
        elif isinstance(img, str):
            # If it's a string URL, wrap it
            formatted_images.append({'url': img})
    
    if formatted_images:
        payload['field_6389835'] = formatted_images
```

### 2. Enhanced Error Logging
**File:** `backend/app/services/baserow_service.py` (lines 59-76)

Added field-specific error logging to identify which field is causing the validation error:

```python
# Log field-specific errors for validation issues
if isinstance(error_json, dict):
    for key, value in error_json.items():
        if key not in ['error', 'detail']:
            self.logger.error(f"Field error [{key}]: {value}")
```

### 3. Improved Field Validation
**File:** `backend/app/services/baserow_service.py` (lines 278-286)

Updated validation logic to properly check image field format:

```python
# Check for field type issues
if field_id == 'field_6389835' and isinstance(value, list):  # Image field
    # Ensure all items are valid dicts with 'url' key
    for item in value:
        if isinstance(item, dict):
            if 'url' not in item or not item['url']:
                self.logger.warning(f"Invalid image object - missing or empty 'url': {item}")
        else:
            self.logger.warning(f"Image field expects dict with 'url' key, got: {type(item)}")
```

---

## Debugging Steps

### Step 1: Run the Debug Script
```bash
cd /path/to/garagefy
python debug_baserow_fields.py
```

This script will:
1. Fetch all fields in the Customer details table
2. Show the exact field IDs and types
3. Test creating records with different field combinations
4. Identify which field format is causing the validation error

### Step 2: Check the Logs
```bash
tail -f backend/logs/garagefy.log | grep -i "field error\|validation\|image"
```

Look for:
- Field-specific error messages
- Image field format issues
- Validation errors for specific fields

### Step 3: Test the API Endpoint
```bash
# Test with minimal data (no images)
curl -X POST http://localhost:8099/api/service-requests \
  -F "name=Test User" \
  -F "email=test@example.com" \
  -F "phone=+352 123 456" \
  -F "carBrand=BMW" \
  -F "vin=VIN123456" \
  -F "licensePlate=ABC-123" \
  -F "notes=Test damage"
```

---

## Possible Solutions

### Solution 1: Omit Empty Image Field
If the Image field doesn't accept empty lists, omit it entirely:

```python
# Only add Image field if there are actual images
if formatted_images:
    payload['field_6389835'] = formatted_images
```

**Status:** Already implemented in the fix above.

### Solution 2: Check Image Field Type in Baserow
The Image field might be configured as:
- **File field** - Expects file uploads, not URLs
- **URL field** - Expects just the URL string
- **Link field** - Expects specific format

**Action:** Run `debug_baserow_fields.py` to see the exact field type.

### Solution 3: Verify Cloudinary URLs
Ensure the Cloudinary URLs are valid and accessible:

```bash
# Test if URL is accessible
curl -I https://cloudinary.com/image.jpg
```

### Solution 4: Check Field Permissions
Ensure the API token has permission to write to the Image field.

---

## Testing the Fix

### Test 1: Submit Form Without Images
```bash
# Should work with the fix
POST /api/service-requests
  name: "John Doe"
  email: "john@example.com"
  phone: "+352 123 456"
  carBrand: "BMW"
  vin: "VIN123456"
  licensePlate: "ABC-123"
  notes: "Damage description"
  # No images
```

**Expected:** Success response with record ID

### Test 2: Submit Form With Images
```bash
# Should work with the fix
POST /api/service-requests
  name: "John Doe"
  email: "john@example.com"
  phone: "+352 123 456"
  carBrand: "BMW"
  vin: "VIN123456"
  licensePlate: "ABC-123"
  notes: "Damage description"
  images: [image1.jpg, image2.jpg]
```

**Expected:** Success response with record ID and image URLs

### Test 3: Check Baserow Record
After successful submission, verify the record in Baserow:
1. Go to Baserow Customer details table
2. Find the new record
3. Verify all fields are populated correctly
4. Check that images are linked properly

---

## Monitoring

### Key Logs to Watch
```bash
# Watch for Image field formatting
tail -f backend/logs/garagefy.log | grep "Formatted.*images"

# Watch for validation errors
tail -f backend/logs/garagefy.log | grep "Field error"

# Watch for API errors
tail -f backend/logs/garagefy.log | grep "Baserow API error"
```

### Metrics to Track
- Number of successful submissions
- Number of validation errors
- Which fields cause errors
- Image upload success rate

---

## Next Steps

1. **Run the debug script** to identify the exact issue
2. **Check the logs** for field-specific error messages
3. **Test the API** with the provided curl commands
4. **Verify Baserow configuration** matches the field mappings
5. **Monitor the logs** after deploying the fix

---

## Related Files

- `backend/app/services/baserow_service.py` - Main Baserow service
- `backend/app/api/endpoints/service_requests.py` - Service request endpoint
- `debug_baserow_fields.py` - Debugging script
- `backend/logs/garagefy.log` - Application logs

---

## Additional Resources

- [Baserow API Documentation](https://api.baserow.io/)
- [Baserow File Field Documentation](https://baserow.io/docs/api/database/fields/file)
- [Cloudinary URL Format](https://cloudinary.com/documentation/cloudinary_url_format)

---

## Summary

The fix improves image field handling and adds comprehensive error logging to identify validation issues. The debug script helps identify which specific field is causing the problem, allowing for targeted fixes.

**Status:** Ready for testing
