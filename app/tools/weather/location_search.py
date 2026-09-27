import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
import time
from openai import OpenAI

from app.helpers.openai_loader import OpenAILoader
from app.helpers.tools_selector import ToolSelector
from helpers.model import ModelConst
from constants.system_prompt_constants import SystemPrompt



class LocationSearchWeatherTool:

    # Function to define the tool for searching weather information based on a location name
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


    # Function to search for weather information based on a location name
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


    # Function to search for weather information based on a location name using OpenAI's chat model
    async def search_location_weather_chat(user_prompt :str):
        openai_client = OpenAILoader.openai_loader()

        tools = [{"type": "function", "function": LocationSearchWeatherTool.location_search_tool()}]
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
            model=ModelConst.model(),
            messages=messages,
            tools=tools,
            #    reasoning_effort= "medium",
        )

        if openai_response.choices[0].finish_reason=="tool_calls":
            message = openai_response.choices[0].message

            tool_call_response = ToolSelector.get_tool(message)
            messages.append(message)
            message.extend(tool_call_response)
            response = openai_client.chat.completions.create(model=ModelConst.model(), messages=messages)

            return response.choices[0].message.content


