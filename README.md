# 🗑️ Garbage Classification AI System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.7.1+-red.svg)](https://pytorch.org)

An AI-powered garbage classification system using **Deep Learning (ResNet50)** to automatically categorize waste into 10 different classes. The system features both **image upload** and **live camera detection** capabilities with a modern, responsive UI.

---

## 🎯 Features

### ✨ Core Capabilities
- **Image Upload Classification**: Upload images for instant garbage type prediction
- **Live Camera Detection**: Real-time garbage classification using webcam with bounding box visualization
- **High Accuracy**: ResNet50-based CNN model trained on garbage dataset
- **10 Waste Categories**: Battery, Biological, Cardboard, Clothes, Glass, Metal, Paper, Plastic, Shoes, Trash
- **Confidence Scores**: Shows prediction confidence percentage
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🛡️ Enhanced Error Handling
- Robust file validation (size, format, corrupted images)
- API error handling with proper HTTP status codes
- Frontend error notifications
- Model loading validation
- Graceful fallbacks for camera access issues

---

## 📂 Project Structure

```
Garbage-Classification-Flask-Project/
│
├── backend/                      # FastAPI Backend (Model Inference)
│   ├── api/
│   │   └── routes.py            # API endpoints with error handling
│   ├── apps/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   └── model/
│   │       ├── model.py         # ResNet50 model architecture
│   │       ├── predictor.py     # Prediction logic
│   │       └── renset50_model.pth  # Trained model weights
│   └── utils/
│       └── image_utils.py       # Image processing utilities
│
├── frontend/                     # Flask Frontend (UI)
│   ├── app.py                   # Flask application with routing
│   ├── templates/
│   │   ├── index.html           # Image upload interface
│   │   └── live_camera.html     # Live camera detection interface
│   └── static/
│       └── style.css            # Modern responsive styling
│
├── codes/                        # Training notebooks
├── docker/                       # Docker configuration
├── test images/                  # Sample test images
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam (for live detection feature)
- CUDA-compatible GPU (optional, for faster inference)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd Garbage-Classification-Flask-Project
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Model File
Ensure `renset50_model.pth` exists in `backend/apps/model/` directory.

---

## 🎮 Usage

### Running the Application

You need to run **both** backend and frontend servers:

#### Terminal 1: Start Backend (FastAPI)
```bash
# From project root
uvicorn backend.apps.main:app --reload --port 8000
```
Backend will run on: **http://localhost:8000**

#### Terminal 2: Start Frontend (Flask)
```bash
# From project root
python frontend/app.py
```
Frontend will run on: **http://localhost:5000**

### Using the Application

#### Option A: Image Upload Classification
1. Open **http://localhost:5000** in your browser
2. Click **"📷 Click to upload image"**
3. Select a garbage image from your computer
4. Click **"🔍 Predict"** button
5. View the classification result with confidence score

#### Option B: Live Camera Detection
1. From the home page, click **"📹 Live Camera"** button
2. Allow camera access when prompted
3. Point camera at garbage items
4. Real-time classification will appear with:
   - Category icon and name
   - Confidence percentage
   - Color-coded bounding box

---

## 🎨 Waste Categories

| Category | Icon | Description |
|----------|------|-------------|
| Battery | 🔋 | Batteries and power cells |
| Biological | 🧫 | Organic waste, food scraps |
| Cardboard | 📦 | Cardboard boxes, packaging |
| Clothes | 👕 | Textile waste, fabrics |
| Glass | 🍾 | Glass bottles, containers |
| Metal | 🥫 | Metal cans, containers |
| Paper | 📄 | Paper waste, documents |
| Plastic | 🧴 | Plastic bottles, packaging |
| Shoes | 👟 | Footwear |
| Trash | 🚯 | General waste |

---

## 🧠 Model Architecture

- **Base Model**: ResNet50 (Residual Neural Network)
- **Transfer Learning**: Pre-trained on ImageNet, fine-tuned on garbage dataset
- **Trainable Layers**: Layer 4 + Custom FC layers
- **Input Size**: 256x256 pixels
- **Output**: 10 classes with softmax probabilities
- **Regularization**: Dropout (0.3) to prevent overfitting

```
ResNet50 (frozen layers 1-3)
    ↓
Layer 4 (trainable)
    ↓
Dropout (0.3)
    ↓
FC (2048 → 256)
    ↓
ReLU
    ↓
FC (256 → 10)
    ↓
Softmax
```

---

## 🔧 API Endpoints

### POST /predict
Classifies uploaded image or video frame.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "class": "plastic",
  "confidence": 0.9543
}
```

**Error Responses:**
- `400`: Invalid file format
- `413`: File too large (>10MB)
- `500`: Model prediction error

---

## 🐛 Error Handling Features

### Backend (FastAPI)
- ✅ File format validation (JPG, PNG, JPEG, GIF, BMP)
- ✅ File size limits (max 10MB)
- ✅ Corrupted image detection
- ✅ Model loading error handling
- ✅ Detailed error messages with HTTP status codes

### Frontend (Flask)
- ✅ API connection error handling
- ✅ Camera access error handling
- ✅ User-friendly error notifications
- ✅ Timeout handling for slow connections
- ✅ Fallback UI states

---

## 📊 Testing

Test images are provided in the `test images/` directory:
- `battery_18.jpg` - Battery waste
- `clothes_1051.jpg` - Textile waste
- `202512-plastic18.jpg` - Plastic waste
- `202512-metal20.jpg` - Metal waste
- `trash_129.jpg`, `trash_131.jpg` - General trash

---

## 🐳 Docker Deployment (Optional)

```bash
cd docker
docker-compose up --build
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **PyTorch** | Deep learning framework |
| **ResNet50** | CNN architecture |
| **FastAPI** | Backend API server |
| **Flask** | Frontend web server |
| **Pillow** | Image processing |
| **OpenCV** | Computer vision utilities |
| **HTML5/CSS3** | Modern UI design |
| **JavaScript** | Live camera functionality |

---

## 📝 Configuration

Edit `backend/apps/config.py` to customize:
- Model path
- Allowed file formats
- Maximum file size
- Device (CPU/GPU)
- Logging settings

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Developer

**Ruhul Amin**\
**Email: [ruhul.cse.duet@gmail.com]**

Developed using FastAPI, Flask, PyTorch, and ResNet50

---

## 🔮 Future Enhancements

- [ ] Mobile app version (iOS/Android)
- [ ] Multi-language support
- [ ] Batch image processing
- [ ] Cloud deployment (AWS/GCP)
- [ ] Model retraining pipeline
- [ ] Statistics dashboard
- [ ] User authentication
- [ ] Save classification history

---

## ⚡ Performance Tips

1. **GPU Acceleration**: Use CUDA-enabled GPU for faster inference
2. **Model Caching**: Model is loaded once at startup
3. **Image Optimization**: Resize large images before upload
4. **Browser**: Use modern browsers (Chrome/Firefox) for best camera support

---

## 📞 Support

If you encounter issues:
1. Check if both servers are running
2. Verify model file exists
3. Check camera permissions
4. Review console logs for errors

---

## 🎉 Acknowledgments

- ResNet50 architecture by Microsoft Research
- Garbage dataset from [Kaggle]
- Icons from Unicode Emoji

---

**⭐ If you find this project useful, please give it a star!**
