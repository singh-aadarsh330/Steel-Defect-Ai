# API Documentation: Steel-Defect-Ai

The backend is built with Flask and serves as the bridge between the frontend and the AI model.

## 🌐 Base URL
`http://localhost:5000`

## 📡 Endpoints

### 1. Health Check
Checks if the API and the ML model are loaded and ready.

- **URL**: `/health`
- **Method**: `GET`
- **Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "CPU/GPU"
}
```

### 2. Predict Defect
Accepts an image and returns the predicted defect class and confidence.

- **URL**: `/predict`
- **Method**: `POST`
- **Data Params**: `FormData` with key `image` (File).
- **Response**:
```json
{
  "defect": "crazing",
  "confidence": 0.987,
  "standard": "ISO 14488 / ASTM E155",
  "description": "Network of fine cracks...",
  "severity": "Medium",
  "all_scores": [
    {"class": "crazing", "confidence": 0.987},
    {"class": "inclusion", "confidence": 0.005},
    ...
  ]
}
```

### 3. Defect Metadata
Returns descriptions and standards for all 6 defect classes.

- **URL**: `/api/defects`
- **Method**: `GET`
- **Response**:
```json
{
  "crazing": {
    "title": "Crazing",
    "standard": "ISO 14488",
    "description": "...",
    "severity": "Medium"
  },
  ...
}
```

## 🛠️ Error Handling

The API returns standard HTTP status codes:
- `200`: Success.
- `400`: Invalid image file or missing data.
- `413`: File too large (Max 16MB).
- `500`: Internal server error (Model failed to load).
