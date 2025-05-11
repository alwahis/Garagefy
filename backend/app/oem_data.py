"""
OEM data handler for car diagnostics.
This module provides access to OEM part costs and repair time estimates.
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to ALLDATA files
ALLDATA_DIR = Path(__file__).parent / "data" / "alldata"

# Cache for loaded data
LOADED_LABOUR_TIMES = {}
LOADED_COMMON_ISSUES = {}
LOADED_PART_COSTS = {
    # Default part costs for common repairs when OEM data is not available
    "default": {
        "Engine": {
            "Timing belt replacement": {"min": 150, "max": 350},
            "Water pump replacement": {"min": 80, "max": 200},
            "Spark plugs replacement": {"min": 40, "max": 120},
            "Oxygen sensor replacement": {"min": 100, "max": 300},
            "Valve cover gasket replacement": {"min": 30, "max": 100},
            "Turbocharger replacement": {"min": 800, "max": 2000},
            "Mass airflow sensor": {"min": 120, "max": 350}
        },
        "Transmission": {
            "Clutch replacement": {"min": 300, "max": 800},
            "Transmission fluid change": {"min": 80, "max": 150},
            "Gearbox mount replacement": {"min": 60, "max": 200}
        },
        "Brakes": {
            "Brake pads replacement (front)": {"min": 60, "max": 150},
            "Brake pads replacement (rear)": {"min": 60, "max": 150},
            "Brake discs replacement (front)": {"min": 100, "max": 300},
            "Brake discs replacement (rear)": {"min": 100, "max": 300},
            "Brake fluid flush": {"min": 40, "max": 100},
            "ABS sensor replacement": {"min": 80, "max": 200}
        },
        "Suspension": {
            "Shock absorber replacement (each)": {"min": 80, "max": 200},
            "Control arm replacement": {"min": 120, "max": 350},
            "Wheel bearing replacement": {"min": 100, "max": 300},
            "Tie rod end replacement": {"min": 60, "max": 150}
        },
        "Electrical": {
            "Battery replacement": {"min": 100, "max": 250},
            "Alternator replacement": {"min": 200, "max": 500},
            "Starter motor replacement": {"min": 150, "max": 450}
        },
        "Cooling": {
            "Radiator replacement": {"min": 150, "max": 400},
            "Thermostat replacement": {"min": 50, "max": 150},
            "Coolant flush": {"min": 60, "max": 120},
            "Water pump replacement": {"min": 100, "max": 350}
        }
    }
}

# Premium brand markup factors
PREMIUM_BRAND_MARKUP = {
    "Mercedes-Benz": 1.8,
    "BMW": 1.7,
    "Audi": 1.6,
    "Lexus": 1.5,
    "Porsche": 2.2,
    "Land Rover": 1.9,
    "Jaguar": 1.8,
    "Volvo": 1.5
}

# Labour cost per hour (average)
LABOUR_COST_PER_HOUR = 85  # EUR

def load_labour_times() -> Dict:
    """Load labour times data from ALLDATA"""
    if LOADED_LABOUR_TIMES:
        return LOADED_LABOUR_TIMES
    
    labour_times_path = ALLDATA_DIR / "labour_times.json"
    if not labour_times_path.exists():
        logger.warning(f"Labour times data not found at {labour_times_path}")
        return {}
    
    try:
        with open(labour_times_path, 'r') as f:
            data = json.load(f)
            global LOADED_LABOUR_TIMES
            LOADED_LABOUR_TIMES = data
            logger.info(f"Loaded labour times data")
            return data
    except Exception as e:
        logger.error(f"Error loading labour times data: {str(e)}")
        return {}

def load_common_issues() -> Dict:
    """Load common issues data from ALLDATA"""
    if LOADED_COMMON_ISSUES:
        return LOADED_COMMON_ISSUES
    
    common_issues_path = ALLDATA_DIR / "common_issues.json"
    if not common_issues_path.exists():
        logger.warning(f"Common issues data not found at {common_issues_path}")
        return {}
    
    try:
        with open(common_issues_path, 'r') as f:
            data = json.load(f)
            global LOADED_COMMON_ISSUES
            LOADED_COMMON_ISSUES = data
            logger.info(f"Loaded common issues data")
            return data
    except Exception as e:
        logger.error(f"Error loading common issues data: {str(e)}")
        return {}

def get_repair_estimate(brand: str, model: str, repair_item: str, system: str) -> Tuple[Dict, str]:
    """
    Get repair cost and time estimate for a specific repair item
    
    Returns:
        Tuple containing:
        - Dict with min and max cost
        - String with labor time
    """
    # Load labour times data
    labour_times = load_labour_times()
    
    # Get labour time
    labour_time = "Unknown"
    if brand in labour_times and model in labour_times[brand] and system in labour_times[brand][model]:
        if repair_item in labour_times[brand][model][system]:
            labour_time = labour_times[brand][model][system][repair_item]
    
    # Get part cost
    part_cost = {"min": 0, "max": 0}
    
    # Check if we have specific part costs for this brand/model
    if brand in LOADED_PART_COSTS and model in LOADED_PART_COSTS[brand] and system in LOADED_PART_COSTS[brand][model]:
        if repair_item in LOADED_PART_COSTS[brand][model][system]:
            part_cost = LOADED_PART_COSTS[brand][model][system][repair_item]
    # Fall back to default costs
    elif "default" in LOADED_PART_COSTS and system in LOADED_PART_COSTS["default"]:
        if repair_item in LOADED_PART_COSTS["default"][system]:
            part_cost = LOADED_PART_COSTS["default"][system][repair_item]
            
            # Apply premium brand markup if applicable
            if brand in PREMIUM_BRAND_MARKUP:
                markup = PREMIUM_BRAND_MARKUP[brand]
                part_cost["min"] = int(part_cost["min"] * markup)
                part_cost["max"] = int(part_cost["max"] * markup)
    
    # Calculate labour cost if we have labour time
    if labour_time != "Unknown":
        try:
            # Extract hours from the string (e.g., "2.5 hours" -> 2.5)
            hours = float(labour_time.split()[0])
            labour_cost = hours * LABOUR_COST_PER_HOUR
            
            # Add labour cost to part cost
            total_min = part_cost["min"] + labour_cost
            total_max = part_cost["max"] + labour_cost
            
            return {"min": int(total_min), "max": int(total_max)}, labour_time
        except Exception as e:
            logger.error(f"Error calculating labour cost: {str(e)}")
    
    return part_cost, labour_time

def get_common_issues_for_vehicle(brand: str, model: str, year: int) -> List[str]:
    """Get common issues for a specific vehicle"""
    common_issues = load_common_issues()
    
    if brand not in common_issues or model not in common_issues[brand]:
        return []
    
    # Find the year range that includes this vehicle's year
    for year_range, issues in common_issues[brand][model].items():
        try:
            start_year, end_year = map(int, year_range.split('-'))
            if start_year <= year <= end_year:
                return issues
        except ValueError:
            continue
    
    return []
