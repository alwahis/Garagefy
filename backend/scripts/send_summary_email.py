import os
import asyncio
import aiohttp
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys

# Set up paths
from scripts import setup_paths
setup_paths()

# Import services
from services.airtable_service import AirtableService
from services.email_service import EmailService

load_dotenv()

class SummaryEmailService:
    def __init__(self):
        self.airtable = AirtableService()
        self.email_service = EmailService()
        self.processed_vins_file = 'processed_summary_vins.txt'

    def load_processed_vins(self):
        try:
            with open(self.processed_vins_file, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()

    def save_processed_vin(self, vin):
        with open(self.processed_vins_file, 'a') as f:
            f.write(f"{vin}\n")

    async def get_garage_responses(self, vin):
        # Get all responses for this VIN
        table = self.airtable._get_table('Recevied email')
        responses = table.all(formula=f"{{VIN}} = '{vin}'")
        
        # Get all garages that should have responded
        garages_table = self.airtable._get_table('Fix it Garages')
        all_garages = garages_table.all()
        
        return responses, all_garages

    async def check_and_send_summary(self):
        try:
            # Get all unique VINs with responses
            table = self.airtable._get_table('Recevied email')
            vins = set(record['fields'].get('VIN', '') for record in table.all())
            
            for vin in vins:
                if not vin:
                    continue
                    
                # Skip if we've already sent a summary for this VIN
                processed_vins = self.load_processed_vins()
                if vin in processed_vins:
                    continue
                
                responses, all_garages = await self.get_garage_responses(vin)
                
                # Check if all garages have responded
                garage_emails = {g['fields'].get('Email', '').lower() for g in all_garages 
                               if g['fields'].get('Email')}
                responder_emails = {r['fields'].get('Email', '').lower() 
                                  for r in responses if r['fields'].get('Email')}
                
                if garage_emails.issubset(responder_emails):
                    # All garages have responded, send summary
                    await self.send_summary_email(vin, responses, all_garages)
                    self.save_processed_vin(vin)
                    
        except Exception as e:
            print(f"Error in check_and_send_summary: {e}")

    async def send_summary_email(self, vin, responses, all_garages):
        try:
            # Get original request details (you may need to adjust this based on your schema)
            customer_table = self.airtable._get_table('Customer details')
            customer_record = customer_table.first(formula=f"{{VIN}} = '{vin}'")
            
            if not customer_record:
                print(f"No customer record found for VIN: {vin}")
                return
                
            customer_email = customer_record['fields'].get('Email')
            if not customer_email:
                print(f"No email found for customer with VIN: {vin}")
                return
            
            # Prepare response data
            response_data = []
            for response in responses:
                garage_email = response['fields'].get('Email', '').lower()
                garage = next((g for g in all_garages 
                             if g['fields'].get('Email', '').lower() == garage_email), None)
                
                if garage:
                    response_data.append({
                        'garage_name': garage['fields'].get('Name', 'Unknown Garage'),
                        'email': garage_email,
                        'phone': garage['fields'].get('Phone', 'N/A'),
                        'address': garage['fields'].get('Address', 'N/A'),
                        'response': response['fields'].get('Body', 'No response text'),
                        'response_date': response['fields'].get('Received At', 'N/A')
                    })
            
            # Generate HTML email
            subject = f"Your Repair Quote Summary for VIN: {vin}"
            
            # Create HTML table of responses
            table_rows = ""
            for idx, resp in enumerate(response_data, 1):
                table_rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{resp['garage_name']}</td>
                    <td>{resp['phone']}</td>
                    <td>{resp['address']}</td>
                    <td>{resp['response'][:200]}...</td>
                    <td>{resp['response_date']}</td>
                </tr>
                """
            
            html_content = f"""
            <html>
            <head>
                <style>
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                </style>
            </head>
            <body>
                <h2>Your Repair Quote Summary</h2>
                <p>Hello,</p>
                <p>Here are the responses we've received from garages regarding your vehicle (VIN: {vin}):</p>
                
                <table>
                    <tr>
                        <th>#</th>
                        <th>Garage</th>
                        <th>Phone</th>
                        <th>Address</th>
                        <th>Response</th>
                        <th>Response Date</th>
                    </tr>
                    {table_rows}
                </table>
                
                <p>Please contact the garages directly for more details or to schedule service.</p>
                
                <p>Best regards,<br>The Garagefy Team</p>
            </body>
            </html>
            """.format(vin=vin, table_rows=table_rows)
            
            # Send email
            await self.email_service.send_email(
                to_email=customer_email,
                subject=subject,
                html_content=html_content
            )
            
            print(f"Sent summary email for VIN: {vin} to {customer_email}")
            
        except Exception as e:
            print(f"Error sending summary email for VIN {vin}: {e}")

async def main():
    service = SummaryEmailService()
    await service.check_and_send_summary()

if __name__ == "__main__":
    asyncio.run(main())
