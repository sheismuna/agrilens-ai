# ============================================================
# supabase_client.py - AgriLens AI
# Central Supabase client factory.
#
# Loads credentials from environment variables and exposes a
# single, lazily-initialized Supabase client for the whole app.
#
# SECURITY NOTE:
#   SUPABASE_SERVICE_KEY is the *service role* key. It bypasses
#   Row Level Security and must NEVER be exposed to the frontend
#   or logged. It should only ever live in the backend's env vars
#   (e.g. Render's environment variable settings), never committed
#   to source control.
# ============================================================

import os
import logging

from supabase import create_client, Client

logger = logging.getLogger("agrilens.supabase_client")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

_client: Client | None = None


def get_supabase_client() -> Client | None:
    """
    Returns a lazily-initialized, process-wide Supabase client.

    Returns None (instead of raising) if credentials are missing or
    client creation fails, so that callers can degrade gracefully
    (repository features become a no-op) rather than crashing the
    whole diagnosis flow. See repository_service.py for how this is
    used defensively.
    """
    global _client

    if _client is not None:
        return _client

    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        logger.error(
            "Supabase not configured: missing SUPABASE_URL or "
            "SUPABASE_SERVICE_KEY environment variables. "
            "Repository features will be disabled."
        )
        return None

    try:
        _client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        logger.info("Supabase client initialized successfully.")
        return _client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None


# Bucket / table names centralized here so they aren't magic
# strings scattered across the codebase.
LEAF_IMAGES_BUCKET = "leaf-images"
DIAGNOSES_TABLE = "diagnoses"