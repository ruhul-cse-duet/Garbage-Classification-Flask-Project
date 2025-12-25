"""
Image prediction module with error handling
"""
import torch
from torchvision import transforms
from PIL import Image
import logging
from pathlib import Path

from .model import GarbageModel
from ..config import MODEL_PATH, CLASSES, DEVICE, IMAGE_SIZE

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize device
try:
    device = torch.device(DEVICE if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
except Exception as e:
    logger.warning(f"Error setting device: {e}. Falling back to CPU.")
    device = torch.device("cpu")

# Initialize model
model = None

def load_model():
    """Load the trained model with error handling"""
    global model
    
    try:
        if not Path(MODEL_PATH).exists():
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
        
        logger.info(f"Loading model from: {MODEL_PATH}")
        model = GarbageModel(num_classes=len(CLASSES))
        
        # Load state dict with weights_only=True for security
        state_dict = torch.load(MODEL_PATH, map_location=device, weights_only=True)
        model.load_state_dict(state_dict)
        
        model.to(device)
        model.eval()
        
        logger.info("Model loaded successfully!")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

# Load model at startup
try:
    load_model()
except Exception as e:
    logger.critical(f"Failed to load model at startup: {e}")
    # Model will be None, errors will be caught in predict_image

# Image transformation pipeline
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_image(image: Image.Image) -> dict:
    """
    Predict garbage class for an image
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: Prediction results with class and confidence
        
    Raises:
        ValueError: If model not loaded or image invalid
        RuntimeError: If prediction fails
    """
    try:
        # Check if model is loaded
        if model is None:
            raise ValueError("Model not loaded. Please check model file and restart server.")
        
        # Validate image
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image format. Expected PIL Image.")
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Transform and prepare image
        img_tensor = transform(image).unsqueeze(0).to(device)
        
        # Predict
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, class_idx = torch.max(probabilities, dim=1)
            
            class_id = class_idx.item()
            conf_score = confidence.item()
        
        # Validate class index
        if class_id < 0 or class_id >= len(CLASSES):
            raise ValueError(f"Invalid class index: {class_id}")
        
        result = {
            "class": CLASSES[class_id],
            "confidence": round(conf_score, 4),
            "all_predictions": {
                CLASSES[i]: round(probabilities[0][i].item(), 4) 
                for i in range(len(CLASSES))
            }
        }
        
        logger.info(f"Prediction: {result['class']} ({result['confidence']:.2%})")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise RuntimeError(f"Failed to predict image: {str(e)}")
