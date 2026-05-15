"""
Organize NEU-DET dataset into flat class-folder structure for Keras.

Copies images from:
    dataset/NEU-DET/train/images/<class>/
    dataset/NEU-DET/validation/images/<class>/
Into:
    dataset/<class>/

This merges train + validation into one pool so that train.py can
re-split them with its own train/val ratio.
"""

import os
import shutil

DATASET_ROOT = os.path.join(".", "dataset")
NEU_DET_DIR  = os.path.join(DATASET_ROOT, "NEU-DET")

CLASSES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
]

SPLITS = ["train", "validation"]


def main():
    total_copied = 0

    for cls in CLASSES:
        dest_dir = os.path.join(DATASET_ROOT, cls)
        os.makedirs(dest_dir, exist_ok=True)

        for split in SPLITS:
            src_dir = os.path.join(NEU_DET_DIR, split, "images", cls)
            if not os.path.isdir(src_dir):
                print(f"[WARN] Not found: {src_dir}")
                continue

            files = [f for f in os.listdir(src_dir)
                     if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]

            for fname in files:
                src = os.path.join(src_dir, fname)
                dst = os.path.join(dest_dir, fname)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    total_copied += 1

        count = len(os.listdir(dest_dir))
        print(f"  {cls:<20s} → {count} images")

    print(f"\n✅  Organized {total_copied} images into {DATASET_ROOT}/")


if __name__ == "__main__":
    main()
