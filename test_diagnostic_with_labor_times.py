#!/usr/bin/env python3
import requests
import json
import sys
import os
from colorama import Fore, Style, init

# Initialize colorama
init()

# API endpoint
API_URL = "http://localhost:8099/api/diagnose"

def print_header(text):
    """Print a formatted header"""
    width = 80
    print("\n" + "=" * width)
    print(f"{text.center(width)}")
    print("=" * width + "\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")

def print_warning(text):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_labor_times(labor_times):
    """Print labor time information in a formatted way"""
    if not labor_times:
        print_warning("No labor time information available")
        return
    
    print_info("Labor Time Information from ALLDATA:")
    print(f"  {'Repair'.ljust(35)} | {'Estimated Time'.ljust(15)} | Category")
    print(f"  {'-' * 35} | {'-' * 15} | {'-' * 20}")
    
    for item in labor_times:
        repair = item.get("repair", "Unknown")
        time = item.get("estimated_time", "Unknown")
        category = item.get("category", "Unknown")
        print(f"  {repair.ljust(35)} | {time.ljust(15)} | {category}")

def test_diagnosis_with_labor_times():
    """Test the diagnostic system with labor times integration"""
    print_header("Testing Car Diagnostic System with ALLDATA Labor Times")
    
    test_cases = [
        {
            "car_brand": "Volkswagen",
            "model": "Golf",
            "year": 2018,
            "symptoms": "Engine is making a knocking sound and check engine light is on"
        },
        {
            "car_brand": "BMW",
            "model": "3 Series",
            "year": 2016,
            "symptoms": "Transmission is slipping when shifting gears"
        },
        {
            "car_brand": "Toyota",
            "model": "Corolla",
            "year": 2019,
            "symptoms": "Brakes are squeaking and there's a soft pedal feel"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print_info(f"Test Case {i+1}: {test_case['car_brand']} {test_case['model']} {test_case['year']}")
        print_info(f"Symptoms: {test_case['symptoms']}")
        
        try:
            response = requests.post(API_URL, json=test_case)
            
            if response.status_code == 200:
                data = response.json()
                diagnosis = data.get('diagnosis', {})
                
                # Print diagnosis results
                print_success("Diagnosis received successfully")
                print_info(f"Analysis: {diagnosis.get('analysis', 'N/A')}")
                print_info(f"Repair Category: {diagnosis.get('repair_category', 'N/A')}")
                
                # Print labor times
                print_labor_times(diagnosis.get('labor_times', []))
                
                # Check if ALLDATA is listed as a data source
                data_sources = diagnosis.get('data_sources', [])
                if 'ALLDATA Repair Information' in data_sources:
                    print_success("ALLDATA is correctly included in data sources")
                else:
                    print_warning("ALLDATA is not included in data sources")
            else:
                print_error(f"Diagnosis endpoint returned status code {response.status_code}")
                print_error(f"Error: {response.text}")
        except Exception as e:
            print_error(f"Error testing diagnosis endpoint: {str(e)}")
        
        print()  # Add a blank line between test cases
    
    print_header("Test Summary")
    print_success("All tests completed. Check the results above for details.")

if __name__ == "__main__":
    test_diagnosis_with_labor_times()
