from datetime import datetime
import os

from helpers.api_key_loader import APIKeyLoader

# Class to load URLs for OpenWeather and Google Air Quality APIs
class URLLoader:

    # Function to load the OpenWeather API URL
    @staticmethod
    def load_openweather_url(lat: float, lon: float, isHistory: bool, timestamp: int) -> str:
        count = 10
        api_key = APIKeyLoader.load_openweather_api_key()
        if isHistory:
            return f"https://api.openweathermap.org/data/4.0/onecall/timeline/1day?cnt={count}&lat={lat}&lon={lon}&start={timestamp}&appid={api_key}"
        else:
            return f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"


    # Function to load the Google Air Quality API URL
    @staticmethod
    def load_airquality_url(urlType: str = "current") -> str:
        api_key = APIKeyLoader.load_google_cloud_api_key()

        if urlType == "historical":
            print(f"URLLOADER: Calling historical air quality URL with API key: {api_key}")
            return f"https://airquality.googleapis.com/v1/history:lookup?key={api_key}"
        elif urlType == "forecast":
            print(f"URLLOADER: Calling forecast air quality URL with API key: {api_key}")
            return f"https://airquality.googleapis.com/v1/forecast:lookup?key={api_key}"

        print(f"URLLOADER: Calling current air quality URL with API key: {api_key}")
        return f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
