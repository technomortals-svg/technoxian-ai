import cv2
import requests
from ultralytics import YOLO
from flask import Flask, Response
import threading

HP = "http://<HP_IP>:5001/vision"

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

app = Flask(__name__)

latest_frame = None

def generate():
    global latest_frame
    while True:
        if latest_frame is not None:
            _, buffer = cv2.imencode('.jpg', latest_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def vision_loop():
    global latest_frame
    while True:
        ret, frame = cap.read()
        latest_frame = frame

        detected = False
        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if model.names[cls] in ["person"]:
                    detected = True

        if detected:
            requests.post(HP, json={"event": "intrusion"})
        else:
            requests.post(HP, json={"event": "clear"})

def run_all():
    threading.Thread(target=vision_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)

run_all()