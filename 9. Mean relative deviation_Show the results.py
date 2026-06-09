import numpy as np
import matplotlib.pyplot as plt

# ── Load data ─────────────────────────────────────────────────────────────────
with open('Mean_relative_deviation', 'r') as f:
    D_r_dict = eval(f.read())

with open('Minimum_D', 'r') as f:
    bound_min_dict = eval(f.read())

# N_e = 2,...,14
Comparison_s = {i: [i+2, 13-i] for i in range(13)}

# ── Average ───────────────────────────────────────────────────────────────────
D_r_avg  = {}
bmin_avg = {}

for i in D_r_dict.keys():
    D_r_avg[i]  = {j: sum(D_r_dict[i][j]) / len(D_r_dict[i][j])
                   for j in D_r_dict[i]}
    bmin_avg[i] = {s: sum(bound_min_dict[i][s]) / len(bound_min_dict[i][s])
                   for s in bound_min_dict[i]}

# ── Build meshgrid ────────────────────────────────────────────────────────────
x_ne   = [Comparison_s[i][0] for i in sorted(D_r_avg)]   # [2,...,14]
y_keys = sorted(next(iter(D_r_avg.values())).keys())

X, Y = np.meshgrid(x_ne, y_keys)
Z    = np.zeros_like(X, dtype=float)
for col, i in enumerate(sorted(D_r_avg)):
    for row, y in enumerate(y_keys):
        Z[row, col] = D_r_avg[i].get(y, 0)

opt_x = [Comparison_s[i][0]            for i in sorted(bmin_avg)]
opt_y = [list(bmin_avg[i].keys())[0]   for i in sorted(bmin_avg)]
opt_z = [list(bmin_avg[i].values())[0] for i in sorted(bmin_avg)]

# ── Plot ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(9.5, 5.5))
ax  = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(X, Y, Z, cmap='Blues', edgecolor='none', alpha=0.75, vmin=0, vmax=3.5)
ax.plot(opt_x, opt_y, opt_z, color='#756bb1', linewidth=1.5,
        label=r'$\Delta_{\phi}(x(\xi^{*}))$ with $x(\xi^{*})$ ensuring stability', zorder=10)

ax.legend(ncol=2, loc='upper right', fontsize=13.5, bbox_to_anchor=(0.87, 1))
ax.set_xlabel(r'$N_e$', fontsize=14, labelpad=10)
ax.set_ylabel(r'$\xi$',  fontsize=14, labelpad=10)
ax.set_zlabel("")
ax.text(x=-1.6, y=1.07, z=6.6,
        s=r'$\Delta_{\phi}({x(\xi)})$',
        fontsize=14.5, rotation=90, rotation_mode='anchor')

ax.set_zlim(0, 5.8)
ax.set_xlim(1.5, 14.5)
ax.set_ylim(0.005, 0.995)
ax.view_init(elev=15, azim=210)
ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='z', labelsize=11)
ax.set_xticks(np.arange(2, 15, 2))
ax.set_yticks(np.arange(0, 1.0, 0.1))

cbar = fig.colorbar(surf, ax=ax, shrink=0.65, aspect=13, pad=0.01)
cbar.ax.tick_params(labelsize=11)
ax.grid(True, color='gray', linestyle='--', linewidth=0.4)

plt.tight_layout()
plt.savefig("Relative_deviation.png", dpi=500, bbox_inches='tight', pad_inches=0.5)
plt.show()