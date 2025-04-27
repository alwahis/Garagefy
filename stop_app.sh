#!/bin/bash
# Script to stop all Garagefy processes

echo "=== Stopping all Garagefy processes ==="
pkill -f "npm start" || true
pkill -f "python -m uvicorn" || true
pkill -f "uvicorn app.main:app" || true

echo "=== All Garagefy processes have been stopped ==="
