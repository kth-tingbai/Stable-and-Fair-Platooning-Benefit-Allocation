import numpy as np
import itertools
import copy
from tqdm import tqdm

# ── Parameters ────────────────────────────────────────────────────────────────
epsilon_f = 0.725
epsilon_e = 0.048
tau       = 300
param     = np.linspace(0.005, 0.99, 500)

# N_e = 2,...,14; N_f = 15 - N_e (total N = 15)
Comparison_s = {i: [i+2, 13-i] for i in range(13)}

Payoff_Shapley = {i: {} for i in range(13)}
Payoff_our     = {i: {} for i in range(13)}
Payoff_bound   = {i: {} for i in range(13)}
D_r            = {i: {} for i in range(13)}
bound_min      = {i: {} for i in range(13)}

# ── Main computation ──────────────────────────────────────────────────────────
for i in tqdm(Comparison_s.keys(), ncols=80):
    N_e = Comparison_s[i][0]
    N_f = Comparison_s[i][1]
    N   = N_e + N_f
    N_set_e = {v: {} for v in range(N_e)}
    N_set_f = {v: {} for v in range(N_e, N)}
    N_set   = {**N_set_e, **N_set_f}

    xi_up = epsilon_e / (epsilon_e*(N_e-1) + epsilon_f*N_f)

    for v in N_set_f: N_set[v] = (1 - 1/N) * epsilon_f * tau
    for v in N_set_e: N_set[v] = ((1 - 1/N_e)*epsilon_e + (N_f*epsilon_f)/(N*N_e)) * tau
    Payoff_Shapley[i] = N_set.copy()

    for j in param:
        V_total      = (epsilon_f*N_f + epsilon_e*(N_e-1)) * tau
        N_set_payoff = copy.deepcopy(N_set)
        N_set_min    = copy.deepcopy(N_set)
        leader       = list(N_set_e.keys())[0]

        for v in N_set:
            if v == leader:
                N_set_payoff[v] = j * V_total
                N_set_min[v]    = xi_up * V_total
            elif v in N_set_e:
                N_set_payoff[v] = (1 - j)     * epsilon_e * tau
                N_set_min[v]    = (1 - xi_up) * epsilon_e * tau
            else:
                N_set_payoff[v] = (1 - j) * epsilon_f * tau
                N_set_min[v]    = (1 - j) * epsilon_f * tau

        Payoff_our[i][j]       = N_set_payoff
        Payoff_bound[i][xi_up] = N_set_min

        D_r[i][j]           = [abs(Payoff_Shapley[i][v] - N_set_payoff[v]) / Payoff_Shapley[i][v]
                                for v in N_set]
        bound_min[i][xi_up] = [abs(Payoff_Shapley[i][v] - N_set_min[v]) / Payoff_Shapley[i][v]
                                for v in N_set]

# ── Save ──────────────────────────────────────────────────────────────────────
with open('Mean_relative_deviation', 'w') as f:
    f.write(str(D_r))

with open('Minimum_D', 'w') as f:
    f.write(str(bound_min))

print("Saved: Mean_relative_deviation, Minimum_D")