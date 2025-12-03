#!/usr/bin/env python3
"""
Check Baserow field mappings for Customer details table
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.baserow_service import baserow_service

def get_table_fields(table_id: int):
    """Get field information for a table"""
    endpoint = f'/api/database/fields/table/{table_id}/'
    response = baserow_service._make_request('GET', endpoint)
    return response

def main():
    print("=" * 60)
    print("BASEROW FIELD MAPPINGS")
    print("=" * 60)
    
    # Customer details table
    customer_table_id = baserow_service.table_ids['Customer details']
    print(f"\nCustomer Details Table ID: {customer_table_id}")
    
    try:
        fields = get_table_fields(customer_table_id)
        print(f"\nFound {len(fields)} fields:")
        
        for field in fields:
            field_id = field.get('id')
            field_name = field.get('name')
            field_type = field.get('type')
            print(f"  field_{field_id}: {field_name} ({field_type})")
    except Exception as e:
        print(f"Error fetching fields: {e}")
    
    # Fix it table (for comparison)
    fixit_table_id = baserow_service.table_ids['Fix it']
    print(f"\n\nFix It Table ID: {fixit_table_id}")
    
    try:
        fields = get_table_fields(fixit_table_id)
        print(f"\nFound {len(fields)} fields:")
        
        for field in fields:
            field_id = field.get('id')
            field_name = field.get('name')
            field_type = field.get('type')
            print(f"  field_{field_id}: {field_name} ({field_type})")
    except Exception as e:
        print(f"Error fetching fields: {e}")

if __name__ == "__main__":
    main()
