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
            # Professional subject line with VIN for legitimacy and tracking
            subject = f"Repair Quote Request - VIN: {vin}"
            
            # Build embedded image section
            images_html = ""
            if image_urls:
                images_html = '<p style="margin: 15px 0;"><strong>Damage Photos:</strong></p>'
                for i, url in enumerate(image_urls, 1):
                    images_html += f'<p style="margin: 8px 0;"><a href="{url}" style="color: #0066cc; text-decoration: none;">View Photo {i}</a></p>'
            
            # Build damage description
            damage_description = damage_notes if damage_notes else "See attached photos"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
                <p>Good day,</p>
                
                <p>I am writing to request a repair quotation for the following vehicle:</p>
                
                <p style="margin: 12px 0;">
                    <strong>Vehicle Information:</strong><br>
                    Brand: {car_brand}<br>
                    License Plate: {license_plate if license_plate else 'N/A'}<br>
                    VIN: {vin}
                </p>
                
                <p style="margin: 12px 0;">
                    <strong>Damage Details:</strong><br>
                    {damage_description}
                </p>
                
                {images_html}
                
                <p>Please provide:</p>
                <p style="margin-left: 20px;">
                    1. Estimated repair cost<br>
                    2. Expected repair duration
                </p>
                
                <p>Please reply to this email with your quotation at your earliest convenience.</p>
                
                <p>Thank you for your time and assistance.</p>
                
                <p>Best regards</p>
                
                <p style="font-size: 11px; color: #888; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd;">
                    Reference: {request_id}
                </p>
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
