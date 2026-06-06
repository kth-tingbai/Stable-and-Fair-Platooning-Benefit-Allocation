import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# given parameters
eps_e = 0.048
eps_f = 0.07
N = 12
r = 0.63

Nf_vals = np.arange(1, 11)   # 1,2,...,10
thresholds = Nf_vals / N
feasible = r >= thresholds

plt.figure(figsize=(8, 6))

plt.plot(Nf_vals, thresholds, color='tab:orange', linestyle='--', linewidth=2.2,
         label='Threshold from Theorem 2')
plt.axhline(y=r, color='tab:blue', linestyle='--', linewidth=2.0,
            label=rf'$\epsilon_e/\epsilon_f = {r:.2f}$')

for nf, thr, ok in zip(Nf_vals, thresholds, feasible):
    plt.scatter(nf, r, color='#2a9d8f' if ok else '#d62728', s=70, zorder=3)

plt.fill_between(Nf_vals, thresholds, r, where=(r >= thresholds),
                 color='#2a9d8f', alpha=0.15)
plt.fill_between(Nf_vals, thresholds, r, where=(r < thresholds),
                 color='#d62728', alpha=0.15)

for nf, thr, ok in zip(Nf_vals, thresholds, feasible):
    label = "F" if ok else "I"
    plt.text(nf, r + 0.045, label, ha='center', va='bottom', fontsize=15)  # 稍微远些

plt.xticks(Nf_vals, fontsize=16)
plt.xlim(0.7, 10.3)
plt.ylim(0, 1.02)
plt.gca().tick_params(axis='y', labelsize=16)

plt.xlabel(r'$N_f$ (with $N=12$)', fontsize=16)
plt.ylabel(r'$\epsilon_e/\epsilon_f$', fontsize=16)
plt.grid(alpha=0.25)

extra_handles = [
    Patch(facecolor='#2a9d8f', alpha=0.3, edgecolor='none', label='Feasible region'),
    Patch(facecolor='#d62728', alpha=0.3, edgecolor='none', label='Infeasible region'),
]
plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + extra_handles,
           labels=plt.gca().get_legend_handles_labels()[1] + ['Feasible region', 'Infeasible region'],
           frameon=True, fontsize=14)

plt.tight_layout()
plt.savefig("theorem2_feasible_infeasible_N12.png", dpi=500, bbox_inches="tight")
plt.show()