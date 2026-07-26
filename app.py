# ============================================================
# app.py - Render FastAPI Gateway v4.2
# AgriLens AI - Lightweight API Gateway
# Calls Hugging Face Space for AI inference
# ============================================================

import io
import gc
import os
import base64
import tempfile
import json
import logging

from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from gradio_client import Client, handle_file
from typing import Optional

from utils      import (get_disease_info, build_whatsapp_link,
                        LOADING_MESSAGES)
from disease_db import DISEASE_INFO
from repository_service import store_diagnosis, DiagnosisMetadata, MODEL_VERSION

# ── Logging ──────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agrilens.app")

# ── App ───────────────────────────────────────────────────────
app = FastAPI(
    title="AgriLens AI Gateway",
    description=(
        "Lightweight API gateway for AgriLens AI. "
        "AI inference runs on Hugging Face Spaces."
    ),
    version="4.2",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_LANGUAGES = [
    "english", "pidgin", "yoruba", "hausa", "igbo"
]

UNCERTAIN_MESSAGES = {
    "english": {
        "uncertain": (
            "Analysis Inconclusive. "
            "To avoid a possible misdiagnosis, AgriLens AI could not "
            "reach a reliable confidence level from this image. "
            "Please upload a clear, well-lit photo of a single maize leaf."),
        "healthy_unclear": (
            "Leaf appears healthy or symptoms are unclear. "
            "Monitor closely and recheck in 3 to 5 days."),
        "likely": (
            "This is a likely diagnosis. "
            "Consider consulting an extension officer to confirm.")
    },
    "pidgin": {
        "uncertain": (
            "Analysis No Clear. "
            "To avoid wrong diagnosis, AgriLens AI no fit reach "
            "correct confidence level from this picture. "
            "Please upload clear, well-lit picture of one maize leaf."),
        "healthy_unclear": (
            "The leaf look healthy or the sign no clear. "
            "Keep watching am and check again after 3 to 5 days."),
        "likely": (
            "This na likely result. "
            "Consider asking extension officer to confirm.")
    },
    "yoruba": {
        "uncertain": (
            "Ayewo Ko Daju. "
            "Lati yago fun aisan ayewo, AgriLens AI ko le ri "
            "ipele igbekele to peye lati aworan yii. "
            "Jowo gbe aworan kan ti o daju, ti o ni imole to dara "
            "fun ewe agbado kan soso."),
        "healthy_unclear": (
            "Ewe dabi eni pe o ni ilera tabi ami ko han. "
            "Sakiyesi daradara ki o tun sayewo leyin ojo 3 si 5."),
        "likely": (
            "Eyi je ayewo ti o seese. "
            "Ro lati beere lowo oluko ogbin.")
    },
    "hausa": {
        "uncertain": (
            "Bincike Bai Tabbata Ba. "
            "Don gujewa kuskuren ganewar asali, AgriLens AI bai iya "
            "samun isasshen amincewa daga wannan hoton ba. "
            "Da fatan za a dora hoto mai tsabta, mai kyakkyawan haske "
            "na ganyen masara guda daya."),
        "healthy_unclear": (
            "Ganyen yana da lafiya ko alamomin ba su bayyana sosai. "
            "Ka ci gaba da kallo ka sake duba bayan kwana 3 zuwa 5."),
        "likely": (
            "Wannan shine yiwuwar ganewar cuta. "
            "Yi la'akari da shawartar jami'in fadakarwa.")
    },
    "igbo": {
        "uncertain": (
            "Nyocha Anaghị Edoziputa. "
            "Iji zere nchọpụta na-ezighi ezi, AgriLens AI enweghị ike "
            "iru ezigbo ọkwa ntụkwasị obi site na onyonyo a. "
            "Biko bulite onyonyo doro anya, nke nwere ìhè dị mma "
            "nke otu akwukwo oka."),
        "healthy_unclear": (
            "Akwukwo a dị mma ma obu ihe ọrịa adịghị ihe. "
            "Lelee ya nke ọma ma lelee ọzọ mgbe ubọchị 3 ruo 5 gachara."),
        "likely": (
            "Nke a bu nchọpụta nwere ike ibụ ya. "
            "Tulee ijụ onye ọrụ ugbo ka o kwenye.")
    }
}


# ── Health check ─────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status":  "running",
        "app":     "AgriLens AI Gateway",
        "version": "4.2",
        "message": "Trusted Maize Disease Detection for African Farmers"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.get("/loading-message", tags=["Info"])
def get_loading_message(language: str = "english"):
    msg = LOADING_MESSAGES.get(language, LOADING_MESSAGES["english"])
    return JSONResponse({"language": language, "message": msg})


@app.get("/diseases", tags=["Info"])
def list_diseases():
    result = {}
    for key, info in DISEASE_INFO.items():
        result[key] = {
            "severity":      info["severity"],
            "urgency":       info["urgency"],
            "urgency_color": info["urgency_color"],
            "urgency_icon":  info["urgency_icon"],
            "spread_note":   info["spread_note"],
            "color":         info["color"],
            "english_name":  info["english"]["name"]
        }
    return JSONResponse(result)


def call_hf_space(image_bytes: bytes) -> dict:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        print("Creating HF client...")
        hf_client = Client("Sheismuna/agrilens-ai")
        print("Client created successfully")

        print("Calling HF predict...")
        result = hf_client.predict(
            handle_file(tmp_path),
            api_name="/gradio_predict"
        )

        print("HF RAW RESULT TYPE:", type(result))
        print("HF RAW RESULT:", repr(result))

        if result is None or result == "":
            raise Exception("HF Space returned empty response")

        if isinstance(result, dict):
            return result

        if isinstance(result, str):
            return json.loads(result)

        raise Exception(f"Unexpected result type: {type(result)}: {repr(result)}")

    except Exception as e:
        import traceback
        print("HF ERROR:", str(e))
        traceback.print_exc()
        raise Exception(f"HF Space call failed: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        gc.collect()


@app.post("/diagnose", tags=["Diagnosis"])
async def diagnose(
    file: UploadFile = File(...),
    language: str = Form(default="english"),
    # ── Optional repository metadata (future-proofing) ──────
    # All optional/nullable today. Existing frontend calls that
    # don't send these fields are completely unaffected.
    latitude: Optional[float] = Form(default=None),
    longitude: Optional[float] = Form(default=None),
    state: Optional[str] = Form(default=None),
    lga: Optional[str] = Form(default=None),
    farmer_id: Optional[str] = Form(default=None),
    device_info: Optional[str] = Form(default=None),
    consent_given: Optional[bool] = Form(default=None),
):
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported language '{language}'. "
                f"Choose from: {SUPPORTED_LANGUAGES}"
            )
        )

    allowed = ["image/jpeg", "image/jpg", "image/png"]
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image."
        )

    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read image file."
        )

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG", quality=90)
    img_bytes = img_buffer.getvalue()

    logger.info("Image uploaded: preparing for prediction and repository storage.")

    try:
        hf_result = call_hf_space(img_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI inference failed: {str(e)}"
        )

    if not hf_result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {hf_result.get('error', 'Unknown')}"
        )

    label      = hf_result["label"]
    confidence = hf_result["confidence"]
    all_preds  = [
        (p["label"], p["confidence"])
        for p in hf_result["all_predictions"]
    ]

    print(f"[PREDICTION] label={label}, confidence={confidence:.3f}")

    conf_pct     = confidence * 100
    top_two_diff = (all_preds[0][1] - all_preds[1][1]) * 100 if len(all_preds) > 1 else 100
    healthy_conf = next(
        (p * 100 for l, p in all_preds if "Healthy" in l), 0)

    lang_msgs = UNCERTAIN_MESSAGES.get(language, UNCERTAIN_MESSAGES["english"])

    if conf_pct >= 80:
        diagnosis_status  = "confirmed"
        diagnosis_message = ""
    elif conf_pct >= 70 and top_two_diff >= 15:
        diagnosis_status  = "likely"
        diagnosis_message = lang_msgs["likely"]
    elif healthy_conf >= conf_pct - 10:
        diagnosis_status  = "uncertain"
        diagnosis_message = lang_msgs["healthy_unclear"]
    elif top_two_diff < 15:
        diagnosis_status  = "uncertain"
        diagnosis_message = lang_msgs["uncertain"]
    else:
        diagnosis_status  = "uncertain"
        diagnosis_message = lang_msgs["uncertain"]

    info    = get_disease_info(label, language)
    wa_link = build_whatsapp_link(info, confidence, language)

    # ── Disease Repository: persist image + diagnosis metadata ──
    # This is intentionally isolated behind a broad try/except in
    # addition to repository_service.py's own internal fail-soft
    # handling. Under no circumstances should a repository problem
    # prevent the farmer from receiving their diagnosis below.
    repository_status = {"image_stored": False, "record_saved": False, "record_id": None}
    try:
        metadata = DiagnosisMetadata(
            latitude=latitude,
            longitude=longitude,
            state=state,
            lga=lga,
            farmer_id=farmer_id,
            device_info=device_info,
            consent_given=consent_given,
        )
        repository_status = store_diagnosis(
            image_bytes=img_bytes,
            prediction=label,
            confidence=conf_pct,
            language=language,
            diagnosis_status=diagnosis_status,
            model_version=MODEL_VERSION,
            metadata=metadata,
        )
    except Exception as e:
        # Belt-and-braces: even an unexpected error constructing
        # metadata or calling the service must not break diagnosis.
        logger.error(f"Repository error - unexpected failure, continuing diagnosis: {e}")

    return JSONResponse({
        "success":  True,
        "language": language,
        "diagnosis_status":  diagnosis_status,
        "diagnosis_message": diagnosis_message,
        "prediction": {
            "disease":         info["name"],
            "raw_label":       label,
            "confidence":      round(conf_pct, 2),
            "severity":        info["severity"],
            "urgency":         info["urgency"],
            "urgency_label":   info["urgency_label"],
            "urgency_message": info["urgency_message"],
            "urgency_color":   info["urgency_color"],
            "urgency_icon":    info["urgency_icon"],
            "spread_note":     info["spread_note"],
        },
        "guidance": {
            "symptoms":       info["symptoms"],
            "what_it_is":     info["what_it_is"],
            "what_to_do":     info["what_to_do"],
            "prevention":     info["prevention"],
            "extension_note": info["extension_note"],
            "treatment":      info["what_to_do"],
        },
        "share": {"whatsapp_link": wa_link},
        "all_predictions": [
            {"label": lbl, "confidence": round(prob * 100, 2)}
            for lbl, prob in all_preds
        ],
        "repository": repository_status,
    })


@app.post("/audio", tags=["Audio"])
async def audio_diagnosis(
    text:     str = Form(...),
    language: str = Form(default="english")
):
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{language}'."
        )

    lang_codes = {
        "english": "en",
        "pidgin":  "en",
        "yoruba":  "yo",
        "hausa":   "ha",
        "igbo":    "ig"
    }

    try:
        from gtts import gTTS
        tts = gTTS(
            text=text,
            lang=lang_codes.get(language, "en"),
            slow=False
        )
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        audio_b64 = base64.b64encode(buf.read()).decode("utf-8")

        return JSONResponse({
            "success":   True,
            "language":  language,
            "audio_b64": audio_b64,
            "format":    "mp3",
            "encoding":  "base64"
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Audio failed: {str(e)}"
        )