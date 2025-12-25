"""
FastAPI application main entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.api.routes import router
from backend.apps.config import CORS_ORIGINS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Garbage Classification API",
    description="AI-powered garbage classification using Deep Learning (ResNet50)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# @router.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     """Global exception handler"""
#     logger.error(f"Global exception handler caught: {exc}")
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"detail": "Internal server error"}
#    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use CORS_ORIGINS from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("🚀 Garbage Classification API Starting...")
    logger.info("=" * 60)
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down Garbage Classification API...")

# Run instructions
"""
To run this application:

1. Development mode:
   uvicorn backend.apps.main:app --reload --port 8000

2. Production mode:
   uvicorn backend.apps.main:app --host 0.0.0.0 --port 8000 --workers 4

3. With FastAPI CLI:
   fastapi dev backend/apps/main.py
"""
