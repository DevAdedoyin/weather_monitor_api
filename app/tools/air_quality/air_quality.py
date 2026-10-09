

class AirQualityTool:
    def get_air_quality_tool():

        # This schema tells the model which air-quality actions are available and which
        # parameters are required for each one. The model uses this metadata when deciding
        # whether to request current, historical, or forecast air-quality data.
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
                },

                {
                    "type": "function",
                    "name": "historical",
                    "description": (
                        "Get historical hourly air quality for a location. "
                        "Historical data is available only for dates within the past 30 days."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string"
                            },
                        },
                        "required": ["location"],
                        "additionalProperties": False
                    }
                },

                {
                    "type": "function",
                    "name": "forecast",
                    "description": (
                        "Get forecasted hourly air quality for a location. "
                        "Forecast data is available only for dates within the next 96 hours (4 days)."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string"
                            },
                            "timestamp": {
                                "type": "string",
                                "description": (
                                    "Convert the datetime the user is requesting to an Unix timestamp of the day."
                                    "The datetime should be in this format YYYY-MM-DDTHH:MM:SSZ."
                                    "If time is not explicitly stated, use the day requested and current time in UTC."
                                )
                            }
                        },
                        "required": ["location", "timestamp"],
                        "additionalProperties": False
                    }
                }
            ]
        }