import pandas as pd
import requests
import time
from tqdm import tqdm

def clean_address(address):
    """Clean and format the address."""
    if pd.isna(address):
        return None
    # Remove any extra whitespace
    address = ' '.join(address.split())
    # Ensure it ends with Luxembourg if not present
    if 'luxembourg' not in address.lower():
        address += ', Luxembourg'
    return address

def get_coordinates_photon(address, max_retries=3):
    """Get latitude and longitude using Photon geocoding service."""
    if pd.isna(address):
        return None, None
        
    base_url = "https://photon.komoot.io/api/"
    
    for attempt in range(max_retries):
        try:
            # Add delay to respect rate limits
            time.sleep(1)
            
            params = {
                'q': address,
                'limit': 1,
                'lang': 'en'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('features') and len(data['features']) > 0:
                    coordinates = data['features'][0]['geometry']['coordinates']
                    # Photon returns [lon, lat], we need to swap them
                    return coordinates[1], coordinates[0]
            
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait longer before retry
            
        except Exception as e:
            print(f"\nError geocoding {address}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return None, None

def main():
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv('luxembourg_garages_complete.csv')
    
    # Clean the data
    print("Cleaning data...")
    # Remove rows where both name and address are empty
    df = df.dropna(subset=['name', 'address'], how='all')
    
    # If name is empty but address exists, use first part of address as name
    df['name'] = df.apply(lambda row: row['address'].split(',')[0] if pd.isna(row['name']) else row['name'], axis=1)
    
    # Clean addresses
    df['clean_address'] = df['address'].apply(clean_address)
    
    # Remove duplicates based on clean_address
    df = df.drop_duplicates(subset=['clean_address'])
    
    # Remove rows where clean_address is None
    df = df.dropna(subset=['clean_address'])
    
    total_garages = len(df)
    print(f"Found {total_garages} unique garages to process")

    # Create new columns for coordinates if they don't exist
    if 'latitude' not in df.columns:
        df['latitude'] = None
    if 'longitude' not in df.columns:
        df['longitude'] = None

    # Process each address with progress bar
    print("\nFinding coordinates for each address...")
    processed = 0
    failed = 0
    
    try:
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing garages"):
            if pd.isna(df.at[idx, 'latitude']) or pd.isna(df.at[idx, 'longitude']):
                lat, lon = get_coordinates_photon(row['clean_address'])
                if lat and lon:
                    df.at[idx, 'latitude'] = lat
                    df.at[idx, 'longitude'] = lon
                    processed += 1
                else:
                    failed += 1
                
                # Save progress every 50 records
                if (idx + 1) % 50 == 0:
                    df.to_csv('luxembourg_garages_geocoded.csv', index=False)
                    print(f"\nProgress saved. Processed successfully: {processed}, Failed: {failed}")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Saving progress...")
    finally:
        # Final save
        df.to_csv('luxembourg_garages_geocoded.csv', index=False)
        
        # Print summary
        print("\nProcess completed!")
        print(f"Total unique garages: {total_garages}")
        print(f"Successfully processed: {processed}")
        print(f"Failed to get coordinates: {failed}")
        
        # Check for missing coordinates
        missing_coords = df[df['latitude'].isna() | df['longitude'].isna()]
        if not missing_coords.empty:
            print("\nGarages with missing coordinates:")
            missing_file = 'missing_coordinates.txt'
            with open(missing_file, 'w') as f:
                for _, row in missing_coords.iterrows():
                    line = f"- {row['name']}: {row['clean_address']}\n"
                    f.write(line)
                    print(line.rstrip())
            print(f"\nList of garages with missing coordinates saved to {missing_file}")

if __name__ == "__main__":
    main()
