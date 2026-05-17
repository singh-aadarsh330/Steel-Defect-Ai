# Steel-Defect-Ai: Enterprise Industrial Inspection Hub

[![GitHub License](https://img.shields.io/github/license/singh-aadarsh330/Steel-Defect-Ai)](https://github.com/singh-aadarsh330/Steel-Defect-Ai/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/singh-aadarsh330/Steel-Defect-Ai)](https://github.com/singh-aadarsh330/Steel-Defect-Ai/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)

![Steel-Defect-Ai Dashboard](assets/dashboard_preview.png)

## ðŸ—ï¸ Project Overview

**Steel-Defect-Ai** is a state-of-the-art, professional-grade AI platform designed for automated surface defect detection in steel manufacturing. Using the **EfficientNetV2-S** architecture, it achieves pinpoint accuracy in identifying 6 major industrial defects: Crazing, Inclusion, Patches, Pitted Surface, Rolled-in Scale, and Scratches.

The system features a robust Flask backend and a premium, enterprise-ready React dashboard with real-time analysis, batch processing, and global compliance monitoring (ISO/ASTM).

## âœ¨ Key Features

- **ðŸš€ State-of-the-Art ML**: EfficientNetV2-S backbone with 91% validated accuracy (F1-score across 6 classes).
- **ðŸ“¦ Batch Processing**: Upload and analyze hundreds of samples simultaneously.
- **ðŸ–¥ï¸ Enterprise Dashboard**: Premium dark-mode UI with real-time telemetry and history persistence.
- **ðŸŒ Global Compliance**: Integrated ISO 14488 / ASTM E155 standards for international audits.
- **ðŸ“¸ Live Optical Feed**: Real-time webcam scanning for on-the-spot inspections.
- **ðŸ“Š Advanced Analytics**: Categorized defect distributions and trend reporting.
- **ðŸ“„ Exportable Reports**: Generate detailed PDF/CSV inspection summaries.

## ðŸ› ï¸ Tech Stack

- **Frontend**: React.js, Axios, CSS3 (Glassmorphism), Lucide Icons.
- **Backend**: Flask, Flask-CORS, TensorFlow (Keras).
- **ML Engine**: Python 3.11, EfficientNetV2-S, Scikit-learn, OpenCV.
- **Storage**: Browser LocalStorage for persistence.

## ðŸš€ Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/singh-aadarsh330/steel-defect-ai.git
cd steel-defect-ai
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
cp .env.example .env
npm start
```

## ðŸ“ Project Structure

```text
â”œâ”€â”€ backend/            # Flask API & Preprocessing logic
â”œâ”€â”€ frontend/           # React Dashboard (SaaS UI)
â”œâ”€â”€ model/              # Saved weights (model.h5) and training logs
â”œâ”€â”€ scripts/            # Training, Prediction, and Dataset utilities
â”œâ”€â”€ assets/             # Project screenshots and diagrams
â”œâ”€â”€ dataset/            # NEU-DET training samples (ignored by Git)
â”œâ”€â”€ uploads/            # Temporary storage for uploaded images
â””â”€â”€ docs/               # Technical documentation
```

## ðŸ§  ML Pipeline Explanation

1. **Preprocessing**: Images are resized to 224x224 and scaled via an internal Lambda layer.
2. **Architecture**: EfficientNetV2-S (ImageNet pretrained) with a custom dual-layer classification head.
3. **Training**: 3-phase strategy (Feature Extraction â†’ Fine-tuning â†’ Deep Adaptation) with Label Smoothing.
4. **Inference**: Optimized for low-latency real-time scoring.

## ðŸ“œ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ðŸ‘¤ Author

**Aadarsh Singh**
- GitHub: [@singh-aadarsh330](https://github.com/singh-aadarsh330)
- LinkedIn: [Aadarsh Singh](https://www.linkedin.com/in/aadarsh-singh-kiit)

---
*For professional inquiries or enterprise licensing, please contact us via the GitHub repository.*

## 🤗 Pre-trained Model
Download the model weights directly from Hugging Face:
👉 [singhaadarsh330/steel-defect-ai](https://huggingface.co/singhaadarsh330/steel-defect-ai)


## 📊 Model Performance (v2 - Fine-tuned)

| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Crazing | 1.00 | 0.68 | 0.81 |
| Inclusion | 0.87 | 1.00 | 0.93 |
| Patches | 0.83 | 1.00 | 0.91 |
| Pitted Surface | 0.98 | 0.83 | 0.90 |
| Rolled-in Scale | 0.88 | 0.98 | 0.93 |
| Scratches | 0.97 | 0.97 | 0.97 |
| **Overall Accuracy** | | | **0.91** |

![Confusion Matrix](assets/confusion_matrix.png)

> ⚠️ **Prototype Notice:** This is a demonstration prototype. Browser LocalStorage is used for session persistence. A production deployment would use a proper database (PostgreSQL/MongoDB) and cloud storage.

