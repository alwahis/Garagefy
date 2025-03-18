import sys
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.garage import Base, Garage
from ..core.database import SQLALCHEMY_DATABASE_URL
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sample_data():
    try:
        # Setup database connection
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create session
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Read sample data
        sample_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'sample_garages.json')
        with open(sample_data_path, 'r') as f:
            data = json.load(f)
        
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
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.append(project_root)
    
    load_sample_data()
