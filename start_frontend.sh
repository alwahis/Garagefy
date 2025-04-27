#!/bin/bash
# Start the React frontend server
echo "Starting Garagefy React frontend on port 3006..."
cd frontend
cross-env PORT=3006 npm start
