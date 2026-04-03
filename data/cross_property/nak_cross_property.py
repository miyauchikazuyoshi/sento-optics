"""
Cross-property test: NaK alloy (sp-only control experiment)

Prediction: Within sp metals (no d-electron complication),
δ_elec higher → R higher AND γ higher → positive R-γ correlation.

Data sources:
- γ: Jordan & Lane (1965), Alchagirov (2011), ACS Appl. Mater. Interfaces (2025)
- R: Calculated from Drude model using ω_p and resistivity data
  ω_p(Na) = 5.71 eV, ω_p(K) = 3.72 eV (wave-scattering.com)
  ρ: Howe & Enderby (1971), Fink & Leibowitz (1989)
- Wiedemann & Oswald (2006): R varies 92-98% across NaK composition
"""

import numpy as np
from scipy import stats

# === Data at ~100°C ===

# Composition points (Na atomic fraction)
x_Na = np.array([0.0, 0.10, 0.22, 0.40, 0.50, 0.68, 0.80, 1.0])

# Surface tension γ (mN/m) at ~100°C
# Pure Na ~195 mN/m at 100°C (Jordan & Lane: 200.2 at mp, -0.11/°C)
# Pure K ~106 mN/m at 100°C (Jordan & Lane: 110.3 at mp, -0.06/°C)
# Intermediate: concave curve, K surface segregation
# From Alchagirov (2011) and ACS (2025) data
gamma = np.array([106, 108, 118, 128, 133, 140, 160, 195])

# Resistivity ρ (μΩ·cm) at ~100°C
# Na: 9.7, K: 14.5 at 100°C
# Nearly linear (small Nordheim coefficient for NaK)
# From Howe & Enderby (1971)
rho = np.array([14.5, 14.0, 13.5, 12.5, 12.0, 11.2, 10.5, 9.7])

# Drude reflectivity calculation
# R = 1 - 2*sqrt(2*ε_0*ω / σ) for ω << ω_p (Hagen-Rubens)
# More accurately: use Drude model with plasma frequency and damping
#
# Plasma frequency: ω_p² = n_e * e² / (m* * ε_0)
# For alloy: ω_p(x) interpolated from ω_p(Na)=5.71eV, ω_p(K)=3.72eV
# Damping: γ_D = 1/τ, from ρ via σ = n_e*e²*τ/m* = ε_0*ω_p²*τ
# → τ = ε_0*ω_p² / σ_DC = ε_0*ω_p² * ρ

# Physical constants
hbar = 6.582e-16  # eV·s
e = 1.602e-19     # C
eps0 = 8.854e-12  # F/m

# Plasma frequencies (eV) - linear interpolation as rough approx
omega_p_Na = 5.71
omega_p_K = 3.72
omega_p = x_Na * omega_p_Na + (1 - x_Na) * omega_p_K  # eV

# Convert ρ to SI (Ω·m)
rho_SI = rho * 1e-8  # μΩ·cm → Ω·m

# DC conductivity
sigma_DC = 1.0 / rho_SI  # S/m

# Damping rate from Drude: γ_D = σ_DC / (ε_0 * ω_p²)
# But ω_p is in eV, need to convert to angular frequency (rad/s)
omega_p_rad = omega_p * e / (hbar * e)  # eV → rad/s: ω = E/ℏ
# Actually: ω (rad/s) = E(eV) * e / ℏ(J·s) = E(eV) / ℏ(eV·s)
omega_p_rad = omega_p / hbar  # rad/s

# τ = ε_0 * ω_p² / σ_DC ... no, Drude: σ_DC = ε_0 * ω_p² * τ
# → τ = σ_DC / (ε_0 * ω_p_rad²)
tau = sigma_DC / (eps0 * omega_p_rad**2)
gamma_D = 1.0 / tau  # damping rate (rad/s)
gamma_D_eV = gamma_D * hbar  # eV

# Drude dielectric function at 550nm (2.25 eV)
omega = 2.25 / hbar  # rad/s
omega_eV = 2.25  # eV

# ε(ω) = 1 - ω_p² / (ω² + iωγ)  = 1 - ω_p² / (ω(ω + iγ))
eps1 = 1 - omega_p**2 / (omega_eV**2 + gamma_D_eV**2)
eps2 = omega_p**2 * gamma_D_eV / (omega_eV * (omega_eV**2 + gamma_D_eV**2))

# Complex refractive index: N = n + ik, N² = ε1 + iε2
# n² - k² = ε1, 2nk = ε2
# → k² = (-ε1 + sqrt(ε1² + ε2²)) / 2, n² = ε1 + k²
eps_abs = np.sqrt(eps1**2 + eps2**2)
k = np.sqrt((-eps1 + eps_abs) / 2)
n = eps2 / (2 * k + 1e-30)

# Normal-incidence reflectivity
R = ((n - 1)**2 + k**2) / ((n + 1)**2 + k**2)

print("=== NaK Alloy: Drude-calculated properties at 550nm, ~100°C ===")
print(f"{'x_Na':>5} {'γ(mN/m)':>8} {'ρ(μΩcm)':>8} {'ω_p(eV)':>8} {'γ_D(eV)':>8} {'n':>6} {'k':>6} {'R':>6}")
print("-" * 65)
for i in range(len(x_Na)):
    print(f"{x_Na[i]:>5.2f} {gamma[i]:>8.0f} {rho[i]:>8.1f} {omega_p[i]:>8.2f} {gamma_D_eV[i]:>8.3f} {n[i]:>6.3f} {k[i]:>6.2f} {R[i]:>6.3f}")

print()

# Correlation
r_corr, p_corr = stats.pearsonr(gamma, R)
r_sp, p_sp = stats.spearmanr(gamma, R)
print(f"=== R vs γ correlation (NaK, sp-only) ===")
print(f"Pearson r = {r_corr:.3f}, p = {p_corr:.4f}")
print(f"Spearman ρ = {r_sp:.3f}, p = {p_sp:.4f}")
print()

# Also correlate γ with ω_p (more fundamental)
r_wp, p_wp = stats.pearsonr(gamma, omega_p)
print(f"γ vs ω_p: Pearson r = {r_wp:.3f}, p = {p_wp:.4f}")

# Plot
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.set_facecolor('#0a0e17')

    for ax in axes:
        ax.set_facecolor('#0a0e17')
        ax.tick_params(colors='#94a3b8')
        ax.spines['bottom'].set_color('#2a3550')
        ax.spines['left'].set_color('#2a3550')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Left: R and γ vs composition
    ax1 = axes[0]
    ax1_r = ax1.twinx()
    l1, = ax1.plot(x_Na, gamma, 'o-', color='#38bdf8', label='γ (mN/m)')
    l2, = ax1_r.plot(x_Na, R, 's-', color='#818cf8', label='R (550nm)')
    ax1.set_xlabel('Na fraction x_Na', color='#e2e8f0')
    ax1.set_ylabel('Surface tension γ (mN/m)', color='#38bdf8')
    ax1_r.set_ylabel('Reflectivity R', color='#818cf8')
    ax1.set_title('NaK alloy: γ and R vs composition', color='#94a3b8')
    ax1_r.spines['right'].set_color('#2a3550')
    ax1_r.tick_params(colors='#94a3b8')
    ax1.legend([l1, l2], ['γ (mN/m)', 'R (550nm)'], loc='center left',
               facecolor='#1a2233', edgecolor='#2a3550', labelcolor='#e2e8f0')

    # Right: R vs γ scatter
    ax2 = axes[1]
    ax2.scatter(gamma, R, c='#38bdf8', s=80, zorder=3, edgecolors='white', linewidths=0.5)
    for i, name in enumerate([f'K', '', 'eut', '', '', '', '', 'Na']):
        if name:
            ax2.annotate(name, (gamma[i], R[i]), textcoords="offset points",
                         xytext=(6, 6), fontsize=9, color='#cbd5e1')

    z = np.polyfit(gamma, R, 1)
    x_line = np.linspace(100, 200, 50)
    ax2.plot(x_line, np.polyval(z, x_line), '--', color='#475569',
             label=f'r={r_corr:.2f}, p={p_corr:.3f}')
    ax2.set_xlabel('Surface tension γ (mN/m)', color='#e2e8f0')
    ax2.set_ylabel('Reflectivity R (550nm, Drude)', color='#e2e8f0')
    ax2.set_title('δ prediction: R ∝ γ within sp metals?', color='#94a3b8')
    ax2.legend(facecolor='#1a2233', edgecolor='#2a3550', labelcolor='#e2e8f0')

    fig.tight_layout()
    fig.savefig('/Users/miyauchikazuyoshi/Documents/GitHub/sento-optics/data/NaK_R_vs_gamma.png', dpi=150)
    print("Plot saved: data/NaK_R_vs_gamma.png")
except ImportError:
    print("matplotlib not available")
