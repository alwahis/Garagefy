import os
from typing import Dict, List, Optional, Any
from pyairtable import Api
from dotenv import load_dotenv
from datetime import datetime, timezone
import logging
import json

# Load environment variables
load_dotenv()

class AirtableService:
    def __init__(self):
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        # Read base ID from environment variable instead of hardcoding
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.table_name = 'Customer details'  # Table name in Airtable (exact match)
        
        if not self.api_key:
            raise ValueError("Missing Airtable API key. Please set AIRTABLE_API_KEY in .env")
        if not self.base_id:
            raise ValueError("Missing Airtable base ID. Please set AIRTABLE_BASE_ID in .env")
            
        # Initialize Airtable API with the personal access token
        self.api = Api(api_key=self.api_key)
        self.table = None
        self.logger = logging.getLogger(__name__)
        
    def record_garage_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record a garage's response in the 'Received' table
        
        Args:
            response_data: Dictionary containing response details with keys:
                - garage_name: Name of the garage
                - garage_email: Email of the garage
                - request_id: The service request ID this response is for
                - quote_amount: The quoted amount (optional)
                - notes: Additional notes from the garage (optional)
                - status: Status of the response (e.g., 'quoted', 'declined')
                
        Returns:
            Dict with 'success' status and created record or error message
        """
        try:
            # Prepare the record data for Airtable
            record_data = {
                'Garage Name': response_data.get('garage_name', ''),
                'Email': response_data.get('garage_email', ''),
                'Request ID': response_data.get('request_id'),
                'Quote Amount': response_data.get('quote_amount'),
                'Notes': response_data.get('notes', ''),
                'Status': response_data.get('status', 'received'),
                'Response Date': response_data.get('response_date', datetime.now(timezone.utc).isoformat())
            }
            
            # Remove None values to avoid Airtable errors
            record_data = {k: v for k, v in record_data.items() if v is not None}
            
            # Create the record in the 'Received' table
            table = self._get_table('Received')
            record = table.create(record_data)
            
            self.logger.info(f"Recorded garage response from {response_data.get('garage_name')} for request {response_data.get('request_id')}")
            
            return {
                'success': True,
                'record': record,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Error recording garage response: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'record': None,
                'error': error_msg
            }
            
    def _get_table(self, table_name=None):
        """Get Airtable table instance with error handling"""
        try:
            table_to_use = table_name or self.table_name
            self.logger.info(f"Accessing Airtable table: {table_to_use} in base: {self.base_id}")
            return self.api.table(self.base_id, table_to_use)
        except Exception as e:
            self.logger.error(f"Error accessing Airtable: {str(e)}")
            raise
    
    def get_all_garages(self) -> List[Dict[str, Any]]:
        """
        Fetch all garages from Airtable 'Fix it' table
        
        Returns:
            List of garage dictionaries
        """
        try:
            table = self._get_table('Fix it')
            records = table.all()
            
            garages = []
            for record in records:
                fields = record.get('fields', {})
                
                # Extract garage information - using correct field names from Airtable
                garage = {
                    'id': record.get('id'),
                    'name': fields.get('Name', ''),
                    'email': fields.get('Email', ''),
                    'address': fields.get('Address', ''),
                    'phone': fields.get('Phone', ''),
                    'website': fields.get('Website', ''),
                    'specialties': fields.get('Specialties', ''),
                    'reviews': fields.get('Reviews', '')
                }
                
                # Only add garages with valid email addresses
                if garage['email'] and '@' in garage['email']:
                    garages.append(garage)
                    self.logger.info(f"Loaded garage: {garage['name']} - {garage['email']}")
            
            self.logger.info(f"Successfully loaded {len(garages)} garages from Airtable")
            return garages
            
        except Exception as e:
            self.logger.error(f"Error fetching garages from Airtable: {str(e)}")
            # Return empty list if error
            return []
    
    def get_fix_it_garages(self) -> List[Dict[str, Any]]:
        """
        Fetch all garages from Airtable 'Fix it' table for quote requests
        
        Returns:
            List of garage dictionaries with name, email, and address
        """
        try:
            self.logger.info("🔍 Attempting to access 'Fix it' table in Airtable...")
            table = self._get_table('Fix it')
            self.logger.info("✅ Successfully accessed 'Fix it' table")
            
            records = table.all()
            self.logger.info(f"📊 Found {len(records)} total records in 'Fix it' table")
            
            garages = []
            for record in records:
                fields = record.get('fields', {})
                
                # Extract garage information - using correct field names from Airtable
                garage = {
                    'id': record.get('id'),
                    'name': fields.get('Name', ''),
                    'email': fields.get('Email', ''),
                    'address': fields.get('Address', ''),
                    'phone_number': fields.get('Phone', ''),
                    'website': fields.get('Website', ''),
                    'reviews': fields.get('Reviews', ''),
                    'specialties': fields.get('Specialties', '')
                }
                
                # Only add garages with valid email addresses
                if garage['email'] and '@' in garage['email']:
                    garages.append(garage)
                    self.logger.info(f"✅ Loaded garage: {garage['name']} ({garage['email']})")
                else:
                    self.logger.warning(f"⚠️ Skipping garage '{garage['name']}' - missing or invalid email: '{garage['email']}'")
            
            self.logger.info(f"📧 Total valid garages with emails: {len(garages)}/{len(records)}")
            return garages
            
        except Exception as e:
            self.logger.error(f"❌ ERROR fetching Fix it garages from Airtable: {str(e)}", exc_info=True)
            self.logger.error(f"❌ Make sure:")
            self.logger.error("   1. Table 'Fix it' exists in Airtable")
            self.logger.error("   2. AIRTABLE_API_KEY is correct")
            self.logger.error("   3. AIRTABLE_BASE_ID is correct")
            # Return empty list if error
            return []
    
    def store_received_email(self, email_data: Dict[str, Any], vin: str = None) -> Dict[str, Any]:
        """
        Store a received email in the 'Recevied email' table
        
        Args:
            email_data: Dictionary containing email data with keys:
                - from_email: Sender's email address (maps to a field with the sender's email as the name)
                - subject: Email subject (stored in the field named after the sender's email)
                - body: Email body content (stored in the field named after the sender's email)
                - received_at: When the email was received (defaults to now, stored in the field named after the sender's email)
                - attachments: List of attachment filenames (stored in the field named after the sender's email)
            vin: Vehicle Identification Number (stored in the 'VIN' field)
            
        Returns:
            Dict: Created record data or existing record data if duplicate found
        """
        try:
            # Get the sender's email to determine the field name
            sender_email = email_data.get('from_email', '').strip().lower()
            
            if not sender_email:
                raise ValueError("No sender email provided in email_data")
                
            # Check for existing email from this sender for this VIN (prevent duplicates)
            existing_records = self.get_records(
                'Recevied email',
                formula=f'AND({{VIN}} = "{vin or ""}", {{Email}} = "{sender_email}")'
            )
            
            if existing_records:
                # Return the existing record instead of creating a duplicate
                self.logger.info(f"Duplicate email detected for VIN {vin} from {sender_email}, returning existing record")
                return existing_records[0]
            
            # Create a single text field with all email information
            email_content = f"""
            From: {email_data.get('from_email', '')}
            Subject: {email_data.get('subject', 'No Subject')}
            Date: {email_data.get('received_at', datetime.utcnow().isoformat())}
            
            {email_data.get('body', '')}
            
            Attachments: {', '.join(email_data.get('attachments', [])) if email_data.get('attachments') else 'None'}
            """
            
            # Prepare the data for Airtable - all fields that exist in "Recevied email" table
            record_data = {
                'VIN': vin or '',
                'Email': sender_email,
                'Subject': email_data.get('subject', 'No Subject'),
                'Body': email_data.get('body', ''),
                'Received At': email_data.get('received_at', datetime.utcnow().isoformat())
            }
            
            # Note: Attachment field in Airtable requires URLs in format [{'url': '...'}]
            # Since email attachments are inline (not URLs), we'll add filenames to the Body instead
            # If you want to store actual attachments, upload them to Cloudinary first
            if email_data.get('attachments') and len(email_data.get('attachments', [])) > 0:
                attachment_list = ', '.join(email_data.get('attachments', []))
                record_data['Body'] += f"\n\n📎 Attachments: {attachment_list}"
            
            # Add Quote field if provided (for storing quote amount/details)
            if 'quote' in email_data and email_data['quote']:
                record_data['Quote'] = email_data['quote']
            # Store in the 'Recevied email' table (note the typo in the table name)
            return self.create_record('Recevied email', record_data)
            
        except Exception as e:
            self.logger.error(f"Error storing received email: {str(e)}")
            raise
    
    def create_record(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record in the specified table
        
        Args:
            table_name: Name of the table
            data: Dictionary of field names and values
            
        Returns:
            Dict: Created record data
        """
        try:
            table = self._get_table(table_name)
            record = table.create(data)
            return record
        except Exception as e:
            self.logger.error(f"Error creating record in {table_name}: {str(e)}")
            raise
    
    def get_record(self, table_name: str, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a record by ID from the specified table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to retrieve
            
        Returns:
            Optional[Dict]: Record data if found, None otherwise
        """
        try:
            table = self._get_table(table_name)
            return table.get(record_id)
        except Exception as e:
            self.logger.error(f"Error getting record {record_id} from {table_name}: {str(e)}")
            return None
    
    def get_records(self, table_name: str, formula: str = "", **kwargs) -> List[Dict[str, Any]]:
        """
        Get multiple records from the specified table
        
        Args:
            table_name: Name of the table
            formula: Airtable formula for filtering
            **kwargs: Additional parameters for the query (e.g., sort, fields)
            
        Returns:
            List[Dict]: List of matching records
        """
        try:
            table = self._get_table(table_name)
            if formula:
                self.logger.debug(f"Applying formula filter: {formula}")
                kwargs['formula'] = formula
            return table.all(**kwargs)
        except Exception as e:
            self.logger.error(f"Error getting records from {table_name} with formula '{formula}': {str(e)}", exc_info=True)
            return []
    
    def update_record(self, table_name: str, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a record in the specified table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to update
            data: Dictionary of fields to update
            
        Returns:
            Optional[Dict]: Updated record data if successful, None otherwise
        """
        try:
            table = self._get_table(table_name)
            return table.update(record_id, data)
        except Exception as e:
            self.logger.error(f"Error updating record {record_id} in {table_name}: {str(e)}")
            return None
    
    def delete_record(self, table_name: str, record_id: str) -> bool:
        """
        Delete a record from the specified table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            table = self._get_table(table_name)
            table.delete(record_id)
            return True
        except Exception as e:
            self.logger.error(f"Error deleting record {record_id} from {table_name}: {str(e)}")
            return False
    
    def _upload_file_to_cloudinary(self, file_content, filename):
        """
        Upload a file to Cloudinary and return the URL
        
        Args:
            file_content: File content as bytes or file-like object
            filename: Original filename
            
        Returns:
            str: URL of the uploaded file, or None if upload failed
        """
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
            
            self.logger.info(f"Starting Cloudinary upload for file: {filename}")
            
            # Verify Cloudinary credentials
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
            api_key = os.getenv('CLOUDINARY_API_KEY')
            api_secret = os.getenv('CLOUDINARY_API_SECRET')
            
            self.logger.debug(f"Cloudinary Config - Cloud Name: {'*' * 5}{cloud_name[-3:] if cloud_name else 'None'}")
            self.logger.debug(f"Cloudinary Config - API Key: {'*' * 5}{api_key[-3:] if api_key else 'None'}")
            self.logger.debug(f"Cloudinary Config - API Secret: {'*' * 5}{'*' * 5 if api_secret else 'None'}")
            
            if not all([cloud_name, api_key, api_secret]):
                error_msg = "Missing Cloudinary configuration. Please check environment variables."
                self.logger.error(error_msg)
                return None
                
            self.logger.info("Cloudinary credentials verified")
                
            # Configure Cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            
            # Ensure file_content is in the correct format
            if hasattr(file_content, 'read'):
                # If it's a file-like object, read its content
                file_content = file_content.read()
            
            if not file_content:
                self.logger.error("No file content provided")
                return None
                
            import hashlib
            import time
            
            timestamp = str(int(time.time()))
            file_hash = hashlib.md5(file_content if isinstance(file_content, bytes) else file_content.encode()).hexdigest()
            
            # Clean the filename to remove any special characters
            import re
            clean_filename = re.sub(r'[^\w\d-]', '_', os.path.splitext(filename)[0])
            clean_extension = os.path.splitext(filename)[1].lower()
            public_id = f"garagefy/{clean_filename}_{timestamp}_{file_hash[:8]}{clean_extension}"
            
            self.logger.info(f"Preparing to upload file to Cloudinary. Size: {len(file_content)} bytes, Public ID: {public_id}")
            
            # Upload to Cloudinary with explicit resource type
            resource_type = "auto"
            if isinstance(filename, str):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    resource_type = "image"
                elif filename.lower().endswith(('.mp4', '.webm', '.mov')):
                    resource_type = "video"
                elif filename.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
                    resource_type = "raw"
            
            try:
                result = cloudinary.uploader.upload(
                    file_content,
                    public_id=public_id,
                    folder="garagefy",
                    resource_type=resource_type,
                    overwrite=True,
                    unique_filename=True,
                    use_filename=True,
                    filename_override=os.path.basename(filename),
                    timeout=30  # 30 second timeout
                )
                
                self.logger.debug(f"Cloudinary upload response: {json.dumps(result, default=str)}")
                
                if not result:
                    self.logger.error("Cloudinary upload returned no result")
                    return None
                    
                if 'secure_url' not in result:
                    self.logger.error(f"Cloudinary upload failed. Response: {result}")
                    return None
                    
                self.logger.info(f"Successfully uploaded to Cloudinary: {result['secure_url']}")
                return result['secure_url']
                
            except cloudinary.api.Error as e:
                self.logger.error(f"Cloudinary API error: {str(e)}", exc_info=True)
                return None
            except Exception as e:
                self.logger.exception(f"Unexpected error during Cloudinary upload: {str(e)}")
                return None
            
        except Exception as e:
            self.logger.exception(f"Unexpected error in _upload_file_to_cloudinary: {str(e)}")
            return None
    
    def store_garage_quote(self, customer_email: str, garage_email: str, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store a garage quote in the Customer details table using garage email as field name
        
        Args:
            customer_email: Email of the customer to update
            garage_email: Email of the garage providing the quote (will be used as field name)
            quote_data: Dictionary containing quote details with keys:
                - amount: The quoted amount
                - notes: Additional notes from the garage (optional)
                - valid_until: Quote validity date (optional)
                - status: Quote status (e.g., 'pending', 'accepted', 'rejected')
                
        Returns:
            Dict: {
                'success': bool,
                'record': Dict or None,
                'error': str or None
            }
        """
        try:
            # First, find the customer record by email
            table = self._get_table('Customer details')
            records = table.all(formula=f"LOWER(Email) = '{customer_email.lower()}'")
            
            if not records:
                return {
                    'success': False,
                    'record': None,
                    'error': f'No customer found with email: {customer_email}'
                }
                
            customer_record = records[0]
            record_id = customer_record['id']
            
            # Prepare the update data with garage email as field name
            update_data = {
                garage_email: f"Quote: {quote_data.get('amount', 'N/A')} - {quote_data.get('status', 'pending')}"
            }
            
            # Add optional fields if they exist
            if 'notes' in quote_data:
                update_data[f"{garage_email} Notes"] = quote_data['notes']
            if 'valid_until' in quote_data:
                update_data[f"{garage_email} Valid Until"] = quote_data['valid_until']
            if 'status' in quote_data:
                update_data[f"{garage_email} Status"] = quote_data['status']
            
            # Update the customer record
            updated_record = table.update(record_id, update_data)
            
            self.logger.info(f"Stored quote from {garage_email} for customer {customer_email}")
            
            return {
                'success': True,
                'record': updated_record,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Error storing garage quote: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'record': None,
                'error': error_msg
            }
            
    def create_customer(self, data: dict):
        """
        Create a new customer record in the Customer details table
        
        Args:
            data (dict): Dictionary containing customer data
                - Name (str): Customer name
                - Email (str): Customer email
                - phone (str, optional): Customer phone number
                - VIN (str, optional): Vehicle identification number
                - car_brand (str, optional): Car brand
                - Plate Number (str, optional): License plate number
                - Note (str, optional): Additional notes
                - Image (str or list, optional): URL(s) to customer's image(s)
                
        Returns:
            dict: {
                'success': bool,
                'record_id': str or None,
                'error': str or None
            }
        """
        try:
            # Get the Customer details table using the table name
            table = self._get_table('Customer details')
            self.logger.info(f"Attempting to create customer record with data: {data}")
            
            # Validate required fields
            if not data.get('Name') or not data.get('Email'):
                error_msg = "Name and Email are required fields"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg, 'record_id': None}
            
            # Get current date and time in ISO format
            from datetime import datetime, timezone
            current_datetime = datetime.now(timezone.utc).isoformat()
            
            # Prepare the record data - start with only required fields
            record_data = {
                'Name': data.get('Name', '').strip(),
                'Email': data.get('Email', '').strip(),
            }
            
            # Add optional fields only if they have values
            # This prevents errors when fields don't exist in Airtable
            notes = data.get('Note', '').strip() or data.get('Notes', '').strip()
            if notes:
                record_data['Notes'] = notes
            
            vin = data.get('VIN', '').strip()
            if vin:
                record_data['VIN'] = vin
                
            if 'phone' in data and data['phone']:
                record_data['Phone'] = data['phone'].strip()
            
            if 'car_brand' in data and data['car_brand']:
                record_data['Brand'] = data['car_brand'].strip()
            
            # Add license plate number if present
            plate_number = data.get('Plate Number', '').strip()
            if plate_number:
                record_data['Plate Number'] = plate_number
            
            # Add timestamp - try different field name variants
            record_data['Date and Time'] = current_datetime
                
            if 'Image' in data and data['Image']:
                # Handle both single URL string and list of URLs
                if isinstance(data['Image'], list):
                    # Ensure each item in the list is a dict with 'url' key
                    record_data['Image'] = [{'url': img['url']} if isinstance(img, dict) else {'url': str(img)} for img in data['Image']]
                else:
                    record_data['Image'] = [{'url': str(data['Image'])}]
                
                self.logger.info(f"Added {len(record_data['Image'])} image(s) to record data")
                
            self.logger.info(f"Prepared record data: {record_data}")
            
            # Create the record
            self.logger.info(f"Creating record with data: {record_data}")
            try:
                record = table.create(record_data)
            except Exception as create_error:
                error_str = str(create_error)
                if 'UNKNOWN_FIELD_NAME' in error_str:
                    # Extract the field name from the error message
                    import re
                    field_match = re.search(r'Unknown field name: "([^"]+)"', error_str)
                    missing_field = field_match.group(1) if field_match else "unknown"
                    error_msg = f"Airtable field '{missing_field}' does not exist in your base. Please add this field to the 'Customer details' table in Airtable."
                    self.logger.error(f"{error_msg} | Required fields: Name, Email, VIN, Phone, Brand, Notes, Date and Time, Response Sent")
                    return {'success': False, 'error': error_msg, 'record_id': None}
                raise  # Re-raise if it's a different error
            
            if not record or 'id' not in record:
                error_msg = "Failed to create record: Invalid response from Airtable"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg, 'record_id': None}
                
            self.logger.info(f"Successfully created customer record: {record['id']}")
            return {
                'success': True,
                'record_id': record['id'],
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Error creating customer record: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'record_id': None,
                'error': error_msg
            }

# Singleton instance
airtable_service = AirtableService()
