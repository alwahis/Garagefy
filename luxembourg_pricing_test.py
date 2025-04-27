#!/usr/bin/env python3
"""
Direct test script for Luxembourg region car pricing
This script directly uses the UsedCarService to test the fair pricing calculations
without relying on API endpoints
"""

import asyncio
import json
import sys
from colorama import Fore, Style, init

# Initialize colorama for colored output
init()

# Adjust import path to access the UsedCarService
sys.path.insert(0, '/Users/mudhafar.hamid/Garagefy')
sys.path.insert(0, '/Users/mudhafar.hamid/Garagefy/backend')

# Import the UsedCarService directly
from backend.app.services.used_car_service import UsedCarService

def print_header(text):
    print(f"\n{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{text.center(80)}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}\n")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_json(data):
    """Print formatted JSON with indentation"""
    json_str = json.dumps(data, indent=2)
    print(json_str)
    
def print_price_info(price_data):
    """Format and print price information"""
    estimated_price = price_data.get("estimated_price", "N/A")
    price_range = price_data.get("price_range", {})
    low_price = price_range.get("low", "N/A")
    high_price = price_range.get("high", "N/A")
    
    print_info(f"Estimated Price: €{estimated_price}")
    print_info(f"Price Range: €{low_price} - €{high_price}")
    
    # Print regional prices if available
    regional_prices = price_data.get("regional_prices", {})
    if regional_prices:
        print_info("Regional Prices (within 200km of Luxembourg):")
        for region, price in regional_prices.items():
            print_info(f"  {region}: €{price}")
    
    # Print price factors
    factors = price_data.get("factors", {})
    if factors:
        print_info("Price Factors:")
        for factor, value in factors.items():
            print_info(f"  {factor}: {value}")

async def test_luxembourg_pricing():
    print_header("Luxembourg Region Fair Pricing Test")
    
    # Initialize the UsedCarService directly
    service = UsedCarService()
    print_success("UsedCarService initialized")
    
    # Test cases
    test_cases = [
        # Premium German cars
        {"make": "BMW", "model": "3 Series", "year": 2020, "mileage": 45000, "fuel_type": "diesel", "transmission": "automatic"},
        {"make": "Audi", "model": "A4", "year": 2019, "mileage": 60000, "fuel_type": "diesel", "transmission": "automatic"},
        
        # Popular French cars
        {"make": "Renault", "model": "Megane", "year": 2018, "mileage": 70000, "fuel_type": "diesel", "transmission": "manual"},
        {"make": "Peugeot", "model": "3008", "year": 2021, "mileage": 30000, "fuel_type": "petrol", "transmission": "automatic"},
        
        # Electric car
        {"make": "BMW", "model": "i3", "year": 2022, "mileage": 20000, "fuel_type": "electric", "transmission": "automatic"},
    ]
    
    for i, test_case in enumerate(test_cases):
        make = test_case["make"]
        model = test_case["model"]
        year = test_case["year"]
        mileage = test_case["mileage"]
        fuel_type = test_case["fuel_type"]
        transmission = test_case["transmission"]
        
        print_header(f"Test Case {i+1}: {year} {make} {model}")
        print_info(f"Details: {mileage}km, {fuel_type}, {transmission}")
        
        # Get price estimate directly from the service
        price_data = service._estimate_price_range(
            make=make,
            model=model,
            year=year,
            mileage=mileage,
            fuel_type=fuel_type,
            transmission=transmission
        )
        
        # Print the price information
        print_price_info(price_data)
        
        # Verify Luxembourg region data is present
        if "regional_prices" in price_data:
            print_success("Luxembourg region pricing data is available")
            
            # Check if Luxembourg is more expensive than other regions
            lux_price = price_data.get("regional_prices", {}).get("Luxembourg", 0)
            other_prices = [p for r, p in price_data.get("regional_prices", {}).items() if r != "Luxembourg"]
            if other_prices and lux_price > max(other_prices):
                print_info("✓ Luxembourg prices are higher than neighboring regions as expected")
        else:
            print_warning("Luxembourg region pricing data is missing")
    
    print_header("Test Summary")
    print_success("Luxembourg region fair pricing test completed")
    print_info("The enhanced price estimation now includes data from car websites within 200km of Luxembourg")

if __name__ == "__main__":
    asyncio.run(test_luxembourg_pricing())
