#!/usr/bin/env python

"""

Final Project
CSC-432
Rachelle Pinckney

"""

#IMPORTS:
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


# Plot HR_sv as HR_v varies given:
#   HR_s = 200 bpm
#   HR_0 = 110 bpm
#   HR_min = 30 bpm.

# ordinary variables
hr_s = 200.0 #bpm
hr_0 = 110.0 #bpm
hr_min = 30.0 #bpm

# stock variables
# hr_v

# HR_v grid
# - plot a range of HR_v values from greatest (HR_0) to least (HR_min)
dv = 1.0  #bpm
hr_v_grid = np.arange(hr_0, hr_min-1, -dv)

# derived variables
#hr_sv = hr_v_grid + ((hr_s - hr_0)*((hr_v_grid - hr_min)/(hr_0 - hr_min)))
def hr_sv(hr_v, hr_s, hr_0, hr_min):
    return hr_v + ((hr_s - hr_0)*((hr_v - hr_min)/(hr_0 - hr_min)))

# plot:
fig, ax = plt.subplots(figsize=(12,8), subplot_kw=dict(xlabel="HR_v (bpm)",
                                                       ylabel="HR_sv (bpm)"))
ax.plot(hr_v_grid, hr_sv(hr_v_grid, hr_s, hr_0, hr_min), 'b',
        label="HR_sv as HR_v varies")
ax.set_xlim(hr_0, hr_min)
ax.legend(loc="upper right")
plt.plot(hr_v_grid, [60]*len(hr_v_grid), 'ro')
plt.plot(hr_v_grid, [80]*len(hr_v_grid), 'ro')
plt.show()

# get the slope
delta_y = hr_sv(hr_min, hr_s, hr_0, hr_min) - hr_sv(hr_0, hr_s, hr_0, hr_min)
delta_x = hr_min - hr_0
slope = delta_y/delta_x
print "slope = ", slope
# equals 2.125


# Plot deltaHR as norepinephrine levels vary given:
#   deltaHRmax = 72.6 bpm
#   K_f = 1.21 Hz
#   t_NE = the time constant of the NE removal process = 9.1s

# ordinary  variables
deltaHRmax = 72.6 #bpm
K_f = 1.21 #Hz
t_NE = 9.1 #s

# stock variables
# [NE] = step increase of norepinephrine concentration
# note: HR_s_0 = 120 bpm , f_0 = 50 Hz (as per Mokrane and Nadeau)
# note: f_f = .5 Hz (final freq. value between 4 and .5 Hz)
# note: [NE] = q*t_NE*f (as per Mokrane and Nadeau - eqn. A7)
#       where q = 1 is assumed
ne_0 = 1.0 * t_NE * 50 #units #start
ne_f = 1.0 * t_NE * .5 #units #end

# derived stock variables
def dHR_sdt(ne, deltaHRmax=72.6, K_f=1.21, t_NE=9.1):#rate of change for HR_s
    return (deltaHRmax * ne**2)/((K_f * t_NE)**2 + ne**2)

# norepinephrine concentration grid
d_ne = 1.0  #concentration unit
ne_grid = np.arange(ne_0, ne_f-1, -d_ne)
ne_grid_prime = np.arange(ne_f, -1, -d_ne) #to display effects of concentration
                                           #through total depletion

# plot:
fig, ax = plt.subplots(figsize=(12,8),
                       subplot_kw=dict(xlabel="Norepinephrine Concentration",
                                       ylabel="Change in HR_sv (bpm)"))
ax.plot(ne_grid, dHR_sdt(ne_grid), 'b', label="Norepinephrine Effect on HR")
ax.set_xlim(ne_0, 0)
ax.legend(loc="upper right")
plt.plot(ne_grid_prime, dHR_sdt(ne_grid_prime), 'go')
plt.show()


# Now combine them to solve for HR_sv
# HRsv_i = (2.125 + HRsv_i-1) +
#          ((deltaHR + HRsv_i-1 ) - HR0) *
#          ((2.125 + HRsv_i-1) - HRmin)/(HR0 - HRmin)
def hr_v_func(hr_prev):
    return 2.125 + hr_prev #new hr_v

def hr_s_func(hr_prev, ne):
    return dHR_sdt(ne) + hr_prev #new hr_s

def hr_sv_func(ne, hr_curr, hr_0, hr_min):
    hr_v_new = hr_v_func(hr_curr)
    hr_s_new = hr_s_func(hr_curr, ne)
    hr_curr = hr_v_new+((hr_s_new - hr_0)*((hr_v_new - hr_min)/(hr_0 - hr_min)))
    return hr_curr

hr_curr = hr_0
combined_hr_values = hr_sv_func(ne_grid, hr_curr, hr_0, hr_min)
#print combined_hr_values

# plot:
fig, ax = plt.subplots(figsize=(12,8),
                       subplot_kw=dict(xlabel="Norepinephrine Concentration",
                                       ylabel="HR_sv (bpm)"))
ax.plot(ne_grid, combined_hr_values, 'b', label="HR_sv")
ax.set_xlim(ne_0, ne_f)
ax.legend(loc="upper right")
plt.show()
