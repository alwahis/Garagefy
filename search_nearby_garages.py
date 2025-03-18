import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def get_user_coordinates(address):
    """Get coordinates for user's location."""
    try:
        geolocator = Nominatim(user_agent="garagefy")
        if 'luxembourg' not in address.lower():
            address += ', Luxembourg'
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Error finding your location: {str(e)}")
        return None, None

def find_nearby_garages(user_lat, user_lon, df, max_distance=10):
    """Find garages within max_distance kilometers of user's location."""
    nearby_garages = []
    
    for _, garage in df.iterrows():
        if pd.notna(garage['latitude']) and pd.notna(garage['longitude']):
            distance = geodesic(
                (user_lat, user_lon),
                (garage['latitude'], garage['longitude'])
            ).kilometers
            
            if distance <= max_distance:
                nearby_garages.append({
                    'name': garage['name'],
                    'address': garage['address'],
                    'distance': round(distance, 2),
                    'phone': garage['phone'],
                    'rating': garage['rating'],
                    'hours': garage['hours']
                })
    
    # Sort by distance
    return sorted(nearby_garages, key=lambda x: x['distance'])

def main():
    # Load garage data
    try:
        df = pd.read_csv('luxembourg_garages_with_coords.csv')
    except FileNotFoundError:
        print("Error: Could not find garage data with coordinates. Please run add_coordinates.py first.")
        return
    
    while True:
        # Get user location
        address = input("\nEnter your location (or 'quit' to exit): ")
        if address.lower() == 'quit':
            break
            
        # Get max distance
        try:
            max_distance = float(input("Enter maximum distance in kilometers (default: 10): ") or 10)
        except ValueError:
            max_distance = 10
            print("Invalid input, using default distance of 10 km")
        
        # Get user coordinates
        user_lat, user_lon = get_user_coordinates(address)
        if not user_lat or not user_lon:
            print("Could not find your location. Please try a different address.")
            continue
        
        # Find nearby garages
        nearby = find_nearby_garages(user_lat, user_lon, df, max_distance)
        
        if not nearby:
            print(f"\nNo garages found within {max_distance} km of your location.")
        else:
            print(f"\nFound {len(nearby)} garages within {max_distance} km:")
            for i, garage in enumerate(nearby, 1):
                print(f"\n{i}. {garage['name'] or 'Unnamed Garage'}")
                print(f"   Distance: {garage['distance']} km")
                print(f"   Address: {garage['address']}")
                if garage['phone']:
                    print(f"   Phone: {garage['phone']}")
                if garage['rating']:
                    print(f"   Rating: {garage['rating']}")
                if garage['hours']:
                    print(f"   Hours: {garage['hours']}")

if __name__ == "__main__":
    main()
