#!/usr/bin/env python3
"""
Check which garages received emails for a specific service request
"""
import sys
sys.path.insert(0, 'backend')

from app.services.airtable_service import airtable_service
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

def check_email_status():
    # Get the latest customer request
    table = airtable_service._get_table('Customer details')
    customers = table.all(sort=['-Date and Time'], max_records=5)
    
    print("=" * 80)
    print("RECENT SERVICE REQUESTS AND EMAIL STATUS")
    print("=" * 80)
    
    for idx, customer in enumerate(customers, 1):
        fields = customer['fields']
        vin = fields.get('VIN', 'N/A')
        name = fields.get('Name', 'N/A')
        date = fields.get('Date and Time', 'N/A')
        status = fields.get('Item Status', 'N/A')
        
        print(f"\n{idx}. Request Details:")
        print(f"   VIN: {vin}")
        print(f"   Customer: {name}")
        print(f"   Date: {date}")
        print(f"   Status: {status}")
        
        # Get all garages
        garages = airtable_service.get_fix_it_garages()
        print(f"\n   Garages that should have received email ({len(garages)} total):")
        for i, garage in enumerate(garages, 1):
            print(f"   {i}. {garage['name']}")
            print(f"      Email: {garage['email']}")
        
        print("\n   " + "-" * 76)

if __name__ == "__main__":
    check_email_status()
