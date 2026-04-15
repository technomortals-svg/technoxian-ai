import tkinter as tk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

BLYNK_TOKEN = "YOUR_BLYNK_TOKEN"

time_data = []
risk_data = []

def get_data(pin):
    url = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&{pin}"
    try:
        return float(requests.get(url).text)
    except:
        return 0

# Advanced AI (local verification)
def calculate_risk(distance, gas):
    distance_norm = max(0, min(50, 50 - distance))
    gas_norm = max(0, min(800, gas - 200))

    risk = (distance_norm * 0.6) + (gas_norm * 0.4) / 10
    return risk

def update():
    distance = get_data("V0")
    gas = get_data("V1")

    risk = calculate_risk(distance, gas)

    distance_label.config(text=f"Distance: {distance:.2f}")
    gas_label.config(text=f"Gas: {gas:.2f}")
    risk_label.config(text=f"Risk Score: {risk:.2f}")

    if risk > 60:
        status_label.config(text="STATUS: CRITICAL", fg="red")
    elif risk > 30:
        status_label.config(text="STATUS: WARNING", fg="orange")
    else:
        status_label.config(text="STATUS: SAFE", fg="green")

    # Graph
    time_data.append(time.time())
    risk_data.append(risk)

    if len(time_data) > 20:
        time_data.pop(0)
        risk_data.pop(0)

    ax.clear()
    ax.plot(risk_data)
    ax.set_title("Risk Trend")
    ax.set_ylabel("Risk Score")

    canvas.draw()

    root.after(2000, update)

# GUI
root = tk.Tk()
root.title("ASTRA Monitoring System")
root.geometry("600x600")

distance_label = tk.Label(root, font=("Arial", 14))
distance_label.pack()

gas_label = tk.Label(root, font=("Arial", 14))
gas_label.pack()

risk_label = tk.Label(root, font=("Arial", 14))
risk_label.pack()

status_label = tk.Label(root, font=("Arial", 16, "bold"))
status_label.pack()

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

update()
root.mainloop()