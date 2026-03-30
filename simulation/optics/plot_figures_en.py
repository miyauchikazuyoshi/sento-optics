"""
δ×D_eff Optical Response Maps — English Version
================================================
All figures are generated from dataset_v1.csv (no hardcoded data).
Output: simulation/figures/ (overwrites existing PNGs)
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# ============================================================
# Load data from dataset_v1.csv
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # simulation/optics/ → repo root
CSV_PATH = os.path.join(REPO_ROOT, "data", "dataset_v1.csv")
FIG_DIR = os.path.join(SCRIPT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def _parse_float(s):
    """Parse a float from CSV fields like '~0 (metallic)', '~inf', 'N/A'."""
    s = s.strip()
    if not s or s == "N/A":
        return None
    s = s.lstrip("~")
    if "(" in s:
        s = s[:s.index("(")].strip()
    if s == "inf":
        return 100.0
    try:
        return float(s)
    except ValueError:
        return None

materials = []
with open(CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pi_bw_raw = row["pi_band_width_eV"].strip()
        pi_bw = None if "N/A" in pi_bw_raw else float(pi_bw_raw)

        eff_mass_raw = row["effective_mass_m0"].strip()
        eff_mass = _parse_float(eff_mass_raw)

        inv_mass_raw = row["inv_effective_mass"].strip()
        inv_mass = _parse_float(inv_mass_raw)

        materials.append({
            "name": row["material"].strip(),
            "pi_bw": pi_bw,
            "inv_mass": inv_mass,
            "Eg": float(row["bandgap_eV"]),
            "neg_Eg": -float(row["bandgap_eV"]),
            "D_eff": int(row["D_eff_optical"]),
            "category": row["optical_category"].strip(),
        })

print(f"Loaded {len(materials)} materials from {CSV_PATH}")

# Visual properties (keyed by material name for display)
STYLE = {
    "Diamond":                  {"color": "#1E90FF", "marker": "D", "label": "Diamond"},
    "C60 solid (fcc)":          {"color": "#9932CC", "marker": "p", "label": "C$_{60}$ solid"},
    "SWCNT semiconducting":     {"color": "#FF8C00", "marker": "s", "label": "SWCNT (sc)"},
    "SWCNT metallic":           {"color": "#FF4500", "marker": "s", "label": "SWCNT (m)"},
    "Graphene":                 {"color": "#228B22", "marker": "^", "label": "Graphene"},
    "Graphite":                 {"color": "#2F4F4F", "marker": "o", "label": "Graphite"},
    "h-BN":                     {"color": "#CCCCCC", "marker": "h", "label": "h-BN", "edgecolor": "#333333"},
}

def get_style(name):
    s = STYLE.get(name, {"color": "gray", "marker": "o", "label": name})
    s.setdefault("edgecolor", s["color"])
    return s

matplotlib.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']


# ============================================================
# Figure 1: delta (pi-band width) vs D_eff map
# ============================================================

fig1, ax1 = plt.subplots(figsize=(10, 7))

for m in materials:
    s = get_style(m["name"])
    bw = m["pi_bw"] if m["pi_bw"] is not None else 0.0
    ax1.scatter(bw, m["D_eff"], s=250, c=s["color"], marker=s["marker"],
                edgecolors=s["edgecolor"], linewidths=1.5, zorder=5)
    cat_short = m["category"].split("(")[0].strip()
    ax1.annotate(
        f"{s['label']}\n({cat_short})",
        (bw, m["D_eff"]),
        xytext=(bw + 0.3, m["D_eff"] + 0.08),
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
fig1.savefig(os.path.join(FIG_DIR, "fig1_delta_deff_map.png"), dpi=200, bbox_inches="tight")
print("Saved: fig1_delta_deff_map.png")


# ============================================================
# Figure 2: delta-Eg inverse correlation
# ============================================================

fig2, ax2 = plt.subplots(figsize=(9, 6))

bw_data, eg_data = [], []
for m in materials:
    s = get_style(m["name"])
    if m["pi_bw"] is None:
        continue
    ax2.scatter(m["pi_bw"], m["Eg"], s=200, c=s["color"], marker=s["marker"],
                edgecolors=s["edgecolor"], linewidths=1.5, zorder=5)
    ax2.annotate(s["label"].split("\n")[0], (m["pi_bw"], m["Eg"]),
                 xytext=(m["pi_bw"] + 0.3, m["Eg"] + 0.2), fontsize=9,
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8))
    bw_data.append(m["pi_bw"])
    eg_data.append(m["Eg"])

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
fig2.savefig(os.path.join(FIG_DIR, "fig2_delta_bandgap_correlation.png"), dpi=200, bbox_inches="tight")
print(f"Saved: fig2_delta_bandgap_correlation.png (r={r:.3f})")


# ============================================================
# Figure 3: Inverse effective mass vs D_eff
# ============================================================

fig3, ax3 = plt.subplots(figsize=(10, 7))

for m in materials:
    s = get_style(m["name"])
    if m["inv_mass"] is None:
        continue
    cat_short = m["category"].split("(")[0].strip()
    ax3.scatter(m["inv_mass"], m["D_eff"], s=250, c=s["color"], marker=s["marker"],
                edgecolors=s["edgecolor"], linewidths=1.5, zorder=5)
    ax3.annotate(
        f"{s['label']}\n({cat_short})",
        (m["inv_mass"], m["D_eff"]),
        xytext=(m["inv_mass"] * 1.3, m["D_eff"] + 0.08),
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
fig3.savefig(os.path.join(FIG_DIR, "fig3_invmass_deff_map.png"), dpi=200, bbox_inches="tight")
print("Saved: fig3_invmass_deff_map.png")


# ============================================================
# Figure 4: Indicator consistency (pairwise correlations)
# ============================================================

sp2_mats = [m for m in materials if m["pi_bw"] is not None]

fig4, axes = plt.subplots(1, 3, figsize=(15, 5))

pairs = [
    (r"$\pi$-band width (eV)", r"$1/m^*$ ($m_0^{-1}$)", "pi_bw", "inv_mass"),
    (r"$\pi$-band width (eV)", r"$-E_g$ (eV)", "pi_bw", "neg_Eg"),
    (r"$1/m^*$ ($m_0^{-1}$)", r"$-E_g$ (eV)", "inv_mass", "neg_Eg"),
]

sp2_colors = ["#9932CC", "#FF8C00", "#FF4500", "#228B22", "#2F4F4F", "#999999"]

for ax, (xname, yname, xkey, ykey) in zip(axes, pairs):
    for m, c in zip(sp2_mats, sp2_colors):
        s = get_style(m["name"])
        xval = m[xkey]
        yval = m[ykey]
        if xval is None or yval is None:
            continue
        ax.scatter(xval, yval, s=120, c=c, edgecolors="black", linewidths=0.5, zorder=5)
        ax.annotate(s["label"].split("\n")[0], (xval, yval),
                    xytext=(5, 5), textcoords="offset points", fontsize=7)
    xvals = [m[xkey] for m in sp2_mats if m[xkey] is not None]
    yvals = [m[ykey] for m in sp2_mats if m[ykey] is not None]
    r = np.corrcoef(xvals, yvals)[0, 1]
    ax.set_xlabel(xname, fontsize=10)
    ax.set_ylabel(yname, fontsize=10)
    ax.set_title(f"Pearson $r = {r:.3f}$", fontsize=11, fontweight="bold")
    ax.grid(True, alpha=0.3)

fig4.suptitle(r"Consistency among $\delta$-proxy indicators (pairwise correlations)", fontsize=13, fontweight="bold")
fig4.tight_layout()
fig4.savefig(os.path.join(FIG_DIR, "fig4_indicator_consistency.png"), dpi=200, bbox_inches="tight")
print("Saved: fig4_indicator_consistency.png")


# ============================================================
# Figure 6: Eg vs D_eff classification map
# ============================================================

cat_colors2 = {
    "Transparent": "#87CEEB", "White": "#87CEEB",
    "Nearly transparent": "#87CEEB",
    "Colored": "#9932CC",
    "Black": "#696969",
    "Black+gloss": "#2F2F2F",
    "Metallic luster": "#FFD700",
}

def get_category_color(cat):
    cat_l = cat.lower()
    if "transparent" in cat_l or "white" in cat_l:
        return "#87CEEB"
    elif "black" in cat_l and ("gloss" in cat_l or "luster" not in cat_l):
        if "gloss" in cat_l:
            return "#2F2F2F"
        return "#696969"
    elif "black" in cat_l:
        return "#696969"
    elif "colored" in cat_l or "purple" in cat_l:
        return "#9932CC"
    return "gray"

fig6, ax6 = plt.subplots(figsize=(10, 7))

for m in materials:
    s = get_style(m["name"])
    c = get_category_color(m["category"])
    ec = "black" if "Black" not in m["category"] or "gloss" not in m["category"].lower() else "white"
    ax6.scatter(m["Eg"], m["D_eff"], s=300, c=c, marker=s["marker"],
                edgecolors=ec, linewidths=1.5, zorder=5)
    ox, oy = 0.2, 0.1
    if "Graphite" in m["name"]:
        ox, oy = 0.15, -0.2
    elif "SWCNT metallic" in m["name"]:
        ox, oy = 0.1, -0.2
    elif "h-BN" in m["name"]:
        ox, oy = -1.5, 0.1
    ax6.annotate(s["label"], (m["Eg"], m["D_eff"]),
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
fig6.savefig(os.path.join(FIG_DIR, "fig6_Eg_Deff_classification.png"), dpi=200, bbox_inches="tight")
print("Saved: fig6_Eg_Deff_classification.png")

plt.close("all")
print(f"\nAll 5 figures saved to {FIG_DIR} (English version, data from {CSV_PATH}).")
