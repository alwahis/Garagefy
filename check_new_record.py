#!/usr/bin/env python3
"""
Check if the new record has VIN field populated
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.baserow_service import baserow_service

def check_record(record_id: int):
    """Check a specific record"""
    print(f"Checking record {record_id}...")
    
    try:
        table_id = baserow_service.table_ids['Customer details']
        endpoint = f'/api/database/rows/table/{table_id}/{record_id}/'
        record = baserow_service._make_request('GET', endpoint)
        
        print("\nRecord fields:")
        for key, value in record.items():
            if key != 'id' and key != 'order':
                # Check if it's a field ID
                if key.startswith('field_'):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value}")
        
        # Check specifically for VIN field
        vin_value = record.get('field_6389831')  # VIN field ID
        if vin_value:
            print(f"\n✅ VIN field populated: {vin_value}")
            return True
        else:
            print(f"\n❌ VIN field is empty")
            return False
            
    except Exception as e:
        print(f"Error checking record: {e}")
        return False

if __name__ == "__main__":
    # Check the latest record (53)
    success = check_record(53)
    
    # Also check one of the old records (52)
    print("\n" + "="*60)
    print("Comparing with old record 52:")
    check_record(52)
    
    sys.exit(0 if success else 1)
