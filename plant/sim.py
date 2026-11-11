import numpy as np
from plant.quad_tank import quad_tank_dynamics

# Initial water levels (m)
h = np.array([0.2, 0.2, 0.2, 0.2])

# Pump inputs (V)
u = np.array([2.0, 2.0])

# Time step (s) and total simulation time (s)
dt = 0.1
t_end = 600.0

for step in range(int(t_end / dt)):
    dh_dt = quad_tank_dynamics(h, u)   # rates of change
    h = np.maximum(h + dh_dt * dt, 0)  # Euler update; levels can't go below 0

    if step % int(60 / dt) == 0:       # print once per simulated minute
        print(f"t = {step * dt:6.1f} s   h = {np.round(h, 4)}")

print(f"t = {t_end:6.1f} s   h = {np.round(h, 4)}")