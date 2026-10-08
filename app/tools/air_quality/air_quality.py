

class AirQualityTool:
    def get_air_quality_tool():

        # Function to define the tool for searching air quality information based on a location name
        return {
            "type": "namespace",
            "name": "air_quality",
            "description": "Air quality tools for air quality information.",
            "tools": [
                {
                    "type": "function",
                    "name": "current_air_quality",
                    "description": "Search for current air quality information based on a location name.",
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
            ]
        }