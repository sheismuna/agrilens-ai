# ============================================================
# config.py
# AgriLens AI - Central Configuration
# Works locally (Windows paths) and on Render (Linux paths)
# ============================================================

import os

# Base directory - works on both Windows and Linux
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # Model files - uses environment variable if set,
    # otherwise looks in the same folder as this file
    "model_save_path": os.environ.get(
        "MODEL_SAVE_PATH",
        os.path.join(BASE_DIR, "agrilens_model.h5")
    ),
    "labels_save_path": os.environ.get(
        "LABELS_SAVE_PATH",
        os.path.join(BASE_DIR, "agrilens_labels.json")
    ),

    # Image size for model input
    "img_size": (224, 224),
}