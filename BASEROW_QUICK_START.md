# Baserow Migration - Quick Start Guide

## TL;DR - What Changes

### 1. Install Baserow
```bash
# Cloud: https://baserow.io
# Self-hosted: docker-compose up
```

### 2. Update Dependencies
```bash
# Remove from requirements.txt
pyairtable

# Keep (already present)
requests
```

### 3. Create New Service File
Create `/backend/app/services/baserow_service.py` with HTTP-based API calls instead of SDK.

### 4. Update Environment Variables
```env
# Remove
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...

# Add
BASEROW_URL=https://api.baserow.io
BASEROW_API_TOKEN=your_token
BASEROW_DATABASE_ID=123
BASEROW_TABLE_CUSTOMER_DETAILS=456
BASEROW_TABLE_FIX_IT=457
BASEROW_TABLE_RECEIVED_EMAIL=458
BASEROW_TABLE_RECEIVED=459
```

### 5. Update Imports (5 files)
```python
# In these files, change:
from .airtable_service import airtable_service
# To:
from .baserow_service import baserow_service as airtable_service

# Files:
# - backend/app/services/customer_response_service.py
# - backend/app/services/email_monitor_service.py
# - backend/app/services/fix_it_service.py
# - backend/app/api/endpoints/fix_it.py
```

---

## Key Differences

### API Calls

**Airtable (SDK):**
```python
table = api.table(base_id, 'Table Name')
records = table.all()
table.create({'Field': 'value'})
```

**Baserow (HTTP):**
```python
url = f'{base_url}/api/database/rows/table/{table_id}/'
response = requests.get(url, headers=headers)
response = requests.post(url, json=payload, headers=headers)
```

### Filtering

**Airtable:**
```python
formula='AND({VIN} = "ABC", {Email} = "test@example.com")'
```

**Baserow:**
```python
# Using field IDs (e.g., 3 for VIN, 4 for Email)
filter_string = '3__text__equal=ABC&4__text__equal=test@example.com'
```

### Pagination

**Airtable:**
```python
# Automatic
records = table.all()  # Gets all records
```

**Baserow:**
```python
# Manual
page = 1
while True:
    response = requests.get(url, params={'page': page})
    if not response.json().get('next'):
        break
    page += 1
```

---

## File Structure

```
backend/app/services/
├── airtable_service.py          ← DELETE (or keep as backup)
├── baserow_service.py           ← CREATE (new)
├── customer_response_service.py ← UPDATE import
├── email_monitor_service.py     ← UPDATE import
├── fix_it_service.py            ← UPDATE import
└── ...
```

---

## Method Mapping

| Method | Airtable | Baserow | Effort |
|--------|----------|---------|--------|
| `get_fix_it_garages()` | `table.all()` | `requests.get()` + pagination | Medium |
| `create_customer()` | `table.create()` | `requests.post()` | Low |
| `get_records()` | `table.all(formula=...)` | `requests.get(filter=...)` | Medium |
| `update_record()` | `table.update()` | `requests.patch()` | Low |
| `delete_record()` | `table.delete()` | `requests.delete()` | Low |
| `store_received_email()` | `table.create()` | `requests.post()` | Low |

---

## Baserow Setup (5 minutes)

1. **Create Account**: https://baserow.io
2. **Create Database**: Click "Create database"
3. **Create Tables**: Add 4 tables (Customer details, Fix it, Recevied email, Received)
4. **Add Fields**: Add fields to each table (see full guide)
5. **Get IDs**:
   - Database ID: From URL
   - Table IDs: Hover over table name
   - API Token: Account Settings → API Tokens
6. **Update .env**: Add all IDs and token

---

## Testing Steps

```bash
# 1. Test connection
curl -H "Authorization: Token YOUR_TOKEN" \
  https://api.baserow.io/api/database/rows/table/TABLE_ID/

# 2. Test create
curl -X POST -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Name":"Test","Email":"test@example.com"}' \
  https://api.baserow.io/api/database/rows/table/TABLE_ID/

# 3. Run backend tests
python -m pytest backend/tests/

# 4. Test full flow
# - Submit form on frontend
# - Check Baserow for new customer record
# - Verify emails sent to garages
```

---

## Common Issues & Fixes

### Issue 1: "Invalid table ID"
**Cause**: Table ID is wrong or not numeric
**Fix**: Get correct ID from Baserow UI (hover over table name)

### Issue 2: "Field not found"
**Cause**: Field name doesn't match exactly
**Fix**: Check field names in Baserow table (case-sensitive)

### Issue 3: "Pagination not working"
**Cause**: Not handling `next` URL or page parameter
**Fix**: Use `page` parameter and check `response.json().get('next')`

### Issue 4: "Rate limit exceeded"
**Cause**: Too many requests per second
**Fix**: Add delay between requests or use batch operations

### Issue 5: "Authentication failed"
**Cause**: Invalid API token or expired
**Fix**: Regenerate token in Baserow Account Settings

---

## Rollback (if needed)

```bash
# Revert to Airtable
git checkout backend/app/services/airtable_service.py

# Update imports back to airtable_service
# Update .env with Airtable credentials

# Restart backend
python backend/run.py
```

---

## Performance Tips

1. **Cache field IDs**: Don't fetch them on every request
2. **Batch operations**: Create multiple records in one request (if supported)
3. **Use pagination**: Don't fetch all records at once
4. **Self-host Baserow**: For unlimited API calls and storage
5. **Monitor logs**: Check for slow queries or errors

---

## Cost Comparison

| Plan | Airtable | Baserow Cloud | Baserow Self-Hosted |
|------|----------|---------------|-------------------|
| Free | Limited | Unlimited | Free |
| API Calls | Counted | Unlimited | Unlimited |
| Storage | Per record | Unlimited | Unlimited |
| Support | Yes | Community | Community |

**Recommendation**: Start with Baserow Cloud, migrate to self-hosted if needed.

---

## Next Steps

1. ✅ Read full migration guide: `AIRTABLE_TO_BASEROW_MIGRATION.md`
2. ✅ Create Baserow account and database
3. ✅ Create `baserow_service.py`
4. ✅ Update imports in 5 files
5. ✅ Update `.env` with Baserow credentials
6. ✅ Run tests
7. ✅ Deploy to production

---

## Support

- Baserow Docs: https://baserow.io/docs
- API Reference: https://api.baserow.io/docs
- Community: https://community.baserow.io
- GitHub: https://github.com/bram2000/baserow

