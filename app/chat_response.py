


from tools.weather.generic_weather_query.generic_weather_query import GenericWeatherQuery
from helpers.prompt_loader import PromptLoader
from helpers.tools_selector import ToolSelector
from tools.weather.location_search.location_search import LocationSearchWeatherTool
from helpers.openai_loader import OpenAILoader
from helpers.model import ModelConst
from constants.system_prompt_constants import SystemPrompt


class WeatherChat:
    # Function to search for weather information based on a location name using OpenAI's chat model
    async def weather_chatter(user_prompt :str, lat: float, lon: float, location: str, date: str):
        openai_client = OpenAILoader.openai_loader()

        tools = [
            {"type": "function", "function": LocationSearchWeatherTool.location_search_tool()},
            {"type": "function", "function": GenericWeatherQuery.generic_weather_query_tool()}
        ]
        messages = [
                {
                    "role": "user",
                    "content": PromptLoader.load_prompt(user_prompt, lat=lat, lon=lon, location=location, date=date),
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

        if openai_response.choices[0].finish_reason == "tool_calls":
            message = openai_response.choices[0].message

            tool_call_response = await ToolSelector.get_tool(message)
            messages.append(message)
            messages.extend(tool_call_response)
            response = openai_client.chat.completions.create(model=ModelConst.model(), messages=messages)

            return response.choices[0].message.content
        else:
            return openai_response.choices[0].message.content
