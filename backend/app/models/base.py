from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base class
Base = declarative_base()

# We'll import models in the database.py file after Base is defined
# to avoid circular imports
