# 🛠️ Backend: SteelVision Neural Gateway

The backend service is a high-performance **Flask** API engineered for low-latency inference and secure data handling. It serves as the bridge between the React dashboard and the **EfficientNetV2-S** neural engine.

## 🏗️ Architecture

The backend follows a singleton-registry pattern for ML model management, ensuring that heavy neural weights are loaded only once and shared across all incoming requests.

- **Engine**: TensorFlow 2.15+ (Keras)
- **Framework**: Flask (WSGI)
- **Concurrency**: ModelRegistry Singleton
- **Validation**: Strict byte-stream header verification for image uploads.

## 📁 Key Components

| File | Responsibility |
|---|---|
| `app.py` | Main entry point, route definitions, and CORS configuration. |
| `requirements.txt` | Dependency manifest for the production environment. |
| `.env.example` | Template for secure environment variable management. |

## 🚀 Deployment & Local Setup

### 1. Environment Preparation
It is recommended to use a virtual environment to isolate dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Dependency Installation
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Execution
```bash
python app.py
```
*Server will default to `http://localhost:5000` with hot-reloading enabled in development.*

## 🧠 Neural Pipeline Features

- **⚡ Efficient Loading**: The `ModelRegistry` class utilizes lazy loading to initialize the model on the first request or at startup.
- **🖼️ Internal Preprocessing**: Automated image resizing (224x224) and channel normalization.
- **🛡️ Industrial CORS**: Pre-configured to accept requests only from verified dashboard origins.
- **📊 Telemetry**: Detailed logging for every inference request, including latency and confidence scores.

---
> [!TIP]
> For production deployment, it is recommended to wrap the Flask app in a production-grade WSGI server like **Gunicorn** or **Waitress**.
