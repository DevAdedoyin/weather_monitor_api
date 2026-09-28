


import json
from tools.weather.generic_weather_query.generic_weather_query import GenericWeatherQuery
from tools.weather.location_search.location_search import LocationSearchWeatherTool


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
            if tool_name == "location_search":
                """This tool is used to search for weather information based on a location name."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                location = json.loads(tool_call.function.arguments)["location"]
                open_weather_response = LocationSearchWeatherTool.search_weather_for_location(location)
                responses.append({"role": "tool", "content": json.dumps(open_weather_response), "tool_call_id": tool_call.id})

            elif tool_name == "general_weather_query":
                """This tool is used to answer general weather questions."""
                print(f"ToolSelector: Calling tool {tool_name} with arguments: {tool_call.function.arguments}")
                question = json.loads(tool_call.function.arguments)["general_question"]
                print(f"ToolSelector: Calling GenericWeatherQuery with question: {question}")
                responses.append({"role": "tool", "content": question, "tool_call_id": tool_call.id})
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        return responses


