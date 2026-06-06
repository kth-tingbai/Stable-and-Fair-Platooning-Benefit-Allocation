import numpy as np
import matplotlib.pyplot as plt


def shapley_in_core(N, Nf, ratio):
    return ratio >= Nf / N


def shapley_values(N, Ne, Nf, eps_e, eps_f):
    phi_f = (1.0 - 1.0 / N) * eps_f
    phi_e = (1.0 - 1.0 / Ne) * eps_e + (Nf / (N * Ne)) * eps_f
    return phi_e, phi_f


def stable_allocation_xistar(N, Ne, Nf, eps_e, eps_f):
    vN = eps_e * (Ne - 1) + eps_f * Nf
    xi_star = eps_e / vN
    x_leader = xi_star * vN
    x_e = (1.0 - xi_star) * eps_e
    x_f = (1.0 - xi_star) * eps_f
    return x_leader, x_e, x_f


def mean_relative_deviation(N, Ne, Nf, eps_e, eps_f):
    phi_e, phi_f = shapley_values(N, Ne, Nf, eps_e, eps_f)
    x_leader, x_e, x_f = stable_allocation_xistar(N, Ne, Nf, eps_e, eps_f)

    terms = [abs((x_leader - phi_e) / phi_e)]
    for _ in range(Ne - 1):
        terms.append(abs((x_e - phi_e) / phi_e))
    for _ in range(Nf):
        terms.append(abs((x_f - phi_f) / phi_f))

    return float(np.mean(terms))


def generate_deviation_data(N=12, ratios=None):
    if ratios is None:
        ratios = np.arange(0.1, 1.0, 0.1)

    # keep only N_e > 1, i.e., N_f = 1,...,N-2
    Nf_vals = np.arange(1, N - 1)   # for N=12: 1,...,10

    data = np.full((len(ratios), len(Nf_vals)), np.nan)

    for i, ratio in enumerate(ratios):
        eps_f = 1.0
        eps_e = ratio * eps_f
        for j, Nf in enumerate(Nf_vals):
            Ne = N - Nf
            if not shapley_in_core(N, Nf, ratio):
                data[i, j] = mean_relative_deviation(N, Ne, Nf, eps_e, eps_f)

    return ratios, Nf_vals, data


def find_worst_case(ratios, Nf_vals, data, N, tol=1e-12):
    max_dev = np.nanmax(data)
    worst_points = []

    for i, ratio in enumerate(ratios):
        for j, Nf in enumerate(Nf_vals):
            val = data[i, j]
            if not np.isnan(val) and abs(val - max_dev) <= tol:
                worst_points.append((ratio, int(Nf), int(N - Nf), val))

    return max_dev, worst_points


# ── First plot: rainbow line chart ──────────────────────────────────────────
def plot_deviation_curves_rainbow(
    N=12,
    ratios=None,
    save_path="mean_relative_deviation_rainbow_vs_Nf_over_N_N12.png"
):
    ratios, Nf_vals, data = generate_deviation_data(N=N, ratios=ratios)
    x_vals = Nf_vals / N

    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    cmap = plt.cm.rainbow(np.linspace(0, 1, len(ratios)))

    for i, ratio in enumerate(ratios):
        ax.plot(
            x_vals, data[i, :],
            marker='o', linewidth=2.2, markersize=5.5,
            color=cmap[i],
            label=rf'$\epsilon_e/\epsilon_f = {ratio:.1f}$'
        )

    ax.set_xlabel(r'$N_f/N$ (with $N=12$)', fontsize=18)
    ax.set_ylabel(r'$\Delta_\phi(x(\xi^*))$', fontsize=18)

    ax.set_xticks(x_vals)
    ax.set_xticklabels([rf'${nf}/{N}$' for nf in Nf_vals], fontsize=14)
    ax.set_xlim(x_vals[0] - 0.03, x_vals[-1] + 0.03)

    ax.yaxis.set_tick_params(labelsize=14, width=0.4, length=2.5)
    ax.xaxis.set_tick_params(labelsize=14, width=0.8, length=4)

    ax.set_ylim(0, 0.30)
    ax.grid(alpha=0.25)
    ax.legend(ncol=2, fontsize=13, frameon=True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=1000, bbox_inches="tight")
    plt.show()


# ── Second plot: heatmap ─────────────────────────────────────────────────────
def plot_worst_case_heatmap(
    N=12,
    ratios=None,
    save_path="mean_relative_deviation_heatmap_N12.png"
):
    ratios, Nf_vals, data = generate_deviation_data(N=N, ratios=ratios)
    masked_data = np.ma.masked_invalid(data)

    cmap = plt.cm.Blues.copy()
    cmap.set_bad(color="white")

    fig, ax = plt.subplots(figsize=(9.0, 6.2))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    im = ax.imshow(masked_data, origin='lower', aspect='auto', cmap=cmap)

    ax.set_xticks(np.arange(len(Nf_vals)))
    ax.set_xticklabels(Nf_vals, fontsize=14)
    ax.set_yticks(np.arange(len(ratios)))
    ax.set_yticklabels([f"{r:.1f}" for r in ratios], fontsize=14)

    ax.set_xlabel(r'$N_f$ (with $N=12$)', fontsize=18)
    ax.set_ylabel(r'$\epsilon_e/\epsilon_f$', fontsize=18)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(r'$\Delta_\phi(x(\xi^*))$', fontsize=16)
    cbar.ax.tick_params(labelsize=12)

    max_dev, _ = find_worst_case(ratios, Nf_vals, data, N)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if not np.isnan(val):
                if np.isclose(val, max_dev):
                    ax.add_patch(
                        plt.Rectangle(
                            (j - 0.5, i - 0.5), 1, 1,
                            fill=False, edgecolor='red', linewidth=2.5
                        )
                    )
                ax.text(
                    j, i, f"{val:.3f}",
                    ha='center', va='center',
                    color='white' if val > 0.18 else 'black',
                    fontsize=11
                )

    plt.tight_layout()
    plt.savefig(save_path, dpi=1000, bbox_inches="tight")
    plt.show()


def print_worst_case_summary(N=12, ratios=None):
    ratios, Nf_vals, data = generate_deviation_data(N=N, ratios=ratios)
    max_dev, worst_points = find_worst_case(ratios, Nf_vals, data, N)

    print("=" * 72)
    print(f"Worst-case mean relative deviation for N = {N} with N_e > 1")
    print(f"Maximum Delta_phi(x(xi*)) = {max_dev:.4f}")
    print("-" * 72)
    for ratio, Nf, Ne, val in worst_points:
        print(f"ratio = {ratio:.1f}, Nf = {Nf}, Ne = {Ne}, Delta_phi = {val:.4f}")
    print("=" * 72)


if __name__ == "__main__":
    ratios = np.arange(0.1, 1.0, 0.1)

    plot_deviation_curves_rainbow(
        N=12,
        ratios=ratios,
        save_path="mean_relative_deviation_rainbow_vs_Nf_over_N_N12.png"
    )

    plot_worst_case_heatmap(
        N=12,
        ratios=ratios,
        save_path="mean_relative_deviation_heatmap_N12.png"
    )

    print_worst_case_summary(N=12, ratios=ratios)