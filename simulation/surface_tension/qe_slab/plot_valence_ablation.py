"""
Ablation study: full-electron vs valence-only boundary density.
Tests whether n_mid/n_bulk failure for Na/K is due to core electron contamination.
"""

import numpy as np
import matplotlib.pyplot as plt

bohr2ang = 0.529177

metals = {
    'Na': {'full': 'na_avg.dat', 'val': 'na_val_avg.dat',
           'd': 2.988, 'n_layers': 7, 'type': 'sp',
           'config': '3s¹', 'val_config': '3s¹ only',
           'gamma': 191, 'color': 'royalblue'},
    'K':  {'full': 'k_avg.dat',  'val': 'k_val_avg.dat',
           'd': 3.694, 'n_layers': 7, 'type': 'sp',
           'config': '4s¹', 'val_config': '4s¹ only',
           'gamma': 110, 'color': 'dodgerblue'},
    'Al': {'full': 'al_avg.dat', 'val': 'al_val_avg.dat',
           'd': 2.338, 'n_layers': 7, 'type': 'sp',
           'config': '3s²3p¹', 'val_config': '3s²3p¹ (same)',
           'gamma': 1140, 'color': 'steelblue'},
    'Cu': {'full': 'cu_avg.dat', 'val': 'cu_val_avg.dat',
           'd': 2.087, 'n_layers': 7, 'type': 'd',
           'config': '3d¹⁰4s¹', 'val_config': '3d¹⁰4s¹',
           'gamma': 1330, 'color': 'orangered'},
    'Zn': {'full': 'zn_avg.dat', 'val': 'zn_val_avg.dat',
           'd': 2.474, 'n_layers': 7, 'type': 'd',
           'config': '3d¹⁰4s²', 'val_config': '3d¹⁰4s²',
           'gamma': 782, 'color': 'indianred'},
}

def compute_boundary_ratio(datafile, d, n_layers):
    data = np.loadtxt(datafile)
    z = data[:, 0] * bohr2ang
    rho = data[:, 1]

    layers = np.array([i * d for i in range(n_layers)])

    # Bulk density (central 3 layers)
    center_start = layers[2] - d / 2
    center_end = layers[4] + d / 2
    mask = (z > center_start) & (z < center_end)
    rho_bulk = np.mean(rho[mask])

    # Boundary densities at midpoints
    ratios = []
    for i in range(n_layers - 1):
        z_mid = (layers[i] + layers[i + 1]) / 2
        idx = np.argmin(np.abs(z - z_mid))
        ratios.append(rho[idx] / rho_bulk)

    # Bulk-like boundaries (exclude surface layers)
    bulk_boundary = np.mean(ratios[1:-1])
    return bulk_boundary, z, rho, rho_bulk, layers

# Compute both full and valence for all metals
results = {}
print(f"{'Metal':>5} {'Type':>4} {'Full n_mid/n_bulk':>18} {'Valence n_mid/n_bulk':>20} {'Prediction':>12}")
print("=" * 70)

for name, p in metals.items():
    try:
        full_ratio, z_f, rho_f, rho_bulk_f, layers = compute_boundary_ratio(
            p['full'], p['d'], p['n_layers'])
        val_ratio, z_v, rho_v, rho_bulk_v, _ = compute_boundary_ratio(
            p['val'], p['d'], p['n_layers'])
    except Exception as e:
        print(f"  {name}: {e}")
        continue

    # Prediction check
    if p['type'] == 'sp':
        pred = '> 0.5' if val_ratio > 0.5 else '< 0.5 ✗'
    else:
        pred = '< 0.5' if val_ratio < 0.5 else '> 0.5 ✗'

    results[name] = {
        'full_ratio': full_ratio, 'val_ratio': val_ratio,
        'z_f': z_f, 'rho_f': rho_f, 'rho_bulk_f': rho_bulk_f,
        'z_v': z_v, 'rho_v': rho_v, 'rho_bulk_v': rho_bulk_v,
        'layers': layers,
    }

    print(f"{name:>5} ({p['type']:>2}): {full_ratio:>14.4f}     {val_ratio:>16.4f}     {pred}")

# Summary
print(f"\n{'='*70}")
sp = [r['val_ratio'] for n, r in results.items() if metals[n]['type'] == 'sp']
d = [r['val_ratio'] for n, r in results.items() if metals[n]['type'] == 'd']
print(f"Valence sp average: {np.mean(sp):.4f}")
print(f"Valence d average:  {np.mean(d):.4f}")

# ── Figure: 6-panel ablation comparison ──
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Ablation Study: Full-Electron vs Valence-Only Boundary Density',
             fontsize=14, fontweight='bold')

# (a) Full-electron bar chart
ax = axes[0, 0]
names = list(results.keys())
full_vals = [results[n]['full_ratio'] for n in names]
colors = [metals[n]['color'] for n in names]
bars = ax.bar(names, full_vals, color=colors, edgecolor='black', lw=0.5, alpha=0.7)
for bar, val in zip(bars, full_vals):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.02,
            f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('n_mid / n_bulk')
ax.set_title('(a) Full electron density')
ax.axhline(0.5, color='gray', ls='--', alpha=0.5)
ax.set_ylim(0, 1.2)

# (b) Valence-only bar chart
ax = axes[0, 1]
val_vals = [results[n]['val_ratio'] for n in names]
bars = ax.bar(names, val_vals, color=colors, edgecolor='black', lw=0.5)
for bar, val in zip(bars, val_vals):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.02,
            f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('n_mid / n_bulk (valence)')
ax.set_title('(b) Valence electrons only')
ax.axhline(0.5, color='gray', ls='--', alpha=0.5)
ax.set_ylim(0, 1.2)

# (c) Side-by-side comparison
ax = axes[0, 2]
x = np.arange(len(names))
width = 0.35
bars1 = ax.bar(x - width/2, full_vals, width, label='Full electron',
               color='lightgray', edgecolor='black', lw=0.5)
bars2 = ax.bar(x + width/2, val_vals, width, label='Valence only',
               color=[metals[n]['color'] for n in names], edgecolor='black', lw=0.5)
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylabel('n_mid / n_bulk')
ax.set_title('(c) Full vs Valence comparison')
ax.axhline(0.5, color='gray', ls='--', alpha=0.5)
ax.legend()
ax.set_ylim(0, 1.2)

# (d) Na density profiles: full vs valence
ax = axes[1, 0]
if 'Na' in results:
    r = results['Na']
    z_f = r['z_f']; z_v = r['z_v']
    # Normalize each to its own bulk
    mask_f = (z_f > 0) & (z_f < r['layers'][-1])
    mask_v = (z_v > 0) & (z_v < r['layers'][-1])
    ax.plot(z_f[mask_f], r['rho_f'][mask_f] / r['rho_bulk_f'],
            'gray', lw=1.5, label='Full (2s²2p⁶3s¹)', alpha=0.7)
    ax.plot(z_v[mask_v], r['rho_v'][mask_v] / r['rho_bulk_v'],
            'royalblue', lw=2, label='Valence (3s¹)')
    ax.set_xlabel('z (Å)')
    ax.set_ylabel('n(z) / n_bulk')
    ax.set_title('(d) Na: full vs valence profile')
    ax.legend(fontsize=8)
    ax.axhline(1.0, color='gray', ls=':', alpha=0.5)

# (e) Cu density profiles: full vs valence
ax = axes[1, 1]
if 'Cu' in results:
    r = results['Cu']
    z_f = r['z_f']; z_v = r['z_v']
    mask_f = (z_f > 0) & (z_f < r['layers'][-1])
    mask_v = (z_v > 0) & (z_v < r['layers'][-1])
    ax.plot(z_f[mask_f], r['rho_f'][mask_f] / r['rho_bulk_f'],
            'gray', lw=1.5, label='Full (all core+val)', alpha=0.7)
    ax.plot(z_v[mask_v], r['rho_v'][mask_v] / r['rho_bulk_v'],
            'orangered', lw=2, label='Valence (3d¹⁰4s¹)')
    ax.set_xlabel('z (Å)')
    ax.set_ylabel('n(z) / n_bulk')
    ax.set_title('(e) Cu: full vs valence profile')
    ax.legend(fontsize=8)
    ax.axhline(1.0, color='gray', ls=':', alpha=0.5)

# (f) Valence n_mid/n_bulk vs γ
ax = axes[1, 2]
for name, res in results.items():
    p = metals[name]
    ax.scatter(res['val_ratio'], p['gamma'],
               color=p['color'], s=120, zorder=5, edgecolors='black', lw=1)
    ax.annotate(name, (res['val_ratio'], p['gamma']),
                textcoords="offset points", xytext=(8, 5), fontsize=11)
ax.set_xlabel('n_mid / n_bulk (valence)')
ax.set_ylabel('Surface tension γ (mN/m)')
ax.set_title('(f) Valence boundary density vs γ')

plt.tight_layout()
plt.savefig('../figures/fig_valence_ablation.png', dpi=200, bbox_inches='tight')
print(f"\nFigure saved: ../figures/fig_valence_ablation.png")
plt.close()
