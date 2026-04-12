import requests
import time
import threading
import tkinter as tk
from flask import Flask, request

HP = "http://<HP_IP>:5001/cyber"

THRESHOLD = 15
TIME_WINDOW = 5

timestamps = {}
logs = []

app = Flask(__name__)

@app.route('/')
def home():
    ip = request.remote_addr
    now = time.time()

    if ip not in timestamps:
        timestamps[ip] = []

    timestamps[ip].append(now)

    timestamps[ip] = [t for t in timestamps[ip] if now - t < TIME_WINDOW]

    if len(timestamps[ip]) > THRESHOLD:
        msg = f"⚠ Attack from {ip}"
        logs.append(msg)

        try:
            requests.post(HP, json={"attack": ip})
        except:
            logs.append("⚠ HP not reachable")

        return "Blocked"

    return "Safe"

def run_server():
    app.run(host="0.0.0.0", port=5000)

# ===== GUI =====
root = tk.Tk()
root.title("🔥 Firewall Dashboard")
root.geometry("500x400")
root.configure(bg="black")

title = tk.Label(root, text="FIREWALL SYSTEM", fg="red", bg="black", font=("Arial", 16))
title.pack()

log_box = tk.Text(root, bg="black", fg="lime", font=("Courier", 10))
log_box.pack(fill="both", expand=True)

def update_logs():
    log_box.delete(1.0, tk.END)
    for log in logs[-20:]:
        log_box.insert(tk.END, log + "\n")
    root.after(1000, update_logs)

threading.Thread(target=run_server, daemon=True).start()

update_logs()
root.mainloop()