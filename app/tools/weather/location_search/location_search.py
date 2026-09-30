


class LocationSearchWeatherTool:

    # Function to define the tool for searching weather information based on a location name
    def location_search_tool():
        """Tool for searching weather information based on location."""
        return {
            "name": "location_search",
            "description": "Search for weather information based on a location name.",
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
        }







