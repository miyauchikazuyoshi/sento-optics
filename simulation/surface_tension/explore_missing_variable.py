#!/usr/bin/env python3
"""
Exploration: What physical quantity is missing from the surface tension model?

In Paper 1: optical response required δ × D_eff (not δ alone).
In Paper 2: surface tension with δ-gradient alone ≈ n_bar^(1/6) → trivial.

Question: What measurable quantity, combined with n_bar or δ,
properly predicts surface tension for metals including d-band metals?

Candidates:
  1. Work function φ — surface dipole barrier
  2. Bulk modulus B — resistance to compression
  3. Cohesive energy E_coh — total binding
  4. Melting temperature T_m — proxy for cohesive strength
  5. Debye temperature θ_D — phonon stiffness
  6. DOS at E_F: γ_e (electronic specific heat coefficient)
  7. d-band center ε_d (Nørskov descriptor)
  8. Plasma frequency ω_p (Drude)
  9. Interband transition threshold ω_ib

We collect these from standard references and test which 2-variable
combination best predicts γ_exp for 12 metals.

Key insight from Paper 1: δ alone classifies, but response functions
(ε, D_eff) determine magnitude. For surface tension, the analog
response function might be B, φ, or E_coh.

Data sources:
  - φ: Michaelson (1977) J. Appl. Phys. 48, 4729 (polycrystalline)
  - B: Kittel, Introduction to Solid State Physics
  - E_coh: Kittel; CRC Handbook
  - T_m: CRC Handbook
  - θ_D: Kittel Table 5.1
  - γ_e: Kittel Table 6.2

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from itertools import combinations
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)


# ── Comprehensive metal data ──
# All values from standard references (Kittel, CRC, Michaelson)
METALS = {
    #       r_s    γ_exp    φ[eV]  B[GPa]  E_coh[eV] T_m[K]  θ_D[K]   has_d
    "Al":  (2.07, 1140,    4.28,   76,     3.39,     933,    428,     False),
    "Zn":  (2.12,  782,    4.33,  108,     1.35,     693,    327,     True),
    "Mg":  (2.66,  559,    3.66,   45,     1.51,     923,    400,     False),
    "Li":  (3.25,  398,    2.93,   11,     1.63,     454,    344,     False),
    "Na":  (3.93,  191,    2.75,    6.3,   1.11,     371,    158,     False),
    "K":   (4.86,  150,    2.30,    3.1,   0.93,     337,     91,     False),
    "Cs":  (5.62,   67,    2.14,    1.6,   0.80,     302,     38,     False),
    "Cu":  (2.67, 1285,    4.65,  137,     3.49,    1358,    343,     True),
    "Ga":  (2.19,  718,    4.20,   56,     2.81,     303,    320,     True),
    "Sn":  (2.22,  560,    4.42,   58,     3.14,     505,    200,     False),
    "Pb":  (2.30,  458,    4.25,   46,     2.03,     601,    105,     False),
    "In":  (2.41,  556,    4.12,   41,     2.52,     430,    108,     False),
}

FIELDS = ["r_s", "gamma_exp", "phi", "B", "E_coh", "T_m", "theta_D", "has_d"]


def main():
    print("=" * 70)
    print("EXPLORATION: What Physical Quantity is Missing?")
    print("=" * 70)

    names = list(METALS.keys())
    data = {f: np.array([METALS[m][i] for m in names])
            for i, f in enumerate(FIELDS) if f != "has_d"}

    gamma = data["gamma_exp"]
    n_bar = 3.0 / (4.0 * np.pi * data["r_s"]**3)
    data["n_bar"] = n_bar
    is_d = np.array([METALS[m][7] for m in names])

    # ── Single-variable correlations ──
    print("\n--- Single-Variable Correlations with γ_exp ---")
    print(f"{'Variable':>12s}  {'Pearson r':>10s}  {'Spearman ρ':>10s}  {'p':>10s}")
    print("-" * 50)

    single_vars = {
        "n_bar": n_bar,
        "n_bar^(2/3)": n_bar**(2./3),
        "φ": data["phi"],
        "B": data["B"],
        "E_coh": data["E_coh"],
        "T_m": data["T_m"],
        "θ_D": data["theta_D"],
        "φ × n_bar^(1/3)": data["phi"] * n_bar**(1./3),
        "B^(1/2)": np.sqrt(data["B"]),
        "E_coh × n_bar^(2/3)": data["E_coh"] * n_bar**(2./3),
        "φ²": data["phi"]**2,
        "B × r_s^(-2)": data["B"] / data["r_s"]**2,
    }

    single_results = {}
    for label, x in single_vars.items():
        rp, pp = pearsonr(x, gamma)
        rs, ps = spearmanr(x, gamma)
        single_results[label] = {"r": rp, "rho": rs, "p": pp}
        print(f"{label:>20s}  {rp:10.4f}  {rs:10.4f}  {pp:10.2e}")

    # ── Two-variable linear regression ──
    print("\n--- Two-Variable Models: γ ≈ a×X₁ + b×X₂ + c ---")
    print("(Testing all pairs of physical quantities)")

    base_vars = {
        "n_bar": n_bar,
        "φ": data["phi"],
        "B": data["B"],
        "E_coh": data["E_coh"],
        "T_m": data["T_m"],
        "θ_D": data["theta_D"],
    }

    # LOO R² for two-variable models
    def loo_r2_2var(x1, x2, y):
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
        return 1.0 - ss_res / ss_tot

    def r2_2var(x1, x2, y):
        N = len(y)
        X = np.column_stack([x1, x2, np.ones(N)])
        c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        y_pred = X @ c
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - y.mean())**2)
        return 1.0 - ss_res / ss_tot, c

    results_2var = []
    for (n1, x1), (n2, x2) in combinations(base_vars.items(), 2):
        r2, coeffs = r2_2var(x1, x2, gamma)
        r2_loo = loo_r2_2var(x1, x2, gamma)
        results_2var.append({
            "vars": f"{n1} + {n2}",
            "r2": r2, "r2_loo": r2_loo, "coeffs": coeffs,
            "n1": n1, "n2": n2, "x1": x1, "x2": x2,
        })

    results_2var.sort(key=lambda x: x["r2_loo"], reverse=True)

    print(f"\n{'Variables':>20s}  {'R²':>8s}  {'LOO R²':>8s}")
    print("-" * 45)
    for r in results_2var[:10]:
        print(f"{r['vars']:>20s}  {r['r2']:8.4f}  {r['r2_loo']:8.4f}")

    # ── The key test: does adding a second variable resolve Al vs Zn? ──
    print("\n\n--- AL vs ZN: Which variable explains the discrepancy? ---")
    al_idx = names.index("Al")
    zn_idx = names.index("Zn")

    print(f"\n{'Variable':>12s}  {'Al':>10s}  {'Zn':>10s}  {'Ratio Al/Zn':>12s}  "
          f"{'γ ratio needed':>15s}")
    print("-" * 65)
    gamma_ratio = METALS["Al"][1] / METALS["Zn"][1]  # 1140/782 = 1.458

    for label, x in base_vars.items():
        ratio = x[al_idx] / x[zn_idx] if x[zn_idx] != 0 else np.inf
        print(f"{label:>12s}  {x[al_idx]:10.3f}  {x[zn_idx]:10.3f}  {ratio:12.3f}  "
              f"{gamma_ratio:15.3f}")

    print(f"\n  To explain γ_Al/γ_Zn = {gamma_ratio:.3f}, we need a variable where"
          f" Al/Zn ≈ {gamma_ratio:.2f}")
    print(f"  n_bar: ratio = {n_bar[al_idx]/n_bar[zn_idx]:.3f} → FAILS (too close)")
    print(f"  B:     ratio = {data['B'][al_idx]/data['B'][zn_idx]:.3f} → "
          f"{'WRONG direction (Zn > Al)' if data['B'][zn_idx] > data['B'][al_idx] else 'Possible'}")
    print(f"  E_coh: ratio = {data['E_coh'][al_idx]/data['E_coh'][zn_idx]:.3f} → "
          f"{'Large difference!' if abs(data['E_coh'][al_idx]/data['E_coh'][zn_idx] - gamma_ratio) < 0.5 else 'Moderate'}")
    print(f"  T_m:   ratio = {data['T_m'][al_idx]/data['T_m'][zn_idx]:.3f}")

    # ── Cohesive energy as the missing variable ──
    print("\n\n--- HYPOTHESIS: γ ∝ E_coh × n_bar^(2/3) ---")
    print("(Surface energy = cohesive energy per unit area)")

    predictor_Ecoh_n = data["E_coh"] * n_bar**(2./3)
    r_Ecoh_n, p_Ecoh_n = pearsonr(predictor_Ecoh_n, gamma)
    print(f"  Pearson r = {r_Ecoh_n:.4f} (p = {p_Ecoh_n:.2e})")

    # LOO R²
    N = len(gamma)
    y_pred_loo = np.zeros(N)
    for i in range(N):
        mask = np.ones(N, dtype=bool)
        mask[i] = False
        c = np.polyfit(predictor_Ecoh_n[mask], gamma[mask], 1)
        y_pred_loo[i] = np.polyval(c, predictor_Ecoh_n[i])
    r2_loo_Ecoh = 1.0 - np.sum((gamma - y_pred_loo)**2) / np.sum((gamma - gamma.mean())**2)
    print(f"  LOO R² = {r2_loo_Ecoh:.4f}")

    # Partial correlation controlling for n_bar
    c1 = np.polyfit(n_bar, predictor_Ecoh_n, 1)
    c2 = np.polyfit(n_bar, gamma, 1)
    resid1 = predictor_Ecoh_n - np.polyval(c1, n_bar)
    resid2 = gamma - np.polyval(c2, n_bar)
    r_partial, p_partial = pearsonr(resid1, resid2)
    print(f"  Partial r (control n_bar) = {r_partial:.4f} (p = {p_partial:.4f})")

    # ── Product predictors (like δ × D_eff in Paper 1) ──
    print("\n\n--- PRODUCT PREDICTORS (analog of δ × D_eff) ---")
    products = {
        "n_bar × E_coh": n_bar * data["E_coh"],
        "n_bar^(2/3) × E_coh": n_bar**(2./3) * data["E_coh"],
        "n_bar^(1/3) × φ": n_bar**(1./3) * data["phi"],
        "n_bar^(1/2) × B^(1/2)": n_bar**(1./2) * np.sqrt(data["B"]),
        "n_bar × T_m": n_bar * data["T_m"],
        "n_bar^(2/3) × T_m": n_bar**(2./3) * data["T_m"],
        "n_bar^(2/3) × B^(1/2)": n_bar**(2./3) * np.sqrt(data["B"]),
        "n_bar^(1/3) × E_coh": n_bar**(1./3) * data["E_coh"],
        "φ × E_coh": data["phi"] * data["E_coh"],
        "φ × B^(1/2)": data["phi"] * np.sqrt(data["B"]),
    }

    print(f"\n{'Predictor':>25s}  {'Pearson r':>10s}  {'Spearman ρ':>10s}  "
          f"{'LOO R²':>8s}  {'Partial r':>10s}")
    print("-" * 75)

    best_r = 0
    best_label = ""
    for label, x in products.items():
        rp, pp = pearsonr(x, gamma)
        rs, _ = spearmanr(x, gamma)
        # LOO R²
        y_pred = np.zeros(N)
        for i in range(N):
            mask = np.ones(N, dtype=bool)
            mask[i] = False
            c = np.polyfit(x[mask], gamma[mask], 1)
            y_pred[i] = np.polyval(c, x[i])
        r2_loo = 1.0 - np.sum((gamma - y_pred)**2) / np.sum((gamma - gamma.mean())**2)
        # Partial
        c1 = np.polyfit(n_bar, x, 1)
        c2 = np.polyfit(n_bar, gamma, 1)
        rp_partial, _ = pearsonr(x - np.polyval(c1, n_bar), gamma - np.polyval(c2, n_bar))
        print(f"{label:>25s}  {rp:10.4f}  {rs:10.4f}  {r2_loo:8.4f}  {rp_partial:10.4f}")
        if rp > best_r:
            best_r = rp
            best_label = label

    # ── Best model analysis ──
    best = results_2var[0]
    print(f"\n\n{'='*70}")
    print(f"BEST TWO-VARIABLE MODEL: {best['vars']}")
    print(f"  R² = {best['r2']:.4f}, LOO R² = {best['r2_loo']:.4f}")
    print(f"  γ ≈ {best['coeffs'][0]:.2f}×{best['n1']} "
          f"+ {best['coeffs'][1]:.2f}×{best['n2']} "
          f"+ {best['coeffs'][2]:.2f}")

    # Predicted vs actual
    X_best = np.column_stack([best["x1"], best["x2"], np.ones(N)])
    gamma_pred = X_best @ best["coeffs"]
    print(f"\n{'Metal':>6s}  {'γ_exp':>8s}  {'γ_pred':>8s}  {'Error':>8s}  {'Error%':>8s}")
    print("-" * 45)
    for i, name in enumerate(names):
        err = gamma[i] - gamma_pred[i]
        err_pct = 100 * err / gamma[i]
        print(f"{name:>6s}  {gamma[i]:8.0f}  {gamma_pred[i]:8.0f}  {err:8.0f}  {err_pct:7.1f}%")

    rmse = np.sqrt(np.mean((gamma - gamma_pred)**2))
    print(f"\n  RMSE = {rmse:.0f} erg/cm²")

    # ── Figure ──
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("What Physical Quantity is Missing from the Surface Tension Model?",
                 fontsize=14, y=1.02)

    # (a) Single variable correlations
    ax = axes[0, 0]
    top_single = sorted(single_results.items(), key=lambda x: abs(x[1]["r"]), reverse=True)[:6]
    labels_s = [t[0] for t in top_single]
    rs_s = [t[1]["r"] for t in top_single]
    colors_s = ["#e74c3c" if abs(r) > 0.9 else "#f39c12" if abs(r) > 0.8
                else "#3498db" for r in rs_s]
    ax.barh(labels_s[::-1], rs_s[::-1], color=colors_s[::-1],
            edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Pearson r with γ_exp", fontsize=11)
    ax.set_title("(a) Single-Variable Correlations", fontsize=11)
    ax.set_xlim(0, 1.05)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(rs_s[::-1]):
        ax.text(v + 0.01, i, f"{v:.3f}", va="center", fontsize=9)

    # (b) Best two-variable model: predicted vs actual
    ax = axes[0, 1]
    sp_mask = ~is_d
    ax.scatter(gamma_pred[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp-metals")
    ax.scatter(gamma_pred[is_d], gamma[is_d], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d-metals")
    for i, n in enumerate(names):
        ax.annotate(n, (gamma_pred[i], gamma[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.plot([0, 1400], [0, 1400], "k--", alpha=0.3)
    ax.set_xlabel(f"Predicted γ [{best['vars']}]", fontsize=11)
    ax.set_ylabel("Experimental γ [erg/cm²]", fontsize=11)
    ax.set_title(f"(b) Best model: {best['vars']}\n"
                 f"R²={best['r2']:.3f}, LOO R²={best['r2_loo']:.3f}", fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (c) Al vs Zn: what explains the gap
    ax = axes[0, 2]
    ratio_labels = []
    ratio_vals = []
    for label in ["n_bar", "φ", "B", "E_coh", "T_m", "θ_D"]:
        x = data.get(label, base_vars.get(label))
        if x is not None:
            ratio = x[al_idx] / x[zn_idx] if x[zn_idx] != 0 else 0
            ratio_labels.append(label)
            ratio_vals.append(ratio)
    ratio_labels.append("γ_exp")
    ratio_vals.append(gamma_ratio)

    colors_r = ["#3498db"] * (len(ratio_vals) - 1) + ["#e74c3c"]
    ax.barh(ratio_labels, ratio_vals, color=colors_r,
            edgecolor="black", linewidth=0.5)
    ax.axvline(1.0, color="gray", linestyle="--", alpha=0.3)
    ax.axvline(gamma_ratio, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("Ratio (Al / Zn)", fontsize=11)
    ax.set_title("(c) Al vs Zn: Which variable explains γ gap?", fontsize=11)
    ax.grid(alpha=0.3, axis="x")

    # (d) LOO R² for two-variable models
    ax = axes[1, 0]
    top_2var = results_2var[:8]
    labels_2 = [r["vars"] for r in top_2var]
    r2_2 = [r["r2_loo"] for r in top_2var]
    ax.barh(labels_2[::-1], r2_2[::-1], color="steelblue",
            edgecolor="black", linewidth=0.5)
    ax.set_xlabel("LOO R²", fontsize=11)
    ax.set_title("(d) Two-Variable Models (LOO R²)", fontsize=11)
    ax.set_xlim(0, 1.05)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(r2_2[::-1]):
        ax.text(v + 0.01, i, f"{v:.3f}", va="center", fontsize=9)

    # (e) Product predictors
    ax = axes[1, 1]
    top_products = sorted(
        [(l, pearsonr(x, gamma)[0]) for l, x in products.items()],
        key=lambda t: abs(t[1]), reverse=True
    )[:8]
    labels_p = [t[0] for t in top_products]
    rs_p = [t[1] for t in top_products]
    ax.barh(labels_p[::-1], rs_p[::-1], color="forestgreen",
            edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Pearson r with γ_exp", fontsize=11)
    ax.set_title("(e) Product Predictors (δ × X analog)", fontsize=11)
    ax.set_xlim(0, 1.05)
    ax.grid(alpha=0.3, axis="x")
    for i, v in enumerate(rs_p[::-1]):
        ax.text(v + 0.01, i, f"{v:.3f}", va="center", fontsize=9)

    # (f) Best product: scatter
    ax = axes[1, 2]
    best_prod_label = top_products[0][0]
    best_prod = products[best_prod_label]
    ax.scatter(best_prod[sp_mask], gamma[sp_mask], s=80, c="blue",
               edgecolors="black", linewidth=0.5, zorder=5, label="sp-metals")
    ax.scatter(best_prod[is_d], gamma[is_d], s=80, c="red", marker="^",
               edgecolors="black", linewidth=0.5, zorder=5, label="d-metals")
    for i, n in enumerate(names):
        ax.annotate(n, (best_prod[i], gamma[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    c = np.polyfit(best_prod, gamma, 1)
    x_fit = np.linspace(best_prod.min() * 0.9, best_prod.max() * 1.1, 100)
    ax.plot(x_fit, np.polyval(c, x_fit), "k--", alpha=0.3)
    r_best_prod = top_products[0][1]
    ax.set_xlabel(best_prod_label, fontsize=11)
    ax.set_ylabel("γ_exp [erg/cm²]", fontsize=11)
    ax.set_title(f"(f) Best product: r = {r_best_prod:.3f}", fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_explore_missing_variable.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_explore_missing_variable.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
