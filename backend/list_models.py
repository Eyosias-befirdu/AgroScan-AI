from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def list_models():
    try:
        models = client.models.list()
        for m in models:
            print(f"Model Name: {m.name}, Supported Actions: {m.supported_generation_methods}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
