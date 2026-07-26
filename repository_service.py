# ============================================================
# repository_service.py - AgriLens AI
# Disease Repository service layer.
#
# Responsibilities:
#   - Upload leaf images to Supabase Storage ("leaf-images" bucket)
#   - Persist diagnosis metadata to the "diagnoses" Postgres table
#   - Provide future retrieval hooks (verification queue, exports,
#     heatmap queries) so those features can be added later without
#     touching app.py again.
#
# Design principle: EVERY method here is fail-soft. A repository
# failure must never prevent a farmer from getting their diagnosis
# result. Callers (app.py) get back a result object indicating
# success/failure instead of an exception, except where explicitly
# noted.
# ============================================================

import os
import uuid
import logging
import datetime
from dataclasses import dataclass, field
from typing import Optional, Any

from supabase_client import get_supabase_client, LEAF_IMAGES_BUCKET, DIAGNOSES_TABLE

logger = logging.getLogger("agrilens.repository_service")


# ── Model version tracking ──────────────────────────────────
# Configurable via the MODEL_VERSION environment variable so it
# can be bumped on Render without a code change when a new model
# is deployed to the Hugging Face Space. Falls back to the current
# production model version if the env var isn't set.
CURRENT_PRODUCTION_MODEL_VERSION = "maize_model_v3"
MODEL_VERSION = os.environ.get("MODEL_VERSION", CURRENT_PRODUCTION_MODEL_VERSION)


# ── Result types ─────────────────────────────────────────────

@dataclass
class ImageUploadResult:
    success: bool
    image_url: Optional[str] = None
    storage_path: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DiagnosisSaveResult:
    success: bool
    record_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DiagnosisMetadata:
    """
    Optional metadata that can accompany a diagnosis submission.
    All fields are optional/nullable today. This struct exists so
    that new fields (GPS, farmer identity, device info, consent)
    can be threaded through the API without reshaping function
    signatures later — future-proofing for heatmaps, outbreak
    detection, and verification workflows.
    """
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    farmer_id: Optional[str] = None
    device_info: Optional[str] = None
    consent_given: Optional[bool] = None


# ── Image upload ────────────────────────────────────────────

def upload_leaf_image(image_bytes: bytes, content_type: str = "image/jpeg") -> ImageUploadResult:
    """
    Uploads a leaf image to the 'leaf-images' private Supabase
    Storage bucket under a UUID-based path (images/<uuid>.jpg).

    Never raises. Returns ImageUploadResult(success=False, ...) on
    any failure so the caller can continue the diagnosis flow.
    """
    client = get_supabase_client()
    if client is None:
        logger.error("Image upload skipped: Supabase client unavailable.")
        return ImageUploadResult(success=False, error="Supabase client unavailable")

    file_id = str(uuid.uuid4())
    storage_path = f"images/{file_id}.jpg"

    try:
        client.storage.from_(LEAF_IMAGES_BUCKET).upload(
            path=storage_path,
            file=image_bytes,
            file_options={"content-type": content_type},
        )
        logger.info(f"Storage upload success: {storage_path}")

        # Bucket is private, so we store the storage path rather than
        # a public URL. Signed URLs should be minted on demand at
        # read time (e.g. by an admin/verification tool), not stored
        # long-lived, since they expire.
        image_url = storage_path

        return ImageUploadResult(
            success=True,
            image_url=image_url,
            storage_path=storage_path,
        )

    except Exception as e:
        logger.error(f"Repository error - storage upload failed: {e}")
        return ImageUploadResult(success=False, error=str(e))


# ── Diagnosis record persistence ────────────────────────────

def save_diagnosis_record(
    image_url: Optional[str],
    prediction: str,
    confidence: float,
    language: str,
    diagnosis_status: Optional[str] = None,
    model_version: Optional[str] = None,
    metadata: Optional[DiagnosisMetadata] = None,
) -> DiagnosisSaveResult:
    """
    Inserts a row into the 'diagnoses' table for future model
    training / disease surveillance. verification_status always
    starts as 'pending' — a human verification workflow can later
    update this field.

    diagnosis_status ("confirmed" / "likely" / "uncertain") is the
    model's own confidence assessment, already computed by the
    /diagnose endpoint. It is distinct from verification_status,
    which tracks human review ("pending" / "verified" / "rejected").

    model_version identifies which AI model produced the
    prediction (e.g. "maize_model_v3"), for model monitoring,
    active learning, and retraining. Defaults to MODEL_VERSION
    (configurable via the MODEL_VERSION env var) if not provided.

    Never raises. Returns DiagnosisSaveResult(success=False, ...)
    on any failure so the caller can continue and still return the
    diagnosis result to the farmer.
    """
    client = get_supabase_client()
    if client is None:
        logger.error("Database insert skipped: Supabase client unavailable.")
        return DiagnosisSaveResult(success=False, error="Supabase client unavailable")

    metadata = metadata or DiagnosisMetadata()

    record: dict[str, Any] = {
        "image_url": image_url,
        "prediction": prediction,
        "confidence": confidence,
        "language": language,
        "diagnosis_status": diagnosis_status,
        "model_version": model_version or MODEL_VERSION,
        "verification_status": "pending",
        "created_at": datetime.datetime.utcnow().isoformat(),
        # Optional / future fields — nullable in the schema today.
        "latitude": metadata.latitude,
        "longitude": metadata.longitude,
        "state": metadata.state,
        "lga": metadata.lga,
        "farmer_id": metadata.farmer_id,
        "device_info": metadata.device_info,
        "consent_given": metadata.consent_given,
    }

    try:
        response = client.table(DIAGNOSES_TABLE).insert(record).execute()
        record_id = None
        if response.data and len(response.data) > 0:
            record_id = response.data[0].get("id")

        logger.info(f"Database insert success: diagnoses.id={record_id}")
        return DiagnosisSaveResult(success=True, record_id=record_id)

    except Exception as e:
        logger.error(f"Repository error - database insert failed: {e}")
        return DiagnosisSaveResult(success=False, error=str(e))


# ── Orchestration helper ────────────────────────────────────

def store_diagnosis(
    image_bytes: bytes,
    prediction: str,
    confidence: float,
    language: str,
    diagnosis_status: Optional[str] = None,
    model_version: Optional[str] = None,
    metadata: Optional[DiagnosisMetadata] = None,
) -> dict:
    """
    Convenience wrapper used by app.py: uploads the image, then
    saves the diagnosis record referencing it. Fully fail-soft —
    always returns a status dict, never raises.

    If image upload fails, the diagnosis record is still attempted
    with image_url=None, so at minimum the prediction + metadata
    are captured for surveillance purposes.
    """
    logger.info("Repository: beginning image upload + diagnosis save.")

    upload_result = upload_leaf_image(image_bytes)
    if not upload_result.success:
        logger.error(
            f"Repository: continuing without stored image ({upload_result.error})."
        )

    save_result = save_diagnosis_record(
        image_url=upload_result.image_url,
        prediction=prediction,
        confidence=confidence,
        language=language,
        diagnosis_status=diagnosis_status,
        model_version=model_version,
        metadata=metadata,
    )

    return {
        "image_stored": upload_result.success,
        "record_saved": save_result.success,
        "record_id": save_result.record_id,
    }


# ── Future retrieval methods (architecture placeholders) ────
#
# These are intentionally NOT implemented yet per the current
# scope. They're stubbed here so the service's public surface is
# already shaped for upcoming features:
#   - Disease heatmaps          -> get_diagnoses_by_region()
#   - GPS mapping                -> get_diagnoses_with_location()
#   - Outbreak detection          -> get_recent_diagnoses_by_disease()
#   - Human verification workflow -> get_pending_verifications() /
#                                     update_verification_status()
#   - Dataset export / retraining -> export_verified_dataset()

def get_pending_verifications(limit: int = 50):
    """Future: fetch diagnoses awaiting human verification."""
    raise NotImplementedError("Verification workflow not yet implemented.")


def update_verification_status(record_id: str, status: str):
    """Future: allow an extension officer / admin to confirm or correct a label."""
    raise NotImplementedError("Verification workflow not yet implemented.")


def get_diagnoses_by_region(state: str, lga: Optional[str] = None):
    """Future: power disease heatmaps / regional dashboards."""
    raise NotImplementedError("Regional queries not yet implemented.")


def export_verified_dataset(since: Optional[datetime.datetime] = None):
    """Future: export verified, consented records for model retraining."""
    raise NotImplementedError("Dataset export not yet implemented.")
