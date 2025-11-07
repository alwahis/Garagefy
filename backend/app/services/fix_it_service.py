import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta, timezone
from .airtable_service import airtable_service
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
            # Get all garages from Fix it table
            garages = self.airtable.get_fix_it_garages()
            
            if not garages:
                logger.warning("No garages found in Fix it table")
                return {
                    'success': False,
                    'error': 'No garages available',
                    'garages_contacted': 0
                }
            
            logger.info(f"Sending quote requests to {len(garages)} garages")
            
            # Send email to each garage
            successful_sends = 0
            failed_sends = 0
            
            for garage in garages:
                try:
                    success = await self._send_garage_quote_request(
                        garage=garage,
                        request_id=request_id,
                        car_brand=car_brand,
                        vin=vin,
                        license_plate=license_plate,
                        damage_notes=damage_notes,
                        image_urls=image_urls
                    )
                    
                    if success:
                        successful_sends += 1
                        logger.info(f"Successfully sent quote request to {garage['name']} ({garage['email']})")
                    else:
                        failed_sends += 1
                        logger.error(f"Failed to send quote request to {garage['name']} ({garage['email']})")
                        
                except Exception as e:
                    failed_sends += 1
                    logger.error(f"Error sending quote request to {garage['name']}: {str(e)}", exc_info=True)
            
            logger.info(f"Quote requests sent: {successful_sends} successful, {failed_sends} failed")
            
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
            # Build friendly, human-like email content in English
            subject = f"Quote Request - {car_brand} Repair"
            
            # Build embedded image section
            images_html = ""
            if image_urls:
                images_html = '<div style="margin: 15px 0;">'
                for i, url in enumerate(image_urls, 1):
                    images_html += f'<div style="margin-bottom: 10px;"><img src="{url}" alt="Damage photo {i}" style="max-width: 100%; height: auto; border-radius: 5px;" /></div>'
                images_html += "</div>"
            
            # Build damage description
            damage_description = damage_notes if damage_notes else "Please see photos for details"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <p>Hi there,</p>
                    
                    <p>I hope this email finds you well. I'm reaching out to get a quote for repairing my car.</p>
                    
                    <p><strong>Vehicle Details:</strong></p>
                    <ul style="list-style: none; padding-left: 0;">
                        <li>🚗 <strong>Brand:</strong> {car_brand}</li>
                        <li>🔢 <strong>License Plate:</strong> {license_plate if license_plate else 'Not provided'}</li>
                        <li>🆔 <strong>VIN:</strong> {vin}</li>
                    </ul>
                    
                    <p><strong>Damage Description:</strong><br>{damage_description}</p>
                    
                    {images_html}
                    
                    <p>Could you please provide me with:</p>
                    <ul>
                        <li>An estimated cost for the repair</li>
                        <li>How long the repair would take</li>
                    </ul>
                    
                    <p>Just reply to this email with your quote whenever you get a chance. I appreciate your help!</p>
                    
                    <p>Thanks so much,<br>Best regards</p>
                    
                    <p style="font-size: 12px; color: #666; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                        <em>Ref: {request_id}</em><br>
                        Sent via Garagefy
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Send the email
            success = await self.email_service.send_email(
                to_emails=[garage['email']],
                subject=subject,
                html_content=html_content
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
