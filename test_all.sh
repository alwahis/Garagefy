#!/bin/bash
set -e

echo "Testing entire Garagefy app..."

# Ensure scripts are executable
chmod +x start.sh start_backend.sh start_frontend.sh frontend/run_frontend_tests.sh

# Start backend & frontend
bash start.sh &
APP_PID=$!
# Allow services to initialize
sleep 10

# Run frontend tests
echo "\n=== Frontend Tests ==="
bash frontend/run_frontend_tests.sh

# Run backend API checks
echo "\n=== Backend API Tests ==="
BASE_URL=http://localhost:8099
endpoints=("/" "/health" "/api/car-data")
for ep in "${endpoints[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$ep")
  if [ "$status" -ne 200 ]; then
    echo "FAIL: $ep returned HTTP $status" >&2
    kill $APP_PID
    exit 1
  else
    echo "OK: $ep returned 200"
  fi
done

# Cleanup
kill $APP_PID

echo "\nAll tests passed successfully!"
