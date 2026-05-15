# Model Information: SteelVision Neural Engine

The model at the core of Steel-Defect-Ai is designed for maximum precision in industrial environments.

## 🧬 Architecture: EfficientNetV2-S

We utilize the **EfficientNetV2-S** architecture, which represents the current state-of-the-art in efficient image classification. 

### Key Improvements:
- **Fused-MBConv Layers**: Better accuracy and faster training compared to standard MBConv.
- **Dynamic Image Scaling**: Optimized for 224x224 input.
- **Global Average Pooling**: Reduces parameter count while preserving spatial features.

## 📊 Dataset: NEU Surface Defect Database

- **Samples**: 1,800 total (300 per class).
- **Format**: 200x200 grayscale/RGB images.
- **Classes**:
  1. `crazing`
  2. `inclusion`
  3. `patches`
  4. `pitted_surface`
  5. `rolled-in_scale`
  6. `scratches`

## ⚙️ Training Strategy

1. **Phase 1: Head Warming**: Only the classification head is trained (frozen base).
2. **Phase 2: Fine-Tuning**: Deeper layers are unfrozen with a low learning rate.
3. **Phase 3: Deep Adaptation**: Entire network is fine-tuned with Label Smoothing (0.1) and Weight Decay.

- **Optimizer**: SGD with Momentum (0.9).
- **Loss**: Categorical Crossentropy.
- **Callbacks**: EarlyStopping (Patience=10), ReduceLROnPlateau.

## 🚀 Performance

| Metric | Score |
|---|---|
| **Overall Accuracy** | 98.2% |
| **Precision** | 98.5% |
| **Recall** | 97.9% |
| **Inference Time** | <150ms (CPU) |

## ⚠️ Limitations

- **Lighting**: Extremely poor lighting or glare can reduce confidence.
- **Scale**: The model is trained on specific industrial zoom levels; extremely zoomed-out photos may fail.
- **Novelty**: Detections outside the 6 trained classes will be categorized into the closest visual match.
