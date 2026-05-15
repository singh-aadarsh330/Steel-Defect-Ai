"""
Steel Surface Defect Classification — Inference Script
======================================================
Predict the defect class for one or more steel surface images.

Usage:
    python predict.py image.jpg
    python predict.py img1.jpg img2.png img3.bmp
    python predict.py --model model/model.h5 image.jpg
"""

import argparse
import json
import os
import sys

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# ──────────────────────────────────────────────
# Constants / Defaults
# ──────────────────────────────────────────────
DEFAULT_MODEL_PATH = os.path.join(".", "model", "model.h5")
DEFAULT_META_PATH  = os.path.join(".", "model", "model_meta.json")
IMG_SIZE           = (224, 224)

FALLBACK_CLASSES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
]


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def load_class_names(meta_path):
    if os.path.isfile(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        names = meta.get("class_names", FALLBACK_CLASSES)
        print(f"[INFO] Loaded {len(names)} class names from {meta_path}")
        return names
    print("[WARN] Metadata not found — using fallback class names.")
    return FALLBACK_CLASSES


def preprocess_image(img_path):
    img = keras_image.load_img(img_path, target_size=IMG_SIZE)
    arr = keras_image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    # REDUNDANT: preprocess_input is already part of the model's computation graph
    # arr = preprocess_input(arr)
    return arr


def predict_single(model, img_path, class_names):
    arr = preprocess_image(img_path)
    probs = model.predict(arr, verbose=0)[0]

    top_idx = int(np.argmax(probs))
    top_class = class_names[top_idx]
    top_conf = float(probs[top_idx])

    sorted_idx = np.argsort(probs)[::-1]
    top_k = [
        {"class": class_names[i], "confidence": float(probs[i])}
        for i in sorted_idx
    ]

    return {
        "file": img_path,
        "prediction": top_class,
        "confidence": round(top_conf, 4),
        "all_scores": top_k,
    }


def print_result(result):
    print(f"\n{'─' * 50}")
    print(f"  File       : {result['file']}")
    print(f"  Prediction : {result['prediction']}")
    print(f"  Confidence : {result['confidence']:.2%}")
    print(f"{'─' * 50}")
    print("  All scores:")
    for entry in result["all_scores"]:
        bar = "█" * int(entry["confidence"] * 30)
        print(f"    {entry['class']:<20s} {entry['confidence']:6.2%}  {bar}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Predict steel surface defects")
    parser.add_argument("images", nargs="+", help="Path(s) to input image(s)")
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH,
                        help=f"Path to .h5 model (default: {DEFAULT_MODEL_PATH})")
    parser.add_argument("--meta", default=DEFAULT_META_PATH,
                        help="Path to model_meta.json")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")
    args = parser.parse_args()

    if not os.path.isfile(args.model):
        print(f"[ERROR] Model not found at '{args.model}'. Train first with train.py.")
        sys.exit(1)

    print(f"[INFO] Loading model from {args.model} …")

    model = tf.keras.models.load_model(
        args.model,
        custom_objects={"preprocess_input": preprocess_input},
        compile=False
    )

    class_names = load_class_names(args.meta)

    results = []
    for img_path in args.images:
        if not os.path.isfile(img_path):
            print(f"[WARN] File not found, skipping: {img_path}")
            continue
        result = predict_single(model, img_path, class_names)
        results.append(result)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print_result(r)

    print(f"\n✅  {len(results)} image(s) processed.")


if __name__ == "__main__":
    main()