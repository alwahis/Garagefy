import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
from tqdm import tqdm
import sys

def get_coordinates(geolocator, address, max_retries=3):
    """Get latitude and longitude for an address using Nominatim with retry logic."""
    for attempt in range(max_retries):
        try:
            # Add 'Luxembourg' to the address if not present
            if 'luxembourg' not in address.lower():
                address += ', Luxembourg'
            # Add delay to respect Nominatim's usage policy
            time.sleep(1.5)  # Increased delay to avoid rate limiting
            location = geolocator.geocode(address, timeout=10)
            if location:
                return location.latitude, location.longitude
            return None, None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            if attempt == max_retries - 1:
                print(f"\nError geocoding {address}: {str(e)}")
                return None, None
            time.sleep(2)  # Wait longer before retrying
        except Exception as e:
            print(f"\nUnexpected error for {address}: {str(e)}")
            return None, None

def main():
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv('luxembourg_garages.csv')
    total_garages = len(df)
    print(f"Found {total_garages} garages to process")

    # Create new columns for coordinates if they don't exist
    if 'Latitude' not in df.columns:
        df['Latitude'] = None
    if 'Longitude' not in df.columns:
        df['Longitude'] = None

    # Initialize geolocator
    geolocator = Nominatim(user_agent="luxembourg_garages_bulk")

    # Process each address with progress bar
    print("\nFinding coordinates for each address...")
    processed = 0
    failed = 0
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing garages"):
        if pd.isna(df.at[idx, 'Latitude']) or pd.isna(df.at[idx, 'Longitude']):
            lat, lon = get_coordinates(geolocator, row['Address'])
            if lat and lon:
                df.at[idx, 'Latitude'] = lat
                df.at[idx, 'Longitude'] = lon
                processed += 1
            else:
                failed += 1
            
            # Save progress every 50 records
            if idx % 50 == 0:
                df.to_csv('luxembourg_garages_with_coordinates.csv', index=False)
                print(f"\nProgress saved. Processed: {processed}, Failed: {failed}")

    # Final save
    df.to_csv('luxembourg_garages_with_coordinates.csv', index=False)
    
    # Print summary
    print("\nProcess completed!")
    print(f"Total garages: {total_garages}")
    print(f"Successfully processed: {processed}")
    print(f"Failed to get coordinates: {failed}")
    
    # Check for missing coordinates
    missing_coords = df[df['Latitude'].isna() | df['Longitude'].isna()]
    if not missing_coords.empty:
        print("\nGarages with missing coordinates:")
        for _, row in missing_coords.iterrows():
            print(f"- {row['Name']}: {row['Address']}")

if __name__ == "__main__":
    main()
