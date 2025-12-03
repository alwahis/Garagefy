#!/usr/bin/env python3
"""
Script to analyze empty rows in Baserow and identify their source
"""

import os
import sys
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

print("=" * 70)
print("EMPTY ROWS ANALYZER")
print("=" * 70)

# Step 1: Initialize Baserow service
print("\n[STEP 1] Initializing Baserow service...")
print("-" * 70)

try:
    from backend.app.services.baserow_service import BaserowService
    baserow = BaserowService()
    print(f"  [OK] Baserow service initialized")
    print(f"  [OK] Database ID: {baserow.database_id}")
except Exception as e:
    print(f"  [FAIL] Failed to initialize Baserow service: {str(e)}")
    sys.exit(1)

# Step 2: Fetch all records from Recevied email table
print("\n[STEP 2] Fetching all records from 'Recevied email' table...")
print("-" * 70)

try:
    records = baserow.get_records('Recevied email')
    print(f"  [OK] Found {len(records)} total records")
except Exception as e:
    print(f"  [FAIL] Failed to fetch records: {str(e)}")
    sys.exit(1)

# Step 3: Analyze records for empty VINs
print("\n[STEP 3] Analyzing records for empty VINs...")
print("-" * 70)

empty_vin_records = []
valid_records = []

for record in records:
    fields = record.get('fields', {})
    vin = fields.get('VIN') or fields.get('field_6389842', '')
    
    if not vin or not str(vin).strip():
        empty_vin_records.append(record)
    else:
        valid_records.append(record)

print(f"  [INFO] Valid records (with VIN): {len(valid_records)}")
print(f"  [INFO] Empty records (no VIN): {len(empty_vin_records)}")

# Step 4: Display empty records
if empty_vin_records:
    print("\n[STEP 4] Empty Records Details:")
    print("-" * 70)
    
    for i, record in enumerate(empty_vin_records[-10:]):  # Show last 10
        fields = record.get('fields', {})
        print(f"\n  Record {i+1} (ID: {record.get('id')}):")
        print(f"    Email: {fields.get('Email') or fields.get('field_6389838', 'EMPTY')}")
        print(f"    Subject: {fields.get('Subject') or fields.get('field_6389839', 'EMPTY')}")
        print(f"    Body: {(fields.get('Body') or fields.get('field_6389840', 'EMPTY'))[:50]}...")
        print(f"    VIN: {fields.get('VIN') or fields.get('field_6389842', 'EMPTY')}")
        print(f"    Created: {fields.get('created_on', 'UNKNOWN')}")
        
        # Check if all fields are empty
        all_fields_empty = all(
            not (fields.get(k) or fields.get(v, ''))
            for k, v in [
                ('Email', 'field_6389838'),
                ('Subject', 'field_6389839'),
                ('Body', 'field_6389840'),
                ('VIN', 'field_6389842')
            ]
        )
        
        if all_fields_empty:
            print(f"    ⚠️  ALL FIELDS EMPTY - Likely created by automation or webhook")
        else:
            print(f"    ⚠️  PARTIAL DATA - Missing VIN but has other fields")
else:
    print("\n  [OK] No empty records found! ✅")

# Step 5: Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if empty_vin_records:
    print(f"\n⚠️  Found {len(empty_vin_records)} records without VIN")
    print("\nPossible sources:")
    print("  1. Baserow automation creating records")
    print("  2. Baserow webhook receiving empty data")
    print("  3. Manual entries in Baserow UI")
    print("  4. Old code still running somewhere")
    print("\nNext steps:")
    print("  1. Check Baserow automations")
    print("  2. Check Baserow webhooks")
    print("  3. Check Baserow audit log")
    print("  4. Verify latest code is deployed")
else:
    print("\n✅ All records have VIN - No empty rows detected!")
    print("The validation is working correctly.")

print("\n" + "=" * 70)
