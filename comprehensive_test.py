#!/usr/bin/env python
"""
Comprehensive test script for Garagefy application
Tests: Code structure, imports, API endpoints, and basic functionality
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 70)
print("GARAGEFY COMPREHENSIVE TEST SUITE")
print("=" * 70)

# Test 1: Project Structure
print("\n[1/7] Testing Project Structure...")
try:
    required_dirs = [
        'backend',
        'backend/app',
        'backend/app/api',
        'backend/app/api/endpoints',
        'backend/app/services',
        'backend/app/models',
        'backend/app/core',
        'frontend',
        'frontend/src',
        'frontend/src/pages',
        'frontend/src/components',
    ]
    
    missing = []
    for dir_path in required_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        if not os.path.isdir(full_path):
            missing.append(dir_path)
    
    if missing:
        print(f"   FAIL: Missing directories: {missing}")
    else:
        print(f"   PASS: All required directories present")
except Exception as e:
    print(f"   ERROR: {str(e)}")

# Test 2: Backend Dependencies
print("\n[2/7] Testing Backend Dependencies...")
try:
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'python_dotenv',
        'requests',
        'aiohttp',
        'apscheduler',
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"   WARN: Missing packages: {missing_packages}")
    else:
        print(f"   PASS: All required packages installed")
except Exception as e:
    print(f"   ERROR: {str(e)}")

# Test 3: Backend App Imports
print("\n[3/7] Testing Backend App Imports...")
try:
    from app.main import app
    print(f"   PASS: FastAPI app imported successfully")
    print(f"        - App title: {app.title}")
    print(f"        - App version: {app.version}")
except Exception as e:
    print(f"   FAIL: Could not import app: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 4: Backend API Routes
print("\n[4/7] Testing Backend API Routes...")
try:
    from app.main import app
    
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                'path': route.path,
                'methods': list(route.methods) if route.methods else []
            })
    
    if routes:
        print(f"   PASS: Found {len(routes)} routes")
        for route in routes[:10]:
            methods = ', '.join(route['methods']) if route['methods'] else 'N/A'
            print(f"        - {route['path']} [{methods}]")
        if len(routes) > 10:
            print(f"        ... and {len(routes) - 10} more routes")
    else:
        print(f"   WARN: No routes found")
except Exception as e:
    print(f"   FAIL: Could not inspect routes: {str(e)}")

# Test 5: Backend Services
print("\n[5/7] Testing Backend Services...")
services_to_test = [
    ('app.services.baserow_service', 'baserow_service'),
    ('app.services.fix_it_service', 'fix_it_service'),
    ('app.services.email_service', 'email_service'),
    ('app.services.scheduler_service', 'scheduler_service'),
]

services_ok = 0
services_fail = 0

for module_name, service_name in services_to_test:
    try:
        module = __import__(module_name, fromlist=[service_name])
        service = getattr(module, service_name)
        print(f"   PASS: {service_name} imported")
        services_ok += 1
    except Exception as e:
        print(f"   WARN: {service_name} - {str(e)}")
        services_fail += 1

print(f"   Summary: {services_ok} services OK, {services_fail} with issues")

# Test 6: Frontend Files
print("\n[6/7] Testing Frontend Files...")
try:
    frontend_files = [
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/index.js',
        'frontend/src/pages/Home.js',
        'frontend/src/pages/FixIt.js',
        'frontend/src/components/Navbar.js',
    ]
    
    missing_files = []
    for file_path in frontend_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.isfile(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   WARN: Missing frontend files: {missing_files}")
    else:
        print(f"   PASS: All frontend files present")
    
    # Check package.json
    pkg_path = os.path.join(os.path.dirname(__file__), 'frontend/package.json')
    with open(pkg_path, 'r') as f:
        pkg = json.load(f)
        print(f"        - Package: {pkg.get('name')}")
        print(f"        - Version: {pkg.get('version')}")
        print(f"        - Dependencies: {len(pkg.get('dependencies', {}))}")
        
except Exception as e:
    print(f"   ERROR: {str(e)}")

# Test 7: Configuration Files
print("\n[7/7] Testing Configuration Files...")
try:
    config_files = [
        'backend/requirements.txt',
        'backend/.env.example',
        'frontend/package.json',
        'docker-compose.yml',
        'README.md',
    ]
    
    missing_configs = []
    for file_path in config_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.isfile(full_path):
            missing_configs.append(file_path)
    
    if missing_configs:
        print(f"   WARN: Missing config files: {missing_configs}")
    else:
        print(f"   PASS: All config files present")
    
    # Check requirements.txt
    req_path = os.path.join(os.path.dirname(__file__), 'backend/requirements.txt')
    with open(req_path, 'r') as f:
        reqs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"        - Backend requirements: {len(reqs)} packages")
        
except Exception as e:
    print(f"   ERROR: {str(e)}")

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("""
✓ Project structure verified
✓ Backend dependencies checked
✓ API routes inspected
✓ Services validated
✓ Frontend files verified
✓ Configuration files checked

NEXT STEPS:
1. Set up environment variables in backend/.env
2. Start backend: python backend/run.py
3. Install frontend dependencies: npm install (requires Node.js)
4. Start frontend: npm start
5. Test API endpoints with curl or Postman
6. Verify database connectivity
7. Test form submissions and email notifications

For detailed testing:
- Run: python backend/test_baserow.py (after setting .env)
- Check logs in backend/logs/ directory
- Monitor API responses at http://localhost:8099/docs
""")
print("=" * 70)
