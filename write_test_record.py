#!/usr/bin/env python3
"""
Write a test record directly to Baserow "Recevied email" table
This verifies that Baserow connection and table configuration are working
"""

import sys
import os
import json
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 80)
print("WRITE TEST RECORD TO BASEROW")
print("=" * 80)
print()

try:
    # Import the Baserow service
    from app.services.baserow_service import baserow_service
    print("[OK] Baserow service imported")
    print()
    
    # Verify configuration
    print("Configuration:")
    print(f"  Base URL: {baserow_service.base_url}")
    print(f"  Database ID: {baserow_service.database_id}")
    print(f"  Table ID (Recevied email): {baserow_service.table_ids.get('Recevied email', 'NOT SET')}")
    print()
    
    # Create test data
    test_email = "test.garage@example.com"
    test_subject = "Re: Repair Quote Request - VIN: TESTVIN9876543210Z"
    test_body = "I can fix this vehicle for 500 euros. Please confirm."
    test_vin = "TESTVIN9876543210Z"
    test_received_at = datetime.now(timezone.utc).isoformat()
    
    print("Test Record Data:")
    print(f"  Email: {test_email}")
    print(f"  Subject: {test_subject}")
    print(f"  Body: {test_body}")
    print(f"  VIN: {test_vin}")
    print(f"  Received At: {test_received_at}")
    print()
    
    # Prepare email data
    email_data = {
        'from_email': test_email,
        'subject': test_subject,
        'body': test_body,
        'received_at': test_received_at,
        'attachments': []
    }
    
    print("Calling store_received_email()...")
    print()
    
    # Call the store method
    result = baserow_service.store_received_email(email_data, test_vin)
    
    print("Result:")
    print(json.dumps(result, indent=2, default=str))
    print()
    
    # Check result
    if result:
        if isinstance(result, dict):
            if result.get('id'):
                print(f"[SUCCESS] Record created with ID: {result.get('id')}")
                print()
                print("Go to Baserow and verify:")
                print(f"  Database: 328778")
                print(f"  Table: 755538 (Recevied email)")
                print(f"  Look for record with:")
                print(f"    - Email: {test_email}")
                print(f"    - VIN: {test_vin}")
                sys.exit(0)
            elif 'error' in result:
                print(f"[ERROR] {result.get('error')}")
                sys.exit(1)
            else:
                print("[OK] Record stored (response received)")
                print()
                print("Go to Baserow and verify the record appears")
                sys.exit(0)
        else:
            print(f"[OK] Response received: {result}")
            sys.exit(0)
    else:
        print("[ERROR] No response from store_received_email()")
        sys.exit(1)

except Exception as e:
    print(f"[ERROR] Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
