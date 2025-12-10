# Hardcoded Field IDs Fix for Received Email Table

## Problem
The system could write to the **Customer Details** table but not to the **Received Email** table.

## Root Cause
- **Customer Details table**: Used hardcoded field IDs (e.g., `field_6389828`) ✅ Always worked
- **Received Email table**: Used dynamic field ID lookup by name ❌ Failed if field names didn't match exactly

The dynamic lookup function `_get_field_id_by_name()` would return `None` if:
- Field names had different casing (e.g., "VIN" vs "vin")
- Field names had different spacing (e.g., "Received At" vs "ReceivedAt")
- Field names were slightly different

## Solution Applied
Changed the **Received Email** table to use **hardcoded field IDs** like the Customer Details table.

### Changes Made to `backend/app/services/baserow_service.py`

#### 1. Field IDs Already Defined (lines 47-54)
```python
self.received_email_fields = {
    'VIN': 6389838,      # VIN field
    'Email': 6389839,    # Garage email
    'Subject': 6389840,  # Email subject
    'Body': 6389841,     # Email body
    'Received At': 6389842,  # Timestamp
    'Quote': 6389843,    # Extracted quote/price
}
```

#### 2. Updated `store_received_email()` function (lines 714-740)
**Before:**
```python
# Dynamic lookup - could fail
field_email = self._get_field_id_by_name(table_id, 'Email')
field_subject = self._get_field_id_by_name(table_id, 'Subject')
# ... etc
```

**After:**
```python
# Hardcoded - always works
field_vin = self.received_email_fields['VIN']
field_email = self.received_email_fields['Email']
field_subject = self.received_email_fields['Subject']
field_body = self.received_email_fields['Body']
field_received_at = self.received_email_fields['Received At']
field_quote = self.received_email_fields['Quote']

# Build payload directly
payload = {
    f'field_{field_vin}': vin,
    f'field_{field_email}': email_data.get('from_email', '').strip().lower(),
    f'field_{field_subject}': email_data.get('subject', 'No Subject'),
    f'field_{field_body}': email_data.get('body', ''),
    f'field_{field_received_at}': email_data.get('received_at', datetime.now(timezone.utc).isoformat()),
}
```

#### 3. Updated `record_garage_response()` function (lines 808-834)
Applied the same hardcoded field ID approach.

## Benefits
✅ **Reliable**: No longer depends on exact field name matches  
✅ **Consistent**: Same approach as Customer Details table  
✅ **Predictable**: Field IDs are fixed and won't change  

## Important Notes
⚠️ If you recreate the "Received Email" table in Baserow, you MUST update these field IDs in the code.

## Testing
To verify the fix works:
1. Deploy the updated code to Render
2. Send a test email to trigger the email monitor
3. Check Baserow "Received Email" table for new records
4. Check Render logs for success messages: `✅ Stored email from...`

## Deployment
The changes are ready to deploy. No environment variable changes needed.
