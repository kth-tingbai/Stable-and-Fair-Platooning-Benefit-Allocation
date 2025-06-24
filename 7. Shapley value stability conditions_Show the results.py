# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:56:57 2025

The following code is used to show the 3-D plot of the stability probability for Shapley value-based payoff allocation

@author: tingbai
"""
f=open('Stability_Probability_Shapley_value','r')
a=f.read()
Pro_stability_Shapley=eval(a) 
f.close()

f=open('Probability_Stability_Shapley_value','r') 
a=f.read()
P_bound_stability=eval(a)
f.close()

f=open('Stability_bound_Shapley_value','r') 
a=f.read()
bound_stability=eval(a)
f.close()


import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

# Sort keys to ensure proper plotting order
x_keys = sorted(Pro_stability_Shapley.keys())  # Number of EVs 
y_keys = sorted(next(iter(Pro_stability_Shapley.values())).keys())  # Parameter values

# Create a meshgrid
X, Y = np.meshgrid(x_keys, y_keys)

# Initialize Z-values (stability probabilities)
Z = np.zeros_like(X, dtype=float)

# Populate Z from the dictionary
for i, x in enumerate(x_keys):           # x: number of EVs
    for j, y in enumerate(y_keys):       # y: parameter
        Z[j, i] = Pro_stability_Shapley[x].get(y, 0)      # Use .get() to avoid missing key errors
        

# Plotting the 3D surface
fig = plt.figure(figsize=(8,6))

ax = fig.add_subplot(111, projection='3d')

# Use a color map, e.g., 'plasma' (purple-yellow)
surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none', alpha=0.7, vmin=0.5, vmax=1.0) #'plasma'
    
P_bound_stability_use={}
for i in range(14):
    P_bound_stability_use[i]=P_bound_stability[i][bound_stability[i]]

# Plot optimal line
ax.plot(list(range(14)), list(bound_stability.values()), list(P_bound_stability_use.values()), color='#756bb1', linewidth=1.5, label=r'Stability probability with $\frac{\epsilon_e}{\epsilon_f}=\frac{N_f}{N}$', zorder=10)


# Add a legend to the plot
ax.legend(ncol=2, loc='upper left', fontsize=14, bbox_to_anchor=(0.025, 1))
#ax.legend(loc=2,fontsize=16)

# Axis labels and styling
ax.set_xlabel(r'$N_e$', fontsize=14.5, labelpad=10)
ax.set_ylabel(r'$\epsilon_e/\epsilon_f$', fontsize=14.5, labelpad=10)
ax.set_zlabel("")  # Hide default label

# Manually place and rotate z-label using ax.text()
ax.text(x=-1.6, y=1.08, z=1.1,
        s=r'$\mathbb{P}_{\mathrm{core}}(\phi)$',
        fontsize=15.5, rotation=90, rotation_mode='anchor')

# Set z-axis limits for better scaling
ax.set_zlim(0.35, 1.02)
ax.set_xlim(0.05, 14.8)
ax.set_ylim(0.05, 0.995)



# Set custom view angle for clarity
ax.view_init(elev=10, azim=225)

ax.tick_params(axis='x', labelsize=11.5)
ax.tick_params(axis='y', labelsize=11.5)
ax.tick_params(axis='z', labelsize=11.5)

# Set x-axis ticks from 1 to 13, corresponding to 13 cases
ax.set_xticks(np.arange(1, 15))  # Set x-axis ticks from 1 to 14
ax.set_yticks(np.arange(0.1, 1, 0.1))  # Set x-axis ticks from 1 to 14


# Add color bar
cbar = fig.colorbar(surf, ax=ax, shrink=0.65, aspect=13, pad=0.01)
cbar.ax.tick_params(labelsize=11.5) 

ax.grid(True, color='gray', linestyle='--', linewidth=0.3)

plt.tight_layout()
plt.savefig("Stability_Shapley_value.png", dpi=1000, bbox_inches='tight')
plt.show()