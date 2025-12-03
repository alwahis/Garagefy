# 🧪 Local Testing Guide - Baserow Integration

## Quick Start Testing

### Step 1: Run the Test Script
```bash
cd backend
python test_baserow.py
```

This will verify:
- ✅ Environment variables are set
- ✅ Baserow service imports correctly
- ✅ Can connect to Baserow API
- ✅ Can fetch garages
- ✅ Can create customers
- ✅ All services import correctly

---

## Manual Testing

### Test 1: Check Environment Variables
```bash
# Windows PowerShell
Get-Content backend\.env | Select-String "BASEROW"

# Output should show:
# BASEROW_URL=https://api.baserow.io
# BASEROW_API_TOKEN=1tPB2aQwDrecuCnYU8qRUW3jukpodVs8
# BASEROW_DATABASE_ID=328778
# BASEROW_TABLE_CUSTOMER_DETAILS=755537
# BASEROW_TABLE_FIX_IT=755536
# BASEROW_TABLE_RECEIVED_EMAIL=755538
```

### Test 2: Test Baserow Connection (Direct API)
```bash
# Test connection to Baserow API
curl -H "Authorization: Token 1tPB2aQwDrecuCnYU8qRUW3jukpodVs8" \
  "https://api.baserow.io/api/database/rows/table/755536/?page=1&size=10"

# Expected: JSON response with table data
```

### Test 3: Start Backend Server
```bash
cd backend
python run.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8099
# INFO:     Application startup complete
```

### Test 4: Test API Endpoints

#### Test Garages Endpoint
```bash
curl http://localhost:8099/api/fix-it/test-garages

# Expected response:
# {
#   "success": true,
#   "message": "Found X garages",
#   "garages": [...]
# }
```

#### Test Status Endpoint
```bash
curl http://localhost:8099/api/fix-it/status

# Expected response:
# {
#   "success": true,
#   "status": "operational",
#   "message": "Fix it service is running"
# }
```

### Test 5: Test Customer Creation (Python)
```python
import requests

# Create customer
response = requests.post(
    'http://localhost:8099/api/fix-it/submit',
    json={
        'name': 'Test Customer',
        'email': 'test@example.com',
        'vin': 'TEST123ABC456DEF78',
        'brand': 'Toyota',
        'phone': '+1234567890'
    }
)

print(response.json())
```

### Test 6: Verify Data in Baserow
1. Go to https://baserow.io
2. Open database 328778
3. Check "Customer details" table
4. Should see the test customer record

---

## Testing Checklist

### Connection Tests
- [ ] Environment variables loaded
- [ ] Baserow API responds
- [ ] Service imports without errors
- [ ] Can fetch garages list

### Service Tests
- [ ] `get_fix_it_garages()` returns data
- [ ] `create_customer()` creates record
- [ ] `get_records()` retrieves data
- [ ] `update_record()` modifies data
- [ ] `store_received_email()` stores email

### API Tests
- [ ] `/api/fix-it/test-garages` returns garages
- [ ] `/api/fix-it/status` returns status
- [ ] `/api/fix-it/check-emails` processes emails
- [ ] `/api/fix-it/send-customer-responses` sends responses

### End-to-End Tests
- [ ] Submit form from frontend
- [ ] Customer created in Baserow
- [ ] Email sent to garages
- [ ] Garage reply captured
- [ ] Customer response sent

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution**: Make sure you're in the `backend` directory
```bash
cd backend
python test_baserow.py
```

### Issue: "BASEROW_API_TOKEN not set"
**Solution**: Check `.env` file exists and has the token
```bash
cat backend\.env | grep BASEROW_API_TOKEN
```

### Issue: "Connection refused" to Baserow
**Solution**: Check internet connection and API token validity
```bash
curl -H "Authorization: Token YOUR_TOKEN" https://api.baserow.io/api/database/rows/table/755536/
```

### Issue: "Table not found"
**Solution**: Verify table IDs are correct
```bash
# Check table IDs in Baserow UI
# Fix it: 755536
# Customer details: 755537
# Recevied email: 755538
```

### Issue: "Authentication failed"
**Solution**: Regenerate API token in Baserow
1. Go to https://baserow.io
2. Account Settings → API Tokens
3. Create new token
4. Update `.env` file

---

## Performance Testing

### Test Response Times
```bash
# Fetch garages
time curl http://localhost:8099/api/fix-it/test-garages

# Expected: < 500ms

# Create customer
time curl -X POST http://localhost:8099/api/fix-it/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'

# Expected: < 1000ms
```

### Load Testing
```bash
# Using Apache Bench (if installed)
ab -n 100 -c 10 http://localhost:8099/api/fix-it/test-garages

# Expected: All requests successful, < 500ms avg response time
```

---

## Logging

### View Backend Logs
```bash
# While backend is running, check logs for:
# - Connection messages
# - API calls
# - Errors

# Look for:
# INFO: Initializing Baserow service
# INFO: Fetching garages from Fix it table
# INFO: Created customer record
```

### Enable Debug Logging
Edit `backend/app/main.py`:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

---

## Data Verification

### Check Baserow Data
1. Go to https://baserow.io
2. Open database 328778
3. Check each table:
   - **Fix it**: Should have garages (currently empty)
   - **Customer details**: Should have test customers
   - **Recevied email**: Should have emails from garages

### Export Data
```bash
# Export customer details as CSV
# In Baserow UI: Table menu → Export → CSV
```

---

## Next Steps After Testing

### If All Tests Pass ✅
1. Deploy to Render
2. Test on staging
3. Deploy to production
4. Monitor logs

### If Tests Fail ❌
1. Check error messages
2. Verify environment variables
3. Check Baserow connection
4. Review logs
5. Check table IDs

---

## Quick Commands

```bash
# Test script
python test_baserow.py

# Start backend
python run.py

# Test API
curl http://localhost:8099/api/fix-it/test-garages

# Check env
cat backend\.env | grep BASEROW

# View logs
Get-Content backend/logs/garagefy.log -Tail 50
```

---

## Support

If you encounter issues:

1. **Check logs**: Look for error messages
2. **Verify credentials**: Ensure API token is correct
3. **Test connection**: Use curl to test Baserow API
4. **Review code**: Check `baserow_service.py` for issues
5. **Check documentation**: See migration guides

---

## Success Indicators

✅ All tests pass
✅ API endpoints respond
✅ Data created in Baserow
✅ No errors in logs
✅ Response times acceptable
✅ Ready for deployment

