"""
Plot Wannier spread summary and correlation with surface tension.
"""

import numpy as np
import matplotlib.pyplot as plt

# Wannier spread results (Ang^2)
# For Cu and Zn, separate s and d contributions
data = {
    'Na': {'type': 'sp', 'num_wann': 1, 'avg_spread': 11.7339,
           's_spread': 11.7339, 'd_spread': None,
           'gamma': 191, 'color': 'royalblue'},
    'K':  {'type': 'sp', 'num_wann': 1, 'avg_spread': 3.7481,
           's_spread': 3.7481, 'd_spread': None,
           'gamma': 110, 'color': 'dodgerblue'},
    'Al': {'type': 'sp', 'num_wann': 1, 'avg_spread': 12.9249,
           's_spread': 12.9249, 'd_spread': None,
           'gamma': 1140, 'color': 'steelblue'},
    'Cu': {'type': 'd', 'num_wann': 6, 'avg_spread': 1.9482,
           's_spread': 9.405, 'd_spread': np.mean([0.514, 0.369, 0.514, 0.373, 0.514]),
           'gamma': 1330, 'color': 'orangered'},
    'Zn': {'type': 'd', 'num_wann': 12, 'avg_spread': 0.6714,
           's_spread': np.mean([2.266, 2.266]), 'd_spread': np.mean([0.349, 0.349, 0.351, 0.351, 0.363, 0.349, 0.349, 0.351, 0.351, 0.363]),
           'gamma': 780, 'color': 'darkorange'},
}

# Valence n_mid/n_bulk from ablation study
val_n_ratio = {
    'Na': 1.093, 'K': 1.130, 'Al': 0.963,
    'Cu': 0.329, 'Zn': 0.279,
}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: Wannier spread by metal (s-orbital spread)
ax = axes[0]
names = list(data.keys())
s_spreads = [data[n]['s_spread'] for n in names]
colors = [data[n]['color'] for n in names]
bars = ax.bar(names, s_spreads, color=colors, edgecolor='black', linewidth=0.5)
ax.set_ylabel('s-orbital Wannier spread (Å²)', fontsize=12)
ax.set_title('(a) s-orbital MLWF spread', fontsize=13)
ax.axhline(y=5, color='gray', linestyle='--', alpha=0.5, label='sp/d threshold')
for i, (n, s) in enumerate(zip(names, s_spreads)):
    ax.text(i, s + 0.3, f'{s:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylim(0, 16)

# Panel 2: Wannier spread vs surface tension
ax = axes[1]
for n, d in data.items():
    marker = 'o' if d['type'] == 'sp' else 's'
    ax.scatter(d['s_spread'], d['gamma'], c=d['color'], s=100, marker=marker,
              edgecolors='black', linewidth=0.5, zorder=5)
    offset = (0.3, 20) if n != 'K' else (0.3, -40)
    ax.annotate(n, (d['s_spread'], d['gamma']),
               xytext=offset, textcoords='offset points', fontsize=11, fontweight='bold')
ax.set_xlabel('s-orbital Wannier spread (Å²)', fontsize=12)
ax.set_ylabel('Surface tension γ (mN/m)', fontsize=12)
ax.set_title('(b) Ω_s vs γ', fontsize=13)

# Panel 3: Wannier spread vs valence n_mid/n_bulk
ax = axes[2]
for n, d in data.items():
    marker = 'o' if d['type'] == 'sp' else 's'
    ax.scatter(d['s_spread'], val_n_ratio[n], c=d['color'], s=100, marker=marker,
              edgecolors='black', linewidth=0.5, zorder=5)
    offset = (0.3, 0.01) if n != 'K' else (0.3, -0.05)
    ax.annotate(n, (d['s_spread'], val_n_ratio[n]),
               xytext=(8, 0), textcoords='offset points', fontsize=11, fontweight='bold')
ax.set_xlabel('s-orbital Wannier spread (Å²)', fontsize=12)
ax.set_ylabel('Valence n_mid / n_bulk', fontsize=12)
ax.set_title('(c) Ω_s vs boundary density', fontsize=13)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('fig_wannier_summary.png', dpi=150, bbox_inches='tight')
print("Saved fig_wannier_summary.png")
plt.close()

# Print summary table
print("\n" + "="*60)
print(f"{'Metal':>5}  {'Type':>4}  {'Ω_s (Å²)':>10}  {'Ω_d (Å²)':>10}  {'γ (mN/m)':>10}  {'n_mid/n_bulk':>12}")
print("="*60)
for n, d in data.items():
    d_str = f"{d['d_spread']:.3f}" if d['d_spread'] is not None else "   -"
    print(f"{n:>5}  {d['type']:>4}  {d['s_spread']:>10.3f}  {d_str:>10}  {d['gamma']:>10}  {val_n_ratio[n]:>12.3f}")
