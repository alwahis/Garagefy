# Airtable to Baserow Migration Guide

## Overview
This document outlines all changes required to migrate Garagefy from Airtable to Baserow as the database backend.

---

## 1. Architecture Comparison

### Airtable
- **API**: REST API with `pyairtable` library
- **Authentication**: Personal Access Token
- **Tables**: Named tables accessed by name
- **Records**: Record IDs are alphanumeric strings (e.g., `rec123abc`)
- **Fields**: Dynamic field names, accessed by field name
- **Formulas**: Airtable formula language

### Baserow
- **API**: REST API with HTTP requests (no official Python SDK)
- **Authentication**: API Token or JWT
- **Tables**: Accessed by table ID (numeric)
- **Records**: Record IDs are numeric
- **Fields**: Accessed by field ID (numeric)
- **Filters**: Baserow filter language (different syntax)

---

## 2. Required Changes by File

### A. Dependencies (requirements.txt)

**Current:**
```
pyairtable
```

**New:**
```
requests  # Already present
# Remove: pyairtable
```

**Action**: Remove `pyairtable`, keep `requests` for HTTP calls.

---

### B. Service Layer: Create New `baserow_service.py`

Create: `/backend/app/services/baserow_service.py`

**Key Differences:**
1. Use `requests` library instead of `pyairtable`
2. All API calls are HTTP-based
3. Need to map table names to table IDs
4. Need to map field names to field IDs
5. Different error handling

**Implementation Structure:**

```python
import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

class BaserowService:
    def __init__(self):
        self.base_url = os.getenv('BASEROW_URL', 'https://api.baserow.io')
        self.api_token = os.getenv('BASEROW_API_TOKEN')
        self.database_id = os.getenv('BASEROW_DATABASE_ID')
        
        if not self.api_token:
            raise ValueError("Missing BASEROW_API_TOKEN in .env")
        if not self.database_id:
            raise ValueError("Missing BASEROW_DATABASE_ID in .env")
        
        self.headers = {
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        # Table ID mappings (get these from Baserow UI)
        self.table_ids = {
            'Customer details': int(os.getenv('BASEROW_TABLE_CUSTOMER_DETAILS')),
            'Fix it': int(os.getenv('BASEROW_TABLE_FIX_IT')),
            'Recevied email': int(os.getenv('BASEROW_TABLE_RECEIVED_EMAIL')),
            'Received': int(os.getenv('BASEROW_TABLE_RECEIVED'))
        }
        
        # Field ID mappings (get these from Baserow API)
        self.field_ids = {}
        self._initialize_field_ids()
        
        self.logger = logging.getLogger(__name__)
    
    def _initialize_field_ids(self):
        """Fetch and cache field IDs for all tables"""
        # This needs to be called once to map field names to IDs
        pass
    
    def _get_fields(self, table_id: int) -> Dict[str, int]:
        """Get field mappings for a table"""
        url = f'{self.base_url}/api/database/tables/{table_id}/fields/'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to get fields: {response.text}")
        
        fields = {}
        for field in response.json():
            fields[field['name']] = field['id']
        
        return fields
```

---

### C. Environment Variables (.env)

**Add to .env:**

```env
# Baserow Configuration
BASEROW_URL=https://api.baserow.io
BASEROW_API_TOKEN=your_baserow_api_token_here
BASEROW_DATABASE_ID=your_database_id_here

# Table IDs (numeric IDs from Baserow)
BASEROW_TABLE_CUSTOMER_DETAILS=123
BASEROW_TABLE_FIX_IT=124
BASEROW_TABLE_RECEIVED_EMAIL=125
BASEROW_TABLE_RECEIVED=126

# Remove old Airtable variables
# AIRTABLE_API_KEY=...
# AIRTABLE_BASE_ID=...
```

---

## 3. Detailed Migration: Service Methods

### Method 1: `get_fix_it_garages()`

**Airtable:**
```python
def get_fix_it_garages(self) -> List[Dict[str, Any]]:
    table = self._get_table('Fix it')
    records = table.all()
    
    garages = []
    for record in records:
        fields = record.get('fields', {})
        garage = {
            'id': record.get('id'),
            'name': fields.get('Name', ''),
            'email': fields.get('Email', '')
        }
        garages.append(garage)
    return garages
```

**Baserow:**
```python
def get_fix_it_garages(self) -> List[Dict[str, Any]]:
    table_id = self.table_ids['Fix it']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    garages = []
    page = 1
    
    while True:
        params = {'page': page, 'size': 100}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            self.logger.error(f"Error fetching garages: {response.text}")
            break
        
        data = response.json()
        
        for record in data.get('results', []):
            garage = {
                'id': record.get('id'),
                'name': record.get('Name', ''),
                'email': record.get('Email', '')
            }
            if garage['email'] and '@' in garage['email']:
                garages.append(garage)
        
        # Check if there are more pages
        if not data.get('next'):
            break
        page += 1
    
    return garages
```

**Key Differences:**
- Baserow uses numeric table IDs, not names
- Pagination is manual (Airtable handles it)
- Field access is direct from record dict (no `fields` wrapper)
- Need to handle pagination with `page` parameter

---

### Method 2: `create_customer()`

**Airtable:**
```python
def create_customer(self, data: dict):
    table = self._get_table('Customer details')
    record_data = {
        'Name': data.get('Name'),
        'Email': data.get('Email'),
        'VIN': data.get('VIN')
    }
    record = table.create(record_data)
    return {'success': True, 'record_id': record['id']}
```

**Baserow:**
```python
def create_customer(self, data: dict):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    # Map field names to values
    payload = {
        'Name': data.get('Name'),
        'Email': data.get('Email'),
        'VIN': data.get('VIN'),
        'Date and Time': datetime.now(timezone.utc).isoformat()
    }
    
    response = requests.post(url, json=payload, headers=self.headers)
    
    if response.status_code != 200:
        error_msg = response.json().get('error', 'Unknown error')
        return {'success': False, 'error': error_msg, 'record_id': None}
    
    record = response.json()
    return {'success': True, 'record_id': record['id'], 'error': None}
```

**Key Differences:**
- Use HTTP POST instead of SDK method
- No field ID mapping needed if using field names directly
- Response structure is different
- Error handling is different

---

### Method 3: `get_records()` with Filtering

**Airtable:**
```python
def get_records(self, table_name: str, formula: str = ""):
    table = self._get_table(table_name)
    records = table.all(formula=formula)
    return records
```

**Baserow:**
```python
def get_records(self, table_name: str, filter_dict: Dict = None):
    table_id = self.table_ids[table_name]
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    params = {}
    
    # Baserow uses different filter syntax
    if filter_dict:
        # Example: {'field_name': 'Email', 'type': 'equal', 'value': 'test@example.com'}
        params['filter'] = self._build_baserow_filter(filter_dict)
    
    response = requests.get(url, headers=self.headers, params=params)
    
    if response.status_code != 200:
        self.logger.error(f"Error fetching records: {response.text}")
        return []
    
    return response.json().get('results', [])

def _build_baserow_filter(self, filter_dict: Dict) -> str:
    # Baserow filter format: field_id__field_type__filter_type=value
    # Example: 1__text__contains=hello
    pass
```

**Key Differences:**
- Airtable uses formula language (like Excel)
- Baserow uses field-based filters
- Need to convert filter logic
- Pagination handling required

---

## 4. Filter/Formula Conversion Examples

### Example 1: Simple Equality

**Airtable:**
```python
formula='LOWER(Email) = "test@example.com"'
```

**Baserow:**
```python
# Using field ID 5 for Email field
filter_string = '5__text__equal=test@example.com'
```

### Example 2: AND Condition

**Airtable:**
```python
formula='AND({VIN} = "ABC123", {Email} = "garage@example.com")'
```

**Baserow:**
```python
# Baserow filter format: field_id__type__filter=value
# Multiple filters are combined with &
filter_string = '3__text__equal=ABC123&4__text__equal=garage@example.com'
```

### Example 3: Contains

**Airtable:**
```python
formula='FIND("quote", {Notes}) > 0'
```

**Baserow:**
```python
# Using field ID 6 for Notes
filter_string = '6__text__contains=quote'
```

---

## 5. File-by-File Changes

### 5.1 `/backend/app/services/airtable_service.py`

**Action**: Replace with `baserow_service.py`

**All methods to migrate:**
1. `get_fix_it_garages()` - ✅ See example above
2. `get_all_garages()` - Similar to above
3. `create_customer()` - ✅ See example above
4. `create_record()` - Similar pattern
5. `get_record()` - Use GET with record ID
6. `get_records()` - ✅ See example above
7. `update_record()` - Use PATCH request
8. `store_received_email()` - POST to Received Email table
9. `store_garage_quote()` - Update Customer record
10. `record_garage_response()` - POST to Received table

---

### 5.2 `/backend/app/services/customer_response_service.py`

**Changes:**
```python
# Line 4: Change import
from .airtable_service import airtable_service
# TO:
from .baserow_service import baserow_service as airtable_service

# Line 13: Update reference
self.airtable = airtable_service
# No change needed if using same interface
```

**Note**: If you keep the same method signatures, minimal changes needed.

---

### 5.3 `/backend/app/services/email_monitor_service.py`

**Changes:**
```python
# Line 10: Change import
from .airtable_service import airtable_service
# TO:
from .baserow_service import baserow_service as airtable_service
```

**Note**: Same as above - interface remains the same.

---

### 5.4 `/backend/app/services/fix_it_service.py`

**Changes:**
```python
# Line 4: Change import
from .airtable_service import airtable_service
# TO:
from .baserow_service import baserow_service as airtable_service
```

---

### 5.5 `/backend/app/api/endpoints/fix_it.py`

**Changes:**
```python
# Line 111: Change import
from ...services.airtable_service import airtable_service
# TO:
from ...services.baserow_service import baserow_service as airtable_service
```

---

## 6. API Endpoint Differences

### Baserow REST API Structure

**Get all records:**
```
GET /api/database/rows/table/{table_id}/
```

**Create record:**
```
POST /api/database/rows/table/{table_id}/
Content-Type: application/json

{
  "field_name": "value",
  "another_field": "another_value"
}
```

**Update record:**
```
PATCH /api/database/rows/table/{table_id}/{row_id}/
Content-Type: application/json

{
  "field_name": "new_value"
}
```

**Delete record:**
```
DELETE /api/database/rows/table/{table_id}/{row_id}/
```

**Filter records:**
```
GET /api/database/rows/table/{table_id}/?filter=field_id__type__filter=value
```

---

## 7. Setup Steps for Baserow

### Step 1: Create Baserow Account
- Go to https://baserow.io
- Create account or self-host
- Create a new database

### Step 2: Create Tables
Create these tables with the following fields:

**Table: Customer details**
- Name (Text)
- Email (Email)
- Phone (Phone)
- VIN (Text)
- Brand (Text)
- Plate Number (Text)
- Notes (Long text)
- Image (File)
- Date and Time (Date)
- Sent Emails (Text)

**Table: Fix it**
- Name (Text)
- Email (Email)
- Address (Text)
- Phone (Phone)
- Website (URL)
- Specialties (Text)
- Reviews (Text)

**Table: Recevied email**
- VIN (Text)
- Email (Email)
- Subject (Text)
- Body (Long text)
- Received At (Date)
- Quote (Text)

**Table: Received**
- Garage Name (Text)
- Email (Email)
- Request ID (Text)
- Quote Amount (Number)
- Notes (Long text)
- Status (Single select)
- Response Date (Date)

### Step 3: Get IDs
1. Get Database ID from URL: `https://baserow.io/database/{database_id}`
2. Get Table IDs from Baserow UI (hover over table name)
3. Get Field IDs from API: `GET /api/database/tables/{table_id}/fields/`

### Step 4: Generate API Token
1. Go to Account Settings
2. Create API Token
3. Add to `.env` as `BASEROW_API_TOKEN`

---

## 8. Testing Checklist

- [ ] Create `baserow_service.py` with all methods
- [ ] Update imports in all service files
- [ ] Test `get_fix_it_garages()` returns garages
- [ ] Test `create_customer()` creates record
- [ ] Test `get_records()` with filters
- [ ] Test `update_record()` updates fields
- [ ] Test `store_received_email()` stores emails
- [ ] Test scheduler tasks work
- [ ] Test email sending flow end-to-end
- [ ] Test customer response generation

---

## 9. Rollback Plan

If migration fails:
1. Keep Airtable service file as backup
2. Revert imports to use `airtable_service`
3. Restore from git: `git checkout backend/app/services/airtable_service.py`

---

## 10. Performance Considerations

### Airtable vs Baserow

| Aspect | Airtable | Baserow |
|--------|----------|---------|
| Pagination | Automatic | Manual (100 records/page) |
| Rate Limiting | 5 req/sec | 10 req/sec (self-hosted: unlimited) |
| Field Access | By name | By name or ID |
| Filtering | Formula language | Field-based filters |
| Attachments | Built-in | File field type |

**Optimization Tips:**
1. Cache field ID mappings
2. Batch operations where possible
3. Use pagination efficiently
4. Consider self-hosted Baserow for higher limits

---

## 11. Cost Comparison

| Feature | Airtable | Baserow |
|---------|----------|---------|
| Free Tier | Limited | Unlimited |
| API Calls | Counted | Unlimited (self-hosted) |
| Storage | Per record | Unlimited (self-hosted) |
| Self-hosting | Not available | Available |

**Recommendation**: Use Baserow Cloud for simplicity or self-hosted for unlimited usage.

---

## 12. Migration Timeline

1. **Week 1**: Create `baserow_service.py`, test basic operations
2. **Week 2**: Update all imports, test integrations
3. **Week 3**: End-to-end testing, performance tuning
4. **Week 4**: Deploy to production, monitor

---

## Summary of Changes

| Component | Changes | Effort |
|-----------|---------|--------|
| Dependencies | Remove `pyairtable`, use `requests` | Low |
| Services | Create `baserow_service.py` | High |
| Imports | Update 5 files | Low |
| Environment | Add Baserow variables | Low |
| Testing | Full end-to-end test | Medium |
| **Total** | | **Medium-High** |

---

## References

- Baserow API Docs: https://api.baserow.io/docs
- Baserow Self-Hosting: https://baserow.io/docs
- Migration Support: Contact Baserow support

