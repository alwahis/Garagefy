#!/usr/bin/env python3
"""
ALLDATA Scraper Runner

This script runs the ALLDATA scraper to extract automotive repair data
for enhancing the Used Car Check feature with comprehensive vehicle analysis
based on trusted sources.
"""

import asyncio
import logging
import os
import sys

# Add parent directory to path to import scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.alldata_scraper import AlldataScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Run the ALLDATA scraper"""
    logger.info("Starting ALLDATA scraper")
    
    # Create scraper instance
    scraper = AlldataScraper()
    
    try:
        # Run the scraper
        data = await scraper.scrape_alldata()
        
        # Log results
        manufacturers_count = len(data.get("manufacturers", []))
        common_issues_count = sum(len(models) for make, models in data.get("common_issues", {}).items())
        labour_times_count = sum(len(models) for make, models in data.get("labour_times", {}).items())
        
        logger.info(f"Scraping completed successfully:")
        logger.info(f"- Extracted data for {manufacturers_count} manufacturers")
        logger.info(f"- Extracted common issues for {common_issues_count} models")
        logger.info(f"- Extracted labour times for {labour_times_count} models")
        
    except Exception as e:
        logger.error(f"Error running ALLDATA scraper: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
