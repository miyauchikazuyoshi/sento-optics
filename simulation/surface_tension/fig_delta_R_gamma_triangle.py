#!/usr/bin/env python3
"""
The delta-R-gamma Triangle Figure
==================================

Shows that both reflectivity R and surface tension gamma correlate with
the same delocalization index delta_IPR, implying they are two projections
of a single underlying variable: electronic delocalization.

Panel (a): delta vs R  — optical reflectivity tracks delocalization
Panel (b): delta vs gamma — surface tension tracks delocalization
Panel (c): R vs gamma  — the two observables correlate (indirect)

delta proxy: n_ws^(1/3) from de Boer / Miedema tables (1988).
Justified because Paper 2 (test7) establishes delta_IPR <-> n_ws.

Note on Cu: visible-average R is depressed relative to Drude prediction
because the d->sp interband transition at ~2.1 eV (590 nm) absorbs
strongly in the yellow-red, giving Cu its characteristic colour.
The 64% average is lower than the IR reflectivity (~97%).

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os

FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────
# 12 liquid metals
elements = ["Li", "Na", "K", "Cs", "Be", "Mg", "Al", "Zn", "Cu", "Ga", "In", "Sn"]

# Surface tension gamma (mN/m) — Keene 1993 / Iida-Guthrie 1988
gamma = {
    "Li": 398, "Na": 191, "K": 110, "Cs": 67,
    "Be": 1100, "Mg": 559, "Al": 1140, "Zn": 782,
    "Cu": 1330, "Ga": 718, "In": 556, "Sn": 560,
}

# Normal-incidence reflectivity R (%), visible-average 400-700 nm
# From optical handbooks / Drude fits to experimental data
# Cu: visible-average is low (~64%) due to d->sp interband at 2.1 eV
R = {
    "Li": 91, "Na": 97, "K": 96, "Cs": 95,
    "Be": 50, "Mg": 74, "Al": 91, "Zn": 70,
    "Cu": 64, "Ga": 70, "In": 78, "Sn": 68,
}

# delta proxy: n_ws^(1/3) in (d.u.)^(1/3)
# From de Boer et al. 1988 / Miedema tables
# n_ws is the electron density at the Wigner-Seitz boundary (d.u. = density units)
# n_ws^(1/3) encodes delocalization: higher -> more uniform density -> more delocalized
nws_one_third = {
    "Li": 1.30, "Na": 1.02, "K": 0.82, "Cs": 0.73,
    "Be": 1.67, "Mg": 1.17, "Al": 1.39, "Zn": 1.32,
    "Cu": 1.47, "Ga": 1.31, "In": 1.17, "Sn": 1.24,
}

# Metal type classification for colouring
metal_type = {
    "Li": "alkali", "Na": "alkali", "K": "alkali", "Cs": "alkali",
    "Be": "alkaline_earth", "Mg": "alkaline_earth",
    "Al": "p_block", "Ga": "p_block", "In": "p_block", "Sn": "p_block",
    "Zn": "transition", "Cu": "transition",
}

type_colors = {
    "alkali": "royalblue",
    "alkaline_earth": "seagreen",
    "p_block": "crimson",
    "transition": "darkorange",
}
type_labels = {
    "alkali": "Alkali",
    "alkaline_earth": "Alkaline earth",
    "p_block": "p-block",
    "transition": "Transition / post-transition",
}

# ── Build arrays ──────────────────────────────────────────────────────
delta_arr = np.array([nws_one_third[e] for e in elements])
R_arr     = np.array([R[e] for e in elements], dtype=float)
gamma_arr = np.array([gamma[e] for e in elements], dtype=float)
colors    = [type_colors[metal_type[e]] for e in elements]

# ── Correlations ──────────────────────────────────────────────────────
r_dR, p_dR = pearsonr(delta_arr, R_arr)
r_dg, p_dg = pearsonr(delta_arr, gamma_arr)
r_Rg, p_Rg = pearsonr(R_arr, gamma_arr)

print(f"Pearson r(delta, R)     = {r_dR:.4f}  (p = {p_dR:.4e})")
print(f"Pearson r(delta, gamma) = {r_dg:.4f}  (p = {p_dg:.4e})")
print(f"Pearson r(R, gamma)     = {r_Rg:.4f}  (p = {p_Rg:.4e})")

# ── Figure ────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(
    r"The $\delta$–$R$–$\gamma$ Triangle: Optical Reflectivity and Surface Tension"
    "\nas Projections of Electronic Delocalization",
    fontsize=13, y=1.02,
)

panel_data = [
    # (ax_idx, xdata, ydata, xlabel, ylabel, r_val, p_val, panel_label)
    (0, delta_arr, R_arr,
     r"$\delta$ proxy  ($n_{\rm ws}^{1/3}$, d.u.$^{1/3}$)",
     "Normal-incidence reflectivity $R$ (%)",
     r_dR, p_dR, "(a)"),
    (1, delta_arr, gamma_arr,
     r"$\delta$ proxy  ($n_{\rm ws}^{1/3}$, d.u.$^{1/3}$)",
     r"Surface tension $\gamma$ (mN/m)",
     r_dg, p_dg, "(b)"),
    (2, R_arr, gamma_arr,
     "Normal-incidence reflectivity $R$ (%)",
     r"Surface tension $\gamma$ (mN/m)",
     r_Rg, p_Rg, "(c)"),
]

# Track which type labels have been added to legend
for ax_idx, xdata, ydata, xlabel, ylabel, r_val, p_val, label in panel_data:
    ax = axes[ax_idx]
    legend_done = set()

    for i, elem in enumerate(elements):
        t = metal_type[elem]
        lbl = type_labels[t] if t not in legend_done else None
        legend_done.add(t)
        ax.scatter(xdata[i], ydata[i], s=90, c=colors[i],
                   edgecolors="black", linewidth=0.6, zorder=5, label=lbl)
        # Offset labels to avoid overlap
        dx, dy = 0.02 * (xdata.max() - xdata.min()), 0.02 * (ydata.max() - ydata.min())
        ax.annotate(elem, (xdata[i], ydata[i]),
                    textcoords="offset points", xytext=(6, 5), fontsize=8)

    # Linear fit line
    coeffs = np.polyfit(xdata, ydata, 1)
    x_fit = np.linspace(xdata.min() * 0.92, xdata.max() * 1.05, 100)
    ax.plot(x_fit, np.polyval(coeffs, x_fit), "k--", alpha=0.3, linewidth=1)

    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
    ax.set_title(f"{label}  $r$ = {r_val:.3f}{sig}", fontsize=11)
    ax.grid(alpha=0.25)
    if ax_idx == 0:
        ax.legend(fontsize=7.5, loc="lower right")

fig.tight_layout()
outpath = os.path.join(FIGDIR, "fig_delta_R_gamma_triangle.png")
fig.savefig(outpath, dpi=300, bbox_inches="tight")
print(f"\nSaved: {outpath}")
plt.close("all")
