#!/usr/bin/env python3
"""
Test if the field ID fix is deployed on Render
"""

import requests
import json
import sys

def test_deployment():
    """Test the current deployment"""
    print("Testing Render deployment...")
    
    # Test health endpoint
    try:
        response = requests.get("https://garagefy-1.onrender.com/health", timeout=10)
        if response.status_code == 200:
            print("PASS: Backend is running")
        else:
            print(f"FAIL: Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL: Cannot connect to backend: {e}")
        return False
    
    # Test service request endpoint with minimal data
    print("\nTesting service request endpoint...")
    
    test_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+1234567890',
        'carBrand': 'Test Brand',
        'vin': 'TESTVIN123',
        'licensePlate': 'TEST123',
        'notes': 'Test note',
        'requestId': 'test-123'
    }
    
    try:
        response = requests.post(
            "https://garagefy-1.onrender.com/api/service-requests",
            data=test_data,
            timeout=30
        )
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("PASS: Service request successful")
            return True
        else:
            print("FAIL: Service request failed")
            return False
            
    except Exception as e:
        print(f"FAIL: Service request error: {e}")
        return False

if __name__ == "__main__":
    success = test_deployment()
    sys.exit(0 if success else 1)
