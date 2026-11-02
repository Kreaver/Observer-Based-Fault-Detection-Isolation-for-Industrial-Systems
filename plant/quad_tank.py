


A_i = 100  # Example value, replace with tanks actual cross-sectional area
a_i = 1  # Example value, replace with tanks actual outflow area
h_i = 5  # Initial water level
Qin_i = 2  # Inflow rate
Qout_i = 1  # Outflow rate

h_i = 0.2 #tank hegiht

#Current tank conditions
dt = 0.1  # Time step

#calculate the change in water level over time
dh_dt = (Qin_i - Qout_i) / A_i

#calculate the new water level after one time step
dh = dh_dt * dt

#update the water level
h_i = h_i + dh

print("Updated water level after one time step:", h_i)

