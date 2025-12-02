#!/usr/bin/env python3
"""
Check Baserow configuration from environment variables
This script helps diagnose if Baserow is properly configured
"""

import os
import sys

print("=" * 80)
print("BASEROW CONFIGURATION CHECK")
print("=" * 80)
print()

# Check all Baserow-related environment variables
baserow_vars = [
    'BASEROW_URL',
    'BASEROW_API_TOKEN',
    'BASEROW_DATABASE_ID',
    'BASEROW_TABLE_CUSTOMER_DETAILS',
    'BASEROW_TABLE_FIX_IT',
    'BASEROW_TABLE_RECEIVED_EMAIL',
    'BASEROW_TABLE_QUOTES',
    'BASEROW_TABLE_SERVICE_REQUESTS'
]

print("Environment Variables Status:")
print("-" * 80)

found_count = 0
for var in baserow_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if 'TOKEN' in var:
            display = value[:15] + '...' if len(value) > 15 else value
        else:
            display = value
        print(f"[SET]   {var}: {display}")
        found_count += 1
    else:
        print(f"[UNSET] {var}")

print()
print(f"Summary: {found_count}/{len(baserow_vars)} variables set")
print()

# Check if we can import BaserowService
print("Checking BaserowService Import:")
print("-" * 80)

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    from app.services.baserow_service import BaserowService
    print("[OK] BaserowService imported successfully")
    print()
    
    # Try to initialize
    try:
        service = BaserowService()
        print("[OK] BaserowService initialized successfully")
        print()
        print("Baserow Service Configuration:")
        print(f"  Base URL: {service.base_url}")
        print(f"  Database ID: {service.database_id}")
        print(f"  Table IDs:")
        for table_name, table_id in service.table_ids.items():
            status = "[OK]" if table_id and table_id != 0 else "[MISSING]"
            print(f"    {status} {table_name}: {table_id}")
        print()
        
        # Check if we can make a test request
        print("Testing Baserow API Connection:")
        print("-" * 80)
        
        try:
            # Try to fetch from Customer details table
            customer_table_id = service.table_ids.get('Customer details', 0)
            if customer_table_id and customer_table_id != 0:
                endpoint = f'/api/database/rows/table/{customer_table_id}/'
                params = {'size': 1}
                
                print(f"Fetching from Customer details table (ID: {customer_table_id})...")
                response = service._make_request('GET', endpoint, params=params)
                
                if response:
                    print("[OK] Baserow API is responding")
                    print(f"     Found {response.get('count', 0)} total records")
                else:
                    print("[ERROR] Baserow API returned empty response")
            else:
                print("[WARNING] Customer details table ID not configured")
        
        except Exception as e:
            print(f"[ERROR] Could not connect to Baserow API: {str(e)}")
        
    except ValueError as e:
        print(f"[ERROR] Could not initialize BaserowService: {str(e)}")
        print()
        print("This usually means:")
        print("  - BASEROW_API_TOKEN is not set")
        print("  - BASEROW_DATABASE_ID is not set")
        print()
        print("These must be set in Render environment variables")
    
except ImportError as e:
    print(f"[ERROR] Could not import BaserowService: {str(e)}")

print()
print("=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)
print()

if found_count == 0:
    print("No Baserow environment variables are set!")
    print()
    print("To set them, go to:")
    print("1. Render Dashboard")
    print("2. Your Garagefy API service")
    print("3. Settings → Environment")
    print("4. Add the following variables:")
    print()
    print("   BASEROW_URL = https://api.baserow.io")
    print("   BASEROW_API_TOKEN = [your token from Baserow]")
    print("   BASEROW_DATABASE_ID = [your database ID]")
    print("   BASEROW_TABLE_CUSTOMER_DETAILS = [table ID]")
    print("   BASEROW_TABLE_FIX_IT = [table ID]")
    print("   BASEROW_TABLE_RECEIVED_EMAIL = [table ID]")
    print()
    print("To get table IDs:")
    print("1. Go to Baserow")
    print("2. Open your database")
    print("3. Click on each table")
    print("4. Look at the URL: /table/[TABLE_ID]/")
    print("5. Copy the TABLE_ID number")
elif found_count < len(baserow_vars):
    print(f"Only {found_count}/{len(baserow_vars)} variables are set")
    print()
    print("Missing variables:")
    for var in baserow_vars:
        if not os.getenv(var):
            print(f"  - {var}")
else:
    print("All Baserow variables are configured!")
    print()
    print("The system should be able to:")
    print("  1. Connect to Baserow API")
    print("  2. Read from Customer details table")
    print("  3. Write to Recevied email table")
    print("  4. Process garage responses")
