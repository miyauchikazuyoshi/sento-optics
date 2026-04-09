"""
Phase 1: δ_sp + N_d two-variable regression for n_ws prediction.

Question: Can we predict Miedema's n_ws by adding d-electron count
to δ? If r improves from 0.26 to >0.7, d-electron screening is
the missing factor.
"""

import numpy as np
from scipy import stats
import json

# === Data ===
# de Boer 1988 n_ws (d.u.)
NWS = {
    'Li': 2.85, 'Na': 1.65, 'K': 0.95, 'Be': 7.55, 'Mg': 3.55,
    'Ca': 2.55, 'Al': 5.55, 'Si': 6.75, 'Ga': 5.15, 'Cu': 5.55,
    'Zn': 4.05, 'Fe': 5.55, 'Ni': 5.55, 'Ag': 4.35, 'Ti': 4.25,
}

# delta_val from test7_extended
DELTA_VAL = {
    'Li': 0.186, 'Be': 0.231, 'Na': 0.134, 'Mg': 0.091, 'Al': 0.121,
    'Si': 0.142, 'K': 0.046, 'Ca': 0.058, 'Ti': 0.063, 'Fe': 0.069,
    'Cu': 0.057, 'Zn': 0.052, 'Ga': 0.061, 'Ni': 0.082, 'Ag': 0.051,
}

# Number of d electrons per atom
N_D = {
    'Li': 0, 'Na': 0, 'K': 0, 'Be': 0, 'Mg': 0,
    'Ca': 0, 'Al': 0, 'Si': 0,
    'Ti': 2, 'Fe': 6, 'Ni': 8, 'Cu': 10, 'Zn': 10, 'Ga': 10, 'Ag': 10,
}

# Atomic number (as alternative regressor)
Z = {
    'Li': 3, 'Be': 4, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14,
    'K': 19, 'Ca': 20, 'Ti': 22, 'Fe': 26, 'Ni': 28, 'Cu': 29,
    'Zn': 30, 'Ga': 31, 'Ag': 47,
}

# Keene 1993 gamma at melting
GAMMA = {
    'Li': 398, 'Be': 1145, 'Na': 191, 'Mg': 559, 'Al': 1050,
    'Si': 865, 'K': 101, 'Ca': 361, 'Ti': 1650, 'Fe': 1872,
    'Cu': 1285, 'Zn': 782, 'Ga': 718, 'Ni': 1778, 'Ag': 903,
}

elems = sorted(DELTA_VAL.keys())
n = len(elems)

dv = np.array([DELTA_VAL[e] for e in elems])
nd = np.array([N_D[e] for e in elems])
z = np.array([Z[e] for e in elems])
nws = np.array([NWS[e] for e in elems])
nws13 = nws**(1/3)
gamma = np.array([GAMMA[e] for e in elems])

print("=" * 60)
print("Phase 1: Two-variable regression for n_ws prediction")
print("=" * 60)

# === 1-variable baselines ===
print("\n--- Baseline: 1-variable models ---")
r_dv, p_dv = stats.pearsonr(dv, nws13)
r_nd, p_nd = stats.pearsonr(nd, nws13)
r_z, p_z = stats.pearsonr(z, nws13)
r_g, p_g = stats.pearsonr(gamma, nws13)

print(f"  δ_val vs n_ws^{{1/3}}:     r = {r_dv:.3f}, p = {p_dv:.4f}")
print(f"  N_d vs n_ws^{{1/3}}:       r = {r_nd:.3f}, p = {p_nd:.4f}")
print(f"  Z vs n_ws^{{1/3}}:         r = {r_z:.3f}, p = {r_z:.4f}")
print(f"  γ vs n_ws^{{1/3}}:         r = {r_g:.3f}, p = {p_g:.4f}")

# === 2-variable: δ_val + N_d ===
print("\n--- Model 1: n_ws^{1/3} ~ δ_val + N_d ---")
X = np.column_stack([dv, nd, np.ones(n)])
beta, residuals, rank, sv = np.linalg.lstsq(X, nws13, rcond=None)
nws13_pred = X @ beta
ss_res = np.sum((nws13 - nws13_pred)**2)
ss_tot = np.sum((nws13 - np.mean(nws13))**2)
r2 = 1 - ss_res / ss_tot
r_adj = 1 - (1 - r2) * (n - 1) / (n - 3)
print(f"  β(δ_val) = {beta[0]:.3f}")
print(f"  β(N_d)   = {beta[1]:.4f}")
print(f"  intercept = {beta[2]:.3f}")
print(f"  R² = {r2:.3f}, R²_adj = {r_adj:.3f}")

# === 2-variable: δ_val + Z ===
print("\n--- Model 2: n_ws^{1/3} ~ δ_val + Z ---")
X2 = np.column_stack([dv, z, np.ones(n)])
beta2, _, _, _ = np.linalg.lstsq(X2, nws13, rcond=None)
nws13_pred2 = X2 @ beta2
ss_res2 = np.sum((nws13 - nws13_pred2)**2)
r2_2 = 1 - ss_res2 / ss_tot
r_adj2 = 1 - (1 - r2_2) * (n - 1) / (n - 3)
print(f"  β(δ_val) = {beta2[0]:.3f}")
print(f"  β(Z)     = {beta2[1]:.4f}")
print(f"  intercept = {beta2[2]:.3f}")
print(f"  R² = {r2_2:.3f}, R²_adj = {r_adj2:.3f}")

# === 2-variable: δ_val + γ ===
print("\n--- Model 3: n_ws^{1/3} ~ δ_val + γ ---")
X3 = np.column_stack([dv, gamma, np.ones(n)])
beta3, _, _, _ = np.linalg.lstsq(X3, nws13, rcond=None)
nws13_pred3 = X3 @ beta3
ss_res3 = np.sum((nws13 - nws13_pred3)**2)
r2_3 = 1 - ss_res3 / ss_tot
r_adj3 = 1 - (1 - r2_3) * (n - 1) / (n - 3)
print(f"  β(δ_val) = {beta3[0]:.3f}")
print(f"  β(γ)     = {beta3[1]:.6f}")
print(f"  intercept = {beta3[2]:.3f}")
print(f"  R² = {r2_3:.3f}, R²_adj = {r_adj3:.3f}")

# === 3-variable: δ_val + N_d + γ ===
print("\n--- Model 4: n_ws^{1/3} ~ δ_val + N_d + γ ---")
X4 = np.column_stack([dv, nd, gamma, np.ones(n)])
beta4, _, _, _ = np.linalg.lstsq(X4, nws13, rcond=None)
nws13_pred4 = X4 @ beta4
ss_res4 = np.sum((nws13 - nws13_pred4)**2)
r2_4 = 1 - ss_res4 / ss_tot
r_adj4 = 1 - (1 - r2_4) * (n - 1) / (n - 4)
print(f"  β(δ_val) = {beta4[0]:.3f}")
print(f"  β(N_d)   = {beta4[1]:.4f}")
print(f"  β(γ)     = {beta4[2]:.6f}")
print(f"  intercept = {beta4[3]:.3f}")
print(f"  R² = {r2_4:.3f}, R²_adj = {r_adj4:.3f}")

# === Can N_d alone predict n_ws? ===
print("\n--- Control: N_d alone vs n_ws^{1/3} ---")
r_nd_only, p_nd_only = stats.pearsonr(nd, nws13)
print(f"  r = {r_nd_only:.3f}, p = {p_nd_only:.4f}")

# === Summary ===
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"{'Model':>30} {'R²':>6} {'R²_adj':>8} {'Improvement':>12}")
print("-" * 60)
print(f"{'δ_val only':>30} {r_dv**2:>6.3f} {'—':>8} {'baseline':>12}")
print(f"{'δ_val + N_d':>30} {r2:>6.3f} {r_adj:>8.3f} {'+{:.3f}'.format(r2 - r_dv**2):>12}")
print(f"{'δ_val + Z':>30} {r2_2:>6.3f} {r_adj2:>8.3f} {'+{:.3f}'.format(r2_2 - r_dv**2):>12}")
print(f"{'δ_val + γ':>30} {r2_3:>6.3f} {r_adj3:>8.3f} {'+{:.3f}'.format(r2_3 - r_dv**2):>12}")
print(f"{'δ_val + N_d + γ':>30} {r2_4:>6.3f} {r_adj4:>8.3f} {'+{:.3f}'.format(r2_4 - r_dv**2):>12}")
print(f"{'N_d only':>30} {r_nd**2:>6.3f} {'—':>8} {'(control)':>12}")
print(f"{'γ only':>30} {r_g**2:>6.3f} {'—':>8} {'(control)':>12}")

print("\n--- Interpretation ---")
if r2 > 0.5:
    print("δ_val + N_d model R² > 0.5: d-electron screening is likely the missing factor.")
elif r2 > r_dv**2 + 0.1:
    print("δ_val + N_d improves notably but R² < 0.5: d-screening is a factor but not the only one.")
else:
    print("δ_val + N_d does not improve much: d-screening is NOT the main missing factor.")
