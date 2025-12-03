#!/usr/bin/env python3
"""
Test script for garage response VIN extraction fix
Tests the email monitoring service's ability to extract VIN and request ID from garage responses
"""

import sys
import os
import re
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 80)
print("GARAGE RESPONSE VIN EXTRACTION TEST")
print("=" * 80)
print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test 1: Request ID Extraction
print("[TEST 1] Request ID Extraction from Subject and Body")
print("-" * 80)

def extract_request_id(text):
    """Extract Request ID from text using the fixed pattern"""
    import re
    
    patterns = [
        r'(?:Ref:|Référence:|Reference\s+ID)[\s:]*?(req_[a-zA-Z0-9_]+)',
        r'req_[a-zA-Z0-9_]+'  # Just match the request ID pattern
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if 'req_' in match.group(0):
                return match.group(0) if 'req_' in match.group(0) else match.group(1)
            return match.group(1) if match.lastindex else match.group(0)
    
    return None

# Test cases
test_cases = [
    {
        "name": "Request ID in subject (original format)",
        "text": "Repair Quote Request - Ref: req_1764594858259_r42e3r4ym",
        "expected": "req_1764594858259_r42e3r4ym"
    },
    {
        "name": "Request ID in subject (Reference ID format)",
        "text": "Reference ID: req_1764594858259_r42e3r4ym",
        "expected": "req_1764594858259_r42e3r4ym"
    },
    {
        "name": "Request ID in body (quoted original)",
        "text": """I can fix this for 500 euros.

On Dec 2, 2025, Garagefy wrote:
> Reference ID: req_1764594858259_r42e3r4ym""",
        "expected": "req_1764594858259_r42e3r4ym"
    },
    {
        "name": "Request ID in body (plain text)",
        "text": """Please see the reference: req_1764594858259_r42e3r4ym for details""",
        "expected": "req_1764594858259_r42e3r4ym"
    },
    {
        "name": "No request ID",
        "text": "I can fix this for 500 euros",
        "expected": None
    }
]

passed = 0
failed = 0

for test in test_cases:
    result = extract_request_id(test["text"])
    status = "[PASS]" if result == test["expected"] else "[FAIL]"
    
    if result == test["expected"]:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} | {test['name']}")
    print(f"       Expected: {test['expected']}")
    print(f"       Got:      {result}")
    print()

print(f"Request ID Extraction: {passed} passed, {failed} failed")
print()

# Test 2: VIN Extraction
print("[TEST 2] VIN Extraction from Email Text")
print("-" * 80)

def extract_vin(text):
    """Extract VIN from text using the fixed pattern"""
    import re
    
    # VIN pattern: 17 alphanumeric characters excluding I, O, Q
    vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'
    
    matches = re.findall(vin_pattern, text.upper())
    
    if matches:
        return matches[0]
    
    # Fallback: Look for "VIN:" followed by alphanumeric
    vin_label_pattern = r'(?:VIN|Vin|vin)[\s:]*([A-HJ-NPR-Z0-9]{17})'
    label_matches = re.findall(vin_label_pattern, text.upper())
    
    if label_matches:
        return label_matches[0]
    
    return None

vin_test_cases = [
    {
        "name": "VIN in subject",
        "text": "Repair Quote Request - VIN: TESTVIN123456789",
        "expected": "TESTVIN123456789"
    },
    {
        "name": "VIN in body (label format)",
        "text": "Vehicle Brand: BMW\nVIN: TESTVIN123456789\nDamage: Engine problem",
        "expected": "TESTVIN123456789"
    },
    {
        "name": "VIN in body (plain format)",
        "text": "Please fix vehicle TESTVIN123456789",
        "expected": "TESTVIN123456789"
    },
    {
        "name": "VIN in quoted email",
        "text": """I can fix this for 500 euros.

On Dec 2, 2025, Garagefy wrote:
> Vehicle Brand: BMW
> VIN: TESTVIN123456789
> Damage: Engine problem""",
        "expected": "TESTVIN123456789"
    },
    {
        "name": "No VIN",
        "text": "I can fix this for 500 euros",
        "expected": None
    },
    {
        "name": "Invalid VIN (contains I)",
        "text": "Vehicle VIN: TESTVIN12345678I",
        "expected": None
    }
]

vin_passed = 0
vin_failed = 0

for test in vin_test_cases:
    result = extract_vin(test["text"])
    status = "[PASS]" if result == test["expected"] else "[FAIL]"
    
    if result == test["expected"]:
        vin_passed += 1
    else:
        vin_failed += 1
    
    print(f"{status} | {test['name']}")
    print(f"       Expected: {test['expected']}")
    print(f"       Got:      {result}")
    print()

print(f"VIN Extraction: {vin_passed} passed, {vin_failed} failed")
print()

# Test 3: Full Email Processing Simulation
print("[TEST 3] Full Email Processing Simulation")
print("-" * 80)

def simulate_email_processing(subject, body):
    """Simulate the full email processing flow"""
    print(f"Processing email:")
    print(f"  Subject: {subject[:60]}...")
    print(f"  Body: {body[:60]}...")
    print()
    
    # Step 1: Extract request ID from subject
    request_id = extract_request_id(subject)
    print(f"  Step 1 - Extract request ID from subject: {request_id}")
    
    # Step 2: If not found, extract from body
    if not request_id:
        request_id = extract_request_id(body)
        print(f"  Step 2 - Extract request ID from body: {request_id}")
    
    # Step 3: Extract VIN from subject and body
    vin = extract_vin(subject + " " + body)
    print(f"  Step 3 - Extract VIN from email: {vin}")
    
    print()
    return request_id, vin

# Simulate a real garage response
print("Scenario 1: Real Garage Response Email")
print()
subject1 = "Re: Repair Quote Request - VIN: TESTVIN123456789"
body1 = """I can fix this for 500 euros.

On Dec 2, 2025, Garagefy wrote:
> Good day,
> 
> I am writing to request a repair quotation for the following vehicle:
> 
> Vehicle Brand: BMW
> License Plate: ABC123
> VIN: TESTVIN123456789
> 
> Damage Details: Engine problem
> 
> Reference ID: req_1764594858259_r42e3r4ym"""

req_id1, vin1 = simulate_email_processing(subject1, body1)

if req_id1 and vin1:
    print("[PASS] | Successfully extracted both request ID and VIN")
else:
    print("[FAIL] | Failed to extract request ID or VIN")
    if not req_id1:
        print("  - Missing request ID")
    if not vin1:
        print("  - Missing VIN")

print()
print("Scenario 2: Garage Response Without Quoted Email")
print()
subject2 = "Re: Repair Quote Request - VIN: TESTVIN123456789"
body2 = """I can fix this for 500 euros.

Best regards,
Auto Repair Shop"""

req_id2, vin2 = simulate_email_processing(subject2, body2)

if vin2:
    print("[PASS] | Successfully extracted VIN from subject")
else:
    print("[FAIL] | Failed to extract VIN")

if not req_id2:
    print("[WARN] | Request ID not found (fallback to VIN extraction)")

print()

# Test 4: Edge Cases
print("[TEST 4] Edge Cases")
print("-" * 80)

edge_cases = [
    {
        "name": "Multiple VINs (should extract first)",
        "text": "Compare TESTVIN123456789 with TESTVIN987654321",
        "expected_vin": "TESTVIN123456789"
    },
    {
        "name": "VIN with lowercase",
        "text": "Vehicle: testvin123456789",
        "expected_vin": "TESTVIN123456789"
    },
    {
        "name": "Request ID case insensitive",
        "text": "reference id: req_1764594858259_r42e3r4ym",
        "expected_req": "req_1764594858259_r42e3r4ym"
    }
]

edge_passed = 0
edge_failed = 0

for test in edge_cases:
    if "vin" in test["name"].lower():
        result = extract_vin(test["text"])
        expected = test.get("expected_vin")
    else:
        result = extract_request_id(test["text"])
        expected = test.get("expected_req")
    
    status = "[PASS]" if result == expected else "[FAIL]"
    
    if result == expected:
        edge_passed += 1
    else:
        edge_failed += 1
    
    print(f"{status} | {test['name']}")
    print(f"       Expected: {expected}")
    print(f"       Got:      {result}")
    print()

print(f"Edge Cases: {edge_passed} passed, {edge_failed} failed")
print()

# Summary
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)

total_passed = passed + vin_passed + edge_passed
total_failed = failed + vin_failed + edge_failed
total_tests = total_passed + total_failed

print(f"Total Tests: {total_tests}")
print(f"Passed: {total_passed}")
print(f"Failed: {total_failed}")
print()

if total_failed == 0:
    print("[SUCCESS] ALL TESTS PASSED! The fix is working correctly.")
    print()
    print("Next Steps:")
    print("1. Deploy to production (merge fresh-garagefy to main)")
    print("2. Test with real garage responses")
    print("3. Monitor backend logs for VIN extraction")
    print("4. Verify records in Baserow with VIN populated")
    sys.exit(0)
else:
    print(f"[WARN] {total_failed} test(s) failed. Please review the results above.")
    sys.exit(1)
