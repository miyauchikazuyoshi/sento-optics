#!/usr/bin/env python3
"""
Test 4: Water two-state model with literature-fixed parameters.

Critical question: If we fix all parameters from literature BEFORE
knowing the target (T_max = 3.98°C), does the model still produce
a density maximum near 4°C? Or was the original result just curve fitting?

Literature values:
  - H-bond energy: ~0.2 eV per bond (Suresh & Naik 2000, J. Chem. Phys. 113, 9727)
    But each molecule has ~2 bonds (tetrahedral network, shared),
    so effective ΔE ≈ 0.1-0.2 eV per molecule
  - Fusion entropy: ΔS_fus = 22.0 J/(mol·K) = 2.28e-4 eV/K per molecule
    (standard thermodynamic data for ice melting)
  - Thermal expansion: β = 2.07e-4 K⁻¹ at 20°C for water
    (IAPWS-95, Wagner & Pruss 2002)

The original tuned values were: dE=0.050, dS=2.15e-4, α=3.0e-4
→ produced T_max = 4.5°C

This test: use literature values and see what happens.

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)

kB = 8.617e-5  # eV/K
NA = 6.022e23


def two_state_water_parametric(T_range, delta_E, delta_S, alpha, label=""):
    """Two-state model with explicit parameters."""
    M_water = 18.015
    V_ice = M_water / (0.917 * NA) * 1e24    # Å³ per molecule (ice Ih density)
    V_close = M_water / (1.08 * NA) * 1e24   # close-packed
    T0 = 273.15

    f_A = np.zeros_like(T_range, dtype=float)
    rho = np.zeros_like(T_range, dtype=float)

    for i, T in enumerate(T_range):
        delta_G = delta_E - T * delta_S
        x = delta_G / (kB * T)
        x = np.clip(x, -500, 500)
        f_A[i] = 1.0 / (1.0 + np.exp(-x))

        V_A_T = V_ice * (1.0 + alpha * (T - T0))
        V_B_T = V_close * (1.0 + alpha * (T - T0))
        V_avg = f_A[i] * V_A_T + (1.0 - f_A[i]) * V_B_T
        rho[i] = M_water / (V_avg * 1e-24 * NA)

    T_celsius = T_range - 273.15
    i_max = np.argmax(rho)
    T_max = T_celsius[i_max]
    rho_max = rho[i_max]

    return rho, f_A, T_max, rho_max


def main():
    print("=" * 70)
    print("TEST 4: Water Model with Literature-Fixed Parameters")
    print("Can we PREDICT T_max without tuning?")
    print("=" * 70)

    T_range = np.linspace(253.15, 373.15, 1000)
    T_celsius = T_range - 273.15

    # Experimental data
    T_exp = np.array([0, 4, 10, 20, 30, 40, 50, 60, 80, 100])
    rho_exp = np.array([0.99984, 0.99997, 0.99970, 0.99821,
                         0.99565, 0.99222, 0.98803, 0.98320,
                         0.97179, 0.95835])

    # ── Parameter sets ──
    param_sets = {
        "Original (tuned)": {
            "delta_E": 0.050,     # eV — tuned
            "delta_S": 2.15e-4,   # eV/K — tuned
            "alpha":   3.0e-4,    # K⁻¹ — tuned
            "color": "blue",
            "ls": "-",
        },
        "Literature A\n(ΔE=0.10, ΔS=ΔS_fus)": {
            "delta_E": 0.100,     # eV — ~half of full H-bond energy
            "delta_S": 2.28e-4,   # eV/K — fusion entropy of ice
            "alpha":   2.07e-4,   # K⁻¹ — measured thermal expansion at 20°C
            "color": "red",
            "ls": "--",
        },
        "Literature B\n(ΔE=0.20, ΔS=ΔS_fus)": {
            "delta_E": 0.200,     # eV — full H-bond energy per bond
            "delta_S": 2.28e-4,   # eV/K — fusion entropy of ice
            "alpha":   2.07e-4,   # K⁻¹ — measured thermal expansion
            "color": "darkred",
            "ls": "-.",
        },
        "Literature C\n(ΔE=0.05, ΔS=ΔS_fus)": {
            "delta_E": 0.050,     # eV — same as tuned
            "delta_S": 2.28e-4,   # eV/K — fusion entropy (literature)
            "alpha":   2.07e-4,   # K⁻¹ — thermal expansion (literature)
            "color": "green",
            "ls": "--",
        },
    }

    # ── Also scan ΔE systematically with literature ΔS and α ──
    dE_scan = np.linspace(0.01, 0.30, 60)
    T_max_scan = []
    has_maximum = []

    for dE in dE_scan:
        rho_scan, _, T_max_s, _ = two_state_water_parametric(
            T_range, delta_E=dE, delta_S=2.28e-4, alpha=2.07e-4
        )
        # Check if maximum is in liquid range (0-100°C)
        i_max = np.argmax(rho_scan)
        T_max_C = T_celsius[i_max]
        if 0 < T_max_C < 100:
            T_max_scan.append(T_max_C)
            has_maximum.append(True)
        else:
            T_max_scan.append(np.nan)
            has_maximum.append(False)

    T_max_scan = np.array(T_max_scan)

    # ── Run all parameter sets ──
    print(f"\n{'Parameter set':>35s}  {'T_max [°C]':>10s}  {'ρ_max [g/cm³]':>14s}")
    print("-" * 65)

    results = {}
    for label, params in param_sets.items():
        rho, f_A, T_max, rho_max = two_state_water_parametric(
            T_range, params["delta_E"], params["delta_S"], params["alpha"]
        )
        results[label] = {"rho": rho, "f_A": f_A, "T_max": T_max, "rho_max": rho_max}
        short_label = label.replace("\n", " ")
        print(f"{short_label:>35s}  {T_max:10.1f}  {rho_max:14.5f}")

    print(f"\n  Experimental T_max = 3.98°C, ρ_max = 0.99997 g/cm³")

    # ── Verdict ──
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    lit_a_tmax = results["Literature A\n(ΔE=0.10, ΔS=ΔS_fus)"]["T_max"]
    lit_b_tmax = results["Literature B\n(ΔE=0.20, ΔS=ΔS_fus)"]["T_max"]
    lit_c_tmax = results["Literature C\n(ΔE=0.05, ΔS=ΔS_fus)"]["T_max"]
    orig_tmax = results["Original (tuned)"]["T_max"]

    # Check if ANY literature set gives T_max near 4°C
    for label, r in results.items():
        if "Literature" in label:
            if abs(r["T_max"] - 3.98) < 10:
                print(f"  {label.replace(chr(10), ' ')}: T_max = {r['T_max']:.1f}°C "
                      f"(Δ = {r['T_max'] - 3.98:.1f}°C from experiment)")
            elif abs(r["T_max"]) > 90 or r["T_max"] < -10:
                print(f"  {label.replace(chr(10), ' ')}: NO maximum in liquid range")
            else:
                print(f"  {label.replace(chr(10), ' ')}: T_max = {r['T_max']:.1f}°C "
                      f"(far from 4°C)")

    # Find dE that gives T_max ≈ 4°C with literature dS, alpha
    valid = ~np.isnan(T_max_scan)
    if valid.any():
        best_idx = np.nanargmin(np.abs(T_max_scan - 3.98))
        best_dE = dE_scan[best_idx]
        best_Tmax = T_max_scan[best_idx]
        print(f"\n  For literature ΔS & α, T_max ≈ 4°C requires ΔE ≈ {best_dE:.3f} eV")
        print(f"    (produces T_max = {best_Tmax:.1f}°C)")
        print(f"    Literature H-bond energy: 0.1-0.2 eV per molecule")
        if 0.05 <= best_dE <= 0.25:
            print(f"  ✓ Required ΔE is within physical range")
        else:
            print(f"  ⚠ Required ΔE is outside physical range")

    # ── Figure ──
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Test 4: Water Model — Tuned vs Literature Parameters",
                 fontsize=14, y=1.02)

    # (a) ρ(T) for all parameter sets
    ax = axes[0, 0]
    ax.plot(T_exp, rho_exp, "ko", markersize=8, label="Experiment", zorder=10)
    for label, params in param_sets.items():
        r = results[label]
        short = label.split("\n")[0]
        ax.plot(T_celsius, r["rho"], color=params["color"], linestyle=params["ls"],
                linewidth=2, label=f"{short} (T_max={r['T_max']:.1f}°C)")
    ax.axvline(3.98, color="gray", linestyle=":", alpha=0.5, label="T=3.98°C")
    ax.set_xlabel("Temperature [°C]", fontsize=12)
    ax.set_ylabel("Density [g/cm³]", fontsize=12)
    ax.set_title("(a) Density vs Temperature", fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_xlim(-10, 100)

    # (b) T_max vs ΔE scan (with literature ΔS, α)
    ax = axes[0, 1]
    ax.plot(dE_scan * 1000, T_max_scan, "b-", linewidth=2)
    ax.axhline(3.98, color="red", linestyle="--", label="Experimental T_max = 3.98°C")
    ax.axvspan(100, 200, alpha=0.1, color="green", label="Literature ΔE range (0.1-0.2 eV)")
    if valid.any():
        ax.scatter([best_dE * 1000], [best_Tmax], s=100, c="red", zorder=10,
                   label=f"Best ΔE = {best_dE*1000:.0f} meV")
    ax.set_xlabel("ΔE [meV]", fontsize=12)
    ax.set_ylabel("T_max [°C]", fontsize=12)
    ax.set_title("(b) T_max vs ΔE (ΔS, α from literature)", fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_ylim(-20, 100)

    # (c) f_A(T) comparison
    ax = axes[1, 0]
    for label, params in param_sets.items():
        r = results[label]
        short = label.split("\n")[0]
        ax.plot(T_celsius, r["f_A"], color=params["color"],
                linestyle=params["ls"], linewidth=2, label=short)
    ax.set_xlabel("Temperature [°C]", fontsize=12)
    ax.set_ylabel("H-bond fraction f_A", fontsize=12)
    ax.set_title("(c) H-bond Network Fraction", fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_xlim(-10, 100)

    # (d) Parameter comparison table as text
    ax = axes[1, 1]
    ax.axis("off")
    table_data = [
        ["Parameter", "Tuned", "Lit A", "Lit B", "Lit C", "Source"],
        ["ΔE [eV]", "0.050", "0.100", "0.200", "0.050", "Suresh & Naik 2000"],
        ["ΔS [eV/K]", "2.15e-4", "2.28e-4", "2.28e-4", "2.28e-4", "Ice ΔS_fus"],
        ["α [K⁻¹]", "3.0e-4", "2.07e-4", "2.07e-4", "2.07e-4", "IAPWS-95"],
        ["T_max [°C]", f"{orig_tmax:.1f}", f"{lit_a_tmax:.1f}",
         f"{lit_b_tmax:.1f}", f"{lit_c_tmax:.1f}", "Exp: 3.98"],
    ]
    table = ax.table(cellText=table_data, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.8)
    # Header row
    for j in range(6):
        table[0, j].set_facecolor("#ddd")
        table[0, j].set_text_props(fontweight="bold")
    # T_max row
    for j in range(6):
        table[4, j].set_facecolor("#fff3cd")
    ax.set_title("(d) Parameter Comparison", fontsize=11, pad=20)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test4_water_literature.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test4_water_literature.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
