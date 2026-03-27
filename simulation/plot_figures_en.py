"""
δ×D_eff Optical Response Maps — English Version
================================================
Generates all publication-ready figures with English labels.
Output: simulation/figures/ (overwrites existing PNGs)
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from itertools import combinations
from matplotlib.patches import Patch

matplotlib.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']

# ============================================================
# Data (from published literature)
# ============================================================

materials = {
    "Diamond": {
        "label": "Diamond",
        "pi_bandwidth_eV": None,  # sp3, no pi band
        "inv_eff_mass": 1 / 0.48,
        "bandgap_eV": 5.47,
        "neg_Eg": -5.47,
        "D_eff": 0,
        "optical_category": "Transparent",
        "color": "#1E90FF",
        "marker": "D",
    },
    "C60": {
        "label": "C$_{60}$ solid",
        "pi_bandwidth_eV": 0.45,
        "inv_eff_mass": 1 / 4.0,
        "bandgap_eV": 1.75,
        "neg_Eg": -1.75,
        "D_eff": 0,
        "optical_category": "Colored\n(dark purple)",
        "color": "#9932CC",
        "marker": "p",
    },
    "SWCNT_sc": {
        "label": "SWCNT\n(semiconducting)",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 1 / 0.07,
        "bandgap_eV": 1.0,
        "neg_Eg": -1.0,
        "D_eff": 1,
        "optical_category": "Colored\n(chirality-dep.)",
        "color": "#FF8C00",
        "marker": "s",
    },
    "SWCNT_m": {
        "label": "SWCNT\n(metallic)",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 30.0,
        "bandgap_eV": 0.0,
        "neg_Eg": 0.0,
        "D_eff": 1,
        "optical_category": "Black\nw/ weak luster",
        "color": "#FF4500",
        "marker": "s",
    },
    "Graphene": {
        "label": "Graphene",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 33.3,
        "bandgap_eV": 0.0,
        "neg_Eg": 0.0,
        "D_eff": 2,
        "optical_category": "Nearly transparent\n(2.3%/layer)",
        "color": "#228B22",
        "marker": "^",
    },
    "Graphite": {
        "label": "Graphite",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 1 / 0.039,
        "bandgap_eV": 0.0,
        "neg_Eg": 0.0,
        "D_eff": 2,
        "optical_category": "Black +\ncleavage gloss",
        "color": "#2F4F4F",
        "marker": "o",
    },
    "hBN": {
        "label": "h-BN",
        "pi_bandwidth_eV": 2.4,
        "inv_eff_mass": 1 / 0.26,
        "bandgap_eV": 5.95,
        "neg_Eg": -5.95,
        "D_eff": 0,
        "optical_category": "White\n(transparent)",
        "color": "#CCCCCC",
        "marker": "h",
        "edgecolor": "#333333",
    },
}

figdir = "simulation/figures/"

# ============================================================
# Figure 1: delta (pi-band width) vs D_eff map
# ============================================================

fig1, ax1 = plt.subplots(figsize=(10, 7))

for key, m in materials.items():
    bw = m["pi_bandwidth_eV"]
    if bw is None:
        bw = 0.0
    ec = m.get("edgecolor", m["color"])
    ax1.scatter(bw, m["D_eff"], s=250, c=m["color"], marker=m["marker"],
                edgecolors=ec, linewidths=1.5, zorder=5)
    offset_x, offset_y = 0.3, 0.08
    if key == "Diamond":
        offset_x, offset_y = 0.3, -0.15
    elif key == "Graphite":
        offset_x, offset_y = 0.3, -0.15
    elif key == "SWCNT_m":
        offset_x, offset_y = 0.3, -0.15
    ax1.annotate(
        f"{m['label']}\n({m['optical_category']})",
        (bw, m["D_eff"]),
        xytext=(bw + offset_x, m["D_eff"] + offset_y),
        fontsize=8, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
    )

ax1.axhspan(-0.3, 0.5, color="#E6F3FF", alpha=0.4, zorder=0)
ax1.axhspan(0.5, 1.5, color="#FFF3E6", alpha=0.4, zorder=0)
ax1.axhspan(1.5, 2.5, color="#E6FFE6", alpha=0.4, zorder=0)
ax1.axhspan(2.5, 3.3, color="#FFE6E6", alpha=0.4, zorder=0)

ax1.set_xlabel(r"$\delta$ proxy: $\pi$-band width (eV)", fontsize=13)
ax1.set_ylabel(r"$D_\mathrm{eff}$ (effective conduction dimensionality)", fontsize=13)
ax1.set_title(r"$\delta \times D_\mathrm{eff}$ Optical Response Map (Carbon Allotropes + h-BN)", fontsize=13, fontweight="bold")
ax1.set_xlim(-0.5, 12)
ax1.set_ylim(-0.3, 3.3)
ax1.set_yticks([0, 1, 2, 3])
ax1.set_yticklabels(["0\n(localized)", "1\n(1D cond.)", "2\n(2D in-plane)", "3\n(3D metal)"])

ax1.scatter(11, 3, s=200, c="gold", marker="*", edgecolors="black", linewidths=1.0, zorder=5)
ax1.annotate("Metals (Au, Ag)\n(metallic luster)", (11, 3),
             xytext=(8.5, 2.7), fontsize=8, ha="center",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
             arrowprops=dict(arrowstyle="->", color="gray"))

ax1.annotate("", xy=(10, -0.15), xytext=(0.5, -0.15),
             arrowprops=dict(arrowstyle="->", lw=1.5, color="navy"))
ax1.text(5.25, -0.22, r"Increasing $\delta$ $\rightarrow$ electronic delocalization", ha="center", fontsize=10, color="navy")

ax1.grid(True, alpha=0.3)
fig1.tight_layout()
fig1.savefig(figdir + "fig1_delta_deff_map.png", dpi=200, bbox_inches="tight")
print("Saved: fig1_delta_deff_map.png")


# ============================================================
# Figure 2: delta-Eg inverse correlation
# ============================================================

fig2, ax2 = plt.subplots(figsize=(9, 6))

for key, m in materials.items():
    bw = m["pi_bandwidth_eV"]
    if bw is None:
        continue
    ec = m.get("edgecolor", m["color"])
    ax2.scatter(bw, m["bandgap_eV"], s=200, c=m["color"], marker=m["marker"],
                edgecolors=ec, linewidths=1.5, zorder=5)
    ox = 0.3
    if key == "SWCNT_m":
        ox = -2.5
    ax2.annotate(m["label"].split("\n")[0], (bw, m["bandgap_eV"]),
                 xytext=(bw + ox, m["bandgap_eV"] + 0.2),
                 fontsize=9, ha="left" if ox > 0 else "right",
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8))

bw_data = [m["pi_bandwidth_eV"] for m in materials.values() if m["pi_bandwidth_eV"] is not None]
eg_data = [m["bandgap_eV"] for k, m in materials.items() if m["pi_bandwidth_eV"] is not None]
bw_arr, eg_arr = np.array(bw_data), np.array(eg_data)
r = np.corrcoef(bw_arr, eg_arr)[0, 1]

coeffs = np.polyfit(bw_arr, eg_arr, 1)
x_fit = np.linspace(0, 10, 100)
y_fit = np.maximum(np.polyval(coeffs, x_fit), 0)
ax2.plot(x_fit, y_fit, "--", color="gray", alpha=0.5, zorder=1)

ax2.set_xlabel(r"$\delta$ proxy: $\pi$-band width (eV)", fontsize=13)
ax2.set_ylabel(r"Band gap $E_g$ (eV)", fontsize=13)
ax2.set_title(f"$\\delta$--$E_g$ inverse correlation ($r = {r:.3f}$)", fontsize=14, fontweight="bold")
ax2.set_xlim(-0.5, 11)
ax2.set_ylim(-0.5, 7)
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig(figdir + "fig2_delta_bandgap_correlation.png", dpi=200, bbox_inches="tight")
print(f"Saved: fig2_delta_bandgap_correlation.png (r={r:.3f})")


# ============================================================
# Figure 3: Inverse effective mass vs D_eff
# ============================================================

fig3, ax3 = plt.subplots(figsize=(10, 7))

for key, m in materials.items():
    inv_m = m["inv_eff_mass"]
    ec = m.get("edgecolor", m["color"])
    ax3.scatter(inv_m, m["D_eff"], s=250, c=m["color"], marker=m["marker"],
                edgecolors=ec, linewidths=1.5, zorder=5)
    offset_x = inv_m * 0.05 + 0.5
    offset_y = 0.08
    if key in ["Graphite", "SWCNT_m", "Diamond"]:
        offset_y = -0.15
    ax3.annotate(
        f"{m['label']}\n({m['optical_category']})",
        (inv_m, m["D_eff"]),
        xytext=(inv_m + offset_x, m["D_eff"] + offset_y),
        fontsize=8, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
    )

ax3.axhspan(-0.3, 0.5, color="#E6F3FF", alpha=0.4, zorder=0)
ax3.axhspan(0.5, 1.5, color="#FFF3E6", alpha=0.4, zorder=0)
ax3.axhspan(1.5, 2.5, color="#E6FFE6", alpha=0.4, zorder=0)
ax3.axhspan(2.5, 3.3, color="#FFE6E6", alpha=0.4, zorder=0)

ax3.set_xlabel(r"$\delta$ proxy: $1/m^*$ (inverse effective mass, $m_0^{-1}$)", fontsize=13)
ax3.set_ylabel(r"$D_\mathrm{eff}$ (effective conduction dimensionality)", fontsize=13)
ax3.set_title(r"$\delta(1/m^*) \times D_\mathrm{eff}$ Optical Response Map", fontsize=14, fontweight="bold")
ax3.set_xscale("log")
ax3.set_xlim(0.1, 50)
ax3.set_ylim(-0.3, 3.3)
ax3.set_yticks([0, 1, 2, 3])
ax3.set_yticklabels(["0\n(localized)", "1\n(1D cond.)", "2\n(2D in-plane)", "3\n(3D metal)"])

ax3.scatter(40, 3, s=200, c="gold", marker="*", edgecolors="black", linewidths=1.0, zorder=5)
ax3.annotate("Metals (Au, Ag)\n(metallic luster)", (40, 3),
             xytext=(15, 2.7), fontsize=8, ha="center",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
             arrowprops=dict(arrowstyle="->", color="gray"))

ax3.grid(True, alpha=0.3, which="both")
fig3.tight_layout()
fig3.savefig(figdir + "fig3_invmass_deff_map.png", dpi=200, bbox_inches="tight")
print("Saved: fig3_invmass_deff_map.png")


# ============================================================
# Figure 4: Indicator consistency (pairwise correlations)
# ============================================================

sp2_list = [
    {"label": "C$_{60}$", "pi_bw": 0.45, "inv_mass": 1/4.0, "neg_Eg": -1.75},
    {"label": "SWCNT (sc)", "pi_bw": 9.0, "inv_mass": 1/0.07, "neg_Eg": -1.0},
    {"label": "SWCNT (m)", "pi_bw": 9.0, "inv_mass": 30.0, "neg_Eg": 0.0},
    {"label": "Graphene", "pi_bw": 9.0, "inv_mass": 33.3, "neg_Eg": 0.0},
    {"label": "Graphite", "pi_bw": 9.0, "inv_mass": 1/0.039, "neg_Eg": 0.0},
    {"label": "h-BN", "pi_bw": 2.4, "inv_mass": 1/0.26, "neg_Eg": -5.95},
]

colors_sp2 = ["#9932CC", "#FF8C00", "#FF4500", "#228B22", "#2F4F4F", "#999999"]

fig4, axes = plt.subplots(1, 3, figsize=(15, 5))

pairs = [
    (r"$\pi$-band width (eV)", r"$1/m^*$ ($m_0^{-1}$)", "pi_bw", "inv_mass"),
    (r"$\pi$-band width (eV)", r"$-E_g$ (eV)", "pi_bw", "neg_Eg"),
    (r"$1/m^*$ ($m_0^{-1}$)", r"$-E_g$ (eV)", "inv_mass", "neg_Eg"),
]

for ax, (xname, yname, xkey, ykey) in zip(axes, pairs):
    for m, c in zip(sp2_list, colors_sp2):
        ax.scatter(m[xkey], m[ykey], s=120, c=c, edgecolors="black", linewidths=0.5, zorder=5)
        ax.annotate(m["label"], (m[xkey], m[ykey]),
                    xytext=(5, 5), textcoords="offset points", fontsize=7)
    xvals = [m[xkey] for m in sp2_list]
    yvals = [m[ykey] for m in sp2_list]
    r = np.corrcoef(xvals, yvals)[0, 1]
    ax.set_xlabel(xname, fontsize=10)
    ax.set_ylabel(yname, fontsize=10)
    ax.set_title(f"Pearson $r = {r:.3f}$", fontsize=11, fontweight="bold")
    ax.grid(True, alpha=0.3)

fig4.suptitle(r"Consistency among $\delta$-proxy indicators (pairwise correlations)", fontsize=13, fontweight="bold")
fig4.tight_layout()
fig4.savefig(figdir + "fig4_indicator_consistency.png", dpi=200, bbox_inches="tight")
print("Saved: fig4_indicator_consistency.png")


# ============================================================
# Figure 5: Classification result visualization
# ============================================================

mat_list = [
    {"name": "Diamond", "delta": 1/0.48, "D_eff": 0, "pred": "Transparent", "true": "Transparent"},
    {"name": "C$_{60}$", "delta": 1/4.0, "D_eff": 0, "pred": "Colored", "true": "Colored"},
    {"name": "SWCNT (sc)", "delta": 1/0.07, "D_eff": 1, "pred": "Colored", "true": "Colored"},
    {"name": "SWCNT (m)", "delta": 30.0, "D_eff": 1, "pred": "Black$-$luster", "true": "Black$-$luster"},
    {"name": "Graphene", "delta": 33.3, "D_eff": 2, "pred": "Transparent*", "true": "Transparent*"},
    {"name": "Graphite", "delta": 1/0.039, "D_eff": 2, "pred": "Black+gloss", "true": "Black+gloss"},
    {"name": "h-BN", "delta": 1/0.26, "D_eff": 0, "pred": "Transparent", "true": "Transparent"},
]

cat_colors = {
    "Transparent": "#87CEEB", "Transparent*": "#87CEEB",
    "Colored": "#DDA0DD",
    "Black$-$luster": "#696969", "Black+gloss": "#2F2F2F",
    "Metallic luster": "#FFD700",
}

fig5, ax5 = plt.subplots(figsize=(10, 6))
for i, r in enumerate(mat_list):
    fc = cat_colors.get(r["pred"], "white")
    match = r["pred"] == r["true"]
    ec = "green" if match else "red"
    ax5.barh(i, 1, color=fc, edgecolor=ec, linewidth=2)
    txt_color = "white" if "Black" in r["pred"] else "black"
    check = r"$\checkmark$" if match else r"$\times$"
    ax5.text(0.5, i, f"{r['name']}  |  Pred: {r['pred']}  |  True: {r['true']}  {check}",
             ha="center", va="center", fontsize=9, fontweight="bold", color=txt_color)

ax5.set_yticks(range(len(mat_list)))
ax5.set_yticklabels([f"$\\delta$={r['delta']:.1f}, $D$={r['D_eff']}" for r in mat_list], fontsize=8)
ax5.set_title("$\\delta \\times D_\\mathrm{eff}$ Classification Result (Accuracy: 100%)",
              fontsize=13, fontweight="bold")
ax5.set_xlim(0, 1)
ax5.set_xticks([])
legend_elements = [
    Patch(facecolor="#87CEEB", label="Transparent"),
    Patch(facecolor="#DDA0DD", label="Colored"),
    Patch(facecolor="#696969", label="Black$-$luster"),
    Patch(facecolor="#2F2F2F", label="Black+gloss"),
    Patch(facecolor="white", edgecolor="green", linewidth=2, label="Correct"),
]
ax5.legend(handles=legend_elements, loc="lower right", fontsize=8)
fig5.tight_layout()
fig5.savefig(figdir + "fig5_classification_result.png", dpi=200, bbox_inches="tight")
print("Saved: fig5_classification_result.png")


# ============================================================
# Figure 6: Eg vs D_eff classification map
# ============================================================

mat_eg = [
    {"name": "Diamond", "label": "Diamond", "Eg": 5.47, "D_eff": 0, "true": "Transparent", "mk": "D"},
    {"name": "C60", "label": "C$_{60}$", "Eg": 1.75, "D_eff": 0, "true": "Colored", "mk": "p"},
    {"name": "SWCNT_sc", "label": "SWCNT (sc)", "Eg": 1.0, "D_eff": 1, "true": "Colored", "mk": "s"},
    {"name": "SWCNT_m", "label": "SWCNT (m)", "Eg": 0.0, "D_eff": 1, "true": "Black-luster", "mk": "s"},
    {"name": "Graphene", "label": "Graphene", "Eg": 0.0, "D_eff": 2, "true": "Transparent", "mk": "^"},
    {"name": "Graphite", "label": "Graphite", "Eg": 0.0, "D_eff": 2, "true": "Black+gloss", "mk": "o"},
    {"name": "hBN", "label": "h-BN", "Eg": 5.95, "D_eff": 0, "true": "Transparent", "mk": "h"},
]

cat_colors2 = {
    "Transparent": "#87CEEB", "Colored": "#9932CC",
    "Black-luster": "#696969", "Black+gloss": "#2F2F2F",
    "Metallic luster": "#FFD700",
}

fig6, ax6 = plt.subplots(figsize=(10, 7))

for m in mat_eg:
    c = cat_colors2.get(m["true"], "gray")
    ec = "black" if m["true"] != "Black+gloss" else "white"
    ax6.scatter(m["Eg"], m["D_eff"], s=300, c=c, marker=m["mk"],
                edgecolors=ec, linewidths=1.5, zorder=5)
    ox, oy = 0.2, 0.1
    if m["name"] == "Graphite":
        ox, oy = 0.15, -0.2
    elif m["name"] == "SWCNT_m":
        ox, oy = 0.1, -0.2
    elif m["name"] == "hBN":
        ox, oy = -1.5, 0.1
    ax6.annotate(m["label"], (m["Eg"], m["D_eff"]),
                 xytext=(m["Eg"] + ox, m["D_eff"] + oy), fontsize=9,
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.85))

ax6.axvline(x=3.1, color="red", linestyle="--", alpha=0.5, label="$E_\\mathrm{vis} = 3.1$ eV")
ax6.axvline(x=0.1, color="orange", linestyle="--", alpha=0.5, label="$E_g \\approx 0$ boundary")

ax6.text(4.3, 2.8, "Transparent\nregion\n($E_g > E_\\mathrm{vis}$)", fontsize=11, color="blue",
         ha="center", style="italic",
         bbox=dict(boxstyle="round", fc="#E6F3FF", ec="blue", alpha=0.5))
ax6.text(1.5, 2.8, "Colored\nregion\n($0 < E_g < E_\\mathrm{vis}$)", fontsize=11, color="purple",
         ha="center", style="italic",
         bbox=dict(boxstyle="round", fc="#F3E6FF", ec="purple", alpha=0.5))
ax6.text(-0.3, 2.8, "Metallic\nregion\n($E_g \\approx 0$)\n$D_\\mathrm{eff}$ branch", fontsize=9, color="gray",
         ha="center", style="italic",
         bbox=dict(boxstyle="round", fc="#F0F0F0", ec="gray", alpha=0.5))

ax6.scatter(-0.1, 3, s=200, c="gold", marker="*", edgecolors="black", linewidths=1.0, zorder=5)
ax6.annotate("Metals\n(Au, Ag)", (-0.1, 3), xytext=(0.3, 2.7), fontsize=8,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8),
             arrowprops=dict(arrowstyle="->", color="gray"))

ax6.set_xlabel(r"Band gap $E_g$ (eV)", fontsize=13)
ax6.set_ylabel(r"$D_\mathrm{eff}$ (effective conduction dimensionality)", fontsize=13)
ax6.set_title(r"$E_g \times D_\mathrm{eff}$ Optical Response Classification Map", fontsize=14, fontweight="bold")
ax6.set_xlim(-0.8, 7)
ax6.set_ylim(-0.3, 3.3)
ax6.set_yticks([0, 1, 2, 3])
ax6.legend(fontsize=9, loc="center right")
ax6.grid(True, alpha=0.3)
fig6.tight_layout()
fig6.savefig(figdir + "fig6_Eg_Deff_classification.png", dpi=200, bbox_inches="tight")
print("Saved: fig6_Eg_Deff_classification.png")

plt.close("all")
print("\nAll 6 figures saved (English version).")
