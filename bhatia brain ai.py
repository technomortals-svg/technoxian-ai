from flask import Flask, request
import time

app = Flask(__name__)

events = []

def analyze():
    # Keep last few events
    recent = events[-5:]

    if "person" in recent and "attack" in recent:
        print("🔥 CRITICAL THREAT DETECTED")
        print("→ Trigger bot + block system")

    elif "person" in recent:
        print("⚠️ Physical Threat Detected")

    elif "attack" in recent:
        print("🌐 Cyber Threat Detected")

@app.route('/vision', methods=['POST'])
def vision():
    data = request.json

    print(f"Vision Input: {data}")
    events.append("person")

    analyze()
    return "OK"

@app.route('/cyber', methods=['POST'])
def cyber():
    data = request.json

    print(f"Cyber Input: {data}")
    events.append("attack")

    analyze()
    return "OK"

app.run(host="0.0.0.0", port=5001)