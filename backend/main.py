"""
AgroScan AI – FastAPI Backend
==============================
Crop disease detection API backed by PostgreSQL for persistent history & stats.
Uses a real pre-trained MobileNetV2 model (PlantVillage) for Maize & Wheat;
Smart mock for Teff & Coffee (not in PlantVillage dataset).

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
import random
import time
import uuid
import io
from datetime import datetime
from typing import Optional

# PIL (optional)
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from database import get_db, init_db, check_db_connection
from models import ScanResult
import ai_model  # real inference engine

# ============================================================
# App Configuration
# ============================================================
app = FastAPI(
    title="AgroScan AI API",
    description="AI-powered crop disease detection for Ethiopian farmers",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Create database tables on first run."""
    await init_db()
    print("✅  Database tables verified / created.")


# ============================================================
# Disease Knowledge Base
# ============================================================
DISEASE_DB = {
    "maize": [
        {
            "name": "Gray Leaf Spot",
            "scientific_name": "Cercospora zeae-maydis",
            "icon": "🍂",
            "severity": "high",
            "confidence_range": (85, 96),
            "cause": "Caused by the fungus Cercospora zeae-maydis. Thrives in warm, humid conditions with poor air circulation, especially in densely planted maize fields.",
            "symptoms": [
                "Rectangular gray to tan lesions parallel to leaf veins",
                "Yellow halo surrounding spots",
                "Premature leaf death and crop lodging",
                "Lesions can coalesce to kill entire leaves"
            ],
            "treatment": [
                "Apply fungicides containing azoxystrobin or propiconazole",
                "Remove and destroy heavily infected plant debris",
                "Avoid overhead irrigation",
                "Apply balanced fertilizer to improve plant vigor"
            ],
            "prevention": [
                "Plant disease-resistant maize varieties",
                "Rotate crops — avoid continuous maize planting",
                "Ensure proper plant spacing for air circulation",
                "Monitor fields regularly during humid seasons"
            ],
            "urgency": "Act immediately — Gray Leaf Spot can reduce yields by up to 50% if untreated.",
            "affected_regions": ["Oromia", "Amhara", "SNNPR", "Tigray"]
        },
        {
            "name": "Northern Corn Blight",
            "scientific_name": "Exserohilum turcicum",
            "icon": "🌑",
            "severity": "high",
            "confidence_range": (88, 97),
            "cause": "Caused by Exserohilum turcicum. Spreads rapidly in cool, moist weather through airborne spores from infected crop residue.",
            "symptoms": [
                "Large cigar-shaped gray-green lesions",
                "Lesions turn tan with dark borders",
                "Leaves wilt and die from bottom upward",
                "Dark fungal sporulation in humid conditions"
            ],
            "treatment": [
                "Apply foliar fungicides at early detection",
                "Use triazole-based fungicides for best control",
                "Remove infected lower leaves promptly",
                "Improve field drainage to reduce humidity"
            ],
            "prevention": [
                "Use certified resistant hybrid seeds",
                "Deep plow to bury infected residue",
                "Avoid planting in low-lying areas with poor drainage",
                "Follow a 2–3 year crop rotation"
            ],
            "urgency": "High severity — can cause 30–70% yield loss. Treat within 48 hours of detection.",
            "affected_regions": ["Oromia", "Amhara"]
        },
        {
            "name": "Common Rust",
            "scientific_name": "Puccinia sorghi",
            "icon": "🟤",
            "severity": "moderate",
            "confidence_range": (82, 94),
            "cause": "Caused by Puccinia sorghi, a wind-borne fungal pathogen. Pustules form on both leaf surfaces. Common in Ethiopian highland farming areas.",
            "symptoms": [
                "Brick-red to brown powdery pustules on leaves",
                "Pustules on both upper and lower leaf surfaces",
                "Yellow streaking around pustules",
                "Leaves may dry out and curl in advanced stages"
            ],
            "treatment": [
                "Apply mancozeb or propiconazole fungicide",
                "Remove severely infected leaves",
                "Improve field aeration",
                "Apply foliar nutrition to boost plant immunity"
            ],
            "prevention": [
                "Choose rust-resistant maize varieties",
                "Avoid late planting in high-risk seasons",
                "Monitor fields every 1–2 weeks",
                "Maintain proper field sanitation after harvest"
            ],
            "urgency": "Moderate — reduce spread with prompt fungicide application within 5–7 days.",
            "affected_regions": ["All highland regions"]
        },
        {
            "name": "Ear Rot",
            "scientific_name": "Fusarium / Gibberella spp.",
            "icon": "🌽",
            "severity": "high",
            "confidence_range": (80, 92),
            "cause": "Caused by Fusarium, Gibberella, and Diplodia fungi. Wet harvest conditions and insect damage on husks create entry points.",
            "symptoms": [
                "Pink, red or white mold growing on kernels",
                "Discolored, shriveled kernels",
                "Foul smell from the cob",
                "Premature ear drop in severe cases"
            ],
            "treatment": [
                "Harvest early at proper moisture (<25%)",
                "Dry harvested maize to below 13% moisture quickly",
                "Discard all visibly moldy cobs immediately",
                "Store in dry, ventilated structures"
            ],
            "prevention": [
                "Control insect pests that damage husks",
                "Avoid kernel damage during harvest",
                "Use disease-free certified seeds",
                "Ensure timely harvest before rains"
            ],
            "urgency": "Critical — mycotoxins from Ear Rot are toxic to humans and animals. Do not consume moldy grain.",
            "affected_regions": ["Oromia", "Amhara", "Benishangul-Gumuz"]
        }
    ],
    "wheat": [
        {
            "name": "Leaf Rust",
            "scientific_name": "Puccinia triticina",
            "icon": "🟠",
            "severity": "high",
            "confidence_range": (88, 98),
            "cause": "Caused by Puccinia triticina. One of the most widespread wheat diseases in Ethiopia. Spreads via wind-borne urediniospores in moderate temperatures (15–25°C).",
            "symptoms": [
                "Orange-brown oval pustules on upper leaf surface",
                "Yellow stripe around pustule clusters",
                "Premature leaf death",
                "Reduced grain filling and lower kernel weight"
            ],
            "treatment": [
                "Apply triazole fungicides (tebuconazole, propiconazole)",
                "Spray every 10–14 days during epidemic conditions",
                "Destroy volunteer wheat plants nearby",
                "Prioritize treatment at heading and grain fill stages"
            ],
            "prevention": [
                "Plant certified rust-resistant wheat varieties",
                "Sow at recommended time to escape peak rust season",
                "Scout fields weekly from tillering",
                "Remove crop debris after harvest"
            ],
            "urgency": "High urgency — Leaf Rust can cause 20–60% yield loss. Begin fungicide application immediately.",
            "affected_regions": ["Arsi", "Bale", "Amhara highlands"]
        },
        {
            "name": "Yellow (Stripe) Rust",
            "scientific_name": "Puccinia striiformis f. sp. tritici",
            "icon": "🟡",
            "severity": "high",
            "confidence_range": (87, 97),
            "cause": "Highly devastating in the Ethiopian highlands. Spreads rapidly in cool, moist weather — ideal in Arsi and Bale zones.",
            "symptoms": [
                "Yellow-orange stripes parallel to leaf veins",
                "Powdery pustules arranged in linear rows",
                "Leaves turn completely yellow then die",
                "Early head infection leads to zero grain formation"
            ],
            "treatment": [
                "Apply triazole fungicides immediately on first sign",
                "Treat the entire field, not just visible patches",
                "Use aerial or mechanical spray equipment",
                "Repeat application after 14 days if needed"
            ],
            "prevention": [
                "Grow CIMMYT/KARC-recommended resistant varieties",
                "Report new rust strains to extension agents",
                "Avoid excessive nitrogen fertilization",
                "Monitor highland fields closely in early season"
            ],
            "urgency": "CRITICAL — Yellow Rust can devastate entire fields within 3 weeks in Ethiopia. Act immediately!",
            "affected_regions": ["Arsi", "Bale", "Jimma", "West Hararghe"]
        }
    ],
    "coffee": [
        {
            "name": "Coffee Berry Disease (CBD)",
            "scientific_name": "Colletotrichum kahawae",
            "icon": "☕",
            "severity": "high",
            "confidence_range": (86, 96),
            "cause": "Endemic to Africa. Highly dangerous for Ethiopian Arabica coffee. Spreads via rain splash during berry development.",
            "symptoms": [
                "Dark sunken lesions on green coffee berries",
                "Premature berry drop",
                "Berries shrivel and turn black",
                "Brown discoloration of beans when cut"
            ],
            "treatment": [
                "Apply copper-based fungicides every 2–3 weeks",
                "Remove and destroy all mummified berries",
                "Prune for better canopy airflow",
                "Use Bordeaux mixture (copper sulfate + lime)"
            ],
            "prevention": [
                "Plant CBD-resistant varieties (Catimor-derived)",
                "Harvest ripe berries promptly",
                "Perform regular light pruning",
                "Maintain soil pH and balanced fertilization"
            ],
            "urgency": "High severity — CBD causes up to 80% crop loss in Ethiopia if uncontrolled. Spray immediately.",
            "affected_regions": ["Jimma", "Kaffa", "Sidama", "Yirgacheffe"]
        },
        {
            "name": "Coffee Wilt Disease",
            "scientific_name": "Gibberella xylarioides",
            "icon": "🥀",
            "severity": "high",
            "confidence_range": (83, 94),
            "cause": "Soil-borne fungus that infects roots and vascular tissue. A major economic threat in Ethiopia since the 1940s.",
            "symptoms": [
                "Sudden yellowing and wilting of branches",
                "Brown discoloration inside stem when cut",
                "Rapid defoliation followed by plant death",
                "Dead plants with dried berries still attached"
            ],
            "treatment": [
                "Remove and burn all infected plants immediately",
                "Do not replant in the same spot for 3–5 years",
                "Disinfect tools with bleach between plants",
                "Report outbreak to local agricultural office"
            ],
            "prevention": [
                "Use certified wilt-free seedlings",
                "Avoid moving soil from infected fields",
                "Regularly inspect roots during transplanting",
                "Plant resistant varieties from Jimma University"
            ],
            "urgency": "CRITICAL — Coffee Wilt is lethal. Affected plants cannot be saved. Remove immediately.",
            "affected_regions": ["Jimma", "Kaffa", "Bench-Sheko"]
        }
    ],
    "teff": [
        {
            "name": "Teff Leaf Blotch",
            "scientific_name": "Drechslera spp.",
            "icon": "🌿",
            "severity": "moderate",
            "confidence_range": (77, 90),
            "cause": "Develops in humid conditions with poor drainage. Particularly damaging in Oromia and SNNPR teff growing zones.",
            "symptoms": [
                "Reddish-brown to dark brown oval spots on leaves",
                "Lesions enlarge and coalesce under wet conditions",
                "Yellowing of leaves around spots",
                "Premature drying and lodging"
            ],
            "treatment": [
                "Apply mancozeb or propiconazole fungicide",
                "Improve field drainage to lower humidity",
                "Remove severely infected leaves",
                "Apply balanced fertilizer to support recovery"
            ],
            "prevention": [
                "Use disease-free certified teff seed",
                "Avoid waterlogged field conditions",
                "Practice 2-year rotation with legumes",
                "Plow under crop residue after harvest"
            ],
            "urgency": "Moderate — treat promptly to prevent spread across the field during rainy season.",
            "affected_regions": ["Oromia", "Amhara", "SNNPR"]
        },
        {
            "name": "Head Smut",
            "scientific_name": "Tilletia tef",
            "icon": "🫧",
            "severity": "high",
            "confidence_range": (80, 92),
            "cause": "A seed-borne and soil-borne smut disease specific to teff. Devastating in infected seed lots used for planting.",
            "symptoms": [
                "Entire teff head replaced by black spore mass",
                "Infected panicles emit fishy or rotten smell",
                "Spores released when wind breaks diseased heads",
                "Surrounding soil contaminated after spore release"
            ],
            "treatment": [
                "Treat healthy seed with fungicide before next season",
                "Remove and destroy all smutted plants before spore release",
                "Burn infected material away from the field",
                "Do not use grain from infected crop as seed"
            ],
            "prevention": [
                "Use certified, treated teff seed each season",
                "Apply seed treatment with carboxin or iprodione",
                "Avoid replanting where smut was present for 2 years",
                "Source seeds from government seed enterprises"
            ],
            "urgency": "High — if spores release, soil will be infected for years. Remove smutted heads immediately.",
            "affected_regions": ["Central Ethiopia", "Amhara", "Oromia"]
        }
    ]
}

HEALTHY_RESULT = {
    "name": "Healthy Leaf",
    "scientific_name": "No pathogen detected",
    "icon": "✅",
    "severity": "none",
    "confidence_range": (90, 98),
    "cause": "No signs of disease detected. The leaf appears healthy with normal color and no visible lesions or fungal growth.",
    "symptoms": [
        "Normal green coloration throughout",
        "No visible lesions or spots",
        "Uniform leaf texture",
        "Healthy vein structure"
    ],
    "treatment": [
        "No treatment needed at this time",
        "Continue regular field monitoring",
        "Apply balanced fertilizer if not done yet",
        "Maintain proper irrigation schedule"
    ],
    "prevention": [
        "Continue current crop management practices",
        "Scout weekly for early disease detection",
        "Keep field clean of weeds and crop debris",
        "Rotate crops as planned"
    ],
    "urgency": "No immediate action required. Maintain your current management practices.",
    "affected_regions": []
}


# ============================================================
# AI Inference  (real model — see ai_model.py)
# ============================================================
def run_predict(image_bytes: bytes, crop: str) -> dict:
    """
    Delegates to ai_model.predict():
      - Maize / Wheat → PlantVillage MobileNetV2 (HuggingFace)
      - Teff  / Coffee → Smart confidence-weighted mock
    """
    return ai_model.predict(
        image_bytes=image_bytes,
        crop=crop,
        disease_db=DISEASE_DB,
        healthy_result=HEALTHY_RESULT,
    )


# ============================================================
# API Endpoints
# ============================================================

@app.get("/", tags=["Health"])
async def root():
    db_ok = await check_db_connection()
    return {
        "service":     "AgroScan AI API",
        "version":     "2.0.0",
        "status":      "running",
        "database":    "connected" if db_ok else "disconnected",
        "ai_model":    "PlantVillage-MobileNetV2 (HuggingFace)",
        "description": "AI-powered crop disease detection for Ethiopian farmers",
        "docs":        "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    db_ok = await check_db_connection()
    return {
        "status":    "healthy",
        "database":  "connected" if db_ok else "disconnected",
        "ai_model":  "PlantVillage-MobileNetV2 (HuggingFace)",
        "timestamp": datetime.now().isoformat()
    }


# --------------------------------------------------------
# Predict
# --------------------------------------------------------
@app.post("/predict", tags=["AI Prediction"])
async def predict_disease(
    file: UploadFile = File(...),
    crop: str = Form(default="maize"),
    lang: str = Form(default="en"),
    db: AsyncSession = Depends(get_db),
):
    """
    Main prediction endpoint.

    - **file**: Upload a leaf image (JPG/PNG/WEBP)
    - **crop**: One of `maize`, `wheat`, `coffee`, `teff`

    Returns disease name, confidence score, treatment recommendations
    and **persists the result to PostgreSQL**.
    """
    valid_crops = ["maize", "wheat", "coffee", "teff"]
    if crop.lower() not in valid_crops:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid crop type. Choose from: {', '.join(valid_crops)}"
        )

    content_type = file.content_type or ""
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file (JPG, PNG, WEBP)"
        )

    image_data = await file.read()
    if len(image_data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large. Maximum size is 10MB.")

    if PIL_AVAILABLE:
        try:
            img = Image.open(io.BytesIO(image_data))
            img.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or corrupted image file.")

    # ── Real AI inference (PlantVillage model for maize/wheat;
    #    smart mock for teff/coffee) ──────────────────────────
    result = run_predict(image_data, crop.lower())
    result["filename"]     = file.filename
    result["file_size_kb"] = round(len(image_data) / 1024, 1)

    # ── Dynamic AI Translation for Non-English ──────────────
    if lang.lower() in ["am", "om"]:
        lang_name = "Amharic" if lang.lower() == "am" else "Afaan Oromoo"
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                import json
                client = genai.Client(api_key=api_key)
                text_to_translate = {
                    "disease_name": result["disease_name"],
                    "severity": result["severity"],
                    "cause": result["cause"],
                    "symptoms": result["symptoms"],
                    "treatment": result["treatment"],
                    "prevention": result["prevention"],
                    "urgency": result["urgency"],
                }
                
                resp = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Translate the values of this JSON object exactly into {lang_name}. Do NOT translate the keys. Respond ONLY with valid JSON and no markdown formatting: {json.dumps(text_to_translate)}"
                )
                
                # Clean up response payload to parse JSON
                raw_json = resp.text.strip().removeprefix('```json').removesuffix('```').strip()
                translated_dict = json.loads(raw_json)
                
                for key in translated_dict:
                    if key in result:
                        result[key] = translated_dict[key]
            except Exception as e:
                print(f"Translation failed: {e}")

    # ── Persist to PostgreSQL ───────────────────────────────
    row = ScanResult(
        scan_id          = result["scan_id"],
        crop             = result["crop"],
        filename         = result["filename"],
        file_size_kb     = result["file_size_kb"],
        disease_name     = result["disease_name"],
        scientific_name  = result["scientific_name"],
        icon             = result["icon"],
        confidence       = result["confidence"],
        severity         = result["severity"],
        is_healthy       = result["is_healthy"],
        cause            = result["cause"],
        urgency          = result["urgency"],
        symptoms         = result["symptoms"],
        treatment        = result["treatment"],
        prevention       = result["prevention"],
        affected_regions = result["affected_regions"],
    )
    db.add(row)
    await db.flush()   # get server-generated created_at without closing tx
    result["timestamp"] = row.created_at.isoformat() if row.created_at else result["timestamp"]
    # ──────────────────────────────────────────────────────────

    return JSONResponse(content=result)


# --------------------------------------------------------
# Disease Info
# --------------------------------------------------------
@app.get("/diseases", tags=["Disease Info"])
async def get_all_diseases():
    """Returns the complete disease database for all crops."""
    summary = {}
    for crop, diseases in DISEASE_DB.items():
        summary[crop] = [
            {
                "name":            d["name"],
                "scientific_name": d["scientific_name"],
                "severity":        d["severity"],
                "icon":            d["icon"],
            }
            for d in diseases
        ]
    return {"crops": summary, "total_diseases": sum(len(v) for v in DISEASE_DB.values())}


@app.get("/diseases/{crop}", tags=["Disease Info"])
async def get_diseases_by_crop(crop: str):
    """Returns all known diseases for a specific crop."""
    crop = crop.lower()
    if crop not in DISEASE_DB:
        raise HTTPException(
            status_code=404,
            detail=f"Crop '{crop}' not found. Valid crops: maize, wheat, coffee, teff"
        )
    return {"crop": crop, "diseases": DISEASE_DB[crop]}


# --------------------------------------------------------
# History  (now reads from PostgreSQL)
# --------------------------------------------------------
@app.get("/history", tags=["Scan History"])
async def get_scan_history(
    limit: int = 20,
    crop: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns recent scan history from PostgreSQL.

    - **limit**: Max records to return (default 20, max 200)
    - **crop**: Filter by crop type (optional)
    """
    limit = min(limit, 200)

    query = select(ScanResult).order_by(desc(ScanResult.created_at)).limit(limit)
    if crop:
        query = query.where(ScanResult.crop == crop.lower())

    result = await db.execute(query)
    rows   = result.scalars().all()

    total_query = select(func.count()).select_from(ScanResult)
    if crop:
        total_query = total_query.where(ScanResult.crop == crop.lower())
    total_result = await db.execute(total_query)
    total = total_result.scalar_one()

    return {
        "total_scans": total,
        "returned":    len(rows),
        "history":     [r.to_dict() for r in rows],
    }


# --------------------------------------------------------
# Stats  (now computed from PostgreSQL)
# --------------------------------------------------------
@app.get("/stats", tags=["Statistics"])
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Returns API usage statistics computed from the PostgreSQL database."""

    # Total scans
    total_result = await db.execute(select(func.count()).select_from(ScanResult))
    total = total_result.scalar_one()

    if total == 0:
        return {"total_scans": 0, "message": "No scans yet"}

    # Healthy count
    healthy_result = await db.execute(
        select(func.count()).where(ScanResult.is_healthy == True)  # noqa: E712
    )
    healthy_count = healthy_result.scalar_one()

    # Average confidence
    avg_conf_result = await db.execute(select(func.avg(ScanResult.confidence)))
    avg_confidence = round(float(avg_conf_result.scalar_one() or 0), 1)

    # Top disease (most frequent)
    disease_q = (
        select(ScanResult.disease_name, func.count().label("cnt"))
        .group_by(ScanResult.disease_name)
        .order_by(desc("cnt"))
        .limit(1)
    )
    top_disease_result = await db.execute(disease_q)
    top_disease_row = top_disease_result.first()
    top_disease = top_disease_row[0] if top_disease_row else None

    # Top crop
    crop_q = (
        select(ScanResult.crop, func.count().label("cnt"))
        .group_by(ScanResult.crop)
        .order_by(desc("cnt"))
        .limit(1)
    )
    top_crop_result = await db.execute(crop_q)
    top_crop_row = top_crop_result.first()
    top_crop = top_crop_row[0] if top_crop_row else None

    # Severity breakdown
    severity_q = (
        select(ScanResult.severity, func.count().label("cnt"))
        .group_by(ScanResult.severity)
    )
    sev_result = await db.execute(severity_q)
    severity_breakdown = {row[0]: row[1] for row in sev_result.all()}

    # Crop breakdown
    crop_breakdown_q = (
        select(ScanResult.crop, func.count().label("cnt"))
        .group_by(ScanResult.crop)
    )
    crop_result = await db.execute(crop_breakdown_q)
    crop_breakdown = {row[0]: row[1] for row in crop_result.all()}

    return {
        "total_scans":        total,
        "healthy_scans":      healthy_count,
        "disease_scans":      total - healthy_count,
        "average_confidence": avg_confidence,
        "top_crop":           top_crop,
        "top_disease":        top_disease,
        "severity_breakdown": severity_breakdown,
        "crop_breakdown":     crop_breakdown,
    }


# --------------------------------------------------------
# Delete a scan by scan_id
# --------------------------------------------------------
@app.delete("/history/{scan_id}", tags=["Scan History"])
async def delete_scan(scan_id: str, db: AsyncSession = Depends(get_db)):
    """Deletes a specific scan record by its scan_id."""
    result = await db.execute(select(ScanResult).where(ScanResult.scan_id == scan_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail=f"Scan '{scan_id}' not found.")
    await db.delete(row)
    return {"message": f"Scan '{scan_id}' deleted successfully."}

# --------------------------------------------------------
# Chatbot Integration
# --------------------------------------------------------
from pydantic import BaseModel
import os
from google import genai

class ChatRequest(BaseModel):
    message: str
    language: str = "english"

@app.post("/chat", tags=["Chatbot"])
async def chat_with_bot(request: ChatRequest):
    """
    Agricultural chatbot integration using Google Gemini.
    Translates and communicates in English, Amharic, or Afaan Oromoo.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API Key is not configured on the server")

    try:
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are AgroScan AI's helpful agricultural assistant. You help Ethiopian farmers understand crop diseases, "
            "treatments, and best farming practices. Keep your answers concise, practical, and highly relevant to Ethiopian agriculture. "
            f"You MUST respond exclusively in the following language: {request.language}."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
