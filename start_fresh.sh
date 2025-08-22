#!/bin/bash
# This script:
# 1. Stops any running Garagefy instances
# 2. Starts a fresh instance
# 3. Notifies when ready

echo "=== Stopping any running Garagefy processes ==="
pkill -f "npm start" || true
pkill -f "python -m uvicorn" || true
pkill -f "uvicorn app.main:app" || true

echo "=== Waiting for all processes to fully stop ==="
sleep 3

echo "=== Starting Garagefy with fixed used car check functionality ==="
# Go to Garagefy directory
cd /Users/mudhafar.hamid/Garagefy

# Start using normal start script
./start.sh
