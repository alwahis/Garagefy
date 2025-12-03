import os
import imaplib
import email
from email.header import decode_header
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import base64
import msal
from .baserow_service import baserow_service as airtable_service

logger = logging.getLogger(__name__)

class EmailMonitorService:
    """Service for monitoring incoming emails and processing garage responses"""
    
    def __init__(self):
        self.email_address = os.getenv('EMAIL_ADDRESS', 'info@garagefy.app')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.imap_server = os.getenv('IMAP_SERVER', 'outlook.office365.com')
        self.imap_port = int(os.getenv('IMAP_PORT', '993'))
        self.client_id = os.getenv('MS_CLIENT_ID')
        self.client_secret = os.getenv('MS_CLIENT_SECRET')
        self.tenant_id = os.getenv('MS_TENANT_ID')
        self.airtable = airtable_service
    
    def _get_oauth2_token(self) -> Optional[str]:
        """Get OAuth2 access token for IMAP"""
        try:
            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=authority,
                client_credential=self.client_secret
            )
            
            # Request token for IMAP/SMTP
            scopes = ["https://outlook.office365.com/.default"]
            result = app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" in result:
                return result["access_token"]
            else:
                logger.error(f"Failed to acquire token: {result.get('error_description', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting OAuth2 token: {str(e)}", exc_info=True)
            return None
    
    def _generate_oauth2_string(self, user: str, access_token: str) -> str:
        """Generate OAuth2 authentication string for IMAP"""
        return f"user={user}\x01auth=Bearer {access_token}\x01\x01"
        
    def _connect_to_inbox(self) -> Optional[imaplib.IMAP4_SSL]:
        """Connect to the email inbox using IMAP with OAuth2"""
        try:
            logger.info(f"Connecting to {self.imap_server}:{self.imap_port}")
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            
            # Try OAuth2 first
            if self.client_id and self.client_secret and self.tenant_id:
                try:
                    logger.info("Attempting OAuth2 authentication")
                    access_token = self._get_oauth2_token()
                    
                    if access_token:
                        auth_string = self._generate_oauth2_string(self.email_address, access_token)
                        mail.authenticate('XOAUTH2', lambda x: auth_string.encode())
                        logger.info(f"Successfully connected to inbox using OAuth2: {self.email_address}")
                        return mail
                    else:
                        logger.warning("OAuth2 token acquisition failed, falling back to password")
                except Exception as oauth_error:
                    logger.warning(f"OAuth2 authentication failed: {str(oauth_error)}, falling back to password")
                    # Reconnect since the failed auth may have closed the connection
                    mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            
            # Fallback to password authentication if OAuth2 fails or is not configured
            if self.email_password and self.email_password != 'your_email_password_here':
                logger.info("Attempting password authentication")
                mail.login(self.email_address, self.email_password)
                logger.info(f"Successfully connected to inbox using password: {self.email_address}")
                return mail
            else:
                logger.error("No valid authentication method available (OAuth2 failed and no password)")
                return None
            
        except Exception as e:
            logger.error(f"Error connecting to inbox: {str(e)}", exc_info=True)
            return None
    
    def _decode_email_subject(self, subject: str) -> str:
        """Decode email subject handling encoding"""
        try:
            if subject is None:
                return "No Subject"
            
            decoded_parts = []
            for part, encoding in decode_header(subject):
                if isinstance(part, bytes):
                    decoded_parts.append(part.decode(encoding or 'utf-8', errors='ignore'))
                else:
                    decoded_parts.append(str(part))
            
            return ''.join(decoded_parts)
        except Exception as e:
            logger.error(f"Error decoding subject: {str(e)}")
            return str(subject)
    
    def _extract_email_body(self, msg: email.message.Message) -> str:
        """Extract the body text from an email message"""
        try:
            body = ""
            
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    # Skip attachments
                    if "attachment" in content_disposition:
                        continue
                    
                    # Get text/plain or text/html
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                        except:
                            pass
                    elif content_type == "text/html" and not body:
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except:
                            pass
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            return body
            
        except Exception as e:
            logger.error(f"Error extracting email body: {str(e)}", exc_info=True)
            return ""
    
    def _extract_attachments(self, msg: email.message.Message) -> List[Dict[str, Any]]:
        """Extract attachments from email message"""
        attachments = []
        
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            # Decode filename if needed
                            decoded_filename = self._decode_email_subject(filename)
                            
                            # Get file content
                            file_data = part.get_payload(decode=True)
                            
                            attachments.append({
                                'filename': decoded_filename,
                                'content': file_data,
                                'content_type': part.get_content_type()
                            })
                            
                            logger.info(f"Found attachment: {decoded_filename}")
            
        except Exception as e:
            logger.error(f"Error extracting attachments: {str(e)}", exc_info=True)
        
        return attachments
    
    async def _analyze_attachment_with_deepseek(self, attachment: Dict[str, Any]) -> Optional[str]:
        """Analyze attachment content using DeepSeek LLM"""
        try:
            filename = attachment.get('filename', 'unknown')
            content = attachment.get('content')
            content_type = attachment.get('content_type', '')
            
            logger.info(f"Analyzing attachment with DeepSeek: {filename}")
            
            # For now, handle text-based files and PDFs
            if 'text' in content_type or 'pdf' in content_type.lower():
                # Convert content to text if needed
                if isinstance(content, bytes):
                    try:
                        text_content = content.decode('utf-8', errors='ignore')
                    except:
                        text_content = str(content)
                else:
                    text_content = str(content)
                
                # Prepare prompt for DeepSeek
                prompt = f"""Analyser le contenu suivant extrait d'un fichier joint à un email de devis de garage.
                
Fichier: {filename}
Type: {content_type}

Contenu:
{text_content[:2000]}  # Limit to first 2000 chars

Extraire les informations suivantes si disponibles:
- Montant du devis
- Délai de réparation
- Pièces nécessaires
- Main d'œuvre
- Autres remarques importantes

Résumer en français de manière structurée."""
                
                # Simple text extraction (DeepSeek removed during cleanup)
                # Extract key information from email body
                analysis = {
                    "summary": body_text[:500] if body_text else "No content available",
                    "quote": "See email body for quote details",
                    "contact": "See email for contact information"
                }
                logger.info(f"Email analysis completed for {filename}")
                
                return analysis
            
            else:
                logger.info(f"Skipping DeepSeek analysis for non-text file: {filename}")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing attachment with DeepSeek: {str(e)}", exc_info=True)
            return None
    
    async def check_and_process_new_emails(self, mark_as_read: bool = False) -> Dict[str, Any]:
        """
        Check inbox for new emails and process garage responses
        
        Args:
            mark_as_read: Whether to mark processed emails as read
            
        Returns:
            Dict with processing results
        """
        try:
            mail = self._connect_to_inbox()
            if not mail:
                return {
                    'success': False,
                    'error': 'Failed to connect to inbox',
                    'emails_processed': 0
                }
            
            # Select inbox
            mail.select('INBOX')
            
            # Search for UNREAD emails from today to prevent reprocessing
            # This is the key to avoiding duplicate records
            from datetime import datetime, timedelta
            today_date = datetime.now().strftime("%d-%b-%Y")
            
            # Search for unread emails from today
            # UNSEEN flag = unread emails
            status, messages = mail.search(None, f'(UNSEEN SINCE {today_date})')
            
            if status != 'OK':
                logger.error("Failed to search for emails")
                mail.logout()
                return {
                    'success': False,
                    'error': 'Failed to search emails',
                    'emails_processed': 0
                }
            
            email_ids = messages[0].split() if messages[0] else []
            logger.info(f"Found {len(email_ids)} unread emails from today to check")
            
            # If no unread emails, nothing to process
            if not email_ids:
                logger.info("No unread emails to process")
                mail.logout()
                return {
                    'success': True,
                    'emails_processed': 0,
                    'total_found': 0
                }
            
            processed_count = 0
            errors = []
            
            for email_id in email_ids:
                try:
                    # Fetch the email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        logger.error(f"Failed to fetch email {email_id}")
                        continue
                    
                    # Parse the email
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Check email date to only process recent emails (last 2 minutes)
                    email_date_str = msg.get('Date', '')
                    if email_date_str:
                        try:
                            from email.utils import parsedate_to_datetime
                            email_date = parsedate_to_datetime(email_date_str)
                            current_time = datetime.now(timezone.utc)
                            time_diff = current_time - email_date
                            
                            # Skip emails older than 24 hours (garage responses can be delayed)
                            if time_diff.total_seconds() > 86400:  # 24 hours
                                logger.debug(f"Skipping old email from {msg.get('From', '')} received {time_diff.total_seconds():.0f}s ago")
                                continue
                        except Exception as e:
                            logger.debug(f"Could not parse email date, will process anyway: {str(e)}")
                    
                    # Extract email details
                    from_email = msg.get('From', '')
                    subject = self._decode_email_subject(msg.get('Subject', ''))
                    body = self._extract_email_body(msg)
                    received_at = datetime.now(timezone.utc).isoformat()
                    
                    # Extract attachments
                    attachments = self._extract_attachments(msg)
                    attachment_names = [att['filename'] for att in attachments]
                    
                    logger.info(f"Processing email from {from_email}: {subject}")
                    
                    # Analyze attachments if present
                    attachment_analysis = []
                    for attachment in attachments:
                        analysis = await self._analyze_attachment_with_deepseek(attachment)
                        if analysis:
                            attachment_analysis.append({
                                'filename': attachment['filename'],
                                'analysis': analysis
                            })
                    
                    # Try to extract Request ID from subject or body (format: Ref: req_XXXXX)
                    request_id = self._extract_request_id_from_subject(subject)
                    logger.info(f"🔍 DEBUG: Extracted request ID from subject: {request_id}")
                    
                    # If not found in subject, try to extract from body
                    if not request_id:
                        request_id = self._extract_request_id_from_subject(body)
                        logger.info(f"🔍 DEBUG: Extracted request ID from body: {request_id}")
                    
                    # If we have a request ID, find the VIN from Customer details table
                    vin = None
                    if request_id:
                        vin = self._get_vin_from_request_id(request_id)
                        logger.info(f"Found request ID {request_id}, matched to VIN: {vin}")
                    
                    # Fallback: Try to extract VIN directly from subject or body
                    if not vin:
                        vin = self._extract_vin_from_text(subject + " " + body)
                        if vin:
                            logger.info(f"✅ Extracted VIN from email text: {vin}")
                        else:
                            logger.warning(f"⚠️ Could not extract VIN from email. Subject: {subject[:100]}")
                    
                    # IMPORTANT: Skip emails without VIN to avoid creating empty records
                    if not vin:
                        logger.warning(f"⚠️ Skipping email from {from_email} - no VIN could be extracted. Subject: {subject[:100]}")
                        continue
                    
                    # Note: Duplicate checking is now handled in store_received_email()
                    # which checks by VIN AND Email to avoid storing duplicate responses from same garage
                    
                    # Save to Airtable
                    email_data = {
                        'from_email': from_email,
                        'subject': subject,
                        'body': body,
                        'received_at': received_at,
                        'attachments': attachment_names
                    }
                    
                    # Add attachment analysis to body if available
                    if attachment_analysis:
                        email_data['body'] += "\n\n--- Analyse des pièces jointes ---\n"
                        for analysis in attachment_analysis:
                            email_data['body'] += f"\n{analysis['filename']}:\n{analysis['analysis']}\n"
                    
                    result = self.airtable.store_received_email(email_data, vin)
                    
                    # Check if save was successful
                    if result and result.get('success', False):
                        processed_count += 1
                        logger.info(f"Successfully saved NEW email to Airtable from {from_email}")
                    else:
                        error_msg = result.get('error', 'Unknown error') if result else 'No response'
                        logger.warning(f"Failed to save email from {from_email}: {error_msg}")
                        errors.append(f"Failed to save email from {from_email}: {error_msg}")
                    
                    # ALWAYS mark as read to prevent reprocessing on next check
                    # This is critical - even if save failed, mark as read so we don't process it again
                    try:
                        mail.store(email_id, '+FLAGS', '\\Seen')
                        logger.debug(f"Marked email {email_id} as read")
                    except Exception as e:
                        logger.warning(f"Could not mark email {email_id} as read: {str(e)}")
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_id}: {str(e)}", exc_info=True)
                    errors.append(str(e))
            
            # Logout
            mail.logout()
            
            result = {
                'success': True,
                'emails_processed': processed_count,
                'total_found': len(email_ids),
                'errors': errors
            }
            
            # If we processed any emails, trigger customer response check immediately
            if processed_count > 0:
                logger.info(f"Processed {processed_count} new email(s), triggering immediate customer response check...")
                try:
                    from .customer_response_service import customer_response_service
                    response_result = await customer_response_service.check_and_send_customer_responses()
                    result['customer_responses_sent'] = response_result.get('responses_sent', 0)
                    logger.info(f"Customer response check completed: {response_result.get('responses_sent', 0)} response(s) sent")
                except Exception as e:
                    logger.error(f"Error triggering customer response: {str(e)}", exc_info=True)
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking emails: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'emails_processed': 0
            }
    
    def _extract_request_id_from_subject(self, subject: str) -> Optional[str]:
        """Extract Request ID from email subject (format: Ref: req_XXXXX or in body)"""
        import re
        
        # Pattern to match request ID like "req_1760691162901_aod9uhj2e"
        # Try multiple patterns:
        # 1. "Ref: req_XXXXX" or "Reference: req_XXXXX"
        # 2. "Reference ID: req_XXXXX"
        patterns = [
            r'(?:Ref:|Référence:|Reference\s+ID)[\s:]*?(req_[a-zA-Z0-9_]+)',
            r'req_[a-zA-Z0-9_]+'  # Just match the request ID pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, subject, re.IGNORECASE)
            if match:
                # Extract just the request ID part
                # If pattern has a capture group (group 1), use it; otherwise use the full match
                if match.lastindex and match.lastindex >= 1:
                    # Pattern has capture groups, use the first captured group (the request ID)
                    request_id = match.group(1)
                else:
                    # Pattern has no capture groups, use the full match
                    request_id = match.group(0)
                
                # Ensure we return just the request ID (req_XXXXX format)
                if request_id and 'req_' in request_id:
                    return request_id
        
        return None
    
    def _get_vin_from_request_id(self, request_id: str) -> Optional[str]:
        """Look up VIN from Customer details table using Request ID"""
        try:
            # Search Customer details table for this request ID
            # The request ID should be stored in a field or we can search by DateTime
            customer_records = self.airtable.get_records('Customer details')
            
            # Since request_id contains timestamp, we can try to match it
            # Format: req_TIMESTAMP_RANDOM
            # Extract timestamp
            import re
            timestamp_match = re.search(r'req_(\d+)_', request_id)
            
            if timestamp_match:
                timestamp_ms = int(timestamp_match.group(1))
                
                # Search for customer record with matching timestamp (within 1 second tolerance)
                for record in customer_records:
                    fields = record.get('fields', {})
                    date_str = fields.get('Date and Time') or fields.get('DateTime') or fields.get('Created time')
                    
                    if date_str:
                        try:
                            from datetime import datetime
                            record_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                            record_timestamp_ms = int(record_date.timestamp() * 1000)
                            
                            # Check if timestamps are close (within 2 seconds)
                            if abs(record_timestamp_ms - timestamp_ms) < 2000:
                                vin = fields.get('VIN')
                                if vin:
                                    logger.info(f"Matched request {request_id} to VIN {vin}")
                                    return vin
                        except Exception as e:
                            logger.debug(f"Error parsing date for record: {str(e)}")
                            continue
            
            logger.warning(f"Could not find VIN for request ID: {request_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error looking up VIN from request ID: {str(e)}", exc_info=True)
            return None
    
    def _extract_vin_from_text(self, text: str) -> Optional[str]:
        """Try to extract VIN from text using regex"""
        import re
        
        # VIN pattern: 17 alphanumeric characters excluding I, O, Q
        # Standard VIN pattern
        vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'
        
        matches = re.findall(vin_pattern, text.upper())
        
        if matches:
            logger.debug(f"🔍 DEBUG: Found VIN matches: {matches}")
            return matches[0]
        
        # Fallback: Look for "VIN:" followed by alphanumeric
        vin_label_pattern = r'(?:VIN|Vin|vin)[\s:]*([A-HJ-NPR-Z0-9]{17})'
        label_matches = re.findall(vin_label_pattern, text.upper())
        
        if label_matches:
            logger.debug(f"🔍 DEBUG: Found VIN via label pattern: {label_matches}")
            return label_matches[0]
        
        logger.debug(f"🔍 DEBUG: No VIN found in text")
        return None

# Singleton instance
email_monitor_service = EmailMonitorService()
