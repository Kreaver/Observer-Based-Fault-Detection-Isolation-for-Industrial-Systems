import numpy as np
from plant.quad_tank import quad_tank_dynamics

# Initial water levels (m)
h = np.array([0.2, 0.2, 0.2, 0.2])

# Pump inputs (V)
u = np.array([2.0, 2.0])

# Time step (seconds)
dt = 0.1

# Calculate rates of change
dh_dt = quad_tank_dynamics(h, u)

# Update water levels
h = h + dh_dt * dt

print(h)