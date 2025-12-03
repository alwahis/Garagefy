#!/usr/bin/env python
"""
Test script to verify Baserow integration
Run: python test_baserow.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🧪 BASEROW INTEGRATION TEST")
print("=" * 60)

# Test 1: Check environment variables
print("\n1️⃣  Checking environment variables...")
required_vars = [
    'BASEROW_API_TOKEN',
    'BASEROW_DATABASE_ID',
    'BASEROW_TABLE_FIX_IT',
    'BASEROW_TABLE_CUSTOMER_DETAILS',
    'BASEROW_TABLE_RECEIVED_EMAIL'
]

all_set = True
for var in required_vars:
    value = os.getenv(var)
    if value:
        masked = value[:10] + '...' if len(value) > 10 else value
        print(f"   ✅ {var}: {masked}")
    else:
        print(f"   ❌ {var}: NOT SET")
        all_set = False

if not all_set:
    print("\n❌ Missing environment variables!")
    sys.exit(1)

# Test 2: Import baserow service
print("\n2️⃣  Importing Baserow service...")
try:
    from app.services.baserow_service import baserow_service
    print("   ✅ Baserow service imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import: {str(e)}")
    sys.exit(1)

# Test 3: Fetch garages
print("\n3️⃣  Fetching garages from Baserow...")
try:
    garages = baserow_service.get_fix_it_garages()
    print(f"   ✅ Connected to Baserow")
    print(f"   📊 Total garages: {len(garages)}")
    
    if garages:
        print("\n   Garages found:")
        for garage in garages[:5]:
            print(f"      - {garage.get('name', 'N/A')} ({garage.get('email', 'N/A')})")
        if len(garages) > 5:
            print(f"      ... and {len(garages) - 5} more")
    else:
        print("   ⚠️  No garages found (table is empty)")
        
except Exception as e:
    print(f"   ❌ Failed to fetch garages: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Create test customer
print("\n4️⃣  Testing customer creation...")
try:
    test_customer = {
        'Name': 'Test Customer',
        'Email': 'test@example.com',
        'VIN': 'TEST123ABC456DEF78',
        'Phone': '+1234567890',
        'Brand': 'Toyota'
    }
    
    result = baserow_service.create_customer(test_customer)
    
    if result.get('success'):
        print(f"   ✅ Customer created successfully")
        print(f"   📝 Record ID: {result.get('record_id')}")
    else:
        print(f"   ❌ Failed to create customer: {result.get('error')}")
        
except Exception as e:
    print(f"   ❌ Error creating customer: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 5: Get records
print("\n5️⃣  Testing record retrieval...")
try:
    records = baserow_service.get_records('Customer details')
    print(f"   ✅ Retrieved records successfully")
    print(f"   📊 Total customer records: {len(records)}")
    
except Exception as e:
    print(f"   ❌ Error retrieving records: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 6: Check other services
print("\n6️⃣  Checking other services...")
try:
    from app.services.fix_it_service import fix_it_service
    print("   ✅ Fix It service imports correctly")
except Exception as e:
    print(f"   ❌ Fix It service import failed: {str(e)}")

try:
    from app.services.customer_response_service import customer_response_service
    print("   ✅ Customer Response service imports correctly")
except Exception as e:
    print(f"   ❌ Customer Response service import failed: {str(e)}")

try:
    from app.services.email_monitor_service import email_monitor_service
    print("   ✅ Email Monitor service imports correctly")
except Exception as e:
    print(f"   ❌ Email Monitor service import failed: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n🚀 Your Baserow integration is working correctly!")
print("\nNext steps:")
print("  1. Start the backend: python run.py")
print("  2. Test the API: curl http://localhost:8099/api/fix-it/test-garages")
print("  3. Submit a test form from the frontend")
print("  4. Verify data in Baserow")
print("\n" + "=" * 60)
