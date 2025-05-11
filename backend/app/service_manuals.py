"""
Service manual database for car diagnostics.
This module contains diagnostic information from various car service manuals.
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to service manual JSON files
MANUALS_DIR = Path(__file__).parent / "data" / "manuals"

# Cache for loaded service manuals
LOADED_MANUALS = {}

def load_service_manual(brand: str) -> Dict:
    """Load service manual for a specific brand"""
    brand = brand.lower()
    
    # Return from cache if already loaded
    if brand in LOADED_MANUALS:
        return LOADED_MANUALS[brand]
    
    # Try to find the manual file
    manual_path = MANUALS_DIR / f"{brand}.json"
    if not manual_path.exists():
        logger.warning(f"Service manual for {brand} not found at {manual_path}")
        return {}
    
    try:
        with open(manual_path, 'r') as f:
            manual_data = json.load(f)
            LOADED_MANUALS[brand] = manual_data
            logger.info(f"Loaded service manual for {brand}")
            return manual_data
    except Exception as e:
        logger.error(f"Error loading service manual for {brand}: {str(e)}")
        return {}

def get_available_manuals() -> List[str]:
    """Get list of available service manuals"""
    try:
        return [f.stem for f in MANUALS_DIR.glob("*.json")]
    except Exception as e:
        logger.error(f"Error listing available manuals: {str(e)}")
        return []

def find_matching_subsystem(manual_data: Dict, symptoms: str) -> Optional[Dict]:
    """Find the subsystem that best matches the symptoms"""
    if not manual_data or "systems" not in manual_data:
        return None
    
    symptoms_lower = symptoms.lower()
    best_match = None
    max_matches = 0
    
    # Check each system and subsystem for symptom matches
    for system in manual_data.get("systems", []):
        for subsystem in system.get("subsystems", []):
            subsystem_data = subsystem.get("data", {})
            symptom_list = subsystem_data.get("symptoms", [])
            
            # Count how many symptoms match
            matches = sum(1 for symptom in symptom_list if symptom.lower() in symptoms_lower)
            
            if matches > max_matches:
                max_matches = matches
                best_match = {
                    "system": system.get("system", "Unknown"),
                    "subsystem": subsystem.get("name", "Unknown"),
                    "data": subsystem_data,
                    "matches": matches
                }
    
    return best_match

def get_manual_diagnosis(brand: str, model: str, year: int, symptoms: str) -> Dict:
    """Get diagnosis from service manual with document references"""
    # Load the service manual for the brand
    manual_data = load_service_manual(brand)
    
    # If no manual data is available, return a generic response
    if not manual_data:
        logger.warning(f"No service manual data available for {brand}")
        return {
            'severity': 'Unknown',
            'potential_issues': [{
                'issue': 'No service manual data available',
                'description': f'No manufacturer service manual data available for {brand} {model} {year}',
                'probability': 'Unknown',
                'reference': f"Generic automotive troubleshooting guide"
            }],
            'service_code': 'GENERIC-001',
            'manual_section': 'General Diagnostics'
        }
    
    # Find the subsystem that best matches the symptoms
    matching_subsystem = find_matching_subsystem(manual_data, symptoms)
    
    if not matching_subsystem:
        # If no specific match found, return a generic response with the brand manual reference
        return {
            'severity': 'Medium',
            'potential_issues': [{
                'issue': 'General diagnosis required',
                'description': f'Based on the symptoms for {brand} {model} {year}: {symptoms}',
                'probability': 'Medium',
                'reference': f"{brand} Service Manual {year} - General Diagnostics"
            }],
            'service_code': f'{brand[:3].upper()}-GEN',
            'manual_section': 'General Diagnostics'
        }
    
    # Extract the matched subsystem data
    system = matching_subsystem["system"]
    subsystem = matching_subsystem["subsystem"]
    subsystem_data = matching_subsystem["data"]
    
    # Extract potential issues from the matched subsystem
    potential_issues = []
    for cause in subsystem_data.get("causes", []):
        issue = {
            'issue': cause.get("issue", "Unknown issue"),
            'description': f'Symptoms match {system} > {subsystem} issues in the {brand} service manual',
            'probability': cause.get("severity", "MEDIUM").capitalize(),
            'estimated_cost': f"${cause.get('cost_range', {}).get('min', 0)}-${cause.get('cost_range', {}).get('max', 0)}",
            'reference': cause.get("reference", f"{brand} Service Manual - {system} > {subsystem}")
        }
        potential_issues.append(issue)
    
    # Extract diagnostic steps from the matched subsystem
    diagnostic_steps = []
    for step in subsystem_data.get("diagnostic_steps", []):
        diagnostic_step = {
            'step': step.get("action", "Unknown action"),
            'tools_needed': step.get("tools_needed", []),
            'specifications': step.get("specifications", {}),
            'reference': step.get("reference", f"{brand} Service Manual - {system} > {subsystem}")
        }
        diagnostic_steps.append(diagnostic_step)
    
    # Create the diagnosis response
    diagnosis = {
        'severity': 'High' if any(issue['probability'] == 'High' for issue in potential_issues) else 'Medium',
        'potential_issues': potential_issues,
        'diagnostic_steps': diagnostic_steps,
        'system': system,
        'subsystem': subsystem,
        'service_code': f'{brand[:3].upper()}-{system[:3].upper()}-{subsystem[:3].upper()}',
        'manual_section': f"{brand} Service Manual - {system} > {subsystem}"
    }
    
    return diagnosis

def get_manual_reference(brand: str, model: str, year: int, system: str = None, subsystem: str = None) -> str:
    """Get manual reference with specific section if available"""
    if system and subsystem:
        return f"{brand} {model} {year} Service Manual - {system} > {subsystem}"
    return f"{brand} {model} {year} Service Manual"
