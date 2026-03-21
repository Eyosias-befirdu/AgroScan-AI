from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
client = genai.Client(api_key=api_key)

def list_models():
    try:
        print("Fetching models...")
        models = client.models.list()
        print("Success!")
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_models()
