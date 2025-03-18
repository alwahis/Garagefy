"""
Repair cost estimation module for Garagefy platform
Provides cost estimates for various car repairs in Luxembourg
"""

from typing import Dict, List, Tuple
import random

# Luxembourg-specific repair cost data (in EUR)
# Format: {repair_category: {severity: {min_cost, max_cost, probability_distribution}}}
LUXEMBOURG_REPAIR_COSTS = {
    "engine": {
        "low": {"min": 150, "max": 500, "probabilities": [(0.6, "200-300"), (0.3, "300-400"), (0.1, "400-500")]},
        "medium": {"min": 500, "max": 1500, "probabilities": [(0.5, "600-900"), (0.3, "900-1200"), (0.2, "1200-1500")]},
        "high": {"min": 1500, "max": 5000, "probabilities": [(0.4, "1500-2500"), (0.4, "2500-4000"), (0.2, "4000-5000")]}
    },
    "transmission": {
        "low": {"min": 200, "max": 600, "probabilities": [(0.7, "250-400"), (0.2, "400-500"), (0.1, "500-600")]},
        "medium": {"min": 600, "max": 2000, "probabilities": [(0.5, "700-1200"), (0.3, "1200-1600"), (0.2, "1600-2000")]},
        "high": {"min": 2000, "max": 6000, "probabilities": [(0.3, "2000-3000"), (0.4, "3000-4500"), (0.3, "4500-6000")]}
    },
    "electrical": {
        "low": {"min": 100, "max": 400, "probabilities": [(0.6, "100-200"), (0.3, "200-300"), (0.1, "300-400")]},
        "medium": {"min": 400, "max": 1000, "probabilities": [(0.5, "400-600"), (0.3, "600-800"), (0.2, "800-1000")]},
        "high": {"min": 1000, "max": 3000, "probabilities": [(0.4, "1000-1500"), (0.4, "1500-2200"), (0.2, "2200-3000")]}
    },
    "brakes": {
        "low": {"min": 100, "max": 300, "probabilities": [(0.7, "100-180"), (0.2, "180-240"), (0.1, "240-300")]},
        "medium": {"min": 300, "max": 800, "probabilities": [(0.5, "300-500"), (0.3, "500-650"), (0.2, "650-800")]},
        "high": {"min": 800, "max": 2000, "probabilities": [(0.4, "800-1200"), (0.4, "1200-1600"), (0.2, "1600-2000")]}
    },
    "suspension": {
        "low": {"min": 150, "max": 500, "probabilities": [(0.6, "150-300"), (0.3, "300-400"), (0.1, "400-500")]},
        "medium": {"min": 500, "max": 1200, "probabilities": [(0.5, "500-800"), (0.3, "800-1000"), (0.2, "1000-1200")]},
        "high": {"min": 1200, "max": 3500, "probabilities": [(0.4, "1200-2000"), (0.4, "2000-2800"), (0.2, "2800-3500")]}
    },
    "cooling": {
        "low": {"min": 120, "max": 400, "probabilities": [(0.6, "120-220"), (0.3, "220-320"), (0.1, "320-400")]},
        "medium": {"min": 400, "max": 1000, "probabilities": [(0.5, "400-600"), (0.3, "600-800"), (0.2, "800-1000")]},
        "high": {"min": 1000, "max": 2500, "probabilities": [(0.4, "1000-1500"), (0.4, "1500-2000"), (0.2, "2000-2500")]}
    },
    "fuel": {
        "low": {"min": 100, "max": 500, "probabilities": [(0.6, "100-250"), (0.3, "250-400"), (0.1, "400-500")]},
        "medium": {"min": 500, "max": 1500, "probabilities": [(0.5, "500-800"), (0.3, "800-1200"), (0.2, "1200-1500")]},
        "high": {"min": 1500, "max": 4000, "probabilities": [(0.4, "1500-2500"), (0.4, "2500-3500"), (0.2, "3500-4000")]}
    },
    "exhaust": {
        "low": {"min": 100, "max": 400, "probabilities": [(0.7, "100-200"), (0.2, "200-300"), (0.1, "300-400")]},
        "medium": {"min": 400, "max": 1000, "probabilities": [(0.5, "400-600"), (0.3, "600-800"), (0.2, "800-1000")]},
        "high": {"min": 1000, "max": 2500, "probabilities": [(0.4, "1000-1500"), (0.4, "1500-2000"), (0.2, "2000-2500")]}
    },
    "general": {
        "low": {"min": 100, "max": 300, "probabilities": [(0.7, "100-180"), (0.2, "180-240"), (0.1, "240-300")]},
        "medium": {"min": 300, "max": 800, "probabilities": [(0.5, "300-500"), (0.3, "500-650"), (0.2, "650-800")]},
        "high": {"min": 800, "max": 2000, "probabilities": [(0.4, "800-1200"), (0.4, "1200-1600"), (0.2, "1600-2000")]}
    }
}

# Premium/luxury brand cost multipliers
BRAND_MULTIPLIERS = {
    "Mercedes-Benz": 1.4,
    "BMW": 1.35,
    "Audi": 1.3,
    "Porsche": 1.8,
    "Jaguar": 1.5,
    "Land Rover": 1.5,
    "Lexus": 1.3,
    "Volvo": 1.25,
    "Tesla": 1.6,
    "default": 1.0
}

# Age-based multipliers (older cars may require more work or harder-to-find parts)
AGE_MULTIPLIERS = {
    # Current year minus car year
    0: 1.0,    # New car
    1: 1.0,    # 1 year old
    2: 1.0,    # 2 years old
    3: 1.05,   # 3 years old
    4: 1.1,    # 4 years old
    5: 1.15,   # 5 years old
    6: 1.2,    # 6 years old
    7: 1.25,   # 7 years old
    8: 1.3,    # 8 years old
    9: 1.35,   # 9 years old
    10: 1.4,   # 10 years old
    11: 1.45,  # 11 years old
    12: 1.5,   # 12 years old
    13: 1.55,  # 13 years old
    14: 1.6,   # 14 years old
    15: 1.65,  # 15+ years old
}

def get_age_multiplier(year: int) -> float:
    """Calculate age-based cost multiplier based on car's age"""
    current_year = 2025  # Update this annually
    age = current_year - year
    
    if age <= 0:
        return 1.0
    elif age >= 15:
        return 1.65
    else:
        return AGE_MULTIPLIERS.get(age, 1.0)

def get_brand_multiplier(brand: str) -> float:
    """Get the brand-specific cost multiplier"""
    return BRAND_MULTIPLIERS.get(brand, BRAND_MULTIPLIERS["default"])

def estimate_repair_cost(category: str, severity: str, brand: str, year: int) -> Dict:
    """
    Estimate repair cost based on category, severity, brand, and year
    Returns a dictionary with min, max, and probability distribution of costs
    """
    # Default to general category if the specified category is not found
    if category not in LUXEMBOURG_REPAIR_COSTS:
        category = "general"
    
    # Default to medium severity if the specified severity is not found
    if severity not in ["low", "medium", "high"]:
        severity = "medium"
    
    # Get base cost range
    base_costs = LUXEMBOURG_REPAIR_COSTS[category][severity]
    
    # Apply multipliers
    brand_multiplier = get_brand_multiplier(brand)
    age_multiplier = get_age_multiplier(year)
    total_multiplier = brand_multiplier * age_multiplier
    
    # Calculate adjusted costs
    min_cost = round(base_costs["min"] * total_multiplier)
    max_cost = round(base_costs["max"] * total_multiplier)
    
    # Adjust probability distributions
    adjusted_probabilities = []
    for prob, range_str in base_costs["probabilities"]:
        min_val, max_val = map(int, range_str.split("-"))
        adj_min = round(min_val * total_multiplier)
        adj_max = round(max_val * total_multiplier)
        adjusted_probabilities.append((prob, f"{adj_min}-{adj_max}"))
    
    return {
        "min_cost": min_cost,
        "max_cost": max_cost,
        "currency": "EUR",
        "probability_distribution": adjusted_probabilities,
        "multipliers": {
            "brand": brand_multiplier,
            "age": age_multiplier,
            "total": total_multiplier
        }
    }

def format_cost_estimate(cost_data: Dict) -> str:
    """Format cost estimate data into a human-readable string"""
    result = f"Estimated Repair Cost: {cost_data['min_cost']}-{cost_data['max_cost']} {cost_data['currency']}\n\n"
    result += "Cost Breakdown (with probabilities):\n"
    
    for probability, cost_range in cost_data["probability_distribution"]:
        percentage = int(probability * 100)
        result += f"- {percentage}% chance: {cost_range} {cost_data['currency']}\n"
    
    result += f"\nNote: Estimates are adjusted for {cost_data['multipliers']['brand']}x brand factor "
    result += f"and {cost_data['multipliers']['age']}x age factor."
    
    return result
