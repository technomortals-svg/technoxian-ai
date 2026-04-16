import tkinter as tk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

BLYNK_TOKEN = "YOUR_BLYNK_TOKEN"

inlet_data = []
outlet_data = []
time_data = []

def get_data(pin):
    url = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&{pin}"
    try:
        return float(requests.get(url).text)
    except:
        return 0

def update():
    inlet = get_data("V0")
    outlet = get_data("V1")

    # AI Calculations
    loss = inlet - outlet
    efficiency = (outlet / inlet) * 100 if inlet != 0 else 0
    risk = (loss * 2) + (100 - efficiency)

    # Update labels
    inlet_label.config(text=f"Inlet Flow: {inlet:.2f} L/min")
    outlet_label.config(text=f"Outlet Flow: {outlet:.2f} L/min")
    loss_label.config(text=f"Flow Loss: {loss:.2f}")
    eff_label.config(text=f"Efficiency: {efficiency:.2f}%")

    # Status
    if risk > 60:
        status_label.config(text="STATUS: CRITICAL", fg="red")
    elif risk > 30:
        status_label.config(text="STATUS: WARNING", fg="orange")
    else:
        status_label.config(text="STATUS: SAFE", fg="green")

    # Send to Blynk
    requests.get(f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}&V2={loss}")
    requests.get(f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}&V3={efficiency}")

    # Graph
    inlet_data.append(inlet)
    outlet_data.append(outlet)
    time_data.append(time.time())

    if len(inlet_data) > 20:
        inlet_data.pop(0)
        outlet_data.pop(0)
        time_data.pop(0)

    ax.clear()
    ax.plot(inlet_data, label="Inlet")
    ax.plot(outlet_data, label="Outlet")
    ax.legend()
    ax.set_title("Flow Comparison")

    canvas.draw()

    root.after(2000, update)

# GUI
root = tk.Tk()
root.title("ASTRA Flow Monitoring System")
root.geometry("700x600")

inlet_label = tk.Label(root, font=("Arial", 14))
inlet_label.pack()

outlet_label = tk.Label(root, font=("Arial", 14))
outlet_label.pack()

loss_label = tk.Label(root, font=("Arial", 14))
loss_label.pack()

eff_label = tk.Label(root, font=("Arial", 14))
eff_label.pack()

status_label = tk.Label(root, font=("Arial", 16, "bold"))
status_label.pack()

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

update()
root.mainloop()