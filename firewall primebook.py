from flask import Flask, request
from sklearn.ensemble import IsolationForest
import numpy as np
import requests

app = Flask(__name__)

model = IsolationForest(contamination=0.2)

# training normal behavior
train_data = np.array([[1], [2], [1], [2], [3]])
model.fit(train_data)

request_count = {}

@app.route('/')
def home():
    ip = request.remote_addr

    if ip not in request_count:
        request_count[ip] = 0

    request_count[ip] += 1

    value = np.array([[request_count[ip]]])
    prediction = model.predict(value)

    if prediction[0] == -1:
        print("🚨 Attack Detected")

        requests.post(
            "http://<HP_IP>:5001/cyber",
            json={
                "event": "attack",
                "ip": ip
            }
        )

        return "Blocked"

    return "Safe"

app.run(host="0.0.0.0", port=5000)