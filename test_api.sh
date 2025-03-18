#!/bin/bash
# Script to test the backend API endpoints

echo "Testing Garagefy API endpoints..."

# Test backend health endpoint
echo "Testing backend health endpoint..."
curl -s http://localhost:8099/health
echo -e "\n"

# Test car brands endpoint
echo "Testing car brands endpoint..."
curl -s http://localhost:8099/api/car-data
echo -e "\n"

# Test garages endpoint
echo "Testing garages endpoint..."
curl -s http://localhost:8099/api/garages | head -n 20
echo -e "\n..."

# Test diagnose endpoint
echo "Testing diagnose endpoint..."
curl -X POST -H "Content-Type: application/json" -d '{"car_brand":"toyota", "model":"corolla", "year":2018, "symptoms":"Car won'\''t start and makes clicking noise"}' http://localhost:8099/api/diagnose
echo -e "\n"

echo "API tests completed."
