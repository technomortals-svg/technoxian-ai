from flask import Flask, request, render_template_string
import requests
import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

BOT1 = "http://<BOT1_IP>/control"
BOT2 = "http://<BOT2_IP>/control"
VISION_STREAM = "http://<VISION_IP>:8000/video"

logs = []
intrusion_data = []
cyber_data = []
status = "SAFE"

def send(bot, cmd):
    try:
        requests.get(bot, params={"cmd": cmd})
    except:
        pass

@app.route('/vision', methods=['POST'])
def vision():
    global status
    status = "INTRUSION"
    logs.append(f"{datetime.datetime.now()} → Intrusion")
    intrusion_data.append(len(intrusion_data)+1)

    send(BOT1, "FWD")
    send(BOT2, "FWD")

    return "OK"

@app.route('/cyber', methods=['POST'])
def cyber():
    global status
    status = "CYBER ATTACK"
    logs.append(f"{datetime.datetime.now()} → Cyber Attack")
    cyber_data.append(len(cyber_data)+1)

    send(BOT1, "STOP")
    send(BOT2, "STOP")

    return "OK"

def generate_graph(data, title):
    plt.figure()
    plt.plot(data)
    plt.title(title)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

@app.route('/')
def dashboard():
    intr_graph = generate_graph(intrusion_data, "Intrusions")
    cyber_graph = generate_graph(cyber_data, "Cyber Attacks")

    return render_template_string("""
    <body style="background:#0b0b0b;color:#00ffcc;font-family:Arial">

    <h1>⚡ AEGIS-X PRO DASHBOARD</h1>
    <h2>Status: {{status}}</h2>

    <h3>📹 Live Feed</h3>
    <img src="{{stream}}" width="500"/>

    <h3>📊 Intrusion Graph</h3>
    <img src="data:image/png;base64,{{intr_graph}}"/>

    <h3>📊 Cyber Graph</h3>
    <img src="data:image/png;base64,{{cyber_graph}}"/>

    <h3>📜 Logs</h3>
    {% for log in logs %}
        <p>{{log}}</p>
    {% endfor %}

    </body>
    """, stream=VISION_STREAM,
       intr_graph=intr_graph,
       cyber_graph=cyber_graph,
       logs=logs,
       status=status)

app.run(host="0.0.0.0", port=5001)