#!/bin/bash
# Script to run Garagefy with all fixes applied

echo "=== Stopping any running Garagefy processes ==="
pkill -f "npm start" || true
pkill -f "python -m uvicorn" || true
pkill -f "uvicorn app.main:app" || true

echo "=== Waiting for all processes to fully stop ==="
sleep 3

echo "=== Starting Garagefy with fixed Used Car Check functionality ==="
cd /Users/mudhafar.hamid/Garagefy

# Start backend in background
echo "Starting backend on port 8099..."
./start_backend.sh &
backend_pid=$!

# Wait for backend to initialize
echo "Waiting for backend to initialize..."
sleep 10

# Start frontend
echo "Starting frontend on port 3001..."
echo "Once frontend is started, access the application at: http://localhost:3001"
./start_frontend.sh

# Cleanup when script terminates
trap "kill $backend_pid; exit" INT TERM EXIT
