from pdf2image import convert_from_path
import pytesseract
import csv
import re
from pathlib import Path
import tempfile
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using OCR."""
    print("Converting PDF to images...")
    images = convert_from_path(pdf_path)
    
    print("Performing OCR on images...")
    text = ""
    for i, image in enumerate(images):
        print(f"Processing page {i+1}/{len(images)}")
        text += pytesseract.image_to_string(image)
    
    return text

def clean_text(text):
    """Clean and normalize text."""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s\-\.,@]', '', text)
    return text.strip()

def parse_garage_info(text):
    """Parse garage information from text."""
    garages = []
    
    # Split text into lines and clean up
    lines = [clean_text(line) for line in text.split('\n') if clean_text(line)]
    
    current_garage = None
    description_buffer = []
    
    for line in lines:
        # Start of a new garage entry (contains postal code or looks like a business name)
        if re.search(r'L-\d{4}', line) or (not current_garage and (
            re.search(r'(?:Garage|Auto|Car|Motors?|Service)', line, re.IGNORECASE) or
            len(line.split()) <= 4
        )):
            # Save previous garage if exists
            if current_garage and any(current_garage.values()):
                # Process description buffer
                if description_buffer:
                    desc = ' '.join(description_buffer)
                    if not current_garage['services']:
                        current_garage['services'] = desc
                    else:
                        current_garage['additional'] = desc
                    description_buffer = []
                garages.append(current_garage)
            
            current_garage = {
                'name': '',
                'address': '',
                'phone': '',
                'email': '',
                'website': '',
                'hours': '',
                'services': '',
                'brands': '',
                'languages': '',
                'payment': '',
                'rating': '',
                'reviews': '',
                'additional': ''
            }
            
            # Try to extract address
            address_match = re.search(r'.*(?:L-\d{4})\s+[\w\s\-]+(?:,\s*Luxembourg)?', line)
            if address_match:
                current_garage['address'] = address_match.group(0)
            elif not re.search(r'\d{2}\s*\d{2}\s*\d{2}', line):  # Not a phone number
                current_garage['name'] = line
        
        elif current_garage:
            # Phone number
            if re.search(r'(?:\+352|00352)?\s*\d{2}\s*\d{2}\s*\d{2}(?:\s*-\s*\d{1,2})?', line):
                current_garage['phone'] = line
            
            # Email
            elif re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line):
                current_garage['email'] = line
            
            # Website
            elif re.search(r'www\.[\w\.-]+\.\w+', line):
                current_garage['website'] = line
            
            # Hours (typically contains time patterns)
            elif re.search(r'\d{1,2}[h:]\d{2}', line.lower()) or any(day in line.lower() for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']):
                hours = re.sub(r'Closed\s*-\s*Open\s*', '', line)
                current_garage['hours'] = current_garage['hours'] + ' ' + hours if current_garage['hours'] else hours
            
            # Rating and reviews
            elif re.search(r'\d+(\.\d+)?(/5)?', line):
                if 'rating' in line.lower() or len(line.strip()) <= 3:
                    rating_match = re.search(r'\d+(\.\d+)?', line)
                    if rating_match:
                        current_garage['rating'] = rating_match.group(0)
                elif any(word in line.lower() for word in ['reviews', 'avis']):
                    reviews_match = re.search(r'\d+', line)
                    if reviews_match:
                        current_garage['reviews'] = reviews_match.group(0)
            
            # Car brands
            elif any(brand in line for brand in ['Volkswagen', 'Audi', 'BMW', 'Mercedes', 'Peugeot', 'Renault', 'Toyota', 'Citroen', 'Ford', 'Opel']):
                current_garage['brands'] = line
            
            # Languages
            elif any(lang in line for lang in ['French', 'German', 'English', 'Luxembourgish', 'français', 'deutsch', 'anglais', 'luxembourgeois']):
                current_garage['languages'] = line
            
            # Payment methods
            elif any(payment in line.lower() for payment in ['cash', 'card', 'credit', 'debit', 'transfer', 'payment']):
                current_garage['payment'] = line
            
            # Services or description
            elif len(line.split()) > 3:
                if 'service' in line.lower() or 'repair' in line.lower() or 'maintenance' in line.lower():
                    current_garage['services'] = line
                else:
                    description_buffer.append(line)
    
    # Add the last garage if exists
    if current_garage and any(current_garage.values()):
        if description_buffer:
            desc = ' '.join(description_buffer)
            if not current_garage['services']:
                current_garage['services'] = desc
            else:
                current_garage['additional'] = desc
        garages.append(current_garage)
    
    # Post-process: clean up and merge fragmented entries
    cleaned_garages = []
    for i, garage in enumerate(garages):
        # Skip empty entries
        if not any(garage.values()):
            continue
        
        # If this entry only has an address and the previous entry only has a name, merge them
        if i > 0 and garage['address'] and not garage['name'] and cleaned_garages[-1]['name'] and not cleaned_garages[-1]['address']:
            cleaned_garages[-1]['address'] = garage['address']
            continue
        
        # Clean up hours format
        if garage['hours']:
            garage['hours'] = re.sub(r'Closed\s*-\s*Open\s*', '', garage['hours'])
            garage['hours'] = re.sub(r'\s+', ' ', garage['hours'])
        
        cleaned_garages.append(garage)
    
    return cleaned_garages

def write_to_csv(garages, output_file):
    """Write garage information to CSV file."""
    fieldnames = ['name', 'address', 'phone', 'email', 'website', 'hours', 
                 'services', 'brands', 'languages', 'payment', 'rating', 
                 'reviews', 'additional']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(garages)

def main():
    # File paths
    pdf_path = Path(__file__).parent / 'pdf24_images_merged.pdf'
    csv_path = Path(__file__).parent / 'luxembourg_garages_complete.csv'
    
    print(f"Reading PDF file: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    print("Parsing garage information...")
    garages = parse_garage_info(text)
    
    print(f"Found {len(garages)} garages")
    print(f"Writing to CSV file: {csv_path}")
    write_to_csv(garages, csv_path)
    
    print("Done!")

if __name__ == '__main__':
    main()
