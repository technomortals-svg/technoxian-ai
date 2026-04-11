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
    data = request.json
    pos = data["pos"]

    if pos == "LEFT":
        send(BOT1, "FWD")
        send(BOT2, "STOP")
    elif pos == "RIGHT":
        send(BOT2, "FWD")
        send(BOT1, "STOP")
    else:
        send(BOT1, "FWD")
        send(BOT2, "FWD")

    logs.append(f"Vision: {pos}")
    return "OK"

@app.route('/cyber', methods=['POST'])
def cyber():
    send(BOT1, "STOP")
    send(BOT2, "STOP")

    logs.append("Cyber Attack Detected")
    return "OK"

@app.route('/')
def dashboard():
    return render_template_string("""
    <html>
    <head>
    <title>AI Security Dashboard</title>
    </head>
    <body style="background:black;color:lime;font-family:monospace">
    <h1>⚡ AI SECURITY SYSTEM</h1>
    <h2>Logs:</h2>
    {% for log in logs %}
        <p>{{log}}</p>
    {% endfor %}
    </body>
    </html>
    """, logs=logs)

app.run(host="0.0.0.0", port=5001)