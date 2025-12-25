"""
Configuration settings for Garbage Classification System
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Model Configuration
MODEL_PATH = os.path.join(BASE_DIR, "backend", "apps", "model", "renset50_model.pth")
NUM_CLASSES = 10
DEVICE = "cuda"  # Will fallback to CPU if CUDA not available

# Image Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE_MB = 10
IMAGE_SIZE = (256, 256)

# Model Classes
CLASSES = [
    'battery', 'biological', 'cardboard', 'clothes', 'glass',
    'metal', 'paper', 'plastic', 'shoes', 'trash'
]

# Class Icons and Colors for UI
CLASS_STYLES = {
    'battery': {'icon': '🔋', 'color': '#e74c3c'},
    'biological': {'icon': '🧫', 'color': '#2ecc71'},
    'cardboard': {'icon': '📦', 'color': '#a97142'},
    'clothes': {'icon': '👕', 'color': '#9b59b6'},
    'glass': {'icon': '🍾', 'color': '#1abc9c'},
    'metal': {'icon': '🥫', 'color': '#7f8c8d'},
    'paper': {'icon': '📄', 'color': '#3498db'},
    'plastic': {'icon': '🧴', 'color': '#f39c12'},
    'shoes': {'icon': '👟', 'color': '#34495e'},
    'trash': {'icon': '🚯', 'color': '#2c3e50'}
}

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
FRONTEND_PORT = 5000

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# CORS Settings (if needed)
CORS_ORIGINS = ["http://localhost:5000", "http://127.0.0.1:5000"]
