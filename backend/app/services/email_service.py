import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
import msal
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        self.client_id = os.getenv('MS_CLIENT_ID')
        self.client_secret = os.getenv('MS_CLIENT_SECRET')
        self.tenant_id = os.getenv('MS_TENANT_ID')
        self.user_email = os.getenv('EMAIL_ADDRESS', 'info@garagefy.app')
        
        # Validate required environment variables
        if not self.client_id or not self.client_secret or not self.tenant_id:
            raise ValueError("Missing required Microsoft credentials. Please set MS_CLIENT_ID, MS_CLIENT_SECRET, and MS_TENANT_ID in .env file")
        
        # Microsoft Graph API configuration
        # Using application permissions (client credentials flow)
        self.scopes = ['https://graph.microsoft.com/.default']
        self.authority = f'https://login.microsoftonline.com/{self.tenant_id}'
        self.token_cache = {}
        
        # Microsoft Graph API endpoint
        self.graph_endpoint = 'https://graph.microsoft.com/v1.0'
        
        # Log the configuration (without sensitive data)
        self.logger.info(f"Initializing EmailService for {self.user_email}")
        
        # Initialize token
        try:
            self._ensure_token()
        except Exception as e:
            self.logger.error(f"Failed to initialize EmailService: {str(e)}")
            raise
    
    def _get_token(self):
        """Get access token using MSAL with client credentials flow"""
        try:
            app = msal.ConfidentialClientApplication(
                client_id=self.client_id,
                authority=self.authority,
                client_credential=self.client_secret,
            )
            
            # Try to get a token from cache
            result = app.acquire_token_silent(
                scopes=self.scopes,
                account=None
            )
            
            # If no token in cache, acquire a new one using client credentials flow
            if not result:
                self.logger.info("No token in cache, acquiring new token...")
                result = app.acquire_token_for_client(
                    scopes=self.scopes
                )
            
            if "access_token" in result:
                self.logger.info("Successfully acquired access token")
                return result["access_token"]
            else:
                error_msg = f"Failed to acquire token: {result.get('error')} - {result.get('error_description')}"
                if 'error_codes' in result:
                    error_msg += f" (Error codes: {result['error_codes']})"
                if 'correlation_id' in result:
                    error_msg += f" (Correlation ID: {result['correlation_id']})"
                self.logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(f"Error in _get_token: {str(e)}", exc_info=True)
            raise
    
    def _ensure_token(self):
        """Ensure we have a valid token - always get fresh token since MSAL handles caching"""
        # Don't cache tokens manually - MSAL handles it internally and checks expiration
        return self._get_token()
    
    def _get_auth_string(self):
        """Get the OAuth2 authentication string"""
        token = self._ensure_token()
        if not token:
            raise Exception("No valid OAuth2 token available")
        return f"user={self.user_email}\1auth=Bearer {token}\1\1"
    
    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: str = None,
        cc_emails: List[str] = None,
        bcc_emails: List[str] = None,
        attachments: List[Dict[str, Any]] = None,
    ) -> bool:
        """
        Send an email using Microsoft Graph API
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content of the email (optional)
            cc_emails: List of CC email addresses (optional)
            bcc_emails: List of BCC email addresses (optional)
            attachments: List of attachment dictionaries with 'content' and 'filename' keys
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not text_content:
            # Create a simple text version from HTML if not provided
            import re
            text_content = re.sub(r'<[^>]+>', '', html_content)
        
        try:
            # Get access token first
            access_token = self._ensure_token()
            
            # Prepare the email message with professional sender name and anti-spam headers
            message = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "HTML",
                        "content": html_content
                    },
                    "from": {
                        "emailAddress": {
                            "address": self.user_email,
                            "name": "Garagefy Quote Service"
                        }
                    },
                    "replyTo": [
                        {
                            "emailAddress": {
                                "address": self.user_email,
                                "name": "Garagefy"
                            }
                        }
                    ],
                    "toRecipients": [{"emailAddress": {"address": email}} for email in to_emails],
                    "importance": "normal",
                    "internetMessageHeaders": [
                        {
                            "name": "X-Auto-Response-Suppress",
                            "value": "OOF, AutoReply"
                        },
                        {
                            "name": "X-Entity-ID",
                            "value": "garagefy-quote-request"
                        }
                    ]
                },
                "saveToSentItems": "true"
            }
            
            # Add CC recipients if any
            if cc_emails:
                message["message"]["ccRecipients"] = [{"emailAddress": {"address": email}} for email in cc_emails]
                
            # Add BCC recipients if any
            if bcc_emails:
                message["message"]["bccRecipients"] = [{"emailAddress": {"address": email}} for email in bcc_emails]
            
            # Add attachments if any
            if attachments:
                message["message"]["attachments"] = []
                for attachment in attachments:
                    import base64
                    message["message"]["attachments"].append({
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": attachment['filename'],
                        "contentType": attachment.get('content_type', 'application/octet-stream'),
                        "contentBytes": base64.b64encode(attachment['content']).decode('utf-8')
                    })
            
            # Send the email using Microsoft Graph API with aiohttp
            import aiohttp
            
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    }
                    
                    async with session.post(
                        f"{self.graph_endpoint}/users/{self.user_email}/sendMail",
                        headers=headers,
                        json=message,
                        timeout=30
                    ) as response:
                        response_text = await response.text()
                        
                        if response.status == 202:
                            self.logger.info(f"Email sent successfully to {', '.join(to_emails)}")
                            return True
                        elif response.status == 401:
                            # Token expired, retry once with fresh token
                            self.logger.warning("Token expired (401), retrying with fresh token...")
                            fresh_token = self._get_token()
                            headers['Authorization'] = f'Bearer {fresh_token}'
                            
                            async with session.post(
                                f"{self.graph_endpoint}/users/{self.user_email}/sendMail",
                                headers=headers,
                                json=message,
                                timeout=30
                            ) as retry_response:
                                retry_text = await retry_response.text()
                                if retry_response.status == 202:
                                    self.logger.info(f"Email sent successfully after token refresh to {', '.join(to_emails)}")
                                    return True
                                else:
                                    error_msg = f"Failed to send email after retry: {retry_response.status} - {retry_text}"
                                    self.logger.error(error_msg)
                                    raise Exception(error_msg)
                        else:
                            error_msg = f"Failed to send email: {response.status} - {response_text}"
                            self.logger.error(error_msg)
                            raise Exception(error_msg)
            
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending email: {str(e)}")
                return False
            except Exception as e:
                self.logger.error(f"Error sending email: {str(e)}", exc_info=True)
                return False
                
        except Exception as e:
            self.logger.error(f"Error preparing email: {str(e)}", exc_info=True)
            return False

# Singleton instance - lazy initialization
_email_service_instance = None

def get_email_service():
    """Get or create the EmailService instance (lazy initialization)"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance

# For backward compatibility, create a proxy object
class EmailServiceProxy:
    """Proxy that lazily initializes the actual service"""
    def __getattr__(self, name):
        return getattr(get_email_service(), name)

email_service = EmailServiceProxy()
