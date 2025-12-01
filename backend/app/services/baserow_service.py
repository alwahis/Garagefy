import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from dotenv import load_dotenv
import json

load_dotenv()

class BaserowService:
    """Service for interacting with Baserow database"""
    
    def __init__(self):
        self.base_url = os.getenv('BASEROW_URL', 'https://api.baserow.io')
        self.api_token = os.getenv('BASEROW_API_TOKEN')
        self.database_id = os.getenv('BASEROW_DATABASE_ID')
        
        if not self.api_token:
            raise ValueError("Missing BASEROW_API_TOKEN in .env")
        if not self.database_id:
            raise ValueError("Missing BASEROW_DATABASE_ID in .env")
        
        self.headers = {
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        # Table ID mappings
        self.table_ids = {
            'Customer details': int(os.getenv('BASEROW_TABLE_CUSTOMER_DETAILS', 0)),
            'Fix it': int(os.getenv('BASEROW_TABLE_FIX_IT', 0)),
            'Recevied email': int(os.getenv('BASEROW_TABLE_RECEIVED_EMAIL', 0)),
            'Received': int(os.getenv('BASEROW_TABLE_RECEIVED_EMAIL', 0)),  # Use Recevied email for both
            # Quotes subsystem
            'Quotes': int(os.getenv('BASEROW_TABLE_QUOTES', 0)),
            'Service Requests': int(os.getenv('BASEROW_TABLE_SERVICE_REQUESTS', 0)),
        }
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing Baserow service for database {self.database_id}")
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Make HTTP request to Baserow API"""
        url = f'{self.base_url}{endpoint}'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data, params=params, timeout=30)
            elif method == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if response.status_code >= 400:
                error_msg = response.text
                try:
                    error_msg = response.json().get('error', error_msg)
                except:
                    pass
                self.logger.error(f"API Error ({response.status_code}): {error_msg}")
                raise Exception(f"Baserow API error: {error_msg}")
            
            return response.json() if response.text else {}
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout: {url}")
            raise
        except Exception as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
    
    def get_fix_it_garages(self) -> List[Dict[str, Any]]:
        """
        Fetch all garages from 'Fix it' table
        
        Returns:
            List of garage dictionaries with name, email, address, etc.
        """
        try:
            table_id = self.table_ids['Fix it']
            self.logger.info(f"🔍 Fetching garages from Fix it table (ID: {table_id})")
            
            garages = []
            page = 1
            
            while True:
                endpoint = f'/api/database/rows/table/{table_id}/'
                params = {'page': page, 'size': 100}
                
                response = self._make_request('GET', endpoint, params=params)
                
                for record in response.get('results', []):
                    # Baserow returns fields by ID, try both field names and field IDs
                    # Field mapping for Fix it table:
                    # field_6389820 = Name
                    # field_6389821 = Address
                    # field_6389822 = Phone
                    # field_6389823 = Email
                    # field_6389824 = Website
                    # field_6389825 = Reviews
                    # field_6389826 = Specialties
                    
                    name = record.get('Name') or record.get('field_6389820', '')
                    email = record.get('Email') or record.get('field_6389823', '')
                    address = record.get('Address') or record.get('field_6389821', '')
                    phone_value = record.get('Phone') or record.get('field_6389822', '')
                    website = record.get('Website') or record.get('field_6389824', '')
                    reviews = record.get('Reviews') or record.get('field_6389825', '')
                    specialties = record.get('Specialties') or record.get('field_6389826', '')
                    
                    garage = {
                        'id': record.get('id'),
                        'name': name,
                        'email': email,
                        'address': address,
                        # Expose both 'phone' and 'phone_number' for compatibility
                        'phone': phone_value,
                        'phone_number': phone_value,
                        'website': website,
                        'specialties': specialties,
                        'reviews': reviews
                    }
                    
                    # Only add garages with valid email
                    if garage['email'] and '@' in garage['email']:
                        garages.append(garage)
                        self.logger.info(f"✅ Loaded garage: {garage['name']} ({garage['email']})")
                    else:
                        self.logger.warning(f"⚠️ Skipping garage '{garage['name']}' - invalid email")
                
                # Check if there are more pages
                if not response.get('next'):
                    break
                page += 1
            
            self.logger.info(f"📧 Total valid garages: {len(garages)}")
            return garages
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching garages: {str(e)}", exc_info=True)
            return []
    
    def create_customer(self, data: dict) -> Dict[str, Any]:
        """
        Create a new customer record in 'Customer details' table
        
        Args:
            data: Dictionary with keys like Name, Email, VIN, Phone, etc.
            
        Returns:
            Dict with success status and record_id
        """
        try:
            table_id = self.table_ids['Customer details']
            self.logger.info(f"🔍 DEBUG: Customer details table ID: {table_id}")
            self.logger.info(f"🔍 DEBUG: All table IDs: {self.table_ids}")
            
            # Validate table ID
            if not table_id or table_id == 0:
                error_msg = f"Invalid Customer details table ID: {table_id}. Check BASEROW_TABLE_CUSTOMER_DETAILS env var"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg, 'record_id': None}
            
            # Validate required fields
            if not data.get('Name') or not data.get('Email'):
                error_msg = "Name and Email are required"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg, 'record_id': None}
            
            # Prepare payload with field IDs for Customer details table
            # Customer details table field mappings:
            # field_6389828 = Name
            # field_6389829 = Phone
            # field_6389830 = Email
            # field_6389831 = VIN
            # field_6389832 = Notes
            # field_6389833 = Brand
            # field_6389834 = Date and Time
            # field_6389835 = Image
            # field_6389836 = Sent Emails
            # field_6389837 = Plate Number
            
            payload = {}
            
            # Name (required) - field_6389828
            name_value = (data.get('Name') or '').strip()
            if name_value:
                payload['field_6389828'] = name_value
            
            # Email (required) - field_6389830
            email_value = (data.get('Email') or '').strip()
            if email_value:
                payload['field_6389830'] = email_value

            # VIN - field_6389831
            vin_value = data.get('VIN')
            if vin_value:
                payload['field_6389831'] = str(vin_value).strip()

            # Phone - field_6389829
            phone_value = data.get('Phone') or data.get('phone') or data.get('phone_number')
            if phone_value:
                payload['field_6389829'] = str(phone_value).strip()

            # Brand - field_6389833
            brand_value = data.get('Brand') or data.get('car_brand') or data.get('carBrand')
            if brand_value:
                payload['field_6389833'] = str(brand_value).strip()

            # Plate Number - field_6389837
            plate_value = data.get('Plate Number') or data.get('License Plate') or data.get('license_plate')
            if plate_value:
                payload['field_6389837'] = str(plate_value).strip()

            # Notes - field_6389832
            notes_value = data.get('Notes') or data.get('Note') or data.get('notes')
            if notes_value:
                payload['field_6389832'] = str(notes_value).strip()
            
            # Date and Time - field_6389834
            payload['field_6389834'] = datetime.now(timezone.utc).isoformat()
            
            # Handle images - field_6389835
            if data.get('Image'):
                if isinstance(data['Image'], list):
                    payload['field_6389835'] = data['Image']
                else:
                    payload['field_6389835'] = [data['Image']]
            
            self.logger.info(f"Creating customer record for {data.get('Email')}")
            self.logger.info(f"🔍 DEBUG: Payload being sent: {json.dumps(payload, indent=2)}")
            self.logger.info(f"🔍 DEBUG: Payload keys: {list(payload.keys())}")
            
            endpoint = f'/api/database/rows/table/{table_id}/'
            self.logger.info(f"🔍 DEBUG: Endpoint: {endpoint}")
            self.logger.info(f"🔍 DEBUG: API Token present: {bool(self.api_token)}")
            response = self._make_request('POST', endpoint, data=payload)
            self.logger.info(f"🔍 DEBUG: Response: {json.dumps(response, indent=2)}")
            self.logger.info(f"🔍 DEBUG: Response keys: {list(response.keys()) if response else 'None'}")
            
            record_id = response.get('id')
            self.logger.info(f"✅ Created customer record: {record_id}")
            
            return {
                'success': True,
                'record_id': record_id,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Error creating customer: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'record_id': None,
                'error': error_msg
            }
    
    def get_records(self, table_name: str, formula: str = "", filter_dict: Dict = None) -> List[Dict[str, Any]]:
        """Get records from a table with optional filtering.

        This helper emulates the Airtable SDK shape by returning each row as a
        dict with an ``id`` and a nested ``fields`` mapping so existing code
        that does ``record.get('fields', {})`` continues to work unchanged.

        Supported filtering:
        - No formula: returns all rows (optionally filtered by ``filter_dict``)
        - Simple equality: ``{VIN} = "ABC123"`` or ``{VIN} = 'ABC123'``
        - AND of equalities: ``AND({Email}="x", {Subject}="y")``

        Args:
            table_name: Logical table name (e.g. ``'Customer details'``).
            formula: Simple Airtable-style formula used in existing code.
            filter_dict: Optional simple equality filter of the form::

                {'field': 'VIN', 'value': 'ABC123'}

        Returns:
            List of Airtable-style records: ``{'id': ..., 'fields': {...}}``.
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")

            import re

            def _strip_quotes(value: str) -> str:
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    return value[1:-1]
                return value

            def _match_simple(expr: str, row: Dict[str, Any]) -> bool:
                """Match a simple equality expression against a row.

                Supports patterns like ``{VIN} = "ABC123"``.
                If parsing fails, returns True (non-filtering) to avoid
                accidentally dropping data.
                """
                expr = expr.strip()
                m = re.match(r"^\{\s*([^}]+)\s*\}\s*=\s*(.+)$", expr)
                if not m:
                    return True
                field_name = m.group(1).strip()
                raw_val = _strip_quotes(m.group(2).strip())
                actual = row.get(field_name)
                return str(actual).strip() == raw_val

            def _formula_matches(row: Dict[str, Any]) -> bool:
                if not formula:
                    return True
                expr = formula.strip()
                # Handle AND(condition1, condition2, ...)
                if expr.upper().startswith("AND(") and expr.endswith(")"):
                    inner = expr[4:-1]
                    parts = [p for p in inner.split(',') if p.strip()]
                    for part in parts:
                        if not _match_simple(part, row):
                            return False
                    return True
                # Fallback: single simple condition
                return _match_simple(expr, row)

            records: List[Dict[str, Any]] = []
            page = 1

            while True:
                endpoint = f'/api/database/rows/table/{table_id}/'
                params = {'page': page, 'size': 100}

                response = self._make_request('GET', endpoint, params=params)

                for raw in response.get('results', []):
                    # Apply formula-based filtering first
                    if not _formula_matches(raw):
                        continue

                    # Optional simple client-side filter on a single field
                    if filter_dict:
                        field = filter_dict.get('field')
                        value = filter_dict.get('value')
                        if field and raw.get(field) != value:
                            continue

                    wrapped = {
                        'id': raw.get('id'),
                        'fields': raw,
                    }
                    records.append(wrapped)

                if not response.get('next'):
                    break
                page += 1

            return records

        except Exception as e:
            self.logger.error(f"Error getting records from {table_name}: {str(e)}")
            return []
    
    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a record in a table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to update
            data: Dictionary of fields to update
            
        Returns:
            Updated record or None if failed
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")
            
            endpoint = f'/api/database/rows/table/{table_id}/{record_id}/'
            response = self._make_request('PATCH', endpoint, data=data)

            self.logger.info(f"✅ Updated record {record_id} in {table_name}")

            # Preserve Airtable-style shape for callers expecting 'fields'
            if response:
                return {
                    'id': response.get('id'),
                    'fields': response,
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Error updating record: {str(e)}")
            return None
    
    def delete_record(self, table_name: str, record_id: int) -> bool:
        """
        Delete a record from a table
        
        Args:
            table_name: Name of the table
            record_id: ID of the record to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")
            
            endpoint = f'/api/database/rows/table/{table_id}/{record_id}/'
            self._make_request('DELETE', endpoint)
            
            self.logger.info(f"✅ Deleted record {record_id} from {table_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting record: {str(e)}")
            return False
    
    def store_received_email(self, email_data: Dict[str, Any], vin: str = None) -> Dict[str, Any]:
        """
        Store a received email in the 'Recevied email' table
        
        Args:
            email_data: Dictionary with from_email, subject, body, received_at, attachments
            vin: Vehicle Identification Number
            
        Returns:
            Dict with success status and record data
        """
        try:
            table_id = self.table_ids['Recevied email']
            
            # Check for duplicates
            existing = self.get_records(
                'Recevied email',
                filter_dict={'field': 'VIN', 'value': vin}
            )
            
            if existing:
                self.logger.info(f"Duplicate email detected for VIN {vin}")
                return existing[0]
            
            # Prepare payload
            payload = {
                'VIN': vin or '',
                'Email': email_data.get('from_email', '').strip().lower(),
                'Subject': email_data.get('subject', 'No Subject'),
                'Body': email_data.get('body', ''),
                'Received At': email_data.get('received_at', datetime.now(timezone.utc).isoformat())
            }
            
            if email_data.get('quote'):
                payload['Quote'] = email_data['quote']
            
            endpoint = f'/api/database/rows/table/{table_id}/'
            response = self._make_request('POST', endpoint, data=payload)
            
            self.logger.info(f"✅ Stored email from {payload['Email']} for VIN {vin}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error storing email: {str(e)}", exc_info=True)
            raise
    
    def record_garage_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record a garage response in the 'Recevied email' table
        
        Args:
            response_data: Dictionary with garage_name, garage_email, request_id, etc.
            
        Returns:
            Dict with success status
        """
        try:
            table_id = self.table_ids['Recevied email']
            
            payload = {
                'Email': response_data.get('garage_email', ''),
                'Subject': f"Response from {response_data.get('garage_name', '')}",
                'Body': response_data.get('notes', ''),
                'Received At': response_data.get('response_date', datetime.now(timezone.utc).isoformat())
            }
            
            # Remove None values
            payload = {k: v for k, v in payload.items() if v is not None}
            
            endpoint = f'/api/database/rows/table/{table_id}/'
            response = self._make_request('POST', endpoint, data=payload)
            
            self.logger.info(f"✅ Recorded response from {response_data.get('garage_name')}")
            
            return {
                'success': True,
                'record': response,
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
    
    def get_record(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a single record by ID.

        Returns an Airtable-style dict with ``id`` and ``fields`` keys so code
        written against the original Airtable service keeps working.
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")

            endpoint = f'/api/database/rows/table/{table_id}/{record_id}/'
            response = self._make_request('GET', endpoint)

            if not response:
                return None

            return {
                'id': response.get('id'),
                'fields': response,
            }

        except Exception as e:
            self.logger.error(f"Error getting record: {str(e)}")
            return None
    
    def create_record(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in a table.

        Returns an Airtable-style dict with ``id`` and ``fields`` keys so
        callers like ``quote_service`` can keep using ``record['fields']``.
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")

            endpoint = f'/api/database/rows/table/{table_id}/'
            response = self._make_request('POST', endpoint, data=data)

            return {
                'id': response.get('id') if response else None,
                'fields': response,
            }

        except Exception as e:
            self.logger.error(f"Error creating record: {str(e)}")
            raise
    
    def get_all_garages(self) -> List[Dict[str, Any]]:
        """Alias for get_fix_it_garages for compatibility"""
        return self.get_fix_it_garages()
    
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
            import hashlib
            import time
            import re
            
            self.logger.info(f"Starting Cloudinary upload for file: {filename}")
            
            # Verify Cloudinary credentials
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
            api_key = os.getenv('CLOUDINARY_API_KEY')
            api_secret = os.getenv('CLOUDINARY_API_SECRET')
            
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
            
            timestamp = str(int(time.time()))
            file_hash = hashlib.md5(file_content if isinstance(file_content, bytes) else file_content.encode()).hexdigest()
            
            # Clean the filename to remove any special characters
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


# Singleton instance
baserow_service = BaserowService()
