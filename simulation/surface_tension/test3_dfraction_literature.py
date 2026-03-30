#!/usr/bin/env python3
"""
Test 3: Replace ad-hoc d_fraction values with literature-derived ones.

Critical question: The original d_fraction values (Cu=0.60, Zn=0.45, etc.)
have no cited source. If we use physically justified values from electronic
structure theory, does the correlation improve, stay the same, or collapse?

Literature d_fraction estimates:
  For each metal, d_fraction = N_d / N_total_valence

  Electronic configurations and d-band occupancies:
  - Al (Z=13): [Ne]3s²3p¹ → 3 sp electrons, 0 d → f_d = 0.00
  - Zn (Z=30): [Ar]3d¹⁰4s² → 2 sp + 10 d → f_d = 10/12 = 0.833
  - Mg (Z=12): [Ne]3s² → 2 sp, 0 d → f_d = 0.00
  - Li (Z=3):  [He]2s¹ → 1 sp, 0 d → f_d = 0.00
  - Na (Z=11): [Ne]3s¹ → 1 sp, 0 d → f_d = 0.00
  - K  (Z=19): [Ar]4s¹ → 1 sp, 0 d → f_d = 0.00
  - Cs (Z=55): [Xe]6s¹ → 1 sp, 0 d → f_d = 0.00
  - Cu (Z=29): [Ar]3d¹⁰4s¹ → 1 sp + 10 d → f_d = 10/11 = 0.909
  - Ga (Z=31): [Ar]3d¹⁰4s²4p¹ → 3 sp + 10 d → f_d = 10/13 = 0.769
  - Sn (Z=50): [Kr]4d¹⁰5s²5p² → 4 sp + 10 d → f_d = 10/14 = 0.714
  - Pb (Z=82): [Xe]4f¹⁴5d¹⁰6s²6p² → 4 sp + 10 d + 14 f → f_d = 10/28 ≈ 0.357
  - In (Z=49): [Kr]4d¹⁰5s²5p¹ → 3 sp + 10 d → f_d = 10/13 = 0.769

Note: These are MAXIMUM estimates. In practice, d-bands that are far below
Fermi level contribute less to surface properties. A more physical approach:
  - Weight by DOS at Fermi level: f_d_eff = DOS_d(E_F) / DOS_total(E_F)
  - For Zn, Cu: d-band is ~2-5 eV below E_F → f_d_eff << f_d_config
  - Typical XPS-derived values:
    Cu: ~80% d-character at E_F (copper d-band straddles E_F)
    Zn: ~5% d-character at E_F (d-band fully below E_F by ~9 eV)

We test THREE scenarios:
  A) Full configuration d_fraction (N_d/N_total)
  B) "Effective" d_fraction weighted by proximity to E_F
  C) Original ad-hoc values (for comparison)

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
from scipy.stats import pearsonr, spearmanr
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from delta_vs_nbar import (
    METALS as ORIGINAL_METALS, bulk_density, density_profile,
    compute_delta_gradient, BOHR_TO_ANG,
)

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)


# Three d_fraction schemes
D_FRACTIONS = {
    "Original (ad-hoc)": {
        "Al": 0.00, "Zn": 0.45, "Mg": 0.00, "Li": 0.00,
        "Na": 0.00, "K":  0.00, "Cs": 0.00,
        "Cu": 0.60, "Ga": 0.30, "Sn": 0.10, "Pb": 0.05, "In": 0.05,
    },
    "Config (N_d/N_val)": {
        "Al": 0.000, "Zn": 0.833, "Mg": 0.000, "Li": 0.000,
        "Na": 0.000, "K":  0.000, "Cs": 0.000,
        "Cu": 0.909, "Ga": 0.769, "Sn": 0.714, "Pb": 0.357, "In": 0.769,
    },
    "Effective (DOS-weighted)": {
        # Based on DFT DOS literature:
        # Cu: d-band straddles E_F → high effective d-character
        # Zn: d-band ~9 eV below E_F → negligible at E_F
        # Ga: d-band ~15 eV below E_F → negligible
        # Sn: d-band ~20 eV below E_F → negligible
        # Pb: d-band ~15 eV below E_F → negligible
        # In: d-band ~15 eV below E_F → negligible
        # Source: Papaconstantopoulos (1986) Handbook of Band Structure
        "Al": 0.000, "Zn": 0.050, "Mg": 0.000, "Li": 0.000,
        "Na": 0.000, "K":  0.000, "Cs": 0.000,
        "Cu": 0.800, "Ga": 0.020, "Sn": 0.010, "Pb": 0.010, "In": 0.010,
    },
}


def compute_all_correlations(d_frac_dict, names, z_grid):
    """Compute δ-gradient for each metal with given d_fractions."""
    gammas = []
    dgrads = []
    n_bars = []

    for name in names:
        r_s = ORIGINAL_METALS[name]["r_s"]
        n_bar = bulk_density(r_s)
        d_f = d_frac_dict[name]
        n_z = density_profile(z_grid, r_s, d_fraction=d_f)
        dg = compute_delta_gradient(z_grid, n_z, n_bar)

        gammas.append(ORIGINAL_METALS[name]["gamma_exp"])
        dgrads.append(dg)
        n_bars.append(n_bar)

    gammas = np.array(gammas)
    dgrads = np.array(dgrads)
    n_bars = np.array(n_bars)

    r_corr, p_val = pearsonr(dgrads, gammas)
    r_sp, p_sp = spearmanr(dgrads, gammas)
    r_nbar, _ = pearsonr(n_bars, gammas)

    # LOO R²
    N = len(gammas)
    y_pred_loo = np.zeros(N)
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        c = np.polyfit(dgrads[mask], gammas[mask], 1)
        y_pred_loo[i] = np.polyval(c, dgrads[i])
    ss_res = np.sum((gammas - y_pred_loo)**2)
    ss_tot = np.sum((gammas - gammas.mean())**2)
    r2_loo = 1.0 - ss_res / ss_tot

    # Partial correlation (control for n_bar)
    c1 = np.polyfit(n_bars, dgrads, 1)
    c2 = np.polyfit(n_bars, gammas, 1)
    resid_dg = dgrads - np.polyval(c1, n_bars)
    resid_g = gammas - np.polyval(c2, n_bars)
    r_partial, p_partial = pearsonr(resid_dg, resid_g)

    return {
        "gammas": gammas, "dgrads": dgrads, "n_bars": n_bars,
        "r_pearson": r_corr, "p_pearson": p_val,
        "r_spearman": r_sp,
        "r_nbar": r_nbar,
        "r2_loo": r2_loo,
        "r_partial": r_partial, "p_partial": p_partial,
    }


def main():
    print("=" * 70)
    print("TEST 3: d_fraction — Ad-hoc vs Literature Values")
    print("=" * 70)

    names = list(ORIGINAL_METALS.keys())
    z_grid = np.linspace(-10.0, 10.0, 2000)

    # Compare d_fraction values
    print(f"\n{'Metal':>6s}  {'Original':>9s}  {'Config':>9s}  {'Effective':>9s}")
    print("-" * 40)
    for n in names:
        o = D_FRACTIONS["Original (ad-hoc)"][n]
        c = D_FRACTIONS["Config (N_d/N_val)"][n]
        e = D_FRACTIONS["Effective (DOS-weighted)"][n]
        flag = " ←" if abs(o - c) > 0.2 else ""
        print(f"{n:>6s}  {o:9.3f}  {c:9.3f}  {e:9.3f}{flag}")

    # Run all three
    print(f"\n{'Scheme':>30s}  {'Pearson r':>10s}  {'Spearman ρ':>10s}  "
          f"{'LOO R²':>8s}  {'Partial r':>10s}  {'n_free':>6s}")
    print("-" * 85)

    all_results = {}
    for scheme, d_frac in D_FRACTIONS.items():
        n_free = sum(1 for v in d_frac.values() if v > 0)
        res = compute_all_correlations(d_frac, names, z_grid)
        all_results[scheme] = res
        print(f"{scheme:>30s}  {res['r_pearson']:10.4f}  {res['r_spearman']:10.4f}  "
              f"{res['r2_loo']:8.4f}  {res['r_partial']:10.4f}  {n_free:6d}")

    # Also compute n_bar-only baseline
    r_nbar = all_results["Original (ad-hoc)"]["r_nbar"]
    print(f"{'n_bar alone (baseline)':>30s}  {r_nbar:10.4f}  {'1.0000':>10s}  "
          f"{'—':>8s}  {'—':>10s}  {'0':>6s}")

    # ── Verdict ──
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    orig = all_results["Original (ad-hoc)"]
    config = all_results["Config (N_d/N_val)"]
    eff = all_results["Effective (DOS-weighted)"]

    if config["r_pearson"] < orig["r_pearson"]:
        print(f"  Config d_fractions WORSEN correlation: "
              f"r = {config['r_pearson']:.4f} vs {orig['r_pearson']:.4f}")
        print(f"  → Original values were likely tuned to fit.")
    else:
        print(f"  Config d_fractions IMPROVE correlation: "
              f"r = {config['r_pearson']:.4f} vs {orig['r_pearson']:.4f}")
        print(f"  → Physics-based values work better.")

    if eff["r_pearson"] < r_nbar:
        print(f"  Effective (DOS) d_fractions WORSE THAN n_bar alone: "
              f"r = {eff['r_pearson']:.4f} vs {r_nbar:.4f}")
    print()

    # Check if any scheme has r_partial > 0.5 (genuine beyond-n_bar info)
    for scheme, res in all_results.items():
        if abs(res["r_partial"]) > 0.5:
            print(f"  ✓ {scheme}: partial r = {res['r_partial']:.3f} "
                  f"→ carries info beyond n_bar")
        else:
            print(f"  ✗ {scheme}: partial r = {res['r_partial']:.3f} "
                  f"→ little beyond n_bar")

    # ── Figure ──
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("Test 3: d_fraction — Ad-hoc vs Literature Values",
                 fontsize=14, y=1.02)

    schemes = list(D_FRACTIONS.keys())
    colors_scheme = ["steelblue", "darkred", "forestgreen"]

    # Top row: scatter plots for each scheme
    for idx, (scheme, res) in enumerate(all_results.items()):
        ax = axes[0, idx]
        sp_mask = [not ORIGINAL_METALS[n]["has_d"] for n in names]
        d_mask = [ORIGINAL_METALS[n]["has_d"] for n in names]

        for i, n in enumerate(names):
            c = "blue" if sp_mask[i] else "red"
            m = "o" if sp_mask[i] else "^"
            ax.scatter(res["dgrads"][i], res["gammas"][i],
                       s=70, c=c, marker=m, edgecolors="black", linewidth=0.5, zorder=5)
            ax.annotate(n, (res["dgrads"][i], res["gammas"][i]),
                        textcoords="offset points", xytext=(4, 4), fontsize=7)

        # Fit line
        c = np.polyfit(res["dgrads"], res["gammas"], 1)
        x_fit = np.linspace(res["dgrads"].min() * 0.9, res["dgrads"].max() * 1.1, 100)
        ax.plot(x_fit, np.polyval(c, x_fit), "k--", alpha=0.3)

        ax.set_xlabel("∫(dδ/dz)² dz", fontsize=10)
        ax.set_ylabel("γ_exp [erg/cm²]", fontsize=10)
        short = scheme.split("(")[0].strip()
        ax.set_title(f"({chr(97+idx)}) {short}\nr={res['r_pearson']:.3f}, "
                     f"LOO R²={res['r2_loo']:.3f}", fontsize=10)
        ax.grid(alpha=0.3)

    # Bottom left: d_fraction comparison bar chart
    ax = axes[1, 0]
    x_pos = np.arange(len(names))
    w = 0.25
    for idx, (scheme, d_frac) in enumerate(D_FRACTIONS.items()):
        vals = [d_frac[n] for n in names]
        short = scheme.split("(")[0].strip()
        ax.bar(x_pos + idx * w, vals, w, label=short,
               color=colors_scheme[idx], alpha=0.7, edgecolor="black", linewidth=0.3)
    ax.set_xticks(x_pos + w)
    ax.set_xticklabels(names, rotation=45, fontsize=8)
    ax.set_ylabel("d_fraction", fontsize=11)
    ax.set_title("(d) d_fraction Values by Scheme", fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3, axis="y")

    # Bottom center: summary metrics
    ax = axes[1, 1]
    ax.axis("off")
    metrics = ["Pearson r", "Spearman ρ", "LOO R²", "Partial r\n(control n_bar)",
               "# free params"]
    table_data = [["Metric"] + [s.split("(")[0].strip() for s in schemes] + ["n_bar only"]]
    for m_idx, metric in enumerate(metrics):
        row = [metric]
        for scheme, res in all_results.items():
            if m_idx == 0:
                row.append(f"{res['r_pearson']:.3f}")
            elif m_idx == 1:
                row.append(f"{res['r_spearman']:.3f}")
            elif m_idx == 2:
                row.append(f"{res['r2_loo']:.3f}")
            elif m_idx == 3:
                row.append(f"{res['r_partial']:.3f}")
            elif m_idx == 4:
                n_free = sum(1 for v in D_FRACTIONS[scheme].values() if v > 0)
                row.append(f"{n_free}")
        # n_bar only column
        if m_idx == 0:
            row.append(f"{r_nbar:.3f}")
        elif m_idx == 1:
            row.append("1.000")
        elif m_idx == 4:
            row.append("0")
        else:
            row.append("—")
        table_data.append(row)

    table = ax.table(cellText=table_data, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.6)
    for j in range(5):
        table[0, j].set_facecolor("#ddd")
        table[0, j].set_text_props(fontweight="bold")
    ax.set_title("(e) Summary Metrics", fontsize=10, pad=20)

    # Bottom right: LOO R² comparison
    ax = axes[1, 2]
    labels = [s.split("(")[0].strip() for s in schemes] + ["n_bar\nonly"]
    r2_vals = [all_results[s]["r2_loo"] for s in schemes]
    # Compute n_bar LOO R²
    gammas_arr = all_results["Original (ad-hoc)"]["gammas"]
    nbars_arr = all_results["Original (ad-hoc)"]["n_bars"]
    N = len(gammas_arr)
    y_pred_loo = np.zeros(N)
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        c = np.polyfit(nbars_arr[mask], gammas_arr[mask], 1)
        y_pred_loo[i] = np.polyval(c, nbars_arr[i])
    r2_nbar_loo = 1.0 - np.sum((gammas_arr - y_pred_loo)**2) / np.sum((gammas_arr - gammas_arr.mean())**2)
    r2_vals.append(r2_nbar_loo)

    bar_colors = colors_scheme + ["gray"]
    ax.barh(labels, r2_vals, color=bar_colors, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("LOO R²", fontsize=11)
    ax.set_title("(f) Cross-validated Predictive Power", fontsize=10)
    ax.set_xlim(0, 1.0)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(r2_vals):
        ax.text(v + 0.01, i, f"{v:.3f}", va="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test3_dfraction_literature.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test3_dfraction_literature.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
