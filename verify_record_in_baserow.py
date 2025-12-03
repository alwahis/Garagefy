#!/usr/bin/env python3
"""
Verify that the test record was written to Baserow
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 80)
print("VERIFY TEST RECORD IN BASEROW")
print("=" * 80)
print()

try:
    from app.services.baserow_service import baserow_service
    
    print("Fetching records from 'Recevied email' table...")
    print()
    
    # Fetch records
    records = baserow_service.get_records('Recevied email')
    
    print(f"Total records in table: {len(records)}")
    print()
    
    # Look for our test record
    test_vin = "TESTVIN9876543210Z"
    test_email = "test.garage@example.com"
    
    found = False
    for record in records:
        fields = record.get('fields', {})
        email = fields.get('field_6389838', '')
        vin = fields.get('field_6389842', '')
        subject = fields.get('field_6389839', '')
        
        if vin == test_vin and email == test_email:
            print(f"[SUCCESS] Test record found!")
            print()
            print("Record Details:")
            print(f"  ID: {record.get('id')}")
            print(f"  Email: {email}")
            print(f"  Subject: {subject}")
            print(f"  VIN: {vin}")
            print(f"  Body: {fields.get('field_6389840', '')[:100]}...")
            print(f"  Received At: {fields.get('field_6389841', '')}")
            print()
            found = True
            break
    
    if not found:
        print("[INFO] Test record not found in current fetch")
        print()
        print("Recent records in table:")
        print()
        
        # Show last 5 records
        for i, record in enumerate(records[-5:]):
            fields = record.get('fields', {})
            print(f"Record {i+1}:")
            print(f"  ID: {record.get('id')}")
            print(f"  Email: {fields.get('field_6389838', 'N/A')}")
            print(f"  VIN: {fields.get('field_6389842', 'N/A')}")
            print(f"  Subject: {fields.get('field_6389839', 'N/A')[:60]}...")
            print()

except Exception as e:
    print(f"[ERROR] Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
