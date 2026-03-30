#!/usr/bin/env python3
"""
Test 6: n_ws × δ — The two-factor model for surface tension.

Paper 1 structure: optical response = δ × D_eff
  - δ = how delocalized (quality of electrons)
  - D_eff = effective dimensionality (geometric factor)

Proposed Paper 2 structure: γ = f(n_ws, δ)
  - n_ws = how many electrons at boundary (quantity)
  - δ = how freely they can redistribute (quality)

These are ORTHOGONAL:
  - n_ws alone: r = 0.922 with γ
  - n_ws/n_bar alone: r ≈ 0 with γ
  → They carry independent information
  → Combining them should capture what neither does alone

For δ proxy, we test several options since we don't have DFT IPR
for all 12 metals:
  1. 1/IPR from tight-binding (Paper 1 style) — not available for metals
  2. DOS-weighted effective d_fraction (from Test 3 — worked well)
  3. Inverse of d-band localization energy (1/ε_d from Fermi level)
  4. n_ws^(1/3) / r_s (empirical, dimensionally suggestive)

The key test: does n_ws × δ_proxy beat n_ws alone?
And specifically: does it resolve Al vs Zn?

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)


# ── Data ──
# n_ws^(1/3) from Miedema; d_band_dist = distance of d-band center
# below E_F (eV) from Papaconstantopoulos (1986) / literature
# φ* from Miedema
# V_m in cm³/mol

METALS = {
    #        r_s    γ_exp  n_ws^(1/3)  φ*    V_m   d_band_dist  f_d_eff
    #                                              (eV below EF) (DOS@EF)
    "Li":  (3.25,  398,   1.30,      2.85, 13.1,  None,        0.00),
    "Na":  (3.93,  191,   1.02,      2.70, 23.7,  None,        0.00),
    "K":   (4.86,  101,   0.65,      2.25, 45.5,  None,        0.00),
    "Cs":  (5.62,   67,   0.55,      2.10, 70.0,  None,        0.00),
    "Mg":  (2.66,  559,   1.17,      3.45, 14.0,  None,        0.00),
    "Al":  (2.07, 1140,   1.39,      4.20, 10.0,  None,        0.00),
    "Ga":  (2.19,  718,   1.31,      4.10, 11.8,  15.0,        0.02),
    "In":  (2.41,  556,   1.17,      3.90, 15.7,  15.0,        0.01),
    "Sn":  (2.22,  560,   1.24,      4.15, 16.3,  20.0,        0.01),
    "Pb":  (2.30,  458,   1.15,      4.10, 18.3,  15.0,        0.01),
    "Zn":  (2.12,  782,   1.32,      4.10,  9.2,   9.0,        0.05),
    "Cu":  (2.67, 1285,   1.47,      4.55,  7.1,   2.0,        0.80),
}


def compute_loo_r2(x, y):
    """Leave-one-out cross-validated R²."""
    N = len(y)
    y_pred = np.zeros(N)
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        c = np.polyfit(x[mask], y[mask], 1)
        y_pred[i] = np.polyval(c, x[i])
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    return 1.0 - ss_res / ss_tot


def compute_loo_r2_2var(x1, x2, y):
    """LOO R² for two-variable linear model."""
    N = len(y)
    y_pred = np.zeros(N)
    X = np.column_stack([x1, x2, np.ones(N)])
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        c, _, _, _ = np.linalg.lstsq(X[mask], y[mask], rcond=None)
        y_pred[i] = X[i] @ c
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    return 1.0 - ss_res / ss_tot, y_pred


def main():
    print("=" * 70)
    print("TEST 6: n_ws × δ — The Two-Factor Model")
    print("Surface tension = boundary density × delocalization quality")
    print("=" * 70)

    names = list(METALS.keys())
    N = len(names)

    r_s     = np.array([METALS[m][0] for m in names])
    gamma   = np.array([METALS[m][1] for m in names])
    nws13   = np.array([METALS[m][2] for m in names])
    phi_s   = np.array([METALS[m][3] for m in names])
    V_m     = np.array([METALS[m][4] for m in names])
    d_dist  = np.array([METALS[m][5] if METALS[m][5] is not None else 0.0
                        for m in names])
    f_d_eff = np.array([METALS[m][6] for m in names])

    n_bar = 3.0 / (4.0 * np.pi * r_s**3)
    nws = nws13**3

    # ── Construct δ proxies ──
    # For sp-metals: δ ≈ 1 (electrons are free-electron-like)
    # For d-metals: δ < 1 (d-electrons are more localized)

    # Proxy A: "sp-character" = 1 - f_d_eff
    delta_A = 1.0 - f_d_eff
    # This means Al=1.0, Cu=0.2, Zn=0.95, etc.

    # Proxy B: effective delocalization from d-band distance
    # If d-band is far below E_F → electrons at E_F are sp-like → δ high
    # If d-band straddles E_F → mixed character → δ lower
    # δ_B = 1 for sp-metals, exp(-1/d_dist) for d-metals
    delta_B = np.ones(N)
    has_d = d_dist > 0
    delta_B[has_d] = 1.0 - np.exp(-d_dist[has_d] / 5.0)
    # Cu (d_dist=2): δ = 1-exp(-0.4) = 0.33
    # Zn (d_dist=9): δ = 1-exp(-1.8) = 0.83

    # Proxy C: φ*/φ*_max as "how metallic" (work function reflects surface dipole)
    delta_C = phi_s / phi_s.max()

    # Proxy D: n_ws^(1/3) × V_m^(1/3) (dimensionless, geometric)
    # This combines boundary density with atomic size
    delta_D = nws13 * V_m**(1./3)

    # ── Test all product models: n_ws^α × δ^β ──
    print("\n--- Product Models: γ ∝ n_ws^(5/3) × δ_proxy / V_m^(2/3) ---")
    print("(Miedema form, extended with δ factor)")

    miedema_base = nws**(5./3) / V_m**(2./3)

    products = {
        "Miedema (n_ws only)":        miedema_base,
        "Miedema × δ_A (sp-char)":    miedema_base * delta_A,
        "Miedema × δ_B (d-dist)":     miedema_base * delta_B,
        "Miedema × δ_C (φ-norm)":     miedema_base * delta_C,
        "n_ws × δ_A":                 nws * delta_A,
        "n_ws × δ_B":                 nws * delta_B,
        "n_ws^(5/3) × δ_A":           nws**(5./3) * delta_A,
        "n_ws^(5/3) × δ_B":           nws**(5./3) * delta_B,
    }

    print(f"\n{'Model':>30s}  {'r':>8s}  {'ρ':>8s}  {'LOO R²':>8s}  {'Partial r':>10s}")
    print("-" * 75)

    for label, x in products.items():
        rp, _ = pearsonr(x, gamma)
        rs, _ = spearmanr(x, gamma)
        r2_loo = compute_loo_r2(x, gamma)
        # Partial r controlling for n_ws alone
        c1 = np.polyfit(nws, x, 1)
        c2 = np.polyfit(nws, gamma, 1)
        rp_partial, _ = pearsonr(x - np.polyval(c1, nws),
                                  gamma - np.polyval(c2, nws))
        print(f"{label:>30s}  {rp:8.4f}  {rs:8.4f}  {r2_loo:8.4f}  {rp_partial:10.4f}")

    # ── Two-variable linear models ──
    print("\n--- Two-Variable Linear: γ = a×n_ws + b×δ + c ---")

    deltas = {
        "δ_A (sp-char)": delta_A,
        "δ_B (d-dist)": delta_B,
        "δ_C (φ-norm)": delta_C,
        "f_d_eff": f_d_eff,
    }

    for d_label, d_vals in deltas.items():
        r2_loo, y_pred = compute_loo_r2_2var(nws, d_vals, gamma)
        # Full R²
        X = np.column_stack([nws, d_vals, np.ones(N)])
        c, _, _, _ = np.linalg.lstsq(X, gamma, rcond=None)
        y_full = X @ c
        r2_full = 1.0 - np.sum((gamma - y_full)**2) / np.sum((gamma - gamma.mean())**2)
        r_full = np.sqrt(r2_full) if r2_full > 0 else 0
        print(f"  n_ws + {d_label:>15s}: R²={r2_full:.4f}, LOO R²={r2_loo:.4f}, "
              f"coeffs=[{c[0]:.2f}, {c[1]:.2f}, {c[2]:.2f}]")

    # ── The key: n_ws and δ are orthogonal? ──
    print("\n--- Orthogonality Check ---")
    for d_label, d_vals in deltas.items():
        r_ortho, _ = pearsonr(nws, d_vals)
        print(f"  r(n_ws, {d_label:>15s}) = {r_ortho:.4f}")

    # ── Al vs Zn with two-factor model ──
    print("\n--- Al vs Zn: Two-Factor Decomposition ---")
    al = names.index("Al")
    zn = names.index("Zn")

    print(f"\n  {'':>20s}  {'Al':>10s}  {'Zn':>10s}  {'Al/Zn':>8s}")
    print(f"  {'n_ws (quantity)':>20s}  {nws[al]:10.4f}  {nws[zn]:10.4f}  "
          f"{nws[al]/nws[zn]:8.3f}")
    print(f"  {'δ_A (sp-character)':>20s}  {delta_A[al]:10.4f}  {delta_A[zn]:10.4f}  "
          f"{delta_A[al]/delta_A[zn]:8.3f}")
    print(f"  {'δ_B (d-band dist)':>20s}  {delta_B[al]:10.4f}  {delta_B[zn]:10.4f}  "
          f"{delta_B[al]/delta_B[zn]:8.3f}")
    print(f"  {'n_ws × δ_A':>20s}  {(nws*delta_A)[al]:10.4f}  {(nws*delta_A)[zn]:10.4f}  "
          f"{(nws*delta_A)[al]/(nws*delta_A)[zn]:8.3f}")
    print(f"  {'n_ws × δ_B':>20s}  {(nws*delta_B)[al]:10.4f}  {(nws*delta_B)[zn]:10.4f}  "
          f"{(nws*delta_B)[al]/(nws*delta_B)[zn]:8.3f}")
    print(f"  {'γ_exp':>20s}  {gamma[al]:10.0f}  {gamma[zn]:10.0f}  "
          f"{gamma[al]/gamma[zn]:8.3f}")

    # ── Best model: detailed predictions ──
    print("\n--- Best Product Model: Detailed Predictions ---")
    # Find best
    best_label = None
    best_r2 = -1
    for label, x in products.items():
        r2 = compute_loo_r2(x, gamma)
        if r2 > best_r2:
            best_r2 = r2
            best_label = label

    best_x = products[best_label]
    c = np.polyfit(best_x, gamma, 1)
    gamma_pred = np.polyval(c, best_x)
    r_best, _ = pearsonr(best_x, gamma)

    print(f"\n  Model: {best_label}")
    print(f"  r = {r_best:.4f}, LOO R² = {best_r2:.4f}")
    print(f"\n  {'Metal':>6s}  {'γ_exp':>8s}  {'γ_pred':>8s}  {'Error%':>8s}")
    print(f"  {'-'*35}")
    for i, name in enumerate(names):
        err_pct = 100 * (gamma[i] - gamma_pred[i]) / gamma[i]
        print(f"  {name:>6s}  {gamma[i]:8.0f}  {gamma_pred[i]:8.0f}  {err_pct:7.1f}%")
    rmse = np.sqrt(np.mean((gamma - gamma_pred)**2))
    print(f"\n  RMSE = {rmse:.0f} erg/cm²")

    # ── Verdict ──
    r_nws_only, _ = pearsonr(nws, gamma)
    r2_nws_only = compute_loo_r2(nws, gamma)

    print(f"\n{'='*70}")
    print("VERDICT: Does adding δ to n_ws improve prediction?")
    print(f"{'='*70}")
    print(f"  n_ws alone:        r = {r_nws_only:.4f}, LOO R² = {r2_nws_only:.4f}")
    print(f"  Best product:      r = {r_best:.4f}, LOO R² = {best_r2:.4f}")
    print(f"  Improvement in LOO R²: {best_r2 - r2_nws_only:+.4f}")

    if best_r2 > r2_nws_only + 0.02:
        print(f"\n  ✓ YES: δ adds genuine predictive power beyond n_ws")
        print(f"    → Surface tension = f(n_ws, δ) is a better model than n_ws alone")
        print(f"    → This parallels Paper 1: optical = f(δ, D_eff)")
    else:
        print(f"\n  △ MARGINAL: δ adds little beyond n_ws")

    # ── Figure ──
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("Test 6: Surface Tension = Boundary Density × Delocalization Quality",
                 fontsize=14, y=1.02)

    sp_mask = f_d_eff == 0
    d_mask = ~sp_mask

    # (a) n_ws alone vs γ
    ax = axes[0, 0]
    ax.scatter(nws[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp")
    ax.scatter(nws[d_mask], gamma[d_mask], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d")
    for i, n in enumerate(names):
        ax.annotate(n, (nws[i], gamma[i]),
                    textcoords="offset points", xytext=(4, 4), fontsize=8)
    c_fit = np.polyfit(nws, gamma, 1)
    x_fit = np.linspace(0, nws.max() * 1.1, 100)
    ax.plot(x_fit, np.polyval(c_fit, x_fit), "k--", alpha=0.3)
    ax.set_xlabel("n_ws (boundary density)", fontsize=11)
    ax.set_ylabel("γ_exp [erg/cm²]", fontsize=11)
    ax.set_title(f"(a) n_ws alone: r={pearsonr(nws, gamma)[0]:.3f}", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (b) δ_B alone vs γ
    ax = axes[0, 1]
    ax.scatter(delta_B[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp")
    ax.scatter(delta_B[d_mask], gamma[d_mask], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d")
    for i, n in enumerate(names):
        ax.annotate(n, (delta_B[i], gamma[i]),
                    textcoords="offset points", xytext=(4, 4), fontsize=8)
    r_dB, _ = pearsonr(delta_B, gamma)
    ax.set_xlabel("δ_B (d-band distance proxy)", fontsize=11)
    ax.set_ylabel("γ_exp [erg/cm²]", fontsize=11)
    ax.set_title(f"(b) δ alone: r={r_dB:.3f}", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (c) n_ws × δ_B vs γ (the product)
    product_B = nws * delta_B
    r_prod, _ = pearsonr(product_B, gamma)
    ax = axes[0, 2]
    ax.scatter(product_B[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp")
    ax.scatter(product_B[d_mask], gamma[d_mask], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d")
    for i, n in enumerate(names):
        ax.annotate(n, (product_B[i], gamma[i]),
                    textcoords="offset points", xytext=(4, 4), fontsize=8)
    c_fit = np.polyfit(product_B, gamma, 1)
    x_fit = np.linspace(0, product_B.max() * 1.1, 100)
    ax.plot(x_fit, np.polyval(c_fit, x_fit), "k--", alpha=0.3)
    ax.set_xlabel("n_ws × δ_B", fontsize=11)
    ax.set_ylabel("γ_exp [erg/cm²]", fontsize=11)
    ax.set_title(f"(c) n_ws × δ: r={r_prod:.3f}", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (d) Orthogonality diagram: n_ws vs δ_B colored by γ
    ax = axes[1, 0]
    sc = ax.scatter(nws, delta_B, s=120, c=gamma, cmap="hot",
                    edgecolors="black", linewidth=0.5, zorder=5)
    for i, n in enumerate(names):
        ax.annotate(n, (nws[i], delta_B[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=9)
    plt.colorbar(sc, ax=ax, label="γ_exp [erg/cm²]")
    ax.set_xlabel("n_ws (quantity: boundary density)", fontsize=11)
    ax.set_ylabel("δ_B (quality: delocalization)", fontsize=11)
    ax.set_title("(d) Orthogonal factors, colored by γ", fontsize=11)
    ax.grid(alpha=0.3)

    # (e) Al vs Zn decomposition
    ax = axes[1, 1]
    factors = ["n_ws", "δ_B", "n_ws×δ_B", "γ_exp"]
    al_v = [nws[al], delta_B[al], product_B[al], gamma[al]]
    zn_v = [nws[zn], delta_B[zn], product_B[zn], gamma[zn]]
    # Normalize each pair to Al=1
    al_norm = [1.0] * 4
    zn_norm = [zn_v[i] / al_v[i] for i in range(4)]

    x_pos = np.arange(4)
    ax.bar(x_pos - 0.15, al_norm, 0.3, label="Al", color="steelblue",
           edgecolor="black", linewidth=0.5)
    ax.bar(x_pos + 0.15, zn_norm, 0.3, label="Zn", color="#e74c3c",
           edgecolor="black", linewidth=0.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(factors, fontsize=10)
    ax.set_ylabel("Ratio (Al = 1)", fontsize=11)
    ax.set_title("(e) Al vs Zn decomposition", fontsize=11)
    ax.axhline(1.0, color="gray", linestyle="--", alpha=0.3)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, axis="y")
    for i in range(4):
        ax.text(x_pos[i] + 0.15, zn_norm[i] + 0.02,
                f"{zn_norm[i]:.3f}", ha="center", fontsize=9)

    # (f) Model comparison
    ax = axes[1, 2]
    comparison = {
        "n_bar": compute_loo_r2(n_bar, gamma),
        "n_ws": compute_loo_r2(nws, gamma),
        "Miedema\nn_ws^(5/3)/V^(2/3)": compute_loo_r2(nws**(5./3)/V_m**(2./3), gamma),
        "n_ws × δ_A\n(sp-character)": compute_loo_r2(nws * delta_A, gamma),
        "n_ws × δ_B\n(d-band dist)": compute_loo_r2(nws * delta_B, gamma),
        "Miedema × δ_B": compute_loo_r2(nws**(5./3)/V_m**(2./3) * delta_B, gamma),
    }
    labels = list(comparison.keys())
    vals = list(comparison.values())
    colors = ["gray", "steelblue", "steelblue",
              "forestgreen", "forestgreen", "#e74c3c"]
    ax.barh(labels, vals, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("LOO R²", fontsize=11)
    ax.set_title("(f) Model Comparison (LOO R²)", fontsize=11)
    ax.set_xlim(-0.1, 1.0)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(vals):
        ax.text(max(v + 0.01, 0.02), i, f"{v:.3f}", va="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test6_nws_times_delta.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test6_nws_times_delta.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
