#!/usr/bin/env python3
"""
Test writing a record to Baserow "Recevied email" table
Run this on Render where environment variables are set
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.baserow_service import baserow_service
from datetime import datetime, timezone
import json

print("=" * 80)
print("TEST: Write Record to Baserow 'Recevied email' Table")
print("=" * 80)
print()

# Test data
test_email = "test.garage@example.com"
test_subject = "Re: Repair Quote Request - VIN: TESTVIN1234567890A"
test_body = "I can fix this vehicle for 500 euros. Please confirm."
test_vin = "TESTVIN1234567890A"
test_received_at = datetime.now(timezone.utc).isoformat()

print("Test Record:")
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

try:
    result = baserow_service.store_received_email(email_data, test_vin)
    
    print("Result:")
    print(json.dumps(result, indent=2, default=str))
    print()
    
    if result and isinstance(result, dict):
        if result.get('id'):
            print(f"[SUCCESS] Record created with ID: {result.get('id')}")
            print()
            print("Go to Baserow and check the 'Recevied email' table:")
            print(f"  - Look for email: {test_email}")
            print(f"  - VIN should be: {test_vin}")
        elif 'error' in result:
            print(f"[ERROR] {result.get('error')}")
        else:
            print("[OK] Record stored (response received)")
    else:
        print(f"[WARNING] Unexpected result type: {type(result)}")

except Exception as e:
    print(f"[ERROR] Exception: {str(e)}")
    import traceback
    traceback.print_exc()
