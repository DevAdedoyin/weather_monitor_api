


import json

from geopy import location

from tools.weather.current_location import CurrentLocationWeatherTool
from tools.weather.location_search import LocationSearchWeatherTool


class ToolSelector:

    # Function to select the appropriate tool based on the message content
    @staticmethod
    def get_tool(message: dict):
        responses = []
        """Select the appropriate tool based on the message content."""
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            if tool_name == "location_search":
                location = json.loads(tool_call.function.arguments)["location"]
                open_weather_response = LocationSearchWeatherTool.search_weather_for_location(location)
                responses.append({"role": "tool", "content": json.dumps(open_weather_response), "tool_call_id": tool_call.id})
            elif tool_name == "current_location_weather":
                responses.append(CurrentLocationWeatherTool.current_location_weather_chat)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        return responses