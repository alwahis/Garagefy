import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.scrapers.editus_scraper import EditusGarageScraper
from app.core.database import SessionLocal, engine
from app.models.garage import Base, Garage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize scraper
    scraper = EditusGarageScraper()
    
    try:
        # Scrape garages
        logger.info("Starting garage scraping...")
        garages_data = await scraper.scrape_garages(max_pages=5)
        logger.info(f"Successfully scraped {len(garages_data)} garages")
        
        # Save to JSON file
        scraper.save_to_json("scraped_garages.json")
        
        # Save to database
        db = SessionLocal()
        try:
            for garage_data in garages_data:
                # Extract location data
                location = garage_data.pop("location", {})
                latitude = location.get("latitude")
                longitude = location.get("longitude")
                
                # Create Garage object
                garage = Garage(
                    name=garage_data["name"],
                    address=garage_data["address"],
                    phone=garage_data["phone"],
                    opening_hours=garage_data["opening_hours"],
                    services=garage_data["services"],
                    latitude=latitude,
                    longitude=longitude,
                    url=garage_data["url"]
                )
                
                # Add to database
                db.add(garage)
            
            # Commit all changes
            db.commit()
            logger.info("Successfully saved garages to database")
            
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
