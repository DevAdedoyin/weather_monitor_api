

class HistoricWeatherSearchTool:
    @staticmethod
    def historic_weather_search_tool():
        """Tool for searching historic weather information based on a location name."""
        return {
                    "name": "historic_weather_search",
                    "description": "Search for historic weather information based on a location name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The name of the location to search for historic weather information.",
                            }
                        },
                        "required": ["location"],
                        "additionalProperties": False
                    },
                }
