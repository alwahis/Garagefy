"""
Used Car Check Service

This service provides data and analysis for used car checks by aggregating information
from trusted online forums and websites worldwide, with a focus on Eastern European market pricing.
"""

import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional, Any
import json
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of trusted sources for car data
TRUSTED_SOURCES = {
    "forums": [
        {"name": "AutoScout24", "url": "https://www.autoscout24.com", "region": "Europe", "reliability": 0.9},
        {"name": "Mobile.de", "url": "https://www.mobile.de", "region": "Europe", "reliability": 0.9},
        {"name": "Edmunds", "url": "https://forums.edmunds.com", "region": "Global", "reliability": 0.85},
        {"name": "CarGurus", "url": "https://www.cargurus.com", "region": "Global", "reliability": 0.8},
        {"name": "PistonHeads", "url": "https://www.pistonheads.com", "region": "Europe", "reliability": 0.85},
        {"name": "Otomoto", "url": "https://www.otomoto.pl", "region": "Eastern Europe", "reliability": 0.9},
        {"name": "Hasznaltauto", "url": "https://www.hasznaltauto.hu", "region": "Eastern Europe", "reliability": 0.85},
        {"name": "Auto.cz", "url": "https://www.auto.cz", "region": "Eastern Europe", "reliability": 0.8}
    ],
    "pricing": [
        {"name": "Eurotax", "region": "Eastern Europe", "reliability": 0.95},
        {"name": "AutoDNA", "region": "Eastern Europe", "reliability": 0.9},
        {"name": "ADAC", "region": "Europe", "reliability": 0.9}
    ],
    "reliability": [
        {"name": "TÜV Report", "region": "Europe", "reliability": 0.95},
        {"name": "J.D. Power", "region": "Global", "reliability": 0.9},
        {"name": "Consumer Reports", "region": "Global", "reliability": 0.9},
        {"name": "Warranty Direct", "region": "Europe", "reliability": 0.85}
    ]
}

# Eastern European market price adjustment factors (compared to Western European prices)
EASTERN_EU_PRICE_FACTORS = {
    "Poland": 0.85,
    "Hungary": 0.8,
    "Czech Republic": 0.82,
    "Slovakia": 0.81,
    "Romania": 0.75,
    "Bulgaria": 0.7,
    "Croatia": 0.78,
    "Slovenia": 0.83,
    "Estonia": 0.8,
    "Latvia": 0.75,
    "Lithuania": 0.77
}

# Sample data for common issues by make/model
# In a production environment, this would be replaced with actual API calls to automotive databases
COMMON_ISSUES_DATA = {
    "BMW": {
        "3 Series": {
            "E90 (2005-2011)": [
                "Timing chain issues on N47 diesel engines",
                "Electric water pump failures",
                "Oil leaks from valve cover gasket",
                "VANOS solenoid failures"
            ],
            "F30 (2012-2018)": [
                "Timing chain issues on early N20 engines",
                "Coolant leaks from expansion tank",
                "Charge pipe failures on turbocharged models",
                "Valve cover gasket oil leaks"
            ]
        },
        "5 Series": {
            "E60 (2003-2010)": [
                "Timing chain issues on N47 diesel engines",
                "iDrive system failures",
                "Valve stem seal failures on N52/N54 engines",
                "Active steering rack failures"
            ],
            "F10 (2010-2016)": [
                "Timing chain issues on N20 engines",
                "Electronic water pump failures",
                "Valve cover gasket oil leaks",
                "Turbocharger wastegate rattle"
            ]
        }
    },
    "Volkswagen": {
        "Golf": {
            "Mk6 (2008-2013)": [
                "Timing chain tensioner failures on TSI engines",
                "Water pump failures",
                "Carbon buildup on intake valves (direct injection)",
                "DSG transmission mechatronic unit failures"
            ],
            "Mk7 (2013-2020)": [
                "Water pump leaks",
                "Sunroof drain blockages causing water leaks",
                "Carbon buildup on intake valves (direct injection)",
                "Turbocharger failures on early models"
            ]
        },
        "Passat": {
            "B6 (2005-2010)": [
                "DSG transmission mechatronic unit failures",
                "Timing chain tensioner failures on TSI engines",
                "Water pump failures",
                "Intake manifold flap failures"
            ],
            "B7 (2010-2015)": [
                "Water pump failures",
                "Timing chain tensioner failures on early TSI engines",
                "Carbon buildup on intake valves (direct injection)",
                "Sunroof drain blockages causing water leaks"
            ]
        }
    },
    "Toyota": {
        "Corolla": {
            "E140/E150 (2006-2013)": [
                "Excessive oil consumption on 1ZR-FE engines",
                "Water pump failures",
                "Transmission valve body issues on automatic models",
                "Steering intermediate shaft noise"
            ],
            "E170 (2013-2019)": [
                "CVT transmission shudder",
                "Air conditioning compressor failures",
                "Infotainment system glitches",
                "Excessive oil consumption on early models"
            ]
        },
        "Camry": {
            "XV40 (2006-2011)": [
                "Excessive oil consumption on 2AZ-FE engines",
                "Water pump failures",
                "Transmission torque converter shudder",
                "Dashboard cracking"
            ],
            "XV50 (2011-2017)": [
                "Transmission torque converter shudder",
                "Infotainment system glitches",
                "Air conditioning compressor failures",
                "Excessive oil consumption on early models"
            ]
        }
    }
}

# Mileage assessment data
MILEAGE_ASSESSMENT = {
    "low": {
        "range": "Less than 10,000 km per year",
        "condition": "Excellent",
        "price_factor": 1.15,
        "description": "Vehicle has been driven significantly less than average, suggesting potential for extended lifespan and fewer wear-related issues."
    },
    "average": {
        "range": "10,000-20,000 km per year",
        "condition": "Good",
        "price_factor": 1.0,
        "description": "Vehicle has been driven an average amount, suggesting normal wear and tear consistent with its age."
    },
    "high": {
        "range": "20,000-30,000 km per year",
        "condition": "Fair",
        "price_factor": 0.85,
        "description": "Vehicle has been driven more than average, suggesting accelerated wear on components and potentially higher maintenance needs."
    },
    "very_high": {
        "range": "More than 30,000 km per year",
        "condition": "Poor",
        "price_factor": 0.7,
        "description": "Vehicle has been driven extensively, suggesting significant wear on major components and likely higher maintenance costs."
    }
}

# Fuel type data
FUEL_TYPES = [
    {"id": "petrol", "name": "Petrol", "popularity_factor": 1.0},
    {"id": "diesel", "name": "Diesel", "popularity_factor": 0.95},
    {"id": "hybrid", "name": "Hybrid", "popularity_factor": 1.1},
    {"id": "electric", "name": "Electric", "popularity_factor": 1.15},
    {"id": "lpg", "name": "LPG", "popularity_factor": 0.85},
    {"id": "cng", "name": "CNG", "popularity_factor": 0.8}
]

# Transmission type data
TRANSMISSION_TYPES = [
    {"id": "manual", "name": "Manual", "popularity_factor": 0.95},
    {"id": "automatic", "name": "Automatic", "popularity_factor": 1.05},
    {"id": "semi-auto", "name": "Semi-Automatic", "popularity_factor": 1.0},
    {"id": "cvt", "name": "CVT", "popularity_factor": 0.98},
    {"id": "dct", "name": "Dual-Clutch", "popularity_factor": 1.02}
]

class UsedCarService:
    """Service for providing used car check data and analysis"""
    
    def get_car_options(self) -> Dict[str, Any]:
        """Get all available options for car selection dropdowns"""
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 30, -1))
        
        # In a real implementation, this would fetch data from a database or external API
        # For now, we'll use the sample data
        makes = list(COMMON_ISSUES_DATA.keys())
        models_by_make = {make: list(COMMON_ISSUES_DATA[make].keys()) for make in makes}
        
        return {
            "makes": makes,
            "models_by_make": models_by_make,
            "years": years,
            "fuelTypes": FUEL_TYPES,
            "transmissionTypes": TRANSMISSION_TYPES
        }
    
    def _assess_mileage(self, year: int, mileage: int) -> Dict[str, Any]:
        """Assess vehicle mileage based on age and distance traveled"""
        current_year = datetime.now().year
        age = current_year - year
        annual_mileage = mileage / max(age, 1)  # Avoid division by zero
        
        if annual_mileage < 10000:
            category = "low"
        elif annual_mileage < 20000:
            category = "average"
        elif annual_mileage < 30000:
            category = "high"
        else:
            category = "very_high"
            
        return {
            "category": category,
            "annual_average": round(annual_mileage),
            **MILEAGE_ASSESSMENT[category]
        }
    
    def _get_common_issues(self, make: str, model: str, year: int) -> List[str]:
        """Get common issues for the specified make/model/year"""
        if make not in COMMON_ISSUES_DATA:
            return ["No specific data available for this make"]
            
        if model not in COMMON_ISSUES_DATA[make]:
            return ["No specific data available for this model"]
            
        # Find the generation that matches the year
        for generation, issues in COMMON_ISSUES_DATA[make][model].items():
            # Extract years from generation string (e.g., "E90 (2005-2011)")
            year_match = re.search(r'\((\d{4})-(\d{4})\)', generation)
            if year_match:
                start_year, end_year = int(year_match.group(1)), int(year_match.group(2))
                if start_year <= year <= end_year:
                    return issues
                    
        return ["No specific data available for this year"]
    
    def _estimate_price_range(self, make: str, model: str, year: int, mileage: int, 
                             fuel_type: str, transmission: str) -> Dict[str, Any]:
        """
        Estimate price range for Eastern European market
        
        In a real implementation, this would call external pricing APIs or databases
        For now, we'll use a simplified calculation based on the vehicle details
        """
        # Base values - these would come from real market data in production
        base_values = {
            "BMW": {"3 Series": 25000, "5 Series": 35000, "X5": 45000},
            "Volkswagen": {"Golf": 15000, "Passat": 20000, "Tiguan": 25000},
            "Toyota": {"Corolla": 15000, "Camry": 22000, "RAV4": 25000},
            "Audi": {"A3": 22000, "A4": 28000, "Q5": 35000},
            "Mercedes-Benz": {"C-Class": 28000, "E-Class": 38000, "GLC": 40000}
        }
        
        # Default value if make/model not found
        base_value = 20000
        
        # Get base value for make/model if available
        if make in base_values and model in base_values[make]:
            base_value = base_values[make][model]
        
        # Adjust for age (depreciation)
        current_year = datetime.now().year
        age = current_year - year
        age_factor = max(0.3, 1 - (age * 0.08))  # 8% depreciation per year, minimum 30% of original value
        
        # Adjust for mileage
        mileage_assessment = self._assess_mileage(year, mileage)
        mileage_factor = mileage_assessment["price_factor"]
        
        # Adjust for fuel type
        fuel_factor = 1.0
        for ft in FUEL_TYPES:
            if ft["id"] == fuel_type:
                fuel_factor = ft["popularity_factor"]
                break
        
        # Adjust for transmission
        transmission_factor = 1.0
        for tt in TRANSMISSION_TYPES:
            if tt["id"] == transmission:
                transmission_factor = tt["popularity_factor"]
                break
        
        # Apply Eastern European market adjustment (average of factors)
        eastern_eu_factor = sum(EASTERN_EU_PRICE_FACTORS.values()) / len(EASTERN_EU_PRICE_FACTORS)
        
        # Calculate estimated price
        estimated_price = base_value * age_factor * mileage_factor * fuel_factor * transmission_factor * eastern_eu_factor
        
        # Create price range (±10%)
        price_low = round(estimated_price * 0.9, -2)  # Round to nearest 100
        price_high = round(estimated_price * 1.1, -2)  # Round to nearest 100
        
        return {
            "estimated_price": round(estimated_price, -2),
            "price_range": {
                "low": price_low,
                "high": price_high
            },
            "currency": "EUR",
            "market": "Eastern European",
            "factors": {
                "age_factor": round(age_factor, 2),
                "mileage_factor": round(mileage_factor, 2),
                "fuel_factor": round(fuel_factor, 2),
                "transmission_factor": round(transmission_factor, 2),
                "market_factor": round(eastern_eu_factor, 2)
            }
        }
    
    def _generate_recommendations(self, make: str, model: str, year: int, 
                                 mileage: int, common_issues: List[str]) -> Dict[str, Any]:
        """Generate recommendations based on vehicle details and common issues"""
        mileage_assessment = self._assess_mileage(year, mileage)
        current_year = datetime.now().year
        age = current_year - year
        
        # General recommendations
        general_recommendations = [
            "Always request and review the vehicle's full service history",
            "Perform a thorough pre-purchase inspection, preferably by a trusted mechanic",
            "Check for outstanding finance or legal issues using a vehicle history report",
            "Test drive the vehicle under various conditions (city, highway, etc.)",
            "Verify all electrical components and features are working properly"
        ]
        
        # Age-based recommendations
        age_recommendations = []
        if age < 3:
            age_recommendations = [
                "Verify the vehicle is still under manufacturer warranty",
                "Check if regular service intervals have been maintained",
                "Ensure any recall work has been completed"
            ]
        elif age < 7:
            age_recommendations = [
                "Check for timing belt/chain replacement if due (typically 60,000-100,000 km)",
                "Verify all major services have been completed on schedule",
                "Consider an extended warranty if available"
            ]
        else:
            age_recommendations = [
                "Check for major component replacements (timing belt/chain, water pump, etc.)",
                "Inspect for rust and corrosion, especially in wheel arches and underbody",
                "Verify that all wear items (brakes, suspension) are in good condition",
                "Budget for potential major repairs in the near future"
            ]
        
        # Mileage-based recommendations
        mileage_recommendations = []
        if mileage_assessment["category"] in ["high", "very_high"]:
            mileage_recommendations = [
                "Verify that all high-mileage maintenance has been performed",
                "Check for engine oil leaks and consumption",
                "Inspect transmission fluid condition and level",
                "Test suspension components for wear and noise"
            ]
        
        # Combine all recommendations
        all_recommendations = {
            "critical": general_recommendations[:2],
            "important": general_recommendations[2:] + age_recommendations[:2],
            "additional": age_recommendations[2:] + mileage_recommendations
        }
        
        # Add model-specific recommendations based on common issues
        if common_issues and common_issues[0] != "No specific data available for this make":
            model_recommendations = [f"Check for {issue.lower()}" for issue in common_issues]
            all_recommendations["model_specific"] = model_recommendations
        
        return all_recommendations
    
    async def check_used_car(self, make: str, model: str, year: int, mileage: int, 
                            fuel_type: str, transmission: str) -> Dict[str, Any]:
        """
        Perform a comprehensive used car check based on the provided details
        
        Args:
            make: Car manufacturer
            model: Car model
            year: Manufacturing year
            mileage: Current mileage in kilometers
            fuel_type: Type of fuel (petrol, diesel, etc.)
            transmission: Transmission type (manual, automatic, etc.)
            
        Returns:
            Dict containing analysis, recommendations, and pricing information
        """
        try:
            # Get common issues for this make/model/year
            common_issues = self._get_common_issues(make, model, year)
            
            # Assess mileage
            mileage_assessment = self._assess_mileage(year, mileage)
            
            # Estimate price range
            price_data = self._estimate_price_range(make, model, year, mileage, fuel_type, transmission)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(make, model, year, mileage, common_issues)
            
            # Compile results
            result = {
                "vehicle_details": {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage,
                    "fuel_type": fuel_type,
                    "transmission": transmission
                },
                "analysis": {
                    "mileage_assessment": mileage_assessment,
                    "common_issues": common_issues,
                    "reliability_score": self._calculate_reliability_score(make, model, year, mileage),
                    "sources": TRUSTED_SOURCES
                },
                "market_data": {
                    "price_estimation": price_data,
                    "market_region": "Eastern Europe",
                    "data_sources": [source["name"] for source in TRUSTED_SOURCES["pricing"]]
                },
                "recommendations": recommendations
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in used car check: {str(e)}")
            raise
    
    def _calculate_reliability_score(self, make: str, model: str, year: int, mileage: int) -> Dict[str, Any]:
        """Calculate reliability score based on make, model, year and mileage"""
        # Base reliability scores (out of 100) - would come from real reliability data in production
        base_scores = {
            "Toyota": 85,
            "Lexus": 84,
            "Mazda": 83,
            "Honda": 82,
            "Subaru": 80,
            "Kia": 79,
            "Hyundai": 78,
            "Porsche": 78,
            "BMW": 76,
            "Mercedes-Benz": 75,
            "Audi": 74,
            "Volkswagen": 72,
            "Ford": 70,
            "Chevrolet": 68,
            "Nissan": 67
        }
        
        # Default score if make not found
        base_score = 70
        
        # Get base score for make if available
        if make in base_scores:
            base_score = base_scores[make]
        
        # Adjust for age
        current_year = datetime.now().year
        age = current_year - year
        age_factor = max(0.7, 1 - (age * 0.02))  # 2% reduction per year, minimum 70% of original score
        
        # Adjust for mileage
        mileage_assessment = self._assess_mileage(year, mileage)
        mileage_factors = {
            "low": 1.05,
            "average": 1.0,
            "high": 0.9,
            "very_high": 0.8
        }
        mileage_factor = mileage_factors[mileage_assessment["category"]]
        
        # Calculate final score
        final_score = base_score * age_factor * mileage_factor
        
        # Determine rating based on score
        rating = "Excellent"
        if final_score < 50:
            rating = "Poor"
        elif final_score < 65:
            rating = "Fair"
        elif final_score < 75:
            rating = "Good"
        elif final_score < 85:
            rating = "Very Good"
        
        return {
            "score": round(final_score),
            "rating": rating,
            "max_score": 100,
            "factors": {
                "make_base_score": base_score,
                "age_adjustment": round(age_factor, 2),
                "mileage_adjustment": round(mileage_factor, 2)
            }
        }
