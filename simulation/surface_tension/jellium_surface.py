#!/usr/bin/env python3
"""
Jellium model surface tension simulation.

Goal: Show that surface energy correlates with the gradient of
electron delocalization index δ(z) at the metal-vacuum interface.

Model:
  - Uniform positive background (jellium) terminated at z=0
  - Electrons spill into vacuum → density profile n(z)
  - Thomas-Fermi approximation for self-consistent n(z)
  - Surface energy from kinetic + exchange-correlation energy density

Physics:
  - In bulk (z < 0): n(z) = n_bar, δ high (electrons fully delocalized)
  - At surface (z ≈ 0): n(z) drops → δ drops
  - In vacuum (z >> 0): n(z) → 0, δ → 0
  - Surface energy ∝ ∫ (dδ/dz)² dz  (hypothesis)

Validation:
  - Compare σ_s(r_s) with Lang & Kohn (1970) DFT values
  - Check correlation between δ-gradient integral and σ_s

Reference metals (r_s in Bohr):
  Al: 2.07, Zn: 2.12, Mg: 2.66, Li: 3.25, Na: 3.93, K: 4.86, Cs: 5.62

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.integrate import trapezoid
import os

# Constants (atomic units: ℏ = m_e = e = 1, energies in Hartree)
BOHR_TO_ANGSTROM = 0.529177
HARTREE_TO_EV = 27.2114
HARTREE_TO_ERG_PER_CM2 = 1.557e5  # Hartree/Bohr² → erg/cm²
BOHR2_TO_CM2 = (0.529177e-8) ** 2

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)


# ── Reference data ────────────────────────────────────────────────────
# Experimental surface tensions (mN/m = mJ/m² = erg/cm²)
# and Wigner-Seitz radii (Bohr)
METALS = {
    "Al":  {"r_s": 2.07, "gamma_exp": 1140},
    "Zn":  {"r_s": 2.12, "gamma_exp": 782},
    "Mg":  {"r_s": 2.66, "gamma_exp": 559},
    "Li":  {"r_s": 3.25, "gamma_exp": 398},
    "Na":  {"r_s": 3.93, "gamma_exp": 191},
    "K":   {"r_s": 4.86, "gamma_exp": 101},
    "Cs":  {"r_s": 5.62, "gamma_exp": 67},
}

# Lang & Kohn (1970) DFT surface energies (erg/cm²)
LANG_KOHN = {
    2.0: 3354,
    2.5: 1164,
    3.0: 526,
    3.5: 271,
    4.0: 150,
    4.5: 87,
    5.0: 53,
    5.5: 33,
    6.0: 22,
}


def bulk_density(r_s):
    """Bulk electron density from Wigner-Seitz radius (atomic units)."""
    return 3.0 / (4.0 * np.pi * r_s**3)


def fermi_wavevector(n):
    """Fermi wavevector k_F = (3π²n)^(1/3) (atomic units)."""
    return (3.0 * np.pi**2 * n) ** (1.0 / 3.0)


def thomas_fermi_wavevector(n):
    """Thomas-Fermi screening wavevector q_TF = sqrt(4 k_F / π) (a.u.)."""
    kf = fermi_wavevector(n)
    return np.sqrt(4.0 * kf / np.pi)


# ── Electron density profile ─────────────────────────────────────────
def density_profile_analytical(z_grid, r_s, model="exponential"):
    """
    Analytical model for jellium surface electron density n(z).

    The exponential spillover model:
        n(z) = n_bar                        for z < -d
        n(z) = n_bar * exp(-2 * q_TF * z)   for z > 0
    with a smooth interpolation in [-d, 0].

    More realistic: use a Fermi-function-like profile fitted to
    Lang & Kohn self-consistent results.
    """
    n_bar = bulk_density(r_s)
    kf = fermi_wavevector(n_bar)

    if model == "exponential":
        # Simple exponential decay into vacuum
        # Decay length ≈ 1/(2*q_TF) from Thomas-Fermi theory
        q_tf = thomas_fermi_wavevector(n_bar)
        beta = q_tf  # decay constant

        n_z = np.where(z_grid < 0, n_bar, n_bar * np.exp(-beta * z_grid))

    elif model == "smooth":
        # Smooth profile matching Lang-Kohn shape
        # n(z) = n_bar / (1 + exp(α * z))
        # α calibrated so that spillover length ≈ 1/q_TF
        q_tf = thomas_fermi_wavevector(n_bar)
        alpha = q_tf * 1.5  # empirical fit to LK shape
        n_z = n_bar / (1.0 + np.exp(alpha * z_grid))

    elif model == "friedel":
        # Include Friedel oscillations (more realistic)
        q_tf = thomas_fermi_wavevector(n_bar)
        alpha = q_tf * 1.2

        # Smooth envelope
        envelope = n_bar / (1.0 + np.exp(alpha * z_grid))

        # Friedel oscillations in the bulk side
        # Amplitude decays as 1/z² from the surface
        osc_amplitude = 0.1 * n_bar  # ~10% oscillation
        dist_from_surface = np.abs(z_grid) + 0.5  # avoid divergence
        oscillation = np.where(
            z_grid < 0,
            osc_amplitude / dist_from_surface**2
            * np.cos(2.0 * kf * z_grid),
            0.0,
        )
        n_z = envelope + oscillation
        n_z = np.maximum(n_z, 0.0)  # ensure non-negative

    return n_z


# ── Energy density functionals ────────────────────────────────────────
def kinetic_energy_density(n):
    """
    Thomas-Fermi kinetic energy density t_TF(n) = (3/10)(3π²)^(2/3) n^(5/3).
    """
    cf = (3.0 / 10.0) * (3.0 * np.pi**2) ** (2.0 / 3.0)
    return cf * np.abs(n) ** (5.0 / 3.0)


def exchange_energy_density(n):
    """
    LDA exchange energy density: e_x(n) = -(3/4)(3/π)^(1/3) n^(4/3).
    """
    cx = -(3.0 / 4.0) * (3.0 / np.pi) ** (1.0 / 3.0)
    return cx * np.abs(n) ** (4.0 / 3.0)


def correlation_energy_density(n):
    """
    LDA correlation: Perdew-Zunger (1981) parameterization of
    Ceperley-Alder data.

    For n > 0: compute r_s = (3/(4πn))^(1/3), then use PZ formula.
    """
    eps_c = np.zeros_like(n)
    mask = n > 1e-30

    r_s_local = (3.0 / (4.0 * np.pi * n[mask])) ** (1.0 / 3.0)

    # PZ parameterization
    # r_s >= 1:
    high_rs = r_s_local >= 1.0
    gamma_pz = -0.1423
    beta1 = 1.0529
    beta2 = 0.3334
    r_high = r_s_local[high_rs]
    eps_c_high = gamma_pz / (1.0 + beta1 * np.sqrt(r_high) + beta2 * r_high)

    # r_s < 1:
    low_rs = ~high_rs
    A = 0.0311
    B = -0.048
    C = 0.0020
    D = -0.0116
    r_low = r_s_local[low_rs]
    eps_c_low = A * np.log(r_low) + B + C * r_low * np.log(r_low) + D * r_low

    ec_local = np.zeros_like(r_s_local)
    ec_local[high_rs] = eps_c_high
    ec_local[low_rs] = eps_c_low

    eps_c[mask] = ec_local * n[mask]  # energy density = ε_c × n
    return eps_c


def gradient_correction_energy_density(n, dn_dz):
    """
    von Weizsäcker gradient correction to kinetic energy:
    t_W = (1/8) |∇n|² / n  (with a coefficient λ = 1/9 for TF-vW)
    """
    lam = 1.0 / 9.0  # Thomas-Fermi-von Weizsäcker coefficient
    mask = n > 1e-30
    t_vw = np.zeros_like(n)
    t_vw[mask] = lam * (1.0 / 8.0) * dn_dz[mask] ** 2 / n[mask]
    return t_vw


# ── Surface energy calculation ────────────────────────────────────────
def compute_surface_energy(r_s, z_grid=None, model="smooth"):
    """
    Compute jellium surface energy σ_s for given r_s.

    σ_s = ∫ [e(n(z)) - e(n_bar) * θ(-z)] dz

    where e(n) = t_TF(n) + e_x(n) + e_c(n) + t_vW(n)
    and θ(-z) is the step function (positive background).

    Returns:
        sigma_s: surface energy in erg/cm²
        z_grid: z coordinate grid (Bohr)
        n_z: electron density profile
        delta_z: delocalization index profile
    """
    if z_grid is None:
        z_grid = np.linspace(-15.0, 15.0, 3000)

    dz = z_grid[1] - z_grid[0]
    n_bar = bulk_density(r_s)

    # Electron density profile
    n_z = density_profile_analytical(z_grid, r_s, model=model)

    # Gradient of density
    dn_dz = np.gradient(n_z, dz)

    # Total energy density of inhomogeneous system
    e_total = (
        kinetic_energy_density(n_z)
        + exchange_energy_density(n_z)
        + correlation_energy_density(n_z)
        + gradient_correction_energy_density(n_z, dn_dz)
    )

    # Bulk energy density (uniform electron gas at n_bar)
    e_bulk = (
        kinetic_energy_density(np.array([n_bar]))[0]
        + exchange_energy_density(np.array([n_bar]))[0]
        + correlation_energy_density(np.array([n_bar]))[0]
    )

    # Electrostatic contribution from electron spillover
    # Positive background is a step function: n_+(z) = n_bar for z < 0
    n_plus = np.where(z_grid < 0, n_bar, 0.0)
    charge_density = n_plus - n_z  # net charge (positive = deficit)

    # Electric field from charge distribution (1D Poisson)
    # E(z) = -4π ∫_{-∞}^{z} ρ(z') dz'
    E_field = -4.0 * np.pi * np.cumsum(charge_density) * dz

    # Electrostatic energy density
    e_electrostatic = E_field**2 / (8.0 * np.pi)

    # Surface energy integrand
    # σ = ∫ [e_total(z) + e_es(z) - e_bulk * θ(-z)] dz
    integrand = e_total + e_electrostatic - e_bulk * np.where(z_grid < 0, 1.0, 0.0)

    # Surface energy (Hartree/Bohr²)
    sigma_au = trapezoid(integrand, z_grid)

    # Convert to erg/cm²
    sigma_cgs = sigma_au * HARTREE_TO_ERG_PER_CM2

    # ── Delocalization index δ(z) ──
    # Define δ as a local measure of electron delocalization:
    # δ(z) = n(z) / n_bar  (normalized density, 0 to 1)
    # In bulk: δ = 1, in vacuum: δ → 0
    # This is the simplest proxy; could also use local IPR or
    # kinetic energy ratio.
    delta_z = n_z / n_bar

    return sigma_cgs, z_grid, n_z, delta_z, n_bar


# ── δ-gradient integral ───────────────────────────────────────────────
def delta_gradient_integral(z_grid, delta_z):
    """
    Compute ∫ (dδ/dz)² dz — the "δ-gradient cost" of the interface.

    Hypothesis: surface energy ∝ this integral.
    """
    dz = z_grid[1] - z_grid[0]
    d_delta_dz = np.gradient(delta_z, dz)
    return trapezoid(d_delta_dz**2, z_grid)


# ── Main ──────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Jellium Surface Energy & δ-Gradient Correlation")
    print("=" * 60)

    # 1. Compute surface energy for a range of r_s values
    r_s_range = np.linspace(2.0, 6.0, 30)
    sigma_values = []
    dgrad_values = []

    for r_s in r_s_range:
        sigma, z, n, delta, n_bar = compute_surface_energy(r_s)
        dgrad = delta_gradient_integral(z, delta)
        sigma_values.append(sigma)
        dgrad_values.append(dgrad)

    sigma_values = np.array(sigma_values)
    dgrad_values = np.array(dgrad_values)

    # 2. Compute for specific metals
    print(f"\n{'Metal':>6s}  {'r_s':>5s}  {'σ_calc':>10s}  {'γ_exp':>8s}  {'∫(dδ/dz)²':>12s}")
    print("-" * 55)

    metal_results = {}
    for name, data in METALS.items():
        r_s = data["r_s"]
        sigma, z, n, delta, n_bar = compute_surface_energy(r_s)
        dgrad = delta_gradient_integral(z, delta)
        metal_results[name] = {
            "r_s": r_s,
            "sigma_calc": sigma,
            "gamma_exp": data["gamma_exp"],
            "dgrad": dgrad,
            "z": z,
            "n": n,
            "delta": delta,
            "n_bar": n_bar,
        }
        print(
            f"{name:>6s}  {r_s:5.2f}  {sigma:10.1f}  {data['gamma_exp']:8.0f}  {dgrad:12.4f}"
        )

    # 3. Correlation analysis
    from scipy.stats import pearsonr

    exp_gammas = [metal_results[m]["gamma_exp"] for m in METALS]
    calc_dgrads = [metal_results[m]["dgrad"] for m in METALS]

    r_corr, p_val = pearsonr(calc_dgrads, exp_gammas)
    print(f"\nCorrelation: ∫(dδ/dz)² vs γ_exp")
    print(f"  Pearson r = {r_corr:.4f}  (p = {p_val:.2e})")

    calc_sigmas = [metal_results[m]["sigma_calc"] for m in METALS]
    r_corr2, p_val2 = pearsonr(calc_sigmas, exp_gammas)
    print(f"\nCorrelation: σ_calc vs γ_exp")
    print(f"  Pearson r = {r_corr2:.4f}  (p = {p_val2:.2e})")

    # ── Figures ──

    # Fig 1: Density profiles for selected metals
    fig1, axes1 = plt.subplots(1, 3, figsize=(15, 4.5))
    fig1.suptitle("Jellium Surface: Electron Density & Delocalization Profile",
                   fontsize=14, y=1.02)

    selected = ["Al", "Na", "Cs"]
    colors_metal = ["#e74c3c", "#3498db", "#2ecc71"]

    for ax, name, color in zip(axes1, selected, colors_metal):
        d = metal_results[name]
        z_ang = d["z"] * BOHR_TO_ANGSTROM

        # Left y-axis: n(z)
        ax.plot(z_ang, d["n"], color=color, linewidth=2, label=f"n(z)")
        ax.axhline(d["n_bar"], color=color, linestyle=":", alpha=0.5,
                    label=f"n_bar")
        ax.axvline(0, color="gray", linestyle="--", alpha=0.3)
        ax.fill_betweenx([0, d["n_bar"] * 1.3], -8, 0, alpha=0.05, color="blue",
                          label="Positive background")

        ax.set_xlabel("z [Å]", fontsize=11)
        ax.set_ylabel("n(z) [a.u.]", fontsize=11)
        ax.set_title(f"{name} (r_s = {d['r_s']:.2f})", fontsize=12)
        ax.set_xlim(-4, 4)
        ax.set_ylim(0, d["n_bar"] * 1.3)
        ax.legend(fontsize=8, loc="upper right")
        ax.grid(alpha=0.3)

        # Inset: δ(z)
        ax_in = ax.inset_axes([0.55, 0.4, 0.4, 0.35])
        ax_in.plot(z_ang, d["delta"], color=color, linewidth=1.5)
        ax_in.set_ylabel("δ(z)", fontsize=8)
        ax_in.set_xlabel("z [Å]", fontsize=8)
        ax_in.set_xlim(-4, 4)
        ax_in.set_ylim(-0.05, 1.2)
        ax_in.axhline(1.0, color="gray", linestyle=":", alpha=0.3)
        ax_in.tick_params(labelsize=7)

    fig1.tight_layout()
    fig1.savefig(os.path.join(FIGDIR, "fig_st1_density_profiles.png"),
                 dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_st1_density_profiles.png')}")

    # Fig 2: σ_s(r_s) comparison with Lang-Kohn
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(13, 5))
    fig2.suptitle("Surface Energy: Jellium Model vs Experiment",
                   fontsize=14, y=1.02)

    # Left: σ_s vs r_s
    ax2a.plot(r_s_range, sigma_values, "b-", linewidth=2, label="This work (TF-vW-LDA)")

    # Lang-Kohn reference
    lk_rs = sorted(LANG_KOHN.keys())
    lk_sigma = [LANG_KOHN[rs] for rs in lk_rs]
    ax2a.plot(lk_rs, lk_sigma, "k--", linewidth=1.5, marker="s", markersize=5,
              label="Lang & Kohn (1970)")

    # Experimental points
    for name, d in metal_results.items():
        ax2a.scatter(d["r_s"], d["gamma_exp"], s=80, zorder=5,
                     edgecolors="black", linewidth=0.8)
        ax2a.annotate(name, (d["r_s"], d["gamma_exp"]),
                      textcoords="offset points", xytext=(5, 5), fontsize=9)

    ax2a.set_xlabel("r_s [Bohr]", fontsize=12)
    ax2a.set_ylabel("Surface Energy [erg/cm²]", fontsize=12)
    ax2a.set_title("(a) Surface Energy vs Wigner-Seitz Radius", fontsize=11)
    ax2a.legend(fontsize=9)
    ax2a.grid(alpha=0.3)
    ax2a.set_xlim(1.5, 6.5)

    # Right: δ-gradient integral vs experimental γ
    metal_colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(METALS)))
    ax2b.scatter(calc_dgrads, exp_gammas, s=100, c=metal_colors,
                 edgecolors="black", linewidth=0.8, zorder=5)

    for name, dgrad, gamma in zip(METALS.keys(), calc_dgrads, exp_gammas):
        ax2b.annotate(name, (dgrad, gamma),
                      textcoords="offset points", xytext=(5, 5), fontsize=10)

    # Fit line
    coeffs = np.polyfit(calc_dgrads, exp_gammas, 1)
    dgrad_fit = np.linspace(min(calc_dgrads) * 0.9, max(calc_dgrads) * 1.1, 100)
    ax2b.plot(dgrad_fit, np.polyval(coeffs, dgrad_fit), "r--", alpha=0.5,
              label=f"Linear fit (r={r_corr:.3f})")

    ax2b.set_xlabel("∫(dδ/dz)² dz  [Bohr⁻¹]", fontsize=12)
    ax2b.set_ylabel("Experimental γ [erg/cm²]", fontsize=12)
    ax2b.set_title("(b) δ-Gradient Integral vs Surface Tension", fontsize=11)
    ax2b.legend(fontsize=10)
    ax2b.grid(alpha=0.3)

    fig2.tight_layout()
    fig2.savefig(os.path.join(FIGDIR, "fig_st2_surface_energy.png"),
                 dpi=150, bbox_inches="tight")
    print(f"Saved: {os.path.join(FIGDIR, 'fig_st2_surface_energy.png')}")

    # Fig 3: Reflectivity vs surface tension (the δ bridge)
    fig3, ax3 = plt.subplots(figsize=(7, 6))
    fig3.suptitle("Reflectivity vs Surface Tension: δ as Common Origin",
                   fontsize=14, y=1.02)

    # Drude model with damping: ε(ω) = 1 - ω_p²/(ω² + iωγ_d)
    # γ_d = scattering rate ≈ 0.1-1 eV for metals
    # ω_p = √(4πn) in atomic units
    omega_vis = 2.5 / HARTREE_TO_EV  # Hartree
    # Typical Drude damping rates (eV) — from literature
    DAMPING = {
        "Al": 0.05, "Zn": 0.1, "Mg": 0.1,
        "Li": 0.15, "Na": 0.1, "K": 0.1, "Cs": 0.1,
    }

    R_drude = []
    for name in METALS:
        d = metal_results[name]
        n_bar = d["n_bar"]
        omega_p = np.sqrt(4.0 * np.pi * n_bar)  # plasma frequency (a.u.)
        gamma_d = DAMPING.get(name, 0.1) / HARTREE_TO_EV  # convert to a.u.

        # Drude dielectric function
        eps = 1.0 - omega_p**2 / (omega_vis**2 + 1j * omega_vis * gamma_d)
        n_complex = np.sqrt(eps)
        R = float(np.abs((n_complex - 1) / (n_complex + 1))**2)
        R_drude.append(R)

    ax3.scatter(exp_gammas, R_drude, s=120, c=metal_colors,
                edgecolors="black", linewidth=0.8, zorder=5)

    for name, gamma, R in zip(METALS.keys(), exp_gammas, R_drude):
        ax3.annotate(name, (gamma, R),
                     textcoords="offset points", xytext=(5, 5), fontsize=10)

    r_Rg, p_Rg = pearsonr(exp_gammas, R_drude)
    ax3.set_xlabel("Surface Tension γ [erg/cm²]", fontsize=12)
    ax3.set_ylabel("Visible-range Reflectivity R (Drude estimate)", fontsize=12)
    ax3.set_title(f"R vs γ correlation (r = {r_Rg:.3f})", fontsize=12)
    ax3.grid(alpha=0.3)

    # Add annotation
    ax3.text(0.05, 0.95,
             "Both R and γ increase with\nbulk electron density n̄ (∝ δ)",
             transform=ax3.transAxes, fontsize=10, va="top",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.5))

    fig3.tight_layout()
    fig3.savefig(os.path.join(FIGDIR, "fig_st3_reflectivity_vs_gamma.png"),
                 dpi=150, bbox_inches="tight")
    print(f"Saved: {os.path.join(FIGDIR, 'fig_st3_reflectivity_vs_gamma.png')}")

    plt.close("all")

    print("\n" + "=" * 60)
    print("Surface tension simulation complete.")
    print(f"Figures saved to {FIGDIR}")
    print("=" * 60)

    return metal_results, r_corr, p_val


if __name__ == "__main__":
    metal_results, r_corr, p_val = main()
