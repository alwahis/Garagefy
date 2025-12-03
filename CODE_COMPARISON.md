# Airtable vs Baserow - Code Comparison

## Overview
This document shows side-by-side code comparisons for common operations.

---

## 1. Initialization

### Airtable
```python
from pyairtable import Api

class AirtableService:
    def __init__(self):
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.api = Api(api_key=self.api_key)
        self.table = None
```

### Baserow
```python
import requests

class BaserowService:
    def __init__(self):
        self.base_url = os.getenv('BASEROW_URL', 'https://api.baserow.io')
        self.api_token = os.getenv('BASEROW_API_TOKEN')
        self.database_id = os.getenv('BASEROW_DATABASE_ID')
        
        self.headers = {
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        self.table_ids = {
            'Customer details': int(os.getenv('BASEROW_TABLE_CUSTOMER_DETAILS')),
            'Fix it': int(os.getenv('BASEROW_TABLE_FIX_IT'))
        }
```

**Key Differences:**
- Airtable: Uses SDK with base ID
- Baserow: Uses HTTP with table IDs

---

## 2. Get All Records

### Airtable
```python
def get_all_records(self):
    table = self.api.table(self.base_id, 'Fix it')
    records = table.all()  # Automatic pagination
    
    result = []
    for record in records:
        fields = record.get('fields', {})
        result.append({
            'id': record.get('id'),
            'name': fields.get('Name'),
            'email': fields.get('Email')
        })
    return result
```

### Baserow
```python
def get_all_records(self):
    table_id = self.table_ids['Fix it']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    result = []
    page = 1
    
    while True:
        params = {'page': page, 'size': 100}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            break
        
        data = response.json()
        
        for record in data.get('results', []):
            result.append({
                'id': record.get('id'),
                'name': record.get('Name'),
                'email': record.get('Email')
            })
        
        if not data.get('next'):
            break
        page += 1
    
    return result
```

**Key Differences:**
- Airtable: Automatic pagination with `.all()`
- Baserow: Manual pagination with `page` parameter
- Airtable: Fields wrapped in `fields` dict
- Baserow: Fields directly in record

---

## 3. Create Record

### Airtable
```python
def create_customer(self, name, email):
    table = self.api.table(self.base_id, 'Customer details')
    
    record = table.create({
        'Name': name,
        'Email': email,
        'Date and Time': datetime.now(timezone.utc).isoformat()
    })
    
    return {
        'success': True,
        'record_id': record['id']
    }
```

### Baserow
```python
def create_customer(self, name, email):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    payload = {
        'Name': name,
        'Email': email,
        'Date and Time': datetime.now(timezone.utc).isoformat()
    }
    
    response = requests.post(url, headers=self.headers, json=payload)
    
    if response.status_code != 200:
        return {
            'success': False,
            'error': response.json().get('error')
        }
    
    record = response.json()
    return {
        'success': True,
        'record_id': record['id']
    }
```

**Key Differences:**
- Airtable: SDK method returns record directly
- Baserow: HTTP POST returns JSON response
- Airtable: Exceptions on error
- Baserow: Check status code

---

## 4. Update Record

### Airtable
```python
def update_customer(self, record_id, data):
    table = self.api.table(self.base_id, 'Customer details')
    
    updated = table.update(record_id, data)
    
    return {
        'success': True,
        'record': updated
    }
```

### Baserow
```python
def update_customer(self, record_id, data):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/{record_id}/'
    
    response = requests.patch(url, headers=self.headers, json=data)
    
    if response.status_code != 200:
        return {
            'success': False,
            'error': response.json().get('error')
        }
    
    return {
        'success': True,
        'record': response.json()
    }
```

**Key Differences:**
- Airtable: `.update()` method
- Baserow: HTTP PATCH request
- Airtable: Exceptions on error
- Baserow: Check status code

---

## 5. Delete Record

### Airtable
```python
def delete_customer(self, record_id):
    table = self.api.table(self.base_id, 'Customer details')
    
    table.delete(record_id)
    
    return {'success': True}
```

### Baserow
```python
def delete_customer(self, record_id):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/{record_id}/'
    
    response = requests.delete(url, headers=self.headers)
    
    if response.status_code != 204:
        return {
            'success': False,
            'error': 'Delete failed'
        }
    
    return {'success': True}
```

**Key Differences:**
- Airtable: `.delete()` method
- Baserow: HTTP DELETE request
- Baserow: Returns 204 on success

---

## 6. Filter Records

### Airtable
```python
def get_customer_by_email(self, email):
    table = self.api.table(self.base_id, 'Customer details')
    
    records = table.all(
        formula=f'LOWER({{Email}}) = "{email.lower()}"'
    )
    
    return records
```

### Baserow (Option 1: Client-side)
```python
def get_customer_by_email(self, email):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    response = requests.get(url, headers=self.headers)
    records = response.json().get('results', [])
    
    # Filter client-side
    filtered = [r for r in records if r.get('Email', '').lower() == email.lower()]
    
    return filtered
```

### Baserow (Option 2: Server-side)
```python
def get_customer_by_email(self, email):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    # Field ID 4 is Email field
    filter_string = '4__text__equal=' + email
    params = {'filter': filter_string}
    
    response = requests.get(url, headers=self.headers, params=params)
    records = response.json().get('results', [])
    
    return records
```

**Key Differences:**
- Airtable: Formula language (like Excel)
- Baserow: Field-based filters or client-side filtering
- Baserow: Requires field ID for server-side filtering

---

## 7. Complex Filtering

### Airtable
```python
def get_pending_quotes(self):
    table = self.api.table(self.base_id, 'Received')
    
    records = table.all(
        formula='AND({Status} = "pending", {Response Date} > "2025-01-01")'
    )
    
    return records
```

### Baserow (Client-side)
```python
def get_pending_quotes(self):
    table_id = self.table_ids['Received']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    response = requests.get(url, headers=self.headers)
    records = response.json().get('results', [])
    
    # Filter client-side
    from datetime import datetime
    cutoff_date = datetime.fromisoformat('2025-01-01')
    
    filtered = [
        r for r in records
        if r.get('Status') == 'pending' and 
           datetime.fromisoformat(r.get('Response Date', '')) > cutoff_date
    ]
    
    return filtered
```

**Key Differences:**
- Airtable: Complex formula in one line
- Baserow: Multiple conditions in Python code

---

## 8. Error Handling

### Airtable
```python
def create_customer(self, data):
    try:
        table = self.api.table(self.base_id, 'Customer details')
        record = table.create(data)
        return record
    except Exception as e:
        # Airtable raises exceptions
        logger.error(f"Airtable error: {str(e)}")
        raise
```

### Baserow
```python
def create_customer(self, data):
    try:
        table_id = self.table_ids['Customer details']
        url = f'{self.base_url}/api/database/rows/table/{table_id}/'
        
        response = requests.post(url, headers=self.headers, json=data)
        
        # Check status code
        if response.status_code >= 400:
            error = response.json().get('error', 'Unknown error')
            logger.error(f"Baserow error: {error}")
            raise Exception(error)
        
        return response.json()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
```

**Key Differences:**
- Airtable: SDK raises exceptions
- Baserow: Check HTTP status codes
- Baserow: Parse error from JSON response

---

## 9. Batch Operations

### Airtable
```python
def create_multiple_records(self, records_list):
    table = self.api.table(self.base_id, 'Customer details')
    
    # Create one by one (no batch API)
    created = []
    for data in records_list:
        record = table.create(data)
        created.append(record)
    
    return created
```

### Baserow
```python
def create_multiple_records(self, records_list):
    table_id = self.table_ids['Customer details']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    # Baserow doesn't have batch API either
    # Create one by one
    created = []
    for data in records_list:
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            created.append(response.json())
    
    return created
```

**Key Differences:**
- Both: No batch API, must create one by one
- Baserow: Could add delays to avoid rate limiting

---

## 10. Pagination Handling

### Airtable
```python
def get_all_records_paginated(self):
    table = self.api.table(self.base_id, 'Fix it')
    
    # Automatic pagination
    for record in table.all():
        print(record)
```

### Baserow
```python
def get_all_records_paginated(self):
    table_id = self.table_ids['Fix it']
    url = f'{self.base_url}/api/database/rows/table/{table_id}/'
    
    page = 1
    while True:
        params = {'page': page, 'size': 100}
        response = requests.get(url, headers=self.headers, params=params)
        
        data = response.json()
        
        for record in data.get('results', []):
            print(record)
        
        # Check if there are more pages
        if not data.get('next'):
            break
        
        page += 1
```

**Key Differences:**
- Airtable: Automatic pagination with iterator
- Baserow: Manual pagination with page parameter
- Baserow: Must check `next` field

---

## 11. Field Mapping

### Airtable
```python
# Access fields by name directly
fields = record.get('fields', {})
name = fields.get('Name')
email = fields.get('Email')
```

### Baserow
```python
# Option 1: Access fields by name directly
name = record.get('Name')
email = record.get('Email')

# Option 2: Access fields by ID (if needed)
# field_id = 3
# value = record.get(f'field_{field_id}')
```

**Key Differences:**
- Airtable: Fields wrapped in `fields` dict
- Baserow: Fields directly in record
- Baserow: Can use field IDs if needed

---

## 12. Authentication

### Airtable
```python
# Token-based
api = Api(api_key='your_token')
```

### Baserow
```python
# Token-based
headers = {
    'Authorization': f'Token {api_token}',
    'Content-Type': 'application/json'
}

# Or JWT-based (for user authentication)
# headers = {
#     'Authorization': f'JWT {jwt_token}',
#     'Content-Type': 'application/json'
# }
```

**Key Differences:**
- Both: Token-based authentication
- Baserow: Also supports JWT
- Baserow: Must add to headers manually

---

## Summary Table

| Operation | Airtable | Baserow | Difficulty |
|-----------|----------|---------|-----------|
| Get all | `.all()` | Manual pagination | Medium |
| Get one | `.get(id)` | `GET /rows/{id}` | Low |
| Create | `.create(data)` | `POST /rows` | Low |
| Update | `.update(id, data)` | `PATCH /rows/{id}` | Low |
| Delete | `.delete(id)` | `DELETE /rows/{id}` | Low |
| Filter | `formula=...` | Field filters or client-side | Medium |
| Error handling | Exceptions | Status codes | Low |
| Pagination | Automatic | Manual | Medium |

---

## Migration Checklist

- [ ] Replace `pyairtable` with `requests`
- [ ] Update initialization (credentials and table IDs)
- [ ] Implement manual pagination
- [ ] Convert formulas to filters or client-side logic
- [ ] Update error handling (status codes)
- [ ] Test each operation
- [ ] Update imports in all services
- [ ] Run full test suite

