


import json
from data.weather_data import WeatherData
from helpers.location_searcher import LocationSearcher
from datetime import datetime, timezone


class ToolSelector:

    # Function to select the appropriate tool based on the message content
    @staticmethod
    async def get_tool(message):
        responses = []
        """Select the appropriate tool based on the message content."""
        print(f"ToolSelector: Received message: {message}")
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            # if statement to select the appropriate tool based on the tool name
            if tool_name == "historic_weather_search":
                """This tool is used to search for historical weather information based on a location name."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                location = json.loads(tool_call.function.arguments)["location"]
                timestamp = json.loads(tool_call.function.arguments)["timestamp"]
                print(f"REQUESTED TimeStamp {timestamp}")
                latlng = await LocationSearcher.search_location_for_weather(location=location)
                open_weather_response = WeatherData.get_weather_data(lat=latlng["lat"], lon=latlng["lon"], isHistory=True, timestamp=timestamp)
                responses.append({"role": "tool", "content": json.dumps(open_weather_response), "tool_call_id": tool_call.id})

            elif tool_name == "location_search":
                """This tool is used to search for weather information based on a location name."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                location = json.loads(tool_call.function.arguments)["location"]
                # timestamp: int = int(datetime.now(timezone.utc).timestamp())
                latlng = await LocationSearcher.search_location_for_weather(location=location)
                open_weather_response = WeatherData.get_weather_data(lat=latlng["lat"], lon=latlng["lon"], isHistory=False)
                responses.append({"role": "tool", "content": json.dumps(open_weather_response), "tool_call_id": tool_call.id})

            elif tool_name == "air_quality_search":
                """This tool is used to search for air quality information based on a location name."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                location = json.loads(tool_call.function.arguments)["location"]
                # timestamp: int = int(datetime.now(timezone.utc).timestamp())
                air_quality_response = LocationSearcher.search_air_quality_for_location(location=location)
                responses.append({"role": "tool", "content": json.dumps(air_quality_response), "tool_call_id": tool_call.id})

            elif tool_name == "general_weather_query":
                """This tool is used to answer general weather questions."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                question = json.loads(tool_call.function.arguments)["general_question"]
                print(f"ToolSelector: Calling GenericWeatherQuery with question: {question}")
                responses.append({"role": "tool", "content": question, "tool_call_id": tool_call.id})

            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        return responses


