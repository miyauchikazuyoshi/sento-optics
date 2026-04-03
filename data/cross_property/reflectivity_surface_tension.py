"""
Cross-property correlation test: Reflectivity R vs Surface tension γ
for liquid metals.

Prediction (δ framework): R and γ should be positively correlated,
because both are governed by δ_elec (electronic delocalization).

No prior paper has tested this directly (Miedema & Boom 1978 is closest
but never plotted R vs γ).
"""

import numpy as np

# === Data ===
# Surface tension γ (mN/m) at melting point
# Sources: Keene (1993), Mills & Su (2006), Suryanaryana & Mika (2019)
#
# Reflectivity R at ~550nm (visible), normal incidence
# Sources: Johnson & Christy (1972/1974), Rakic (1998), Palik,
#          Miller (1969) for liquid, Siegel (1976) for liquid calc.
#
# Note: Most R data is for solid metals. For liquid metals, R changes
# slightly upon melting (typically decreases by a few %). We use solid
# R as a proxy — the ranking should be preserved.

metals = {
    # metal: (γ mN/m, R at ~550nm, type)
    'K':  (120,  0.96, 'sp'),   # alkali, very high R in IR, ~0.96 visible
    'Na': (210,  0.97, 'sp'),   # alkali
    'Hg': (485,  0.74, 'sp'),   # liquid at RT, Inagaki 1981
    'Pb': (480,  0.62, 'sp-p'), # Johnson & Christy
    'Sn': (610,  0.79, 'sp-p'), # Palik
    'Ga': (720,  0.76, 'sp-p'), # Schulz 1957 / Kofman
    'Zn': (800,  0.60, 'd'),    # d-metal
    'Al': (1020, 0.92, 'sp'),   # Rakic 1998
    'Ag': (960,  0.98, 'd'),    # Johnson & Christy 1972
    'Au': (1190, 0.81, 'd'),    # Johnson & Christy 1972 (interband at 550nm)
    'Cu': (1400, 0.62, 'd'),    # Johnson & Christy 1972 (interband at 550nm)
    'Ni': (1850, 0.66, 'd'),    # Johnson & Christy 1974
    'Fe': (1930, 0.56, 'd'),    # Johnson & Christy 1974
}

names = list(metals.keys())
gamma = np.array([metals[m][0] for m in names])
R = np.array([metals[m][1] for m in names])
types = [metals[m][2] for m in names]

# === Correlation ===
from scipy import stats

r_all, p_all = stats.pearsonr(gamma, R)
r_sp, p_sp = stats.spearmanr(gamma, R)

print("=== R vs γ correlation (all metals) ===")
print(f"Pearson r = {r_all:.3f}, p = {p_all:.4f}")
print(f"Spearman ρ = {r_sp:.3f}, p = {p_sp:.4f}")
print()

# Separate sp and d metals
sp_mask = np.array(['sp' in t for t in types])
d_mask = np.array(['d' in t and 'sp' not in t for t in types])

if sp_mask.sum() >= 3:
    r_sp_only, p_sp_only = stats.pearsonr(gamma[sp_mask], R[sp_mask])
    print(f"sp metals only: r = {r_sp_only:.3f}, p = {p_sp_only:.4f} (n={sp_mask.sum()})")

if d_mask.sum() >= 3:
    r_d_only, p_d_only = stats.pearsonr(gamma[d_mask], R[d_mask])
    print(f"d metals only:  r = {r_d_only:.3f}, p = {p_d_only:.4f} (n={d_mask.sum()})")

print()
print("=== Per-metal data ===")
print(f"{'Metal':<5} {'γ(mN/m)':>8} {'R(550nm)':>9} {'Type':>6}")
print("-" * 32)
for m in names:
    g, r, t = metals[m]
    print(f"{m:<5} {g:>8} {r:>9.2f} {t:>6}")

# === Plot ===
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))

    colors = {'sp': '#38bdf8', 'd': '#818cf8', 'sp-p': '#22d3ee'}

    for m in names:
        g, r, t = metals[m]
        base_t = 'sp' if 'sp' in t else 'd'
        c = colors.get(t, colors[base_t])
        ax.scatter(g, r, c=c, s=80, zorder=3, edgecolors='white', linewidths=0.5)
        ax.annotate(m, (g, r), textcoords="offset points",
                    xytext=(6, 6), fontsize=9, color='#cbd5e1')

    # Trend line
    z = np.polyfit(gamma, R, 1)
    x_line = np.linspace(gamma.min() - 50, gamma.max() + 50, 100)
    ax.plot(x_line, np.polyval(z, x_line), '--', color='#475569', linewidth=1,
            label=f'Linear fit: r={r_all:.2f}, p={p_all:.3f}')

    ax.set_xlabel('Surface tension γ (mN/m)', fontsize=12, color='#e2e8f0')
    ax.set_ylabel('Reflectivity R at ~550nm', fontsize=12, color='#e2e8f0')
    ax.set_title('δ framework prediction: R and γ should correlate\n(both governed by electronic delocalization)',
                 fontsize=11, color='#94a3b8')
    ax.legend(fontsize=10, facecolor='#1a2233', edgecolor='#2a3550', labelcolor='#e2e8f0')

    ax.set_facecolor('#0a0e17')
    fig.set_facecolor('#0a0e17')
    ax.tick_params(colors='#94a3b8')
    ax.spines['bottom'].set_color('#2a3550')
    ax.spines['left'].set_color('#2a3550')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_ylim(0.4, 1.05)

    fig.tight_layout()
    fig.savefig('/Users/miyauchikazuyoshi/Documents/GitHub/sento-optics/data/R_vs_gamma.png', dpi=150)
    print("\nPlot saved: data/R_vs_gamma.png")

except ImportError:
    print("\nmatplotlib not available, skipping plot")
