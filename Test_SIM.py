##Kevin Rivera
##Test 

import numpy as np
import scipy
import matplotlib as plt
import control 


print("Hello, World! Python is working?")
print("Numpy version:", np.__version__)

time = np.linspace(0, 10, 100)
water_level = 5 + 0.5 * time

plt.plot(time, water_level)
plt.xlabel("Time")
plt.ylabel("Water Level")
plt.title("Water Level Simulation")
plt.show()

print("Final water level:", water_level[-1])