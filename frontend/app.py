"""
Flask frontend application with error handling
"""
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import logging
from werkzeug.utils import secure_filename
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this!

# Configuration
API_URL = "http://127.0.0.1:8000/predict"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    """Home page with image upload"""
    result = None
    error = None
    
    if request.method == "POST":
        try:
            # Check if file was uploaded
            if 'image' not in request.files:
                error = "No file uploaded. Please select an image."
                return render_template("index.html", result=result, error=error)
            
            file = request.files['image']
            
            # Check if filename is empty
            if file.filename == '':
                error = "No file selected. Please choose an image."
                return render_template("index.html", result=result, error=error)
            
            # Validate file extension
            if not allowed_file(file.filename):
                error = f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
                return render_template("index.html", result=result, error=error)
            
            # Check file size (read first to get size)
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if file_size > MAX_FILE_SIZE:
                error = f"File too large. Maximum size is 10MB."
                return render_template("index.html", result=result, error=error)
            
            if file_size == 0:
                error = "Uploaded file is empty."
                return render_template("index.html", result=result, error=error)
            
            # Make API request
            try:
                logger.info(f"Sending file to API: {file.filename}")
                
                response = requests.post(
                    API_URL, 
                    files={"file": (secure_filename(file.filename), file, file.content_type)},
                    timeout=30  # 30 second timeout
                )
                
                # Check response status
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Prediction successful: {result}")
                elif response.status_code == 400:
                    error_detail = response.json().get('detail', 'Invalid request')
                    error = f"Validation error: {error_detail}"
                elif response.status_code == 413:
                    error = "File too large for processing."
                elif response.status_code == 503:
                    error = "Model service unavailable. Please contact administrator."
                else:
                    error = f"Server error ({response.status_code}). Please try again."
                    
            except requests.exceptions.Timeout:
                error = "Request timeout. The server is taking too long to respond."
                logger.error("API request timeout")
            except requests.exceptions.ConnectionError:
                error = "Cannot connect to API server. Please ensure backend is running on port 8000."
                logger.error("API connection error")
            except requests.exceptions.RequestException as e:
                error = f"Network error: {str(e)}"
                logger.error(f"API request error: {e}")
            except ValueError as e:
                error = "Invalid response from server."
                logger.error(f"JSON decode error: {e}")
                
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
            logger.error(f"Unexpected error: {e}")
    
    return render_template("index.html", result=result, error=error)

@app.route("/live")
def live():
    """Live camera detection page"""
    return render_template("live_camera.html")

@app.route("/health")
def health():
    """Health check endpoint"""
    try:
        # Check if API is reachable
        response = requests.get("http://127.0.0.1:8000/health", timeout=20)
        api_status = "online" if response.status_code == 200 else "offline"
    except:
        api_status = "offline"
    
    return jsonify({
        "frontend": "online",
        "backend": api_status
    })

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template("index.html", error="Page not found"), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    logger.error(f"Internal server error: {e}")
    return render_template("index.html", error="Internal server error"), 500

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🌐 Starting Flask Frontend Server")
    logger.info("=" * 60)
    logger.info("Frontend URL: http://localhost:5000")
    logger.info("Make sure backend is running on http://localhost:8000")
    logger.info("=" * 60)
    
    app.run(host="0.0.0.0", port=5000, debug=True)
