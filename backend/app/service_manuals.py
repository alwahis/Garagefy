"""
Service manual database for car diagnostics.
This module contains diagnostic information from various car service manuals.
"""

# Service manual database structure
SERVICE_MANUALS = {
    'BMW': {
        'models': {
            '3 Series': {
                'engine': {
                    'noise': {
                        'potential_issues': [
                            {
                                'issue': 'Timing Chain Wear',
                                'probability': 'High',
                                'actions': [
                                    'Check timing chain tensioner',
                                    'Inspect chain guides for wear',
                                    'Listen for rattling noise at startup'
                                ],
                                'estimated_cost': '$800-1500',
                                'manual_section': 'Engine > Timing Components > Section 11-30'
                            },
                            {
                                'issue': 'VANOS System Failure',
                                'probability': 'Medium',
                                'actions': [
                                    'Check VANOS solenoids',
                                    'Inspect seals for leaks',
                                    'Verify timing with diagnostic tool'
                                ],
                                'estimated_cost': '$600-1200',
                                'manual_section': 'Engine > VANOS > Section 11-34'
                            }
                        ],
                        'severity': 'Medium',
                        'service_code': 'BMW-ENG-001'
                    },
                    'overheating': {
                        'potential_issues': [
                            {
                                'issue': 'Electric Water Pump Failure',
                                'probability': 'High',
                                'actions': [
                                    'Check pump operation',
                                    'Test electrical connections',
                                    'Verify coolant circulation'
                                ],
                                'estimated_cost': '$800-1200',
                                'manual_section': 'Cooling > Water Pump > Section 17-10'
                            }
                        ],
                        'severity': 'High',
                        'service_code': 'BMW-ENG-002'
                    }
                }
            }
        }
    },
    'Mercedes-Benz': {
        'models': {
            'C-Class': {
                'transmission': {
                    'shifting': {
                        'potential_issues': [
                            {
                                'issue': '13-Pin Connector Failure',
                                'probability': 'High',
                                'actions': [
                                    'Check connector for corrosion',
                                    'Test pin continuity',
                                    'Inspect transmission fluid'
                                ],
                                'estimated_cost': '$400-800',
                                'manual_section': 'Transmission > Electrical > Section 27-15'
                            },
                            {
                                'issue': 'Valve Body Issues',
                                'probability': 'Medium',
                                'actions': [
                                    'Perform transmission adaptation',
                                    'Check solenoid operation',
                                    'Inspect valve body assembly'
                                ],
                                'estimated_cost': '$1500-2500',
                                'manual_section': 'Transmission > Valve Body > Section 27-20'
                            }
                        ],
                        'severity': 'Medium',
                        'service_code': 'MB-TRN-001'
                    }
                }
            }
        }
    },
    'Toyota': {
        'models': {
            'Camry': {
                'engine': {
                    'vibration': {
                        'potential_issues': [
                            {
                                'issue': 'Motor Mounts',
                                'probability': 'High',
                                'actions': [
                                    'Inspect all engine mounts',
                                    'Check for rubber deterioration',
                                    'Test under load conditions'
                                ],
                                'estimated_cost': '$300-600',
                                'manual_section': 'Engine Mechanical > Mounts > Section EM-60'
                            }
                        ],
                        'severity': 'Medium',
                        'service_code': 'TOY-ENG-001'
                    }
                }
            }
        }
    }
}

def get_manual_diagnosis(brand, model, year, symptoms):
    """Get diagnosis from service manual"""
    # This is a mock implementation. In a real app, this would query a database of service manuals
    return {
        'severity': 'Medium',
        'potential_issues': [{
            'issue': 'Service Manual Diagnosis',
            'description': f'Based on the symptoms for {brand} {model} {year}: {symptoms}',
            'probability': 'Medium',
            'technical_details': {
                'system_affected': 'Engine',
                'components': ['Engine Control Module', 'Sensors'],
                'common_causes': ['Faulty sensor', 'Wiring issues']
            },
            'diagnostic_steps': [
                {
                    'step': 'Visual Inspection',
                    'details': 'Check for obvious signs of damage or wear',
                    'warning_signs': ['Corrosion', 'Loose connections'],
                    'expected_values': 'No visible damage'
                }
            ],
            'actions': [
                'Perform diagnostic scan',
                'Check sensor connections',
                'Verify wiring integrity'
            ],
            'safety_notes': [
                'Ensure engine is cool before inspection',
                'Disconnect battery before working on electrical components'
            ]
        }],
        'service_code': f'{brand[:3].upper()}-001',
        'manual_section': 'Engine Diagnostics'
    }

def get_manual_reference(brand, model, year):
    """Get manual reference"""
    # This is a mock implementation
    return f"{brand} {model} {year} Service Manual - Section 3.2"
