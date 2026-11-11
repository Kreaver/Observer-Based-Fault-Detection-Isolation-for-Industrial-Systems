# plant/quad_tank.py
# Kevin Rivera

import numpy as np

## Position of the tanks in the system
#        Tank_1              Tank_2
#          |                   |
#        Tank_3              Tank_4


#################
#tank 1 var 
A1 = 100  # Example value, replace with tanks actual cross-sectional area
a1 = 1  # Example value, replace with tanks actual outflow area

#tank 2 var
A2 = 100  # Example value, replace with tanks actual cross-sectional area
a2 = 1  # Example value, replace with tanks actual outflow area

#tank 3 var
A3 = 100  # Example value, replace with tanks actual cross-sectional area
a3 = 1  # Example value, replace with tanks actual outflow area

#tank 4 var
A4 = 100  # Example value, replace with tanks actual cross-sectional area
a4 = 1  # Example value, replace with tanks actual outflow area

##################

g = 9.81  # Acceleration due to gravity (m/s^2)

#Current tank conditions
dt = 0.1  # Time step


#2 Pump flow rates: Add controlable pumps flow rate later
k1 = 3.33e-6
k2 = 3.35e-6

Q1 = k1 * u1  # Inflow rate to Tank 1
Q2 = k2 * u2  # Inflow rate to Tank 2

#valve split ratios: Add controlable valve split ratios later
gamma1 = 0.7  # Split ratio for Tank 1
gamma2 = 0.6  # Split ratio for Tank 2


#Function to calculate the change in water level over time
def quad_tank_dynamics(h1, h2, h3, h4, u1, u2):
   
#pump flow rates to tanks: Add controlable pumps flow rate later
Q1_in = (1 - gamma1) * Q1  
Q3_in = gamma1 * Q1  

Q2_in = (1 - gamma2) * Q2  
Q4_in = gamma2 * Q2  


Q1_out = a1 * np.sqrt(2 * g * h1)  # Outflow rate from Tank 1
Q2_out = a2 * np.sqrt(2 * g * h2)  # Outflow rate from Tank 2

Q3_total_in = Q1_out +  Q3_in 
Q4_total_in = Q2_out +  Q4_in


Q3_out = a3 * np.sqrt(2 * g * h3)
Q4_out = a4 * np.sqrt(2 * g * h4)

#calculate the change in water level over time
dh1_dt = (Q1_in - Q1_out) / A1
dh2_dt = (Q2_in - Q2_out) / A2
dh3_dt = (Q3_total_in - Q3_out) / A3
dh4_dt = (Q4_total_in - Q4_out) / A4

return np.array([dh1_dt, dh2_dt, dh3_dt, dh4_dt])


#calculate the new water level after one time step
# dh1 = dh1_dt * dt 
# dh2 = dh2_dt * dt
# dh3 = dh3_dt * dt
# dh4 = dh4_dt * dt

#update the water level
# h1 = h1 + dh1
# h2 = h2 + dh2
# h3 = h3 + dh3
# h4 = h4 + dh4

# print("Updated water level after one time step:", h1, h2, h3, h4)

