import tkinter as tk
from tkinter import font as tkfont
import threading
import time
import math
import random
import collections
import sys

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────
BLYNK_TOKEN  = "l6NUfEJvhtnACBZBAN310UcQ0oEEUZ6U"
BLYNK_BASE   = "https://blynk.cloud/external/api/get"
UPDATE_HZ    = 2          # 2 Hz polling
HISTORY_LEN  = 60         # scrolling window points

# Colour palette
BG_DEEP      = "#0A0E14"
BG_PANEL     = "#0F1520"
BG_CARD      = "#141C2B"
ACCENT_CYAN  = "#00E5FF"
ACCENT_GREEN = "#00FF9F"   # emerald
ACCENT_AMBER = "#FFB300"
ACCENT_RED   = "#FF3D3D"
TEXT_WHITE   = "#FFFFFF"
TEXT_DIM     = "#4A5568"
GRID_LINE    = "#1A2435"
BORDER_COLOR = "#1E2D45"

STATUS_COLORS = {
    "NORMAL":   ACCENT_GREEN,
    "WARNING":  ACCENT_AMBER,
    "CRITICAL": ACCENT_RED,
}

# ─────────────────────────────────────────────
#  DATA MODEL
# ─────────────────────────────────────────────
class SensorData:
    def __init__(self):
        self.inlet  = 0.0
        self.outlet = 0.0
        self.inlet_history  = collections.deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
        self.outlet_history = collections.deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
        self.lock   = threading.Lock()
        self.online = False
        self._sim_t = 0.0

    def fetch_blynk(self):
        if not REQUESTS_AVAILABLE:
            return False
        try:
            ri = requests.get(BLYNK_BASE, params={"token": BLYNK_TOKEN, "v0": ""}, timeout=2)
            ro = requests.get(BLYNK_BASE, params={"token": BLYNK_TOKEN, "v1": ""}, timeout=2)
            if ri.status_code == 200 and ro.status_code == 200:
                with self.lock:
                    self.inlet  = float(ri.text.strip())
                    self.outlet = float(ro.text.strip())
                    self.inlet_history.append(self.inlet)
                    self.outlet_history.append(self.outlet)
                    self.online = True
                return True
        except Exception:
            pass
        return False

    def simulate(self):
        self._sim_t += 0.15
        t = self._sim_t
        inlet  = 45 + 30 * math.sin(t * 0.7) + 8  * math.sin(t * 2.3) + random.gauss(0, 1.5)
        outlet = 38 + 25 * math.sin(t * 0.7 - 0.4) + 6 * math.sin(t * 2.1) + random.gauss(0, 1.2)
        inlet  = max(0, min(100, inlet))
        outlet = max(0, min(100, outlet))
        with self.lock:
            self.inlet  = round(inlet,  1)
            self.outlet = round(outlet, 1)
            self.inlet_history.append(self.inlet)
            self.outlet_history.append(self.outlet)
            self.online = False

    def status(self):
        with self.lock:
            v = max(self.inlet, self.outlet)
        if v > 80:
            return "CRITICAL"
        if v > 60:
            return "WARNING"
        return "NORMAL"

    def snapshot(self):
        with self.lock:
            return (self.inlet, self.outlet,
                    list(self.inlet_history),
                    list(self.outlet_history),
                    self.online)

# ─────────────────────────────────────────────
#  BACKGROUND POLLING THREAD
# ─────────────────────────────────────────────
def poll_loop(data: SensorData, stop_event: threading.Event):
    while not stop_event.is_set():
        if not data.fetch_blynk():
            data.simulate()
        time.sleep(1.0 / UPDATE_HZ)

# ─────────────────────────────────────────────
#  HELPER: rounded rectangle on canvas
# ─────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r=12, **kwargs):
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)

# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class SewageMonitorApp:
    def __init__(self):
        self.data       = SensorData()
        self.stop_event = threading.Event()
        self._orb_phase = 0.0
        self._last_status = "NORMAL"

        # ── Root window ──────────────────────────
        self.root = tk.Tk()
        self.root.title("INDUSTRIAL SEWAGE MONITORING SYSTEM")
        self.root.configure(bg=BG_DEEP)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost',    True)
        try:
            self.root.overrideredirect(True)
        except Exception:
            pass
        self.root.bind('<Escape>', self._quit)

        self.W = self.root.winfo_screenwidth()
        self.H = self.root.winfo_screenheight()

        self._build_ui()

        # Start poll thread
        self._poll_thread = threading.Thread(
            target=poll_loop, args=(self.data, self.stop_event), daemon=True)
        self._poll_thread.start()

        # Kick off UI refresh
        self.root.after(100, self._ui_tick)

    # ── BUILD UI ─────────────────────────────────
    def _build_ui(self):
        W, H = self.W, self.H

        # ── Background canvas (static decorative layer) ──
        self.bg_canvas = tk.Canvas(self.root, bg=BG_DEEP,
                                   highlightthickness=0, bd=0)
        self.bg_canvas.place(x=0, y=0, width=W, height=H)
        self._draw_background()

        # ── ROW 0a: Info bar (date / time / connection) ──
        info_h = max(28, int(H * 0.035))
        self.info_frame = tk.Frame(self.root, bg=BG_DEEP,
                                   highlightthickness=0)
        self.info_frame.place(x=10, y=4, width=W-20, height=info_h)

        self.lbl_time = tk.Label(self.info_frame, text="",
                                  font=("Arial", self._fs(12)),
                                  fg=TEXT_DIM, bg=BG_DEEP)
        self.lbl_time.place(x=6, rely=0.5, anchor="w")

        self.lbl_conn = tk.Label(self.info_frame, text="● SIM",
                                  font=("Arial", self._fs(12), "bold"),
                                  fg=ACCENT_AMBER, bg=BG_DEEP)
        self.lbl_conn.place(relx=1.0, x=-6, rely=0.5, anchor="e")

        # ── ROW 0b: Title bar ────────────────────
        title_y = 4 + info_h + 4
        title_h = max(64, int(H * 0.085))
        self.title_frame = tk.Frame(self.root, bg=BG_PANEL,
                                    highlightbackground=BORDER_COLOR,
                                    highlightthickness=1)
        self.title_frame.place(x=10, y=title_y, width=W-20, height=title_h)

        self.lbl_title = tk.Label(
            self.title_frame,
            text="SEWAGE MONITORING SYSTEM",
            font=("Arial", self._fs(36), "bold"),
            fg=TEXT_WHITE, bg=BG_PANEL)
        self.lbl_title.place(relx=0.5, rely=0.5, anchor="center")

        # ── ROW 1: Metric cards ──────────────────
        row1_y = title_y + title_h + 10
        row1_h = max(140, int(H * 0.185))
        card_w = int((W - 40) / 3) - 8
        gap    = 14

        self.card_inlet  = self._metric_card(10,          row1_y, card_w, row1_h,
                                             "INLET FLOW", "m³/h", ACCENT_CYAN)
        self.card_outlet = self._metric_card(10+card_w+gap, row1_y, card_w, row1_h,
                                             "OUTLET FLOW", "m³/h", ACCENT_GREEN)
        self.card_diff   = self._metric_card(10+2*(card_w+gap), row1_y, card_w, row1_h,
                                             "DIFFERENTIAL", "m³/h", ACCENT_AMBER)

        # ── ROW 2: Status panel ──────────────────
        row2_y = row1_y + row1_h + 14
        row2_h = max(160, int(H * 0.215))
        status_w = int((W - 40) * 0.52)
        gauge_w  = (W - 40) - status_w - gap

        self.status_frame = tk.Frame(self.root, bg=BG_CARD,
                                     highlightbackground=BORDER_COLOR,
                                     highlightthickness=1)
        self.status_frame.place(x=10, y=row2_y, width=status_w, height=row2_h)

        tk.Label(self.status_frame, text="SYSTEM STATUS",
                 font=("Arial", self._fs(16), "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).place(relx=0.5, y=14, anchor="n")

        self.lbl_status = tk.Label(self.status_frame, text="NORMAL",
                                    font=("Arial", self._fs(64), "bold"),
                                    fg=ACCENT_GREEN, bg=BG_CARD)
        self.lbl_status.place(relx=0.5, rely=0.50, anchor="center")

        # Pulsing orb canvas
        self.orb_canvas = tk.Canvas(self.status_frame, bg=BG_CARD,
                                    highlightthickness=0, bd=0,
                                    width=40, height=40)
        self.orb_canvas.place(relx=0.5, rely=0.82, anchor="center")
        self.orb_oval = self.orb_canvas.create_oval(6, 6, 34, 34,
                                                     fill=ACCENT_GREEN,
                                                     outline=ACCENT_GREEN,
                                                     width=2)

        # Gauge panel
        self.gauge_frame = tk.Frame(self.root, bg=BG_CARD,
                                    highlightbackground=BORDER_COLOR,
                                    highlightthickness=1)
        self.gauge_frame.place(x=10+status_w+gap, y=row2_y,
                               width=gauge_w, height=row2_h)

        tk.Label(self.gauge_frame, text="LOAD GAUGES",
                 font=("Arial", self._fs(16), "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).place(relx=0.5, y=14, anchor="n")

        self.gauge_canvas = tk.Canvas(self.gauge_frame, bg=BG_CARD,
                                      highlightthickness=0, bd=0)
        self.gauge_canvas.place(x=0, y=40,
                                width=gauge_w, height=row2_h-50)
        self._gauge_w = gauge_w
        self._gauge_h = row2_h - 50
        self._bar_ids = {}
        self._bar_txt = {}
        self._draw_gauge_bg()

        # ── ROW 3: Trend graph ───────────────────
        graph_y = row2_y + row2_h + 14
        graph_h = H - graph_y - 10
        self.graph_frame = tk.Frame(self.root, bg=BG_CARD,
                                    highlightbackground=ACCENT_CYAN,
                                    highlightthickness=1)
        self.graph_frame.place(x=10, y=graph_y, width=W-20, height=graph_h)

        tk.Label(self.graph_frame, text="▶  FLOW VARIATION",
                 font=("Arial", self._fs(14), "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD).place(x=14, y=8)

        if MATPLOTLIB_AVAILABLE:
            self._build_graph(W-20, graph_h)
        else:
            tk.Label(self.graph_frame,
                     text="matplotlib not available — install to enable trend graph",
                     font=("Arial", self._fs(14)), fg=TEXT_DIM, bg=BG_CARD
                     ).place(relx=0.5, rely=0.5, anchor="center")

    # ── DECORATIVE BACKGROUND ────────────────────
    def _draw_background(self):
        W, H = self.W, self.H
        c = self.bg_canvas
        # scanlines
        for y in range(0, H, 6):
            c.create_line(0, y, W, y, fill="#0D1118", width=1)
        # corner accent lines
        col = "#0E1825"
        for i in range(0, 200, 20):
            c.create_line(0, i, i, 0, fill=col, width=1)
            c.create_line(W, H-i, W-i, H, fill=col, width=1)

    # ── METRIC CARD ──────────────────────────────
    def _metric_card(self, x, y, w, h, label, unit, color):
        f = tk.Frame(self.root, bg=BG_CARD,
                     highlightbackground=color,
                     highlightthickness=1)
        f.place(x=x, y=y, width=w, height=h)

        tk.Label(f, text=label,
                 font=("Arial", self._fs(13), "bold"),
                 fg=color, bg=BG_CARD).place(relx=0.5, rely=0.12, anchor="center")

        lbl_val = tk.Label(f, text="—",
                           font=("Arial", self._fs(46), "bold"),
                           fg=TEXT_WHITE, bg=BG_CARD)
        lbl_val.place(relx=0.5, rely=0.52, anchor="center")

        tk.Label(f, text=unit,
                 font=("Arial", self._fs(12)),
                 fg=TEXT_DIM, bg=BG_CARD).place(relx=0.5, rely=0.84, anchor="center")

        # bottom accent bar
        bar = tk.Frame(f, bg=color, height=3)
        bar.place(x=0, rely=1.0, anchor="sw", width=w)

        return {"frame": f, "val": lbl_val, "bar": bar, "color": color}

    # ── GAUGE BARS ───────────────────────────────
    def _draw_gauge_bg(self):
        c   = self.gauge_canvas
        gw  = self._gauge_w
        gh  = self._gauge_h
        bar_h = max(24, int(gh * 0.22))
        pad   = 16
        lbl_gap = self._fs(13) + 6          # space above each bar for label
        total_needed = 2 * (lbl_gap + bar_h)
        spacing = max(14, (gh - total_needed) // 3)

        labels = [("INLET",  ACCENT_CYAN), ("OUTLET", ACCENT_GREEN)]

        for i, (lbl, color) in enumerate(labels):
            y_lbl = spacing + i * (lbl_gap + bar_h + spacing)
            y0    = y_lbl + lbl_gap
            y1    = y0 + bar_h

            # track bg
            rounded_rect(c, pad, y0, gw-pad, y1, r=bar_h//2,
                         fill=GRID_LINE, outline="")
            # filled bar (starts at 0)
            bid = rounded_rect(c, pad, y0, pad, y1, r=bar_h//2,
                               fill=color, outline="")
            # label — placed clearly above bar
            c.create_text(pad + 4, y_lbl + lbl_gap//2,
                          text=lbl,
                          font=("Arial", self._fs(11), "bold"),
                          fill=color, anchor="w")
            # value text — centred inside bar
            tid = c.create_text(gw // 2, (y0 + y1) // 2,
                                 text="0.0",
                                 font=("Arial", self._fs(14), "bold"),
                                 fill=TEXT_WHITE, anchor="center")
            self._bar_ids[lbl] = (bid, y0, y1, pad, gw - pad)
            self._bar_txt[lbl] = tid

    def _update_gauge(self, label, value, max_val=100):
        if label not in self._bar_ids:
            return
        bid, y0, y1, x0, x1 = self._bar_ids[label]
        frac = min(max(value / max_val, 0), 1)
        new_x = x0 + int((x1 - x0) * frac)
        bar_h = y1 - y0
        self.gauge_canvas.coords(bid, x0, y0, max(new_x, x0+1), y1)
        color = ACCENT_RED if frac > 0.8 else (ACCENT_AMBER if frac > 0.6 else
                (ACCENT_CYAN if label == "INLET" else ACCENT_GREEN))
        self.gauge_canvas.itemconfig(bid, fill=color)
        self.gauge_canvas.itemconfig(self._bar_txt[label],
                                     text=f"{value:.1f}")

    # ── MATPLOTLIB GRAPH ─────────────────────────
    def _build_graph(self, fw, fh):
        dpi    = 96
        fig_w  = (fw - 4) / dpi
        fig_h  = (fh - 44) / dpi

        self.fig = Figure(figsize=(fig_w, fig_h), dpi=dpi,
                          facecolor=BG_CARD)
        self.ax  = self.fig.add_subplot(111)
        self._style_ax()

        xs = list(range(HISTORY_LEN))
        self.line_inlet,  = self.ax.plot(xs, [0]*HISTORY_LEN,
                                          color=TEXT_WHITE, linewidth=1.8,
                                          label="INLET", zorder=3)
        self.line_outlet, = self.ax.plot(xs, [0]*HISTORY_LEN,
                                          color=ACCENT_GREEN, linewidth=1.8,
                                          label="OUTLET", zorder=3)

        # Fill areas
        self.fill_inlet  = self.ax.fill_between(xs, [0]*HISTORY_LEN,
                                                  color=TEXT_WHITE, alpha=0.05)
        self.fill_outlet = self.ax.fill_between(xs, [0]*HISTORY_LEN,
                                                  color=ACCENT_GREEN, alpha=0.07)

        legend = self.ax.legend(
            loc="upper right",
            facecolor=BG_PANEL, edgecolor=BORDER_COLOR,
            labelcolor=TEXT_WHITE,
            fontsize=self._fs(11))

        self.fig.tight_layout(pad=0.5)

        self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_mpl.get_tk_widget().place(x=0, y=36,
                                               width=fw-4, height=fh-40)
        self.canvas_mpl.draw()

    def _style_ax(self):
        ax = self.ax
        ax.set_facecolor(BG_CARD)
        ax.tick_params(colors=TEXT_DIM, labelsize=self._fs(9))
        ax.spines["bottom"].set_color(BORDER_COLOR)
        ax.spines["left"].set_color(BORDER_COLOR)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlim(0, HISTORY_LEN - 1)
        ax.set_ylim(0, 105)
        ax.set_ylabel("m³/h", color=TEXT_DIM, fontsize=self._fs(10))
        ax.yaxis.label.set_color(TEXT_DIM)
        ax.grid(True, color=GRID_LINE, linewidth=0.6, linestyle="--", alpha=0.8)
        ax.set_xticks([])

    def _update_graph(self, inlet_h, outlet_h):
        if not MATPLOTLIB_AVAILABLE:
            return
        xs = list(range(HISTORY_LEN))
        self.line_inlet.set_ydata(inlet_h)
        self.line_outlet.set_ydata(outlet_h)

        # Redraw fill
        for coll in [self.fill_inlet, self.fill_outlet]:
            coll.remove()
        self.fill_inlet  = self.ax.fill_between(xs, inlet_h,
                                                  color=TEXT_WHITE, alpha=0.05)
        self.fill_outlet = self.ax.fill_between(xs, outlet_h,
                                                  color=ACCENT_GREEN, alpha=0.07)
        self.canvas_mpl.draw_idle()

    # ── PULSING ORB ──────────────────────────────
    def _pulse_orb(self, status):
        self._orb_phase += 0.15
        alpha_frac = (math.sin(self._orb_phase) + 1) / 2   # 0..1
        color = STATUS_COLORS.get(status, ACCENT_GREEN)

        # Interpolate size
        size = int(8 + 14 * alpha_frac)
        cx, cy = 20, 20
        self.orb_canvas.coords(self.orb_oval,
                               cx-size, cy-size, cx+size, cy+size)
        self.orb_canvas.itemconfig(self.orb_oval, fill=color, outline=color)

    # ── MAIN UI TICK ─────────────────────────────
    def _ui_tick(self):
        try:
            inlet, outlet, inlet_h, outlet_h, online = self.data.snapshot()
            diff   = inlet - outlet
            status = self.data.status()

            # ── Timestamp ──────────────────────────
            self.lbl_time.config(
                text=time.strftime("%Y-%m-%d   %H:%M:%S"))

            # ── Connection indicator ────────────────
            if online:
                self.lbl_conn.config(text="● LIVE", fg=ACCENT_GREEN)
            else:
                self.lbl_conn.config(text="● SIM",  fg=ACCENT_AMBER)

            # ── Metric cards ───────────────────────
            self.card_inlet["val"].config(text=f"{inlet:.1f}")
            self.card_outlet["val"].config(text=f"{outlet:.1f}")

            diff_color = ACCENT_RED if abs(diff) > 20 else ACCENT_AMBER if abs(diff) > 10 else ACCENT_GREEN
            self.card_diff["val"].config(text=f"{diff:+.1f}", fg=diff_color)

            # ── Status label ───────────────────────
            s_color = STATUS_COLORS.get(status, ACCENT_GREEN)
            self.lbl_status.config(text=status, fg=s_color)

            # ── Orb pulse ──────────────────────────
            self._pulse_orb(status)

            # ── Gauge bars ─────────────────────────
            self._update_gauge("INLET",  inlet)
            self._update_gauge("OUTLET", outlet)

            # ── Graph ──────────────────────────────
            self._update_graph(inlet_h, outlet_h)

        except Exception as e:
            pass  # Keep running silently

        self.root.after(int(1000 / (UPDATE_HZ * 2)), self._ui_tick)

    # ── HELPERS ──────────────────────────────────
    def _fs(self, base):
        """Scale font size relative to screen height (base designed for 1080p)."""
        scale = self.H / 1080
        return max(8, int(base * scale))

    def _quit(self, event=None):
        self.stop_event.set()
        try:
            self.root.destroy()
        except Exception:
            pass
        sys.exit(0)

    def run(self):
        self.root.mainloop()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = SewageMonitorApp()
    app.run()
