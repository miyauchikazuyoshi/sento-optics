#!/usr/bin/env python3
"""
Plot Wannier spread comparison: Diamond vs K-metal vs Graphite.

Panel (a): Omega/WF bar chart across systems (optical category coloring)
Panel (b): Individual WF spreads for graphite (sigma vs pi decomposition)
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# ── Data ──────────────────────────────────────────────────────────

# From this calculation
diamond_wf_spreads = [1.01628, 0.93378, 0.93378, 0.93378,
                      1.01627, 0.93377, 0.93377, 0.93377]

graphite_wf_spreads = [5.98146, 5.97573, 6.14199, 6.26738,
                       8.18615, 7.31627, 5.63835, 5.49497]

# From Paper II (K metal, 1 WF)
k_metal_omega = 3.748

# Per-WF averages
diamond_omega_per_wf = np.mean(diamond_wf_spreads)
graphite_omega_per_wf = np.mean(graphite_wf_spreads)
k_omega_per_wf = k_metal_omega  # 1 WF

# ── Figure ────────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5),
                                gridspec_kw={'width_ratios': [1, 1.2]})

# ── Panel (a): Omega/WF comparison ──

systems = ['Diamond\n(sp$^3$, insulator)', 'K metal\n(4s, metal)',
           'Graphite\n(sp$^2$+$\\pi$, semimetal)']
omega_vals = [diamond_omega_per_wf, k_omega_per_wf, graphite_omega_per_wf]
colors_a = ['#4393c3', '#d4a017', '#2d2d2d']  # blue, gold, near-black
edge_colors = ['#2166ac', '#8b6914', '#000000']

bars = ax1.bar(systems, omega_vals, color=colors_a, edgecolor=edge_colors,
               linewidth=1.2, width=0.6, zorder=3)

# Value labels on bars
for bar, val in zip(bars, omega_vals):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
             f'{val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylabel('$\\Omega$ / WF  ($\\mathrm{\\AA}^2$)', fontsize=12)
ax1.set_title('(a) Wannier spread per orbital', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 8.0)
ax1.grid(axis='y', alpha=0.3, zorder=0)
ax1.tick_params(axis='x', labelsize=9)

# Annotation: arrow showing "more delocalized"
ax1.annotate('', xy=(2.3, 7.2), xytext=(-0.3, 7.2),
             arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5))
ax1.text(1.0, 7.5, 'more delocalized  $\\rightarrow$',
         ha='center', va='bottom', fontsize=9, color='#666666', style='italic')

# ── Panel (b): Graphite individual WF spreads ──

# Sort spreads and classify sigma vs pi
spreads_sorted = sorted(enumerate(graphite_wf_spreads), key=lambda x: x[1])
sigma_threshold = 6.5  # Ang^2 — visual separation

wf_indices = list(range(1, 9))
colors_b = []
labels_added = {'sigma': False, 'pi': False}

for i, (orig_idx, spread) in enumerate(spreads_sorted):
    if spread > sigma_threshold:
        colors_b.append('#c44e52')  # red for pi
    else:
        colors_b.append('#4c72b0')  # blue for sigma

spreads_sorted_vals = [s for _, s in spreads_sorted]

bars2 = ax2.barh(range(8), spreads_sorted_vals, color=colors_b,
                 edgecolor=['#333333'] * 8, linewidth=0.8, height=0.6, zorder=3)

# Labels
for i, (orig_idx, spread) in enumerate(spreads_sorted):
    label = '$\\pi$' if spread > sigma_threshold else '$\\sigma$'
    ax2.text(spread + 0.15, i, f'{spread:.2f}', va='center', fontsize=9)

ax2.set_yticks(range(8))
ax2.set_yticklabels([f'WF {orig_idx+1}' for orig_idx, _ in spreads_sorted], fontsize=9)
ax2.set_xlabel('Spread ($\\mathrm{\\AA}^2$)', fontsize=12)
ax2.set_title('(b) Graphite: individual WF spreads', fontsize=12, fontweight='bold')
ax2.set_xlim(0, 10)
ax2.grid(axis='x', alpha=0.3, zorder=0)

# Legend for sigma/pi
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#4c72b0', edgecolor='#333', label='$\\sigma$ (sp$^2$ bonds)'),
                   Patch(facecolor='#c44e52', edgecolor='#333', label='$\\pi$ (delocalized)')]
ax2.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.9)

# Diamond reference line
ax2.axvline(x=diamond_omega_per_wf, color='#4393c3', linestyle='--', alpha=0.7, lw=1.2)
ax2.text(diamond_omega_per_wf + 0.1, 7.3, 'Diamond\navg', fontsize=8,
         color='#4393c3', va='top')

plt.tight_layout()

# Save
fig_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(fig_dir, 'fig_wannier_comparison.png')
plt.savefig(out_path, dpi=200, bbox_inches='tight')
print(f"Saved: {out_path}")

out_pdf = os.path.join(fig_dir, 'fig_wannier_comparison.pdf')
plt.savefig(out_pdf, bbox_inches='tight')
print(f"Saved: {out_pdf}")

plt.show()
