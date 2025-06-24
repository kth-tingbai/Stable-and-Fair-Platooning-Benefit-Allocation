# -*- coding: utf-8 -*-
"""
Created on Tue May  6 17:10:58 2025

The code is used to show the 3-D plot of the stability probability of the payoff allocation proposed in Theorem 1 
with different xi in different cases

@author: tingbai
"""
f=open('Probability_in_different_parameters_Case1','r')
a=f.read()
Pro_stability_save=eval(a) 
f.close()

f=open('Upbound_parameters_Case1','r')
a=f.read()
upbound_1=eval(a) 
f.close()

epsilon_f=0.07
epsilon_e=0.048

Pro_stability_1=Pro_stability_save[(epsilon_f,epsilon_e)]

import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

# Sort keys to ensure proper plotting order
x_keys = sorted(Pro_stability_1.keys())  # Number of EVs 
y_keys = sorted(next(iter(Pro_stability_1.values())).keys())  # Parameter values

# Create a meshgrid
X, Y = np.meshgrid(x_keys, y_keys)

# Initialize Z-values (stability probabilities)
Z = np.zeros_like(X, dtype=float)

# Populate Z from the dictionary
for i, x in enumerate(x_keys):           # x: number of EVs
    for j, y in enumerate(y_keys):       # y: parameter
        Z[j, i] = Pro_stability_1[x].get(y, 0)      # Use .get() to avoid missing key errors
        
opt_x = sorted(upbound_1.keys())  
opt_y = [upbound_1[k] for k in opt_x]

def get_closest_key(d, target, tol=0):
    return min(d.keys(), key=lambda x: abs(x - target) if abs(x - target) < tol else float('inf'))

opt_z=[]
opt_z_low=[]
for k in opt_x:
    y_dict = Pro_stability_1[k]        # Inner dictionary
    param_val = upbound_1[k]           # Float parameter
    closest_key = get_closest_key(y_dict, param_val)
    opt_z.append(y_dict[closest_key])

# Plotting the 3D surface
fig = plt.figure(figsize=(9.5, 6))


ax = fig.add_subplot(111, projection='3d')

# Use a color map, e.g., 'plasma' (purple-yellow)
surf = ax.plot_surface(X, Y, Z, cmap='GnBu_r', edgecolor='none', alpha=0.8, vmin=0.6, vmax=1.0) # plasma


# Plot optimal line
ax.plot(opt_x, list(upbound_1.values()), opt_z, color='#4682B4', linewidth=1.5, label=r'Stability probability with $\xi=\frac{\epsilon_e}{\epsilon_e(N_e-1)+\epsilon_fN_f}$', zorder=10)


# Add a legend to the plot
ax.legend(ncol=2, loc='upper right', fontsize=14.5, bbox_to_anchor=(0.85, 1.0))

# Axis labels and styling
ax.set_xlabel(r'$N_e$', fontsize=14.5, labelpad=10)
ax.set_ylabel(r'$\xi$', fontsize=14.5, labelpad=10)
ax.set_zlabel("")  # Hide default label

# Manually place and rotate z-label using ax.text()
ax.text(x=-1.6, y=0.175, z=1.09,
        s=r'$\mathbb{P}_{\mathrm{core}}(x(\xi))$',
        fontsize=14.5, rotation=90, rotation_mode='anchor')


# Set z-axis limits for better scaling
ax.set_zlim(0.43, 1.0)
#ax.set_zlim(0.401, 1.0)# Case2-4

ax.set_xlim(0.0, 14.3)
ax.set_ylim(0.01, 0.16)


# Set custom view angle for clarity
ax.view_init(elev=20, azim=210) #Case1
#ax.view_init(elev=20, azim=215) #Case2-4

ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='z', labelsize=11)

# Set x-axis ticks from 1 to 14
ax.set_xticks(np.arange(1, 15))  # Set x-axis ticks from 1 to 14


# Add color bar
cbar = fig.colorbar(surf, ax=ax, shrink=0.65, aspect=13, pad=0.01)
cbar.ax.tick_params(labelsize=11) 

ax.grid(True, color='gray', linestyle='--', linewidth=0.3)

plt.tight_layout()
plt.savefig("Stability_comparison_xi_Case1.png", dpi=1000, bbox_inches='tight')
plt.show()