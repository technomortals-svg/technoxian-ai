# 🧠 AEGIS-X: Unified Autonomous Security System

## (Vision AI + Cyber Firewall + Dual Bot Control)

---

# 📌 PROJECT OVERVIEW

Aegis-X is a **multi-layer security system** that integrates:

* 👁 **AI Vision Detection (YOLO)**
* 🔐 **Cyber Firewall (ML-based)**
* 🤖 **Two Autonomous Ground Bots**
* 🎛 **Central Brain + Live Dashboard**

---

# 🧩 SYSTEM ARCHITECTURE

```
[ GPU Laptop ]
   Vision AI (YOLO)
        ↓
[ HP Laptop ]
   Main Brain + Dashboard
        ↑
[ Primebook ]
   Firewall AI

HP → controls → Bot 1 (Front) & Bot 2 (Back)
```

---

# 🧱 SYSTEM LOGIC

```
LEFT detection  → Bot 1 moves
RIGHT detection → Bot 2 moves
CENTER          → Both move
CYBER ATTACK    → Both STOP
```

---

# 💻 DEVICE ROLES

| Device       | Role                   |
| ------------ | ---------------------- |
| GPU Laptop   | Vision AI              |
| HP Laptop    | Main Brain + Dashboard |
| Primebook    | Firewall AI            |
| ESP8266 Bots | Movement               |

---

# 🌐 NETWORK REQUIREMENTS

* All devices must be on **same WiFi**
* Disable mobile data
* Note all IP addresses

---

# ⚙️ INSTALLATION GUIDE

---

## 🟢 GPU LAPTOP (VISION AI)

### Install Python packages:

```
pip install ultralytics opencv-python requests
```

### Download YOLO model:

```
python
from ultralytics import YOLO
YOLO("yolov8n.pt")
```

---

## 🔵 HP LAPTOP (MAIN BRAIN)

### Install packages:

```
pip install flask requests
```

---

## 🟡 PRIMEBOOK (PYDROID)

### Install packages:

```
pip install flask
pip install numpy
pip install scikit-learn
pip install requests
```

---

## 🤖 ESP8266 SETUP (ARDUINO IDE)

### Install:

* ESP8266 Board Package
* ESP8266WiFi
* ESP8266WebServer

---

# 🔌 HARDWARE WIRING (ESP8266 + L298N)

```
IN1 → D1
IN2 → D2
IN3 → D3
IN4 → D4

Battery → L298N
L298N 5V → ESP Vin
GND → Common
```

---

# 🤖 ESP8266 BOT CODE

Upload same code to both bots:

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";

ESP8266WebServer server(80);

#define IN1 D1
#define IN2 D2
#define IN3 D3
#define IN4 D4

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void left() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void right() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void stopBot() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

void handleControl() {
  String cmd = server.arg("cmd");

  if (cmd == "FWD") forward();
  else if (cmd == "LEFT") left();
  else if (cmd == "RIGHT") right();
  else stopBot();

  server.send(200, "text/plain", "OK");
}

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  Serial.begin(115200);
  Serial.println(WiFi.localIP());

  server.on("/control", handleControl);
  server.begin();
}

void loop() {
  server.handleClient();
}
```

---

# 🟢 VISION AI CODE (GPU LAPTOP)

```python
from ultralytics import YOLO
import cv2, requests

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
            if model.names[cls] == "person":
                x1, y1, x2, y2 = box.xyxy[0]
                cx = int((x1 + x2) / 2)

                if cx < w/3: pos = "LEFT"
                elif cx > 2*w/3: pos = "RIGHT"
                else: pos = "CENTER"

                requests.post(HP, json={"pos": pos})

    cv2.imshow("Vision", frame)
    if cv2.waitKey(1) == 27: break
```

---

# 🟡 FIREWALL AI CODE (PRIMEBOOK)

```python
from flask import Flask, request
from sklearn.ensemble import IsolationForest
import numpy as np, requests

app = Flask(__name__)
model = IsolationForest(contamination=0.2)
model.fit(np.array([[1],[2],[1],[2],[3]]))

counts = {}
HP = "http://<HP_IP>:5001/cyber"

@app.route('/')
def home():
    ip = request.remote_addr
    counts[ip] = counts.get(ip, 0) + 1

    if model.predict([[counts[ip]]])[0] == -1:
        requests.post(HP, json={"attack": ip})
        return "Blocked"

    return "Safe"

app.run(host="0.0.0.0", port=5000)
```

---

# 🔴 MAIN BRAIN + DASHBOARD (HP LAPTOP)

```python
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BOT1 = "http://<BOT1_IP>/control"
BOT2 = "http://<BOT2_IP>/control"

logs = []

def send(bot, cmd):
    try:
        requests.get(bot, params={"cmd": cmd})
    except:
        pass

@app.route('/vision', methods=['POST'])
def vision():
    pos = request.json["pos"]

    if pos == "LEFT":
        send(BOT1, "FWD"); send(BOT2, "STOP")
    elif pos == "RIGHT":
        send(BOT2, "FWD"); send(BOT1, "STOP")
    else:
        send(BOT1, "FWD"); send(BOT2, "FWD")

    logs.append(f"Vision: {pos}")
    return "OK"

@app.route('/cyber', methods=['POST'])
def cyber():
    send(BOT1, "STOP")
    send(BOT2, "STOP")
    logs.append("Cyber Attack")
    return "OK"

@app.route('/')
def dashboard():
    return render_template_string("""
    <body style="background:black;color:lime">
    <h1>AI SECURITY DASHBOARD</h1>
    {% for log in logs %}
    <p>{{log}}</p>
    {% endfor %}
    </body>
    """, logs=logs)

app.run(host="0.0.0.0", port=5001)
```

---

# 🌐 GET IP ADDRESSES

### On Laptop:

```
ipconfig
```

### On ESP8266:

* Open Serial Monitor → shows IP

---

# 🚀 RUN ORDER

1. Start Brain (HP)
2. Start Firewall (Primebook)
3. Start Vision (GPU)
4. Power ON Bots

---

# 🧪 TESTING

### Test Bot:

```
http://BOT_IP/control?cmd=FWD
```

### Test Vision:

* Stand in camera → bot moves

### Test Cyber:

* Spam requests → bots STOP

---

# ⚠️ COMMON ISSUES

* Wrong IP → fix manually
* Different WiFi → reconnect
* Bot not moving → check battery
* Module error → reinstall using pip

---

# 🏆 FINAL RESULT

* 🤖 Dual bot autonomous system
* 👁 AI vision tracking
* 🔐 Cyber attack detection
* 🎛 Live dashboard monitoring

---

# 🔥 FINAL LINE

“An integrated autonomous system combining AI vision, robotics, and cybersecurity into a unified intelligent defense platform.”

---
