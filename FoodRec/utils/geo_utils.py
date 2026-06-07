from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import streamlit as st

@st.cache_resource
def get_geocoder():
    """Initialize Nominatim geocoder with a custom user agent."""
    return Nominatim(user_agent="food_rec_app_trae")

def get_coordinates(address):
    """Get latitude and longitude from address using Nominatim."""
    try:
        geocoder = get_geocoder()
        location = geocoder.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return None, None

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in KM between two points."""
    try:
        return geodesic((lat1, lon1), (lat2, lon2)).km
    except:
        return float('inf')

def get_user_location():
    """Default user location if geolocation is not available."""
    # Bhubaneswar coordinates as default
    return 20.2961, 85.8245
