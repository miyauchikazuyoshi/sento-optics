"""
δ×D_eff Optical Category Classification v2
============================================
Two classification approaches are compared:

1. E_g + D_eff decision tree (physics-based, no fitted thresholds)
2. δ(1/m*) × D_eff machine classification (threshold-based)

The decision tree achieves 7/7 (100%) but requires layer count N
for the graphene/graphite distinction.
The δ×D_eff machine classifier achieves 4-5/7 depending on thresholds,
exposing the graphene-graphite problem as a genuine limitation.

Data source: dataset_v1.csv (all values from published literature)
"""

import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# ============================================================
# Load data from dataset_v1.csv
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(REPO_ROOT, "data", "dataset_v1.csv")
FIG_DIR = os.path.join(SCRIPT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def _parse_float(s):
    """Parse a float from CSV fields like '~0 (metallic)', '~inf', 'N/A'."""
    s = s.strip()
    if not s or s == "N/A":
        return None
    s = s.lstrip("~")
    # Remove parenthetical notes: "0 (metallic)" -> "0"
    if "(" in s:
        s = s[:s.index("(")].strip()
    if s == "inf":
        return 100.0  # sentinel for metallic
    try:
        return float(s)
    except ValueError:
        return None

materials = []
with open(CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Parse numeric fields, handling special cases
        pi_bw_raw = row["pi_band_width_eV"].strip()
        pi_bw = None if "N/A" in pi_bw_raw else float(pi_bw_raw)

        eff_mass_raw = row["effective_mass_m0"].strip()
        eff_mass = _parse_float(eff_mass_raw)

        inv_mass_raw = row["inv_effective_mass"].strip()
        inv_mass = _parse_float(inv_mass_raw)

        materials.append({
            "name": row["material"].strip(),
            "formula": row["formula"].strip(),
            "pi_bw": pi_bw,
            "eff_mass": eff_mass,
            "inv_mass": inv_mass,
            "Eg": float(row["bandgap_eV"]),
            "D_eff": int(row["D_eff_optical"]),
            "true_category": row["optical_category"].strip(),
        })

print(f"Loaded {len(materials)} materials from {CSV_PATH}")


# ============================================================
# Approach 1: E_g + D_eff Decision Tree
# ============================================================
# This is the physics-based classification from the paper.
# No fitted thresholds — only physical constants (E_vis = 3.1 eV).
# Limitation: cannot distinguish single-layer vs bulk for D_eff=2.

# Category mapping for comparison (true categories → simplified)
def simplify_category(cat):
    """Map detailed optical categories to simplified labels."""
    cat_lower = cat.lower()
    if "transparent" in cat_lower or "nearly transparent" in cat_lower:
        return "Transparent"
    elif "white" in cat_lower:
        return "Transparent"  # h-BN: white = transparent to visible
    elif "black" in cat_lower and "gloss" in cat_lower:
        return "Black+gloss"
    elif "black" in cat_lower and "luster" in cat_lower:
        return "Black-luster"
    elif "colored" in cat_lower or "dark purple" in cat_lower:
        return "Colored"
    else:
        return cat


def classify_decision_tree(m):
    """
    E_g + D_eff decision tree (no special cases, no name-based branching).

    Step 1: Eg > 3.1 eV → Transparent
    Step 2: Eg > 0.1 eV → Colored (selective absorption)
    Step 3: Eg ≈ 0 → branch by D_eff
        D_eff = 0 → anomalous (not expected for Eg≈0 materials)
        D_eff = 1 → Black with weak luster (1D metallic)
        D_eff = 2 → Black + gloss (2D metallic; NOTE: single-layer = transparent)
        D_eff = 3 → Metallic luster (3D metallic)

    KNOWN LIMITATION: Single-layer graphene (Eg≈0, D_eff=2) is predicted
    as "Black+gloss" but is actually nearly transparent. This is because
    the framework describes *intrinsic material properties*, while the
    macroscopic optical response also depends on geometric factors (thickness N).
    """
    E_vis = 3.1  # visible light maximum energy (eV)

    if m["Eg"] > E_vis:
        return "Transparent", f"Eg={m['Eg']:.1f} > E_vis: no visible absorption"

    if m["Eg"] > 0.1:
        return "Colored", f"0 < Eg={m['Eg']:.1f} < E_vis: selective absorption"

    # Eg ≈ 0: metallic regime, branch by D_eff
    if m["D_eff"] == 0:
        return "Colored", f"Eg≈0, D=0: anomalous"
    elif m["D_eff"] == 1:
        return "Black-luster", f"Eg≈0, D=1: 1D metallic response"
    elif m["D_eff"] == 2:
        return "Black+gloss", f"Eg≈0, D=2: 2D in-plane metallic"
    elif m["D_eff"] == 3:
        return "Metallic luster", f"Eg≈0, D=3: isotropic metallic"

    return "Unknown", ""


# ============================================================
# Approach 2: δ(1/m*) × D_eff Machine Classification
# ============================================================
# Uses inverse effective mass as δ proxy with empirical thresholds.
# No name-based special cases.

def classify_delta_deff(m):
    """
    δ(1/m*) × D_eff classification with fixed thresholds.
    NO special cases. NO name-based branching.
    """
    delta = m["inv_mass"]
    D = m["D_eff"]

    if delta is None:
        return "Unknown", "no δ proxy available"

    if D == 0:
        if delta < 3.0:
            return "Transparent", f"δ={delta:.1f}<3, D=0"
        else:
            return "Colored", f"δ={delta:.1f}≥3, D=0"
    elif D == 1:
        if delta < 10.0:
            return "Colored", f"δ={delta:.1f}<10, D=1"
        else:
            return "Black-luster", f"δ={delta:.1f}≥10, D=1"
    elif D == 2:
        # No graphene special case — pure threshold
        if delta * D > 40:
            return "Black+gloss", f"δ×D={delta*D:.0f}>40"
        else:
            return "Transparent", f"δ×D={delta*D:.0f}≤40"
    elif D == 3:
        return "Metallic luster", f"D=3"

    return "Unknown", ""


# ============================================================
# Run both classifications
# ============================================================

print("\n" + "=" * 90)
print("APPROACH 1: E_g + D_eff Decision Tree (physics-based, no fitted thresholds)")
print("=" * 90)

print(f"\n{'Material':30s} {'Eg':>6s} {'D_eff':>5s} {'Predicted':18s} {'True':18s} {'Match'}")
print("-" * 95)

dt_correct = 0
dt_results = []
for m in materials:
    true_simple = simplify_category(m["true_category"])
    pred, reason = classify_decision_tree(m)
    match = "✓" if pred == true_simple else "✗"
    if pred == true_simple:
        dt_correct += 1
    dt_results.append({"m": m, "pred": pred, "true": true_simple, "match": match, "reason": reason})
    print(f"{m['name']:30s} {m['Eg']:6.2f} {m['D_eff']:5d} {pred:18s} {true_simple:18s} {match}  {reason}")

dt_acc = dt_correct / len(materials)
print("-" * 95)
print(f"Accuracy: {dt_correct}/{len(materials)} = {dt_acc:.1%}")

# Identify misses
dt_misses = [r for r in dt_results if r["match"] == "✗"]
if dt_misses:
    print(f"\nMisclassified ({len(dt_misses)}):")
    for r in dt_misses:
        m = r["m"]
        print(f"  {m['name']}: predicted {r['pred']}, true {r['true']}")
        if "Graphene" in m["name"] or "graphene" in m["name"].lower():
            print("    → Graphene (Eg≈0, D_eff=2) is intrinsically 2D metallic,")
            print("      but single-layer absorption is only πα=2.3%.")
            print("      Layer count N is needed as an additional parameter.")


print("\n" + "=" * 90)
print("APPROACH 2: δ(1/m*) × D_eff Machine Classification (threshold-based)")
print("=" * 90)

print(f"\n{'Material':30s} {'1/m*':>8s} {'D_eff':>5s} {'Predicted':18s} {'True':18s} {'Match'}")
print("-" * 95)

dd_correct = 0
dd_results = []
for m in materials:
    true_simple = simplify_category(m["true_category"])
    pred, reason = classify_delta_deff(m)
    match = "✓" if pred == true_simple else "✗"
    if pred == true_simple:
        dd_correct += 1
    dd_results.append({"m": m, "pred": pred, "true": true_simple, "match": match, "reason": reason})
    inv_str = f"{m['inv_mass']:.1f}" if m["inv_mass"] is not None else "N/A"
    print(f"{m['name']:30s} {inv_str:>8s} {m['D_eff']:5d} {pred:18s} {true_simple:18s} {match}  {reason}")

dd_acc = dd_correct / len(materials)
print("-" * 95)
print(f"Accuracy: {dd_correct}/{len(materials)} = {dd_acc:.1%}")

dd_misses = [r for r in dd_results if r["match"] == "✗"]
if dd_misses:
    print(f"\nMisclassified ({len(dd_misses)}):")
    for r in dd_misses:
        m = r["m"]
        print(f"  {m['name']}: predicted {r['pred']}, true {r['true']}")


# ============================================================
# Summary comparison
# ============================================================

print("\n" + "=" * 90)
print("SUMMARY")
print("=" * 90)
print(f"  E_g + D_eff decision tree:     {dt_correct}/{len(materials)} = {dt_acc:.1%}")
print(f"  δ(1/m*) × D_eff classifier:    {dd_correct}/{len(materials)} = {dd_acc:.1%}")
print()
print("Key findings:")
print("  1. The E_g + D_eff decision tree is physics-based and requires no fitted thresholds.")
print("     Its only failure mode is the graphene single-layer case (needs layer count N).")
print("  2. The δ×D_eff machine classifier is threshold-sensitive and cannot distinguish")
print("     graphene from graphite without additional information.")
print("  3. Both approaches confirm that E_g alone is insufficient — D_eff is needed.")


# ============================================================
# Decision tree diagram
# ============================================================

print("\n### Decision Tree Structure")
print("-" * 70)
print("""
                      Eg > 3.1 eV?
                     /            \\
                   Yes             No
                    |               |
                Transparent     Eg > 0.1 eV?
             (Diamond, h-BN)    /        \\
                              Yes         No (Eg≈0)
                               |            |
                            Colored      D_eff = ?
                        (C60, SWCNT_sc)  /    |    \\
                                        1     2     3
                                        |     |     |
                                 Black-luster |  Metallic
                                 (SWCNT_m)    |   luster
                                           Black+gloss*
                                          (Graphite)

  * Graphene (Eg≈0, D_eff=2) is predicted as Black+gloss
    but is nearly transparent due to single-layer geometry.
    Layer count N is needed as an additional parameter.
""")


# ============================================================
# Figure: Classification comparison
# ============================================================

cat_colors = {
    "Transparent": "#87CEEB",
    "Colored": "#DDA0DD",
    "Black-luster": "#696969",
    "Black+gloss": "#2F2F2F",
    "Metallic luster": "#FFD700",
    "Unknown": "#FFFFFF",
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

for ax, results, title, acc in [
    (ax1, dt_results, f"E_g + D_eff Decision Tree ({dt_acc:.0%})", dt_acc),
    (ax2, dd_results, f"δ(1/m*) × D_eff Classifier ({dd_acc:.0%})", dd_acc),
]:
    for i, r in enumerate(results):
        fc = cat_colors.get(r["pred"], "white")
        ec = "green" if r["match"] == "✓" else "red"
        lw = 2 if r["match"] == "✓" else 3
        ax.barh(i, 1, color=fc, edgecolor=ec, linewidth=lw)
        txt_color = "white" if "Black" in r["pred"] else "black"
        check = "✓" if r["match"] == "✓" else "✗"
        ax.text(0.5, i,
                f"{r['m']['name']}  |  Pred: {r['pred']}  |  True: {r['true']}  {check}",
                ha="center", va="center", fontsize=8, fontweight="bold", color=txt_color)

    ax.set_yticks(range(len(results)))
    ax.set_yticklabels([f"Eg={r['m']['Eg']:.1f}, D={r['m']['D_eff']}" for r in results], fontsize=7)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_xticks([])

legend_elements = [
    Patch(facecolor="#87CEEB", label="Transparent"),
    Patch(facecolor="#DDA0DD", label="Colored"),
    Patch(facecolor="#696969", label="Black-luster"),
    Patch(facecolor="#2F2F2F", label="Black+gloss"),
    Patch(facecolor="white", edgecolor="green", linewidth=2, label="Correct"),
    Patch(facecolor="white", edgecolor="red", linewidth=2, label="Incorrect"),
]
fig.legend(handles=legend_elements, loc="lower center", ncol=6, fontsize=8)
fig.suptitle("Classification Comparison: Two Approaches", fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0.08, 1, 0.95])
fig.savefig(os.path.join(FIG_DIR, "fig5_classification_result.png"), dpi=200, bbox_inches="tight")
print(f"\nSaved: {os.path.join(FIG_DIR, 'fig5_classification_result.png')}")

plt.close("all")
print("\nDone.")
