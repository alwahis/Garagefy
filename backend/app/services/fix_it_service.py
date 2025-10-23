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
        damage_notes: str,
        image_urls: List[str]
    ) -> Dict[str, Any]:
        """
        Send quote requests to all garages in the Fix it table
        
        Args:
            request_id: Unique identifier for this request
            car_brand: Car brand
            vin: Vehicle Identification Number
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
        damage_notes: str,
        image_urls: List[str]
    ) -> bool:
        """
        Send a quote request email to a single garage in French
        
        Args:
            garage: Garage information dict
            request_id: Unique request identifier
            car_brand: Car brand
            vin: Vehicle Identification Number
            damage_notes: Description of damage
            image_urls: List of image URLs
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            # Calculate response deadline (2 business days)
            deadline = self._calculate_business_days_deadline(2)
            
            # Build French email content
            subject = f"🚗 Demande de devis - {car_brand} (Ref: {request_id})"
            
            # Build embedded image section
            images_html = ""
            if image_urls:
                images_html = '<div style="margin: 20px 0;"><h3 style="color: #0078D4; margin-bottom: 15px;">📸 Photos des dommages:</h3>'
                for i, url in enumerate(image_urls, 1):
                    images_html += f'''
                    <div style="margin-bottom: 15px;">
                        <img src="{url}" alt="Dommage photo {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />
                        <p style="font-size: 12px; color: #666; margin-top: 5px;">Photo {i}</p>
                    </div>
                    '''
                images_html += "</div>"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 650px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%); padding: 30px 20px; text-align: center;">
                        <h1 style="color: #0078D4; margin: 0; font-size: 28px; font-weight: bold;">Garagefy</h1>
                        <p style="color: #1A202C; margin: 10px 0 0 0; font-size: 16px;">Nouvelle demande de devis</p>
                    </div>
                    
                    <div style="padding: 30px 20px;">
                        <p style="font-size: 16px; margin-bottom: 20px;">Bonjour <strong>{garage['name']}</strong>,</p>
                        
                        <!-- Vehicle Info Box -->
                        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 8px; border-left: 4px solid #0078D4; margin: 20px 0;">
                            <h3 style="color: #0078D4; margin-top: 0;">📋 Informations du véhicule</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px 0; font-weight: bold; width: 140px;">Marque:</td>
                                    <td style="padding: 8px 0;">{car_brand}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: bold;">VIN:</td>
                                    <td style="padding: 8px 0; font-family: monospace; font-size: 14px;">{vin}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: bold; vertical-align: top;">Description:</td>
                                    <td style="padding: 8px 0;">{damage_notes if damage_notes else "Non spécifié"}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; font-weight: bold;">Référence:</td>
                                    <td style="padding: 8px 0;"><code style="background: #e2e8f0; padding: 4px 8px; border-radius: 4px;">{request_id}</code></td>
                                </tr>
                            </table>
                        </div>
                        
                        {images_html}
                        
                        <!-- Deadline Box -->
                        <div style="background-color: #FFF5E1; padding: 20px; border-radius: 8px; border-left: 4px solid #F59E0B; margin: 20px 0;">
                            <p style="margin: 0; font-size: 16px;"><strong>⏰ Répondre avant le:</strong> <span style="color: #C05621; font-weight: bold;">{deadline.strftime('%d/%m/%Y à %H:%M')}</span></p>
                            <p style="margin: 10px 0 0 0; font-size: 14px; color: #666;">Délai: 2 jours ouvrables</p>
                        </div>
                        
                        <!-- Action Required -->
                        <div style="background-color: #0078D4; color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: white;">💼 Répondez simplement à cet email avec:</h3>
                            <ul style="margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                                <li style="margin: 8px 0;"><strong>Coût de réparation:</strong> Prix total estimé</li>
                                <li style="margin: 8px 0;"><strong>Délai nécessaire:</strong> Temps pour effectuer la réparation</li>
                                <li style="margin: 8px 0;"><strong>Notes:</strong> (optionnel) Toute clarification nécessaire</li>
                            </ul>
                        </div>
                        
                        <p style="margin-top: 30px; color: #666; font-size: 14px;">Cordialement,<br><strong>L'équipe Garagefy</strong></p>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f7fafc; padding: 20px; text-align: center; font-size: 12px; color: #718096;">
                        <p style="margin: 0;">📧 Répondez directement à cet email avec votre devis</p>
                        <p style="margin: 10px 0 0 0;">Garagefy - Plateforme de comparaison de devis carrosserie</p>
                    </div>
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
