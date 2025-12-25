# 🏗️ Project Architecture & Structure

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GARBAGE CLASSIFICATION SYSTEM                 │
│                         Version 2.0.0                            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     HTTP      ┌──────────────┐     Tensor    ┌────────────┐
│   Frontend   │──────────────▶│   Backend    │────────────▶│   Model    │
│   (Flask)    │               │   (FastAPI)   │              │  (ResNet50)│
│  Port 5000   │◀──────────────│  Port 8000    │◀────────────│            │
└──────────────┘    JSON       └──────────────┘   Prediction  └────────────┘
       │
       │
       ▼
┌──────────────┐
│   Browser    │
│  - Upload    │
│  - Camera    │
└──────────────┘
```

---

## 📂 Directory Structure

```
Garbage-Classification-Flask-Project/
│
├── 📄 README.md                    ← Main documentation (339 lines)
├── 📄 QUICKSTART.md                ← Setup guide (314 lines)
├── 📄 TESTING_GUIDE.md             ← Test cases (425 lines)
├── 📄 CHANGELOG.md                 ← Version history (279 lines)
├── 📄 PROJECT_UPDATE_SUMMARY.md    ← This update summary
├── 📄 requirements.txt             ← Python dependencies
├── 📄 runtime.txt                  ← Python version
├── 🚀 run.bat                      ← Windows launcher
├── 🚀 run.sh                       ← Linux/Mac launcher
│
├── 🗂️ backend/                     ← Backend API (FastAPI)
│   ├── 🗂️ api/
│   │   ├── routes.py              ← API endpoints (182 lines)
│   │   └── __pycache__/
│   │
│   ├── 🗂️ apps/
│   │   ├── main.py                ← FastAPI app (66 lines)
│   │   ├── config.py              ← Configuration (51 lines)
│   │   ├── __init__.py
│   │   │
│   │   └── 🗂️ model/
│   │       ├── model.py           ← ResNet50 architecture
│   │       ├── predictor.py       ← Prediction logic (131 lines)
│   │       ├── renset50_model.pth ← Trained weights (90MB)
│   │       └── __pycache__/
│   │
│   └── 🗂️ utils/
│       └── image_utils.py         ← Image processing
│
├── 🗂️ frontend/                    ← Frontend UI (Flask)
│   ├── app.py                     ← Flask app (147 lines)
│   │
│   ├── 🗂️ templates/
│   │   ├── index.html             ← Upload UI (179 lines)
│   │   └── live_camera.html       ← Live detection (278 lines)
│   │
│   └── 🗂️ static/
│       └── style.css              ← Styling (387 lines)
│
├── 🗂️ codes/                       ← Training notebooks
│   └── garbage-classification-resnet50-pytorch.ipynb
│
├── 🗂️ docker/                      ← Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── 🗂️ test images/                 ← Sample test files
│   ├── battery_18.jpg
│   ├── plastic_18.jpg
│   ├── metal_20.jpg
│   ├── clothes_1051.jpg
│   └── trash_129.jpg
│
└── 🗂️ .idea/                       ← IDE settings
    └── ...
```

---

## 🔄 Data Flow

### 1. Image Upload Flow

```
┌─────────────┐
│   User      │
│ Selects     │
│   Image     │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Frontend Validation                      │
│  ✓ Check file type                        │
│  ✓ Check file size (<10MB)                │
│  ✓ Show preview                           │
└──────┬───────────────────────────────────┘
       │
       │ POST /predict
       │ (multipart/form-data)
       ▼
┌──────────────────────────────────────────┐
│  Backend API (routes.py)                  │
│  ✓ Validate file extension                │
│  ✓ Validate file size                     │
│  ✓ Check corruption                       │
│  ✓ Convert to PIL Image                   │
└──────┬───────────────────────────────────┘
       │
       │ Image object
       ▼
┌──────────────────────────────────────────┐
│  Predictor (predictor.py)                 │
│  ✓ Resize to 256x256                      │
│  ✓ Convert to tensor                      │
│  ✓ Normalize                              │
│  ✓ Add batch dimension                    │
└──────┬───────────────────────────────────┘
       │
       │ Tensor
       ▼
┌──────────────────────────────────────────┐
│  ResNet50 Model                           │
│  ✓ Forward pass                           │
│  ✓ Apply softmax                          │
│  ✓ Get predictions                        │
└──────┬───────────────────────────────────┘
       │
       │ {class, confidence, all_predictions}
       ▼
┌──────────────────────────────────────────┐
│  Frontend Display                         │
│  ✓ Show garbage type                      │
│  ✓ Display confidence bar                 │
│  ✓ Show icon                              │
└──────────────────────────────────────────┘
```

### 2. Live Camera Flow

```
┌─────────────┐
│   User      │
│  Clicks     │
│ Live Camera │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Browser Camera API                       │
│  ✓ Request camera access                 │
│  ✓ Start video stream                    │
│  ✓ Display in <video>                    │
└──────┬───────────────────────────────────┘
       │
       │ Every 1 second
       ▼
┌──────────────────────────────────────────┐
│  JavaScript Canvas                        │
│  ✓ Capture frame from video               │
│  ✓ Convert to blob (JPEG)                 │
│  ✓ Create FormData                        │
└──────┬───────────────────────────────────┘
       │
       │ POST /predict
       │ (frame as blob)
       ▼
┌──────────────────────────────────────────┐
│  Backend API                              │
│  (Same validation as upload)              │
└──────┬───────────────────────────────────┘
       │
       │ {class, confidence}
       ▼
┌──────────────────────────────────────────┐
│  Update Detection Box                     │
│  ✓ Change border color                    │
│  ✓ Update label text                      │
│  ✓ Show icon + class + confidence         │
│  ✓ Update statistics                      │
└──────────────────────────────────────────┘
```

---

## 🧩 Component Details

### Backend Components

#### 1. FastAPI Application (`main.py`)
```python
Purpose: Main application entry point
Features:
  - CORS configuration
  - Router inclusion
  - Startup/shutdown events
  - API documentation
```

#### 2. API Routes (`routes.py`)
```python
Endpoints:
  GET  /          → Health check
  GET  /health    → Detailed status
  POST /predict   → Image classification

Error Handling:
  - 400: Bad Request (invalid file)
  - 413: Payload Too Large
  - 500: Internal Server Error
  - 503: Service Unavailable
```

#### 3. Model (`model.py` + `predictor.py`)
```python
Architecture: ResNet50
  - Frozen layers: 1-3
  - Trainable: layer4 + custom FC
  - Classes: 10 garbage types
  
Prediction:
  - Input: 256x256 RGB image
  - Output: class + confidence + all predictions
  - Device: Auto-detect CUDA/CPU
```

### Frontend Components

#### 1. Flask Application (`app.py`)
```python
Routes:
  GET  /        → Home page
  POST /        → Handle upload
  GET  /live    → Camera page
  GET  /health  → Status check

Features:
  - File validation
  - API communication
  - Error handling
  - Timeout management
```

#### 2. Upload UI (`index.html`)
```html
Features:
  - File selection
  - Image preview
  - Drag & drop ready
  - Confidence visualization
  - Error display
  - Category reference
```

#### 3. Live Camera UI (`live_camera.html`)
```html
Features:
  - Video streaming
  - Bounding box overlay
  - Start/Stop controls
  - Real-time stats
  - Color-coded results
  - Error handling
```

#### 4. Styling (`style.css`)
```css
Components:
  - Responsive layout
  - Gradient backgrounds
  - Animations
  - Color coding per class
  - Mobile optimization
```

---

## 🔐 Security Layers

```
Layer 1: Frontend Validation
  ├─ File type check
  ├─ File size check
  └─ Client-side preview

Layer 2: Backend Validation
  ├─ Extension whitelist
  ├─ Size limit enforcement
  ├─ MIME type verification
  └─ Content corruption check

Layer 3: Model Security
  ├─ Weights-only loading
  ├─ Path validation
  └─ Error sanitization

Layer 4: API Security
  ├─ CORS configuration
  ├─ Request validation
  └─ Rate limiting ready
```

---

## 📊 Error Handling Flow

```
┌─────────────┐
│   Request   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Validation Layer       │
│  ✓ File present?        │
│  ✓ Valid format?        │
│  ✓ Size OK?             │
│  ✓ Not corrupted?       │
└──────┬──────────────────┘
       │
       ├─ Invalid ──▶ Return 400 with details
       │
       ▼ Valid
┌─────────────────────────┐
│  Processing Layer       │
│  ✓ Convert image        │
│  ✓ Transform            │
│  ✓ Prepare tensor       │
└──────┬──────────────────┘
       │
       ├─ Error ────▶ Return 400 with message
       │
       ▼ Success
┌─────────────────────────┐
│  Model Layer            │
│  ✓ Model loaded?        │
│  ✓ Prediction succeed?  │
│  ✓ Valid output?        │
└──────┬──────────────────┘
       │
       ├─ Error ────▶ Return 500/503 with log
       │
       ▼ Success
┌─────────────────────────┐
│  Return Result          │
│  {class, confidence}    │
└─────────────────────────┘
```

---

## 🎨 UI Component Hierarchy

```
┌────────────────────────────────────────────────────┐
│                    Browser Window                   │
│  ┌──────────────────────────────────────────────┐  │
│  │              Navigation Bar                   │  │
│  │  [Upload] [Live Camera]                      │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │           Upload Mode (index.html)           │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │       Upload Box / Preview             │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │          Predict Button                │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │        Result Box (if predicted)       │  │  │
│  │  │  - Icon                                │  │  │
│  │  │  - Class name                          │  │  │
│  │  │  - Confidence bar                      │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │         Error Box (if error)           │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │        Live Camera Mode (live_camera.html)   │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │       Video Feed with Detection Box    │  │  │
│  │  │  ┌──────────────────────────────────┐  │  │  │
│  │  │  │ [🔋 BATTERY 95.3%] (in box)      │  │  │  │
│  │  │  └──────────────────────────────────┘  │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  [Start] [Stop] Controls               │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  Statistics: Predictions | Conf | FPS  │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

---

## 🔄 State Management

### Upload Mode States:
1. **Initial**: Upload box visible
2. **File Selected**: Preview shown, upload box hidden
3. **Uploading**: Button disabled, "Predicting..." text
4. **Success**: Result box displayed
5. **Error**: Error box displayed (auto-hide after 10s)

### Live Camera States:
1. **Initializing**: "Requesting camera access..."
2. **Ready**: Video visible, "Start Detection" button
3. **Detecting**: Detection active, "Stop Detection" button
4. **Paused**: Detection stopped, "Start Detection" button
5. **Error**: Error message, no controls

---

## 📈 Performance Optimization

```
┌─────────────────────────────────────────┐
│  Model Loading (Startup)                │
│  • Load once at backend startup         │
│  • Cache in memory                      │
│  • ~2-3 seconds one-time cost           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Prediction (Per Request)               │
│  • Image preprocessing: ~50ms           │
│  • Model inference: ~1-2s (CPU)         │
│  • Model inference: ~200ms (GPU)        │
│  • Response formatting: ~10ms           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Live Camera (Continuous)               │
│  • Frame capture: ~10ms                 │
│  • Prediction: 1 per second             │
│  • UI update: ~5ms                      │
│  • Smooth 30 FPS video                  │
└─────────────────────────────────────────┘
```

---

## 🌐 Network Communication

```
Frontend (localhost:5000) ←→ Backend (localhost:8000)

Request Types:
  1. POST /predict
     Content-Type: multipart/form-data
     Body: file (image blob)
     
  2. GET /health
     Response: {status, model_loaded, version}

Response Format:
  Success (200):
    {
      "class": "plastic",
      "confidence": 0.9543,
      "all_predictions": {...}
    }
  
  Error (4xx/5xx):
    {
      "detail": "Error message"
    }
```

---

## 📦 Deployment Architecture

```
Development:
  Frontend: localhost:5000 (Flask dev server)
  Backend: localhost:8000 (Uvicorn with reload)

Production (Recommended):
  Frontend: Gunicorn + Flask
  Backend: Uvicorn workers (4+)
  Reverse Proxy: Nginx
  SSL: Let's Encrypt

Docker (Optional):
  docker-compose up:
    - backend service
    - frontend service
    - shared volume for model
```

---

## 🎯 Testing Strategy

```
Unit Tests (Not Yet Implemented):
  • Model loading
  • Prediction function
  • File validation
  • API endpoints

Integration Tests:
  • Upload flow
  • Camera flow
  • Error handling
  • End-to-end

Manual Tests (See TESTING_GUIDE.md):
  • UI interactions
  • Browser compatibility
  • Performance
  • Error scenarios
```

---

**This architecture provides a solid, production-ready foundation for the Garbage Classification System! 🎊**
