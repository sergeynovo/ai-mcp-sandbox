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

print(response)

# Note: US users may need api.binance.us (binance.com is geo-blocked in the US)
url = f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
response = requests.get(url)
data = response.json()
print(data)

# Define the function
def get_crypto_price(symbol: str) -> Dict[str, Any]:
    """
    Get the current price of a cryptocurrency from Binance API
    """
    # Note: US users may need api.binance.us (binance.com is geo-blocked in the US)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

price = get_crypto_price("BTCUSDT")
print(f"BTC Price in USDT: {price}")

tools = [
    {
        "function_declarations": [
            {
                "name": "get_crypto_price",
                "description": "Get cryptocurrency price in USDT from Binance",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The cryptocurrency trading pair symbol (e.g., BTCUSDT, ETHUSDT). \
                                            The symbol for Bitcoin is BTCUSDT. \
                                            The symbol for Ethereum is ETHUSDT."
                        }
                    },
                    "required": ["symbol"]
                }
            }
        ]
    }
]

PROMPT = "What is the current price of Bitcoin?"
chat = client.chats.create(model=model, config={"tools": tools})
response = chat.send_message(PROMPT)
print(response)

price = get_crypto_price("BTCUSDT")

final_response = chat.send_message(
    types.Part.from_function_response(
        name="get_crypto_price",
        response={"price": price},
    )
)
print(final_response)

print(final_response.text)
