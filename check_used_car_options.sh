#!/bin/bash
# Start backend (assumes venv and requirements already installed)
cd /Users/mudhafar.hamid/Garagefy
chmod +x start.sh
./start.sh &
BACKEND_PID=$!
sleep 10

echo "Checking /api/used-car/options..."
curl -s http://localhost:8099/api/used-car/options | tee used_car_options_output.json

# Kill the backend after check
echo "Stopping backend..."
kill $BACKEND_PID
