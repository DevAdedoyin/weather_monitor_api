


class ToolSelector:
    @staticmethod
    def get_tool(tool_name: str):
        if tool_name == "location_search":
            from app.tools.weather.location_search import LocationSearchWeatherTool
            return LocationSearchWeatherTool
        elif tool_name == "current_location":
            from app.tools.weather.current_location import CurrentLocationWeatherTool
            return CurrentLocationWeatherTool
        else:
            raise ValueError(f"Unknown tool name: {tool_name}")