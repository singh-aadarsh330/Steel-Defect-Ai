# 🛠️ Scripts: SteelVision Automation Suite

A collection of high-performance Python utilities for training models, performing batch inference, and dataset management.

## 📁 Tool Inventory

| Script | Purpose |
|---|---|
| `train.py` | The **Grandmaster** training pipeline using EfficientNetV2-S. |
| `predict.py` | A CLI-based inference tool for rapid local testing and validation. |
| `organize_dataset.py` | Automates the sorting of raw NEU-DET files into class folders. |

## 🚀 Script Usage

### 🏋️ Training the Model
The `train.py` script supports multi-phase transfer learning and automated checkpointing.
```bash
python scripts/train.py --epochs 50 --batch 16 --finetune
```
*Key Features: EarlyStopping, ReduceLROnPlateau, and Label Smoothing (0.1).*

### 🔍 Local Inference
Test the model on a single image without starting the Flask server:
```bash
python scripts/predict.py path/to/steel_sample.jpg
```

### 🧹 Dataset Organization
Prepare raw files for training:
```bash
python scripts/organize_dataset.py --source /path/to/raw --dest dataset/
```

## ⚙️ Technical Requirements
All scripts require the root environment dependencies:
```bash
pip install -r requirements.txt
```

---
> [!NOTE]
> All scripts are designed to be executed from the **root directory** of the project to maintain path consistency for models and datasets.
