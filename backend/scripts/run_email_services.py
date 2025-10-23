import asyncio
import time
import os
import sys

# Set up paths
from scripts import setup_paths
setup_paths()

# Import services
from scripts.ingest_garage_replies import ingest_garage_replies
from scripts.send_summary_email import SummaryEmailService

async def run_services():
    summary_service = SummaryEmailService()
    
    while True:
        try:
            # Run email ingestion
            print("\n--- Checking for new garage replies ---")
            await ingest_garage_replies()
            
            # Check and send summary emails
            print("\n--- Checking for VINs ready for summary ---")
            await summary_service.check_and_send_summary()
            
            # Wait for 1 minute before next check
            print("\nWaiting 1 minute before next check...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            await asyncio.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    print("Starting Garagefy Email Services...")
    print("Press Ctrl+C to stop\n")
    
    try:
        asyncio.run(run_services())
    except KeyboardInterrupt:
        print("\nStopping Garagefy Email Services...")
