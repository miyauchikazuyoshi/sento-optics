"""
Analyze valence n_mid/n_bulk for all 14 metals (5 existing + 9 new).
Tests sp/d bifurcation hypothesis across expanded element set.
"""

import numpy as np
import os

bohr2ang = 0.529177
QE_DIR = os.path.dirname(os.path.abspath(__file__))

# All metals with their parameters
metals = {
    # Existing 5
    'Na': {'val': 'na_val_avg.dat', 'd': 2.988, 'n_layers': 7,
           'type': 'sp', 'gamma': 191},
    'K':  {'val': 'k_val_avg.dat',  'd': 3.694, 'n_layers': 7,
           'type': 'sp', 'gamma': 101},
    'Al': {'val': 'al_val_avg.dat', 'd': 2.338, 'n_layers': 7,
           'type': 'sp', 'gamma': 1050},
    'Cu': {'val': 'cu_val_avg.dat', 'd': 2.087, 'n_layers': 7,
           'type': 'd', 'gamma': 1285},
    'Zn': {'val': 'zn_val_avg.dat', 'd': 2.474, 'n_layers': 7,
           'type': 'd', 'gamma': 782},
    # New 9
    'Li': {'val': 'li_val_avg.dat',
           'd': 3.49 * np.sqrt(2) / 2,  # BCC(110) interlayer
           'n_layers': 7, 'type': 'sp', 'gamma': 398},
    'Be': {'val': 'be_val_avg.dat', 'd': 3.58 / 2,  # HCP c/2
           'n_layers': 7, 'type': 'sp', 'gamma': 1145},
    'Mg': {'val': 'mg_val_avg.dat', 'd': 5.21 / 2,
           'n_layers': 7, 'type': 'sp', 'gamma': 559},
    'Ca': {'val': 'ca_val_avg.dat',
           'd': 5.58 / np.sqrt(3),  # FCC(111)
           'n_layers': 7, 'type': 'sp', 'gamma': 361},
    'Si': {'val': 'si_val_avg.dat',
           'd': 5.43 / np.sqrt(3),  # diamond(111), approximate
           'n_layers': 8, 'type': 'sp3', 'gamma': 865},
    'Ga': {'val': 'ga_val_avg.dat',
           'd': 4.51 / np.sqrt(3),
           'n_layers': 7, 'type': 'd', 'gamma': 718},  # has 3d10 core
    'Ti': {'val': 'ti_val_avg.dat', 'd': 4.69 / 2,
           'n_layers': 7, 'type': 'd', 'gamma': 1650},
    'Ag': {'val': 'ag_val_avg.dat',
           'd': 4.09 / np.sqrt(3),
           'n_layers': 7, 'type': 'd', 'gamma': 903},
    'Fe': {'val': 'fe_val_avg.dat',
           'd': 2.87 * np.sqrt(2) / 2,  # BCC(110)
           'n_layers': 7, 'type': 'd', 'gamma': 1872},
}


def compute_boundary_ratio(datafile, d, n_layers):
    """Compute n_mid/n_bulk from planar average data."""
    filepath = os.path.join(QE_DIR, datafile)
    data = np.loadtxt(filepath)
    z = data[:, 0] * bohr2ang  # Convert bohr to angstrom
    rho = data[:, 1]

    layers = np.array([i * d for i in range(n_layers)])

    # Bulk density: average over central 3 layers
    center_start = layers[2] - d / 2
    center_end = layers[4] + d / 2
    mask = (z > center_start) & (z < center_end)
    if mask.sum() == 0:
        # Try broader range
        mask = (z > layers[1]) & (z < layers[5])
    rho_bulk = np.mean(rho[mask]) if mask.sum() > 0 else 1.0

    # Boundary densities at midpoints (exclude surface layers)
    ratios = []
    for i in range(1, n_layers - 2):  # skip first and last boundary
        z_mid = (layers[i] + layers[i + 1]) / 2
        idx = np.argmin(np.abs(z - z_mid))
        if rho_bulk > 0:
            ratios.append(rho[idx] / rho_bulk)

    return np.mean(ratios) if ratios else 0.0


# === Compute all ===
print("=" * 70)
print("14-Metal Slab Analysis: Valence n_mid/n_bulk")
print("=" * 70)
print(f"\n{'Metal':>5} {'Type':>5} {'n_mid/n_bulk':>12} {'gamma':>8} {'Prediction':>12}")
print("-" * 50)

results = {}
for name, p in sorted(metals.items(), key=lambda x: x[1]['type']):
    try:
        ratio = compute_boundary_ratio(p['val'], p['d'], p['n_layers'])
        results[name] = {'ratio': ratio, 'type': p['type'], 'gamma': p['gamma']}

        # Prediction check
        if p['type'] in ('sp', 'sp3'):
            pred = 'PASS' if ratio > 0.4 else 'FAIL'
        else:
            pred = 'PASS' if ratio < 0.5 else 'FAIL'

        print(f"{name:>5} {p['type']:>5} {ratio:>12.3f} {p['gamma']:>8} {pred:>12}")
    except Exception as e:
        print(f"{name:>5} {p['type']:>5} {'ERROR':>12} {p['gamma']:>8} {str(e)[:20]}")

# === Statistics ===
print("\n" + "=" * 70)
print("STATISTICS")
print("=" * 70)

sp_ratios = [r['ratio'] for r in results.values() if r['type'] in ('sp', 'sp3')]
d_ratios = [r['ratio'] for r in results.values() if r['type'] == 'd']
sp_names = [n for n, r in results.items() if r['type'] in ('sp', 'sp3')]
d_names = [n for n, r in results.items() if r['type'] == 'd']

print(f"\nsp metals ({len(sp_ratios)}): {', '.join(sp_names)}")
print(f"  ratios: {[f'{r:.3f}' for r in sp_ratios]}")
print(f"  mean: {np.mean(sp_ratios):.3f} ± {np.std(sp_ratios):.3f}")

print(f"\nd metals ({len(d_ratios)}): {', '.join(d_names)}")
print(f"  ratios: {[f'{r:.3f}' for r in d_ratios]}")
print(f"  mean: {np.mean(d_ratios):.3f} ± {np.std(d_ratios):.3f}")

if d_ratios:
    ratio = np.mean(sp_ratios) / np.mean(d_ratios)
    print(f"\nsp/d ratio: {ratio:.1f}x (was 3.5x for 5 metals)")

# t-test
from scipy import stats
if len(sp_ratios) >= 2 and len(d_ratios) >= 2:
    t, p = stats.ttest_ind(sp_ratios, d_ratios)
    print(f"t-test: t = {t:.2f}, p = {p:.6f}")
    print(f"  {'SIGNIFICANT' if p < 0.05 else 'NOT significant'} at p < 0.05")

# === Plot ===
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.set_facecolor('#0a0e17')
    for ax in axes:
        ax.set_facecolor('#0a0e17')
        ax.tick_params(colors='#94a3b8')
        for s in ['bottom', 'left']:
            ax.spines[s].set_color('#2a3550')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Left: bar chart of n_mid/n_bulk
    ax = axes[0]
    names_sorted = sorted(results.keys(),
                          key=lambda x: (-1 if results[x]['type'] in ('sp','sp3') else 1,
                                         -results[x]['ratio']))
    colors = ['#38bdf8' if results[n]['type'] in ('sp', 'sp3') else '#818cf8'
              for n in names_sorted]
    ratios_sorted = [results[n]['ratio'] for n in names_sorted]

    bars = ax.bar(range(len(names_sorted)), ratios_sorted, color=colors,
                  edgecolor='white', linewidth=0.5)
    ax.set_xticks(range(len(names_sorted)))
    ax.set_xticklabels(names_sorted, rotation=45)
    ax.set_ylabel('Valence n_mid/n_bulk', color='#e2e8f0')
    ax.set_title('14-Metal Slab: sp vs d Boundary Density', color='#e2e8f0')
    ax.axhline(0.5, color='#475569', linestyle=':', alpha=0.5)

    # Legend
    from matplotlib.patches import Patch
    ax.legend([Patch(facecolor='#38bdf8'), Patch(facecolor='#818cf8')],
              ['sp metals', 'd metals'], facecolor='#1a2233',
              edgecolor='#2a3550', labelcolor='#e2e8f0')

    # Right: n_mid/n_bulk vs gamma
    ax = axes[1]
    for n, r in results.items():
        c = '#38bdf8' if r['type'] in ('sp', 'sp3') else '#818cf8'
        ax.scatter(r['gamma'], r['ratio'], c=c, s=60, zorder=3,
                   edgecolors='w', linewidths=0.5)
        ax.annotate(n, (r['gamma'], r['ratio']), xytext=(4, 4),
                    textcoords='offset points', fontsize=8, color='#cbd5e1')

    ax.set_xlabel('Surface tension γ (mN/m)', color='#e2e8f0')
    ax.set_ylabel('Valence n_mid/n_bulk', color='#e2e8f0')
    ax.set_title('Boundary Density vs Surface Tension', color='#e2e8f0')
    ax.axhline(0.5, color='#475569', linestyle=':', alpha=0.5)

    fig.tight_layout()
    figpath = os.path.join(QE_DIR, '..', 'figures', 'slab_14metals.png')
    fig.savefig(figpath, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved: {figpath}")

except ImportError:
    print("\nmatplotlib not available")
