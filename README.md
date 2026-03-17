# Agricultural Disease Scan – README
## AI Crop Disease Detection for Ethiopian Farmers 🇪🇹🌿

Agricultural Disease Scan is a full-stack web application that uses computer vision AI to detect crop diseases from leaf images. Built specifically for Ethiopian farmers growing Teff, Maize, Wheat, and Coffee.

---

## Project Structure

```
agricultural-disease-scan/
├── frontend/
│   ├── index.html       ← Main web page (all sections)
│   ├── style.css        ← Dark theme, glassmorphism, animations
│   ├── app.js           ← Disease DB, upload logic, AI simulation
│   └── assets/
│       ├── hero_farm.png
│       └── logo.png
│
├── backend/
│   ├── main.py          ← FastAPI server with prediction endpoints
│   └── requirements.txt
│
└── README.md
```

---

## Running the Frontend

Simply open `frontend/index.html` in a browser — no build step needed.

Or serve it with Python:
```bash
cd frontend
python -m http.server 3000
# Visit http://localhost:3000
```

---

## Running the Backend (FastAPI)

```bash
cd backend

# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# OR
source venv/bin/activate    # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload --port 8000

# 4. Open API docs
# http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| POST | `/predict` | **Upload leaf + get disease prediction** |
| GET | `/diseases` | All diseases in database |
| GET | `/diseases/{crop}` | Diseases for a specific crop |
| GET | `/history` | Recent scan history |
| GET | `/stats` | Usage statistics |

### Example `/predict` call (curl):
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@leaf_photo.jpg" \
  -F "crop=maize"
```

### Example Response:
```json
{
  "scan_id": "a3f8bc12",
  "timestamp": "2025-03-14T09:32:56",
  "crop": "maize",
  "disease_name": "Gray Leaf Spot",
  "scientific_name": "Cercospora zeae-maydis",
  "confidence": 92.4,
  "severity": "high",
  "cause": "Caused by the fungus Cercospora zeae-maydis...",
  "symptoms": ["Rectangular gray lesions...", ...],
  "treatment": ["Apply azoxystrobin...", ...],
  "prevention": ["Plant resistant varieties...", ...],
  "urgency": "Act immediately — can reduce yields by 50%",
  "is_healthy": false
}
```

---

## Crops & Diseases Supported

| Crop | Diseases |
|------|----------|
| 🌽 Maize (በቆሎ) | Gray Leaf Spot, N. Corn Blight, Common Rust, Ear Rot |
| 🌾 Wheat (ስንዴ) | Leaf Rust, Yellow Rust, Septoria |
| ☕ Coffee (ቡና) | Coffee Berry Disease, Leaf Rust, Wilt Disease |
| 🌿 Teff (ጤፍ) | Leaf Blotch, Head Smut |

---

## Tech Stack

**Frontend:**
- Pure HTML5 + Vanilla CSS + JavaScript
- Google Fonts (Inter, Space Grotesk)
- Zero dependencies — runs in any browser

**Backend:**
- Python 3.10+
- FastAPI
- Uvicorn
- Pillow (image validation)

**AI Model (Production):**
- TensorFlow / PyTorch
- EfficientNet (transfer learning)
- OpenCV for preprocessing
- PlantVillage dataset + custom Ethiopian crop images

---

## Next Steps for Production

1. **Train a real model** using PlantVillage dataset + Ethiopian field images
2. **Add TensorFlow serving** — replace `mock_predict()` in `main.py`
3. **Add SQLite/PostgreSQL** database for scan persistence
4. **Add Amharic language** support for UI
5. **Build Android app** for offline mobile use
6. **Add SMS/USSD support** for feature phone users

---

*Built with ❤️ for Ethiopian farmers*
