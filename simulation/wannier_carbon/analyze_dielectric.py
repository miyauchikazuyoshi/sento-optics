#!/usr/bin/env python3
"""
Analysis of DFPT dielectric constants vs experimental refractive indices.

DFT-PBE band gap problem and its impact on ε∞ prediction.
"""

import numpy as np

print("=" * 70)
print("DFPT Dielectric Constants: DFT-PBE vs Experiment")
print("=" * 70)

# DFPT results (this work, ph.x with epsil=.true.)
results = {
    "C (diamond)": {
        "eps_inf_dft": 5.890,
        "n_exp": 2.417,
        "Eg_exp": 5.47,    # eV
        "Eg_pbe": 4.15,    # eV (typical PBE value)
        "omega_per_wf": 0.954,
    },
    "Si": {
        "eps_inf_dft": 23.31,
        "n_exp": 3.44,
        "Eg_exp": 1.12,
        "Eg_pbe": 0.52,    # eV (typical PBE value)
        "omega_per_wf": 3.049,
    },
    "Ge": {
        "eps_inf_dft": None,  # DFPT failed: PBE closes gap
        "n_exp": 4.00,
        "Eg_exp": 0.661,
        "Eg_pbe": 0.0,     # PBE predicts zero/negative gap
        "omega_per_wf": 2.275,
    },
}

# === Table 1: Raw comparison ===
print("\n--- DFT-PBE vs Experiment ---")
print(f"{'Element':<14} {'ε∞(DFT)':>10} {'n_calc':>8} {'n_exp':>7} {'error':>8} {'Eg_PBE':>7} {'Eg_exp':>7}")
print("-" * 70)
for name, d in results.items():
    if d["eps_inf_dft"] is not None:
        n_calc = np.sqrt(d["eps_inf_dft"])
        err = (n_calc - d["n_exp"]) / d["n_exp"] * 100
        print(f"{name:<14} {d['eps_inf_dft']:>10.3f} {n_calc:>8.3f} {d['n_exp']:>7.3f} {err:>+7.1f}% {d['Eg_pbe']:>7.2f} {d['Eg_exp']:>7.3f}")
    else:
        print(f"{name:<14} {'FAILED':>10} {'—':>8} {d['n_exp']:>7.3f} {'—':>8} {d['Eg_pbe']:>7.2f} {d['Eg_exp']:>7.3f}")

# === Analysis: Gap error → ε error ===
print("\n--- Band Gap Error Amplification ---")
print("  Penn model: ε∞ - 1 ∝ 1/Eg²")
print("  → Relative error in ε scales as (Eg_exp/Eg_PBE)²")
print()
for name, d in results.items():
    if d["Eg_pbe"] > 0:
        gap_ratio = d["Eg_exp"] / d["Eg_pbe"]
        eps_exp = d["n_exp"]**2
        print(f"  {name:<14}")
        print(f"    Eg_exp/Eg_PBE = {gap_ratio:.2f}")
        print(f"    (Eg_exp/Eg_PBE)² = {gap_ratio**2:.2f}")
        if d["eps_inf_dft"] is not None:
            eps_ratio = d["eps_inf_dft"] / eps_exp
            print(f"    ε∞(DFT)/ε∞(exp) = {eps_ratio:.2f}")
            print(f"    → Gap error accounts for {(gap_ratio**2 / eps_ratio) * 100:.0f}% of ε overestimation")
    else:
        print(f"  {name:<14}")
        print(f"    Eg_PBE = 0 → DFPT impossible (metallic)")

# === Scissor correction estimate ===
print("\n--- Scissor-Corrected Estimate ---")
print("  If we apply scissor operator Δ = Eg_exp - Eg_PBE:")
print("  ε_corrected ≈ 1 + (ε_DFT - 1) × (Eg_PBE/Eg_exp)²")
print()
print(f"{'Element':<14} {'Δ(eV)':>7} {'ε_corr':>8} {'n_corr':>8} {'n_exp':>7} {'error':>8}")
print("-" * 55)
for name, d in results.items():
    if d["eps_inf_dft"] is not None and d["Eg_pbe"] > 0:
        scissor = d["Eg_exp"] - d["Eg_pbe"]
        ratio = (d["Eg_pbe"] / d["Eg_exp"])**2
        eps_corr = 1 + (d["eps_inf_dft"] - 1) * ratio
        n_corr = np.sqrt(eps_corr)
        err = (n_corr - d["n_exp"]) / d["n_exp"] * 100
        print(f"{name:<14} {scissor:>7.2f} {eps_corr:>8.3f} {n_corr:>8.3f} {d['n_exp']:>7.3f} {err:>+7.1f}%")

# === Connection to Wannier spread ===
print("\n--- Connection to δ (Wannier Spread) ---")
print("  The PBE gap problem is orthogonal to Wannier spread accuracy.")
print("  Wannier spread Ω/WF is determined by occupied-state wavefunctions,")
print("  not by the gap. So:")
print("    ✓ Ω/WF values (0.95, 3.05, 2.28) are reliable")
print("    ✗ ε∞ from PBE underestimates Eg → overestimates ε")
print("    → The three-factor model δ × α / Eg² needs EXPERIMENTAL Eg,")
print("      not PBE Eg, for quantitative predictions.")
print()
print("  This is consistent with our finding: δ (from Wannier) captures")
print("  the delocalization physics correctly, but quantitative optical")
print("  prediction requires accurate Eg (beyond PBE).")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("  1. Diamond: ε∞ = 5.89, n = 2.43 (exp 2.42) — excellent (+0.4%)")
print("  2. Si:      ε∞ = 23.3, n = 4.83 (exp 3.44) — PBE gap too small (+40%)")
print("  3. Ge:      DFPT failed — PBE predicts zero gap (metallic)")
print()
print("  The DFT-PBE band gap problem dominates optical predictions.")
print("  Wannier spread (δ_elec) is unaffected by this problem.")
print("  For quantitative n prediction across elements,")
print("  either scissor correction or hybrid functional (HSE06) is needed.")
