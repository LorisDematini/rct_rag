# setup.py or config.py (create this in your project)
import os
from dotenv import load_dotenv
import openai

def configure_openai():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
