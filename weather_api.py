import requests
from config import API_KEY, BASE_URL

def get_weather(location):
    """Fetch weather data for a given location"""
    try:
        params = {
            'q': location,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None