from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

BOT1 = "http://<BOT1_IP>/control"
BOT2 = "http://<BOT2_IP>/control"

logs = []
mode = "PATROL"
last_seen = time.time()

def send(bot, cmd):
    try:
        requests.get(bot, params={"cmd": cmd})
    except:
        logs.append("Bot error")

def patrol():
    # alternate movement
    send(BOT1, "FWD")
    send(BOT2, "LEFT")

def converge():
    send(BOT1, "FWD")
    send(BOT2, "FWD")

def stop_all():
    send(BOT1, "STOP")
    send(BOT2, "STOP")

@app.route('/vision', methods=['POST'])
def vision():
    global mode, last_seen

    data = request.json

    if data["event"] == "intrusion":
        mode = "ALERT"
        last_seen = time.time()
        logs.append("Intrusion Detected")
        converge()

    elif data["event"] == "clear":
        if time.time() - last_seen > 3:
            mode = "PATROL"
            patrol()

    return "OK"

@app.route('/cyber', methods=['POST'])
def cyber():
    global mode
    mode = "CYBER ATTACK"
    logs.append("Cyber Attack")
    stop_all()
    return "OK"

@app.route('/')
def dashboard():
    return render_template_string("""
    <body style="background:#111;color:#0f0;font-family:monospace">
    <h1>⚡ SWARM CONTROL DASHBOARD</h1>
    <h2>Mode: {{mode}}</h2>

    <h3>Logs:</h3>
    {% for log in logs %}
        <p>{{log}}</p>
    {% endfor %}
    </body>
    """, logs=logs, mode=mode)

app.run(host="0.0.0.0", port=5001)