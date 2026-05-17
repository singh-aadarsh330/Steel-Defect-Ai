Steel-Defect-Ai: Enterprise Industrial Inspection Hub
Show Image
Show Image
Show Image
Show Image
Show Image
Project Overview
Steel-Defect-Ai is a professional-grade AI platform for automated surface defect detection in steel manufacturing. Using EfficientNetV2-S, it identifies 6 major industrial defects: Crazing, Inclusion, Patches, Pitted Surface, Rolled-in Scale, and Scratches.
Key Features

State-of-the-Art ML: EfficientNetV2-S backbone with 91% validated accuracy (F1-score across 6 classes).
Batch Processing: Upload and analyze hundreds of samples simultaneously.
Enterprise Dashboard: Premium dark-mode UI with real-time telemetry and history persistence.
Global Compliance: Integrated ISO 14488 / ASTM E155 standards for international audits.
Live Optical Feed: Real-time webcam scanning for on-the-spot inspections.
Advanced Analytics: Categorized defect distributions and trend reporting.
Exportable Reports: Generate detailed PDF/CSV inspection summaries.

Model Performance (v2 - Fine-tuned)
ClassPrecisionRecallF1-ScoreCrazing1.000.680.81Inclusion0.871.000.93Patches0.831.000.91Pitted Surface0.980.830.90Rolled-in Scale0.880.980.93Scratches0.970.970.97Overall Accuracy0.91
Show Image
Pre-trained Model
Download model weights from Hugging Face: singhaadarsh330/steel-defect-ai

model.h5 - Original model
model_improved.keras - Fine-tuned model (91% accuracy)

Tech Stack

Frontend: React.js, Axios, CSS3 (Glassmorphism), Lucide Icons
Backend: Flask, Flask-CORS, TensorFlow (Keras)
ML Engine: Python 3.11, EfficientNetV2-S, Scikit-learn, OpenCV
Storage: Browser LocalStorage for persistence


Prototype Notice: This is a demonstration prototype. Browser LocalStorage is used for session persistence. A production deployment would use a proper database (PostgreSQL/MongoDB) and cloud storage.

Installation & Setup
Prerequisites

Python 3.11+
Node.js 18+
Git

1. Clone the Repository
git clone https://github.com/singh-aadarsh330/Steel-Defect-Ai.git
cd Steel-Defect-Ai
2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
3. Frontend Setup
cd ../frontend
npm install
npm start
Project Structure
├── backend/         # Flask API & preprocessing logic
├── frontend/        # React dashboard
├── model/           # Model info and training logs
├── scripts/         # Training, evaluation, and dataset utilities
├── tests/           # API unit tests
├── assets/          # Screenshots and diagrams
└── dataset/         # NEU-DET training samples (ignored by Git)
ML Pipeline

Preprocessing: Images resized to 224x224 via internal Lambda layer.
Architecture: EfficientNetV2-S (ImageNet pretrained) with custom classification head.
Training: 3-phase strategy (Feature Extraction → Fine-tuning → Deep Adaptation) with class weighting and label smoothing.
Inference: Optimized for low-latency real-time scoring.

License
MIT License - see the LICENSE file for details.
Author
Aadarsh Singh

GitHub: @singh-aadarsh330
LinkedIn: Aadarsh Singh
