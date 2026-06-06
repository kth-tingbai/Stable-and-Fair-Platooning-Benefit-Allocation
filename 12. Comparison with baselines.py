import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

mpl.rcParams.update({
    "axes.linewidth": 0.9,
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
})

N = 12
ratios  = np.arange(0.1, 1.0, 0.1)
Nf_vals = np.arange(1, N - 1)      # Nf = 1,...,10
method_names = ["ES", "FO-ES", "TP-S", "LS-T", "ALC", "SV", "Proposed"]

# ── 公共函数 ──────────────────────────────────────────────────────────────────
def cv(NeS, NfS, e, f):
    if NeS + NfS == 0: return 0.0
    if NeS >= 1: return e * (NeS - 1) + f * NfS
    return f * (NfS - 1)

def gv(Nf, e, f, N=12): return cv(N - Nf, Nf, e, f)

def check_core(x, Nf, e, f, tol=1e-10, N=12):
    if abs(np.sum(x) - gv(Nf, e, f, N)) > tol: return False
    pt = ["e"] * (N - Nf) + ["f"] * Nf
    for mask in range(1, 1 << N):
        idx = [i for i in range(N) if (mask >> i) & 1]
        NeS = sum(1 for i in idx if pt[i] == "e")
        if np.sum(x[idx]) + tol < cv(NeS, len(idx) - NeS, e, f): return False
    return True

def alloc_SV(Nf, e, f, N=12):
    Ne = N - Nf; x = np.zeros(N)
    x[:Ne] = (1 - 1/Ne) * e + (Nf / (N * Ne)) * f
    x[Ne:] = (1 - 1/N) * f
    return x

def alloc_ES(Nf, e, f, N=12): return np.ones(N) * (gv(Nf, e, f, N) / N)

def alloc_FOES(Nf, e, f, N=12):
    x = np.zeros(N); x[1:] = gv(Nf, e, f, N) / (N - 1); return x

def alloc_TPS(Nf, e, f, N=12):
    Ne = N - Nf; x = np.zeros(N); x[1:Ne] = e; x[Ne:] = f; return x

def alloc_LST(Nf, e, f, N=12, tau=0.1):
    Ne = N - Nf; vN = gv(Nf, e, f, N); x = np.zeros(N)
    x[0] = tau * vN; x[1:Ne] = (1 - tau) * e; x[Ne:] = (1 - tau) * f; return x

def alloc_ALC(Nf, e, f, N=12, beta=0.1):
    Ne = N - Nf; vN = gv(Nf, e, f, N); x = np.zeros(N)
    fg = [e] * max(Ne - 1, 0) + [f] * Nf
    if not fg: return x
    x[0] = beta * max(fg); rem = vN - x[0]; d = sum(fg)
    x[1:Ne] = e / d * rem; x[Ne:] = f / d * rem; return x

def alloc_proposed(Nf, e, f, N=12):
    Ne = N - Nf; vN = gv(Nf, e, f, N); xi = e / vN; x = np.zeros(N)
    x[0] = xi * vN; x[1:Ne] = (1 - xi) * e; x[Ne:] = (1 - xi) * f; return x

def mrd(x, phi, tol=1e-12):
    ps = np.where(np.abs(phi) < tol, tol, phi)
    return np.mean(np.abs((x - phi) / ps))

alloc_fns = {
    "ES": alloc_ES, "FO-ES": alloc_FOES, "TP-S": alloc_TPS,
    "LS-T": alloc_LST, "ALC": alloc_ALC, "SV": alloc_SV, "Proposed": alloc_proposed
}

# ── 计算数据 ──────────────────────────────────────────────────────────────────
stability = {n: np.zeros((len(ratios), len(Nf_vals))) for n in method_names}
deviation  = {n: np.zeros((len(ratios), len(Nf_vals))) for n in method_names}

for i, r in enumerate(ratios):
    for j, Nf in enumerate(Nf_vals):
        phi = alloc_SV(Nf, r, 1.0, N)
        for name in method_names:
            x = alloc_fns[name](Nf, r, 1.0, N)
            stability[name][i, j] = 1 if check_core(x, Nf, r, 1.0, N=N) else 0
            deviation[name][i, j]  = mrd(x, phi)

avg_stability = [np.mean(stability[n]) * 100 for n in method_names]
avg_deviation  = [np.mean(deviation[n])       for n in method_names]
dev_data       = [deviation[n].flatten()       for n in method_names]

C_BASE     = "#5A8FC2"
C_PROPOSED = "#C0392B"
C_FILL_B   = "#D0E4F5"
C_FILL_P   = "#F5C6C0"

# ══════════════════════════════════════════════════════════════════════════════
# Figure 2: Violin
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8.0, 5.8))

parts = ax.violinplot(dev_data,
                      positions=np.arange(1, len(method_names) + 1),
                      showmedians=True, showextrema=True, widths=0.65)

for i, pc in enumerate(parts["bodies"]):
    is_prop = method_names[i] == "Proposed"
    pc.set_facecolor(C_FILL_P if is_prop else C_FILL_B)
    pc.set_edgecolor(C_PROPOSED if is_prop else C_BASE)
    pc.set_linewidth(1.5 if is_prop else 1.0)
    pc.set_alpha(0.85)

col_list = [C_PROPOSED if method_names[i] == "Proposed" else C_BASE
            for i in range(len(method_names))]
for part in ["cmedians", "cmins", "cmaxes", "cbars"]:
    parts[part].set_colors(col_list)
parts["cmedians"].set_linewidth(2.5)   # median 加粗
for part in ["cmins", "cmaxes", "cbars"]:
    parts[part].set_linewidth(1.0)

rng = np.random.default_rng(42)
for i, (data, name) in enumerate(zip(dev_data, method_names)):
    c = C_PROPOSED if name == "Proposed" else C_BASE
    ax.scatter(i + 1 + rng.uniform(-0.15, 0.15, len(data)),
               data, s=10, alpha=0.35, color=c, zorder=3)

for i, (data, name) in enumerate(zip(dev_data, method_names)):
    c = C_PROPOSED if name == "Proposed" else C_BASE
    ax.scatter(i + 1, np.mean(data), marker='D', s=55, color=c, zorder=5)

ax.set_xticks(range(1, len(method_names) + 1))
ax.set_xticklabels(method_names, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', pad=10)
ax.set_ylabel("Mean relative deviation", fontsize=18)
ax.set_xlabel("Allocation schemes", fontsize=18, labelpad=14)
ax.set_xlim(0.4, len(method_names) + 0.6)
ax.set_ylim(0, 1.8)
ax.set_yticks(np.arange(0, 1.9, 0.3))
ax.yaxis.grid(True, alpha=0.3, linewidth=0.7)
ax.set_axisbelow(True)
for sp in ax.spines.values():
    sp.set_visible(True); sp.set_linewidth(0.9)

legend_elements = [
    Line2D([0],[0], marker='D', color='w', markerfacecolor='#5A8FC2',
           markersize=8, label='Mean value'),
    Line2D([0],[0], color='#5A8FC2', linewidth=2.5, label='Median'),
    Line2D([0],[0], color='#5A8FC2', linewidth=1.0,
           marker='_', markersize=10, label='Min / Max'),
]
ax.legend(handles=legend_elements, fontsize=13, frameon=False, loc="upper right")

plt.tight_layout()
plt.savefig("fig2_violin.png", dpi=1000, bbox_inches="tight")
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 3: 双轴柱线图
# ══════════════════════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(9, 6.0))
ax2 = ax1.twinx()

xpos     = np.arange(len(method_names))
width    = 0.38
prop_idx = method_names.index("Proposed")
bar_colors = [C_PROPOSED if n == "Proposed" else C_BASE for n in method_names]
bar_edge   = [C_PROPOSED if n == "Proposed" else "#3A6FA0" for n in method_names]

ax1.add_patch(Rectangle(
    (prop_idx - 0.42, 0), 0.84, 100,
    color="#FDF0EF", zorder=0, alpha=0.8
))

ax1.bar(xpos, avg_stability, width,
        color=bar_colors, edgecolor=bar_edge,
        linewidth=1.0, alpha=0.88, zorder=3)

ax2.plot(xpos, avg_deviation, 'o--', color="#444444", linewidth=1.6, markersize=6, zorder=4)
ax2.plot(prop_idx, avg_deviation[prop_idx], 'o', color=C_PROPOSED, markersize=9, zorder=5)

for i, (val, name) in enumerate(zip(avg_stability, method_names)):
    c  = C_PROPOSED if name == "Proposed" else "#333"
    fw = "bold" if name == "Proposed" else "normal"
    ax1.text(i, val + 1.0, f"{val:.0f}%", ha="center", va="bottom",
             fontsize=11, color=c, fontweight=fw)

for i, (val, name) in enumerate(zip(avg_deviation, method_names)):
    c  = C_PROPOSED if name == "Proposed" else "#444"
    fw = "bold" if name == "Proposed" else "normal"
    if name == "Proposed":
        ax2.annotate(f"{val:.3f}",
                     xy=(i, val), xytext=(i + 0.38, val + 0.025),
                     fontsize=11, color=c, fontweight=fw,
                     arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
    else:
        ax2.text(i, val + 0.014, f"{val:.3f}", ha="center", va="bottom",
                 fontsize=11, color=c, fontweight=fw)

ax1.set_xticks(xpos)
ax1.set_xticklabels(method_names, fontsize=14)
ax1.tick_params(axis='x', pad=10)
ax1.set_xlabel("Allocation schemes", fontsize=18, labelpad=14)
ax1.set_ylim(0, 130)
ax1.set_yticks([0, 20, 40, 60, 80, 100])
ax1.set_ylabel("Ave. stability rate [%]", fontsize=18)
ax1.tick_params(axis='y', labelsize=14)

ax2.set_ylim(0, max(avg_deviation) * 1.65)
ax2.set_ylabel("Ave. mean relative deviation", fontsize=18)
ax2.tick_params(axis='y', labelsize=14)

ax1.yaxis.grid(True, alpha=0.25, linewidth=0.7, zorder=0)
ax1.set_axisbelow(True)
for sp in ax1.spines.values():
    sp.set_visible(True); sp.set_linewidth(0.9)
for sp in ax2.spines.values():
    sp.set_visible(True); sp.set_linewidth(0.9)

ax1.legend(handles=[
    Patch(facecolor=C_BASE, edgecolor="#3A6FA0", alpha=0.88, label="Ave. stability rate"),
    Line2D([0], [0], color="#444", linestyle='--', marker='o',
           markersize=6, label="Ave. mean relative deviation"),
], fontsize=13, frameon=True, edgecolor="#ccc", framealpha=0.9, loc="upper left")

plt.tight_layout()
plt.savefig("fig3_summary.png", dpi=1000, bbox_inches="tight")
plt.show()