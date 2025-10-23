#!/usr/bin/env python3
"""
Script to set up the required Airtable tables for the Garagefy quote system.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from pyairtable import Api
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_airtable_tables():
    """Set up the required Airtable tables for the quote system."""
    try:
        # Load environment variables
        load_dotenv()
        
        api_key = os.getenv('AIRTABLE_API_KEY')
        base_id = os.getenv('AIRTABLE_BASE_ID')
        
        if not api_key:
            logger.error("AIRTABLE_API_KEY environment variable not set")
            sys.exit(1)
        
        # Initialize Airtable API
        api = Api(api_key)
        base = api.base(base_id)
        
        # Table schemas
        tables_schema = {
            "Quotes": {
                "fields": [
                    {"name": "Request ID", "type": "singleLineText", "description": "ID of the service request"},
                    {"name": "Customer ID", "type": "singleLineText", "description": "ID of the customer"},
                    {"name": "Customer Name", "type": "singleLineText", "description": "Name of the customer"},
                    {"name": "Customer Email", "type": "email", "description": "Email of the customer"},
                    {"name": "Garage ID", "type": "singleLineText", "description": "ID of the garage"},
                    {"name": "Garage Name", "type": "singleLineText", "description": "Name of the garage"},
                    {"name": "Amount", "type": "currency", "options": {"precision": 2}, "description": "Quote amount in euros"},
                    {"name": "Notes", "type": "multilineText", "description": "Additional notes from the garage"},
                    {"name": "Valid Until", "type": "date", "description": "Date until the quote is valid (YYYY-MM-DD)"},
                    {"name": "Status", "type": "singleSelect", "options": {"choices": [
                        {"name": "pending", "color": "yellow"},
                        {"name": "accepted", "color": "green"},
                        {"name": "rejected", "color": "red"},
                        {"name": "expired", "color": "gray"}
                    ]}, "description": "Current status of the quote"},
                    {"name": "Created At", "type": "dateTime", "description": "When the quote was created"},
                    {"name": "Updated At", "type": "dateTime", "description": "When the quote was last updated"}
                ]
            },
            "Service Requests": {
                "fields_to_add": [
                    {"name": "Quote Count", "type": "number", "description": "Number of quotes received for this request"},
                    {"name": "Notified Garages Count", "type": "number", "description": "Number of garages notified about this request"},
                    {"name": "Quote Summary Sent", "type": "checkbox", "description": "Whether the quote summary has been sent to the customer"},
                    {"name": "Quote Summary Sent At", "type": "dateTime", "description": "When the quote summary was sent to the customer"}
                ]
            }
        }
        
        # Get existing tables
        existing_tables = base.tables()
        logger.info(f"Existing tables: {', '.join(existing_tables)}")
        
        # Create or update tables
        for table_name, schema in tables_schema.items():
            if table_name not in existing_tables:
                # Create new table
                logger.info(f"Creating table: {table_name}")
                table = base.create_table(table_name, fields=schema['fields'])
                logger.info(f"Created table: {table_name} with ID: {table.id}")
            else:
                # Table exists, check if we need to add fields
                logger.info(f"Table {table_name} already exists, checking fields...")
                table = base.table(table_name)
                existing_fields = {f['name']: f for f in table.fields()}
                
                # For Service Requests table, we only add fields
                if table_name == "Service Requests":
                    for field in schema['fields_to_add']:
                        field_name = field['name']
                        if field_name not in existing_fields:
                            logger.info(f"Adding field '{field_name}' to table '{table_name}'")
                            table.create_field(field_name, field['type'], options=field.get('options', {}))
                        else:
                            logger.info(f"Field '{field_name}' already exists in table '{table_name}'")
                else:
                    # For other tables, check all fields
                    for field in schema['fields']:
                        field_name = field['name']
                        if field_name not in existing_fields:
                            logger.info(f"Adding field '{field_name}' to table '{table_name}'")
                            table.create_field(field_name, field['type'], options=field.get('options', {}))
                        else:
                            logger.info(f"Field '{field_name}' already exists in table '{table_name}'")
        
        logger.info("Airtable tables setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Error setting up Airtable tables: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("Setting up Airtable tables for Garagefy quote system...")
    setup_airtable_tables()
    print("Setup completed!")
