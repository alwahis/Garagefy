CAR_BRANDS = {
    "Toyota": {
        "Camry": list(range(2000, 2025)),
        "Corolla": list(range(2000, 2025)),
        "RAV4": list(range(2000, 2025)),
        "Highlander": list(range(2000, 2025)),
        "Prius": list(range(2004, 2025)),
        "Tacoma": list(range(2000, 2025))
    },
    "Honda": {
        "Civic": list(range(2000, 2025)),
        "Accord": list(range(2000, 2025)),
        "CR-V": list(range(2000, 2025)),
        "Pilot": list(range(2000, 2025)),
        "HR-V": list(range(2016, 2025)),
        "Odyssey": list(range(2000, 2025))
    },
    "BMW": {
        "3 Series": list(range(2000, 2025)),
        "5 Series": list(range(2000, 2025)),
        "X3": list(range(2000, 2025)),
        "X5": list(range(2000, 2025)),
        "7 Series": list(range(2000, 2025)),
        "M3": list(range(2000, 2025)),
        "M5": list(range(2000, 2025))
    },
    "Mercedes-Benz": {
        "C-Class": list(range(2000, 2025)),
        "E-Class": list(range(2000, 2025)),
        "GLC": list(range(2000, 2025)),
        "GLE": list(range(2000, 2025)),
        "S-Class": list(range(2000, 2025)),
        "A-Class": list(range(2019, 2025))
    },
    "Volkswagen": {
        "Golf": list(range(2000, 2025)),
        "Passat": list(range(2000, 2025)),
        "Tiguan": list(range(2009, 2025)),
        "Atlas": list(range(2018, 2025))
    },
    "Audi": {
        "A4": list(range(2000, 2025)),
        "A6": list(range(2000, 2025)),
        "Q5": list(range(2009, 2025)),
        "Q7": list(range(2007, 2025))
    }
}

# Service manual references and common issues
SERVICE_MANUALS = {
    "Toyota": {
        "manual_refs": {
            "Camry": "Toyota Camry Factory Service Manual (TSM-CAM-{year})",
            "Corolla": "Toyota Corolla Technical Guide (TTG-COR-{year})",
            "RAV4": "Toyota RAV4 Service & Repair Manual (SRM-RAV-{year})",
            "Highlander": "Toyota Highlander Technical Reference (THR-HIG-{year})",
            "Prius": "Toyota Prius Hybrid Service Manual (THS-PRI-{year})",
            "Tacoma": "Toyota Tacoma Truck Service Guide (TTG-TAC-{year})"
        },
        "repair_categories": {
            "engine": {
                "symptoms": ["Engine knocking", "Timing chain", "Oil consumption", "Rough idle", "Loss of power", "Check engine light"],
                "severity": {
                    "high": ["Engine knocking", "Timing chain failure"],
                    "medium": ["Oil consumption", "Check engine light"],
                    "low": ["Rough idle", "Minor power loss"]
                }
            },
            "transmission": {
                "symptoms": ["Shifting issues", "Transmission fluid", "Clutch", "Delayed engagement", "Slipping", "Grinding noise"],
                "severity": {
                    "high": ["No gear engagement", "Transmission fluid leak"],
                    "medium": ["Delayed shifting", "Grinding noise"],
                    "low": ["Minor shifting hesitation", "Transmission fluid service due"]
                }
            },
            "electrical": {
                "symptoms": ["Battery", "Alternator", "Starter", "Electrical shorts", "Warning lights", "Power windows"],
                "severity": {
                    "high": ["No start condition", "Alternator failure"],
                    "medium": ["Battery weak", "Intermittent electrical issues"],
                    "low": ["Warning light on", "Minor electrical glitches"]
                }
            },
            "suspension": {
                "symptoms": ["Shocks", "Struts", "Wheel alignment", "Bouncing", "Steering pull", "Tire wear"],
                "severity": {
                    "high": ["Broken springs", "Severe misalignment"],
                    "medium": ["Worn shocks", "Uneven tire wear"],
                    "low": ["Minor vibration", "Slight pull to one side"]
                }
            }
        }
    },
    "Honda": {
        "manual_refs": {
            "Civic": "Honda Civic Service Manual (HSM-CIV-{year})",
            "Accord": "Honda Accord Technical Guide (HTG-ACC-{year})",
            "CR-V": "Honda CR-V Repair Manual (HRM-CRV-{year})",
            "Pilot": "Honda Pilot Service Reference (HPR-PIL-{year})",
            "HR-V": "Honda HR-V Service Guide (HSG-HRV-{year})",
            "Odyssey": "Honda Odyssey Technical Documentation (HTD-ODY-{year})"
        },
        "repair_categories": {
            "engine": {
                "symptoms": ["VTEC system", "Timing belt", "Fuel injection", "Rough idle", "Loss of power", "Check engine light"],
                "severity": {
                    "high": ["VTEC failure", "Timing belt failure"],
                    "medium": ["Fuel injection issues", "Check engine light"],
                    "low": ["Rough idle", "Minor power loss"]
                }
            },
            "transmission": {
                "symptoms": ["CVT issues", "Automatic transmission", "Manual transmission", "Delayed engagement", "Slipping", "Grinding noise"],
                "severity": {
                    "high": ["No gear engagement", "Transmission fluid leak"],
                    "medium": ["Delayed shifting", "Grinding noise"],
                    "low": ["Minor shifting hesitation", "Transmission fluid service due"]
                }
            },
            "electrical": {
                "symptoms": ["ECU", "Sensors", "Wiring", "Electrical shorts", "Warning lights", "Power windows"],
                "severity": {
                    "high": ["No start condition", "ECU failure"],
                    "medium": ["Sensor issues", "Intermittent electrical issues"],
                    "low": ["Warning light on", "Minor electrical glitches"]
                }
            },
            "suspension": {
                "symptoms": ["Control arms", "Ball joints", "Bushings", "Bouncing", "Steering pull", "Tire wear"],
                "severity": {
                    "high": ["Broken control arms", "Severe misalignment"],
                    "medium": ["Worn ball joints", "Uneven tire wear"],
                    "low": ["Minor vibration", "Slight pull to one side"]
                }
            }
        }
    },
    "BMW": {
        "manual_refs": {
            "3 Series": "BMW 3 Series Technical Documentation (BTD-3S-{year})",
            "5 Series": "BMW 5 Series Service Guide (BSG-5S-{year})",
            "X3": "BMW X3 Repair Manual (BRM-X3-{year})",
            "X5": "BMW X5 Technical Reference (BTR-X5-{year})",
            "7 Series": "BMW 7 Series Service Documentation (BSD-7S-{year})",
            "M3": "BMW M3 Technical Guide (BTG-M3-{year})",
            "M5": "BMW M5 Service Manual (BSM-M5-{year})"
        },
        "repair_categories": {
            "engine": {
                "symptoms": ["VANOS", "Timing chain", "Turbocharger", "Rough idle", "Loss of power", "Check engine light"],
                "severity": {
                    "high": ["VANOS failure", "Timing chain failure"],
                    "medium": ["Turbocharger issues", "Check engine light"],
                    "low": ["Rough idle", "Minor power loss"]
                }
            },
            "transmission": {
                "symptoms": ["ZF transmission", "SMG", "Transfer case", "Delayed engagement", "Slipping", "Grinding noise"],
                "severity": {
                    "high": ["No gear engagement", "Transmission fluid leak"],
                    "medium": ["Delayed shifting", "Grinding noise"],
                    "low": ["Minor shifting hesitation", "Transmission fluid service due"]
                }
            },
            "electrical": {
                "symptoms": ["DME", "CAN bus", "Comfort access", "Electrical shorts", "Warning lights", "Power windows"],
                "severity": {
                    "high": ["No start condition", "DME failure"],
                    "medium": ["CAN bus issues", "Intermittent electrical issues"],
                    "low": ["Warning light on", "Minor electrical glitches"]
                }
            },
            "suspension": {
                "symptoms": ["Adaptive suspension", "Air suspension", "Dynamic control", "Bouncing", "Steering pull", "Tire wear"],
                "severity": {
                    "high": ["Broken springs", "Severe misalignment"],
                    "medium": ["Worn shocks", "Uneven tire wear"],
                    "low": ["Minor vibration", "Slight pull to one side"]
                }
            }
        }
    },
    "Mercedes-Benz": {
        "manual_refs": {
            "C-Class": "Mercedes C-Class Workshop Manual (MWM-C-{year})",
            "E-Class": "Mercedes E-Class Service Documentation (MSD-E-{year})",
            "GLC": "Mercedes GLC Technical Guide (MTG-GLC-{year})",
            "GLE": "Mercedes GLE Repair Manual (MRM-GLE-{year})",
            "S-Class": "Mercedes S-Class Service Reference (MSR-S-{year})",
            "A-Class": "Mercedes A-Class Technical Documentation (MTD-A-{year})"
        },
        "repair_categories": {
            "engine": {
                "symptoms": ["BlueTEC", "Kompressor", "Direct injection", "Rough idle", "Loss of power", "Check engine light"],
                "severity": {
                    "high": ["BlueTEC failure", "Kompressor failure"],
                    "medium": ["Direct injection issues", "Check engine light"],
                    "low": ["Rough idle", "Minor power loss"]
                }
            },
            "transmission": {
                "symptoms": ["7G-TRONIC", "9G-TRONIC", "4MATIC", "Delayed engagement", "Slipping", "Grinding noise"],
                "severity": {
                    "high": ["No gear engagement", "Transmission fluid leak"],
                    "medium": ["Delayed shifting", "Grinding noise"],
                    "low": ["Minor shifting hesitation", "Transmission fluid service due"]
                }
            },
            "electrical": {
                "symptoms": ["COMAND", "ESP", "ABC system", "Electrical shorts", "Warning lights", "Power windows"],
                "severity": {
                    "high": ["No start condition", "COMAND failure"],
                    "medium": ["ESP issues", "Intermittent electrical issues"],
                    "low": ["Warning light on", "Minor electrical glitches"]
                }
            },
            "suspension": {
                "symptoms": ["AIRMATIC", "Active Body Control", "Agility Control", "Bouncing", "Steering pull", "Tire wear"],
                "severity": {
                    "high": ["Broken springs", "Severe misalignment"],
                    "medium": ["Worn shocks", "Uneven tire wear"],
                    "low": ["Minor vibration", "Slight pull to one side"]
                }
            }
        }
    },
    "Volkswagen": {
        "manual_refs": {
            "Golf": "Volkswagen Golf Service Manual (VSM-GOL-{year})",
            "Passat": "Volkswagen Passat Technical Guide (VPG-PAS-{year})",
            "Tiguan": "Volkswagen Tiguan Repair Manual (VRM-TIG-{year})",
            "Atlas": "Volkswagen Atlas Service Reference (VAS-ATL-{year})"
        },
        "repair_categories": {
            "engine": {
                "symptoms": ["Timing belt", "Fuel injection", "Rough idle", "Loss of power", "Check engine light"],
                "severity": {
                    "high": ["Timing belt failure", "Fuel injection issues"],
                    "medium": ["Check engine light"],
                    "low": ["Rough idle", "Minor power loss"]
                }
            },
            "transmission": {
                "symptoms": ["Automatic transmission", "Manual transmission", "Delayed engagement", "Slipping", "Grinding noise"],
                "severity": {
                    "high": ["No gear engagement", "Transmission fluid leak"],
                    "medium": ["Delayed shifting", "Grinding noise"],
                    "low": ["Minor shifting hesitation", "Transmission fluid service due"]
                }
            },
            "electrical": {
                "symptoms": ["ECU", "Sensors", "Wiring", "Electrical shorts", "Warning lights", "Power windows"],
                "severity": {
                    "high": ["No start condition", "ECU failure"],
                    "medium": ["Sensor issues", "Intermittent electrical issues"],
                    "low": ["Warning light on", "Minor electrical glitches"]
                }
            },
            "suspension": {
                "symptoms": ["Shocks", "Struts", "Wheel alignment", "Bouncing", "Steering pull", "Tire wear"],
                "severity": {
                    "high": ["Broken springs", "Severe misalignment"],
                    "medium": ["Worn shocks", "Uneven tire wear"],
                    "low": ["Minor vibration", "Slight pull to one side"]
                }
            }
        }
    },
    "Audi": {
        "manual_refs": {
            "A4": "Audi A4 Service Manual (ASM-A4-{year})",
            "A6": "Audi A6 Technical Guide (ATG-A6-{year})",
            "Q5": "Audi Q5 Repair Manual (ARM-Q5-{year})",
            "Q7": "Audi Q7 Service Reference (ASR-Q7-{year})"
        },
        "repair_categories": {
            "engine": {
                "symptoms": ["Timing belt", "Fuel injection", "Rough idle", "Loss of power", "Check engine light"],
                "severity": {
                    "high": ["Timing belt failure", "Fuel injection issues"],
                    "medium": ["Check engine light"],
                    "low": ["Rough idle", "Minor power loss"]
                }
            },
            "transmission": {
                "symptoms": ["Automatic transmission", "Manual transmission", "Delayed engagement", "Slipping", "Grinding noise"],
                "severity": {
                    "high": ["No gear engagement", "Transmission fluid leak"],
                    "medium": ["Delayed shifting", "Grinding noise"],
                    "low": ["Minor shifting hesitation", "Transmission fluid service due"]
                }
            },
            "electrical": {
                "symptoms": ["ECU", "Sensors", "Wiring", "Electrical shorts", "Warning lights", "Power windows"],
                "severity": {
                    "high": ["No start condition", "ECU failure"],
                    "medium": ["Sensor issues", "Intermittent electrical issues"],
                    "low": ["Warning light on", "Minor electrical glitches"]
                }
            },
            "suspension": {
                "symptoms": ["Shocks", "Struts", "Wheel alignment", "Bouncing", "Steering pull", "Tire wear"],
                "severity": {
                    "high": ["Broken springs", "Severe misalignment"],
                    "medium": ["Worn shocks", "Uneven tire wear"],
                    "low": ["Minor vibration", "Slight pull to one side"]
                }
            }
        }
    }
}

# Dummy garage data with location information
NEARBY_GARAGES = [
    {
        "id": 1,
        "name": "AutoCare Express",
        "address": "123 Main Street",
        "distance": 0.5,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "rating": 4.5,
        "specialties": ["Toyota", "Honda"],
        "repair_capabilities": {
            "Toyota": ["engine", "transmission", "electrical"],
            "Honda": ["engine", "transmission", "electrical"]
        },
        "available_slots": ["9:00 AM", "2:00 PM", "4:00 PM"],
        "phone": "(555) 123-4567",
        "website": "www.autocareexpress.com"
    },
    {
        "id": 2,
        "name": "Premium Auto Service",
        "address": "456 Oak Avenue",
        "distance": 1.2,
        "latitude": 37.7746,
        "longitude": -122.4159,
        "rating": 4.8,
        "specialties": ["BMW", "Mercedes-Benz"],
        "repair_capabilities": {
            "BMW": ["engine", "electrical", "suspension"],
            "Mercedes-Benz": ["engine", "electrical", "suspension"]
        },
        "available_slots": ["10:00 AM", "1:00 PM", "3:00 PM"],
        "phone": "(555) 234-5678",
        "website": "www.premiumauto.com"
    }
]
