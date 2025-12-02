#!/usr/bin/env python3
"""
Test script to write a test record to Baserow "Recevied email" table
This verifies that the Baserow connection and table configuration are correct
"""

import os
import sys
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("BASEROW WRITE TEST - Recevied email Table")
print("=" * 80)
print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Check environment variables
print("[STEP 1] Checking Environment Variables")
print("-" * 80)

required_vars = {
    'BASEROW_API_TOKEN': 'API Token for authentication',
    'BASEROW_DATABASE_ID': 'Database ID',
    'BASEROW_TABLE_RECEIVED_EMAIL': 'Table ID for Recevied email',
    'BASEROW_URL': 'Baserow API URL (optional, defaults to https://api.baserow.io)'
}

env_vars = {}
all_set = True

for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if 'TOKEN' in var:
            masked = value[:10] + '...' if len(value) > 10 else value
        else:
            masked = value
        print(f"[OK] {var}: {masked}")
        env_vars[var] = value
    else:
        print(f"[MISSING] {var}: NOT SET")
        all_set = False

print()

if not all_set:
    print("[ERROR] Missing environment variables!")
    print("Please set the following in your .env file or Render environment:")
    for var in required_vars:
        if var not in env_vars:
            print(f"  - {var}")
    sys.exit(1)

# Step 2: Initialize Baserow connection
print("[STEP 2] Initializing Baserow Connection")
print("-" * 80)

import requests

base_url = env_vars.get('BASEROW_URL', 'https://api.baserow.io')
api_token = env_vars['BASEROW_API_TOKEN']
database_id = env_vars['BASEROW_DATABASE_ID']
table_id = env_vars['BASEROW_TABLE_RECEIVED_EMAIL']

headers = {
    'Authorization': f'Token {api_token}',
    'Content-Type': 'application/json'
}

print(f"Base URL: {base_url}")
print(f"Database ID: {database_id}")
print(f"Table ID: {table_id}")
print(f"API Token: {api_token[:10]}...")
print()

# Step 3: Create test data
print("[STEP 3] Preparing Test Data")
print("-" * 80)

test_email = "test.garage@example.com"
test_subject = "Re: Repair Quote Request - VIN: TESTVIN1234567890A"
test_body = "I can fix this vehicle for 500 euros. Please confirm."
test_vin = "TESTVIN1234567890A"
test_received_at = datetime.now(timezone.utc).isoformat()

# Field mappings for "Recevied email" table
# field_6389838 = Email
# field_6389839 = Subject
# field_6389840 = Body
# field_6389841 = Received At
# field_6389842 = VIN

payload = {
    'field_6389838': test_email,           # Email
    'field_6389839': test_subject,         # Subject
    'field_6389840': test_body,            # Body
    'field_6389841': test_received_at,     # Received At
    'field_6389842': test_vin               # VIN
}

print("Test Record Data:")
print(json.dumps(payload, indent=2))
print()

# Step 4: Write to Baserow
print("[STEP 4] Writing to Baserow")
print("-" * 80)

try:
    endpoint = f'{base_url}/api/database/rows/table/{table_id}/'
    print(f"Endpoint: {endpoint}")
    print()
    
    print("Sending POST request to Baserow...")
    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print(f"Response Status Code: {response.status_code}")
    print()
    
    if response.status_code >= 400:
        print("[ERROR] Request failed!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        try:
            error_json = response.json()
            print(f"Error JSON: {json.dumps(error_json, indent=2)}")
        except:
            pass
        
        sys.exit(1)
    
    response_data = response.json()
    print("[SUCCESS] Record written to Baserow!")
    print()
    print("Response Data:")
    print(json.dumps(response_data, indent=2))
    print()
    
    # Extract record ID
    record_id = response_data.get('id')
    if record_id:
        print(f"Record ID: {record_id}")
        print()
    
except requests.exceptions.Timeout:
    print("[ERROR] Request timeout!")
    sys.exit(1)
except requests.exceptions.ConnectionError as e:
    print(f"[ERROR] Connection error: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Verify the record
print("[STEP 5] Verifying Record in Baserow")
print("-" * 80)

try:
    print("Fetching the record we just created...")
    
    # Fetch all records and find our test record
    get_endpoint = f'{base_url}/api/database/rows/table/{table_id}/'
    get_response = requests.get(
        get_endpoint,
        headers=headers,
        params={'size': 100},
        timeout=30
    )
    
    if get_response.status_code == 200:
        records = get_response.json().get('results', [])
        print(f"Total records in table: {len(records)}")
        print()
        
        # Find our test record
        found = False
        for record in records:
            fields = record.get('fields', {})
            email = fields.get('field_6389838', '')
            vin = fields.get('field_6389842', '')
            
            if email == test_email and vin == test_vin:
                print("[SUCCESS] Test record found in Baserow!")
                print()
                print("Record Details:")
                print(f"  ID: {record.get('id')}")
                print(f"  Email: {fields.get('field_6389838', 'N/A')}")
                print(f"  Subject: {fields.get('field_6389839', 'N/A')}")
                print(f"  Body: {fields.get('field_6389840', 'N/A')}")
                print(f"  VIN: {fields.get('field_6389842', 'N/A')}")
                print(f"  Received At: {fields.get('field_6389841', 'N/A')}")
                print()
                found = True
                break
        
        if not found:
            print("[WARNING] Record not found in fetch results")
            print("This might be due to:")
            print("  1. Record was created but not yet visible in fetch")
            print("  2. Different table or database")
            print("  3. Duplicate detection skipped the record")
    else:
        print(f"[WARNING] Could not fetch records: {get_response.status_code}")
        print(f"Response: {get_response.text}")

except Exception as e:
    print(f"[WARNING] Could not verify record: {str(e)}")

print()

# Summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print()
print("[SUCCESS] Test completed!")
print()
print("What this test did:")
print("1. Verified environment variables are set")
print("2. Connected to Baserow API")
print("3. Created a test record in 'Recevied email' table with:")
print(f"   - Email: {test_email}")
print(f"   - Subject: {test_subject}")
print(f"   - VIN: {test_vin}")
print()
print("Next Steps:")
print("1. Go to Baserow")
print(f"2. Open database {database_id}")
print(f"3. Open table {table_id} (Recevied email)")
print("4. Look for the test record with:")
print(f"   - Email: {test_email}")
print(f"   - VIN: {test_vin}")
print()
print("If you see the record, the Baserow connection is working correctly!")
print("If you don't see it, check:")
print("  - Are you looking at the correct database and table?")
print("  - Is the API token valid?")
print("  - Are the field IDs correct?")
