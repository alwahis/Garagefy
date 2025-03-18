import json
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..core.database import get_db
from ..models.garage import Base, Garage
import logging

logger = logging.getLogger(__name__)

async def load_sample_data():
    try:
        # Read sample data
        with open('sample_garages.json', 'r') as f:
            data = json.load(f)
        
        # Get database session
        db = next(get_db())
        
        # Clear existing data
        db.query(Garage).delete()
        
        # Insert sample garages
        for garage_data in data['garages']:
            garage = Garage(
                name=garage_data['name'],
                address=garage_data['address'],
                phone=garage_data['phone'],
                services=garage_data['services'],
                opening_hours=garage_data['opening_hours'],
                latitude=garage_data['latitude'],
                longitude=garage_data['longitude'],
                url=garage_data['url']
            )
            db.add(garage)
        
        # Commit changes
        db.commit()
        logger.info(f"Successfully loaded {len(data['garages'])} sample garages")
        
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(load_sample_data())
