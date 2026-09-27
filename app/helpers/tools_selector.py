


import json

from tools.weather.current_location import CurrentLocationWeatherTool
from tools.weather.location_search.location_search import LocationSearchWeatherTool


class ToolSelector:

    # Function to select the appropriate tool based on the message content
    @staticmethod
    async def get_tool(message):
        responses = []
        """Select the appropriate tool based on the message content."""
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            # if statement to select the appropriate tool based on the tool name
            if tool_name == "location_search":
                """This tool is used to search for weather information based on a location name."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                location = json.loads(tool_call.function.arguments)["location"]
                open_weather_response = LocationSearchWeatherTool.search_weather_for_location(location)
                responses.append({"role": "tool", "content": json.dumps(open_weather_response), "tool_call_id": tool_call.id})

            elif tool_name == "current_location_weather":
                """This tool is used to search for weather information based on the user's current location."""
                location = json.loads(tool_call.function.arguments)["current_location"]
                open_weather_response = CurrentLocationWeatherTool.get_current_location_weather(location)
                responses.append({"role": "tool", "content": json.dumps(open_weather_response), "tool_call_id": tool_call.id})

            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        return responses


