# Scripts: Automation & Training

Utility scripts for training models and performing standalone inference.

## 📁 Files

- `train.py`: The Grandmaster training pipeline. Supports two-phase transfer learning and hyperparameter tuning.
- `predict.py`: CLI tool for rapid local inference.
- `organize_dataset.py`: Script to prepare raw NEU-DET files for the training pipeline.

## 🚀 Usage

### Training
```bash
python scripts/train.py --epochs 50 --batch 16 --finetune
```

### CLI Inference
```bash
python scripts/predict.py path/to/sample.jpg
```

## ⚠️ Notes
All scripts assume they are being run from the root of the project.
