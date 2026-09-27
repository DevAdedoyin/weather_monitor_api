


from helpers.tools_selector import ToolSelector
from tools.weather.location_search.location_search import LocationSearchWeatherTool
from helpers.openai_loader import OpenAILoader
from helpers.model import ModelConst
from constants.system_prompt_constants import SystemPrompt


class SearchLocationWeatherChat:
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

            tool_call_response = await ToolSelector.get_tool(message)
            messages.append(message)
            messages.extend(tool_call_response)
            response = openai_client.chat.completions.create(model=ModelConst.model(), messages=messages)

            return response.choices[0].message.content
