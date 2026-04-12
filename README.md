# 🧠 AEGIS-X PRO SWARM SECURITY SYSTEM (FINAL README)

---

# 📌 PROJECT OVERVIEW

**Aegis-X Pro** is a **distributed AI-based surveillance and security system** combining:

* 👁 AI Vision (intrusion detection)
* 🤖 Swarm robotics (2 autonomous bots)
* 🔐 Cybersecurity firewall (attack detection)
* 📹 Live video streaming
* 📊 Real-time analytics (graphs + logs)
* 🎛 Professional dashboards

This system works **completely on a local network (no internet required)**.

---

# 🧩 SYSTEM ARCHITECTURE

```
[ GPU Laptop ]
(Vision AI + Camera Streaming)
        ↓
[ HP Laptop ]
(Main Brain + Dashboard + Graphs)
        ↓
[ Bot 1 ]       [ Bot 2 ]

[ Firewall Laptop ]
(Cybersecurity + GUI)
        ↓
[ HP Laptop ]
```

---

# ⚙️ CORE LOGIC

```
PATROL MODE → Bots move in predefined pattern
INTRUSION → Bots converge to target
NO ACTIVITY → Return to patrol
CYBER ATTACK → Bots STOP immediately
FAILSAFE → One bot continues if other fails
```

---

# 💻 DEVICE ROLES

| Device          | Role                            |
| --------------- | ------------------------------- |
| GPU Laptop      | AI Detection + Camera Streaming |
| HP Laptop       | Main Brain + Dashboard + Graphs |
| Firewall Laptop | Cybersecurity System            |
| ESP8266 Bots    | Movement Execution              |

---

# 📦 INSTALLATION

---

## 🟢 GPU LAPTOP

```
pip install ultralytics opencv-python flask requests tkinter
```

---

## 🔴 HP LAPTOP

```
pip install flask requests matplotlib
```

---

## 🟡 FIREWALL LAPTOP (THONNY / WINDOWS)

```
pip install flask requests matplotlib
```

---

## 🤖 ESP8266

Install in Arduino IDE:

* ESP8266 Board Package
* ESP8266WiFi
* ESP8266WebServer

---

# 🌐 NETWORK REQUIREMENTS

* All devices must be on the **same WiFi network**
* Use **local IP addresses**
* Disable mobile data

---

# 🔧 CONFIGURATION

---

## Replace these in ALL codes:

---

### HP Laptop IP

```
http://<HP_IP>:5001
```

---

### Vision Laptop IP

```
http://<VISION_IP>:8000/video
```

---

### Bot IPs

```
http://<BOT1_IP>/control
http://<BOT2_IP>/control
```

---

---

# 🚀 EXECUTION STEPS (IMPORTANT ORDER)

---

## 1️⃣ Start Vision System (GPU Laptop)

```
python vision_system.py
```

👉 Starts:

* AI detection
* Camera streaming

---

## 2️⃣ Start Main Brain (HP Laptop)

```
python brain_pro.py
```

Open dashboard:

```
http://<HP_IP>:5001
```

---

## 3️⃣ Start Firewall System

```
python firewall_pro.py
```

👉 Opens desktop GUI

---

## 4️⃣ Power ON Bots

---

# 📹 LIVE CAMERA FEED

* Camera is connected to GPU laptop
* Stream is sent to HP dashboard
* Displayed in real time

---

# 📊 LIVE GRAPHS

---

## Intrusion Graph

* Updates when object detected
* Shows activity trend

---

## Cyber Attack Graph

* Updates on firewall detection
* Shows attack frequency

---

# 🤖 BOT CONTROL

---

## Commands:

| Command | Action       |
| ------- | ------------ |
| FWD     | Move forward |
| STOP    | Stop         |

---

## Behavior:

* Patrol → autonomous
* Intrusion → converge
* Cyber attack → stop

---

# 🧪 TESTING

---

## 👁 Intrusion Test

* Stand in front of camera
  👉 Bots move forward

---

## 🔐 Cyber Attack Test

Run:

```python
import requests
for i in range(30):
    requests.get("http://<FIREWALL_IP>:5000/")
```

👉 Bots stop
👉 Dashboard updates

---

# 🎛 DASHBOARDS

---

| Device          | Type                  |
| --------------- | --------------------- |
| GPU Laptop      | Vision (local window) |
| HP Laptop       | Web Dashboard         |
| Firewall Laptop | Desktop GUI           |

---

# ⚠️ TROUBLESHOOTING

---

## ❌ Camera not showing

* Check Vision IP
* Ensure script running

---

## ❌ Bots not moving

* Check wiring
* Test manually:

```
http://BOT_IP/control?cmd=FWD
```

---

## ❌ No communication

* Same WiFi
* Correct IP

---

## ❌ Modules missing

```
pip install <module>
```

---

# 🏆 FINAL OUTPUT

✔ Autonomous swarm bots
✔ AI-based intrusion detection
✔ Cybersecurity integration
✔ Live camera streaming
✔ Real-time graphs + logs
✔ Professional dashboards

---

# 🔥 FINAL STATEMENT

“Aegis-X Pro is a fully integrated, AI-powered swarm surveillance system capable of autonomous patrol, intelligent threat detection, and real-time response using low-cost hardware and local networking.”

---
