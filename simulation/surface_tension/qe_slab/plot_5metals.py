"""
Compare boundary densities across 5 metals: Na, K (sp), Al (sp), Zn (d), Cu (d).
Tests the prediction: sp metals have high n_mid/n_bulk, d metals have low.
"""

import numpy as np
import matplotlib.pyplot as plt

bohr2ang = 0.529177

# ── Metal parameters ──
metals = {
    'Na': {'file': 'na_avg.dat', 'd': 2.988, 'n_layers': 7, 'type': 'sp',
            'config': '3s¹', 'gamma': 191, 'color': 'royalblue'},
    'K':  {'file': 'k_avg.dat',  'd': 3.694, 'n_layers': 7, 'type': 'sp',
            'config': '4s¹', 'gamma': 110, 'color': 'dodgerblue'},
    'Al': {'file': 'al_avg.dat', 'd': 2.338, 'n_layers': 7, 'type': 'sp',
            'config': '3s²3p¹', 'gamma': 1140, 'color': 'steelblue'},
    'Cu': {'file': 'cu_avg.dat', 'd': 2.087, 'n_layers': 7, 'type': 'd',
            'config': '3d¹⁰4s¹', 'gamma': 1330, 'color': 'orangered'},
    'Zn': {'file': 'zn_avg.dat', 'd': 2.474, 'n_layers': 7, 'type': 'd',
            'config': '3d¹⁰4s²', 'gamma': 782, 'color': 'indianred'},
}

results = {}

for name, params in metals.items():
    try:
        data = np.loadtxt(params['file'])
    except FileNotFoundError:
        print(f"  {name}: file not found, skipping")
        continue

    z = data[:, 0] * bohr2ang
    rho = data[:, 1]

    d = params['d']
    n_layers = params['n_layers']
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

    results[name] = {
        'z': z, 'rho': rho, 'rho_bulk': rho_bulk,
        'layers': layers, 'bulk_boundary': bulk_boundary,
        'all_ratios': ratios
    }

    print(f"{name} ({params['config']}, {params['type']}): "
          f"n_mid/n_bulk = {bulk_boundary:.4f}, γ = {params['gamma']} mN/m")

print(f"\n{'='*60}")
print(f"PREDICTION TEST:")
print(f"{'='*60}")

sp_metals = {k: v for k, v in results.items() if metals[k]['type'] == 'sp'}
d_metals = {k: v for k, v in results.items() if metals[k]['type'] == 'd'}

if sp_metals and d_metals:
    sp_avg = np.mean([v['bulk_boundary'] for v in sp_metals.values()])
    d_avg = np.mean([v['bulk_boundary'] for v in d_metals.values()])
    print(f"  sp-metal average n_mid/n_bulk: {sp_avg:.4f}")
    print(f"  d-metal average n_mid/n_bulk:  {d_avg:.4f}")
    print(f"  Ratio sp/d: {sp_avg/d_avg:.2f}")

    if sp_avg > 0.5 and d_avg < 0.5:
        print(f"\n  ✓ PREDICTION CONFIRMED: sp metals have HIGH boundary density,")
        print(f"    d metals have LOW boundary density.")
    else:
        print(f"\n  Mixed result — check individual values.")

# ── Figure: 4-panel comparison ──
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Boundary Density Across 5 Metals: sp vs d Electron Delocalization',
             fontsize=14, fontweight='bold')

# (a) All density profiles, surface-referenced
ax = axes[0, 0]
for name, res in results.items():
    p = metals[name]
    z_surf = res['z'] - res['layers'][-1]
    mask = (z_surf > -8) & (z_surf < 6)
    ax.plot(z_surf[mask], res['rho'][mask] / res['rho_bulk'],
            color=p['color'], lw=1.5, label=f"{name} ({p['config']})", alpha=0.8)
ax.axhline(1.0, color='gray', ls=':', alpha=0.5)
ax.axvline(0, color='gray', ls='--', alpha=0.3)
ax.set_xlabel('z − z_surface (Å)')
ax.set_ylabel('n(z) / n_bulk')
ax.set_title('(a) Charge density profiles (surface-referenced)')
ax.legend(fontsize=8)
ax.set_ylim(-0.1, 3.5)

# (b) Bar chart: n_mid/n_bulk
ax = axes[0, 1]
names = list(results.keys())
values = [results[n]['bulk_boundary'] for n in names]
colors = [metals[n]['color'] for n in names]
bars = ax.bar(names, values, color=colors, edgecolor='black', lw=0.5)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.02,
            f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('n_mid / n_bulk')
ax.set_title('(b) Interstitial charge density ratio')
ax.axhline(0.5, color='gray', ls='--', alpha=0.5, label='sp/d boundary')
ax.legend()

# (c) n_mid/n_bulk vs γ
ax = axes[1, 0]
for name, res in results.items():
    p = metals[name]
    ax.scatter(res['bulk_boundary'], p['gamma'],
               color=p['color'], s=100, zorder=5, edgecolors='black')
    ax.annotate(name, (res['bulk_boundary'], p['gamma']),
                textcoords="offset points", xytext=(8, 5), fontsize=10)
ax.set_xlabel('n_mid / n_bulk')
ax.set_ylabel('Surface tension γ (mN/m)')
ax.set_title('(c) Boundary density vs surface tension')

# (d) Summary: sp vs d
ax = axes[1, 1]
# Create grouped comparison
sp_names = [n for n in names if metals[n]['type'] == 'sp']
d_names = [n for n in names if metals[n]['type'] == 'd']

sp_vals = [results[n]['bulk_boundary'] for n in sp_names]
d_vals = [results[n]['bulk_boundary'] for n in d_names]

x = np.arange(max(len(sp_names), len(d_names)))
width = 0.35

if sp_vals:
    ax.bar(x[:len(sp_vals)] - width/2, sp_vals, width,
           label='sp metals', color='steelblue', edgecolor='black')
    for i, (n, v) in enumerate(zip(sp_names, sp_vals)):
        ax.text(i - width/2, v + 0.02, n, ha='center', fontsize=9)

if d_vals:
    ax.bar(x[:len(d_vals)] + width/2, d_vals, width,
           label='d metals', color='indianred', edgecolor='black')
    for i, (n, v) in enumerate(zip(d_names, d_vals)):
        ax.text(i + width/2, v + 0.02, n, ha='center', fontsize=9)

ax.set_ylabel('n_mid / n_bulk')
ax.set_title('(d) sp vs d metals: systematic trend')
ax.legend()
ax.set_xticks([])

plt.tight_layout()
plt.savefig('../figures/fig_5metals_boundary.png', dpi=200, bbox_inches='tight')
print(f"\nFigure saved: ../figures/fig_5metals_boundary.png")
plt.close()
