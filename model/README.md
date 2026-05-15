# Model: SteelVision Neural Weights

This folder contains the brain of the system: the trained neural network weights and its associated metadata.

## 📁 Files

- `model.h5`: The Keras model file containing architecture and weights.
- `model_meta.json`: Class mappings and training statistics.
- `confusion_matrix.png`: Evaluation breakdown.
- `training_history.png`: Accuracy/Loss curves.

## 🧬 Specifications

- **Architecture**: EfficientNetV2-S
- **Input**: 224x224x3 (RGB)
- **Classes**: 6 (Crazing, Inclusion, Patches, Pitted Surface, Rolled-in Scale, Scratches)
- **Accuracy**: ~98.2% on NEU-DET.

## ⚠️ Management
Do not rename `model.h5` or `model_meta.json`, as the backend and scripts expect these exact names for automated loading.
