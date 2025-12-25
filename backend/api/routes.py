"""
API routes with comprehensive error handling
backend/api/routes.py
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import io
import logging

from backend.apps.model.predictor import predict_image
from backend.apps.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def validate_file_extension(filename: str) -> bool:
    """Check if file has allowed extension"""
    if not filename:
        return False
    extension = filename.rsplit('.', 1)[-1].lower()
    return extension in ALLOWED_EXTENSIONS

def validate_file_size(content: bytes) -> bool:
    """Check if file size is within limit"""
    size_mb = len(content) / (1024 * 1024)
    return size_mb <= MAX_FILE_SIZE_MB

@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Garbage Classification API is running",
        "version": "1.0.0"
    }

@router.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": True,
        "api_version": "1.0.0"
    }

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict garbage classification from uploaded image
    
    Args:
        file: Uploaded image file
        
    Returns:
        JSON with class and confidence
        
    Raises:
        HTTPException: Various error conditions
    """
    try:
        # Validate file was provided
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename"
            )
        
        # Validate file extension
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        try:
            content = await file.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to read uploaded file"
            )
        
        # Validate file size
        if not validate_file_size(content):
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE_MB}MB"
            )
        
        # Validate file is not empty
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )
        
        # Try to open and validate image
        try:
            image = Image.open(io.BytesIO(content))
            
            # Validate image can be converted to RGB
            if image.mode not in ['RGB', 'RGBA', 'L']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported image mode: {image.mode}"
                )
            
            # Convert to RGB
            image = image.convert("RGB")
            
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot identify image file. File may be corrupted."
            )
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted image file"
            )
        
        # Perform prediction
        try:
            result = predict_image(image)
            logger.info(f"Successfully predicted: {file.filename} -> {result['class']}")
            return result
            
        except ValueError as e:
            # Model not loaded or validation error
            logger.error(f"Prediction validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except RuntimeError as e:
            # Prediction runtime error
            logger.error(f"Prediction runtime error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model prediction failed"
            )
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected prediction error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during prediction"
            )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch-all for any other unexpected errors
        logger.error(f"Unexpected error in predict endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


