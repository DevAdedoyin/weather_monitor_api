
from tools.air_quality.air_quality import AirQualityTool
from tools.weather.weather_tool import WeatherTool
from helpers.prompt_loader import PromptLoader
from helpers.tools_selector import ToolSelector
from helpers.openai_loader import OpenAILoader
from helpers.model import ModelConst
from constants.system_prompt_constants import SystemPrompt


class WeatherChat:
    # This method orchestrates the model call: it builds the prompt, sends the
    # configured tool definitions, and then executes any relevant weather/air-quality tool.
    async def weather_chatter(user_prompt :str, lat: float, lon: float, location: str, date: str):
        openai_client = OpenAILoader.openai_loader()

        # The model is allowed to call either weather or air-quality tools, depending on the user request.
        tools = [
            WeatherTool.get_weather_tool(),
            AirQualityTool.get_air_quality_tool(),
            {"type": "web_search"},
        ]

        # The first prompt contains the user query plus contextual location metadata.
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

        # Initial model call decides if a tool is required to answer the question.
        openai_response = openai_client.responses.create(
            model=ModelConst.model(),
            input=messages,
            tools=tools,
            include=["web_search_call.results"],
        )

        # Execute the selected tool and return the tool results in a follow up response.
        tool_call_response = await ToolSelector.get_tool(openai_response)

        response = openai_client.responses.create(
            model=ModelConst.model(),
            previous_response_id=openai_response.id,
            input=tool_call_response,
            tools=tools,
            include=["web_search_call.results"],
        )

        print("\n" + response.output_text)
        return response.output_text
