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

def print_repair_costs(labor_times):
    """Print repair cost information in a formatted way"""
    if not labor_times:
        print_warning("No repair cost information available")
        return
    
    print_info("Repair Cost Information:")
    print(f"  {'Repair'.ljust(35)} | {'Labor'.ljust(15)} | {'Parts'.ljust(15)} | {'Total'.ljust(15)} | Category")
    print(f"  {'-' * 35} | {'-' * 15} | {'-' * 15} | {'-' * 15} | {'-' * 20}")
    
    for item in labor_times:
        repair = item.get("repair", "Unknown")
        
        # Get cost information
        costs = item.get("costs", {})
        labor_cost = costs.get("labor", {}).get("cost", "N/A")
        if labor_cost != "N/A":
            labor_cost = f"€{labor_cost}"
            
        part_cost = costs.get("parts", {}).get("price", "N/A")
        if part_cost != "N/A":
            part_cost = f"€{part_cost}"
            
        total_cost = costs.get("total", {}).get("amount", "N/A")
        if total_cost != "N/A":
            total_cost = f"€{total_cost}"
            
        category = item.get("category", "Unknown")
        
        print(f"  {repair.ljust(35)} | {str(labor_cost).ljust(15)} | {str(part_cost).ljust(15)} | {str(total_cost).ljust(15)} | {category}")

def test_diagnosis_with_costs():
    """Test the diagnostic system with labor times and repair costs integration"""
    print_header("Testing Car Diagnostic System with Repair Costs")
    
    test_cases = [
        {
            "car_brand": "Volkswagen",
            "model": "Golf",
            "car_model": "Golf",  # Including both field names to satisfy all validation layers
            "year": 2018,
            "symptoms": "Engine is making a knocking sound and check engine light is on"
        },
        {
            "car_brand": "BMW",
            "model": "3 Series",
            "car_model": "3 Series",  # Including both field names
            "year": 2016,
            "symptoms": "Transmission is slipping when shifting gears"
        },
        {
            "car_brand": "Toyota",
            "model": "Corolla",
            "car_model": "Corolla",  # Including both field names
            "year": 2019,
            "symptoms": "Brakes are squeaking and there's a soft pedal feel"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print_info(f"Test Case {i+1}: {test_case['car_brand']} {test_case['model']} {test_case['year']}")
        print_info(f"Symptoms: {test_case['symptoms']}")
        
        try:
            print_info(f"Sending request with data: {json.dumps(test_case)}")
            response = requests.post(API_URL, json=test_case)
            
            if response.status_code == 200:
                data = response.json()
                diagnosis = data.get('diagnosis', {})
                
                # Print diagnosis results
                print_success("Diagnosis received successfully")
                print_info(f"Analysis: {diagnosis.get('analysis', 'N/A')}")
                print_info(f"Repair Category: {diagnosis.get('repair_category', 'N/A')}")
                
                # Print raw data for debugging
                print_info(f"Raw diagnosis data: {json.dumps(diagnosis, indent=2)}"[:200] + '...')
                
                # Print repair costs
                print_repair_costs(diagnosis.get('labor_times', []))
                
                # Check if all data sources are included
                data_sources = diagnosis.get('data_sources', [])
                expected_sources = ['ALLDATA Repair Information', 'Autodoc Parts Pricing', 'Technical Service Bulletins']
                
                for source in expected_sources:
                    if source in data_sources:
                        print_success(f"{source} is correctly included in data sources")
                    else:
                        print_warning(f"{source} is not included in data sources")
            else:
                print_error(f"Diagnosis endpoint returned status code {response.status_code}")
                print_error(f"Error: {response.text}")
        except Exception as e:
            print_error(f"Error testing diagnosis endpoint: {str(e)}")
        
        print()  # Add a blank line between test cases
    
    print_header("Test Summary")
    print_success("All tests completed. Check the results above for details.")

if __name__ == "__main__":
    test_diagnosis_with_costs()
