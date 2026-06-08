import base64
import json
from dotenv import load_dotenv
from groq import Groq
import os

class ExpenseAgent:
    def __init__(self):
        load_dotenv (".env")
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key)
        

        pass

    def extract_from_bytes(self, image_bytes, media_type):
        pass