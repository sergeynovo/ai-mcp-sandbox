# Import necessary libraries
import os
from typing import Any, Dict

# NOTE: google.generativeai is deprecated; use the new unified google-genai SDK
from google import genai
from google.genai import types
import requests
from dotenv import load_dotenv

os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_CLOUD_REGION"] = "us-central1"

print("We are up and running!")
# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key.startswith("ADD YOUR"):
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
client = genai.Client(api_key=api_key)
model = "gemini-3.6-flash"

print(f"Gemini model loaded successfully: {model}")
PROMPT = "What is the current price of Bitcoin?"
chat = client.chats.create(model=model)
response = chat.send_message(PROMPT)
print(response.text)
