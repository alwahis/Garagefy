# 📧 Customer Follow-up Email System

## Overview
Garagefy automatically sends a **consolidated quote email** to customers after they submit a repair request. The email is sent when **one of two conditions** is met:

1. ✅ **All garages have responded** (immediate notification)
2. ⏰ **2 business days have passed** (even if not all garages responded)

---

## How It Works

### 1. Customer Submits Request
- Customer fills out form with car details and damage photos
- Data saved to Airtable "Customer details" table
- Quote requests sent to all garages in "Fix it" table

### 2. Garages Respond
- Garages reply via email with quotes
- Email monitor service checks inbox every minute
- Responses saved to "Received email" table in Airtable
- Each response linked to VIN (Vehicle Identification Number)

### 3. Automated Follow-up Check
**Scheduler runs every minute** and checks:
- Has 2 business days passed since submission?
- Have all garages responded?

**If either condition is TRUE:**
- System compiles all received quotes
- Sends one consolidated email to customer
- Marks request as "sent" to prevent duplicates

### 4. Customer Receives Email
Email includes:
- ✅ All quotes received from garages
- 📞 Garage contact information (phone, email, address)
- 💰 Price estimates
- 💬 Full garage responses
- 📋 Next steps to book appointment

---

## Technical Details

### Scheduler Configuration
**File**: `backend/app/services/scheduler_service.py`

```python
# Runs every 1 minute
self.scheduler.add_job(
    func=self._send_customer_responses_task,
    trigger=IntervalTrigger(minutes=1),
    id='send_customer_responses',
    name='Send compiled quotes to customers'
)
```

### Business Logic
**File**: `backend/app/services/customer_response_service.py`

```python
# Check conditions (line 128)
should_send = all_garages_responded or business_days_passed >= 2

if should_send:
    reason = "all garages responded" if all_garages_responded else "2 business days passed"
    logger.info(f"Sending consolidated response for VIN {vin} ({reason})")
    await self._send_customer_response(record_id, fields, vin)
```

### Business Days Calculation
- **Excludes weekends** (Saturday & Sunday)
- Only counts Monday-Friday
- Example: Request on Friday → 2 business days = Tuesday

---

## Email Content

### Subject
```
🚗 Vos devis - [Car Brand]
```

### Body Includes
1. **Greeting** with customer name
2. **Vehicle info** (VIN, car brand)
3. **Quote cards** for each garage:
   - Garage name
   - Price estimate
   - Contact info (phone, email, address)
   - Full garage response
   - Date received
4. **Next steps** guide
5. **Garagefy branding** and contact

### Mobile-Friendly Design
- Responsive layout
- Large touch-friendly buttons
- Clear pricing display
- Easy-to-read cards

---

## Duplicate Prevention

### One Email Per VIN
- System groups requests by VIN
- Only sends **ONE consolidated email** per VIN
- Prevents multiple emails for same vehicle

### Tracking
- Uses "Sent Emails" field in Airtable
- Marks as: `"Quote sent on YYYY-MM-DD HH:MM:SS"`
- Skips records already marked as sent

### Auto-Cleanup
- Requests older than 7 days auto-marked as sent
- Prevents processing historical data

---

## Monitoring & Logs

### Check Scheduler Status
Look for these logs in Render:
```
[SCHEDULED] Starting customer response check at [timestamp]
[SCHEDULED] Customer response check completed: X responses sent
```

### Successful Email Send
```
Sending consolidated response for VIN [VIN] to [email] (all garages responded)
Successfully sent response to [email]
Marked record [id] for VIN [VIN] as sent
```

### No Action Needed
```
VIN [VIN]: X/Y garages responded. All responded: False
Business days passed: 1 (need 2)
```

---

## Configuration

### Timing Settings
**File**: `backend/app/services/customer_response_service.py`

```python
# Line 128: Change number of days
business_days_passed >= 2  # Change "2" to adjust timing
```

### Email Template
**File**: `backend/app/services/customer_response_service.py`
- Lines 397-444: HTML email template
- Lines 465-523: Quote cards builder

---

## Testing

### Manual Test
1. Submit a repair request via frontend
2. Wait 2 business days OR have all garages respond
3. Check customer email inbox
4. Verify consolidated quote email received

### Check Logs
```bash
# On Render dashboard
1. Go to: https://dashboard.render.com/web/srv-d3l5r2t3jqtc738he5d0/logs
2. Search for: "SCHEDULED] Customer response check"
3. Look for: "responses sent"
```

### Verify in Airtable
1. Open "Customer details" table
2. Check "Sent Emails" field
3. Should show: "Quote sent on [date]"

---

## Troubleshooting

### Email Not Sent After 2 Days
**Check:**
1. Is scheduler running? (Check Render logs)
2. Is "Sent Emails" field already populated?
3. Are business days calculated correctly? (excludes weekends)
4. Is submission date older than 7 days? (auto-marked as sent)

### Duplicate Emails
**Check:**
1. "Sent Emails" field should prevent duplicates
2. VIN grouping should consolidate records
3. Check logs for "already sent" messages

### No Quotes in Email
**Check:**
1. Are garages responding?
2. Is "Received email" table populated?
3. Does VIN match between tables?
4. Check email monitor service logs

---

## Summary

✅ **Automatic**: No manual intervention needed  
✅ **Smart Timing**: 2 days OR all responses  
✅ **No Duplicates**: One email per VIN  
✅ **Professional**: Beautiful, mobile-friendly design  
✅ **Complete Info**: All quotes + contact details  
✅ **Reliable**: Runs every minute, never misses  

The system is **fully automated** and **production-ready**! 🎉
