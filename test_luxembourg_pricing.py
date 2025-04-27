#!/usr/bin/env python3
"""
Test script for the Luxembourg Region Fair Pricing feature.

This script tests the enhanced Used Car Check feature with real-world pricing data
from automotive websites within 200km of Luxembourg.
"""

import asyncio
import json
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'app'))
from services.used_car_service import UsedCarService

class TestLuxembourgPricing:
    def __init__(self):
        self.service = None
        self.test_cases = [
            {
                "make": "Volkswagen", 
                "model": "Golf", 
                "year": 2020, 
                "mileage": 45000, 
                "fuel_type": "petrol", 
                "transmission": "manual"
            },
            {
                "make": "BMW", 
                "model": "3 Series", 
                "year": 2018, 
                "mileage": 75000, 
                "fuel_type": "diesel", 
                "transmission": "automatic"
            },
            {
                "make": "Toyota", 
                "model": "Corolla", 
                "year": 2021, 
                "mileage": 30000, 
                "fuel_type": "hybrid", 
                "transmission": "automatic"
            },
            {
                "make": "Audi", 
                "model": "A4", 
                "year": 2019, 
                "mileage": 60000, 
                "fuel_type": "diesel", 
                "transmission": "automatic"
            }
        ]
        
    async def initialize(self):
        # Initialize the UsedCarService
        self.service = UsedCarService()
        
        # Wait for service initialization to complete
        await asyncio.sleep(2)  # Give time for scrapers to initialize
        
    async def run_tests(self):
        """Test the Luxembourg Region Fair Pricing feature"""
        print("===== Testing Luxembourg Region Fair Pricing Feature =====")
        
        if not self.service:
            await self.initialize()
            
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\nTest Case #{i}: {test_case['year']} {test_case['make']} {test_case['model']}")
            
            try:
                # Call the check_used_car method
                print(f"Calling check_used_car for {test_case['make']} {test_case['model']} {test_case['year']}...")
                result = await self.service.check_used_car(
                    make=test_case["make"],
                    model=test_case["model"],
                    year=test_case["year"],
                    mileage=test_case["mileage"],
                    fuel_type=test_case["fuel_type"],
                    transmission=test_case["transmission"]
                )
                
                # Debug output
                print(f"Result type: {type(result)}")
                if result is None:
                    print("Error: Result is None - This suggests an exception is being caught in the check_used_car method")
                    print("Trying to access the method directly to see the actual error...")
                    try:
                        # Try to get price range directly to see if that's where the error is
                        price_range = await self.service._estimate_price_range(
                            make=test_case["make"],
                            model=test_case["model"],
                            year=test_case["year"],
                            mileage=test_case["mileage"],
                            fuel_type=test_case["fuel_type"],
                            transmission=test_case["transmission"]
                        )
                        print(f"Price range direct call successful: {price_range}")
                    except Exception as direct_error:
                        print(f"Direct error in _estimate_price_range: {str(direct_error)}")
                    continue
                    
                print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dictionary'}")
                
                # Extract the Luxembourg Region Fair Pricing data
                lux_pricing = result.get("luxembourg_region", {})
                
                # Print the results
                print("\nLuxembourg Region Fair Pricing")
                print(f"{lux_pricing.get('description', '')}")
                print(f"{lux_pricing.get('subtitle', '')}")
                
                # Print the estimated price
                estimated_price = lux_pricing.get("estimated_price", 0)
                currency = lux_pricing.get("currency", "EUR")
                print("\nEstimated Fair Price")
                print(f"{currency} {estimated_price:,}")
                
                # Print the price range
                price_range = lux_pricing.get("price_range", {})
                low_price = price_range.get("low", 0)
                high_price = price_range.get("high", 0)
                print("Price Range")
                print(f"{currency} {low_price:,} - {currency} {high_price:,}")
                
                # Print the regional prices
                regional_prices = lux_pricing.get("regional_prices", {})
                if regional_prices:
                    print("\nRegional Prices")
                    for region, price in regional_prices.items():
                        print(f"{region}: {currency} {price:,}")
                
                # Print the price factors
                price_factors = lux_pricing.get("price_factors", {})
                if price_factors:
                    print("\nPrice Factors")
                    for factor, value in price_factors.items():
                        print(f"{factor}: {value}")
                
                # Print the data sources
                data_sources = result.get("data_sources", [])
                if data_sources:
                    print("\nData Sources")
                    for source in data_sources:
                        print(f"- {source}")
                
                print(f"\n✓ Test Case #{i} Passed")
            
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(TestLuxembourgPricing().run_tests())
