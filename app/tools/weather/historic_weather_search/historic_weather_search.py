

class HistoricWeatherSearchTool:
    @staticmethod
    def historic_weather_search_tool():
        """Tool for searching historic weather information based on a location name."""
        return {
                    "name": "historic_weather_search",
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
                }
