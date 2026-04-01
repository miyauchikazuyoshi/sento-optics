#!/usr/bin/env python3
"""
Three-factor correction test for Group 14 elements.

Problem: Omega/WF ordering (C < Ge < Si) does not match n ordering (C < Si < Ge).
Hypothesis: n^2 - 1 ∝ delta_elec × alpha_atom / E_g^2

This script tests whether the three-factor composite delta_eff
recovers the correct refractive index ordering.
"""

import numpy as np

# === Wannier spread data (this work) ===
data = {
    "C (diamond)": {
        "period": 2,
        "omega_per_wf": 0.954,   # Ang^2, from Wannier90
        "E_g": 5.47,             # eV, experimental band gap
        "n_exp": 2.417,          # experimental refractive index
        "alpha_atom": 1.76,      # Ang^3, atomic polarizability (lit.)
        "d_screening": False,
    },
    "Si": {
        "period": 3,
        "omega_per_wf": 3.049,
        "E_g": 1.12,
        "n_exp": 3.44,
        "alpha_atom": 5.38,
        "d_screening": False,
    },
    "Ge": {
        "period": 4,
        "omega_per_wf": 2.275,
        "E_g": 0.661,
        "n_exp": 4.00,
        "alpha_atom": 6.07,
        "d_screening": True,     # 3d10 screens sp3
    },
}

print("=" * 72)
print("Three-Factor Correction: delta_eff = Omega/WF × alpha / E_g^2")
print("=" * 72)

# === Table 1: Raw data ===
print("\n--- Raw Data ---")
print(f"{'Element':<14} {'Period':>6} {'Ω/WF':>8} {'E_g':>6} {'α_atom':>7} {'n_exp':>6} {'n²-1':>7}")
print("-" * 60)
for name, d in data.items():
    n2m1 = d["n_exp"]**2 - 1
    print(f"{name:<14} {d['period']:>6} {d['omega_per_wf']:>8.3f} {d['E_g']:>6.3f} {d['alpha_atom']:>7.2f} {d['n_exp']:>6.3f} {n2m1:>7.2f}")

# === Table 2: Three-factor composite ===
print("\n--- Three-Factor Composite ---")
print(f"{'Element':<14} {'δ_elec':>8} {'α/E_g²':>10} {'δ_eff':>10} {'n²-1':>7} {'ratio':>8}")
print("-" * 62)

delta_effs = {}
for name, d in data.items():
    delta_elec = d["omega_per_wf"]
    alpha_over_eg2 = d["alpha_atom"] / d["E_g"]**2
    delta_eff = delta_elec * alpha_over_eg2
    n2m1 = d["n_exp"]**2 - 1
    delta_effs[name] = delta_eff
    print(f"{name:<14} {delta_elec:>8.3f} {alpha_over_eg2:>10.3f} {delta_eff:>10.3f} {n2m1:>7.2f} {n2m1/delta_eff:>8.2f}")

# === Ordering check ===
print("\n--- Ordering Check ---")
names = list(data.keys())
n_order = sorted(names, key=lambda x: data[x]["n_exp"])
delta_elec_order = sorted(names, key=lambda x: data[x]["omega_per_wf"])
delta_eff_order = sorted(names, key=lambda x: delta_effs[x])

print(f"  n ordering:         {' < '.join(n_order)}")
print(f"  δ_elec ordering:    {' < '.join(delta_elec_order)}")
print(f"  δ_eff ordering:     {' < '.join(delta_eff_order)}")

match_elec = (delta_elec_order == n_order)
match_eff = (delta_eff_order == n_order)
print(f"\n  δ_elec matches n?   {'YES ✓' if match_elec else 'NO ✗'}")
print(f"  δ_eff matches n?    {'YES ✓' if match_eff else 'NO ✗'}")

# === Proportionality constant ===
print("\n--- Proportionality: n²-1 = C × δ_eff ---")
C_values = []
for name, d in data.items():
    n2m1 = d["n_exp"]**2 - 1
    C = n2m1 / delta_effs[name]
    C_values.append(C)
    print(f"  {name:<14} C = {C:.2f}")
C_mean = np.mean(C_values)
C_std = np.std(C_values)
print(f"  Mean C = {C_mean:.2f} ± {C_std:.2f}  (CV = {C_std/C_mean*100:.1f}%)")

# === Predicted n from delta_eff ===
print("\n--- Predicted n from δ_eff (using mean C) ---")
print(f"{'Element':<14} {'n_pred':>7} {'n_exp':>7} {'error':>8}")
print("-" * 40)
for name, d in data.items():
    n_pred = np.sqrt(1 + C_mean * delta_effs[name])
    n_exp = d["n_exp"]
    err = (n_pred - n_exp) / n_exp * 100
    print(f"{name:<14} {n_pred:>7.3f} {n_exp:>7.3f} {err:>7.1f}%")

# === Decomposition: how much does each factor contribute? ===
print("\n--- Factor Decomposition (Si → Ge) ---")
si = data["Si"]
ge = data["Ge"]

r_delta = ge["omega_per_wf"] / si["omega_per_wf"]
r_alpha = ge["alpha_atom"] / si["alpha_atom"]
r_eg2 = (si["E_g"] / ge["E_g"])**2  # inverse because 1/E_g^2
r_total = r_delta * r_alpha * r_eg2
r_n2m1 = (ge["n_exp"]**2 - 1) / (si["n_exp"]**2 - 1)

print(f"  Ω/WF ratio (Ge/Si):     {r_delta:.3f}  (d-screening → Ge shrinks)")
print(f"  α ratio (Ge/Si):         {r_alpha:.3f}  (Ge atom larger)")
print(f"  (E_g_Si/E_g_Ge)² ratio:  {r_eg2:.3f}  (Ge gap much smaller)")
print(f"  Product:                 {r_total:.3f}")
print(f"  Actual (n²-1) ratio:     {r_n2m1:.3f}")
print(f"  Agreement:               {r_total/r_n2m1*100:.0f}%")

# === What would Ge's Omega/WF be without d-screening? ===
print("\n--- Hypothetical: Ge without d-screening ---")
# If Ge followed the same shell-expansion trend as C→Si (no d-screening),
# extrapolate from periods 2→3 to period 4
omega_C = data["C (diamond)"]["omega_per_wf"]
omega_Si = data["Si"]["omega_per_wf"]
# Linear extrapolation in period number
slope = (omega_Si - omega_C) / (3 - 2)  # per period
omega_Ge_nodscreen = omega_C + slope * (4 - 2)
print(f"  C (period 2):   Ω/WF = {omega_C:.3f}")
print(f"  Si (period 3):  Ω/WF = {omega_Si:.3f}")
print(f"  Trend: +{slope:.3f} Ang²/period")
print(f"  Ge (period 4, extrapolated, no d-screening): Ω/WF = {omega_Ge_nodscreen:.3f}")
print(f"  Ge (period 4, actual, with d-screening):     Ω/WF = {data['Ge']['omega_per_wf']:.3f}")
print(f"  d-screening contraction: {(1 - data['Ge']['omega_per_wf']/omega_Ge_nodscreen)*100:.0f}%")

# delta_eff with hypothetical unscreened Ge
delta_eff_Ge_nodscreen = omega_Ge_nodscreen * ge["alpha_atom"] / ge["E_g"]**2
print(f"\n  δ_eff (screened):     {delta_effs['Ge']:.3f}")
print(f"  δ_eff (unscreened):   {delta_eff_Ge_nodscreen:.3f}")
print(f"  Ratio: unscreened/screened = {delta_eff_Ge_nodscreen/delta_effs['Ge']:.2f}x")

# === Penn model approach: volume-normalized ===
print("\n--- Penn Model Approach: n²-1 ∝ N_wf × Ω / (V_cell × E_g²) ---")
print("  (Ω/V = fraction of cell covered by each WF)")

# Primitive cell volumes (FCC: V = a^3 / 4)
volumes = {
    "C (diamond)": 3.567**3 / 4,   # 11.34 Ang^3
    "Si":          5.431**3 / 4,    # 40.05 Ang^3
    "Ge":          5.658**3 / 4,    # 45.27 Ang^3
}

print(f"\n{'Element':<14} {'V_cell':>8} {'Ω/V':>8} {'NΩ/(V·Eg²)':>12} {'n²-1':>7} {'C_penn':>8}")
print("-" * 65)
penn_effs = {}
for name, d in data.items():
    V = volumes[name]
    N_wf = 8  # all have 8 WFs per primitive cell
    omega_over_V = d["omega_per_wf"] / V
    penn_eff = N_wf * d["omega_per_wf"] / (V * d["E_g"]**2)
    n2m1 = d["n_exp"]**2 - 1
    C_penn = n2m1 / penn_eff
    penn_effs[name] = penn_eff
    print(f"{name:<14} {V:>8.2f} {omega_over_V:>8.4f} {penn_eff:>12.4f} {n2m1:>7.2f} {C_penn:>8.1f}")

penn_order = sorted(names, key=lambda x: penn_effs[x])
print(f"\n  Penn δ_eff ordering:  {' < '.join(penn_order)}")
match_penn = (penn_order == n_order)
print(f"  Matches n ordering?   {'YES ✓' if match_penn else 'NO ✗'}")

C_penn_vals = [((data[n]["n_exp"]**2 - 1) / penn_effs[n]) for n in names]
C_penn_mean = np.mean(C_penn_vals)
C_penn_std = np.std(C_penn_vals)
print(f"  C_penn: {C_penn_mean:.1f} ± {C_penn_std:.1f} (CV = {C_penn_std/C_penn_mean*100:.0f}%)")

# === Predicted n from Penn model ===
print(f"\n  Predicted n (Penn model, C = {C_penn_mean:.1f}):")
for name, d in data.items():
    n_pred = np.sqrt(1 + C_penn_mean * penn_effs[name])
    n_exp = d["n_exp"]
    err = (n_pred - n_exp) / n_exp * 100
    print(f"    {name:<14} n_pred = {n_pred:.3f}  n_exp = {n_exp:.3f}  ({err:+.1f}%)")

# === Alternative: use Ω × (Z_eff / r_cov²) as screened polarizability ===
print("\n--- Alternative: Clausius-Mossotti with Ω as bond polarizability ---")
print("  α_bond ≈ Ω/WF (spatial extent → polarizability proxy)")
print("  n²-1 ∝ (N/V) × α_bond / (1 + contribution from E_g)")

# Simple Clausius-Mossotti: (n²-1)/(n²+2) = (4π/3) × (N/V) × α_eff
# → test if α_eff ∝ Ω/WF
print(f"\n{'Element':<14} {'(n²-1)/(n²+2)':>14} {'N/V':>8} {'α_CM':>8} {'Ω/WF':>8} {'α_CM/Ω':>8}")
print("-" * 65)
for name, d in data.items():
    V = volumes[name]
    N = 2  # atoms per cell
    n2 = d["n_exp"]**2
    LHS = (n2 - 1) / (n2 + 2)  # Clausius-Mossotti LHS
    NoverV = N / V
    alpha_CM = LHS / (NoverV * 4 * np.pi / 3)  # effective polarizability per atom
    omega = d["omega_per_wf"]
    print(f"{name:<14} {LHS:>14.4f} {NoverV:>8.4f} {alpha_CM:>8.4f} {omega:>8.3f} {alpha_CM/omega:>8.4f}")

print("\n" + "=" * 72)
print("CONCLUSION")
print("=" * 72)
if match_eff:
    print("  The three-factor composite δ_eff = Ω/WF × α / E_g²")
    print("  RECOVERS the correct refractive index ordering: C < Si < Ge")
    print("  even though δ_elec alone gives the WRONG ordering: C < Ge < Si.")
    print()
    print("  The d-screening effect (Ge Ω/WF < Si Ω/WF) is real but is")
    print("  overcompensated by Ge's larger polarizability and smaller gap.")
else:
    print("  The three-factor model did NOT recover the correct ordering.")
    print("  Further investigation needed.")
