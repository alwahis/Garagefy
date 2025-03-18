#!/bin/bash
# Start the FastAPI backend server
echo "Starting Garagefy FastAPI backend on port 8099..."
source venv/bin/activate || echo "Virtual environment not found, proceeding without activation"
python main.py
