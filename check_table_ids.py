#!/usr/bin/env python3
"""
Check if Baserow table IDs are properly configured
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("BASEROW TABLE ID CONFIGURATION CHECK")
print("=" * 60)

table_ids = {
    'BASEROW_TABLE_CUSTOMER_DETAILS': os.getenv('BASEROW_TABLE_CUSTOMER_DETAILS', 'NOT SET'),
    'BASEROW_TABLE_FIX_IT': os.getenv('BASEROW_TABLE_FIX_IT', 'NOT SET'),
    'BASEROW_TABLE_RECEIVED_EMAIL': os.getenv('BASEROW_TABLE_RECEIVED_EMAIL', 'NOT SET'),
    'BASEROW_TABLE_QUOTES': os.getenv('BASEROW_TABLE_QUOTES', 'NOT SET'),
    'BASEROW_TABLE_SERVICE_REQUESTS': os.getenv('BASEROW_TABLE_SERVICE_REQUESTS', 'NOT SET'),
}

print("\nEnvironment Variables:")
for key, value in table_ids.items():
    status = "✅" if value != 'NOT SET' and value != '0' else "❌"
    print(f"  {status} {key}: {value}")

print("\n" + "=" * 60)

# Check if they're valid integers
print("\nValidation:")
for key, value in table_ids.items():
    if value == 'NOT SET':
        print(f"  ❌ {key}: NOT SET - Please set this environment variable")
    elif value == '0':
        print(f"  ❌ {key}: 0 - Invalid table ID (should be a positive integer)")
    else:
        try:
            int_val = int(value)
            if int_val > 0:
                print(f"  ✅ {key}: {value} (valid)")
            else:
                print(f"  ❌ {key}: {value} (invalid - must be positive)")
        except ValueError:
            print(f"  ❌ {key}: {value} (invalid - not an integer)")

print("\n" + "=" * 60)
print("IMPORTANT: The 'Recevied email' table is used for storing garage responses")
print(f"Current value: {table_ids['BASEROW_TABLE_RECEIVED_EMAIL']}")
print("=" * 60)
