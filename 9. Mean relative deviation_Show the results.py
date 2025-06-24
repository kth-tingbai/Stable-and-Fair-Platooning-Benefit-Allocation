# -*- coding: utf-8 -*-
"""
Created on Fri May 16 13:14:05 2025

The following code is used to show the 3-D plot of the mean relative deviation, to verify Theorem 3

@author: tingbai
"""

f=open('Mean_relative_deviation','r')
a=f.read()
D_r_dict=eval(a) 
f.close()

f=open('Minimum_D','r')
a=f.read()
bound_min_dict=eval(a) 
f.close()


D_r={}
bound_min={}

for i in D_r_dict.keys():
    D_r[i]={}
    bound_min[i]={}
    for s in bound_min_dict[i].keys():
        bound_min[i][s]=sum(bound_min_dict[i][s])/len(bound_min_dict[i][s])
    
    for j in D_r_dict[i].keys():
        D_r[i][j]=sum(D_r_dict[i][j])/len(D_r_dict[i][j])
        


import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

# Sort keys to ensure proper plotting order
x_keys = sorted(D_r.keys())  # Number of EVs 
y_keys = sorted(next(iter(D_r.values())).keys())  # Parameter values

# Create a meshgrid
X, Y = np.meshgrid(x_keys, y_keys)

# Initialize Z-values (stability probabilities)
Z = np.zeros_like(X, dtype=float)

# Populate Z from the dictionary
for i, x in enumerate(x_keys):           # x: number of EVs
    for j, y in enumerate(y_keys):       # y: parameter
        Z[j, i] = D_r[x].get(y, 0)      # Use .get() to avoid missing key errors
        
opt_x = sorted(bound_min.keys())  # 0 to 13
opt_y = []
opt_z = []
for k in opt_x:
    for y in bound_min[k].keys():
        opt_y.append(y)
    
for i in range(14):
    j=list(bound_min[i].keys())[0]
    opt_z.append(bound_min[i][j])


def get_closest_key(d, target, tol=0):
    return min(d.keys(), key=lambda x: abs(x - target) if abs(x - target) < tol else float('inf'))



# Plotting the 3D surface
fig = plt.figure(figsize=(9.5, 5.5))


ax = fig.add_subplot(111, projection='3d')

# Use a color map, e.g., 'plasma' (purple-yellow)
surf = ax.plot_surface(X, Y, Z, cmap='Blues', edgecolor='none', alpha=0.75, vmin=0, vmax=3.5) #cividis


# Plot optimal line
ax.plot(opt_x, opt_y, opt_z, color='#756bb1', linewidth=1.5, label=r'$\Delta_{\phi}(x(\xi^{*}))$ with $x(\xi^{*})$ ensuring stability', zorder=10)


# Add a legend to the plot
ax.legend(ncol=2, loc='upper right', fontsize=13.5, bbox_to_anchor=(0.87, 1))
#ax.legend(loc=2,fontsize=16)

# Axis labels and styling
ax.set_xlabel(r'$N_e$', fontsize=14, labelpad=10)
ax.set_ylabel(r'$\xi$', fontsize=14, labelpad=10)
ax.set_zlabel("")  # Hide default label

# Manually place and rotate z-label using ax.text()
ax.text(x=-1.6, y=1.07, z=6.6,
        s=r'$\Delta_{\phi}({x(\xi)})$',
        fontsize=14.5, rotation=90, rotation_mode='anchor')


# Set z-axis limits for better scaling
ax.set_zlim(0, 5.8)
ax.set_xlim(0.05, 14.5)
ax.set_ylim(0.005, 0.995)


# Set custom view angle for clarity
ax.view_init(elev=15, azim=210)

ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='z', labelsize=11)

# Set x-axis ticks from 1 to 14
ax.set_xticks(np.arange(2, 15, 2))  # Set x-axis ticks from 1 to 14
ax.set_yticks(np.arange(0, 1.0, 0.1))  # Set x-axis ticks from 1 to 14


# Add color bar
cbar = fig.colorbar(surf, ax=ax, shrink=0.65, aspect=13, pad=0.01)
cbar.ax.tick_params(labelsize=11) 

ax.grid(True, color='gray', linestyle='--', linewidth=0.4)

plt.tight_layout()
plt.savefig("Relative_deviation.png", dpi=500, bbox_inches='tight')
plt.show()