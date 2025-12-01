#!/usr/bin/env python3
"""
Debug script to identify Baserow field validation issues
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Baserow credentials
BASEROW_URL = os.getenv('BASEROW_URL', 'https://api.baserow.io')
BASEROW_API_TOKEN = os.getenv('BASEROW_API_TOKEN')
BASEROW_DATABASE_ID = os.getenv('BASEROW_DATABASE_ID')
BASEROW_TABLE_CUSTOMER_DETAILS = int(os.getenv('BASEROW_TABLE_CUSTOMER_DETAILS', 0))

if not BASEROW_API_TOKEN or not BASEROW_DATABASE_ID or not BASEROW_TABLE_CUSTOMER_DETAILS:
    print("ERROR: Missing required environment variables")
    print(f"  BASEROW_API_TOKEN: {bool(BASEROW_API_TOKEN)}")
    print(f"  BASEROW_DATABASE_ID: {BASEROW_DATABASE_ID}")
    print(f"  BASEROW_TABLE_CUSTOMER_DETAILS: {BASEROW_TABLE_CUSTOMER_DETAILS}")
    sys.exit(1)

headers = {
    'Authorization': f'Token {BASEROW_API_TOKEN}',
    'Content-Type': 'application/json'
}

def get_table_fields():
    """Get all fields in the Customer details table"""
    print(f"\n[*] Fetching fields for table {BASEROW_TABLE_CUSTOMER_DETAILS}...")
    
    url = f"{BASEROW_URL}/api/database/tables/{BASEROW_TABLE_CUSTOMER_DETAILS}/fields/"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"ERROR: Failed to get fields - {response.status_code}")
        print(response.text)
        return None
    
    fields = response.json()
    print(f"\n[+] Found {len(fields)} fields:")
    
    field_map = {}
    for field in fields:
        field_id = field['id']
        field_name = field['name']
        field_type = field['field_type']
        field_map[field_id] = {
            'name': field_name,
            'type': field_type,
            'id': field_id
        }
        print(f"  field_{field_id} = {field_name} ({field_type})")
        
        # Print field-specific configuration
        if field_type == 'file':
            print(f"    -> File field configuration: {json.dumps(field, indent=6)}")
    
    return field_map

def test_create_record(field_map):
    """Test creating a record with various field combinations"""
    print(f"\n[*] Testing record creation...")
    
    # Find the field IDs we need
    name_field = None
    email_field = None
    image_field = None
    
    for field_id, info in field_map.items():
        if info['name'] == 'Name':
            name_field = field_id
        elif info['name'] == 'Email':
            email_field = field_id
        elif info['name'] == 'Image':
            image_field = field_id
    
    if not name_field or not email_field:
        print("ERROR: Could not find Name or Email fields")
        return
    
    print(f"\nField mapping:")
    print(f"  Name field: field_{name_field}")
    print(f"  Email field: field_{email_field}")
    print(f"  Image field: field_{image_field if image_field else 'NOT FOUND'}")
    
    # Test 1: Minimal record (just Name and Email)
    print(f"\n[TEST 1] Creating record with just Name and Email...")
    payload = {
        f'field_{name_field}': 'Test Customer',
        f'field_{email_field}': 'test@example.com'
    }
    
    url = f"{BASEROW_URL}/api/database/rows/table/{BASEROW_TABLE_CUSTOMER_DETAILS}/"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"[+] SUCCESS: Record created")
        record_id = response.json().get('id')
        print(f"    Record ID: {record_id}")
        
        # Delete the test record
        delete_url = f"{BASEROW_URL}/api/database/rows/table/{BASEROW_TABLE_CUSTOMER_DETAILS}/{record_id}/"
        requests.delete(delete_url, headers=headers)
        print(f"    Deleted test record")
    else:
        print(f"[-] FAILED: {response.status_code}")
        print(f"    Response: {response.text}")
        return
    
    # Test 2: Record with Image field (empty list)
    if image_field:
        print(f"\n[TEST 2] Creating record with Image field (empty list)...")
        payload = {
            f'field_{name_field}': 'Test Customer 2',
            f'field_{email_field}': 'test2@example.com',
            f'field_{image_field}': []
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"[+] SUCCESS: Record created with empty image list")
            record_id = response.json().get('id')
            print(f"    Record ID: {record_id}")
            
            # Delete the test record
            delete_url = f"{BASEROW_URL}/api/database/rows/table/{BASEROW_TABLE_CUSTOMER_DETAILS}/{record_id}/"
            requests.delete(delete_url, headers=headers)
            print(f"    Deleted test record")
        else:
            print(f"[-] FAILED: {response.status_code}")
            print(f"    Response: {response.text}")
        
        # Test 3: Record with Image field (with URL)
        print(f"\n[TEST 3] Creating record with Image field (with URL)...")
        payload = {
            f'field_{name_field}': 'Test Customer 3',
            f'field_{email_field}': 'test3@example.com',
            f'field_{image_field}': [{'url': 'https://example.com/image.jpg'}]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"[+] SUCCESS: Record created with image URL")
            record_id = response.json().get('id')
            print(f"    Record ID: {record_id}")
            
            # Delete the test record
            delete_url = f"{BASEROW_URL}/api/database/rows/table/{BASEROW_TABLE_CUSTOMER_DETAILS}/{record_id}/"
            requests.delete(delete_url, headers=headers)
            print(f"    Deleted test record")
        else:
            print(f"[-] FAILED: {response.status_code}")
            print(f"    Response: {response.text}")

if __name__ == '__main__':
    print("=" * 60)
    print("Baserow Field Debugging Script")
    print("=" * 60)
    
    field_map = get_table_fields()
    if field_map:
        test_create_record(field_map)
    
    print("\n" + "=" * 60)
    print("Debug complete")
    print("=" * 60)
