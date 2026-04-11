from flask import Flask, request, render_template_string
from sklearn.ensemble import IsolationForest
import numpy as np
import requests

app = Flask(__name__)

HP = "http://<HP_IP>:5001/cyber"

model = IsolationForest(contamination=0.2)
model.fit(np.array([[1],[2],[1],[2],[3]]))

counts = {}
logs = []

@app.route('/')
def home():
    ip = request.remote_addr
    counts[ip] = counts.get(ip, 0) + 1

    if model.predict([[counts[ip]]])[0] == -1:
        logs.append(f"Attack from {ip}")
        requests.post(HP, json={"attack": ip})
        return "Blocked"

    return "Safe"

@app.route('/dashboard')
def dash():
    return render_template_string("""
    <body style="background:black;color:red;font-family:monospace">
    <h1>🔥 FIREWALL DASHBOARD</h1>
    {% for log in logs %}
        <p>{{log}}</p>
    {% endfor %}
    </body>
    """, logs=logs)

app.run(host="0.0.0.0", port=5000)