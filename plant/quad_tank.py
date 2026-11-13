# plant/quad_tank.py
# Kevin Rivera
#
# Standard quadruple-tank process (Johansson, 2000), with cross-coupled pumps.

import numpy as np

## Position of the tanks in the system
#
#        Tank_1              Tank_2          <- top tanks
#          |                   |
#        Tank_3              Tank_4          <- bottom tanks
#
#   Pump 1 --(gamma1)-------> Tank_3   (bottom, same side)
#          --(1 - gamma1)---> Tank_2   (top, opposite side)
#
#   Pump 2 --(gamma2)-------> Tank_4   (bottom, same side)
#          --(1 - gamma2)---> Tank_1   (top, opposite side)
#
#   Tank_1 drains into Tank_3, Tank_2 drains into Tank_4.
#
# Mapping to Johansson's paper numbering:
#   ours Tank_3 = paper Tank 1,  ours Tank_4 = paper Tank 2,
#   ours Tank_1 = paper Tank 3,  ours Tank_2 = paper Tank 4.

# All units SI (m, m^2, m^3/s). Values are Johansson's lab values converted
# to SI -- replace with your tanks' actual values.

#################
# tank 1 var (top left)
A1 = 28e-4     # cross-sectional area (m^2)   [28 cm^2]
a1 = 0.071e-4  # outflow hole area (m^2)      [0.071 cm^2]

# tank 2 var (top right)
A2 = 32e-4     # [32 cm^2]
a2 = 0.057e-4  # [0.057 cm^2]

# tank 3 var (bottom left)
A3 = 28e-4     # [28 cm^2]
a3 = 0.071e-4  # [0.071 cm^2]

# tank 4 var (bottom right)
A4 = 32e-4     # [32 cm^2]
a4 = 0.057e-4  # [0.057 cm^2]
##################

g = 9.81  # Acceleration due to gravity (m/s^2)

# Pump gains (m^3/s per V)
k1 = 3.33e-6
k2 = 3.35e-6

# Valve split ratios: fraction of each pump's flow that goes to the bottom tank
# on its own side. gamma1 + gamma2 > 1 -> minimum phase; < 1 -> non-minimum phase.
gamma1 = 0.7
gamma2 = 0.6


# Function to calculate the change in water level over time
def quad_tank_dynamics(h, u):
    h1, h2, h3, h4 = np.maximum(h, 0.0)  # Unpack levels; clamp so sqrt never sees a negative
    u1, u2 = u                           # Unpack pump voltages

    # Pump flow rates
    Q1 = k1 * u1
    Q2 = k2 * u2

    # Pump flow split to tanks (cross-coupled)
    Q3_pump = gamma1 * Q1          # pump 1 -> bottom left
    Q2_pump = (1 - gamma1) * Q1    # pump 1 -> top right
    Q4_pump = gamma2 * Q2          # pump 2 -> bottom right
    Q1_pump = (1 - gamma2) * Q2    # pump 2 -> top left

    # Outflows (Torricelli)
    Q1_out = a1 * np.sqrt(2 * g * h1)
    Q2_out = a2 * np.sqrt(2 * g * h2)
    Q3_out = a3 * np.sqrt(2 * g * h3)
    Q4_out = a4 * np.sqrt(2 * g * h4)

    # Change in water level over time
    dh1_dt = (Q1_pump - Q1_out) / A1
    dh2_dt = (Q2_pump - Q2_out) / A2
    dh3_dt = (Q3_pump + Q1_out - Q3_out) / A3   # top-left drains into tank 3
    dh4_dt = (Q4_pump + Q2_out - Q4_out) / A4   # top-right drains into tank 4

    return np.array([dh1_dt, dh2_dt, dh3_dt, dh4_dt])



def steady_state(u):
    """Compute the steady-state water levels for given pump voltages u."""
    u1, u2 = u
    Q1 = k1 * u1
    Q2 = k2 * u2

    # Steady-state outflows equal inflows
    h1_ss = (Q2 * (1 - gamma2) / a1) ** 2 / (2 * g)
    h2_ss = (Q1 * (1 - gamma1) / a2) ** 2 / (2 * g)
    h3_ss = ((gamma1 * Q1 + a1 * np.sqrt(2 * g * h1_ss)) / a3) ** 2 / (2 * g)
    h4_ss = ((gamma2 * Q2 + a2 * np.sqrt(2 * g * h2_ss)) / a4) ** 2 / (2 * g)

    return np.array([h1_ss, h2_ss, h3_ss, h4_ss])