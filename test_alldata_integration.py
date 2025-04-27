#!/usr/bin/env python3
"""
Test script for ALLDATA integration with the Used Car Check feature
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.services.used_car_service import UsedCarService

async def test_alldata_integration():
    """Test the ALLDATA integration with the Used Car Check feature"""
    print("Testing ALLDATA integration with the Used Car Check feature...")
    
    # Create service instance
    service = UsedCarService()
    
    # Test with a Volkswagen Golf
    result = await service.check_used_car('Volkswagen', 'Golf', 2018, 85000, 'diesel', 'manual')
    
    print("\nALLDATA Integration Test Results:")
    print(f"Common Issues: {result['analysis']['common_issues']}")
    print(f"Sources: {result['sources']}")
    print(f"Recommendation: {result['recommendation']['recommendation']}")
    print(f"Overall Score: {result['recommendation']['overall_score']}")
    
    # Test with a BMW 3 Series
    result = await service.check_used_car('BMW', '3 Series', 2015, 120000, 'petrol', 'automatic')
    
    print("\nALLDATA Integration Test Results (BMW):")
    print(f"Common Issues: {result['analysis']['common_issues']}")
    print(f"Sources: {result['sources']}")
    print(f"Recommendation: {result['recommendation']['recommendation']}")
    print(f"Overall Score: {result['recommendation']['overall_score']}")

if __name__ == "__main__":
    asyncio.run(test_alldata_integration())
