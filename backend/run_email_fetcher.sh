#!/bin/bash

# Navigate to the project directory
cd /Users/mudhafar.hamid/Garagefy/backend

# Activate virtual environment if needed
source venv/bin/activate  # Uncomment if using a virtual environment

# Run the email fetcher script
python fetch_and_store_emails.py >> /tmp/email_fetcher.log 2>&1

# Add a timestamp to the log
echo "[$(date)] Email fetcher completed" >> /tmp/email_fetcher.log
