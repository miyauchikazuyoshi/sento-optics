"""
Plot planar-averaged charge density from QE slab calculation.
Identifies the surface spillover region and boundary densities.
"""

import numpy as np
import matplotlib.pyplot as plt

# Read avg.dat from average.x
data = np.loadtxt('avg.dat')
z_bohr = data[:, 0]  # z in Bohr
rho = data[:, 1]  # planar-averaged charge density (e/Bohr^3)

# Convert to Angstrom
bohr2ang = 0.529177
z_ang = z_bohr * bohr2ang

# Al(111) slab parameters
d_layer = 2.338  # interlayer spacing in Angstrom
n_layers = 7
layer_positions = np.array([i * d_layer for i in range(n_layers)])

# Cell height
c_ang = 31.366  # Angstrom (from input)

# Bulk-like density: average over the 3 central layers
# (layers 3, 4, 5 — indices 2, 3, 4)
bulk_region_start = layer_positions[2] - d_layer / 2
bulk_region_end = layer_positions[4] + d_layer / 2
bulk_mask = (z_ang > bulk_region_start) & (z_ang < bulk_region_end)
rho_bulk = np.mean(rho[bulk_mask])

print(f"Bulk-like charge density (central 3 layers): {rho_bulk:.6f} e/Bohr^3")
print(f"Bulk-like charge density: {rho_bulk / bohr2ang**3:.6f} e/Ang^3")

# Normalized density δ(z) = n(z) / n_bulk
delta_z = rho / rho_bulk

# Boundary densities at midpoints between layers
print(f"\nBoundary densities (at midpoints between layers):")
for i in range(n_layers - 1):
    z_mid = (layer_positions[i] + layer_positions[i + 1]) / 2
    idx = np.argmin(np.abs(z_ang - z_mid))
    rho_mid = rho[idx]
    ratio = rho_mid / rho_bulk
    label = "surface" if i == 0 or i == n_layers - 2 else "bulk-like"
    print(f"  Layer {i+1}-{i+2} (z={z_mid:.2f} A): "
          f"rho = {rho_mid:.6f} e/Bohr^3, "
          f"n/n_bulk = {ratio:.4f}  [{label}]")

# Surface spillover: density at the vacuum side
vacuum_start = layer_positions[-1] + d_layer
vacuum_mask = z_ang > vacuum_start
if np.any(vacuum_mask):
    rho_vacuum = rho[vacuum_mask]
    print(f"\nVacuum region density (should → 0): {np.mean(rho_vacuum):.2e} e/Bohr^3")

# ──────────────────────────────────────────────
# Figure: 3-panel plot
# ──────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(10, 12))

# Panel (a): Full charge density profile
ax = axes[0]
ax.plot(z_ang, rho, 'b-', lw=1.5)
for zl in layer_positions:
    ax.axvline(zl, color='gray', ls='--', alpha=0.4, lw=0.8)
ax.axhline(rho_bulk, color='red', ls=':', alpha=0.6, label=f'$n_{{bulk}}$ = {rho_bulk:.4f}')
ax.set_xlabel('z (Angstrom)')
ax.set_ylabel('Charge density (e/Bohr$^3$)')
ax.set_title('(a) Al(111) slab: planar-averaged charge density from DFT')
ax.legend()
ax.set_xlim(-1, c_ang * bohr2ang * 0.6)  # Show slab + some vacuum

# Panel (b): δ(z) = n(z)/n_bulk
ax = axes[1]
ax.plot(z_ang, delta_z, 'b-', lw=1.5)
for zl in layer_positions:
    ax.axvline(zl, color='gray', ls='--', alpha=0.4, lw=0.8)
ax.axhline(1.0, color='red', ls=':', alpha=0.6, label='δ = 1 (bulk)')
ax.set_xlabel('z (Angstrom)')
ax.set_ylabel('δ(z) = n(z) / n$_{bulk}$')
ax.set_title('(b) Delocalization profile: δ(z) at the metal–vacuum interface')
ax.legend()
ax.set_xlim(-1, c_ang * bohr2ang * 0.6)

# Panel (c): Surface region zoom — the money plot
ax = axes[2]
# Focus on the last 3 layers + vacuum
z_focus_start = layer_positions[-3] - 1
z_focus_end = layer_positions[-1] + 8  # 8 Ang into vacuum
focus_mask = (z_ang > z_focus_start) & (z_ang < z_focus_end)

ax.plot(z_ang[focus_mask], rho[focus_mask], 'b-', lw=2)
for zl in layer_positions:
    if zl > z_focus_start:
        ax.axvline(zl, color='gray', ls='--', alpha=0.4, lw=0.8)
ax.axhline(rho_bulk, color='red', ls=':', alpha=0.6, label='$n_{bulk}$')

# Mark the spillover region
ax.fill_between(z_ang[focus_mask], 0, rho[focus_mask],
                where=(z_ang[focus_mask] > layer_positions[-1]),
                alpha=0.2, color='orange', label='Spillover into vacuum')

# Mark boundary density at last interlayer midpoint
z_last_mid = (layer_positions[-2] + layer_positions[-1]) / 2
idx_last_mid = np.argmin(np.abs(z_ang - z_last_mid))
ax.plot(z_last_mid, rho[idx_last_mid], 'ro', ms=10, zorder=5,
        label=f'Surface boundary: n = {rho[idx_last_mid]:.4f}')

ax.set_xlabel('z (Angstrom)')
ax.set_ylabel('Charge density (e/Bohr$^3$)')
ax.set_title('(c) Surface region: charge spillover and boundary density')
ax.legend()

plt.tight_layout()
plt.savefig('../figures/fig_al111_slab_density.png', dpi=200, bbox_inches='tight')
print(f"\nFigure saved: ../figures/fig_al111_slab_density.png")
plt.close()

# ──────────────────────────────────────────────
# Compute (dδ/dz)² profile
# ──────────────────────────────────────────────
dz = z_ang[1] - z_ang[0]
ddelta_dz = np.gradient(delta_z, dz)
ddelta_sq = ddelta_dz ** 2

# Integral of (dδ/dz)² — the original hypothesis (falsified for jellium,
# but let's see what real DFT gives)
integral = np.trapezoid(ddelta_sq, z_ang)
print(f"\n∫(dδ/dz)² dz = {integral:.4f} (1/Ang)")
print(f"This is the REAL DFT value, not the jellium approximation.")
