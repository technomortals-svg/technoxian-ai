print("🚀 CODE STARTED")

import requests

url = "http://192.168.1.145:5001/alert"

try:
    response = requests.post(url, json={"type": "object"})
    print("✅ Response:", response.text)
except Exception as e:
    print("❌ Error:", e)