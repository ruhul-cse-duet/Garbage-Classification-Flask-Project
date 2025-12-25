import cv2
import torch
import torchvision.transforms as transforms
from PIL import Image
from apps.model import garbage_Model

# -------- CONFIG --------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CLASS_NAMES = [
    'battery','biological','cardboard','clothes','glass',
    'metal','paper','plastic','shoes','trash'
]

# -------- LOAD MODEL --------
model = garbage_Model(num_classes=10)
model.load_state_dict(torch.load("models/resnet50_model.pth", map_location=DEVICE))
model.to(DEVICE)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

# -------- CAMERA --------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # ---- CENTER ROI (Pseudo Bounding Box) ----
    box_size = 300
    x1 = w//2 - box_size//2
    y1 = h//2 - box_size//2
    x2 = w//2 + box_size//2
    y2 = h//2 + box_size//2

    roi = frame[y1:y2, x1:x2]

    # ---- PREDICTION ----
    img = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    input_tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, 1)

    label = CLASS_NAMES[pred.item()]
    confidence = conf.item()

    # ---- DRAW BOX ----
    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 3)
    cv2.putText(
        frame,
        f"{label} ({confidence:.2f})",
        (x1, y1-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0,255,0),
        2
    )

    cv2.imshow("Garbage Classification (Live)", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
