from ultralytics import YOLO
import cv2
import requests

model = YOLO("yolov8n.pt")

HP = "http://<HP_IP>:5001/vision"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    h, w, _ = frame.shape

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                x1, y1, x2, y2 = box.xyxy[0]
                cx = int((x1 + x2) / 2)

                if cx < w/3:
                    pos = "LEFT"
                elif cx > 2*w/3:
                    pos = "RIGHT"
                else:
                    pos = "CENTER"

                requests.post(HP, json={"pos": pos})

    cv2.imshow("Vision", frame)

    if cv2.waitKey(1) == 27:
        break