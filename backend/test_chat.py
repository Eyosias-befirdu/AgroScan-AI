import requests
import json

URL = "http://localhost:8000/chat"
PAYLOAD = {
    "message": "Hello, what diseases can you detect for maize?",
    "language": "English"
}

def test_chat():
    try:
        response = requests.post(URL, json=PAYLOAD)
        if response.status_code == 200:
            print("Chat Response:")
            print(response.json().get("response"))
        else:
            print(f"Error ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_chat()
