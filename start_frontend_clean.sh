#!/bin/bash

# Kill any existing frontend processes
pkill -f "npm start"
pkill -f "node.*react-scripts"

# Wait for processes to terminate
sleep 2

# Start frontend on port 3008
cd frontend && PORT=3008 npm start
