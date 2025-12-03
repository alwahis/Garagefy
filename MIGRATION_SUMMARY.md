# Airtable to Baserow Migration - Executive Summary

## Quick Overview

Migrating Garagefy from Airtable to Baserow requires:
- **Effort**: Medium (2-3 weeks)
- **Risk**: Low (can rollback easily)
- **Cost Savings**: Significant (especially with self-hosted)
- **Downtime**: Minimal (can run parallel)

---

## What Needs to Change

### 1. Backend Service Layer (High Impact)

| Component | Current (Airtable) | New (Baserow) | Complexity |
|-----------|-------------------|---------------|-----------|
| **Library** | `pyairtable` SDK | `requests` HTTP | Low |
| **Authentication** | API Token | API Token | Low |
| **Table Access** | By name | By numeric ID | Medium |
| **Record IDs** | Alphanumeric | Numeric | Low |
| **Filtering** | Formula language | Field-based filters | Medium |
| **Pagination** | Automatic | Manual | Medium |
| **Error Handling** | SDK exceptions | HTTP status codes | Low |

### 2. Files Affected

```
backend/
├── requirements.txt                          [MODIFY] Remove pyairtable
├── .env                                      [MODIFY] Add Baserow variables
├── app/
│   ├── services/
│   │   ├── airtable_service.py              [DELETE or REPLACE]
│   │   ├── baserow_service.py               [CREATE]
│   │   ├── customer_response_service.py     [UPDATE import]
│   │   ├── email_monitor_service.py         [UPDATE import]
│   │   ├── fix_it_service.py                [UPDATE import]
│   │   └── scheduler_service.py             [NO CHANGE]
│   └── api/
│       └── endpoints/
│           └── fix_it.py                    [UPDATE import]
```

### 3. Environment Variables

**Remove:**
```env
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...
```

**Add:**
```env
BASEROW_URL=https://api.baserow.io
BASEROW_API_TOKEN=...
BASEROW_DATABASE_ID=...
BASEROW_TABLE_CUSTOMER_DETAILS=...
BASEROW_TABLE_FIX_IT=...
BASEROW_TABLE_RECEIVED_EMAIL=...
BASEROW_TABLE_RECEIVED=...
```

---

## Detailed Changes by File

### File 1: `requirements.txt`

```diff
  fastapi
  uvicorn
  python-dotenv
  python-multipart
  requests
- pyairtable
  msal
  cloudinary
  apscheduler
  sqlalchemy
  psycopg2-binary
  aiohttp
```

**Action**: Remove `pyairtable` line

---

### File 2: `backend/app/services/baserow_service.py` (NEW)

**Create new file** with these key methods:

```python
class BaserowService:
    def __init__(self):
        # Initialize with Baserow credentials
        
    def get_fix_it_garages(self) -> List[Dict]:
        # Fetch garages with pagination
        
    def create_customer(self, data: dict) -> Dict:
        # Create customer record
        
    def get_records(self, table_name: str) -> List[Dict]:
        # Get records with optional filtering
        
    def update_record(self, table_name: str, record_id: int, data: Dict) -> Dict:
        # Update record
        
    def store_received_email(self, email_data: Dict, vin: str) -> Dict:
        # Store email in Recevied email table
        
    def record_garage_response(self, response_data: Dict) -> Dict:
        # Record garage response
```

**See**: `BASEROW_SERVICE_TEMPLATE.py` for full implementation

---

### File 3: `backend/app/services/customer_response_service.py`

**Change line 4:**
```python
# OLD:
from .airtable_service import airtable_service

# NEW:
from .baserow_service import baserow_service as airtable_service
```

**Why**: Keeps interface the same, just swaps backend

---

### File 4: `backend/app/services/email_monitor_service.py`

**Change line 10:**
```python
# OLD:
from .airtable_service import airtable_service

# NEW:
from .baserow_service import baserow_service as airtable_service
```

---

### File 5: `backend/app/services/fix_it_service.py`

**Change line 4:**
```python
# OLD:
from .airtable_service import airtable_service

# NEW:
from .baserow_service import baserow_service as airtable_service
```

---

### File 6: `backend/app/api/endpoints/fix_it.py`

**Change line 111:**
```python
# OLD:
from ...services.airtable_service import airtable_service

# NEW:
from ...services.baserow_service import baserow_service as airtable_service
```

---

## API Comparison

### Getting Records

**Airtable:**
```python
table = api.table(base_id, 'Fix it')
records = table.all()
```

**Baserow:**
```python
url = f'{base_url}/api/database/rows/table/{table_id}/'
response = requests.get(url, headers=headers, params={'page': 1})
records = response.json()['results']
```

### Creating Records

**Airtable:**
```python
record = table.create({
    'Name': 'Garage Name',
    'Email': 'garage@example.com'
})
```

**Baserow:**
```python
response = requests.post(
    f'{base_url}/api/database/rows/table/{table_id}/',
    headers=headers,
    json={'Name': 'Garage Name', 'Email': 'garage@example.com'}
)
record = response.json()
```

### Updating Records

**Airtable:**
```python
table.update(record_id, {'Status': 'completed'})
```

**Baserow:**
```python
requests.patch(
    f'{base_url}/api/database/rows/table/{table_id}/{record_id}/',
    headers=headers,
    json={'Status': 'completed'}
)
```

### Filtering

**Airtable:**
```python
records = table.all(formula='AND({VIN} = "ABC123", {Email} = "test@example.com")')
```

**Baserow:**
```python
# Option 1: Client-side filtering
records = get_all_records()
filtered = [r for r in records if r['VIN'] == 'ABC123' and r['Email'] == 'test@example.com']

# Option 2: Server-side filtering (more complex)
filter_string = '3__text__equal=ABC123&4__text__equal=test@example.com'
response = requests.get(url, params={'filter': filter_string})
```

---

## Migration Steps

### Phase 1: Preparation (Day 1)
- [ ] Create Baserow account
- [ ] Create database and tables
- [ ] Get all IDs (database, tables, fields)
- [ ] Generate API token
- [ ] Document all IDs

### Phase 2: Development (Days 2-5)
- [ ] Create `baserow_service.py`
- [ ] Implement all methods
- [ ] Update imports in 5 files
- [ ] Update `requirements.txt`
- [ ] Update `.env` with Baserow credentials

### Phase 3: Testing (Days 6-8)
- [ ] Unit test each method
- [ ] Integration test with scheduler
- [ ] End-to-end test (form → email → Baserow)
- [ ] Performance testing
- [ ] Error handling testing

### Phase 4: Deployment (Days 9-10)
- [ ] Deploy to staging
- [ ] Run full test suite
- [ ] Deploy to production
- [ ] Monitor logs
- [ ] Verify all systems working

### Phase 5: Cleanup (Day 11)
- [ ] Remove old Airtable service (optional)
- [ ] Update documentation
- [ ] Archive Airtable data (optional)

---

## Testing Checklist

### Unit Tests
- [ ] `get_fix_it_garages()` returns list of garages
- [ ] `create_customer()` creates record with correct ID
- [ ] `get_records()` returns records
- [ ] `update_record()` updates fields
- [ ] `store_received_email()` stores email
- [ ] `record_garage_response()` records response

### Integration Tests
- [ ] Scheduler can fetch garages
- [ ] Email service can store emails
- [ ] Customer response service can update records
- [ ] Fix it service can create customers

### End-to-End Tests
- [ ] Submit form on frontend
- [ ] Customer record created in Baserow
- [ ] Emails sent to garages
- [ ] Garage reply captured
- [ ] Customer receives compiled quotes

---

## Rollback Plan

If migration fails:

```bash
# Step 1: Revert code
git checkout backend/app/services/airtable_service.py

# Step 2: Update imports back
# In customer_response_service.py, email_monitor_service.py, etc.
# Change: from .baserow_service import baserow_service
# To: from .airtable_service import airtable_service

# Step 3: Update .env
# Remove Baserow variables
# Add back Airtable variables

# Step 4: Restart backend
python backend/run.py
```

**Estimated rollback time**: 15 minutes

---

## Cost Analysis

### Current (Airtable)
- **Free tier**: Limited (1,200 records)
- **Pro tier**: $20/month
- **API calls**: Counted against limit
- **Storage**: Per record

### Baserow Cloud
- **Free tier**: Unlimited
- **Pro tier**: $10/month
- **API calls**: Unlimited
- **Storage**: Unlimited

### Baserow Self-Hosted
- **Cost**: Free (Docker)
- **API calls**: Unlimited
- **Storage**: Unlimited
- **Maintenance**: Required

**Recommendation**: Start with Baserow Cloud ($10/month), migrate to self-hosted if needed.

---

## Performance Comparison

| Metric | Airtable | Baserow Cloud | Baserow Self-Hosted |
|--------|----------|---------------|-------------------|
| API Response Time | 200-500ms | 100-300ms | 50-200ms |
| Rate Limit | 5 req/sec | 10 req/sec | Unlimited |
| Pagination | Auto | Manual | Manual |
| Concurrent Users | Unlimited | Unlimited | Depends on server |
| Uptime SLA | 99.9% | 99.5% | Depends on setup |

---

## Known Limitations

### Baserow Limitations
1. **No formula language**: Use client-side filtering or API filters
2. **Manual pagination**: Must handle page parameter
3. **Field IDs**: Must map field names to numeric IDs
4. **Smaller ecosystem**: Fewer integrations than Airtable

### Workarounds
1. Implement filtering in Python code
2. Cache field ID mappings
3. Use field names in API (if supported)
4. Build custom integrations as needed

---

## Support & Resources

- **Baserow Docs**: https://baserow.io/docs
- **API Reference**: https://api.baserow.io/docs
- **Community**: https://community.baserow.io
- **GitHub**: https://github.com/bram2000/baserow
- **Docker Hub**: https://hub.docker.com/r/baserow/baserow

---

## Success Criteria

Migration is successful when:
- ✅ All tests pass
- ✅ Form submissions create records in Baserow
- ✅ Emails sent to garages
- ✅ Garage replies captured
- ✅ Customer responses sent
- ✅ No data loss
- ✅ Performance acceptable
- ✅ No errors in logs

---

## Timeline & Effort

| Phase | Duration | Effort | Risk |
|-------|----------|--------|------|
| Preparation | 1 day | Low | Low |
| Development | 4 days | Medium | Medium |
| Testing | 3 days | Medium | Low |
| Deployment | 2 days | Low | Medium |
| Cleanup | 1 day | Low | Low |
| **Total** | **11 days** | **Medium** | **Low** |

---

## Next Steps

1. **Read full guide**: `AIRTABLE_TO_BASEROW_MIGRATION.md`
2. **Quick start**: `BASEROW_QUICK_START.md`
3. **Review template**: `BASEROW_SERVICE_TEMPLATE.py`
4. **Create Baserow account**: https://baserow.io
5. **Set up database and tables**
6. **Implement `baserow_service.py`**
7. **Run tests**
8. **Deploy**

---

## Questions?

Refer to:
- Full migration guide for detailed explanations
- Quick start for common issues
- Template for code examples
- Baserow docs for API details

