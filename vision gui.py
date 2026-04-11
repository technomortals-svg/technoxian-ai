import cv2
import requests
from ultralytics import YOLO
import tkinter as tk

HP = "http://<HP_IP>:5001/vision"

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Vision AI Dashboard")

status = tk.StringVar()
status.set("Idle")

label = tk.Label(root, textvariable=status, font=("Arial", 16))
label.pack()

def run():
    ret, frame = cap.read()
    detected = False

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = model.names[cls]

            if name in ["person", "dog", "cat"]:
                detected = True

    if detected:
        status.set("⚠ Intrusion Detected")
        requests.post(HP, json={"event": "intrusion"})
    else:
        status.set("✅ Patrol Mode")
        requests.post(HP, json={"event": "clear"})

    cv2.imshow("Camera", frame)
    root.after(100, run)

root.after(100, run)
root.mainloop()