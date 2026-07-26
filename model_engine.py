# ============================================================
# model_engine.py (IMPROVED - BALANCED TOLERANCE + ERROR HANDLING)
# AgriLens AI - Model Loading and Prediction Engine
# Crash-proof validation gate with graceful error recovery
# ============================================================
import json
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions
from config import CONFIG


def load_inference_model():
    model = load_model(CONFIG["model_save_path"], compile=False)
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"])
    return model


def load_label_map():
    with open(CONFIG["labels_save_path"]) as f:
        return json.load(f)


def predict(model, label_map, img: Image.Image):
    img_resized = img.resize(CONFIG["img_size"])
    arr = np.array(img_resized, dtype=np.float32)
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)

    preds      = model.predict(arr, verbose=0)[0]
    top_idx    = int(np.argmax(preds))
    top_label  = label_map[str(top_idx)]
    confidence = float(preds[top_idx])
    all_preds  = sorted(
        [(label_map[str(i)], float(preds[i]))
         for i in range(len(preds))],
        key=lambda x: x[1],
        reverse=True)
    return top_label, confidence, all_preds


# ============================================================
# MAIZE LEAF VALIDATION GATE - balanced acceptance approach
# Allow real plants through while rejecting obvious non-plants
# NOW WITH CRASH-PROOF ERROR HANDLING
# ============================================================

_imagenet_model = MobileNetV2(weights="imagenet")

MAIZE_POSITIVE_KEYWORDS = [
    'corn', 'maize', 'cob', 'ear_of_corn',
]

PLANT_KEYWORDS = [
    'leaf', 'plant', 'vegetable', 'flower', 'fungus',
    'mushroom', 'broccoli', 'cabbage', 'cauliflower',
    'zucchini', 'cucumber', 'banana', 'fig'
]

NONPLANT_KEYWORDS = [
    'dog', 'cat', 'puppy', 'kitten', 
    'laptop', 'notebook', 'monitor', 'desktop_computer', 'screen',
    'cellular_telephone', 'iphone', 'television', 'tv', 'remote_control',
    'keyboard', 'mouse', 'printer', 'projector',
    'car', 'automobile', 'truck', 'bus', 'motorcycle', 'bicycle',
    'building', 'house', 'window', 'door', 'wall', 'room',
    'envelope', 'website', 'web_site', 'menu', 'book_jacket',
    'packet', 'logo', 'street_sign', 'traffic_light',
    'binder', 'paper', 'page', 'comic_book', 'crossword',
    'sofa', 'chair', 'table', 'bed', 'curtain', 'dog', 'cat', 'puppy', 'kitten',
]

def _green_ratio(img_array):
    """Calculate ratio of green pixels in HSV space."""
    try:
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        lower = np.array([20, 25, 25])
        upper = np.array([100, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        return mask.sum() / (mask.shape[0] * mask.shape[1] * 255)
    except Exception as e:
        print(f"Warning: _green_ratio failed: {e}")
        return 0.0


def _blur_score(img_array):
    """Calculate image sharpness using Laplacian variance."""
    try:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    except Exception as e:
        print(f"Warning: _blur_score failed: {e}")
        return 0.0


def _edge_density(img_array):
    """Calculate edge density using Canny edge detection."""
    try:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return edges.sum() / (edges.shape[0] * edges.shape[1] * 255)
    except Exception as e:
        print(f"Warning: _edge_density failed: {e}")
        return 0.0


def _white_background_ratio(img_array):
    """Calculate ratio of white pixels."""
    try:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        white_mask = gray > 235
        return white_mask.sum() / white_mask.size
    except Exception as e:
        print(f"Warning: _white_background_ratio failed: {e}")
        return 0.0


def _uniform_color_ratio(img_array):
    """Calculate how uniform the color distribution is (logo detection)."""
    try:
        small = cv2.resize(img_array, (64, 64))
        pixels = small.reshape(-1, 3)
        quantized = (pixels // 16) * 16
        _, counts = np.unique(quantized, axis=0, return_counts=True)
        return counts.max() / pixels.shape[0]
    except Exception as e:
        print(f"Warning: _uniform_color_ratio failed: {e}")
        return 0.0


def _elongation_score(img_array):
    """
    Detects whether the dominant green region has a long, narrow
    leaf-like shape rather than a blob (animal body, face, etc).
    Returns a value 0.0-1.0; higher = more leaf-shaped.
    """
    try:
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        lower = np.array([20, 25, 25])
        upper = np.array([100, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return 0.0

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area < (mask.shape[0] * mask.shape[1] * 0.05):
            return 0.0

        x, y, w, h = cv2.boundingRect(largest)
        if w == 0 or h == 0:
            return 0.0

        aspect = max(w, h) / max(min(w, h), 1)
        score = min((aspect - 1.0) / 1.5, 1.0)
        return max(score, 0.0)
    except Exception as e:
        print(f"Warning: _elongation_score failed: {e}")
        return 0.0


def _imagenet_top5(img_array):
    """
    Get top-5 ImageNet predictions for an image.
    CRASH-PROOF: returns empty list on any error instead of crashing.
    """
    try:
        # Ensure image is proper dtype and format
        if not isinstance(img_array, np.ndarray):
            img_array = np.array(img_array)
        
        # Convert to float32 if needed
        if img_array.dtype != np.float32:
            img_array = img_array.astype(np.float32)
        
        # Handle grayscale images (convert to RGB)
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:  # RGBA to RGB
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # Preprocess for ImageNet
        arr = preprocess_input(img_array)
        arr = np.expand_dims(arr, axis=0)
        
        # Predict with error handling
        preds = _imagenet_model.predict(arr, verbose=0)
        
        # Safely decode predictions
        decoded = decode_predictions(preds, top=5)[0]
        return decoded
        
    except Exception as e:
        print(f"Warning: ImageNet prediction failed: {type(e).__name__}: {e}")
        print(f"  Image shape: {img_array.shape if isinstance(img_array, np.ndarray) else 'unknown'}")
        print(f"  Image dtype: {img_array.dtype if isinstance(img_array, np.ndarray) else 'unknown'}")
        # Return empty list = no ImageNet match = neutral in scoring
        return []


def check_maize_leaf(img: Image.Image, threshold: float = 0.48):
    """
    BALANCED gate: relaxed tolerance for better plant detection.
    Rejects only obvious non-plants while accepting varied real leaves.
    NOW CRASH-PROOF: gracefully handles all image types.

    Key improvements:
    - Fixed scoring weights to sum to 1.0
    - Relaxed hard-reject thresholds for real-world plants
    - Crash-proof error handling for all components
    - Graceful degradation when any check fails

    Returns:
        is_valid    (bool)
        score       (float) - maize-leaf confidence score (0.0-1.0)
        diagnostics (dict)
    """
    try:
        img_resized = img.resize(CONFIG["img_size"])
        img_array = np.array(img_resized)
    except Exception as e:
        return False, 0.0, {
            "reason": "image_load_failed",
            "error": str(e)
        }

    # Get ImageNet predictions (crash-proof)
    decoded = _imagenet_top5(img_array)
    top_labels = [(label.lower(), float(prob)) for _, label, prob in decoded] if decoded else []

    # Hard reject 1: VERY confident non-plant match
    # Only reject if ImageNet is VERY sure it's a non-plant
    for label, prob in top_labels:
        if any(k in label for k in NONPLANT_KEYWORDS) and prob > 0.55:
            return False, 0.0, {
                "reason": "imagenet_nonplant_match",
                "detected_as": label,
                "confidence": round(prob, 3)
            }

    # Calculate all metrics with error handling
    white_bg = _white_background_ratio(img_array)
    uniform  = _uniform_color_ratio(img_array)
    green    = _green_ratio(img_array)
    blur     = _blur_score(img_array)
    edges    = _edge_density(img_array)
    elong    = _elongation_score(img_array)

    # Hard reject 2: VERY flat white background
    if white_bg > 0.50:
        return False, 0.0, {
            "reason": "flat_white_background",
            "white_ratio": round(white_bg, 3),
        }

    # Hard reject 3: flat graphic (uniform color, very low green)
    if uniform > 0.55 and green < 0.18:
        return False, 0.0, {
            "reason": "flat_graphic",
            "uniform_ratio": round(uniform, 3),
            "green_ratio": round(green, 3),
        }

    # Hard reject 4: insufficient green coverage
    if green < 0.07:
        return False, 0.0, {
            "reason": "insufficient_green_coverage",
            "green_ratio": round(green, 3),
        }

    # Positive evidence scoring
    maize_match = any(
        any(k in label for k in MAIZE_POSITIVE_KEYWORDS) and prob > 0.05
        for label, prob in top_labels
    )
    plant_match = any(
        any(k in label for k in PLANT_KEYWORDS) and prob > 0.05
        for label, prob in top_labels
    )

    if maize_match:
        imagenet_score = 1.0
    elif plant_match:
        imagenet_score = 0.7
    else:
        imagenet_score = 0.35

    # Component scoring with normalized weights (sum to 1.0)
    green_score = min(green / 0.30, 1.0)
    blur_ok     = min(blur / 40, 1.0)
    edge_score  = min(edges / 0.04, 1.0)
    elong_score = min(elong / 0.35, 1.0)

    # CORRECTED WEIGHTS: sum to 1.0
    score = (
        0.25 * green_score +
        0.20 * elong_score +
        0.20 * blur_ok +
        0.20 * edge_score +
        0.15 * imagenet_score
    )

    diagnostics = {
        "green_ratio": round(green, 3),
        "blur_score": round(blur, 1),
        "edge_density": round(edges, 3),
        "elongation_score": round(elong, 3),
        "white_background_ratio": round(white_bg, 3),
        "uniform_color_ratio": round(uniform, 3),
        "imagenet_top1": top_labels[0][0] if top_labels else None,
        "imagenet_top1_confidence": round(top_labels[0][1], 3) if top_labels else 0,
        "maize_keyword_match": maize_match,
        "plant_keyword_match": plant_match,
        "maize_leaf_score": round(score, 3),
        # Component contributions (for debugging)
        "green_component": round(0.25 * green_score, 3),
        "elongation_component": round(0.20 * elong_score, 3),
        "blur_component": round(0.20 * blur_ok, 3),
        "edge_component": round(0.20 * edge_score, 3),
        "imagenet_component": round(0.15 * imagenet_score, 3),
    }

    return score >= threshold, score, diagnostics