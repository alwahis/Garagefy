#!/bin/bash
# Script to test Used Car Check API endpoints

echo "==== Testing /api/used-car/options ===="
curl -s http://localhost:8099/api/used-car/options | jq '.'

echo "==== Testing /api/used-car/check ===="
curl -s -X POST http://localhost:8099/api/used-car/check \
    -H "Content-Type: application/json" \
    -d '{
      "make": "Toyota",
      "model": "Corolla",
      "year": 2015,
      "mileage": 60000,
      "fuel_type": "petrol",
      "transmission": "manual"
    }' | jq '.'
