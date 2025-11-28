import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta, timezone
from .baserow_service import baserow_service as airtable_service
from .email_service import email_service

logger = logging.getLogger(__name__)

class FixItService:
    """Service for handling Fix it quote requests"""
    
    def __init__(self):
        self.airtable = airtable_service
        self.email_service = email_service
    
    async def send_quote_requests(
        self,
        request_id: str,
        car_brand: str,
        vin: str,
        license_plate: str,
        damage_notes: str,
        image_urls: List[str]
    ) -> Dict[str, Any]:
        """
        Send quote requests to all garages in the Fix it table
        
        Args:
            request_id: Unique identifier for this request
            car_brand: Car brand
            vin: Vehicle Identification Number
            license_plate: Vehicle license plate number
            damage_notes: Notes describing the damage
            image_urls: List of Cloudinary URLs for damage photos
            
        Returns:
            Dict with success status and details
        """
        try:
            import asyncio
            
            # Get all garages from Fix it table
            logger.info("⚡ Fetching garages from Airtable 'Fix it' table...")
            garages = self.airtable.get_fix_it_garages()
            
            if not garages:
                logger.error("❌ NO GARAGES FOUND IN FIX IT TABLE!")
                logger.error("❌ Please check:")
                logger.error("   1. Airtable base has a table named 'Fix it' (exact spelling)")
                logger.error("   2. Table contains garage records")
                logger.error("   3. Each garage has a valid Email field")
                return {
                    'success': False,
                    'error': 'No garages available in Fix it table',
                    'garages_contacted': 0
                }
            
            logger.info(f"✅ Found {len(garages)} garages in Fix it table")
            logger.info(f"📧 Sending quote requests to {len(garages)} garages in parallel batches...")
            
            # Send emails in parallel batches to avoid timeout
            # Process in batches of 10 to avoid overwhelming the email service
            BATCH_SIZE = 10
            successful_sends = 0
            failed_sends = 0
            
            # Split garages into batches
            for i in range(0, len(garages), BATCH_SIZE):
                batch = garages[i:i + BATCH_SIZE]
                logger.info(f"Processing batch {i//BATCH_SIZE + 1} of {(len(garages) + BATCH_SIZE - 1)//BATCH_SIZE} ({len(batch)} garages)")
                
                # Create tasks for parallel sending
                tasks = []
                for garage in batch:
                    task = self._send_garage_quote_request(
                        garage=garage,
                        request_id=request_id,
                        car_brand=car_brand,
                        vin=vin,
                        license_plate=license_plate,
                        damage_notes=damage_notes,
                        image_urls=image_urls
                    )
                    tasks.append(task)
                
                # Send all emails in this batch in parallel
                try:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Count successes and failures
                    for idx, result in enumerate(results):
                        garage = batch[idx]
                        if isinstance(result, Exception):
                            failed_sends += 1
                            logger.error(f"Error sending to {garage['name']}: {str(result)}")
                        elif result:
                            successful_sends += 1
                            logger.info(f"✅ Sent to {garage['name']} ({garage['email']})")
                        else:
                            failed_sends += 1
                            logger.error(f"❌ Failed to send to {garage['name']} ({garage['email']})")
                    
                    # Small delay between batches to avoid rate limiting
                    if i + BATCH_SIZE < len(garages):
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logger.error(f"Error processing batch: {str(e)}", exc_info=True)
                    failed_sends += len(batch)
            
            logger.info(f"✅ Quote requests sent: {successful_sends} successful, {failed_sends} failed out of {len(garages)} total")
            
            return {
                'success': True,
                'garages_contacted': successful_sends,
                'garages_failed': failed_sends,
                'total_garages': len(garages)
            }
            
        except Exception as e:
            logger.error(f"Error sending quote requests: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'garages_contacted': 0
            }
    
    async def _send_garage_quote_request(
        self,
        garage: Dict[str, Any],
        request_id: str,
        car_brand: str,
        vin: str,
        license_plate: str,
        damage_notes: str,
        image_urls: List[str]
    ) -> bool:
        """
        Send a quote request email to a single garage in English
        
        Args:
            garage: Garage information dict
            request_id: Unique request identifier
            car_brand: Car brand
            vin: Vehicle Identification Number
            license_plate: Vehicle license plate number
            damage_notes: Description of damage
            image_urls: List of image URLs
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            # Professional subject line with VIN for legitimacy and tracking
            subject = f"Repair Quote Request - VIN: {vin}"
            
            # Build embedded image section - show images directly in email
            images_html = ""
            if image_urls:
                images_html = '<div style="margin: 20px 0;"><p style="margin-bottom: 10px;"><strong>Damage Photos:</strong></p>'
                for i, url in enumerate(image_urls, 1):
                    images_html += f'''
                    <div style="margin: 15px 0;">
                        <p style="margin: 5px 0; font-size: 14px; color: #666;">Photo {i}:</p>
                        <img src="{url}" alt="Damage Photo {i}" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; display: block; margin-top: 5px;" />
                    </div>
                    '''
                images_html += '</div>'
            
            # Build damage description
            damage_description = damage_notes if damage_notes else "See attached photos"
            
            # Create plain text version for better deliverability
            plain_text = f"""
Good day,

I am writing to request a repair quotation for the following vehicle:

Vehicle Information:
Brand: {car_brand}
License Plate: {license_plate if license_plate else 'N/A'}
VIN: {vin}

Damage Details:
{damage_description}

{"Damage Photos: " + ", ".join([url for url in image_urls]) if image_urls else ""}

Please provide:
1. Estimated repair cost
2. Expected repair duration

Please reply to this email with your quotation at your earliest convenience.

Thank you for your time and assistance.

Best regards,
Garagefy Quote Service

Reference: {request_id}
            """
            
            html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
                <p>Good day,</p>
                
                <p>I am writing to request a repair quotation for the following vehicle:</p>
                
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <tr>
                        <td style="padding: 8px; font-weight: bold; width: 150px;">Vehicle Brand:</td>
                        <td style="padding: 8px;">{car_brand}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">License Plate:</td>
                        <td style="padding: 8px;">{license_plate if license_plate else 'N/A'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">VIN:</td>
                        <td style="padding: 8px;">{vin}</td>
                    </tr>
                </table>
                
                <p style="margin: 15px 0;">
                    <strong>Damage Details:</strong><br>
                    {damage_description}
                </p>
                
                {images_html}
                
                <p><strong>Please provide:</strong></p>
                <ol style="margin: 10px 0; padding-left: 20px;">
                    <li>Estimated repair cost</li>
                    <li>Expected repair duration</li>
                </ol>
                
                <p>Please reply to this email with your quotation at your earliest convenience.</p>
                
                <p>Thank you for your time and assistance.</p>
                
                <p>Best regards,<br>
                <strong>Garagefy Quote Service</strong></p>
                
                <div style="font-size: 11px; color: #888; margin-top: 25px; padding-top: 15px; border-top: 1px solid #ddd;">
                    <p>Reference ID: {request_id}</p>
                    <p>This is an automated quote request. Please reply directly to this email.</p>
                </div>
            </body>
            </html>
            """
            
            # Send the email with both HTML and plain text versions
            success = await self.email_service.send_email(
                to_emails=[garage['email']],
                subject=subject,
                html_content=html_content,
                text_content=plain_text
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending quote request to {garage.get('name', 'unknown')}: {str(e)}", exc_info=True)
            return False
    
    def _calculate_business_days_deadline(self, business_days: int) -> datetime:
        """
        Calculate deadline date excluding weekends
        
        Args:
            business_days: Number of business days from now
            
        Returns:
            datetime: Deadline date
        """
        current = datetime.now(timezone.utc)
        days_added = 0
        
        while days_added < business_days:
            current += timedelta(days=1)
            # Skip weekends (Saturday=5, Sunday=6)
            if current.weekday() < 5:
                days_added += 1
        
        return current

# Singleton instance
fix_it_service = FixItService()
