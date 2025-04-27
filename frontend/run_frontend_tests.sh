#!/bin/bash
npm install
echo "Running all frontend tests..."
npm test -- --watchAll=false
