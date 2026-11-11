# plant/quad_tank.py
# Kevin Rivera

import numpy as np

## Position of the tanks in the system
#        Tank_1              Tank_2
#          |                   |
#        Tank_3              Tank_4

# All units SI (m, m^2, m^3/s). Values below are the standard Johansson
# quadruple-tank lab values converted to SI -- replace with your tanks' actual values.

#################
# tank 1 var
A1 = 28e-4     # cross-sectional area (m^2)   [28 cm^2]
a1 = 0.071e-4  # outflow hole area (m^2)      [0.071 cm^2]

# tank 2 var
A2 = 32e-4     # [32 cm^2]
a2 = 0.057e-4  # [0.057 cm^2]

# tank 3 var
A3 = 28e-4     # [28 cm^2]
a3 = 0.071e-4  # [0.071 cm^2]

# tank 4 var
A4 = 32e-4     # [32 cm^2]
a4 = 0.057e-4  # [0.057 cm^2]
##################

g = 9.81  # Acceleration due to gravity (m/s^2)

# Pump gains (m^3/s per V): Add controllable pump flow rates later
k1 = 3.33e-6
k2 = 3.35e-6

# Valve split ratios: Add controllable valve split ratios later
gamma1 = 0.7  # Split ratio for pump 1
gamma2 = 0.6  # Split ratio for pump 2


# Function to calculate the change in water level over time
def quad_tank_dynamics(h, u):
    h1, h2, h3, h4 = np.maximum(h, 0.0)  # Unpack levels; clamp so sqrt never sees a negative
    u1, u2 = u                           # Unpack pump voltages

    # Pump flow rates (need u, so they must be computed inside the function)
    Q1 = k1 * u1
    Q2 = k2 * u2

    # Pump flow split to tanks
    Q1_in = (1 - gamma1) * Q1
    Q3_in = gamma1 * Q1

    Q2_in = (1 - gamma2) * Q2
    Q4_in = gamma2 * Q2

    # Outflows (Torricelli)
    Q1_out = a1 * np.sqrt(2 * g * h1)
    Q2_out = a2 * np.sqrt(2 * g * h2)
    Q3_out = a3 * np.sqrt(2 * g * h3)
    Q4_out = a4 * np.sqrt(2 * g * h4)

    # Top tanks drain into the tanks below them
    Q3_total_in = Q1_out + Q3_in
    Q4_total_in = Q2_out + Q4_in

    # Change in water level over time
    dh1_dt = (Q1_in - Q1_out) / A1
    dh2_dt = (Q2_in - Q2_out) / A2
    dh3_dt = (Q3_total_in - Q3_out) / A3
    dh4_dt = (Q4_total_in - Q4_out) / A4

    return np.array([dh1_dt, dh2_dt, dh3_dt, dh4_dt])