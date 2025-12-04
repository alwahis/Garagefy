import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from .baserow_service import baserow_service as airtable_service
from .email_service import email_service

logger = logging.getLogger(__name__)

class CustomerResponseService:
    """Service for sending compiled quotes to customers"""
    
    # Field ID mappings for Customer details table
    # These map logical field names to Baserow field IDs
    CUSTOMER_FIELD_IDS = {
        'Name': 'field_6389828',
        'Email': 'field_6389829',
        'Phone': 'field_6389830',
        'VIN': 'field_6389831',
        'Car Brand': 'field_6389832',
        'Plate Number': 'field_6389833',
        'Notes': 'field_6389834',
        'Images': 'field_6389835',
        'Sent Emails': 'field_6389836',
        'Date and Time': 'field_6389837',
    }
    
    def __init__(self):
        self.airtable = airtable_service
        self.email_service = email_service
    
    def _get_field(self, fields: dict, field_name: str, default: str = '') -> str:
        """Get field value by name or field ID"""
        # Try field name first
        value = fields.get(field_name)
        if value:
            return str(value).strip()
        
        # Try field ID
        field_id = self.CUSTOMER_FIELD_IDS.get(field_name)
        if field_id:
            value = fields.get(field_id)
            if value:
                return str(value).strip()
        
        return default
    
    def _calculate_business_days_ago(self, days: int) -> datetime:
        """Calculate a datetime N business days ago"""
        current = datetime.now(timezone.utc)
        days_subtracted = 0
        
        while days_subtracted < days:
            current -= timedelta(days=1)
            # Skip weekends
            if current.weekday() < 5:
                days_subtracted += 1
        
        return current
    
    async def check_and_send_customer_responses(self) -> Dict[str, Any]:
        """
        Check for customers ready to receive responses and send them
        
        IMPORTANT: Uses VIN as the unique identifier for each request.
        Each VIN receives ONLY ONE consolidated email with all garage responses.
        
        A customer is ready when:
        1. All garages have responded, OR
        2. 2 business days have passed since quote request was sent
        
        Returns:
            Dict with processing results
        """
        try:
            # Get all customer records from Customer details table
            customer_records = self.airtable.get_records('Customer details')
            
            logger.info(f"Checking {len(customer_records)} customer records")
            
            # Group records by VIN to ensure ONE email per VIN
            vin_groups = {}
            for record in customer_records:
                fields = record.get('fields', {})
                # Use helper to get VIN from either field name or ID
                vin = self._get_field(fields, 'VIN')
                
                if not vin:
                    logger.warning(f"Record {record.get('id')} has no VIN, skipping")
                    continue
                
                # Check if response already sent using Sent Emails field
                sent_emails = self._get_field(fields, 'Sent Emails')
                if sent_emails and 'quote sent' in sent_emails.lower():
                    logger.debug(f"Response already sent for VIN {vin} (Sent Emails: {sent_emails}), skipping")
                    continue
                
                # Group by VIN - use the most recent record for each VIN
                if vin not in vin_groups:
                    vin_groups[vin] = {
                        'record': record,
                        'fields': fields,
                        'all_records': [record]  # Keep track of all records for this VIN
                    }
                else:
                    # Keep track of all records with this VIN
                    vin_groups[vin]['all_records'].append(record)
                    # Use the most recent record
                    existing_date = vin_groups[vin]['fields'].get('Date and Time', '')
                    new_date = fields.get('Date and Time', '')
                    if new_date > existing_date:
                        vin_groups[vin]['record'] = record
                        vin_groups[vin]['fields'] = fields
            
            logger.info(f"Found {len(vin_groups)} unique VINs to process")
            
            responses_sent = 0
            errors = []
            
            # Process each VIN (ONE email per VIN)
            for vin, vin_data in vin_groups.items():
                try:
                    fields = vin_data['fields']
                    record_id = vin_data['record'].get('id')
                    all_records = vin_data['all_records']
                    
                    # Get submission date using helper
                    # Log available fields for first record to help debug
                    if vin == list(vin_groups.keys())[0]:
                        logger.info(f"📋 Available fields in Customer details: {list(fields.keys())}")
                        # Log all field values to help identify correct date field
                        for key, value in fields.items():
                            if value and isinstance(value, str) and len(str(value)) > 0:
                                logger.info(f"  Field {key}: {str(value)[:50]}")
                    
                    submission_date_str = self._get_field(fields, 'Date and Time')
                    current_time = datetime.now(timezone.utc)
                    
                    # Validate and parse date - use fallback if invalid
                    submission_date = None
                    if submission_date_str:
                        try:
                            # Check if it looks like a date (contains - or T or :)
                            if any(c in submission_date_str for c in ['-', 'T', ':']):
                                submission_date = datetime.fromisoformat(submission_date_str.replace('Z', '+00:00'))
                            else:
                                logger.warning(f"Date field contains non-date value: '{submission_date_str}' for VIN {vin}")
                        except ValueError as e:
                            logger.warning(f"Invalid date format '{submission_date_str}' for VIN {vin}: {e}")
                    
                    if not submission_date:
                        # Use fallback: assume request was made 1 day ago
                        logger.info(f"Using fallback date (1 day ago) for VIN {vin}")
                        submission_date = current_time - timedelta(days=1)
                    
                    # Skip old requests (older than 7 days) to prevent processing historical data
                    days_since_submission = (current_time - submission_date).days
                    if days_since_submission > 7:
                        # Mark all records with this VIN as sent
                        for rec in all_records:
                            try:
                                self.airtable.update_record(
                                    'Customer details',
                                    rec.get('id'),
                                    {'Sent Emails': f'Quote sent on {current_time.strftime("%Y-%m-%d")}'}
                                )
                            except Exception as e:
                                logger.warning(f"Could not auto-mark old request: {str(e)}")
                        logger.info(f"Auto-marked {len(all_records)} old record(s) for VIN {vin} ({days_since_submission} days old) as sent")
                        continue
                    
                    # Calculate business days
                    business_days_passed = self._count_business_days(submission_date, current_time)
                    
                    # Check if ALL garages have responded
                    all_garages_responded = self._check_all_garages_responded(vin)
                    
                    # Send response if:
                    # 1. All garages have responded, OR
                    # 2. 2 business days have passed
                    should_send = all_garages_responded or business_days_passed >= 2
                    
                    if should_send:
                        reason = "all garages responded" if all_garages_responded else "2 business days passed"
                        logger.info(f"Sending consolidated response for VIN {vin} to {fields.get('Email')} ({reason})")
                        
                        success = await self._send_customer_response(record_id, fields, vin)
                        
                        if success:
                            responses_sent += 1
                            # Mark ALL records with this VIN as sent to prevent duplicate emails
                            for rec in all_records:
                                try:
                                    sent_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                                    self.airtable.update_record(
                                        'Customer details',
                                        rec.get('id'),
                                        {'Sent Emails': f'Quote sent on {sent_time}'}
                                    )
                                    logger.info(f"Marked record {rec.get('id')} for VIN {vin} as sent")
                                except Exception as update_error:
                                    logger.warning(f"Could not update Sent Emails for {rec.get('id')}: {str(update_error)}")
                        else:
                            errors.append(f"Failed to send response for VIN {vin} to {fields.get('Email')}")
                    
                except Exception as e:
                    logger.error(f"Error processing VIN {vin}: {str(e)}", exc_info=True)
                    errors.append(str(e))
            
            return {
                'success': True,
                'responses_sent': responses_sent,
                'total_vins_checked': len(vin_groups),
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error checking customer responses: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'responses_sent': 0
            }
    
    def _count_business_days(self, start_date: datetime, end_date: datetime) -> int:
        """Count business days between two dates"""
        current = start_date
        business_days = 0
        
        while current < end_date:
            current += timedelta(days=1)
            # Skip weekends
            if current.weekday() < 5:
                business_days += 1
        
        return business_days
    
    def _extract_price_from_text(self, text: str) -> Optional[str]:
        """
        Extract price from email text
        
        Looks for patterns like:
        - "300 euros"
        - "300€"
        - "300-400 euros" (range)
        - "EUR 300"
        - "€300"
        
        Args:
            text: Email body text
            
        Returns:
            Extracted price string or None
        """
        if not text:
            return None
        
        import re
        
        # Patterns to match prices (in order of specificity)
        price_patterns = [
            # Range with currency: "300-400 euros", "300-400€", "300 - 400 euros"
            r'(\d+[\s]*[-–]\s*\d+)\s*(?:euros?|€|EUR)',
            # Single price with currency after: "300 euros", "300€"
            r'(\d+(?:[.,]\d{1,2})?)\s*(?:euros?|€|EUR)',
            # Currency before price: "EUR 300", "€300"
            r'(?:euros?|€|EUR)\s*(\d+(?:[.,]\d{1,2})?)',
            # Just numbers followed by currency symbol (more lenient)
            r'(\d+)\s*€',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                price = match.group(1).strip()
                # Check if we captured the currency, if not add it
                if '€' not in match.group(0) and 'euro' not in match.group(0).lower():
                    return f"{price}€"
                else:
                    # Return the full matched text
                    return match.group(0).strip()
        
        return None
    
    def _check_all_garages_responded(self, vin: str) -> bool:
        """
        Check if all garages in the 'Fix it' table have responded for this VIN
        
        Args:
            vin: Vehicle Identification Number
            
        Returns:
            bool: True if all garages have responded
        """
        try:
            # Get all garages from Fix it table
            garages = self.airtable.get_fix_it_garages()
            total_garages = len(garages)
            
            if total_garages == 0:
                logger.warning("No garages found in Fix it table")
                return False
            
            # Get all responses from Received email table for this VIN
            received_emails = self.airtable.get_records(
                'Recevied email',
                formula=f'{{VIN}} = "{vin}"'
            )
            
            # Get unique garage emails that have responded
            responded_emails = set()
            for email_record in received_emails:
                email_fields = email_record.get('fields', {})
                garage_email = email_fields.get('Email', '').strip().lower()
                if garage_email:
                    # Extract just the email address from "Name <email@domain.com>" format
                    import re
                    email_match = re.search(r'<(.+?)>', garage_email)
                    if email_match:
                        garage_email = email_match.group(1).strip().lower()
                    # Final normalization: remove whitespace
                    garage_email = garage_email.replace(' ', '')
                    if garage_email:
                        responded_emails.add(garage_email)
                        logger.debug(f"Garage responded: {garage_email}")
            
            # Get all garage emails (just the address part)
            all_garage_emails = set()
            for g in garages:
                if g.get('email'):
                    email = g['email'].strip().lower()
                    # Extract just the email address from "Name <email@domain.com>" format if present
                    import re
                    email_match = re.search(r'<(.+?)>', email)
                    if email_match:
                        email = email_match.group(1).strip().lower()
                    # Final normalization: remove whitespace
                    email = email.replace(' ', '')
                    if email:
                        all_garage_emails.add(email)
                        logger.debug(f"Expected garage: {email}")
            
            # Check if all garages have responded
            # All garages have responded if: responded_emails contains all garage emails
            all_responded = all_garage_emails.issubset(responded_emails) if len(all_garage_emails) > 0 else False
            
            logger.info(f"VIN {vin}: {len(responded_emails)}/{len(all_garage_emails)} garages responded")
            logger.info(f"  Expected garages: {all_garage_emails}")
            logger.info(f"  Responded garages: {responded_emails}")
            logger.info(f"  All responded: {all_responded}")
            
            return all_responded
            
        except Exception as e:
            logger.error(f"Error checking if all garages responded: {str(e)}", exc_info=True)
            return False
    
    async def _send_customer_response(self, record_id: str, customer_fields: Dict[str, Any], vin: str) -> bool:
        """
        Send compiled quotes to customer for a specific VIN
        
        Args:
            record_id: Airtable record ID
            customer_fields: Customer record fields
            vin: Vehicle Identification Number (unique identifier for the request)
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            # Use helper to get fields by name or ID
            customer_email = self._get_field(customer_fields, 'Email')
            customer_name = self._get_field(customer_fields, 'Name') or 'Cher client'
            car_brand = self._get_field(customer_fields, 'Car Brand') or 'N/A'
            
            if not customer_email:
                logger.error(f"No customer email found. Fields: {list(customer_fields.keys())}")
                return False
            
            logger.info(f"📧 Customer: {customer_name} <{customer_email}>, Car: {car_brand}")
            
            logger.info(f"Compiling quotes for VIN {vin}, customer: {customer_email}")
            
            # Get all quotes from Received email table matching this VIN
            received_emails = self.airtable.get_records(
                'Recevied email',
                formula=f'{{VIN}} = "{vin}"'
            )
            
            logger.info(f"Found {len(received_emails)} response(s) from garages for VIN {vin}")
            
            # Get all garages from Fix it table (includes phone, address, etc.)
            garages = self.airtable.get_fix_it_garages()
            garage_dict = {g['email'].strip().lower(): g for g in garages}
            
            # Compile quotes with garage contact information
            quotes = []
            for email_record in received_emails:
                email_fields = email_record.get('fields', {})
                garage_email_raw = email_fields.get('Email', '').strip().lower()
                
                # Extract just the email address from "Name <email@domain.com>" format
                import re
                email_match = re.search(r'<(.+?)>', garage_email_raw)
                garage_email_clean = email_match.group(1).strip().lower() if email_match else garage_email_raw
                
                # Get garage details from Fix it table using clean email
                garage = garage_dict.get(garage_email_clean, {})
                
                # Extract only the garage's direct response (before email thread)
                body_full = email_fields.get('Body', '')
                
                # Remove email thread - split by common email reply markers
                import re
                
                # Try to extract price from body if not already set
                quote_amount = email_fields.get('Quote', '')
                if not quote_amount or quote_amount == 'Non spécifié':
                    quote_amount = self._extract_price_from_text(body_full) or 'Non spécifié'
                
                # Try multiple splitting patterns (in order of most specific to least)
                body_clean = body_full
                
                # Pattern to match email thread markers
                # The pattern "On [date]... wrote:" can span multiple lines
                patterns_to_try = [
                    # Match "On [date]... wrote:" even if it spans lines (use .+? to allow > in email addresses)
                    (r'\n\nOn\s+.+?wrote\s*:', re.DOTALL | re.IGNORECASE),
                    (r'\nOn\s+.+?wrote\s*:', re.DOTALL | re.IGNORECASE),
                    # Match quoted reply lines (lines starting with >)
                    (r'\n>', 0),
                    # Match email separator
                    (r'\n-{3,}', 0),
                    # Match "From:" header
                    (r'\nFrom\s*:', 0),
                ]
                
                for pattern, flags in patterns_to_try:
                    match = re.search(pattern, body_clean, flags=flags)
                    if match:
                        # Take everything before the match
                        body_clean = body_clean[:match.start()].strip()
                        break
                
                # Final cleanup: remove any trailing whitespace
                body_clean = body_clean.strip()
                
                quotes.append({
                    'garage_name': garage.get('name', 'Garage inconnu'),
                    'garage_email': garage_email_clean,
                    'garage_phone': garage.get('phone_number', 'Non disponible'),  # From Fix it table Phone field (phone_number)
                    'garage_address': garage.get('address', 'Non disponible'),  # From Fix it table Address field
                    'quote_amount': quote_amount,  # Extracted from email body if not set
                    'subject': email_fields.get('Subject', ''),
                    'body': body_clean,  # Only garage's response, not email thread
                    'received_at': email_fields.get('Received At', '')
                })
            
            # Build email content
            subject = f"🚗 Vos devis - {car_brand}"
            
            # Build quotes cards (mobile-friendly)
            quotes_html = self._build_quotes_cards(quotes)
            
            html_content = f"""
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; margin: 0; padding: 0;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white;">
                    
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%); padding: 30px 20px; text-align: center;">
                        <h1 style="color: #0078D4; margin: 0; font-size: 28px; font-weight: bold;">Garagefy</h1>
                        <p style="color: #1A202C; margin: 10px 0 0 0; font-size: 16px;">Vos devis sont prêts!</p>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 20px;">
                        <p style="font-size: 16px; margin-bottom: 20px;">Bonjour <strong>{customer_name}</strong>,</p>
                        
                        <p style="font-size: 15px; color: #666;">Nous avons reçu <strong style="color: #0078D4;">{len(quotes)} devis</strong> pour votre <strong>{car_brand}</strong></p>
                        
                        <!-- Vehicle Info -->
                        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #0078D4; margin: 20px 0; font-size: 14px;">
                            <p style="margin: 5px 0;"><strong>VIN:</strong> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 3px; font-size: 12px;">{vin}</code></p>
                        </div>
                        
                        {quotes_html}
                        
                        <!-- Next Steps -->
                        <div style="background-color: #0078D4; color: white; padding: 20px; border-radius: 8px; margin: 25px 0;">
                            <h3 style="margin-top: 0; color: white; font-size: 18px;">📋 Prochaines étapes</h3>
                            <ol style="margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                                <li>Comparez les prix et détails ci-dessus</li>
                                <li>Contactez le garage de votre choix</li>
                                <li>Prenez rendez-vous</li>
                            </ol>
                        </div>
                        
                        <p style="margin-top: 30px; color: #666; font-size: 14px;">Cordialement,<br><strong>L'équipe Garagefy</strong></p>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f7fafc; padding: 20px; text-align: center; font-size: 12px; color: #718096;">
                        <p style="margin: 0;">Garagefy - Plateforme de comparaison de devis carrosserie</p>
                        <p style="margin: 10px 0 0 0;"><a href="mailto:info@garagefy.app" style="color: #0078D4;">info@garagefy.app</a></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Send email
            success = await self.email_service.send_email(
                to_emails=[customer_email],
                subject=subject,
                html_content=html_content
            )
            
            if success:
                logger.info(f"Successfully sent response to {customer_email}")
            else:
                logger.error(f"Failed to send response to {customer_email}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending customer response: {str(e)}", exc_info=True)
            return False
    
    def _build_quotes_cards(self, quotes: List[Dict[str, Any]]) -> str:
        """Build mobile-friendly quote cards with garage contact information"""
        if not quotes:
            return """
            <div style="background-color: #FFF3CD; padding: 20px; border-radius: 8px; border-left: 4px solid #FFC107; margin: 20px 0;">
                <p style="margin: 0; font-weight: bold;">⚠️ Aucun devis reçu</p>
                <p style="margin: 10px 0 0 0; font-size: 14px;">Malheureusement, nous n'avons pas encore reçu de réponses des garages.</p>
            </div>
            """
        
        cards_html = '<h3 style="color: #0078D4; margin: 25px 0 15px 0;">💬 Devis reçus:</h3>'
        
        for i, quote in enumerate(quotes):
            # Get full garage response (body)
            garage_response = quote.get('body', 'Aucune réponse détaillée fournie')
            
            cards_html += f"""
            <div style="background-color: white; border: 2px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                
                <!-- Garage Name & Price -->
                <div style="border-bottom: 2px solid #0078D4; padding-bottom: 15px; margin-bottom: 15px;">
                    <h3 style="color: #0078D4; margin: 0 0 10px 0; font-size: 20px;">🔧 {quote['garage_name']}</h3>
                    <div style="background-color: #E8F5E9; padding: 12px; border-radius: 6px; text-align: center;">
                        <p style="margin: 0; font-size: 14px; color: #666;">Prix estimé</p>
                        <p style="margin: 5px 0 0 0; font-size: 28px; font-weight: bold; color: #2E7D32;">{quote.get('quote_amount', 'Non spécifié')}</p>
                    </div>
                </div>
                
                <!-- Contact Info -->
                <div style="background-color: #f7fafc; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <h4 style="color: #0078D4; margin: 0 0 12px 0; font-size: 16px;">📞 Contact</h4>
                    
                    <p style="margin: 8px 0; font-size: 14px; line-height: 1.6;">
                        <strong>📍 Adresse:</strong><br>
                        <span style="color: #666;">{quote['garage_address']}</span>
                    </p>
                    
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>📞 Téléphone:</strong><br>
                        <a href="tel:{quote['garage_phone']}" style="color: #0078D4; text-decoration: none; font-weight: bold;">{quote['garage_phone']}</a>
                    </p>
                    
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>📧 Email:</strong><br>
                        <a href="mailto:{quote['garage_email']}" style="color: #0078D4; text-decoration: none;">{quote['garage_email']}</a>
                    </p>
                </div>
                
                <!-- Garage Response -->
                <div style="background-color: #fffef0; padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700;">
                    <h4 style="color: #1A202C; margin: 0 0 10px 0; font-size: 15px;">💬 Réponse du garage:</h4>
                    <div style="font-size: 14px; color: #333; line-height: 1.7; white-space: pre-wrap; word-wrap: break-word;">{garage_response}</div>
                    <p style="margin: 12px 0 0 0; font-size: 12px; color: #999;">Reçu le: {quote.get('received_at', 'N/A')[:16]}</p>
                </div>
                
            </div>
            """
        
        return cards_html

# Singleton instance
customer_response_service = CustomerResponseService()
