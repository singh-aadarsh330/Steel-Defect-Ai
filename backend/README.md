# Backend: Steel-Defect-Ai API

This folder contains the Flask-based API that serves the EfficientNetV2 model for real-time defect detection.

## 📁 Files

- `app.py`: Main Flask application with `/predict`, `/health`, and `/api/defects` endpoints.
- `requirements.txt`: Python dependencies.
- `.env.example`: Template for environment variables.

## 🚀 Getting Started

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```

## 🧠 Key Features
- **Model Registry**: Singleton pattern ensures the model is loaded once and shared across requests.
- **Image Preprocessing**: Handles conversion from raw bytes to tensor-ready format.
- **CORS**: Configured for secure frontend communication.
- **Error Handling**: Graceful failure modes for invalid uploads or model errors.
