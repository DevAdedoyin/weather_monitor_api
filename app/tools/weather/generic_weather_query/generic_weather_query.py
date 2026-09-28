


class GenericWeatherQuery:

    @staticmethod
    # Function to define the tool for searching weather information based on a location name
    def generic_weather_query_tool():
        """Tool for answering general weather questions."""
        return {
            "name": "general_weather_query",
            "description": "Accurately answer general weather questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "general_question": {
                        "type": "string",
                        "description": "The question to answer about the weather.",
                    }
                },
                "required": ["general_question"],
                "additionalProperties": False
            },
        }