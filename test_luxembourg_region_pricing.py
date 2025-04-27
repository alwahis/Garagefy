#!/usr/bin/env python3
"""
Test script for the enhanced Luxembourg region car price estimation feature.
This script tests the used car check API with a focus on regional pricing.
"""

import requests
import json
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

# Base URL for the API
BASE_URL = "http://localhost:8099"

def print_header(text):
    print(f"\n{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{text.center(80)}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}\n")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_json(data):
    """Print formatted JSON with indentation"""
    json_str = json.dumps(data, indent=2)
    print(json_str)

def test_car_model(make, model, year, mileage, fuel_type, transmission):
    """Test the used car check API with specified parameters"""
    print_info(f"Testing: {year} {make} {model} - {mileage}km, {fuel_type}, {transmission}")
    
    # Prepare request data
    data = {
        "make": make,
        "model": model,
        "year": year,
        "mileage": mileage,
        "fuel_type": fuel_type,
        "transmission": transmission
    }
    
    try:
        # Make API request
        response = requests.post(f"{BASE_URL}/api/used-car/check", json=data)
        
        # Check response
        if response.status_code == 200:
            print_success("Response received successfully")
            result = response.json()
            
            # Extract and display price data
            market_data = result.get("market_data", {})
            estimated_price = market_data.get("estimated_price", "N/A")
            price_range = market_data.get("price_range", {})
            low_price = price_range.get("low", "N/A")
            high_price = price_range.get("high", "N/A")
            
            print_info(f"Estimated Price: €{estimated_price}")
            print_info(f"Price Range: €{low_price} - €{high_price}")
            
            # Display regional prices
            print_info("Regional Prices (within 200km of Luxembourg):")
            luxembourg_region = result.get("luxembourg_region", {})
            regional_prices = luxembourg_region.get("regional_prices", {})
            
            if regional_prices:
                for region, price in regional_prices.items():
                    print_info(f"  {region}: €{price}")
            else:
                print_warning("No regional price data available")
            
            # Display market insights
            market_insights = luxembourg_region.get("market_insights", [])
            if market_insights:
                print_info("Market Insights:")
                for insight in market_insights:
                    print_info(f"  • {insight}")
            
            # Display data sources
            sources = result.get("sources", [])
            if sources:
                print_info("Data Sources:")
                for source in sources:
                    print_info(f"  • {source}")
            
            return True
        else:
            print_error(f"API request failed with status code {response.status_code}")
            print_error(f"Error message: {response.text}")
            return False
    
    except Exception as e:
        print_error(f"Exception occurred: {str(e)}")
        return False

def main():
    print_header("Testing Luxembourg Region Car Price Estimation")
    
    # Test cases
    test_cases = [
        # Premium German cars
        {"make": "BMW", "model": "3 Series", "year": 2020, "mileage": 45000, "fuel_type": "diesel", "transmission": "automatic"},
        {"make": "Audi", "model": "A4", "year": 2019, "mileage": 60000, "fuel_type": "diesel", "transmission": "automatic"},
        
        # Popular French cars
        {"make": "Renault", "model": "Megane", "year": 2018, "mileage": 70000, "fuel_type": "diesel", "transmission": "manual"},
        {"make": "Peugeot", "model": "3008", "year": 2021, "mileage": 30000, "fuel_type": "petrol", "transmission": "automatic"},
        
        # Economical Japanese cars
        {"make": "Toyota", "model": "Corolla", "year": 2019, "mileage": 50000, "fuel_type": "hybrid", "transmission": "automatic"},
        
        # Czech value car
        {"make": "Skoda", "model": "Octavia", "year": 2017, "mileage": 90000, "fuel_type": "diesel", "transmission": "manual"},
    ]
    
    # Run test cases
    success_count = 0
    for i, test_case in enumerate(test_cases):
        print_header(f"Test Case {i+1}: {test_case['year']} {test_case['make']} {test_case['model']}")
        if test_car_model(**test_case):
            success_count += 1
    
    # Print summary
    print_header("Test Summary")
    if success_count == len(test_cases):
        print_success(f"All {success_count} tests passed successfully!")
    else:
        print_warning(f"{success_count} of {len(test_cases)} tests passed.")

if __name__ == "__main__":
    main()
