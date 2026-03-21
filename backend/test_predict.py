import requests
import os

URL = "http://localhost:8000/predict"
IMAGE_PATH = "test_maize_leaf.jpg"

def test_predict():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: {IMAGE_PATH} not found.")
        return

    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("test_maize_leaf.jpg", f, "image/jpeg")}
        data = {"crop": "maize", "lang": "en"}
        try:
            response = requests.post(URL, files=files, data=data)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Prediction Success!")
                # print(response.json())
                res = response.json()
                print(f"Detected: {res.get('disease_name')} with {res.get('confidence')}% confidence")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_predict()
