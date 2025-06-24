# -*- coding: utf-8 -*-
"""
Created on Tue May 13 09:51:32 2025

Code used to compute the Shapley value-based payoff allocations proposed in Proposition 1

@author: tingbai
"""
import matplotlib.pyplot as plt
import numpy as np

epsilon_f=0.07
epsilon_e=0.048
tau=300

phi={}

for N_i in range(14):
    N=N_i+2# the number of trucks in the platoon
    phi[N]={} 
    phi_e={} # the Shapley value of ET
    phi_f={} # the Shapley value of FT
    for N_f_i in range(N):
        N_f=N_f_i+1
        N_e=N-N_f
        if N_e!=0:
            phi_e[N_f]=((1-1/N_e)*epsilon_e+(N_f*epsilon_f)/(N*N_e))*tau # the payoff of ET when the FPT is N_f
            phi_f[N_f]=(1-1/N)*epsilon_f*tau
    phi[N]['e']=phi_e
    phi[N]['f']=phi_f
        


import matplotlib.cm as cm

plt.figure(figsize=(12.5, 9.7))

# Sequential colormap: 'viridis'
num_trucks = list(range(2, 16))
cmap = cm.get_cmap('coolwarm', len(num_trucks))


for i, total_trucks in enumerate(num_trucks):
    color = cmap(i)

    # ET payoff
    x_et = list(phi[total_trucks]['e'].keys())
    y_et = list(phi[total_trucks]['e'].values())
    plt.plot(x_et, y_et, label=f"ET (N={total_trucks})", linestyle='-', marker='s', markersize=7, color=color)

    # FPT payoff
    x_fpt = list(phi[total_trucks]['f'].keys())
    y_fpt = list(phi[total_trucks]['f'].values())
    plt.plot(x_fpt, y_fpt, label=f"FPT (N={total_trucks})", linestyle='--', marker='^', markersize=9, color=color)

# Axis labels and ticks
plt.xlabel(r"$N_f$", fontsize=24)
plt.ylabel(r"Payoff $\phi_i$ [Euro]", fontsize=24)
plt.xticks(fontsize=21)
plt.yticks(fontsize=21)
plt.grid(True)

plt.xlim(0.95, 14.05)
plt.ylim(9.5,20.5)
plt.xticks(np.arange(1, 15, step=1))

# Legend
handles, labels = plt.gca().get_legend_handles_labels()
et = [(h, l) for h, l in zip(handles, labels) if 'ET' in l]
fpt = [(h, l) for h, l in zip(handles, labels) if 'FPT' in l]
sorted_handles, sorted_labels = zip(*(et + fpt))

# Legend
handles, labels = plt.gca().get_legend_handles_labels()
et = [(h, l) for h, l in zip(handles, labels) if 'ET' in l]
fpt = [(h, l) for h, l in zip(handles, labels) if 'FPT' in l]
sorted_handles, sorted_labels = zip(*(et + fpt))

plt.legend(sorted_handles, sorted_labels,
           ncol=4,  # Adjust number of columns as needed
           fontsize=18.5,
           loc='upper center',
           bbox_to_anchor=(0.493, -0.11))  # Move legend below

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)  # Add space at the bottom for the legend
plt.savefig("Shapley_value_based_payoff.png", dpi=500, bbox_inches='tight')
plt.show()

