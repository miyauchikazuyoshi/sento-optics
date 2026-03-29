#!/usr/bin/env python3
"""
Water anomalies from the δ_nuc framework.

Goal: Show that water's density maximum at 4°C and surface tension
both emerge from the temperature dependence of nuclear delocalization δ_nuc.

Physics:
  Water molecules exist in two competing local states:
  (1) H-bonded tetrahedral network (ice-like): open structure, LOW density,
      LOW δ_nuc (molecules locked in H-bond network)
  (2) Non-bonded close-packed: HIGH density,
      HIGH δ_nuc (molecules free to move/rotate)

  At low T: state (1) dominates → open network → density < 1.0 g/cm³
  At ~4°C: optimal balance → density maximum (0.99997 g/cm³)
  At high T: state (2) + thermal expansion → density decreases

Models:
  1. Two-state thermodynamic model for ρ(T) with δ_nuc(T)
  2. Vectorized 2D MD with LJ + H-bond for interface δ_nuc(z) profile
  3. Vectorized NPT Monte Carlo for density vs temperature

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)

kB = 8.617e-5  # eV/K
NA = 6.022e23


# ══════════════════════════════════════════════════════════════════════
# Model 1: Two-State Thermodynamic Model
# ══════════════════════════════════════════════════════════════════════

def two_state_water(T_range):
    """
    Two-state model for water density anomaly.
    State A: H-bonded tetrahedral (open), State B: close-packed.
    """
    M_water = 18.015
    V_ice = M_water / (0.917 * NA) * 1e24    # Å³ per molecule (ice Ih)
    V_close = M_water / (1.08 * NA) * 1e24  # close-packed (8% denser than ice)

    # Tuned parameters for Tmax ≈ 4°C (277 K)
    # The maximum occurs where d(ρ)/dT = 0, i.e. where the rate of
    # H-bond network collapse (increasing density) exactly balances
    # thermal expansion (decreasing density).
    delta_E = 0.050   # eV (effective H-bond energy per molecule)
    delta_S = 2.15e-4 # eV/K (entropy gain from H-bond breaking)
    alpha = 3.0e-4    # K⁻¹ thermal expansion
    T0 = 273.15

    f_A = np.zeros_like(T_range, dtype=float)
    rho = np.zeros_like(T_range, dtype=float)
    delta_nuc = np.zeros_like(T_range, dtype=float)

    for i, T in enumerate(T_range):
        delta_G = delta_E - T * delta_S
        x = delta_G / (kB * T)
        x = np.clip(x, -500, 500)
        f_A[i] = 1.0 / (1.0 + np.exp(-x))

        V_A_T = V_ice * (1.0 + alpha * (T - T0))
        V_B_T = V_close * (1.0 + alpha * (T - T0))
        V_avg = f_A[i] * V_A_T + (1.0 - f_A[i]) * V_B_T
        rho[i] = M_water / (V_avg * 1e-24 * NA)

        delta_A = 0.15
        delta_B = 0.65
        thermal_factor = np.sqrt(T / 300.0)
        delta_nuc[i] = (f_A[i] * delta_A + (1.0 - f_A[i]) * delta_B) * thermal_factor

    return rho, f_A, delta_nuc


# ══════════════════════════════════════════════════════════════════════
# Model 2: Vectorized 2D MD (LJ + H-bond)
# ══════════════════════════════════════════════════════════════════════

def water_md_2d(N=100, T_target=300.0, n_steps=8000,
                box_x=30.0, box_y=60.0):
    """
    2D MD in reduced LJ units (σ=1, ε=1, m=1).
    Slab geometry. LJ + Gaussian H-bond attraction.
    Strong Langevin thermostat for reliable equilibration.
    """
    # All in reduced units: σ=1, ε=1, m=1
    # Real mapping: σ=2.75Å, ε=0.007eV, T*=kBT/ε
    sigma_real = 2.75  # Å
    eps_real = 0.007   # eV
    T_star = kB * T_target / eps_real  # reduced temperature

    # H-bond in reduced units
    r_hb_star = 2.8 / sigma_real  # ~1.018
    eps_hb_star = 0.025 / eps_real  # ~3.57
    hb_w_star = 0.5 / sigma_real   # ~0.182

    r_cut_star = 3.0
    Lx = box_x / sigma_real
    Ly = box_y / sigma_real
    dt = 0.002  # reduced time
    gamma = 1.0  # strong Langevin friction

    np.random.seed(42)

    # Grid init in reduced units
    y_lo, y_hi = Ly * 0.25, Ly * 0.75
    slab_h = y_hi - y_lo
    sp = 1.12  # spacing ≈ LJ minimum (2^(1/6) ≈ 1.122)
    nx = int(Lx / sp)
    ny = int(slab_h / sp)
    N = min(N, nx * ny)

    pos = []
    for iy in range(ny):
        for ix in range(nx):
            if len(pos) >= N:
                break
            pos.append([(ix + 0.5) * sp, y_lo + (iy + 0.5) * sp])
    pos = np.array(pos[:N])
    N = len(pos)
    vel = np.random.randn(N, 2) * np.sqrt(T_star)
    vel -= vel.mean(axis=0)

    print(f"  Water 2D MD (reduced units): N={N}, T*={T_star:.3f}, "
          f"Lx={Lx:.1f}, Ly={Ly:.1f}")

    def forces_and_pe(pos):
        dx = pos[:, 0, None] - pos[None, :, 0]
        dy = pos[:, 1, None] - pos[None, :, 1]
        dx -= Lx * np.round(dx / Lx)
        r_sq = dx**2 + dy**2
        np.fill_diagonal(r_sq, np.inf)
        mask = (r_sq < r_cut_star**2)

        r_inv2 = np.where(mask, 1.0 / np.maximum(r_sq, 0.5), 0.0)
        r_inv6 = r_inv2**3
        r_inv12 = r_inv6**2

        # LJ: f/r = 24*(2*r^-14 - r^-8)
        f_over_r = np.where(mask, 24.0 * (2.0 * r_inv12 * r_inv2 - r_inv6 * r_inv2), 0.0)

        # H-bond
        r = np.sqrt(np.where(mask, r_sq, 1.0))
        dr = r - r_hb_star
        f_hb = np.where(mask, eps_hb_star * dr / hb_w_star**2 *
                         np.exp(-0.5 * (dr / hb_w_star)**2) / (r + 1e-30), 0.0)

        f_tot = f_over_r + f_hb
        fx = np.sum(f_tot * dx, axis=1)
        fy = np.sum(f_tot * dy, axis=1)
        return np.column_stack([fx, fy])

    positions_history = []
    n_equil = n_steps * 2 // 3

    f = forces_and_pe(pos)

    for step in range(n_steps):
        # Velocity Verlet + Langevin
        vel += 0.5 * dt * f
        vel *= np.exp(-gamma * dt)
        vel += np.sqrt(T_star * (1 - np.exp(-2 * gamma * dt))) * np.random.randn(N, 2)
        pos += dt * vel
        pos[:, 0] %= Lx

        # Reflecting walls
        lo = pos[:, 1] < 0; hi = pos[:, 1] > Ly
        pos[lo, 1] *= -1; vel[lo, 1] *= -1
        pos[hi, 1] = 2 * Ly - pos[hi, 1]; vel[hi, 1] *= -1

        f = forces_and_pe(pos)
        vel += 0.5 * dt * f

        if step >= n_equil and step % 3 == 0:
            # Convert back to Å for storage
            positions_history.append(pos * sigma_real)

        if step % 2000 == 0:
            T_inst = np.mean(vel**2)  # <v²> = d*T* (d=2)
            print(f"    step {step:5d}/{n_steps}: T*={T_inst/2:.3f} "
                  f"(target {T_star:.3f})")

    return positions_history, box_x, box_y


def compute_profiles(positions_history, box_y, n_bins=30):
    """Compute density and δ_nuc profiles from MD trajectory."""
    n_frames = len(positions_history)
    y_edges = np.linspace(0, box_y, n_bins + 1)
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    density_profile = np.zeros(n_bins)
    for pos in positions_history:
        hist, _ = np.histogram(pos[:, 1], bins=y_edges)
        density_profile += hist
    density_profile /= n_frames

    # δ_nuc: displacement between consecutive snapshots, binned
    delta_profile = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    step = max(1, n_frames // 40)

    for t in range(0, n_frames - 1, step):
        pos_t = positions_history[t]
        pos_t1 = positions_history[min(t + 3, n_frames - 1)]
        dr_sq = np.sum((pos_t1 - pos_t)**2, axis=1)

        bins = np.digitize(pos_t[:, 1], y_edges) - 1
        for b in range(n_bins):
            mask = bins == b
            if mask.sum() > 0:
                delta_profile[b] += np.sqrt(np.mean(dr_sq[mask]))
                counts[b] += 1

    nonzero = counts > 0
    delta_profile[nonzero] /= (counts[nonzero] * 2.8)  # normalize by nn distance

    return y_centers, density_profile, delta_profile


# ══════════════════════════════════════════════════════════════════════
# Model 3: Vectorized NPT Monte Carlo
# ══════════════════════════════════════════════════════════════════════

def density_vs_temperature_mc(temperatures, N=64, n_steps=3000):
    """Vectorized NPT MC for 2D water-like fluid."""
    sigma = 2.75
    epsilon = 0.007
    eps_hb = 0.025
    r_hb = 2.8
    hb_w = 0.5
    r_cut = 3.5 * sigma
    P_target = 0.0

    results = {"T": [], "rho": [], "delta_nuc": []}

    for T in temperatures:
        beta = 1.0 / (kB * T)
        n_side = int(np.ceil(np.sqrt(N)))
        spacing = 3.0
        box_L = n_side * spacing

        ix = np.arange(N) % n_side
        iy = np.arange(N) // n_side
        pos = np.column_stack([(ix + 0.5) * spacing, (iy + 0.5) * spacing])
        pos %= box_L

        def total_energy(pos, L):
            dx = pos[:, 0, None] - pos[None, :, 0]
            dy = pos[:, 1, None] - pos[None, :, 1]
            dx -= L * np.round(dx / L)
            dy -= L * np.round(dy / L)
            r_sq = dx**2 + dy**2
            np.fill_diagonal(r_sq, np.inf)
            mask = (r_sq < r_cut**2) & (r_sq > 0.25)
            r = np.sqrt(np.where(mask, r_sq, 1.0))
            sr6 = np.where(mask, (sigma / r)**6, 0.0)
            e_lj = np.sum(4.0 * epsilon * (sr6**2 - sr6)) / 2
            dr_hb = r - r_hb
            e_hb = -np.sum(np.where(mask, eps_hb * np.exp(-0.5 * (dr_hb / hb_w)**2), 0.0)) / 2
            return e_lj + e_hb

        def single_energy(pos, idx, L):
            """Energy of particle idx with all others."""
            dx = pos[idx, 0] - pos[:, 0]
            dy = pos[idx, 1] - pos[:, 1]
            dx -= L * np.round(dx / L)
            dy -= L * np.round(dy / L)
            r_sq = dx**2 + dy**2
            r_sq[idx] = np.inf
            mask = (r_sq < r_cut**2) & (r_sq > 0.25)
            r = np.sqrt(np.where(mask, r_sq, 1.0))
            sr6 = np.where(mask, (sigma / r)**6, 0.0)
            e_lj = np.sum(4.0 * epsilon * (sr6**2 - sr6))
            dr_hb = r - r_hb
            e_hb = -np.sum(np.where(mask, eps_hb * np.exp(-0.5 * (dr_hb / hb_w)**2), 0.0))
            return e_lj + e_hb

        dr_max = 0.3
        dL_max = 0.2
        n_equil = n_steps // 2
        areas = []
        pos_snapshots = []

        for step in range(n_steps):
            # Particle move
            i = np.random.randint(N)
            e_old = single_energy(pos, i, box_L)
            pos_old = pos[i].copy()
            pos[i] += np.random.uniform(-dr_max, dr_max, 2)
            pos[i] %= box_L
            e_new = single_energy(pos, i, box_L)
            dE = e_new - e_old
            if dE > 0 and np.random.random() >= np.exp(-beta * dE):
                pos[i] = pos_old

            # Volume move (every 20 steps)
            if step % 20 == 0:
                L_new = box_L + np.random.uniform(-dL_max, dL_max)
                if L_new > 2 * sigma:
                    pe_old = total_energy(pos, box_L)
                    scale = L_new / box_L
                    pos_s = pos * scale
                    pe_new = total_energy(pos_s, L_new)
                    dW = (pe_new - pe_old + P_target * (L_new**2 - box_L**2)
                          - N * kB * T * 2 * np.log(scale))
                    if dW < 0 or np.random.random() < np.exp(-beta * dW):
                        pos = pos_s
                        box_L = L_new

            if step >= n_equil and step % 5 == 0:
                areas.append(box_L**2)
                pos_snapshots.append(pos.copy())

        avg_area = np.mean(areas)
        rho_2d = N / avg_area

        # δ from positional fluctuations
        if len(pos_snapshots) > 5:
            all_pos = np.array(pos_snapshots)
            mean_pos = all_pos.mean(axis=0)
            displ_sq = np.mean(np.sum((all_pos - mean_pos)**2, axis=2))
            delta_nuc = np.sqrt(displ_sq) / sigma
        else:
            delta_nuc = 0.0

        results["T"].append(T)
        results["rho"].append(rho_2d)
        results["delta_nuc"].append(delta_nuc)

        T_C = T - 273.15
        print(f"    T={T_C:6.1f}°C: ρ_2D={rho_2d:.4f} Å⁻², δ={delta_nuc:.4f}, L={box_L:.2f}")

    return results


# ══════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("Water Anomalies in the δ_nuc Framework")
    print("=" * 60)

    # ── 1. Two-state model ──
    print("\n[1/3] Two-state model: density anomaly...")
    T_range = np.linspace(253.15, 373.15, 500)
    T_celsius = T_range - 273.15
    rho_model, f_hbond, delta_nuc_model = two_state_water(T_range)

    i_max = np.argmax(rho_model)
    T_max = T_celsius[i_max]
    rho_max = rho_model[i_max]
    delta_at_max = delta_nuc_model[i_max]

    print(f"  Density maximum: T = {T_max:.1f}°C, ρ = {rho_max:.5f} g/cm³")
    print(f"  δ_nuc at density max: {delta_at_max:.4f}")

    # Experimental data
    T_exp = np.array([0, 4, 10, 20, 30, 40, 50, 60, 80, 100])
    rho_exp = np.array([0.99984, 0.99997, 0.99970, 0.99821,
                         0.99565, 0.99222, 0.98803, 0.98320,
                         0.97179, 0.95835])

    # ── 2. MC density vs T ──
    print("\n[2/3] NPT Monte Carlo: density vs temperature...")
    mc_temps = np.array([268, 273, 275, 277, 280, 285, 293, 303, 323, 343]) + 0.15
    mc_results = density_vs_temperature_mc(mc_temps, N=36, n_steps=3000)

    # ── 3. MD surface ──
    print("\n[3/3] 2D MD surface profile at 300K...")
    pos_history, box_x, box_y = water_md_2d(
        N=100, T_target=300.0, n_steps=6000, box_x=30.0, box_y=60.0
    )
    y_centers, density_prof, delta_prof = compute_profiles(pos_history, box_y, n_bins=25)

    # ── Figures ──
    print("\nGenerating figures...")

    # === Fig W1: Density anomaly ===
    fig1, axes1 = plt.subplots(2, 2, figsize=(13, 10))
    fig1.suptitle("Water Density Anomaly in the δ_nuc Framework",
                   fontsize=14, y=1.02)

    ax = axes1[0, 0]
    ax.plot(T_celsius, rho_model, "b-", linewidth=2, label="Two-state model")
    ax.plot(T_exp, rho_exp, "ko", markersize=6, label="Experimental", zorder=5)
    ax.axvline(T_max, color="red", linestyle="--", alpha=0.5,
               label=f"T_max = {T_max:.1f}°C")
    ax.set_xlabel("Temperature [°C]", fontsize=12)
    ax.set_ylabel("Density [g/cm³]", fontsize=12)
    ax.set_title("(a) Density vs Temperature", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(-10, 100)

    ax = axes1[0, 1]
    ax.plot(T_celsius, f_hbond, "g-", linewidth=2)
    ax.axvline(T_max, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("Temperature [°C]", fontsize=12)
    ax.set_ylabel("H-bond fraction f_A", fontsize=12)
    ax.set_title("(b) H-bond Network Order", fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xlim(-10, 100)
    ax.annotate("Ice-like\n(tetrahedral)", xy=(0, f_hbond[np.argmin(np.abs(T_celsius))]),
                xytext=(20, 0.85), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="green"),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.5))

    ax = axes1[1, 0]
    ax.plot(T_celsius, delta_nuc_model, "r-", linewidth=2)
    ax.axvline(T_max, color="red", linestyle="--", alpha=0.5)
    ax.axhline(delta_at_max, color="gray", linestyle=":", alpha=0.3)
    ax.set_xlabel("Temperature [°C]", fontsize=12)
    ax.set_ylabel("δ_nuc", fontsize=12)
    ax.set_title("(c) Nuclear Delocalization Index", fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xlim(-10, 100)
    ax.annotate(f"δ* = {delta_at_max:.3f}\n(density max)",
                xy=(T_max, delta_at_max),
                xytext=(T_max + 20, delta_at_max - 0.03),
                fontsize=9, arrowprops=dict(arrowstyle="->", color="red"),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.5))

    ax = axes1[1, 1]
    scatter = ax.scatter(delta_nuc_model[::5], rho_model[::5], c=T_celsius[::5],
                          cmap="coolwarm", s=20, zorder=5)
    plt.colorbar(scatter, ax=ax, label="Temperature [°C]")
    ax.scatter([delta_at_max], [rho_max], s=200, marker="*", c="red",
               edgecolors="black", zorder=10, label=f"ρ_max at δ*={delta_at_max:.3f}")
    ax.set_xlabel("δ_nuc", fontsize=12)
    ax.set_ylabel("Density [g/cm³]", fontsize=12)
    ax.set_title("(d) Density vs δ_nuc: The Anomaly", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    ax.text(0.05, 0.95,
            "Low δ: H-bond network → open structure\n"
            "High δ: thermal motion → expansion\n"
            "Density max at optimal δ*",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.5))

    fig1.tight_layout()
    fig1.savefig(os.path.join(FIGDIR, "fig_w1_density_anomaly.png"),
                 dpi=150, bbox_inches="tight")
    print(f"  Saved: fig_w1_density_anomaly.png")

    # === Fig W2: Surface profile ===
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(13, 5))
    fig2.suptitle("Water-Vacuum Interface: Density and δ_nuc Profile (2D MD)",
                   fontsize=14, y=1.02)

    ax2a.plot(y_centers, density_prof, "b-", linewidth=2)
    ax2a.fill_between(y_centers, 0, density_prof, alpha=0.2, color="blue")
    ax2a.set_xlabel("z [Å]", fontsize=12)
    ax2a.set_ylabel("Particle count per bin", fontsize=12)
    ax2a.set_title("(a) Density Profile n(z)", fontsize=11)
    ax2a.grid(alpha=0.3)

    ax2b.plot(y_centers, delta_prof, "r-", linewidth=2)
    ax2b.set_xlabel("z [Å]", fontsize=12)
    ax2b.set_ylabel("δ_nuc(z)", fontsize=12)
    ax2b.set_title("(b) Delocalization Profile δ_nuc(z)", fontsize=11)
    ax2b.grid(alpha=0.3)
    ax2b_twin = ax2b.twinx()
    dn = density_prof / max(density_prof.max(), 1)
    ax2b_twin.plot(y_centers, dn, "b--", alpha=0.3, linewidth=1, label="n(z)")
    ax2b_twin.set_ylabel("n(z) / n_bulk", fontsize=10, color="blue")
    ax2b_twin.tick_params(axis="y", labelcolor="blue")

    fig2.tight_layout()
    fig2.savefig(os.path.join(FIGDIR, "fig_w2_surface_profile.png"),
                 dpi=150, bbox_inches="tight")
    print(f"  Saved: fig_w2_surface_profile.png")

    # === Fig W3: MC results ===
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(13, 5))
    fig3.suptitle("Monte Carlo: 2D Water-like Fluid", fontsize=14, y=1.02)

    mc_T_C = np.array(mc_results["T"]) - 273.15
    mc_rho = np.array(mc_results["rho"])
    mc_delta = np.array(mc_results["delta_nuc"])
    mc_rho_norm = mc_rho / mc_rho.max() if mc_rho.max() > 0 else mc_rho

    ax3a.plot(mc_T_C, mc_rho_norm, "bo-", linewidth=2, markersize=6)
    ax3a.set_xlabel("Temperature [°C]", fontsize=12)
    ax3a.set_ylabel("ρ / ρ_max (2D)", fontsize=12)
    ax3a.set_title("(a) Normalized Density vs Temperature", fontsize=11)
    ax3a.grid(alpha=0.3)

    ax3b.scatter(mc_delta, mc_rho_norm, c=mc_T_C, cmap="coolwarm",
                 s=80, edgecolors="black", linewidth=0.5, zorder=5)
    plt.colorbar(ax3b.collections[0], ax=ax3b, label="Temperature [°C]")
    ax3b.set_xlabel("δ_nuc (MC)", fontsize=12)
    ax3b.set_ylabel("ρ / ρ_max (2D)", fontsize=12)
    ax3b.set_title("(b) Density vs δ_nuc (MC)", fontsize=11)
    ax3b.grid(alpha=0.3)

    fig3.tight_layout()
    fig3.savefig(os.path.join(FIGDIR, "fig_w3_mc_density.png"),
                 dpi=150, bbox_inches="tight")
    print(f"  Saved: fig_w3_mc_density.png")

    # === Fig W4: γ vs δ ===
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    gamma_water = 75.6 - 0.14 * (T_celsius - 20)
    liquid = T_celsius >= 0
    sc = ax4.scatter(delta_nuc_model[liquid][::5], gamma_water[liquid][::5],
                c=T_celsius[liquid][::5], cmap="coolwarm", s=25, zorder=5)
    plt.colorbar(sc, ax=ax4, label="Temperature [°C]")
    ax4.set_xlabel("δ_nuc", fontsize=12)
    ax4.set_ylabel("Surface Tension γ [mN/m]", fontsize=12)
    ax4.set_title("Surface Tension vs δ_nuc", fontsize=12)
    ax4.grid(alpha=0.3)
    ax4.text(0.05, 0.95,
             "Low δ: strong H-bond → high γ\n"
             "High δ: broken network → low γ\n"
             "γ decreases monotonically with δ",
             transform=ax4.transAxes, fontsize=9, va="top",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.5))
    fig4.tight_layout()
    fig4.savefig(os.path.join(FIGDIR, "fig_w4_gamma_vs_delta.png"),
                 dpi=150, bbox_inches="tight")
    print(f"  Saved: fig_w4_gamma_vs_delta.png")

    plt.close("all")

    print(f"\nKey result: density max at T={T_max:.1f}°C, δ*={delta_at_max:.4f}")
    print("=" * 60)

    return rho_model, delta_nuc_model, T_celsius


if __name__ == "__main__":
    rho, delta, T_C = main()
