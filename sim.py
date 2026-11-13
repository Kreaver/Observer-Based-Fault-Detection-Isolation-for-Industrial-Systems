import numpy as np
import matplotlib.pyplot as plt
from plant.quad_tank import quad_tank_dynamics, steady_state

# Initial water levels (m)
h = np.array([0.5, 0.35, 0.22, 0.1])

# Pump inputs (V)
u = np.array([3.0, 3.0])

# Time step (s) and total simulation time (s)
dt = 0.1
t_end = 600.0
n_steps = int(t_end / dt)

# Storage for plotting (row k = state at time[k])
time = np.arange(n_steps + 1) * dt
h_history = np.zeros((n_steps + 1, 4))
h_history[0] = h

for k in range(n_steps):
    dh_dt = quad_tank_dynamics(h, u)   # rates of change
    h = np.maximum(h + dh_dt * dt, 0)  # Euler update; levels can't go below 0
    h_history[k + 1] = h

print(f"Final levels at t = {t_end:.0f} s: {np.round(h, 4)}")

# Split columns out per tank
h1_values = h_history[:, 0]
h2_values = h_history[:, 1]
h3_values = h_history[:, 2]
h4_values = h_history[:, 3]

plt.plot(time, h1_values, label="Tank 1")
plt.plot(time, h2_values, label="Tank 2")
plt.plot(time, h3_values, label="Tank 3")
plt.plot(time, h4_values, label="Tank 4")

plt.xlabel("Time (s)")
plt.ylabel("Water Level (m)")
plt.title(f"Quad tank levels (u1 = {u[0]} V, u2 = {u[1]} V)")
plt.legend()
plt.grid()
plt.savefig("tank_levels.png", dpi=150)
plt.show()

u = np.array([3.0, 3.0])
h0 = steady_state(u)
print(h0)
print(quad_tank_dynamics(h0, u))