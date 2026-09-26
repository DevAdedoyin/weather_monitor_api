import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
import time
from openai import OpenAI

from constants.system_prompt_constants import SystemPrompt



class LocationSearchTool:

    @staticmethod
    def location_search_tool():
        """Tool for searching weather information based on location."""
        return {
            "name": "location_search",
            "description": "Search for weather information based on a location name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of the location to search for weather information.",
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            },
        }


    @staticmethod
    def search_weather_for_location(location: str) -> dict[str, str | float | None]:
        """Resolve a place name to coordinates using OpenWeather geocoding."""

        load_dotenv()

        location = location.strip()
        if not location:
            raise ValueError("Location must not be empty")

        api_key = os.getenv("OPEN_WEATHER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENWEATHER_API_KEY is not configured")

        # instantiate a new Nominatim client
        app = Nominatim(user_agent="weather_monitor_api")

        # Geocoding API to get coordinates


        time.sleep(1)

        location = app.geocode(location).raw

        lat = location["lat"]
        lon = location["lon"]

        # Weather API to get weather information
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
        with urlopen(url, timeout=10) as response:
            results = json.loads(response.read().decode("utf-8"))

        if not results:
            raise LookupError(f"No weather data found for location: {location}")

        return results



    async def search_location_weather_chat(user_prompt :str):
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        openai_client = OpenAI(api_key=openai_api_key)

        tools = [{"type": "function", "function": LocationSearchTool.location_search_tool()}]
        messages = [
                {
                    "role": "user",
                    "content": user_prompt,
                },
                {
                    "role": "system",
                    "content": SystemPrompt.get_system_prompt(),
                },
            ]

        openai_response = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools,
            #    reasoning_effort= "medium",
        )

        if openai_response.choices[0].finish_reason=="tool_calls":
            message = openai_response.choices[0].message
            tool_call = message.tool_calls[0]

            location = json.loads(tool_call.function.arguments)["location"]

            open_weather_response = LocationSearchTool.search_weather_for_location(location)
            messages.append({
                "role": "assistant",
                "content": json.dumps(open_weather_response)
            })
            response = openai_client.chat.completions.create(model="gpt-4.1-mini", messages=messages)

            return response.choices[0].message.content


