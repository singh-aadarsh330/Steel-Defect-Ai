# 🧬 Model: SteelVision Neural Weights

This repository stores the localized neural network weights and evaluation metrics for the Steel Defect Detection system.

## 📊 Performance Metrics

| Metric | Score |
|---|---|
| **Validation Accuracy** | 98.24% |
| **Precision (Weighted)** | 98.50% |
| **Recall (Weighted)** | 97.90% |
| **Inference Latency** | ~120ms (CPU) |

## 📁 File Manifest

| File | Description |
|---|---|
| `model.h5` | The finalized Keras model containing the **EfficientNetV2-S** weights. |
| `model_meta.json` | JSON registry for class names, normalization factors, and model versioning. |
| `confusion_matrix.png` | Visual breakdown of class-wise precision and recall. |
| `training_history.png` | Epoch-wise accuracy and loss curves from the training session. |

## 🧠 Model Architecture

The system utilizes **EfficientNetV2-S**, a state-of-the-art backbone optimized for high accuracy with low parameter counts.

- **Input Shape**: 224x224x3 (RGB)
- **Pre-scaling**: Integrated `Rescaling` layer [0, 1].
- **Augmentation**: In-situ random flips, rotations, and contrast adjustments during training.
- **Head**: Global Average Pooling → Dense(512) → Dropout(0.3) → Dense(256) → Softmax(6).

## ⚠️ Management Guidelines

> [!WARNING]
> Do not modify the structure of `model_meta.json`. The `ModelRegistry` in the backend relies on exact key mappings for class index synchronization.

### Updating Weights
To deploy a new model version, simply overwrite `model.h5` and update the version number in `model_meta.json`. The Flask backend will auto-reload the new weights on the next request.
