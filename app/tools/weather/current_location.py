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


    async def current_location_weather_chat(user_prompt: str) -> str:
        """Search for weather information based on the user's current location."""
        openai_client = OpenAILoader.openai_loader()

        tools = [{"type": "function", "function": CurrentLocationWeatherTool.location_search_tool()}]
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
            tool_call = message.tool_calls[0]

            location = json.loads(tool_call.function.arguments)["location"]

            open_weather_response = CurrentLocationWeatherTool.get_current_location_weather(location)
            messages.append({
                "role": "assistant",
                "content": json.dumps(open_weather_response)
            })
            response = openai_client.chat.completions.create(model=ModelConst.model(), messages=messages)

            return response.choices[0].message.content
