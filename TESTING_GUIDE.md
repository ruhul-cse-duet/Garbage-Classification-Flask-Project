# 🧪 Testing Guide - Garbage Classification System

This guide will help you test all features of the Garbage Classification System to ensure everything works correctly.

---

## 📋 Pre-Testing Checklist

Before starting tests, ensure:
- ✅ Virtual environment is activated
- ✅ All dependencies are installed (`pip install -r requirements.txt`)
- ✅ Model file exists at `backend/apps/model/renset50_model.pth`
- ✅ Both backend and frontend servers are running

---

## 🚀 Quick Start Testing

### Method 1: Using Run Script
```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

### Method 2: Manual Start
```bash
# Terminal 1 - Backend
uvicorn backend.apps.main:app --reload --port 8000

# Terminal 2 - Frontend
python frontend/app.py
```

---

## 🔍 Test Cases

### 1. Backend API Tests

#### Test 1.1: Health Check
```bash
# Using curl
curl http://localhost:8000/health

# Expected Response:
{
  "status": "healthy",
  "model_loaded": true,
  "api_version": "1.0.0"
}
```

#### Test 1.2: API Documentation
- Open browser: `http://localhost:8000/docs`
- ✅ Should see interactive Swagger UI
- ✅ Test `/predict` endpoint directly from docs

#### Test 1.3: Valid Image Upload
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test images/battery_18.jpg"

# Expected Response:
{
  "class": "battery",
  "confidence": 0.9543,
  "all_predictions": {...}
}
```

#### Test 1.4: Invalid File Format Error
```bash
# Try uploading a text file
curl -X POST "http://localhost:8000/predict" \
  -F "file=@requirements.txt"

# Expected Response: 400 Bad Request
{
  "detail": "Invalid file format. Allowed formats: png, jpg, jpeg, gif, bmp"
}
```

#### Test 1.5: Large File Error
- Upload file > 10MB
- Expected: 413 Request Entity Too Large

#### Test 1.6: Corrupted Image Error
- Create corrupted image file
- Expected: 400 Bad Request with "corrupted image" message

---

### 2. Frontend UI Tests

#### Test 2.1: Homepage Load
1. Open `http://localhost:5000`
2. ✅ Page loads without errors
3. ✅ "Upload Image" and "Live Camera" buttons visible
4. ✅ Upload box displayed
5. ✅ Category icons shown at bottom

#### Test 2.2: Image Upload - Valid Image
1. Click "📷 Click to upload image"
2. Select `test images/plastic_18.jpg`
3. ✅ Image preview shows
4. ✅ "Remove" button appears
5. Click "🔍 Predict"
6. ✅ Result shows with:
   - Garbage type (e.g., "PLASTIC")
   - Confidence percentage
   - Confidence bar
   - Icon

#### Test 2.3: Image Upload - Invalid Format
1. Try uploading `.txt` file
2. ✅ Browser should block or show error
3. ✅ Alert: "Invalid file type!"

#### Test 2.4: Image Upload - Large File
1. Try uploading file > 10MB
2. ✅ Alert: "File too large! Maximum size is 10MB."

#### Test 2.5: Remove Image
1. Upload an image
2. Click "❌ Remove" button
3. ✅ Preview disappears
4. ✅ Upload box reappears
5. ✅ Can upload new image

#### Test 2.6: Backend Connection Error
1. Stop backend server
2. Try uploading image
3. ✅ Error message: "Cannot connect to API server"
4. ✅ Red error box displayed

#### Test 2.7: Multiple Predictions
1. Upload different garbage types:
   - Battery image → should predict "battery"
   - Plastic bottle → should predict "plastic"
   - Paper → should predict "paper"
   - Cardboard → should predict "cardboard"
2. ✅ Each prediction accurate with >70% confidence

---

### 3. Live Camera Tests

#### Test 3.1: Camera Access
1. Click "📹 Live Camera" button
2. ✅ Browser asks for camera permission
3. Allow camera access
4. ✅ Video feed displays
5. ✅ Bounding box overlay visible
6. ✅ "Start Detection" button appears

#### Test 3.2: Camera Permission Denied
1. Click "📹 Live Camera"
2. Deny camera permission
3. ✅ Error message: "Camera access denied"
4. ✅ Instructions to allow access shown

#### Test 3.3: Start Live Detection
1. Click "▶️ Start Detection"
2. ✅ Detection starts (label updates every 1 second)
3. ✅ "Stop Detection" button appears
4. ✅ Stats box shows:
   - Prediction count
   - Average confidence
   - FPS

#### Test 3.4: Live Detection with Objects
1. Start detection
2. Show different garbage items to camera:
   - Plastic bottle
   - Paper
   - Metal can
   - Battery
3. ✅ Classification updates in real-time
4. ✅ Bounding box color changes per class
5. ✅ Icon and confidence % displayed

#### Test 3.5: Stop Detection
1. During live detection
2. Click "⏸️ Stop Detection"
3. ✅ Detection pauses
4. ✅ Label shows "Detection Paused"
5. ✅ "Start Detection" button reappears

#### Test 3.6: Stats Accuracy
1. Run detection for 30 seconds
2. ✅ Prediction count increases
3. ✅ Average confidence calculates correctly
4. ✅ FPS displays (~1 since predict every 1 second)

#### Test 3.7: Backend Offline During Live
1. Start live detection
2. Stop backend server
3. ✅ Label shows "⚠️ Error - Check backend"
4. ✅ Red background on label

#### Test 3.8: Multiple Class Detection
1. Cycle through different items
2. ✅ Each class has unique:
   - Icon (🔋, 🧴, 📄, etc.)
   - Border color
   - Background color

---

### 4. Error Handling Tests

#### Test 4.1: No File Selected
1. Click "🔍 Predict" without selecting file
2. ✅ HTML5 validation: "Please select a file"

#### Test 4.2: Empty File
1. Create 0-byte image file
2. Upload it
3. ✅ Error: "Uploaded file is empty"

#### Test 4.3: Network Timeout
1. Set very slow network
2. Upload image
3. Wait 30+ seconds
4. ✅ Error: "Request timeout"

#### Test 4.4: Model Not Loaded
1. Rename/remove model file
2. Restart backend
3. Try prediction
4. ✅ Error 503: "Model service unavailable"

#### Test 4.5: Invalid Image Mode
1. Upload grayscale or CMYK image
2. ✅ Should convert to RGB automatically
3. ✅ Prediction works

---

### 5. UI/UX Tests

#### Test 5.1: Responsive Design - Mobile
1. Open browser DevTools
2. Switch to mobile view (375x667)
3. ✅ UI adjusts correctly
4. ✅ Buttons stack vertically
5. ✅ Text readable
6. ✅ Upload box accessible

#### Test 5.2: Responsive Design - Tablet
1. Test at 768x1024
2. ✅ Layout adapts
3. ✅ All features work

#### Test 5.3: Browser Compatibility
Test on:
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari (Mac only)

#### Test 5.4: Loading States
1. Upload large image
2. ✅ Button shows "⏳ Predicting..."
3. ✅ Button disabled during prediction

#### Test 5.5: Error Auto-Hide
1. Trigger an error
2. ✅ Error box displays
3. Wait 10 seconds
4. ✅ Error fades out automatically

---

### 6. Performance Tests

#### Test 6.1: Prediction Speed
1. Upload image
2. ✅ Prediction completes in < 3 seconds (CPU)
3. ✅ Prediction completes in < 1 second (GPU)

#### Test 6.2: Multiple Rapid Uploads
1. Upload 10 images rapidly
2. ✅ All process without errors
3. ✅ No memory leaks

#### Test 6.3: Live Detection Performance
1. Run live detection for 5 minutes
2. ✅ FPS stays consistent
3. ✅ No lag in video feed
4. ✅ Predictions remain accurate

---

### 7. Integration Tests

#### Test 7.1: End-to-End Flow
1. Start application
2. Upload test image
3. Get prediction
4. Switch to live camera
5. Get live predictions
6. Return to upload
7. ✅ All transitions smooth
8. ✅ No errors

#### Test 7.2: Concurrent Users (Optional)
1. Open app in 3 browser tabs
2. Use features simultaneously
3. ✅ All work independently

---

## 🐛 Known Issues & Limitations

### Current Limitations:
1. Live camera limited to 1 FPS (by design for performance)
2. Max file size: 10MB
3. Single bounding box (not multiple objects)
4. No GPU auto-detection message

### Future Improvements:
- [ ] Batch upload support
- [ ] Multiple object detection
- [ ] Save classification history
- [ ] Export results to CSV

---

## 📊 Test Results Template

Create a copy and fill:

```
Test Date: ______________
Tester: ______________

Backend Tests:
□ Health check passed
□ API docs accessible
□ Valid upload works
□ Error handling correct

Frontend Tests:
□ Homepage loads
□ Image upload works
□ Error messages show
□ UI responsive

Live Camera Tests:
□ Camera access works
□ Detection accurate
□ Stats update
□ Stop/Start works

Issues Found:
1. ___________________________
2. ___________________________

Overall Status: ☐ PASS  ☐ FAIL

Notes:
_________________________________
_________________________________
```

---

## 🔧 Troubleshooting

### Problem: Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

### Problem: Frontend won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000
```

### Problem: Camera not working
- Check browser camera permissions
- Try different browser
- Ensure no other app using camera

### Problem: Low prediction accuracy
- Check model file integrity
- Verify image quality
- Test with provided test images first

---

## 📞 Support

If tests fail consistently:
1. Check logs in terminal
2. Verify all dependencies installed
3. Ensure model file present
4. Try on different machine/browser

---

## ✅ Success Criteria

**Minimum Requirements to Pass:**
- ✅ Backend starts without errors
- ✅ Frontend loads correctly
- ✅ Image upload and prediction works
- ✅ Live camera displays video
- ✅ Predictions accurate (>70% confidence)
- ✅ Error messages clear and helpful

**All Tests Passed:** 🎉 System ready for deployment!
