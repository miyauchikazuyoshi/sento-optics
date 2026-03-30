"""
Compare Al(111) vs Zn(0001) slab charge density profiles.
The key test: sp-metal (Al) vs d-metal (Zn) boundary density.

If δ_IPR → n_ws → γ is correct:
  - Al: sp electrons → more uniform → higher boundary density → higher γ
  - Zn: d electrons → more localized → lower boundary density → lower γ
"""

import numpy as np
import matplotlib.pyplot as plt

# ── Load data ──
al_data = np.loadtxt('al_avg.dat')
zn_data = np.loadtxt('zn_avg.dat')

bohr2ang = 0.529177

# Al(111)
al_z = al_data[:, 0] * bohr2ang  # Bohr → Ang
al_rho = al_data[:, 1]  # e/Bohr³

# Zn(0001)
zn_z = zn_data[:, 0] * bohr2ang
zn_rho = zn_data[:, 1]

# ── Slab parameters ──
al_d = 2.338  # Al(111) interlayer spacing (Ang)
zn_d = 2.474  # Zn(0001) interlayer spacing (Ang)
n_layers = 7

al_layers = np.array([i * al_d for i in range(n_layers)])
zn_layers = np.array([i * zn_d for i in range(n_layers)])

# ── Bulk density (average over central 3 layers) ──
def get_bulk_density(z, rho, layers, d):
    center_start = layers[2] - d / 2
    center_end = layers[4] + d / 2
    mask = (z > center_start) & (z < center_end)
    return np.mean(rho[mask])

al_rho_bulk = get_bulk_density(al_z, al_rho, al_layers, al_d)
zn_rho_bulk = get_bulk_density(zn_z, zn_rho, zn_layers, zn_d)

print(f"Al bulk density: {al_rho_bulk:.6f} e/Bohr³ ({al_rho_bulk/bohr2ang**3:.4f} e/Ang³)")
print(f"Zn bulk density: {zn_rho_bulk:.6f} e/Bohr³ ({zn_rho_bulk/bohr2ang**3:.4f} e/Ang³)")
print(f"Ratio Zn/Al: {zn_rho_bulk/al_rho_bulk:.3f}")

# ── Normalized profiles δ(z) = n(z)/n_bulk ──
al_delta = al_rho / al_rho_bulk
zn_delta = zn_rho / zn_rho_bulk

# ── Boundary densities ──
print(f"\n{'='*60}")
print(f"BOUNDARY DENSITIES (at interlayer midpoints)")
print(f"{'='*60}")

def get_boundary_densities(z, rho, rho_bulk, layers, label):
    """Get boundary density at each interlayer midpoint."""
    ratios = []
    for i in range(len(layers) - 1):
        z_mid = (layers[i] + layers[i + 1]) / 2
        idx = np.argmin(np.abs(z - z_mid))
        ratio = rho[idx] / rho_bulk
        loc = "surface" if i == 0 or i == len(layers) - 2 else "bulk"
        print(f"  {label} Layer {i+1}-{i+2}: n_mid/n_bulk = {ratio:.4f}  [{loc}]")
        ratios.append(ratio)
    return np.array(ratios)

print(f"\nAl(111):")
al_ratios = get_boundary_densities(al_z, al_rho, al_rho_bulk, al_layers, "Al")
print(f"\nZn(0001):")
zn_ratios = get_boundary_densities(zn_z, zn_rho, zn_rho_bulk, zn_layers, "Zn")

# Focus on bulk-like boundaries (exclude surface layers)
al_bulk_boundary = np.mean(al_ratios[1:-1])  # layers 2-3, 3-4, 4-5, 5-6
zn_bulk_boundary = np.mean(zn_ratios[1:-1])

print(f"\n{'='*60}")
print(f"KEY RESULT: Bulk-like boundary density")
print(f"{'='*60}")
print(f"  Al: n_boundary/n_bulk = {al_bulk_boundary:.4f}")
print(f"  Zn: n_boundary/n_bulk = {zn_bulk_boundary:.4f}")
print(f"  Ratio Al/Zn: {al_bulk_boundary/zn_bulk_boundary:.4f}")
print(f"")
print(f"  Experimental γ(Al)/γ(Zn) = 1140/782 = {1140/782:.3f}")
print(f"  Miedema n_ws(Al)/n_ws(Zn) ≈ 1.6 (from de Boer 1988)")
print(f"")

if al_bulk_boundary > zn_bulk_boundary:
    print(f"  ✓ Al has HIGHER boundary density than Zn")
    print(f"  ✓ Consistent with δ_IPR → n_ws → γ hypothesis")
else:
    print(f"  ✗ Al has LOWER boundary density — INCONSISTENT with hypothesis")
    print(f"  Note: This tests interstitial density, not WS boundary density")

# ── Surface boundary comparison ──
al_surface_boundary = al_ratios[-1]  # outermost midpoint
zn_surface_boundary = zn_ratios[-1]
print(f"\n  Surface boundary density:")
print(f"    Al: {al_surface_boundary:.4f}")
print(f"    Zn: {zn_surface_boundary:.4f}")

# ── Figure ──
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Al(111) vs Zn(0001): DFT Charge Density at Metal–Vacuum Interface',
             fontsize=14, fontweight='bold')

# (a) Raw charge density
ax = axes[0, 0]
# Normalize z so that the last layer is at 0 (surface reference)
al_z_surf = al_z - al_layers[-1]
zn_z_surf = zn_z - zn_layers[-1]

# Only plot the surface region
al_mask = (al_z_surf > -10) & (al_z_surf < 8)
zn_mask = (zn_z_surf > -10) & (zn_z_surf < 8)

ax.plot(al_z_surf[al_mask], al_rho[al_mask] / al_rho_bulk, 'b-', lw=1.5,
        label=f'Al (sp, γ=1140)', alpha=0.8)
ax.plot(zn_z_surf[zn_mask], zn_rho[zn_mask] / zn_rho_bulk, 'r-', lw=1.5,
        label=f'Zn (d¹⁰, γ=782)', alpha=0.8)
ax.axhline(1.0, color='gray', ls=':', alpha=0.5)
ax.axvline(0, color='gray', ls='--', alpha=0.5, label='Surface layer')
ax.set_xlabel('z − z_surface (Angstrom)')
ax.set_ylabel('n(z) / n_bulk')
ax.set_title('(a) Normalized charge density near surface')
ax.legend(fontsize=9)

# (b) Surface spillover zoom
ax = axes[0, 1]
spill_al = (al_z_surf > -3) & (al_z_surf < 6)
spill_zn = (zn_z_surf > -3) & (zn_z_surf < 6)

ax.plot(al_z_surf[spill_al], al_rho[spill_al] / al_rho_bulk, 'b-', lw=2,
        label='Al')
ax.plot(zn_z_surf[spill_zn], zn_rho[spill_zn] / zn_rho_bulk, 'r-', lw=2,
        label='Zn')
ax.axhline(1.0, color='gray', ls=':', alpha=0.5)
ax.axvline(0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('z − z_surface (Angstrom)')
ax.set_ylabel('n(z) / n_bulk')
ax.set_title('(b) Surface spillover comparison')
ax.legend()

# (c) (dδ/dz)² comparison
ax = axes[1, 0]
for z_arr, delta_arr, z_surf, mask, color, label in [
    (al_z, al_delta, al_z_surf, al_mask, 'b', 'Al'),
    (zn_z, zn_delta, zn_z_surf, zn_mask, 'r', 'Zn')]:
    dz = z_arr[1] - z_arr[0]
    ddelta = np.gradient(delta_arr, dz)
    ddelta_sq = ddelta**2

    # Shift to surface reference
    z_plot = z_arr - (al_layers[-1] if label == 'Al' else zn_layers[-1])
    plot_mask = (z_plot > -5) & (z_plot < 8)
    ax.plot(z_plot[plot_mask], ddelta_sq[plot_mask], f'{color}-', lw=1.5,
            label=label, alpha=0.8)

ax.set_xlabel('z − z_surface (Angstrom)')
ax.set_ylabel('(dδ/dz)²')
ax.set_title('(c) Delocalization gradient squared')
ax.legend()

# (d) Summary bar chart
ax = axes[1, 1]
categories = ['Bulk boundary\nn_mid/n_bulk', 'Surface boundary\nn_mid/n_bulk',
              'γ (mN/m)\n÷1000']
al_vals = [al_bulk_boundary, al_surface_boundary, 1.140]
zn_vals = [zn_bulk_boundary, zn_surface_boundary, 0.782]

x = np.arange(len(categories))
width = 0.35
bars1 = ax.bar(x - width/2, al_vals, width, label='Al (sp)', color='steelblue')
bars2 = ax.bar(x + width/2, zn_vals, width, label='Zn (d¹⁰)', color='indianred')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9)
ax.set_title('(d) Al vs Zn: boundary density and surface tension')
ax.legend()

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('../figures/fig_al_vs_zn_slab.png', dpi=200, bbox_inches='tight')
print(f"\nFigure saved: ../figures/fig_al_vs_zn_slab.png")
plt.close()
