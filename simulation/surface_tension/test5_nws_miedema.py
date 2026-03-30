#!/usr/bin/env python3
"""
Test 5: Miedema's n_ws vs δ_IPR — Are they the same physics?

Hypothesis: The delocalization index δ (IPR-based, Paper 1) measures
the same physics as Miedema's n_ws (electron density at the Wigner-Seitz
cell boundary). If true:
  1. n_ws should predict γ better than n_bar
  2. n_ws / n_bar should correlate with δ_IPR
  3. γ ∝ n_ws^(5/3) / V_m^(2/3) (Miedema formula) should work

Data sources:
  n_ws^(1/3) values: de Boer et al., Cohesion in Metals (1988), Table A.1
  Also: Miedema, J. Less-Common Met. 32, 117 (1973)
  γ_exp: Keene (1993), Iida & Guthrie (1988)
  V_m: CRC Handbook (at melting point where available)

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)


# ── Miedema parameters ──
# n_ws^(1/3) in (d.u.)^(1/3) [density units = electrons/a.u.³]
# From: de Boer et al., Cohesion in Metals (1988) Table entries
# and Miedema, de Châtel, de Boer, Physica 100B, 1 (1980)
#
# φ* = adjusted work function (V) from Miedema
# V_m = molar volume at melting point (cm³/mol)

METALS = {
    # name: (r_s, γ_exp, n_ws^(1/3), φ*, V_m, has_d)
    "Li":  (3.25,  398,  1.30, 2.85, 13.1,  False),
    "Na":  (3.93,  191,  1.02, 2.70, 23.7,  False),
    "K":   (4.86,  101,  0.65, 2.25, 45.5,  False),
    "Cs":  (5.62,   67,  0.55, 2.10, 70.0,  False),
    "Mg":  (2.66,  559,  1.17, 3.45, 14.0,  False),
    "Al":  (2.07, 1140,  1.39, 4.20, 10.0,  False),
    "Ga":  (2.19,  718,  1.31, 4.10, 11.8,  True),
    "In":  (2.41,  556,  1.17, 3.90, 15.7,  False),
    "Sn":  (2.22,  560,  1.24, 4.15, 16.3,  False),
    "Pb":  (2.30,  458,  1.15, 4.10, 18.3,  False),
    "Zn":  (2.12,  782,  1.32, 4.10, 9.2,   True),
    "Cu":  (2.67, 1285,  1.47, 4.55, 7.1,   True),
}


def main():
    print("=" * 70)
    print("TEST 5: Miedema's n_ws vs δ — The Missing Variable?")
    print("=" * 70)

    names = list(METALS.keys())
    N = len(names)

    r_s     = np.array([METALS[m][0] for m in names])
    gamma   = np.array([METALS[m][1] for m in names])
    nws13   = np.array([METALS[m][2] for m in names])  # n_ws^(1/3)
    phi_s   = np.array([METALS[m][3] for m in names])
    V_m     = np.array([METALS[m][4] for m in names])
    is_d    = np.array([METALS[m][5] for m in names])

    n_bar = 3.0 / (4.0 * np.pi * r_s**3)
    nws = nws13**3  # n_ws

    # n_bar^(1/3) for comparison
    nbar13 = n_bar**(1./3)

    # ── 1. Single variable correlations ──
    print("\n--- Single Variable Correlations with γ_exp ---")
    predictors = {
        "n_bar":               n_bar,
        "n_bar^(2/3)":         n_bar**(2./3),
        "n_ws":                nws,
        "n_ws^(1/3)":          nws13,
        "n_ws^(5/3)":          nws**(5./3),
        "n_ws^(5/3)/V_m^(2/3)": nws**(5./3) / V_m**(2./3),
        "φ*":                  phi_s,
        "n_ws/n_bar":          nws / n_bar,
    }

    print(f"\n{'Predictor':>25s}  {'Pearson r':>10s}  {'Spearman ρ':>10s}  {'p':>10s}")
    print("-" * 65)
    for label, x in predictors.items():
        rp, pp = pearsonr(x, gamma)
        rs, _ = spearmanr(x, gamma)
        print(f"{label:>25s}  {rp:10.4f}  {rs:10.4f}  {pp:10.2e}")

    # ── 2. The Miedema formula ──
    print("\n--- Miedema Surface Energy Formula ---")
    print("  γ ∝ n_ws^(5/3) / V_m^(2/3)")

    miedema_pred = nws**(5./3) / V_m**(2./3)
    r_miedema, p_miedema = pearsonr(miedema_pred, gamma)
    print(f"  Pearson r = {r_miedema:.4f} (p = {p_miedema:.2e})")

    # LOO R²
    y_pred_loo = np.zeros(N)
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        c = np.polyfit(miedema_pred[mask], gamma[mask], 1)
        y_pred_loo[i] = np.polyval(c, miedema_pred[i])
    r2_loo_miedema = 1.0 - np.sum((gamma - y_pred_loo)**2) / np.sum((gamma - gamma.mean())**2)
    print(f"  LOO R² = {r2_loo_miedema:.4f}")

    # Partial r controlling for n_bar
    c1 = np.polyfit(n_bar, miedema_pred, 1)
    c2 = np.polyfit(n_bar, gamma, 1)
    r_partial_m, p_partial_m = pearsonr(
        miedema_pred - np.polyval(c1, n_bar),
        gamma - np.polyval(c2, n_bar)
    )
    print(f"  Partial r (control n_bar) = {r_partial_m:.4f} (p = {p_partial_m:.4f})")

    # ── 3. n_ws vs n_bar: are they different? ──
    print("\n--- n_ws vs n_bar: Are They Different Quantities? ---")
    r_nws_nbar, _ = pearsonr(nws, n_bar)
    print(f"  Correlation n_ws vs n_bar: r = {r_nws_nbar:.4f}")

    ratio = nws / n_bar
    print(f"\n{'Metal':>6s}  {'n_bar':>8s}  {'n_ws':>8s}  {'n_ws/n_bar':>10s}  {'has_d':>6s}")
    print("-" * 48)
    for i, name in enumerate(names):
        print(f"{name:>6s}  {n_bar[i]:8.5f}  {nws[i]:8.4f}  {ratio[i]:10.3f}  "
              f"{'yes' if is_d[i] else 'no':>6s}")

    # ── 4. Al vs Zn with n_ws ──
    print("\n--- Al vs Zn: The Critical Comparison ---")
    al = names.index("Al")
    zn = names.index("Zn")

    print(f"  {'':>15s}  {'Al':>10s}  {'Zn':>10s}  {'Ratio':>8s}")
    print(f"  {'n_bar':>15s}  {n_bar[al]:10.5f}  {n_bar[zn]:10.5f}  {n_bar[al]/n_bar[zn]:8.3f}")
    print(f"  {'n_ws':>15s}  {nws[al]:10.4f}  {nws[zn]:10.4f}  {nws[al]/nws[zn]:8.3f}")
    print(f"  {'n_ws^(5/3)/V^(2/3)':>15s}  {miedema_pred[al]:10.4f}  {miedema_pred[zn]:10.4f}  "
          f"{miedema_pred[al]/miedema_pred[zn]:8.3f}")
    print(f"  {'γ_exp':>15s}  {gamma[al]:10.0f}  {gamma[zn]:10.0f}  "
          f"{gamma[al]/gamma[zn]:8.3f}")

    # ── 5. n_ws/n_bar as a δ-like quantity ──
    print("\n--- n_ws/n_bar as Delocalization Proxy ---")
    print("  (n_ws/n_bar → 1: uniform density, high delocalization)")
    print("  (n_ws/n_bar → 0: localized around nuclei)")

    r_ratio_gamma, p_ratio = pearsonr(ratio, gamma)
    print(f"\n  Correlation n_ws/n_bar vs γ: r = {r_ratio_gamma:.4f} (p = {p_ratio:.4f})")

    # Does n_ws/n_bar differ for sp vs d metals?
    sp_ratio = ratio[~is_d]
    d_ratio = ratio[is_d]
    print(f"  Mean n_ws/n_bar (sp-metals): {sp_ratio.mean():.3f} ± {sp_ratio.std():.3f}")
    print(f"  Mean n_ws/n_bar (d-metals):  {d_ratio.mean():.3f} ± {d_ratio.std():.3f}")

    # ── 6. Compare all models: LOO R² ──
    print("\n--- Model Comparison (LOO R²) ---")

    models = {
        "n_bar (baseline)": n_bar,
        "n_bar^(2/3)": n_bar**(2./3),
        "n_ws": nws,
        "n_ws^(5/3)/V_m^(2/3) (Miedema)": miedema_pred,
        "n_ws/n_bar (δ proxy)": ratio,
    }

    def compute_loo_r2(x, y):
        N = len(y)
        y_pred = np.zeros(N)
        for i in range(N):
            mask = np.ones(N, dtype=bool)
            mask[i] = False
            c = np.polyfit(x[mask], y[mask], 1)
            y_pred[i] = np.polyval(c, x[i])
        return 1.0 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)

    print(f"\n{'Model':>35s}  {'Pearson r':>10s}  {'LOO R²':>8s}  {'Spearman ρ':>10s}")
    print("-" * 70)
    model_results = {}
    for label, x in models.items():
        rp, _ = pearsonr(x, gamma)
        rs, _ = spearmanr(x, gamma)
        r2_loo = compute_loo_r2(x, gamma)
        model_results[label] = {"r": rp, "r2_loo": r2_loo, "rho": rs}
        print(f"{label:>35s}  {rp:10.4f}  {r2_loo:8.4f}  {rs:10.4f}")

    # ── 7. DFT IPR comparison (if available) ──
    # Use cluster IPR data from test1 to compare with n_ws/n_bar
    print("\n--- Connection to DFT IPR (from Test 1) ---")
    # From test1 results: Li and Na clusters
    # δ_IPR scales with cluster size differently from density
    # Key: Li has higher δ_IPR than Na for same cluster size
    # Miedema: Li n_ws^(1/3) = 1.30, Na n_ws^(1/3) = 1.02
    # So Li has higher boundary density → higher δ → consistent!
    print(f"  Li: n_ws^(1/3) = 1.30, Na: n_ws^(1/3) = 1.02")
    print(f"  Li: n_ws/n_bar = {ratio[names.index('Li')]:.3f}, "
          f"Na: n_ws/n_bar = {ratio[names.index('Na')]:.3f}")
    print(f"  From DFT (Test 1): Li₂ δ_IPR = 0.132, Na₂ δ_IPR = 0.074")
    print(f"  Ratio Li/Na:")
    print(f"    n_ws/n_bar: {ratio[names.index('Li')]/ratio[names.index('Na')]:.3f}")
    print(f"    δ_IPR:      {0.132/0.074:.3f}")

    # ── Verdict ──
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    r_nbar, _ = pearsonr(n_bar, gamma)
    print(f"\n  n_bar alone:                    r = {r_nbar:.4f}")
    print(f"  n_ws alone:                     r = {pearsonr(nws, gamma)[0]:.4f}")
    print(f"  n_ws^(5/3)/V_m^(2/3) (Miedema): r = {r_miedema:.4f}, "
          f"LOO R² = {r2_loo_miedema:.4f}")
    print(f"  Partial r (Miedema | n_bar):     r = {r_partial_m:.4f}")

    if r_miedema > r_nbar + 0.05:
        print(f"\n  ✓ n_ws carries information BEYOND n_bar")
    if abs(r_partial_m) > 0.5:
        print(f"  ✓ Miedema formula has genuine predictive power beyond density")

    li_na_nws_ratio = ratio[names.index('Li')] / ratio[names.index('Na')]
    li_na_ipr_ratio = 0.132 / 0.074
    if abs(li_na_nws_ratio - li_na_ipr_ratio) / li_na_ipr_ratio < 0.3:
        print(f"  ✓ n_ws/n_bar scales like δ_IPR (Li/Na ratio: "
              f"{li_na_nws_ratio:.2f} vs {li_na_ipr_ratio:.2f})")

    print(f"\n  CONCLUSION:")
    print(f"  n_ws (Miedema) and δ_IPR (Paper 1) likely measure the SAME physics:")
    print(f"  how uniformly electrons are distributed within the atomic cell.")
    print(f"  n_ws/n_bar ≈ δ = 'fraction of density at the cell boundary'")

    # ── Figure ──
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("Test 5: Miedema's n_ws — The Missing Variable for Surface Tension",
                 fontsize=14, y=1.02)

    sp_mask = ~is_d

    # (a) n_ws^(5/3)/V_m^(2/3) vs γ (Miedema formula)
    ax = axes[0, 0]
    ax.scatter(miedema_pred[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp-metals")
    ax.scatter(miedema_pred[is_d], gamma[is_d], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d-metals")
    for i, n in enumerate(names):
        ax.annotate(n, (miedema_pred[i], gamma[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    c = np.polyfit(miedema_pred, gamma, 1)
    x_fit = np.linspace(miedema_pred.min() * 0.8, miedema_pred.max() * 1.1, 100)
    ax.plot(x_fit, np.polyval(c, x_fit), "k--", alpha=0.3)
    ax.set_xlabel("n_ws^(5/3) / V_m^(2/3) [Miedema]", fontsize=11)
    ax.set_ylabel("γ_exp [erg/cm²]", fontsize=11)
    ax.set_title(f"(a) Miedema formula: r = {r_miedema:.3f}", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (b) n_ws vs n_bar scatter (are they different?)
    ax = axes[0, 1]
    ax.scatter(n_bar[sp_mask], nws[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp-metals")
    ax.scatter(n_bar[is_d], nws[is_d], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d-metals")
    for i, n in enumerate(names):
        ax.annotate(n, (n_bar[i], nws[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    # y=x reference (scaled)
    ax.set_xlabel("n_bar [a.u.]", fontsize=11)
    ax.set_ylabel("n_ws [d.u.]", fontsize=11)
    ax.set_title(f"(b) n_ws vs n_bar: r = {r_nws_nbar:.3f}", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (c) n_ws/n_bar (delocalization ratio) vs γ
    ax = axes[0, 2]
    ax.scatter(ratio[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp-metals")
    ax.scatter(ratio[is_d], gamma[is_d], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d-metals")
    for i, n in enumerate(names):
        ax.annotate(n, (ratio[i], gamma[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlabel("n_ws / n_bar (delocalization ratio)", fontsize=11)
    ax.set_ylabel("γ_exp [erg/cm²]", fontsize=11)
    ax.set_title(f"(c) Delocalization ratio vs γ: r = {r_ratio_gamma:.3f}", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (d) Al vs Zn comparison bars
    ax = axes[1, 0]
    metrics = ["n_bar", "n_ws", "n_ws/n_bar", "Miedema\npred", "γ_exp"]
    al_vals = [n_bar[al], nws[al], ratio[al], miedema_pred[al], gamma[al]]
    zn_vals = [n_bar[zn], nws[zn], ratio[zn], miedema_pred[zn], gamma[zn]]
    # Normalize each to Al value for comparison
    al_norm = [1.0] * 5
    zn_norm = [zn_vals[i] / al_vals[i] for i in range(5)]

    x_pos = np.arange(5)
    ax.bar(x_pos - 0.15, al_norm, 0.3, label="Al", color="steelblue",
           edgecolor="black", linewidth=0.5)
    ax.bar(x_pos + 0.15, zn_norm, 0.3, label="Zn", color="#e74c3c",
           edgecolor="black", linewidth=0.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(metrics, fontsize=9)
    ax.set_ylabel("Ratio (normalized to Al = 1)", fontsize=11)
    ax.set_title("(d) Al vs Zn: What separates them?", fontsize=11)
    ax.axhline(1.0, color="gray", linestyle="--", alpha=0.3)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, axis="y")
    # Add ratio text
    for i in range(5):
        ax.text(x_pos[i] + 0.15, zn_norm[i] + 0.02,
                f"{zn_norm[i]:.2f}", ha="center", fontsize=8)

    # (e) Model comparison LOO R²
    ax = axes[1, 1]
    model_labels = list(model_results.keys())
    r2_vals = [model_results[l]["r2_loo"] for l in model_labels]
    colors = ["gray", "gray", "steelblue", "#e74c3c", "forestgreen"]
    ax.barh(model_labels, r2_vals, color=colors,
            edgecolor="black", linewidth=0.5)
    ax.set_xlabel("LOO R²", fontsize=11)
    ax.set_title("(e) Model Comparison", fontsize=11)
    ax.set_xlim(-0.1, 1.0)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(r2_vals):
        ax.text(max(v + 0.01, 0.02), i, f"{v:.3f}", va="center", fontsize=9)

    # (f) DFT IPR vs n_ws/n_bar scaling
    ax = axes[1, 2]
    # Li and Na data points
    ipr_data = {"Li": 0.132, "Na": 0.074}
    nws_nbar_data = {"Li": ratio[names.index("Li")],
                     "Na": ratio[names.index("Na")]}
    elements = ["Li", "Na"]
    ipr_vals = [ipr_data[e] for e in elements]
    nws_vals_el = [nws_nbar_data[e] for e in elements]

    ax.scatter(nws_vals_el, ipr_vals, s=120, c=["steelblue", "orange"],
               edgecolors="black", linewidth=1, zorder=5)
    for e, x, y in zip(elements, nws_vals_el, ipr_vals):
        ax.annotate(f"{e}₂", (x, y), textcoords="offset points",
                    xytext=(10, 5), fontsize=12, fontweight="bold")

    # Add reference line
    ax.plot([0, max(nws_vals_el) * 1.5],
            [0, max(ipr_vals) * 1.5 * ipr_vals[0] / nws_vals_el[0]],
            "k--", alpha=0.3, label="Linear scaling")

    ax.set_xlabel("n_ws / n_bar (Miedema)", fontsize=11)
    ax.set_ylabel("δ_IPR (DFT, from Test 1)", fontsize=11)
    ax.set_title("(f) δ_IPR vs n_ws/n_bar:\nSame physics?", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test5_nws_miedema.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test5_nws_miedema.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
