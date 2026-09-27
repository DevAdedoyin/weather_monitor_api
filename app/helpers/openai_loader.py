import os
from dotenv import load_dotenv
from openai import OpenAI

class OpenAILoader:
    def openai_loader():
        """Load the OpenAI API key from environment variables."""
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables.")
        return OpenAI(api_key=openai_api_key)