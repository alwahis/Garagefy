import requests
import csv
import json
import time
from typing import List, Dict

API_KEY = 'fc-1c87a620a94c43fc82cfa64c636a4279'
URL = 'https://www.editus.lu/en/results/vehicle-maintenance/garage-1101r'

def scrape_garages() -> List[Dict]:
    # Initialize Firecrawl API endpoint
    api_url = 'https://app.firecrawl.io/api/scrape'
    
    # Configure the scraping parameters
    payload = {
        'url': URL,
        'selectors': {
            'garages': {
                'selector': '.result-item',
                'type': 'list',
                'data': {
                    'name': '.company-name',
                    'address': '.address',
                    'phone': '.phone',
                    'website': {
                        'selector': '.website a',
                        'attribute': 'href'
                    },
                    'email': '.email',
                    'opening_hours': '.opening-hours',
                    'services': '.services',
                    'rating': '.rating',
                    'reviews_count': '.reviews-count'
                }
            }
        }
    }
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"Making API request to {api_url}...")
        response = requests.post(api_url, json=payload, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        print(f"Response data: {json.dumps(data, indent=2)}")
        
        if 'data' in data and 'garages' in data['data']:
            return data['data']['garages']
        else:
            print("No garage data found in response")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def save_to_csv(garages: List[Dict], filename: str = 'luxembourg_garages.csv'):
    # Define CSV headers based on the data structure
    fieldnames = [
        'name', 'address', 'phone', 'email', 'website',
        'opening_hours', 'services', 'rating', 'reviews_count'
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write garage data
            for garage in garages:
                writer.writerow(garage)
                
        print(f"Successfully saved data to {filename}")
        
    except IOError as e:
        print(f"Error saving to CSV: {e}")

def main():
    print("Starting garage data scraping...")
    garages = scrape_garages()
    
    if garages:
        print(f"Found {len(garages)} garages")
        save_to_csv(garages)
    else:
        print("No garage data to save")

if __name__ == "__main__":
    main()
