import pandas as pd
from geopy.geocoders import Nominatim
import time

def get_coordinates(address):
    """Get latitude and longitude for an address using Nominatim."""
    try:
        geolocator = Nominatim(user_agent="my_garage_app")
        # Add 'Luxembourg' to the address if not present
        if 'luxembourg' not in address.lower():
            address += ', Luxembourg'
        # Add delay to respect Nominatim's usage policy
        time.sleep(1)
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {str(e)}")
        return None, None

# Read the CSV file
df = pd.read_csv('luxembourg_garages.csv')

# Create new columns for coordinates
df['Latitude'] = None
df['Longitude'] = None

# Process each address
print("Finding coordinates for each address...")
for idx, row in df.iterrows():
    print(f"Processing: {row['Name']} - {row['Address']}")
    lat, lon = get_coordinates(row['Address'])
    df.at[idx, 'Latitude'] = lat
    df.at[idx, 'Longitude'] = lon

# Save the updated data
df.to_csv('luxembourg_garages_with_coordinates.csv', index=False)
print("Done! Saved to luxembourg_garages_with_coordinates.csv")
