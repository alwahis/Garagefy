#!/usr/bin/env python3
"""
Test script to verify garage response storage in Baserow
"""

import os
import sys
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("GARAGE RESPONSE STORAGE TEST")
print("=" * 70)

# Step 1: Check environment variables
print("\n[STEP 1] Checking environment variables...")
print("-" * 70)

required_vars = {
    'BASEROW_API_TOKEN': os.getenv('BASEROW_API_TOKEN'),
    'BASEROW_DATABASE_ID': os.getenv('BASEROW_DATABASE_ID'),
    'BASEROW_TABLE_RECEIVED_EMAIL': os.getenv('BASEROW_TABLE_RECEIVED_EMAIL'),
}

all_set = True
for var_name, var_value in required_vars.items():
    if var_value and var_value != '0':
        print(f"  [OK] {var_name}: {var_value[:20]}..." if len(str(var_value)) > 20 else f"  [OK] {var_name}: {var_value}")
    else:
        print(f"  [FAIL] {var_name}: NOT SET or 0")
        all_set = False

if not all_set:
    print("\n[FAIL] ERROR: Missing required environment variables!")
    print("Please set BASEROW_TABLE_RECEIVED_EMAIL in your .env file")
    sys.exit(1)

# Step 2: Initialize Baserow service
print("\n[STEP 2] Initializing Baserow service...")
print("-" * 70)

try:
    from backend.app.services.baserow_service import BaserowService
    baserow = BaserowService()
    print(f"  [OK] Baserow service initialized")
    print(f"  [OK] Database ID: {baserow.database_id}")
    print(f"  [OK] Table IDs: {json.dumps(baserow.table_ids, indent=4)}")
except Exception as e:
    print(f"  [FAIL] Failed to initialize Baserow service: {str(e)}")
    sys.exit(1)

# Step 3: Test storing an email
print("\n[STEP 3] Testing email storage...")
print("-" * 70)

test_email_data = {
    'from_email': 'test-garage@example.com',
    'subject': 'Test Response - VIN TEST123456',
    'body': 'This is a test garage response. Price estimate: 500€',
    'received_at': datetime.now(timezone.utc).isoformat()
}

test_vin = 'TEST123456'

try:
    print(f"  Storing test email for VIN: {test_vin}")
    print(f"  Email data: {json.dumps(test_email_data, indent=2)}")
    
    result = baserow.store_received_email(test_email_data, test_vin)
    
    if result and 'id' in result:
        print(f"  [OK] Email stored successfully!")
        print(f"  [OK] Record ID: {result['id']}")
        print(f"  [OK] Full response: {json.dumps(result, indent=2)}")
    elif result and result.get('success') == False:
        print(f"  [FAIL] Failed to store email: {result.get('error')}")
    else:
        print(f"  [WARN] Unexpected response: {json.dumps(result, indent=2)}")
        
except Exception as e:
    print(f"  [FAIL] Error storing email: {str(e)}")
    import traceback
    traceback.print_exc()

# Step 4: Test recording a garage response
print("\n[STEP 4] Testing garage response recording...")
print("-" * 70)

test_response_data = {
    'garage_name': 'Test Garage',
    'garage_email': 'response-garage@example.com',
    'subject': 'Response to Service Request',
    'body': 'We can fix your car for 600€',
    'vin': 'TEST789012',
    'response_date': datetime.now(timezone.utc).isoformat()
}

try:
    print(f"  Recording test garage response for VIN: {test_response_data['vin']}")
    print(f"  Response data: {json.dumps(test_response_data, indent=2)}")
    
    result = baserow.record_garage_response(test_response_data)
    
    if result and result.get('success'):
        print(f"  [OK] Garage response recorded successfully!")
        print(f"  [OK] Record ID: {result.get('record', {}).get('id')}")
        print(f"  [OK] Full response: {json.dumps(result, indent=2)}")
    elif result and result.get('success') == False:
        print(f"  [FAIL] Failed to record response: {result.get('error')}")
    else:
        print(f"  [WARN] Unexpected response: {json.dumps(result, indent=2)}")
        
except Exception as e:
    print(f"  [FAIL] Error recording response: {str(e)}")
    import traceback
    traceback.print_exc()

# Step 5: Verify records in Baserow
print("\n[STEP 5] Verifying records in Baserow...")
print("-" * 70)

try:
    print(f"  Fetching records from 'Recevied email' table...")
    records = baserow.get_records('Recevied email')
    
    if records:
        print(f"  [OK] Found {len(records)} records in 'Recevied email' table")
        
        # Show the most recent records
        print(f"\n  Most recent records:")
        for i, record in enumerate(records[-3:]):  # Show last 3
            fields = record.get('fields', {})
            print(f"\n    Record {i+1}:")
            print(f"      ID: {record.get('id')}")
            print(f"      Email: {fields.get('Email') or fields.get('field_6389838', 'N/A')}")
            print(f"      Subject: {fields.get('Subject') or fields.get('field_6389839', 'N/A')}")
            print(f"      VIN: {fields.get('VIN') or fields.get('field_6389842', 'N/A')}")
    else:
        print(f"  [WARN] No records found in 'Recevied email' table")
        
except Exception as e:
    print(f"  [FAIL] Error fetching records: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nSummary:")
print("  - If all steps show [OK], garage response storage is working!")
print("  - If you see [FAIL], check the error messages above")
print("  - If you see [WARN], there may be a configuration issue")
print("\n" + "=" * 70)
