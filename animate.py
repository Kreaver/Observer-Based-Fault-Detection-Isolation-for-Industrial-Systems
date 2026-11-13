# animate.py
# Live animation of the quadruple-tank process.
# Run from the project folder:  python3 animate.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle

from plant import quad_tank as qt
from plant.quad_tank import quad_tank_dynamics, steady_state

# ---------------- Settings (edit these) ----------------
h = np.array([0.05, 0.05, 0.05, 0.05])  # initial levels (m)
u = np.array([3.0, 3.0])                # pump voltages (V)
dt = 0.1                                # integration step (s)
t_end = 1000.0                          # simulated time (s)
STEPS_PER_FRAME = 20                    # sim steps per frame -> speed (20 x 0.1 s = 2 s per frame)
TANK_HEIGHT = 0.20                      # physical tank height (m), Johansson's rig = 20 cm
# -------------------------------------------------------

h_ss = steady_state(u)
n_frames = int(t_end / (dt * STEPS_PER_FRAME))
CM = 100  # m -> cm for display


def flows(h, u):
    """All flows in the system (m^3/s), using the parameters in quad_tank.py."""
    h = np.maximum(h, 0.0)
    Q1, Q2 = qt.k1 * u[0], qt.k2 * u[1]
    out = np.array([qt.a1, qt.a2, qt.a3, qt.a4]) * np.sqrt(2 * qt.g * h)
    return {
        "p1_to_3": qt.gamma1 * Q1,
        "p1_to_2": (1 - qt.gamma1) * Q1,
        "p2_to_4": qt.gamma2 * Q2,
        "p2_to_1": (1 - qt.gamma2) * Q2,
        "out": out,  # outflow of tanks 1..4
    }


# ---------------- Figure layout ----------------
fig = plt.figure(figsize=(13, 7))
fig.canvas.manager.set_window_title("Quadruple-Tank Process")
ax_tanks = fig.add_axes([0.02, 0.05, 0.45, 0.90])
ax_plot = fig.add_axes([0.55, 0.40, 0.42, 0.52])
ax_info = fig.add_axes([0.55, 0.04, 0.42, 0.26])

ax_tanks.set_xlim(0, 10)
ax_tanks.set_ylim(0, 10.5)
ax_tanks.set_aspect("equal")
ax_tanks.axis("off")
ax_info.axis("off")

# Tank geometry in drawing coordinates: (x_left, y_bottom), width, height
TW, TH = 2.0, 3.0
tank_xy = [(1.5, 5.5), (6.5, 5.5), (1.5, 1.5), (6.5, 1.5)]  # tanks 1, 2, 3, 4
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

# Reservoir and pumps
ax_tanks.add_patch(Rectangle((0, 0), 10, 0.9, color="lightsteelblue", alpha=0.5))
ax_tanks.text(5, 0.35, "reservoir", ha="center", fontsize=9, color="gray")
for x, name in [(0.5, "P1"), (9.5, "P2")]:
    ax_tanks.add_patch(Circle((x, 0.5), 0.35, fc="white", ec="black", lw=1.5, zorder=3))
    ax_tanks.text(x, 0.5, name, ha="center", va="center", fontsize=8, weight="bold", zorder=4)

# Pipes (pump 1 = solid dark, pump 2 = dashed dark)
pipe = dict(color="dimgray", lw=2, zorder=1)
# Pump 1 -> tank 3 (same side, gamma1) and -> tank 2 (cross, 1-gamma1)
ax_tanks.plot([0.5, 0.5, 7.2, 7.2], [0.85, 9.7, 9.7, 8.6], **pipe)
ax_tanks.plot([0.5, 2.2, 2.2], [4.9, 4.9, 4.6], **pipe)
# Pump 2 -> tank 4 (same side, gamma2) and -> tank 1 (cross, 1-gamma2)
ax_tanks.plot([9.5, 9.5, 2.8, 2.8], [0.85, 9.25, 9.25, 8.6], ls="--", **pipe)
ax_tanks.plot([9.5, 7.8, 7.8], [4.9, 4.9, 4.6], ls="--", **pipe)
# Drains: tank 1 -> 3, tank 2 -> 4, tanks 3/4 -> reservoir
for x, y0, y1 in [(2.5, 5.5, 4.6), (7.5, 5.5, 4.6), (2.5, 1.5, 0.9), (7.5, 1.5, 0.9)]:
    ax_tanks.annotate("", xy=(x, y1), xytext=(x, y0),
                      arrowprops=dict(arrowstyle="->", color="steelblue", lw=1.5))

# Flow labels (updated every frame)
flow_txt = {
    "p1_to_3": ax_tanks.text(0.65, 5.1, "", fontsize=7.5),
    "p1_to_2": ax_tanks.text(4.0, 9.85, "", fontsize=7.5, ha="center"),
    "p2_to_4": ax_tanks.text(9.35, 5.1, "", fontsize=7.5, ha="right"),
    "p2_to_1": ax_tanks.text(5.0, 8.85, "", fontsize=7.5, ha="center"),
}
out_txt = [
    ax_tanks.text(2.6, 4.95, "", fontsize=7.5, color="steelblue"),
    ax_tanks.text(7.6, 4.95, "", fontsize=7.5, color="steelblue"),
    ax_tanks.text(2.6, 1.05, "", fontsize=7.5, color="steelblue"),
    ax_tanks.text(7.6, 1.05, "", fontsize=7.5, color="steelblue"),
]

# Tanks: outline, water, steady-state marker, labels
outlines, waters, level_txt = [], [], []
for i, (x, y) in enumerate(tank_xy):
    water = Rectangle((x, y), TW, 0, color=colors[i], alpha=0.55, zorder=2)
    outline = Rectangle((x, y), TW, TH, fill=False, ec="black", lw=2, zorder=3)
    ax_tanks.add_patch(water)
    ax_tanks.add_patch(outline)
    y_ss = y + TH * min(h_ss[i] / TANK_HEIGHT, 1.0)
    ax_tanks.plot([x, x + TW], [y_ss, y_ss], ls=":", color="black", lw=1.2, zorder=4)
    ax_tanks.text(x + TW / 2, y + TH - 0.3, f"Tank {i + 1}", ha="center", va="center", fontsize=10, weight="bold", zorder=5)
    level_txt.append(ax_tanks.text(x + TW / 2, y + TH / 2, "", ha="center", va="center",
                                   fontsize=10, weight="bold", zorder=5))
    waters.append(water)
    outlines.append(outline)

# Sensor tags on the measured tanks (3 and 4)
for i, name in [(2, "y1"), (3, "y2")]:
    x, y = tank_xy[i]
    ax_tanks.text(x + TW + 0.1, y + TH - 0.2, f"◉ {name}", fontsize=9, color="purple", weight="bold")
ax_tanks.text(0.1, 10.3, "dotted line = steady state   ◉ = level sensor",
              fontsize=8, color="gray")

# Level plot
ax_plot.set_xlim(0, t_end)
ax_plot.set_ylim(0, max(TANK_HEIGHT, h.max(), h_ss.max()) * CM * 1.15)
ax_plot.set_xlabel("Time (s)")
ax_plot.set_ylabel("Water level (cm)")
ax_plot.set_title("Tank levels")
ax_plot.grid(alpha=0.4)
ax_plot.axhline(TANK_HEIGHT * CM, color="black", lw=1, alpha=0.5)
ax_plot.text(5, TANK_HEIGHT * CM + 0.3, "tank top", fontsize=8, alpha=0.6)
lines = []
for i in range(4):
    (ln,) = ax_plot.plot([], [], color=colors[i], label=f"Tank {i + 1}")
    ax_plot.axhline(h_ss[i] * CM, color=colors[i], ls=":", lw=1)
    lines.append(ln)
ax_plot.legend(loc="upper right", fontsize=8)

info = ax_info.text(0, 1, "", va="top", family="monospace", fontsize=9.5)

# ---------------- Simulation state ----------------
t = 0.0
t_hist, h_hist = [0.0], [h.copy()]


def update(frame):
    global h, t
    for _ in range(STEPS_PER_FRAME):
        h = np.maximum(h + quad_tank_dynamics(h, u) * dt, 0.0)
        t += dt
    t_hist.append(t)
    h_hist.append(h.copy())

    # Tanks
    for i, (x, y) in enumerate(tank_xy):
        frac = h[i] / TANK_HEIGHT
        waters[i].set_height(TH * min(frac, 1.0))
        overflow = frac > 1.0
        outlines[i].set_edgecolor("red" if overflow else "black")
        level_txt[i].set_text(f"{h[i] * CM:.2f} cm" + ("\nOVERFLOW" if overflow else ""))
        level_txt[i].set_color("red" if overflow else "black")

    # Flows (cm^3/s)
    f = flows(h, u)
    flow_txt["p1_to_3"].set_text(f"γ1·Q1\n{f['p1_to_3'] * 1e6:.2f}")
    flow_txt["p1_to_2"].set_text(f"(1-γ1)·Q1 = {f['p1_to_2'] * 1e6:.2f} cm³/s")
    flow_txt["p2_to_4"].set_text(f"γ2·Q2\n{f['p2_to_4'] * 1e6:.2f}")
    flow_txt["p2_to_1"].set_text(f"(1-γ2)·Q2 = {f['p2_to_1'] * 1e6:.2f} cm³/s")
    for i in range(4):
        out_txt[i].set_text(f"{f['out'][i] * 1e6:.2f}")

    # Plot
    H = np.array(h_hist) * CM
    for i in range(4):
        lines[i].set_data(t_hist, H[:, i])

    # Info panel
    err = (h - h_ss) * CM
    phase = "minimum phase" if qt.gamma1 + qt.gamma2 > 1 else "NON-minimum phase"
    info.set_text(
        f"t = {t:7.1f} s   ({STEPS_PER_FRAME * dt:.0f} s simulated per frame)\n"
        f"Pumps:  u1 = {u[0]:.2f} V   u2 = {u[1]:.2f} V\n"
        f"Valves: γ1 = {qt.gamma1:.2f}   γ2 = {qt.gamma2:.2f}   "
        f"(γ1+γ2 = {qt.gamma1 + qt.gamma2:.2f}, {phase})\n"
        f"\n"
        f"           Tank 1   Tank 2   Tank 3   Tank 4\n"
        f"level cm  {h[0]*CM:7.2f}  {h[1]*CM:7.2f}  {h[2]*CM:7.2f}  {h[3]*CM:7.2f}\n"
        f"target cm {h_ss[0]*CM:7.2f}  {h_ss[1]*CM:7.2f}  {h_ss[2]*CM:7.2f}  {h_ss[3]*CM:7.2f}\n"
        f"error cm  {err[0]:7.2f}  {err[1]:7.2f}  {err[2]:7.2f}  {err[3]:7.2f}\n"
        f"Measured outputs: y1 = h3 = {h[2]*CM:.2f} cm,  y2 = h4 = {h[3]*CM:.2f} cm"
    )
    return []


anim = FuncAnimation(fig, update, frames=n_frames, interval=30, repeat=False)

if __name__ == "__main__":
    plt.show()
