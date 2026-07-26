# ============================================================
# utils.py
# AgriLens AI — Utility & Helper Functions
# Updated: Urgency fully translated, optimized preprocessing
# ============================================================

import io
import base64
import urllib.parse
from datetime import datetime
from PIL import Image

from disease_db import DISEASE_INFO, LABEL_ALIAS

# ── Urgency translations ─────────────────────────────────────
URGENCY_TRANSLATIONS = {
    "Corn_Common_Rust": {
        "english": {
            "urgency_label":   "Treat Soon — This Week",
            "urgency_message": "Act before it spreads further"
        },
        "pidgin": {
            "urgency_label":   "Treat Am This Week",
            "urgency_message": "Do something before e spread more"
        },
        "yoruba": {
            "urgency_label":   "Tọju Ni Ọsẹ Yii",
            "urgency_message": "Ṣe nkan ki o to tàn sii"
        },
        "hausa": {
            "urgency_label":   "Yi Magani Wannan Mako",
            "urgency_message": "Yi aiki kafin ta yadu"
        },
        "igbo": {
            "urgency_label":   "Gwoo N'izu A",
            "urgency_message": "Mee ihe tupu ọ gbasa"
        }
    },
    "Corn_Northern_Leaf_Blight": {
        "english": {
            "urgency_label":   "Treat Immediately This Week",
            "urgency_message": "Risk of serious yield loss"
        },
        "pidgin": {
            "urgency_label":   "Treat Am Now Now",
            "urgency_message": "E fit destroy your harvest"
        },
        "yoruba": {
            "urgency_label":   "Tọju Lẹsẹkẹsẹ",
            "urgency_message": "Ewu ipadanu ọja nla"
        },
        "hausa": {
            "urgency_label":   "Yi Magani Nan Take",
            "urgency_message": "Haɗarin asarar girbi"
        },
        "igbo": {
            "urgency_label":   "Gwoo Ozugbo",
            "urgency_message": "Ihe ize ndụ maka ọmụmụ"
        }
    },
    "Corn_Maize_Streak": {
        "english": {
            "urgency_label":   "CRITICAL — Remove Infected Plants Now",
            "urgency_message": "Viral disease — NO cure. Act immediately"
        },
        "pidgin": {
            "urgency_label":   "EMERGENCY — Comot Sick Plants Now",
            "urgency_message": "Virus sickness — no medicine. Act fast"
        },
        "yoruba": {
            "urgency_label":   "PAJAWIRI — Yọ Irugbin Aisan Kuro",
            "urgency_message": "Arun ọlọjẹ — ko si arowoto. Ṣe ni kiakia"
        },
        "hausa": {
            "urgency_label":   "GAGGAWA — Cire Tsiron Da Ya Kamu Nan Take",
            "urgency_message": "Cuta ta kwayar cuta — babu magani. Yi aiki yanzu"
        },
        "igbo": {
            "urgency_label":   "IHE IZE NDU — Wepu Osisi Oria Ugbua",
            "urgency_message": "Oria virus — enwegh ogwu. Mee ihe ngwa ngwa"
        }
    },
    "Corn_Healthy": {
        "english": {
            "urgency_label":   "Your Crop Looks Healthy",
            "urgency_message": "Keep monitoring regularly"
        },
        "pidgin": {
            "urgency_label":   "Your Maize Dey Fine",
            "urgency_message": "Keep checking am regularly"
        },
        "yoruba": {
            "urgency_label":   "Irugbin Rẹ Dara",
            "urgency_message": "Máa ṣàyẹ̀wò rẹ nigbagbogbo"
        },
        "hausa": {
            "urgency_label":   "Gonarku Tana Da Lafiya",
            "urgency_message": "Ci gaba da dubawa kullum"
        },
        "igbo": {
            "urgency_label":   "Oka Gi Di Mma",
            "urgency_message": "Gaa n'ihu ilelee ya mgbe nile"
        }
    }
}

# ── Loading messages per language ────────────────────────────
LOADING_MESSAGES = {
    "english": "Analyzing maize leaf...",
    "hausa":   "Ana nazarin ganyen masara...",
    "yoruba":  "N ṣe ayẹwo ewe agbado...",
    "igbo":    "Na-enyocha akwukwo oka...",
    "pidgin":  "Dey check maize leaf..."
}


def get_disease_info(label: str,
                     language: str = "english") -> dict:
    """
    Resolve a raw model label to full disease info.
    Urgency is based on disease severity NOT confidence.
    MSD is always RED regardless of confidence score.
    """
    key      = LABEL_ALIAS.get(label,
                   LABEL_ALIAS.get(
                       label.replace(" ", "_"),
                       "Corn_Healthy"))
    info     = DISEASE_INFO.get(key,
                   DISEASE_INFO["Corn_Healthy"])
    lang_info = info.get(language, info["english"])

    # Get translated urgency
    urgency_trans = URGENCY_TRANSLATIONS.get(
        key, URGENCY_TRANSLATIONS["Corn_Healthy"])
    urgency_lang  = urgency_trans.get(
        language, urgency_trans["english"])

    return {
        "name":            lang_info["name"],
        "what_it_is":      lang_info["what_it_is"],
        "symptoms":        lang_info["symptoms"],
        "what_to_do":      lang_info["what_to_do"],
        "prevention":      lang_info["prevention"],
        "extension_note":  lang_info["extension_note"],
        # Urgency — disease based, fully translated
        "urgency":         info["urgency"],
        "urgency_label":   urgency_lang["urgency_label"],
        "urgency_message": urgency_lang["urgency_message"],
        "urgency_color":   info["urgency_color"],
        "urgency_icon":    info["urgency_icon"],
        "spread_note":     info["spread_note"],
        "severity":        info["severity"],
        "color":           info["color"],
        "accent":          info["accent"],
        "border":          info["border"],
    }


def img_to_b64(img: Image.Image,
               max_size: tuple = (300, 300)) -> str:
    """
    Convert PIL Image to base64 JPEG string
    for embedding in HTML.
    """
    img_copy = img.copy()
    img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img_copy.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def build_whatsapp_link(info: dict,
                        confidence: float,
                        language: str) -> str:
    """
    Build pre-filled wa.me WhatsApp share link
    from diagnosis result.
    """
    conf_pct = confidence * 100
    msg = (
        f"🌱 *AgriLens AI Diagnosis*\n\n"
        f"🔬 Disease: *{info['name']}*\n"
        f"📊 Confidence: *{conf_pct:.1f}%*\n"
        f"⚠️ Severity: *{info['severity']}*\n"
        f"{info['urgency_icon']} "
        f"*{info['urgency_label']}*\n\n"
        f"🔍 *What It Looks Like:*\n"
        f"{info['symptoms']}\n\n"
        f"💊 *What To Do:*\n"
        f"{info['what_to_do']}\n\n"
        f"🌱 *Prevention:*\n"
        f"{info['prevention']}\n\n"
        f"🌍 Language: {language.capitalize()}\n"
        f"🕐 {datetime.now().strftime('%d %b %Y %H:%M')}\n\n"
        f"_Powered by AgriLens AI — "
        f"Trusted Maize Disease Detection "
        f"for African Farmers_"
    )
    return f"https://wa.me/?text={urllib.parse.quote(msg)}"