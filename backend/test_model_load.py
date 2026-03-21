from transformers import pipeline
import time

MODEL_ID = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

def test_load():
    try:
        print(f"Attempting to load {MODEL_ID}...")
        t0 = time.time()
        pipe = pipeline("image-classification", model=MODEL_ID)
        print(f"Success! Loaded in {time.time()-t0:.2f}s")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_load()
