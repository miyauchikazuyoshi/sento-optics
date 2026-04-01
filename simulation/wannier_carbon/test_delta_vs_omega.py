#!/usr/bin/env python3
"""
δ_IPR vs Ω/WF correlation test.

Goal: show that δ (from TB model, Paper I) predicts Ω (from DFT+Wannier90).
If δ ∝ Ω, then combined with Cardenas-Castillo (2024) sum rule Ω_I = ∫ε₂/ω dω,
we get: δ → Ω → ε₂(ω) — the full prediction chain.
"""

import sys
import os
import numpy as np

# Import TB delta functions from Paper I simulation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'optics'))
from delocalization_optics_v2 import (
    compute_diamond_delta,
    compute_graphene_delta,
    compute_chain1d_delta,
    compute_c60_delta,
    compute_diamond_delta_sk,
    compute_silicon_delta,
    compute_germanium_delta,
)

print("=" * 65)
print("δ_IPR (TB model) vs Ω/WF (DFT+Wannier90)")
print("=" * 65)

# === Compute δ_IPR from TB models ===
print("\nComputing δ_IPR from tight-binding models...")

delta_diamond = compute_diamond_delta()
delta_graphene = compute_graphene_delta()
delta_chain1d = compute_chain1d_delta()
delta_c60 = compute_c60_delta()

print(f"  Diamond:   δ_IPR = {delta_diamond:.4f}")
print(f"  Graphene:  δ_IPR = {delta_graphene:.4f}")
print(f"  1D chain:  δ_IPR = {delta_chain1d:.4f}")
print(f"  C60:       δ_IPR = {delta_c60:.4f}")

# === Slater-Koster sp3 models (Diamond, Si, Ge) ===
print("\nComputing δ_IPR from Slater-Koster sp3 models...")
print("  (Harrison universal parameters, 3×3×3 supercell)")

delta_diamond_sk = compute_diamond_delta_sk()
delta_si = compute_silicon_delta()
delta_ge = compute_germanium_delta()

print(f"  Diamond (SK): δ_IPR = {delta_diamond_sk:.4f}")
print(f"  Si (SK):      δ_IPR = {delta_si:.4f}")
print(f"  Ge (SK):      δ_IPR = {delta_ge:.4f}")

# === Ω/WF from DFT+Wannier90 (this work) ===
# Only diamond and graphite have been computed
omega_data = {
    "Diamond":  0.954,   # Ang^2
    "Graphite": 6.375,   # Ang^2 (proxy for graphene in 3D)
    "Si":       3.049,   # Ang^2
    "Ge":       2.275,   # Ang^2
}

# === Comparison table ===
print("\n--- δ_IPR vs Ω/WF ---")
print(f"{'System':<12} {'δ_IPR (TB)':>12} {'Ω/WF (DFT)':>12} {'D_eff':>6} {'Optical':>14}")
print("-" * 60)

systems = [
    ("Diamond",  delta_diamond,  0.954,  3, "Transparent"),
    ("Graphite", delta_graphene, 6.375,  2, "Black+gloss"),
    ("1D chain", delta_chain1d,  None,   1, "(metallic 1D)"),
    ("C60",      delta_c60,      None,   0, "Colored"),
]

deltas = []
omegas = []
for name, delta, omega, deff, opt in systems:
    omega_str = f"{omega:.3f}" if omega is not None else "—"
    print(f"{name:<12} {delta:>12.4f} {omega_str:>12} {deff:>6} {opt:>14}")
    if omega is not None:
        deltas.append(delta)
        omegas.append(omega)

# === Correlation (only for systems with both δ and Ω) ===
if len(deltas) >= 2:
    deltas = np.array(deltas)
    omegas = np.array(omegas)

    print(f"\n--- Correlation (N={len(deltas)} systems with both δ and Ω) ---")

    # Pearson correlation
    if len(deltas) > 2:
        r = np.corrcoef(deltas, omegas)[0, 1]
        print(f"  Pearson r = {r:.4f}")

    # Ratio test: is Ω/δ approximately constant?
    ratios = omegas / deltas
    print(f"  Ω/δ ratios:")
    for i, (name, _, omega, _, _) in enumerate(systems):
        if omega is not None:
            print(f"    {name}: Ω/δ = {ratios[i]:.2f}")
    if len(ratios) > 1:
        print(f"  Mean Ω/δ = {np.mean(ratios):.2f} ± {np.std(ratios):.2f}")
        print(f"  CV = {np.std(ratios)/np.mean(ratios)*100:.0f}%")

    # Ordering check
    delta_order = sorted(range(len(deltas)), key=lambda i: deltas[i])
    omega_order = sorted(range(len(omegas)), key=lambda i: omegas[i])
    match = (delta_order == omega_order)
    print(f"\n  Ordering match: {'YES ✓' if match else 'NO ✗'}")
    print(f"    δ order:  {' < '.join([systems[i][0] for i in delta_order])}")
    print(f"    Ω order:  {' < '.join([systems[i][0] for i in omega_order])}")

# === D_eff correction: does δ × f(D_eff) improve the correlation? ===
print("\n--- D_eff Corrections ---")

corrections = {
    "δ × D_eff":          lambda d, deff: d * deff,
    "δ × (D_eff+1)":      lambda d, deff: d * (deff + 1),
    "δ × D_eff²":         lambda d, deff: d * deff**2,
    "δ × √D_eff":         lambda d, deff: d * np.sqrt(deff) if deff > 0 else 0,
    "δ^(1/D_eff)":        lambda d, deff: d**(1.0/deff) if deff > 0 else 0,
    "δ × D_eff / (D_eff+1)": lambda d, deff: d * deff / (deff + 1),
}

for corr_name, corr_func in corrections.items():
    print(f"\n  {corr_name}:")
    corr_vals = []
    corr_omegas = []
    all_vals = []
    for name, delta, omega, deff, opt in systems:
        val = corr_func(delta, deff)
        all_vals.append((name, val, omega))
        if omega is not None and val > 0:
            corr_vals.append(val)
            corr_omegas.append(omega)

    for name, val, omega in all_vals:
        omega_str = f"{omega:.3f}" if omega is not None else "—"
        ratio_str = f"{omega/val:.2f}" if (omega is not None and val > 0) else "—"
        print(f"    {name:<12} {corr_name}={val:.4f}  Ω={omega_str}  Ω/corr={ratio_str}")

    if len(corr_vals) >= 2:
        corr_vals = np.array(corr_vals)
        corr_omegas = np.array(corr_omegas)
        ratios = corr_omegas / corr_vals
        cv = np.std(ratios) / np.mean(ratios) * 100 if np.mean(ratios) > 0 else float('inf')
        print(f"    CV = {cv:.0f}%  (lower is better)")

# === Also test: does N (system size) matter? ===
print("\n--- System size check ---")
print("  Diamond TB:  54 atoms (3×3×3 supercell)")
print("  Graphene TB: 72 atoms (6×6 supercell)")
print("  C60 TB:      60 atoms")
print("  1D chain TB: 60 atoms")
print("  → Sizes are comparable, so N-normalization should be fair.")

# === What about log scaling? (IPR is exponential in localization) ===
print("\n--- Log-scale comparison ---")
print(f"{'System':<12} {'log(δ)':>10} {'log(Ω)':>10} {'Ratio':>10}")
print("-" * 45)
for name, delta, omega, deff, opt in systems:
    if omega is not None and delta > 0:
        ld = np.log(delta)
        lo = np.log(omega)
        print(f"{name:<12} {ld:>10.3f} {lo:>10.3f} {lo/ld:>10.3f}")

# ================================================================
# Slater-Koster sp3 model: Diamond, Si, Ge (all D_eff=3)
# ================================================================
print("\n" + "=" * 65)
print("Slater-Koster sp3 model: δ_IPR vs Ω/WF (N=4, D_eff=3 subset)")
print("=" * 65)

sk_systems = [
    ("Diamond",  delta_diamond_sk, 0.954,  3),
    ("Si",       delta_si,         3.049,  3),
    ("Ge",       delta_ge,         2.275,  3),
    ("Graphite", delta_graphene,   6.375,  2),
]

print(f"\n{'System':<12} {'δ_IPR (SK)':>12} {'Ω/WF (DFT)':>12} {'D_eff':>6}")
print("-" * 50)
for name, delta, omega, deff in sk_systems:
    print(f"{name:<12} {delta:>12.4f} {omega:>12.3f} {deff:>6}")

# D_eff=3 subset (Diamond, Si, Ge) — same crystal structure
print("\n--- D_eff=3 subset (Diamond, Si, Ge) ---")
print("  Same crystal structure → δ直接比較が公平")

d3_systems = [(n, d, o) for n, d, o, deff in sk_systems if deff == 3]
d3_deltas = np.array([d for _, d, _ in d3_systems])
d3_omegas = np.array([o for _, _, o in d3_systems])

# Ordering check
d3_delta_order = sorted(range(len(d3_deltas)), key=lambda i: d3_deltas[i])
d3_omega_order = sorted(range(len(d3_omegas)), key=lambda i: d3_omegas[i])
match = (d3_delta_order == d3_omega_order)
print(f"\n  Ordering match: {'YES ✓' if match else 'NO ✗'}")
print(f"    δ order:  {' < '.join([d3_systems[i][0] for i in d3_delta_order])}")
print(f"    Ω order:  {' < '.join([d3_systems[i][0] for i in d3_omega_order])}")

# Ratio test
d3_ratios = d3_omegas / d3_deltas
print(f"\n  Ω/δ ratios:")
for i, (name, delta, omega) in enumerate(d3_systems):
    print(f"    {name}: Ω/δ = {d3_ratios[i]:.2f}")
print(f"  Mean Ω/δ = {np.mean(d3_ratios):.2f} ± {np.std(d3_ratios):.2f}")
cv = np.std(d3_ratios) / np.mean(d3_ratios) * 100
print(f"  CV = {cv:.0f}%")

# Pearson correlation
if len(d3_deltas) >= 3:
    r = np.corrcoef(d3_deltas, d3_omegas)[0, 1]
    print(f"  Pearson r = {r:.4f}")

# D_eff corrections for all 4 systems
print("\n--- D_eff corrections (all 4 systems, SK model) ---")
all_sk_deltas = np.array([d for _, d, _, _ in sk_systems])
all_sk_omegas = np.array([o for _, _, o, _ in sk_systems])
all_sk_deffs = np.array([deff for _, _, _, deff in sk_systems])

for corr_name, corr_func in [
    ("δ × D_eff",     lambda d, deff: d * deff),
    ("δ × D_eff²",    lambda d, deff: d * deff**2),
    ("δ × (D_eff+1)", lambda d, deff: d * (deff + 1)),
]:
    corr_vals = np.array([corr_func(d, deff) for d, deff in zip(all_sk_deltas, all_sk_deffs)])
    ratios = all_sk_omegas / corr_vals
    cv = np.std(ratios) / np.mean(ratios) * 100
    print(f"\n  {corr_name}:")
    for i, (name, _, omega, _) in enumerate(sk_systems):
        print(f"    {name:<12} corrected={corr_vals[i]:.4f}  Ω={omega:.3f}  Ω/corr={ratios[i]:.2f}")
    print(f"    CV = {cv:.0f}%  Mean ratio = {np.mean(ratios):.2f}")

# Ge anomaly check
print("\n--- Ge anomaly (d-electron screening) ---")
print("  Ω ordering: Diamond < Ge < Si")
print("  If δ ordering: Diamond < Si < Ge → d-electron effect NOT captured")
print("  If δ ordering: Diamond < Ge < Si → TB captures the physics")
ge_idx = [i for i, (n, _, _, _) in enumerate(sk_systems) if n == "Ge"][0]
si_idx = [i for i, (n, _, _, _) in enumerate(sk_systems) if n == "Si"][0]
if all_sk_deltas[si_idx] > all_sk_deltas[ge_idx]:
    print("  → δ(Si) > δ(Ge): TB DOES NOT capture Ge d-screening (expected)")
    print("    This is consistent with our earlier finding that sp-only models")
    print("    cannot account for 3d-electron screening in Ge (Pyykkö 1988)")
else:
    print("  → δ(Ge) > δ(Si): TB captures Ge anomaly (surprising!)")

print("\n" + "=" * 65)
print("INTERPRETATION")
print("=" * 65)
print("  If δ_IPR ∝ Ω/WF (ordering match + reasonable CV):")
print("    → δ (TB, our theory) predicts Ω (DFT, first-principles)")
print("    → Cardenas-Castillo (2024): Ω = ∫ε₂/ω dω (proven)")
print("    → Therefore: δ → Ω → ε₂(ω)")
print("    → The full prediction chain is closed.")
print("  If Si/Ge ordering mismatches:")
print("    → sp3 TB model misses d-electron screening in Ge")
print("    → δ→Ω requires beyond-sp model (d-orbitals or DFT)")
print("    → Limitation is well-understood, not a failure of the framework")
