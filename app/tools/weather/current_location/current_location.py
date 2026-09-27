import json
from dotenv import load_dotenv
from helpers.model import ModelConst
from constants.system_prompt_constants import SystemPrompt
from helpers.openai_loader import OpenAILoader


class CurrentLocationWeatherTool:

    def current_location_weather_tool():
        """Tool for searching weather information based on location."""
        return {
            "name": "current_location_weather",
            "description": "Search for weather information based on the user's current location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The coordinates or name of the user's current location to search for weather information.",
                    }
                },
                "required": ["current_location"],
                "additionalProperties": False
            },
        }


    def get_current_location_weather(latlon: dict[str, float]) -> dict[str, str | float | None]:
        
        load_dotenv()
        url = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
