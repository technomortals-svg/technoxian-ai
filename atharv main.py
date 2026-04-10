from ultralytics import YOLO
import cv2
import requests

model = YOLO("yolov8n.pt")  # auto-download

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = model.names[cls]

            if label == "person" and conf > 0.6:
                print("🚨 Person Detected")

                requests.post(
                    "http://<HP_IP>:5001/vision",
                    json={
                        "event": "person",
                        "confidence": conf
                    }
                )

    cv2.imshow("Vision AI", frame)

    if cv2.waitKey(1) == 27:
        break