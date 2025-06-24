# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:46:51 2025

The following code is used to show the 3-D plot of stability probability in homogeneous truck platooning

@author: tingbai
"""
f=open('Probability_homogeneous','r')
a=f.read()
Pro_stability_save=eval(a) 
f.close()

f=open('Upbound_homogeneous','r')
a=f.read()
upbound_1=eval(a) 
f.close()


epsilon_f=0.07
Pro_stability_1=Pro_stability_save[(epsilon_f)]

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
fig = plt.figure(figsize=(9, 6))



ax = fig.add_subplot(111, projection='3d')

# Use a color map, e.g., 'plasma' (purple-yellow)
surf = ax.plot_surface(X, Y, Z, cmap='pink', edgecolor='none', alpha=0.8, vmin=0.5, vmax=1.0) # GnBu_r


# Plot optimal line
ax.plot(opt_x, list(upbound_1.values()), opt_z, color='#4682B4', linewidth=1.5, label=r'Stability probability with $\xi=\frac{1}{N-1}$', zorder=10)
##ax.plot(opt_x, opt_y_low, opt_z_low, color='green', linewidth=1.5, label=r'Lower bound of $\xi$ for fairness', zorder=10)
#ax.scatter(opt_x, opt_y, opt_z, color='blue', s=30, label='Optimal point', zorder=30)

# Add a legend to the plot
ax.legend(ncol=2, loc='upper right', fontsize=14, bbox_to_anchor=(0.68, 1.0))
#ax.legend(loc=2,fontsize=16)

# Axis labels and styling
ax.set_xlabel(r'$N$', fontsize=14.5, labelpad=10)
ax.set_ylabel(r'$\xi$', fontsize=14.5, labelpad=10)
ax.set_zlabel("")  # Hide default label

# Manually place and rotate z-label using ax.text()
ax.text(x=-1.6, y=1.17, z=1.14,
        s=r'$\mathbb{P}_{\mathrm{core}}(x(\xi))$',
        fontsize=14.5, rotation=90, rotation_mode='anchor')

# Set z-axis limits for better scaling
ax.set_zlim(0.4, 1.0)
ax.set_xlim(1.2, 15.2)
ax.set_ylim(0.0, 1.17)

# Set custom view angle for clarity
ax.view_init(elev=25, azim=220)

ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='z', labelsize=11)

# Set x-axis ticks from 1 to 14
ax.set_xticks(np.arange(2, 16))  # Set x-axis ticks from 2 to 15
plt.yticks(np.arange(0.0, 1.105, 0.1))

# Add color bar
cbar = fig.colorbar(surf, ax=ax, shrink=0.65, aspect=13, pad=0.01)
cbar.ax.tick_params(labelsize=11) 

ax.grid(True, color='gray', linestyle='--', linewidth=0.3)

plt.tight_layout()
plt.savefig("Stability_homogeneous.png", dpi=1000, bbox_inches='tight')
plt.show()