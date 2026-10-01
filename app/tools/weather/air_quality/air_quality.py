

class AirQualityTool:
    def get_air_quality_tool():

        # Function to define the tool for searching air quality information based on a location name
        return {
            "name": "air_quality_search",
            "description": "Search for air quality information based on a location name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of the location to search for air quality information.",
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            },
        }