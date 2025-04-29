import requests
import os

# Set your Google Maps API key in the .env file and load it here
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')  # TODO: Fill in your API key

# Example: Geocoding API
GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def geocode_address(address):
    """
    Given a string address, return geocoded latitude and longitude using Google Maps API.
    """
    if not GOOGLE_MAPS_API_KEY:
        raise ValueError('Google Maps API key not set.')
    params = {'address': address, 'key': GOOGLE_MAPS_API_KEY}
    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code != 200:
        raise Exception('Failed to contact Google Maps API')
    data = response.json()
    if data.get('status') != 'OK':
        raise Exception(f"Google Maps API error: {data.get('status')}")
    location = data['results'][0]['geometry']['location']
    return location['lat'], location['lng']

# You can add more functions for Place Details, Reverse Geocoding, etc.
# Example usage (in your route):
#   from app.utils.google_maps import geocode_address
#   lat, lng = geocode_address('Boston, MA')