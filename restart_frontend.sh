#!/bin/bash
# Restart React frontend to pick up code changes

echo "=== Stopping existing React processes ==="
pkill -f "react-scripts start" || true
pkill -f webpack-dev-server || true

sleep 2

echo "=== Starting React frontend ==="
cd frontend
npm start
