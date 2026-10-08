


import json
from utility_data.air_quality_data import AirQualityData
from utility_data.weather_data import WeatherData
from helpers.location_searcher import LocationSearcher


class ToolSelector:

    # Function to select the appropriate tool based on the message content
    @staticmethod
    async def get_tool(message):
        responses = []
        """Select the appropriate tool based on the message content."""
        print(f"ToolSelector: Received message: {message}")
        for tool_call in message.output:

             # Ignore reasoning, message, web search, etc.
            if tool_call.type != "function_call":
                continue

            namespace = tool_call.namespace
            tool_name = tool_call.name
            arguments = json.loads(tool_call.arguments)

            # if statement to select the appropriate tool based on the tool name

            # WEATHER NAMESPACE
            if namespace == "weather":

                if tool_name == "historical":
                    location = arguments["location"]
                    timestamp = arguments["timestamp"]

                    latlng = await LocationSearcher.search_location_for_weather(
                        location=location
                    )

                    weather_response = WeatherData.get_weather_data(
                        lat=latlng["lat"],
                        lon=latlng["lon"],
                        isHistory=True,
                        location=location,
                        timestamp=timestamp
                    )

                    responses.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(weather_response)
                    })

                elif tool_name == "current":
                    location = arguments["location"]

                    latlng = await LocationSearcher.search_location_for_weather(
                        location=location
                    )

                    weather_response = WeatherData.get_weather_data(
                        lat=latlng["lat"],
                        lon=latlng["lon"],
                        isHistory=False,
                        location=location
                    )

                    responses.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(weather_response)
                    })

                else:
                    raise ValueError(
                        f"Unknown weather tool: {tool_name}"
                    )


            # AIR QUALITY NAMESPACE
            elif namespace == "air_quality":

                if tool_name == "current_air_quality":
                    location = arguments["location"]

                    latlng = await LocationSearcher.search_location_for_weather(
                        location=location
                    )

                    air_quality_response = (
                        AirQualityData.get_air_quality_data(
                            location=location,
                            lat=latlng["lat"],
                            lon=latlng["lon"]
                        )
                    )

                    responses.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(air_quality_response)
                    })

                else:
                    raise ValueError(
                        f"Unknown air quality tool: {tool_name}"
                    )

            else:
                raise ValueError(
                    f"Unknown namespace: {namespace}"
                )

        return responses
