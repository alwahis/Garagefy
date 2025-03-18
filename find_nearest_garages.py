import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
from typing import List, Tuple, Dict
import json

class GarageLocator:
    def __init__(self, garages_file: str):
        """Initialize with the path to the garages CSV file."""
        self.df = pd.read_csv(garages_file)
        self.geolocator = Nominatim(user_agent="garagefy_search")
        
    def get_user_coordinates(self, address: str) -> Tuple[float, float]:
        """Get coordinates for a given address."""
        try:
            # Add Luxembourg to the address if not present
            if 'luxembourg' not in address.lower():
                address += ', Luxembourg'
            # Add delay to respect Nominatim's usage policy
            time.sleep(1)
            location = self.geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            return None, None
        except Exception as e:
            print(f"Error finding your location: {str(e)}")
            return None, None

    def find_nearest_garages(self, user_lat: float, user_lon: float, 
                           max_distance: float = 10.0, limit: int = 5) -> List[Dict]:
        """Find the nearest garages within max_distance kilometers."""
        if user_lat is None or user_lon is None:
            return []

        # Calculate distances for all garages
        distances = []
        for _, garage in self.df.iterrows():
            if pd.notna(garage['latitude']) and pd.notna(garage['longitude']):
                distance = geodesic(
                    (user_lat, user_lon),
                    (garage['latitude'], garage['longitude'])
                ).kilometers

                if distance <= max_distance:
                    garage_info = {
                        'name': garage['name'],
                        'address': garage['clean_address'],
                        'distance': round(distance, 2),
                        'coordinates': (garage['latitude'], garage['longitude'])
                    }
                    
                    # Add optional fields if they exist and are not empty
                    for field in ['phone', 'email', 'website', 'hours', 'services']:
                        if field in garage and pd.notna(garage[field]):
                            garage_info[field] = garage[field]
                    
                    distances.append(garage_info)

        # Sort by distance and return the nearest ones
        return sorted(distances, key=lambda x: x['distance'])[:limit]

def format_garage_info(garage: Dict) -> str:
    """Format garage information for display."""
    info = [
        f"📍 {garage['name']}",
        f"📏 Distance: {garage['distance']} km",
        f"🏠 Address: {garage['address']}"
    ]
    
    if 'phone' in garage:
        info.append(f"📞 Phone: {garage['phone']}")
    if 'email' in garage:
        info.append(f"📧 Email: {garage['email']}")
    if 'website' in garage:
        info.append(f"🌐 Website: {garage['website']}")
    if 'hours' in garage:
        info.append(f"🕒 Hours: {garage['hours']}")
    if 'services' in garage:
        info.append(f"🔧 Services: {garage['services']}")
    
    return '\n'.join(info)

def main():
    # Initialize the garage locator
    locator = GarageLocator('luxembourg_garages_geocoded.csv')
    
    while True:
        # Get user's address
        print("\nEnter your address in Luxembourg (or 'quit' to exit):")
        address = input().strip()
        
        if address.lower() == 'quit':
            break
        
        # Get coordinates for the address
        print("\nFinding your location...")
        user_lat, user_lon = locator.get_user_coordinates(address)
        
        if user_lat is None or user_lon is None:
            print("❌ Sorry, couldn't find your location. Please try a different address.")
            continue
        
        # Find nearest garages
        print("\nSearching for nearby garages...")
        nearest_garages = locator.find_nearest_garages(user_lat, user_lon)
        
        if not nearest_garages:
            print("❌ No garages found within 10 km of your location.")
        else:
            print("\n🔍 Found these garages near you:\n")
            for i, garage in enumerate(nearest_garages, 1):
                print(f"\n--- Garage #{i} ---")
                print(format_garage_info(garage))

if __name__ == "__main__":
    main()
