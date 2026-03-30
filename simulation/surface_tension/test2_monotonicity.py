#!/usr/bin/env python3
"""
Test 2: Monotonicity & residual analysis for jellium surface tension.

Critical question: Is the r=0.956 correlation between ∫(dδ/dz)² and γ_exp
just an artifact of both being monotonic functions of r_s?

Tests:
  (a) Spearman rank correlation (invariant to monotonic transformations)
  (b) Residuals of γ vs n_bar linear fit — does δ-gradient capture residual?
  (c) Leave-one-out cross-validation for r² stability
  (d) Comparison with trivial predictors (n_bar, n_bar^(2/3), r_s^(-4))
  (e) Partial correlation: r(δ-grad, γ | n_bar)

If δ = n/n_bar, then ∫(dδ/dz)² = (1/n_bar²)∫(dn/dz)². This means
δ-gradient carries LESS information than n_bar alone (it divides by n_bar²).
This test checks whether the correlation is trivially explained.

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from scipy.integrate import trapezoid
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from jellium_surface import (
    METALS, compute_surface_energy, delta_gradient_integral, bulk_density,
    BOHR_TO_ANGSTROM, HARTREE_TO_ERG_PER_CM2,
)

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)


def main():
    print("=" * 70)
    print("TEST 2: Monotonicity & Residual Analysis")
    print("Is r=0.956 trivial?")
    print("=" * 70)

    # Compute all quantities for the 7 metals
    names = list(METALS.keys())
    r_s_vals = np.array([METALS[m]["r_s"] for m in names])
    gamma_exp = np.array([METALS[m]["gamma_exp"] for m in names])
    n_bar_vals = np.array([bulk_density(rs) for rs in r_s_vals])

    dgrad_vals = []
    for m in names:
        rs = METALS[m]["r_s"]
        _, z, n, delta, nb = compute_surface_energy(rs)
        dg = delta_gradient_integral(z, delta)
        dgrad_vals.append(dg)
    dgrad_vals = np.array(dgrad_vals)

    # ── (a) Spearman rank correlation ──
    print("\n--- (a) Spearman Rank Correlation ---")
    print("(Invariant to monotonic transformations)")
    print()

    predictors = {
        "n_bar":           n_bar_vals,
        "n_bar^(2/3)":     n_bar_vals**(2./3),
        "r_s^(-4)":        r_s_vals**(-4),
        "∫(dδ/dz)²":      dgrad_vals,
        "n_bar² × ∫(dδ/dz)²": n_bar_vals**2 * dgrad_vals,  # = ∫(dn/dz)²
    }

    print(f"{'Predictor':>25s}  {'Pearson r':>10s}  {'Spearman ρ':>10s}  {'p (Pearson)':>12s}")
    print("-" * 65)
    for label, x in predictors.items():
        rp, pp = pearsonr(x, gamma_exp)
        rs_corr, ps = spearmanr(x, gamma_exp)
        print(f"{label:>25s}  {rp:10.4f}  {rs_corr:10.4f}  {pp:12.2e}")

    # Key check: if Spearman is the same for all predictors,
    # the correlation is just monotonicity
    spearman_vals = [spearmanr(x, gamma_exp)[0] for x in predictors.values()]
    all_same_rank = len(set([f"{s:.4f}" for s in spearman_vals])) == 1
    print(f"\n  All Spearman ρ identical? → {all_same_rank}")
    if all_same_rank:
        print("  ⚠ ALL predictors have the same rank correlation.")
        print("    This means the data is purely monotonic in r_s.")
        print("    Pearson r differences reflect only nonlinearity, not physics.")

    # ── (b) Residual analysis ──
    print("\n--- (b) Residual Analysis ---")
    print("Does ∫(dδ/dz)² explain variance beyond n_bar?")

    # Linear fit: γ vs n_bar
    coeffs_nbar = np.polyfit(n_bar_vals, gamma_exp, 1)
    gamma_pred_nbar = np.polyval(coeffs_nbar, n_bar_vals)
    resid_nbar = gamma_exp - gamma_pred_nbar

    # Linear fit: γ vs ∫(dδ/dz)²
    coeffs_dgrad = np.polyfit(dgrad_vals, gamma_exp, 1)
    gamma_pred_dgrad = np.polyval(coeffs_dgrad, dgrad_vals)
    resid_dgrad = gamma_exp - gamma_pred_dgrad

    # Can δ-gradient explain residuals from n_bar fit?
    r_resid, p_resid = pearsonr(dgrad_vals, resid_nbar)
    print(f"  Correlation of ∫(dδ/dz)² with residuals(γ - γ_pred(n_bar)):")
    print(f"    r = {r_resid:.4f}, p = {p_resid:.4f}")

    # Analytical check: since δ = n/n_bar, ∫(dδ/dz)² = ∫(dn/dz)²/n_bar²
    # For exponential profile with decay q_TF:
    # ∫(dn/dz)² = n_bar² × q_TF/2
    # So ∫(dδ/dz)² = q_TF/2 ∝ n^(1/6) ∝ r_s^(-1/2)
    print(f"\n  Analytical check:")
    print(f"  Since δ = n/n_bar → ∫(dδ/dz)² = q_TF/2 ∝ n_bar^(1/6)")
    dgrad_analytical = np.array([bulk_density(rs)**(1./6) for rs in r_s_vals])
    r_ana, _ = pearsonr(dgrad_analytical, dgrad_vals)
    print(f"  Correlation between n_bar^(1/6) and actual ∫(dδ/dz)²: r = {r_ana:.4f}")

    # ── (c) Partial correlation ──
    print("\n--- (c) Partial Correlation ---")
    print("r(∫(dδ/dz)², γ | n_bar) = correlation after removing n_bar effect")

    # Partial correlation: regress both on n_bar, correlate residuals
    coeffs_dg_nb = np.polyfit(n_bar_vals, dgrad_vals, 1)
    resid_dg = dgrad_vals - np.polyval(coeffs_dg_nb, n_bar_vals)
    r_partial, p_partial = pearsonr(resid_dg, resid_nbar)
    print(f"  Partial r = {r_partial:.4f}, p = {p_partial:.4f}")
    if abs(r_partial) < 0.3:
        print("  ⚠ δ-gradient carries NO information beyond n_bar.")
    elif abs(r_partial) > 0.5:
        print("  ✓ δ-gradient carries information beyond n_bar.")
    else:
        print("  △ Weak partial correlation — marginal.")

    # ── (d) Leave-one-out cross-validation ──
    print("\n--- (d) Leave-One-Out Cross-Validation ---")
    N = len(gamma_exp)

    def loo_r2(x, y):
        """LOO cross-validated R²."""
        y_pred_loo = np.zeros(N)
        for i in range(N):
            mask = np.ones(N, dtype=bool)
            mask[i] = False
            c = np.polyfit(x[mask], y[mask], 1)
            y_pred_loo[i] = np.polyval(c, x[i])
        ss_res = np.sum((y - y_pred_loo)**2)
        ss_tot = np.sum((y - y.mean())**2)
        return 1.0 - ss_res / ss_tot

    r2_loo_nbar = loo_r2(n_bar_vals, gamma_exp)
    r2_loo_dgrad = loo_r2(dgrad_vals, gamma_exp)
    r2_loo_nbar23 = loo_r2(n_bar_vals**(2./3), gamma_exp)
    r2_loo_rs4 = loo_r2(r_s_vals**(-4), gamma_exp)
    r2_loo_dn2 = loo_r2(n_bar_vals**2 * dgrad_vals, gamma_exp)

    print(f"  {'Predictor':>25s}  {'LOO R²':>10s}")
    print(f"  {'-'*40}")
    print(f"  {'n_bar':>25s}  {r2_loo_nbar:10.4f}")
    print(f"  {'n_bar^(2/3)':>25s}  {r2_loo_nbar23:10.4f}")
    print(f"  {'r_s^(-4)':>25s}  {r2_loo_rs4:10.4f}")
    print(f"  {'∫(dδ/dz)²':>25s}  {r2_loo_dgrad:10.4f}")
    print(f"  {'∫(dn/dz)²':>25s}  {r2_loo_dn2:10.4f}")

    # ── (e) Summary verdict ──
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    if all_same_rank:
        print("FAIL: All predictors have identical rank correlation.")
        print("      The r=0.956 is due to monotonicity in r_s, not δ physics.")
    if abs(r_partial) < 0.3:
        print("FAIL: Partial correlation near zero — δ-gradient = n_bar repackaged.")
    if r2_loo_nbar > r2_loo_dgrad:
        print(f"FAIL: n_bar (LOO R²={r2_loo_nbar:.4f}) outperforms "
              f"∫(dδ/dz)² (LOO R²={r2_loo_dgrad:.4f})")
    print()

    # ── Figure ──
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Test 2: Is δ-Gradient Just a Monotonic Proxy for Electron Density?",
                 fontsize=14, y=1.02)

    # (a) All predictors vs γ (normalized)
    ax = axes[0, 0]
    for label, x in predictors.items():
        x_norm = (x - x.min()) / (x.max() - x.min() + 1e-30)
        g_norm = (gamma_exp - gamma_exp.min()) / (gamma_exp.max() - gamma_exp.min())
        ax.plot(x_norm, g_norm, "o-", markersize=6, label=label)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.3, label="y=x")
    ax.set_xlabel("Normalized predictor", fontsize=11)
    ax.set_ylabel("Normalized γ_exp", fontsize=11)
    ax.set_title("(a) All predictors collapse (monotonicity)", fontsize=11)
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(alpha=0.3)

    # (b) Residuals from n_bar fit
    ax = axes[0, 1]
    colors = ["#e74c3c" if n == "Al" or n == "Zn" else "#3498db" for n in names]
    ax.bar(names, resid_nbar, color=colors, edgecolor="black", linewidth=0.5)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("Residual γ_exp - γ_pred(n_bar) [erg/cm²]", fontsize=10)
    ax.set_title(f"(b) Residuals from n_bar linear fit", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    # Highlight Al-Zn
    if "Al" in names and "Zn" in names:
        al_idx = names.index("Al")
        zn_idx = names.index("Zn")
        ax.annotate(f"Al-Zn: Δn_bar={abs(n_bar_vals[al_idx]-n_bar_vals[zn_idx]):.5f}\n"
                    f"Δγ={abs(gamma_exp[al_idx]-gamma_exp[zn_idx])} erg/cm²",
                    xy=(0.5, 0.95), xycoords="axes fraction", fontsize=9, va="top",
                    bbox=dict(facecolor="lightyellow", alpha=0.8))

    # (c) Partial correlation scatter
    ax = axes[1, 0]
    ax.scatter(resid_dg, resid_nbar, s=80, c="steelblue", edgecolors="black", zorder=5)
    for i, n in enumerate(names):
        ax.annotate(n, (resid_dg[i], resid_nbar[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=9)
    ax.axhline(0, color="gray", linestyle="--", alpha=0.3)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.3)
    ax.set_xlabel("Residual ∫(dδ/dz)² | n_bar", fontsize=11)
    ax.set_ylabel("Residual γ_exp | n_bar", fontsize=11)
    ax.set_title(f"(c) Partial correlation (r = {r_partial:.3f})", fontsize=11)
    ax.grid(alpha=0.3)

    # (d) LOO R² comparison
    ax = axes[1, 1]
    loo_labels = ["n_bar", "n_bar^(2/3)", "r_s^(-4)", "∫(dδ/dz)²", "∫(dn/dz)²"]
    loo_vals = [r2_loo_nbar, r2_loo_nbar23, r2_loo_rs4, r2_loo_dgrad, r2_loo_dn2]
    bar_colors = ["steelblue"] * 3 + ["#e74c3c"] + ["orange"]
    ax.barh(loo_labels, loo_vals, color=bar_colors, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Leave-One-Out R²", fontsize=11)
    ax.set_title("(d) Cross-validated predictive power", fontsize=11)
    ax.set_xlim(0, 1.05)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(loo_vals):
        ax.text(v + 0.01, i, f"{v:.3f}", va="center", fontsize=10)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test2_monotonicity.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test2_monotonicity.png')}")
    plt.close("all")

    return {
        "all_same_rank": all_same_rank,
        "partial_r": r_partial,
        "loo_r2_nbar": r2_loo_nbar,
        "loo_r2_dgrad": r2_loo_dgrad,
    }


if __name__ == "__main__":
    results = main()
