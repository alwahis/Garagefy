#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Garagefy locally...${NC}"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}tmux is not installed. Please install it first.${NC}"
    echo "You can install it with: brew install tmux"
    exit 1
fi

# Create a new tmux session
SESSION_NAME="garagefy"

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION_NAME

# Split the window horizontally
tmux split-window -h -t $SESSION_NAME

# Start backend in the left pane
tmux send-keys -t $SESSION_NAME:0.0 "cd $(pwd)/backend && python -m app.main" C-m

# Start frontend in the right pane
tmux send-keys -t $SESSION_NAME:0.1 "cd $(pwd)/frontend && npm start" C-m

echo -e "${GREEN}Garagefy servers are starting...${NC}"
echo -e "${BLUE}Backend will be available at: ${GREEN}http://localhost:8099${NC}"
echo -e "${BLUE}Frontend will be available at: ${GREEN}http://localhost:3000${NC}"
echo -e "${BLUE}Attach to tmux session with: ${GREEN}tmux attach -t $SESSION_NAME${NC}"
echo -e "${BLUE}Detach from tmux session with: ${GREEN}Ctrl+B, then D${NC}"

# Attach to the tmux session
tmux attach -t $SESSION_NAME
