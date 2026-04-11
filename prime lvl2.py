from flask import Flask, request
from sklearn.ensemble import IsolationForest
import numpy as np
import requests

app = Flask(__name__)

model = IsolationForest(contamination=0.2)
model.fit(np.array([[1],[2],[1],[2],[3]]))

counts = {}
HP = "http://<HP_IP>:5001/cyber"

@app.route('/')
def home():
    ip = request.remote_addr

    if ip not in counts:
        counts[ip] = 0

    counts[ip] += 1

    pred = model.predict([[counts[ip]]])

    if pred[0] == -1:
        requests.post(HP, json={"attack": ip})
        return "Blocked"

    return "Safe"

app.run(host="0.0.0.0", port=5000)