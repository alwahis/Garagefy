#!/bin/bash
# Master script to start both backend and frontend
echo "Starting Garagefy application..."

# Make the scripts executable
chmod +x start_backend.sh
chmod +x start_frontend.sh

# Check and setup Python environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Check and setup Node environment
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start backend in the background
echo "Starting backend on port 8099..."
./start_backend.sh &
backend_pid=$!

# Wait a moment for the backend to initialize
sleep 5

# Start frontend
echo "Starting frontend on port 1234..."
echo "Once the frontend is started, you can access the application at: http://localhost:1234"
./start_frontend.sh

# Cleanup when the script is terminated
trap "kill $backend_pid; exit" INT TERM EXIT
