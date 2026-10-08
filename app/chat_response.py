
from tools.air_quality.air_quality import AirQualityTool
from tools.weather.weather_tool import WeatherTool
from helpers.prompt_loader import PromptLoader
from helpers.tools_selector import ToolSelector
from helpers.openai_loader import OpenAILoader
from helpers.model import ModelConst
from constants.system_prompt_constants import SystemPrompt


class WeatherChat:
    # Function to search for weather information based on a location name using OpenAI's chat model
    async def weather_chatter(user_prompt :str, lat: float, lon: float, location: str, date: str):
        openai_client = OpenAILoader.openai_loader()

        tools = [
            WeatherTool.get_weather_tool(),
            AirQualityTool.get_air_quality_tool(),
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

        openai_response = openai_client.responses.create(
            model=ModelConst.model(),
            input=messages,
            tools=tools,
            include=["web_search_call.results"],
        )

        tool_call_response = await ToolSelector.get_tool(openai_response)

        print(f"Tool call response: {tool_call_response}")

        response = openai_client.responses.create(
            model=ModelConst.model(),
            previous_response_id=openai_response.id,
            input=tool_call_response,
            tools=tools,
            include=["web_search_call.results"],
        )

        print(response.model_dump_json(indent=2))

        print("\n" + response.output_text)
        return response.output_text
