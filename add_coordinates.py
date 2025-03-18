import pandas as pd
import requests
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_coordinates(address):
    """Get latitude and longitude for an address using Nominatim."""
    try:
        geolocator = Nominatim(user_agent="garagefy")
        # Add 'Luxembourg' to the address if not present
        if 'luxembourg' not in address.lower():
            address += ', Luxembourg'
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except (GeocoderTimedOut, Exception) as e:
        print(f"Error geocoding {address}: {str(e)}")
        return None, None

def main():
    # Read the CSV file
    df = pd.read_csv('luxembourg_garages_complete.csv')
    
    # Add latitude and longitude columns if they don't exist
    if 'latitude' not in df.columns:
        df['latitude'] = None
    if 'longitude' not in df.columns:
        df['longitude'] = None
    
    # Get coordinates for each garage
    for idx, row in df.iterrows():
        if pd.isna(row['latitude']) or pd.isna(row['longitude']):
            if pd.notna(row['address']):
                lat, lon = get_coordinates(row['address'])
                if lat and lon:
                    df.at[idx, 'latitude'] = lat
                    df.at[idx, 'longitude'] = lon
                    print(f"Added coordinates for: {row['address']}")
                else:
                    print(f"Could not find coordinates for: {row['address']}")
            time.sleep(1)  # Be nice to the geocoding service
    
    # Save the updated CSV
    df.to_csv('luxembourg_garages_with_coords.csv', index=False)
    print("Done! Updated CSV saved as luxembourg_garages_with_coords.csv")

if __name__ == "__main__":
    main()
