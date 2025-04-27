#!/usr/bin/env python3
"""
Comprehensive Test Script for Used Car Check Feature with ALLDATA Integration

This script tests the Used Car Check feature by:
1. Testing the backend API endpoints
2. Testing the integration with ALLDATA data
3. Testing different car makes and models to verify comprehensive coverage
"""

import asyncio
import json
import sys
import os
import requests
import time
from pprint import pprint

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the service directly for testing
from backend.app.services.used_car_service import UsedCarService

# Colors for console output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_section(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'-' * 50}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

async def test_service_directly():
    """Test the UsedCarService directly"""
    print_section("Testing UsedCarService directly")
    
    service = UsedCarService()
    
    # Test cases with different makes/models
    test_cases = [
        {
            "make": "Volkswagen", 
            "model": "Golf", 
            "year": 2018, 
            "mileage": 85000, 
            "fuel_type": "diesel", 
            "transmission": "manual",
            "expected_sources": ["ALLDATA"]
        },
        {
            "make": "BMW", 
            "model": "3 Series", 
            "year": 2015, 
            "mileage": 120000, 
            "fuel_type": "petrol", 
            "transmission": "automatic",
            "expected_sources": ["ALLDATA"]
        },
        {
            "make": "Toyota", 
            "model": "Corolla", 
            "year": 2019, 
            "mileage": 50000, 
            "fuel_type": "petrol", 
            "transmission": "manual",
            "expected_sources": []  # Toyota Corolla not in our ALLDATA sample
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print_info(f"Test Case {i+1}: {test_case['make']} {test_case['model']} {test_case['year']}")
        
        try:
            result = await service.check_used_car(
                test_case["make"], 
                test_case["model"], 
                test_case["year"], 
                test_case["mileage"], 
                test_case["fuel_type"], 
                test_case["transmission"]
            )
            
            # Check if the result contains the expected data
            if result:
                print_success("Service returned a result")
                
                # Check if vehicle info is correct
                vehicle_info = result.get("vehicle_info", {})
                if (vehicle_info.get("make") == test_case["make"] and 
                    vehicle_info.get("model") == test_case["model"] and
                    vehicle_info.get("year") == test_case["year"]):
                    print_success("Vehicle information is correct")
                else:
                    print_error("Vehicle information is incorrect")
                
                # Check if sources include ALLDATA when expected
                sources = result.get("sources", [])
                if "ALLDATA" in sources and "ALLDATA" in test_case["expected_sources"]:
                    print_success("ALLDATA is correctly included in sources")
                elif "ALLDATA" not in sources and "ALLDATA" not in test_case["expected_sources"]:
                    print_success("ALLDATA is correctly not included in sources")
                elif "ALLDATA" in sources and "ALLDATA" not in test_case["expected_sources"]:
                    print_warning("ALLDATA is included but was not expected")
                else:
                    print_error("ALLDATA is not included but was expected")
                
                # Print key information from the result
                print_info(f"Reliability Score: {result.get('analysis', {}).get('reliability_score', {}).get('score', 'N/A')}")
                print_info(f"Recommendation: {result.get('recommendation', {}).get('recommendation', 'N/A')}")
                print_info(f"Common Issues Count: {len(result.get('analysis', {}).get('common_issues', []))}")
                
                # Check if common issues are present when expected
                if test_case["make"] in ["Volkswagen", "BMW"]:
                    common_issues = result.get("analysis", {}).get("common_issues", [])
                    if len(common_issues) > 0:
                        print_success("Common issues are present as expected")
                    else:
                        print_error("Common issues are missing")
            else:
                print_error("Service did not return a result")
                
        except Exception as e:
            print_error(f"Error testing service: {str(e)}")
        
        print()  # Add a blank line between test cases

def test_api_endpoints():
    """Test the Used Car Check API endpoints"""
    print_section("Testing Used Car Check API endpoints")
    
    # Check if the backend server is running
    try:
        response = requests.get("http://localhost:8099/api/used-car/options")
        if response.status_code != 200:
            print_error("Backend server is not running or options endpoint is not available")
            print_info("Please start the backend server with ./start_backend.sh")
            return False
        print_success("Backend server is running")
    except requests.exceptions.ConnectionError:
        print_error("Backend server is not running")
        print_info("Please start the backend server with ./start_backend.sh")
        return False
    
    # Test the options endpoint
    print_info("Testing /api/used-car/options endpoint")
    try:
        response = requests.get("http://localhost:8099/api/used-car/options")
        if response.status_code == 200:
            data = response.json()
            if "makes" in data and "models_by_make" in data and "years" in data:
                print_success("Options endpoint returned expected data structure")
                print_info(f"Number of makes: {len(data['makes'])}")
                print_info(f"Number of years: {len(data['years'])}")
            else:
                print_error("Options endpoint returned unexpected data structure")
        else:
            print_error(f"Options endpoint returned status code {response.status_code}")
    except Exception as e:
        print_error(f"Error testing options endpoint: {str(e)}")
    
    # Test the check endpoint
    print_info("Testing /api/used-car/check endpoint")
    test_cases = [
        {
            "make": "Volkswagen", 
            "model": "Golf", 
            "year": 2018, 
            "mileage": 85000, 
            "fuel_type": "diesel", 
            "transmission": "manual"
        },
        {
            "make": "Toyota", 
            "model": "Corolla", 
            "year": 2019, 
            "mileage": 50000, 
            "fuel_type": "petrol", 
            "transmission": "manual"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print_info(f"API Test Case {i+1}: {test_case['make']} {test_case['model']} {test_case['year']}")
        try:
            response = requests.post(
                "http://localhost:8099/api/used-car/check",
                json=test_case
            )
            if response.status_code == 200:
                data = response.json()
                if "analysis" in data and "recommendation" in data:
                    print_success("Check endpoint returned expected data structure")
                    print_info(f"Recommendation: {data.get('recommendation', {}).get('recommendation', 'N/A')}")
                else:
                    print_error("Check endpoint returned unexpected data structure")
            else:
                print_error(f"Check endpoint returned status code {response.status_code}")
        except Exception as e:
            print_error(f"Error testing check endpoint: {str(e)}")
        
        print()  # Add a blank line between test cases
    
    return True

async def main():
    """Main test function"""
    print_header("Used Car Check Feature Comprehensive Test")
    
    # Test the service directly
    await test_service_directly()
    
    # Test the API endpoints
    api_test_result = test_api_endpoints()
    
    print_header("Test Summary")
    if api_test_result:
        print_success("All tests completed. Check the results above for details.")
    else:
        print_warning("Some tests could not be completed. Check the results above for details.")
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
