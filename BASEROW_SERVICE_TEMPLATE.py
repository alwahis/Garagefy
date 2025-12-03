# Template for baserow_service.py
# This is a starting point - adapt to your needs

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
        
        # Table ID mappings - get these from Baserow UI
        self.table_ids = {
            'Customer details': int(os.getenv('BASEROW_TABLE_CUSTOMER_DETAILS', 0)),
            'Fix it': int(os.getenv('BASEROW_TABLE_FIX_IT', 0)),
            'Recevied email': int(os.getenv('BASEROW_TABLE_RECEIVED_EMAIL', 0)),
            'Received': int(os.getenv('BASEROW_TABLE_RECEIVED', 0))
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
                    garage = {
                        'id': record.get('id'),
                        'name': record.get('Name', ''),
                        'email': record.get('Email', ''),
                        'address': record.get('Address', ''),
                        'phone': record.get('Phone', ''),
                        'website': record.get('Website', ''),
                        'specialties': record.get('Specialties', ''),
                        'reviews': record.get('Reviews', '')
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
            
            # Validate required fields
            if not data.get('Name') or not data.get('Email'):
                error_msg = "Name and Email are required"
                self.logger.error(error_msg)
                return {'success': False, 'error': error_msg, 'record_id': None}
            
            # Prepare payload
            payload = {
                'Name': data.get('Name', '').strip(),
                'Email': data.get('Email', '').strip(),
            }
            
            # Add optional fields
            if data.get('VIN'):
                payload['VIN'] = data['VIN'].strip()
            if data.get('Phone'):
                payload['Phone'] = data['Phone'].strip()
            if data.get('Brand'):
                payload['Brand'] = data['Brand'].strip()
            if data.get('Plate Number'):
                payload['Plate Number'] = data['Plate Number'].strip()
            if data.get('Notes'):
                payload['Notes'] = data['Notes'].strip()
            
            # Add timestamp
            payload['Date and Time'] = datetime.now(timezone.utc).isoformat()
            
            # Handle images (if provided as list of URLs)
            if data.get('Image'):
                if isinstance(data['Image'], list):
                    payload['Image'] = data['Image']
                else:
                    payload['Image'] = [data['Image']]
            
            self.logger.info(f"Creating customer record for {data.get('Email')}")
            
            endpoint = f'/api/database/rows/table/{table_id}/'
            response = self._make_request('POST', endpoint, data=payload)
            
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
    
    def get_records(self, table_name: str, filter_dict: Dict = None) -> List[Dict[str, Any]]:
        """
        Get records from a table with optional filtering
        
        Args:
            table_name: Name of the table (e.g., 'Customer details')
            filter_dict: Optional filter (e.g., {'field': 'Email', 'value': 'test@example.com'})
            
        Returns:
            List of records
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")
            
            records = []
            page = 1
            
            while True:
                endpoint = f'/api/database/rows/table/{table_id}/'
                params = {'page': page, 'size': 100}
                
                # Add filter if provided
                if filter_dict:
                    # Example: filter_dict = {'field': 'Email', 'value': 'test@example.com', 'type': 'equal'}
                    # This needs to be converted to Baserow filter format
                    # For now, we'll do client-side filtering
                    pass
                
                response = self._make_request('GET', endpoint, params=params)
                
                for record in response.get('results', []):
                    # Client-side filtering if needed
                    if filter_dict:
                        field = filter_dict.get('field')
                        value = filter_dict.get('value')
                        if record.get(field) != value:
                            continue
                    
                    records.append(record)
                
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
            return response
            
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
        Record a garage response in the 'Received' table
        
        Args:
            response_data: Dictionary with garage_name, garage_email, request_id, etc.
            
        Returns:
            Dict with success status
        """
        try:
            table_id = self.table_ids['Received']
            
            payload = {
                'Garage Name': response_data.get('garage_name', ''),
                'Email': response_data.get('garage_email', ''),
                'Request ID': response_data.get('request_id'),
                'Quote Amount': response_data.get('quote_amount'),
                'Notes': response_data.get('notes', ''),
                'Status': response_data.get('status', 'received'),
                'Response Date': response_data.get('response_date', datetime.now(timezone.utc).isoformat())
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
        """
        Get a single record by ID
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            
        Returns:
            Record data or None if not found
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")
            
            endpoint = f'/api/database/rows/table/{table_id}/{record_id}/'
            response = self._make_request('GET', endpoint)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting record: {str(e)}")
            return None
    
    def create_record(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record in a table
        
        Args:
            table_name: Name of the table
            data: Dictionary of field values
            
        Returns:
            Created record data
        """
        try:
            table_id = self.table_ids.get(table_name)
            if not table_id:
                raise ValueError(f"Unknown table: {table_name}")
            
            endpoint = f'/api/database/rows/table/{table_id}/'
            response = self._make_request('POST', endpoint, data=data)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error creating record: {str(e)}")
            raise


# Singleton instance
baserow_service = BaserowService()
