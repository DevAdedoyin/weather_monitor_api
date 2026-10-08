


class WeatherTool:

    @staticmethod
    def get_weather_tool():

        return {
            "type": "namespace",
            "name": "weather",
            "description": "Weather tools for current, forecast, and historical weather information.",
            "tools": [

                {
                    "type": "function",
                    "name": "current",
                    "description": "Search for current weather information based on a location name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The name of the location to search for weather information.",
                            }
                        },
                        "required": ["location"],
                        "additionalProperties": False
                    },
                },

                {
                    "type": "function",
                    "name": "historical",
                    "description": "Search for historic weather information based on a location name and time.",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The name of the location to search for historic weather information.",
                            },
                             "timestamp": {
                                "type": "integer",
                                "description": "Convert the datetime the user is requesting to an Unix timestamp of the day.",
                            }
                        },
                        "required": ["location", "timestamp"],
                        "additionalProperties": False
                    },
                },
            ]
        }