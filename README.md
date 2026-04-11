# 🧠 AEGIS-X SWARM SECURITY SYSTEM (FINAL README)

---

# 📌 PROJECT OVERVIEW

Aegis-X is a **low-cost, AI-powered autonomous swarm security system** designed for real-time surveillance and threat response.

It integrates:

* 👁 **AI Vision Detection (Intrusion Detection)**
* 🤖 **Dual Bot Swarm (Autonomous Patrol + Converge)**
* 🔐 **Cybersecurity Firewall (Attack Detection)**
* 🎛 **Multi-Device GUI Dashboards**

---

# 🧩 SYSTEM ARCHITECTURE

```
GPU Laptop (Vision AI + GUI)
        ↓
HP Laptop (Main Brain + Swarm Logic + Dashboard)
        ↓
Bot 1 (Front)     Bot 2 (Back)

Primebook / Any Laptop (Firewall AI + Dashboard)
        ↓
HP Laptop (Cyber Alerts)
```

---

# ⚙️ CORE SYSTEM LOGIC

```
NORMAL MODE → Bots patrol area autonomously
INTRUSION → Both bots converge toward target
NO ACTIVITY → Resume patrol after delay
CYBER ATTACK → All bots STOP immediately
FAILSAFE → Remaining bot continues if one fails
```

---

# 💻 DEVICE ROLES

| Device                 | Role                              |
| ---------------------- | --------------------------------- |
| GPU Laptop             | Vision AI (Object Detection)      |
| HP Laptop              | Brain + Swarm Control + Dashboard |
| Primebook / Any Laptop | Firewall AI                       |
| ESP8266 Bots           | Movement Execution                |

---

# ❓ CAN PRIMEBOOK CODE RUN ON WINDOWS?

✅ **YES — FULLY COMPATIBLE**

The firewall code uses:

* Flask
* NumPy
* Scikit-learn

👉 These run on:

* Windows ✔
* Linux ✔
* Mac ✔

📌 On Windows, just install using:

```
pip install flask numpy scikit-learn requests
```

---

# 🌐 NETWORK REQUIREMENTS

* All devices must be on **same WiFi network**
* Disable mobile data
* Note all IP addresses

---

# 📦 INSTALLATION

---

## 🟢 GPU LAPTOP (VISION AI)

```
pip install ultralytics opencv-python requests tkinter
```

---

## 🔵 HP LAPTOP (MAIN BRAIN)

```
pip install flask requests
```

---

## 🟡 FIREWALL DEVICE (PRIMEBOOK OR WINDOWS LAPTOP)

```
pip install flask numpy scikit-learn requests
```

---

## 🤖 ESP8266 SETUP (ARDUINO IDE)

Install:

* ESP8266 Board Package
* ESP8266WiFi
* ESP8266WebServer

---

# 🔌 HARDWARE (BOT)

## Wiring

```
L298N → ESP8266

IN1 → D1
IN2 → D2
IN3 → D3
IN4 → D4

Battery → L298N
L298N 5V → ESP Vin
GND → Common
```

---

# 🚀 EXECUTION STEPS

---

## 1️⃣ Start Main Brain (HP Laptop)

```
python brain_swarm.py
```

Open dashboard:

```
http://<HP_IP>:5001
```

---

## 2️⃣ Start Firewall System

```
python firewall_gui.py
```

---

## 3️⃣ Start Vision AI

```
python vision_gui.py
```

---

## 4️⃣ Power ON Bots

---

# 🧪 TESTING

---

## 👁 Intrusion Test

* Stand in camera view
  👉 Bots move forward

---

## 🛣 Patrol Mode

* No object detected
  👉 Bots move in patrol pattern

---

## 🔐 Cyber Attack Test

Run:

```python
import requests
for i in range(30):
    requests.get("http://<FIREWALL_IP>:5000/")
```

👉 Bots STOP
👉 Dashboard updates

---

# 🎛 DASHBOARDS

| Device          | Dashboard Type |
| --------------- | -------------- |
| GPU Laptop      | Tkinter GUI    |
| HP Laptop       | Web Dashboard  |
| Firewall Device | Web Dashboard  |

---

# ⚠️ TROUBLESHOOTING

---

## ❌ Bots not moving

* Check battery
* Check wiring
* Test manually:

```
http://BOT_IP/control?cmd=FWD
```

---

## ❌ No communication

* Check IP addresses
* Ensure same WiFi

---

## ❌ Module error

```
pip install <module>
```

---

## ❌ Camera not opening

* Close other apps using camera

---

# 🏆 FINAL OUTPUT

✔ Autonomous dual-bot swarm
✔ AI-based intrusion detection
✔ Cyber attack detection
✔ Real-time dashboards
✔ Fully integrated system

---

# 🔥 FINAL STATEMENT

“Aegis-X demonstrates a unified, AI-driven swarm security system capable of autonomous patrol, intelligent threat detection, and adaptive response using low-cost hardware.”

---
