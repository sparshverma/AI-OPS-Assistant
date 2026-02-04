import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str):
    """
    Fetches the current weather for a specific city.
    
    Args:
        city (str): The name of the city.
        
    Returns:
        dict: A dictionary containing temperature, condition, and city name, or an error message.
    """
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY not found in environment variables."}
        
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric" # Default to Celsius
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data.get("name"),
            "temperature_c": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            return {"error": f"City '{city}' not found."}
        return {"error": f"Weather API Error: {err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
