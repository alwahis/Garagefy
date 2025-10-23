import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
import msal
import aiohttp
from dotenv import load_dotenv
import sys

# Set up paths
from scripts import setup_paths
setup_paths()

# Import services using relative paths
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import the services
from app.services.airtable_service import AirtableService
from app.services.email_service import get_access_token

# Initialize Airtable service
airtable_service = AirtableService()

load_dotenv()

logger = logging.getLogger("garagefy.email_ingestion")

MS_CLIENT_ID = os.getenv('MS_CLIENT_ID')
MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET')
MS_TENANT_ID = os.getenv('MS_TENANT_ID')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

SCOPES = ['https://graph.microsoft.com/.default']
AUTHORITY = f'https://login.microsoftonline.com/{MS_TENANT_ID}'
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# Utility to get access token
async def get_access_token():
    app = msal.ConfidentialClientApplication(
        client_id=MS_CLIENT_ID,
        authority=AUTHORITY,
        client_credential=MS_CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        return result["access_token"]
    raise Exception(f"Failed to acquire token: {result.get('error_description')}")

# Utility to extract VIN from subject or body
# Matches various VIN patterns and formats
VIN_REGEXES = [
    # Standard VIN patterns
    re.compile(r'VIN[\s\-:]*([A-HJ-NPR-Z0-9]{8,17})', re.IGNORECASE),
    # Vehicle ID patterns
    re.compile(r'Vehicle[\s\-]*(?:ID|Number|No\.?|#)?[\s\-:]*([A-HJ-NPR-Z0-9]{8,17})', re.IGNORECASE),
    # Service request patterns
    re.compile(r'(?:Service Request|Quote|Estimate|Request)[\s\-]*(?:for|#)?[\s\-:]*([A-HJ-NPR-Z0-9]{8,17})', re.IGNORECASE),
    # Common patterns in email subjects
    re.compile(r'(?:VIN|ID|No\.?)[\s\-:]*([A-HJ-NPR-Z0-9]{8,17})', re.IGNORECASE),
    # Any standalone VIN (17 chars)
    re.compile(r'\b([A-HJ-NPR-Z0-9]{17})\b', re.IGNORECASE),
    # Shorter VINs (6-16 chars) with word boundaries
    re.compile(r'\b([A-HJ-NPR-Z0-9]{6,16})\b', re.IGNORECASE),
    # Look for VINs in common email formats
    re.compile(r'(?:VIN|ID|No\.?)[\s\-:]*([A-Z0-9]{6,})', re.IGNORECASE),
    # Look for VINs after common prefixes
    re.compile(r'(?:VIN|ID|No\.?|#)[\s\-:]*([A-Z0-9]{6,})', re.IGNORECASE)
]

def extract_vin(subject: str, body: str) -> str:
    """Extract VIN from email subject or body using multiple patterns."""
    if not subject and not body:
        return None
        
    # Clean up the text by removing common noise
    def clean_text(text):
        if not text:
            return ""
        # Remove HTML tags if present
        text = re.sub(r'<[^>]+>', ' ', text)
        # Remove common email quoting patterns
        text = re.sub(r'On\s+.*?wrote:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Le\s+.*?a écrit\s*:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^>+\s*', '', text, flags=re.MULTILINE)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    # Check both subject and body, but prioritize subject
    for text in [subject, body]:
        text = clean_text(text)
        if not text:
            continue
            
        for regex in VIN_REGEXES:
            try:
                matches = regex.findall(text)
                if matches:
                    # Get the longest match (more likely to be a complete VIN)
                    vin = max(matches, key=len)
                    print(f"VIN regex '{regex.pattern}' matched: {vin} in '{text[:80]}...'")
                    return vin.upper()  # Standardize to uppercase
            except Exception as e:
                print(f"Error applying regex {regex.pattern}: {str(e)}")
                continue
    
    # If no VIN found with patterns, try to find any 6+ digit/letter sequence in subject
    if subject:
        possible_vin = re.search(r'([A-Z0-9]{6,})', subject.upper())
        if possible_vin:
            vin = possible_vin.group(1)
            print(f"Found potential VIN in subject using fallback: {vin}")
            return vin
    
    return None
    return ""

# Track processed email IDs to avoid duplicates
PROCESSED_EMAILS_FILE = 'processed_emails.txt'

def load_processed_emails():
    try:
        with open(PROCESSED_EMAILS_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def save_processed_email(email_id):
    with open(PROCESSED_EMAILS_FILE, 'a') as f:
        f.write(f"{email_id}\n")

async def get_recent_emails():
    """Fetch recent unprocessed emails from the inbox."""
    processed_emails = load_processed_emails()
    new_emails = []
    
    try:
        # Get access token
        token = await get_access_token()
        if not token:
            print("Error: Failed to get Microsoft Graph API access token")
            return []

        # Set up API request headers
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Prefer': 'outlook.body-content-type="text"'  # Get plain text body
        }
        
        # Get emails from the last 7 days
        since = datetime.utcnow() - timedelta(days=7)
        url = (
            f"{GRAPH_ENDPOINT}/users/{EMAIL_ADDRESS}/mailFolders/inbox/messages"
            f"?$top=50"  # Increase limit to 50 emails
            f"&$orderby=receivedDateTime desc"
            f"&$select=id,receivedDateTime,subject,from,body,hasAttachments"
            f"&$filter=receivedDateTime ge {get_iso8601(since)}"
        )
        
        print(f"Fetching emails since {since.isoformat()}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    print(f"Error fetching emails: {resp.status} - {error_text}")
                    return []
                    
                data = await resp.json()
                emails = data.get('value', [])
                print(f"Found {len(emails)} emails in inbox")
                
                for item in emails:
                    try:
                        email_id = item.get('id')
                        if not email_id or email_id in processed_emails:
                            continue
                        
                        # Extract email data
                        from_email = item.get('from', {}).get('emailAddress', {}).get('address', '')
                        subject = item.get('subject', 'No Subject')
                        body = item.get('body', {}).get('content', '')
                        received_at = item.get('receivedDateTime', '')
                        
                        # Skip system or notification emails
                        if any(domain in from_email for domain in ['no-reply', 'notifications', 'noreply']):
                            print(f"Skipping system/notification email from: {from_email}")
                            save_processed_email(email_id)
                            continue
                        
                        email_data = {
                            'id': email_id,
                            'from_email': from_email,
                            'subject': subject,
                            'body': body,
                            'received_at': received_at,
                            'has_attachments': item.get('hasAttachments', False)
                        }
                        
                        new_emails.append(email_data)
                        
                    except Exception as e:
                        print(f"Error processing email item: {str(e)}")
                        continue
                
                print(f"Found {len(new_emails)} new, unprocessed emails")
                return new_emails
                
    except Exception as e:
        print(f"Failed to get recent emails: {e}")

def get_iso8601(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

async def ingest_garage_replies():
    """Process new emails, extract VINs, and store in Airtable."""
    try:
        new_emails = await get_recent_emails()
        if not new_emails:
            print("No new emails to process.")
            return True
            
        processed_count = 0
        for email in new_emails:
            try:
                email_id = email.get('id')
                from_email = email.get('from_email', '').strip()
                subject = email.get('subject', '').strip()
                body = email.get('body', '')
                received_at = email.get('received_at')
                
                print(f"\n{'='*80}")
                print(f"Processing email ID: {email_id}")
                print(f"From: {from_email}")
                print(f"Subject: {subject}")
                print(f"Received: {received_at}")
                
                # Extract VIN from email
                vin = extract_vin(subject, body)
                print(f"Extracted VIN: {vin if vin else 'None'}")
                
                if not vin:
                    print("No VIN found in email, skipping...")
                    save_processed_email(email_id)  # Mark as processed to avoid reprocessing
                    continue
                
                # Prepare the email data for Airtable
                email_data = {
                    'VIN': vin,
                    'Email': from_email,
                    'Subject': subject,
                    'Body': body[:5000],  # Limit body length to avoid Airtable field limits
                    'Received At': received_at or datetime.utcnow().isoformat()
                }
                
                print(f"Storing in Airtable: {email_data}")
                
                # Store in Airtable
                result = airtable_service.store_received_email(email_data, vin)
                if result and result.get('id'):
                    print(f"Successfully stored email in Airtable (Record ID: {result.get('id')})")
                    processed_count += 1
                else:
                    print(f"Warning: Email stored but no record ID returned: {result}")
                
                # Mark as processed
                save_processed_email(email_id)
                
            except Exception as e:
                print(f"Error processing email {email_id}: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\nProcessing complete. Successfully processed {processed_count} of {len(new_emails)} emails.")
        return True
        
    except Exception as e:
        print(f"Error in ingest_garage_replies: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(ingest_garage_replies())
