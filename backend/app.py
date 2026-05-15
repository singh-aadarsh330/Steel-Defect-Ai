"""
Steel Surface Defect Detection — Enhanced Flask Backend
======================================================
"""

import argparse
import json
import logging
import os
import tempfile
import traceback
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    from tensorflow.keras.preprocessing import image as keras_image
except ImportError as exc:
    raise SystemExit("[ERROR] TensorFlow not installed.") from exc

# ── Configuration ──────────────────────────────────────────────────────────
# Dynamically find the root regardless of where this script is run
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Check common locations for the model
POTENTIAL_MODEL_PATHS = [
    PROJECT_ROOT / "model" / "model.h5",
    BASE_DIR / "model" / "model.h5",
    Path("model/model.h5"),
    Path("../model/model.h5")
]

MODEL_PATH = next((p for p in POTENTIAL_MODEL_PATHS if p.exists()), POTENTIAL_MODEL_PATHS[0])
META_PATH = MODEL_PATH.parent / "model_meta.json"

IMG_SIZE = (224, 224)

DEFECT_INFO = {
    "crazing": {
        "title": "Crazing",
        "i18n_key": "defect_crazing",
        "standard": "ISO 14488 / ASTM E155",
        "description": "Network of fine cracks on the surface, often caused by thermal stress or excessive cold work. Critical for structural fatigue assessment.",
        "severity": "Medium"
    },
    "inclusion": {
        "title": "Inclusion",
        "i18n_key": "defect_inclusion",
        "standard": "ISO 4967 / ASTM E45",
        "description": "Non-metallic particles trapped in the steel. Significant impact on ductility and fatigue life in global manufacturing standards.",
        "severity": "High"
    },
    "patches": {
        "title": "Patches",
        "i18n_key": "defect_patches",
        "standard": "ISO 8501-1",
        "description": "Localized areas with different texture or color. Often cosmetic but can indicate uneven cooling in industrial batches.",
        "severity": "Low"
    },
    "pitted_surface": {
        "title": "Pitted Surface",
        "i18n_key": "defect_pitting",
        "standard": "ISO 9223 / ASTM G46",
        "description": "Small cavities caused by corrosion or mechanical damage. High risk of localized failure in pressurized applications.",
        "severity": "High"
    },
    "rolled-in_scale": {
        "title": "Rolled-in Scale",
        "i18n_key": "defect_scale",
        "standard": "ISO 12671",
        "description": "Oxide scale pressed into the surface during hot rolling. Affects surface finish and subsequent coating adhesion.",
        "severity": "Medium"
    },
    "scratches": {
        "title": "Scratches",
        "i18n_key": "defect_scratches",
        "standard": "ISO 4287",
        "description": "Linear abrasions caused by mechanical contact. Monitored for surface roughness compliance in precision engineering.",
        "severity": "Medium"
    }
}

# ──────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────
# Model Registry
# ──────────────────────────────────────────────────────────────────────────
class ModelRegistry:
    _model = None
    _class_names = None

    @classmethod
    def load(cls):
        if cls._model is not None: return
        if not MODEL_PATH.exists():
            log.error(f"Model not found at {MODEL_PATH}")
            return

        log.info(f"Loading model from {MODEL_PATH}...")
        cls._model = tf.keras.models.load_model(
            str(MODEL_PATH),
            custom_objects={"preprocess_input": preprocess_input}
        )
        
        if META_PATH.exists():
            with open(META_PATH) as f:
                meta = json.load(f)
            cls._class_names = meta.get("class_names")
        
        if not cls._class_names:
            cls._class_names = sorted(list(DEFECT_INFO.keys()))
        log.info("Model loaded successfully")

    @classmethod
    def predict(cls, img_path):
        if cls._model is None: cls.load()
        img = keras_image.load_img(img_path, target_size=IMG_SIZE)
        arr = keras_image.img_to_array(img)
        arr = np.expand_dims(arr, axis=0)
        # Internal model layer 'mobilenetv2_preprocess' handles the scaling
        # arr = preprocess_input(arr)
        
        probs = cls._model.predict(arr, verbose=0)[0]
        top_idx = int(np.argmax(probs))
        
        results = []
        for i, p in enumerate(probs):
            cls_name = cls._class_names[i]
            results.append({
                "class": cls_name,
                "confidence": float(p),
                "info": DEFECT_INFO.get(cls_name, {})
            })
        
        # Sort by confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results

# ──────────────────────────────────────────────────────────────────────────
# Flask App
# ──────────────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "model_loaded": ModelRegistry._model is not None})

@app.route("/api/defects", methods=["GET"])
def get_defects():
    """Return static information about supported defects."""
    return jsonify(DEFECT_INFO)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files["image"]
    ext = Path(file.filename).suffix.lower()
    
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp_path = tmp.name
        file.save(tmp_path)
    
    try:
        results = ModelRegistry.predict(tmp_path)
        top = results[0]
        return jsonify({
            "defect": top["class"],
            "confidence": top["confidence"],
            "info": top["info"],
            "all_scores": results
        })
    except Exception:
        log.error(traceback.format_exc())
        return jsonify({"error": "Prediction failed"}), 500
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    ModelRegistry.load()
    app.run(host="0.0.0.0", port=5000, debug=False)