

from datetime import datetime

from pydantic import json


class PromptLoader:


    @staticmethod
    def load_prompt(prompt: str, lat: float, lon: float, location: str, date: str) -> str:
        # Implementation for loading prompts from files or other sources

        user_context = {
            "current_location": {
                "latitude": lat,
                "longitude": lon,
                "address": location,
            },
            "date": date,
        }

        return f"""
            User request:
            {prompt}

            Additional context:
            {user_context}
        """
