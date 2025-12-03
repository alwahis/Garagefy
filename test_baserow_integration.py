#!/usr/bin/env python3
"""
Comprehensive test script for Garagefy Baserow integration
Tests all aspects of the system to identify issues
"""

import os
import sys
import logging
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_environment_variables():
    """Test all required environment variables"""
    logger.info("=" * 60)
    logger.info("TESTING ENVIRONMENT VARIABLES")
    logger.info("=" * 60)
    
    required_vars = {
        'BASEROW_URL': 'https://api.baserow.io',
        'BASEROW_API_TOKEN': 'Required for API access',
        'BASEROW_DATABASE_ID': 'Required for database access',
        'BASEROW_TABLE_CUSTOMER_DETAILS': 'Required for customer records',
        'BASEROW_TABLE_FIX_IT': 'Required for garage records',
        'BASEROW_TABLE_RECEIVED_EMAIL': 'Required for email records',
        'MS_CLIENT_ID': 'Required for email sending',
        'MS_CLIENT_SECRET': 'Required for email sending',
        'MS_TENANT_ID': 'Required for email sending',
        'EMAIL_ADDRESS': 'Required for email sending',
        'CLOUDINARY_CLOUD_NAME': 'Required for image uploads',
        'CLOUDINARY_API_KEY': 'Required for image uploads',
        'CLOUDINARY_API_SECRET': 'Required for image uploads',
    }
    
    missing_vars = []
    present_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            present_vars.append(f"✅ {var}: {'*' * len(value) if 'SECRET' in var or 'TOKEN' in var else value}")
        else:
            missing_vars.append(f"❌ {var}: {description}")
    
    logger.info(f"Present variables ({len(present_vars)}):")
    for var in present_vars:
        logger.info(f"  {var}")
    
    if missing_vars:
        logger.error(f"Missing variables ({len(missing_vars)}):")
        for var in missing_vars:
            logger.error(f"  {var}")
        return False
    else:
        logger.info("✅ All required environment variables are present")
        return True

def test_baserow_connection():
    """Test Baserow API connection"""
    logger.info("=" * 60)
    logger.info("TESTING BASEROW CONNECTION")
    logger.info("=" * 60)
    
    try:
        from backend.app.services.baserow_service import baserow_service
        
        # Test initialization
        logger.info(f"Baserow URL: {baserow_service.base_url}")
        logger.info(f"Database ID: {baserow_service.database_id}")
        logger.info(f"API Token present: {'Yes' if baserow_service.api_token else 'No'}")
        logger.info(f"Table IDs: {baserow_service.table_ids}")
        
        # Test API connectivity
        endpoint = f'/api/database/rows/table/{baserow_service.table_ids["Fix it"]}/'
        response = baserow_service._make_request('GET', endpoint, params={'size': 1})
        
        logger.info("✅ Baserow API connection successful")
        logger.info(f"Sample response keys: {list(response.keys())}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Baserow connection failed: {str(e)}")
        return False

def test_garage_retrieval():
    """Test garage data retrieval"""
    logger.info("=" * 60)
    logger.info("TESTING GARAGE RETRIEVAL")
    logger.info("=" * 60)
    
    try:
        from backend.app.services.baserow_service import baserow_service
        
        garages = baserow_service.get_fix_it_garages()
        
        logger.info(f"Found {len(garages)} garages")
        
        if garages:
            logger.info("Sample garage data:")
            sample = garages[0]
            for key, value in sample.items():
                if isinstance(value, str) and len(value) > 100:
                    logger.info(f"  {key}: {value[:100]}...")
                else:
                    logger.info(f"  {key}: {value}")
            
            # Check for required fields
            required_fields = ['name', 'email']
            missing_fields = [f for f in required_fields if f not in sample or not sample[f]]
            
            if missing_fields:
                logger.warning(f"⚠️ Some garages missing required fields: {missing_fields}")
            else:
                logger.info("✅ All required fields present in garage data")
        else:
            logger.warning("⚠️ No garages found in Fix it table")
        
        return len(garages) > 0
        
    except Exception as e:
        logger.error(f"❌ Garage retrieval failed: {str(e)}")
        return False

def test_customer_creation():
    """Test customer record creation"""
    logger.info("=" * 60)
    logger.info("TESTING CUSTOMER CREATION")
    logger.info("=" * 60)
    
    try:
        from backend.app.services.baserow_service import baserow_service
        
        # Test data
        test_customer = {
            'Name': f'Test Customer {datetime.now().strftime("%Y%m%d%H%M%S")}',
            'Email': f'test_{datetime.now().strftime("%Y%m%d%H%M%S")}@example.com',
            'VIN': 'TEST123456789',
            'Phone': '+1234567890',
            'car_brand': 'Test Brand',
            'license_plate': 'TEST123',
            'notes': 'Test customer record for integration testing'
        }
        
        logger.info(f"Creating test customer: {test_customer['Email']}")
        
        result = baserow_service.create_customer(test_customer)
        
        logger.info(f"Creation result: {result}")
        
        if result.get('success'):
            logger.info(f"✅ Customer created successfully with ID: {result.get('record_id')}")
            
            # Verify the record was created
            if result.get('record_id'):
                # Try to retrieve the record
                table_id = baserow_service.table_ids['Customer details']
                endpoint = f'/api/database/rows/table/{table_id}/{result["record_id"]}/'
                record = baserow_service._make_request('GET', endpoint)
                
                logger.info("Retrieved record fields:")
                for key, value in record.items():
                    if key != 'id':
                        logger.info(f"  {key}: {value}")
                
                return True
        else:
            logger.error(f"❌ Customer creation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Customer creation test failed: {str(e)}")
        return False

def test_email_service():
    """Test email service configuration"""
    logger.info("=" * 60)
    logger.info("TESTING EMAIL SERVICE")
    logger.info("=" * 60)
    
    try:
        from backend.app.services.email_service import email_service
        
        logger.info(f"Email service initialized: {type(email_service)}")
        logger.info(f"User email: {email_service.user_email}")
        logger.info(f"Graph endpoint: {email_service.graph_endpoint}")
        logger.info(f"Client ID present: {'Yes' if email_service.client_id else 'No'}")
        logger.info(f"Tenant ID present: {'Yes' if email_service.tenant_id else 'No'}")
        
        # Test token acquisition (but don't send email)
        try:
            token = email_service._get_token()
            logger.info("✅ Email token acquisition successful")
            return True
        except Exception as e:
            logger.error(f"❌ Email token acquisition failed: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Email service test failed: {str(e)}")
        return False

def test_cloudinary():
    """Test Cloudinary configuration"""
    logger.info("=" * 60)
    logger.info("TESTING CLOUDINARY")
    logger.info("=" * 60)
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        config = cloudinary.config()
        logger.info(f"Cloud name: {config.cloud_name}")
        logger.info(f"API key present: {'Yes' if config.api_key else 'No'}")
        logger.info(f"API secret present: {'Yes' if config.api_secret else 'No'}")
        
        if config.cloud_name and config.api_key and config.api_secret:
            logger.info("✅ Cloudinary configuration complete")
            return True
        else:
            logger.error("❌ Cloudinary configuration incomplete")
            return False
            
    except Exception as e:
        logger.error(f"❌ Cloudinary test failed: {str(e)}")
        return False

def test_service_request_flow():
    """Test the complete service request flow"""
    logger.info("=" * 60)
    logger.info("TESTING SERVICE REQUEST FLOW")
    logger.info("=" * 60)
    
    try:
        from backend.app.services.fix_it_service import fix_it_service
        
        # Test data
        test_request = {
            'request_id': f'test_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'car_brand': 'Test Brand',
            'vin': 'TEST123456789',
            'license_plate': 'TEST123',
            'damage_notes': 'Test damage for integration testing',
            'image_urls': []  # No images for testing
        }
        
        logger.info("Testing quote request flow...")
        
        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                fix_it_service.send_quote_requests(
                    request_id=test_request['request_id'],
                    car_brand=test_request['car_brand'],
                    vin=test_request['vin'],
                    license_plate=test_request['license_plate'],
                    damage_notes=test_request['damage_notes'],
                    image_urls=test_request['image_urls']
                )
            )
            
            logger.info(f"Quote request result: {result}")
            
            if result.get('success'):
                logger.info(f"✅ Quote requests sent to {result.get('garages_contacted', 0)} garages")
                return True
            else:
                logger.error(f"❌ Quote request failed: {result.get('error')}")
                return False
                
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"❌ Service request flow test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting Garagefy Baserow Integration Test Suite")
    logger.info(f"Test started at: {datetime.now().isoformat()}")
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Baserow Connection", test_baserow_connection),
        ("Garage Retrieval", test_garage_retrieval),
        ("Customer Creation", test_customer_creation),
        ("Email Service", test_email_service),
        ("Cloudinary", test_cloudinary),
        ("Service Request Flow", test_service_request_flow),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            logger.info(f"\n{'='*20} {test_name} {'='*20}")
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info(f"\nTotal: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 All tests passed! The system is working correctly.")
    else:
        logger.error("⚠️ Some tests failed. Please check the logs above for details.")
    
    return failed == 0

if __name__ == "__main__":
    # Add backend to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
    
    # Run tests
    success = main()
    sys.exit(0 if success else 1)
