# ⚡ Quick Start Guide

Get your Garbage Classification System up and running in 5 minutes!

---

## 🎯 Prerequisites

- Python 3.10 or higher
- Webcam (optional, for live detection)
- 2GB free RAM
- Internet connection (for initial setup)

---

## 🚀 Setup (3 Steps)

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

⏱️ *This takes 2-3 minutes*

### Step 3: Verify Model File

Check that this file exists:
```
backend/apps/model/renset50_model.pth
```

✅ If it exists, you're ready!

---

## ▶️ Running the App

### Option A: Using Run Script (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

The script will:
1. ✅ Check environment
2. ✅ Start backend (port 8000)
3. ✅ Start frontend (port 5000)
4. ✅ Open browser automatically

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
uvicorn backend.apps.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
python frontend/app.py
```

---

## 🎮 Using the App

### 1. Upload Image Mode

1. Open **http://localhost:5000**
2. Click **"📷 Click to upload image"**
3. Choose a garbage image
4. Click **"🔍 Predict"**
5. See result!

### 2. Live Camera Mode

1. Click **"📹 Live Camera"** button
2. Allow camera access
3. Click **"▶️ Start Detection"**
4. Point camera at garbage
5. Watch real-time classification!

---

## 📝 Test It Out

Use the provided test images in `test images/` folder:

```
test images/
├── battery_18.jpg      → Should predict: battery
├── plastic_18.jpg      → Should predict: plastic
├── metal_20.jpg        → Should predict: metal
├── clothes_1051.jpg    → Should predict: clothes
└── trash_129.jpg       → Should predict: trash
```

---

## ❓ Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is busy
# Windows:
netstat -ano | findstr :8000

```

### Frontend won't start?
```bash
# Check if port 5000 is busy
# Windows:
netstat -ano | findstr :5000

# Linux/Mac:
lsof -ti:5000
```

### Camera not working?
- Check browser permissions
- Try Chrome (best compatibility)
- Ensure no other app using camera

### Dependencies error?
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend UI | http://localhost:5000 | Main application |
| Backend API | http://localhost:8000 | Prediction API |
| API Docs | http://localhost:8000/docs | API documentation |
| Health Check | http://localhost:8000/health | Status check |

---

## 🎯 What to Try

### First Time Users:

1. ✅ Upload a test image
2. ✅ Check the prediction confidence
3. ✅ Try the live camera
4. ✅ Test different garbage types
5. ✅ Check the statistics

### Advanced Users:

1. Explore API at http://localhost:8000/docs
2. Try different image formats
3. Test error scenarios
4. Monitor prediction speed
5. Check console logs

---

## 📊 Expected Results

**Good Predictions:**
- Confidence: 70% - 99%
- Response time: < 3 seconds
- Accurate classification

**If confidence < 50%:**
- Image might be unclear
- Object not in training data
- Try better lighting/angle

---

## 🔧 Configuration

Edit `backend/apps/config.py` to customize:

```python
# Model settings
MODEL_PATH = "..."
NUM_CLASSES = 10

# File limits
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Server settings
API_PORT = 8000
FRONTEND_PORT = 5000
```

---

## 📚 Next Steps

1. **Read Full Documentation**: See `README.md`
2. **Run Tests**: Check `TESTING_GUIDE.md`
3. **Review Changes**: See `CHANGELOG.md`
4. **Report Issues**: Create GitHub issue

---

## 💡 Tips for Best Results

### Image Upload:
- ✅ Clear, well-lit photos
- ✅ Single object in frame
- ✅ Avoid cluttered backgrounds
- ✅ File size < 5MB

### Live Camera:
- ✅ Good lighting
- ✅ Hold object steady (1-2 seconds)
- ✅ Fill frame with object
- ✅ Avoid reflections (for glass/metal)

---

## 🎓 Understanding Results

### Confidence Levels:
- **90-100%**: Very confident ✅
- **70-89%**: Confident ✅
- **50-69%**: Moderate ⚠️
- **< 50%**: Uncertain ❌

### What Each Class Means:

| Class | Examples |
|-------|----------|
| Battery | AA, AAA, phone batteries |
| Biological | Food scraps, organic waste |
| Cardboard | Boxes, packaging |
| Clothes | Shirts, pants, fabric |
| Glass | Bottles, jars, broken glass |
| Metal | Cans, tins, foil |
| Paper | Documents, newspapers |
| Plastic | Bottles, containers, bags |
| Shoes | Any footwear |
| Trash | General non-recyclable waste |

---

## 🆘 Quick Help

### Problem: "Model not found"
→ Check `backend/apps/model/renset50_model.pth` exists

### Problem: "Cannot connect to API"
→ Ensure backend is running on port 8000

### Problem: "Camera access denied"
→ Allow camera in browser settings

### Problem: "Slow predictions"
→ Normal on CPU (2-3s), faster on GPU (<1s)

### Problem: "Wrong predictions"
→ Try test images first, ensure good image quality

---

## 🎉 Success Checklist

Before considering setup complete, verify:

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:5000
- [ ] Can upload and predict test images
- [ ] Camera feed displays (if testing live mode)
- [ ] Predictions have >70% confidence on test images
- [ ] Both modes work correctly

---

## 📞 Need More Help?

1. Check **README.md** for detailed documentation
2. Review **TESTING_GUIDE.md** for test cases
3. See **CHANGELOG.md** for recent changes
4. Check console logs for error details

---

**🎊 Congratulations! You're ready to classify garbage with AI!**

*Average setup time: 5 minutes*  
*Difficulty: Easy ⭐*
