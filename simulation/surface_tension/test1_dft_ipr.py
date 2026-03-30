#!/usr/bin/env python3
"""
Test 1: DFT-based IPR calculation for metal clusters.

Critical question: Is the delocalization index δ (defined as 1/(N×⟨IPR⟩)
in Paper 1) genuinely different from normalized electron density n(z)/n̄?

Approach:
  - Use PySCF to compute DFT wavefunctions for small metal clusters
  - Compute IPR from KS orbitals: IPR_n = Σ_i |ψ_n(r_i)|⁴ / (Σ_i |ψ_n(r_i)|²)²
  - Compare IPR-derived δ with density-derived δ = n(z)/n̄
  - If they differ → δ carries genuine delocalization information
  - If they're the same → δ is indeed just density repackaged

Systems:
  - Na clusters: Na₂, Na₄, Na₈ (free-electron-like, sp-metal)
  - Small comparison: Li₂ vs Na₂ (different r_s, should show δ scaling)

Limitation: Clusters ≠ surfaces. But this tests whether IPR-δ and
density-δ are mathematically distinct quantities, which is the core
question.

Author: K. Miyauchi
"""

import numpy as np
import matplotlib.pyplot as plt
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)

try:
    from pyscf import gto, dft
    HAS_PYSCF = True
except ImportError:
    HAS_PYSCF = False
    print("WARNING: PySCF not available. Using analytical model fallback.")


def compute_cluster_ipr_pyscf(atoms, coords, basis="def2-svp", xc="pbe"):
    """
    Compute KS orbital IPR for a metal cluster using PySCF DFT.

    Returns:
        eigenvalues, ipr_per_orbital, delta_ipr, density_on_grid, grid_coords
    """
    # Build molecule
    atom_str = "; ".join(
        f"{a} {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}"
        for a, c in zip(atoms, coords)
    )

    mol = gto.M(atom=atom_str, basis=basis, spin=0, charge=0, verbose=0)

    # DFT calculation
    mf = dft.RKS(mol)
    mf.xc = xc
    mf.kernel()

    if not mf.converged:
        print(f"  WARNING: SCF not converged for {atom_str[:20]}...")

    # Get MO coefficients and occupation
    mo_coeff = mf.mo_coeff  # (nao, nmo)
    mo_occ = mf.mo_occ      # (nmo,)
    mo_energy = mf.mo_energy # (nmo,)

    n_occ = int(np.sum(mo_occ > 0))
    n_ao = mo_coeff.shape[0]

    # Compute IPR in AO basis
    # |ψ_n⟩ = Σ_μ C_μn |φ_μ⟩
    # Probability on AO μ: p_μn = |C_μn|²  (Mulliken-like)
    # IPR_n = Σ_μ p_μn² / (Σ_μ p_μn)²

    # But properly: use overlap matrix S
    # p_μn = Σ_ν C_μn S_μν C_νn (Mulliken population)
    S = mol.intor("int1e_ovlp")

    iprs = []
    for n in range(n_occ):
        c_n = mo_coeff[:, n]
        # Mulliken population: p_μ = c_μ × (S @ c)_μ
        p_mu = c_n * (S @ c_n)
        p_mu = np.abs(p_mu)  # ensure positive
        p_sum = p_mu.sum()
        if p_sum > 1e-10:
            ipr = np.sum(p_mu**2) / p_sum**2
        else:
            ipr = 1.0
        iprs.append(ipr)

    iprs = np.array(iprs)
    mean_ipr = np.mean(iprs)
    delta_ipr = 1.0 / (n_ao * mean_ipr) if mean_ipr > 0 else 0.0

    # Also compute electron density along z-axis for comparison
    # Grid along z through center of molecule
    z_range = np.linspace(
        coords[:, 2].min() - 3.0,
        coords[:, 2].max() + 3.0,
        200
    )
    grid_points = np.zeros((len(z_range), 3))
    grid_points[:, 2] = z_range

    # Evaluate AOs on grid
    ao_vals = mol.eval_gto("GTOval_sph", grid_points)  # (ngrid, nao)

    # Density: ρ(r) = Σ_n f_n |ψ_n(r)|²
    density = np.zeros(len(z_range))
    for n in range(mo_coeff.shape[1]):
        if mo_occ[n] > 0:
            psi_n = ao_vals @ mo_coeff[:, n]  # (ngrid,)
            density += mo_occ[n] * psi_n**2

    # "Density-based δ": normalize to peak
    rho_max = density.max()
    delta_density = density / rho_max if rho_max > 0 else density

    # Local IPR on grid: for each grid point, compute IPR of
    # the orbital amplitudes across occupied MOs
    # This is a different but complementary measure
    local_ipr = np.zeros(len(z_range))
    for g in range(len(z_range)):
        psi_vals = np.array([
            (ao_vals[g] @ mo_coeff[:, n])**2
            for n in range(n_occ)
        ])
        psi_sum = psi_vals.sum()
        if psi_sum > 1e-20:
            local_ipr[g] = np.sum(psi_vals**2) / psi_sum**2
        else:
            local_ipr[g] = 1.0

    # Local δ from IPR
    delta_local_ipr = np.where(
        local_ipr > 1e-10,
        1.0 / (n_occ * local_ipr),
        0.0
    )
    # Clip to [0, 1] range
    delta_local_ipr = np.clip(delta_local_ipr, 0, 1)

    return {
        "mo_energy": mo_energy[:n_occ],
        "iprs": iprs,
        "mean_ipr": mean_ipr,
        "delta_ipr": delta_ipr,
        "n_ao": n_ao,
        "n_occ": n_occ,
        "z_grid": z_range,
        "density": density,
        "delta_density": delta_density,
        "local_ipr": local_ipr,
        "delta_local_ipr": delta_local_ipr,
        "total_energy": mf.e_tot,
    }


def make_linear_cluster(element, n_atoms, bond_length):
    """Create linear cluster coordinates."""
    atoms = [element] * n_atoms
    coords = np.zeros((n_atoms, 3))
    for i in range(n_atoms):
        coords[i, 2] = i * bond_length - (n_atoms - 1) * bond_length / 2
    return atoms, coords


def main():
    print("=" * 70)
    print("TEST 1: DFT IPR-based δ vs Density-based δ")
    print("Are they genuinely different quantities?")
    print("=" * 70)

    if not HAS_PYSCF:
        print("\nPySCF not available. Cannot run DFT calculations.")
        print("Install with: pip install pyscf")
        return

    # Define test systems
    # Bond lengths from literature (Å):
    # Na₂: 3.08 Å, Li₂: 2.67 Å
    systems = {
        "Li₂": {"element": "Li", "n": 2, "bond": 2.67},
        "Na₂": {"element": "Na", "n": 2, "bond": 3.08},
        "Li₄": {"element": "Li", "n": 4, "bond": 2.67},
        "Na₄": {"element": "Na", "n": 4, "bond": 3.08},
        "Li₆": {"element": "Li", "n": 6, "bond": 2.67},
        "Na₆": {"element": "Na", "n": 6, "bond": 3.08},
    }

    all_results = {}

    for sys_name, params in systems.items():
        print(f"\n  Computing {sys_name}...")
        atoms, coords = make_linear_cluster(
            params["element"], params["n"], params["bond"]
        )
        try:
            res = compute_cluster_ipr_pyscf(atoms, coords)
            all_results[sys_name] = res
            print(f"    E_tot = {res['total_energy']:.6f} Ha")
            print(f"    n_AO = {res['n_ao']}, n_occ = {res['n_occ']}")
            print(f"    ⟨IPR⟩ = {res['mean_ipr']:.4f}")
            print(f"    δ_IPR = 1/(N×⟨IPR⟩) = {res['delta_ipr']:.4f}")
        except Exception as e:
            print(f"    FAILED: {e}")

    if len(all_results) == 0:
        print("No calculations completed.")
        return

    # ── Analysis: Compare δ_density vs δ_IPR ──
    print("\n" + "=" * 70)
    print("ANALYSIS: Are density-δ and IPR-δ correlated?")
    print("=" * 70)

    # For each system, compute correlation between delta_density and delta_local_ipr
    print(f"\n{'System':>8s}  {'δ_IPR':>8s}  {'⟨IPR⟩':>8s}  "
          f"{'r(ρ,IPR)':>10s}  {'Peak δ_ρ':>10s}  {'Peak δ_IPR':>10s}")
    print("-" * 65)

    for sys_name, res in all_results.items():
        # Correlation between density-δ and local-IPR-δ on the grid
        # Only where density is non-negligible
        mask = res["density"] > res["density"].max() * 0.01
        if mask.sum() > 5:
            from scipy.stats import pearsonr
            r_corr, _ = pearsonr(
                res["delta_density"][mask],
                res["delta_local_ipr"][mask]
            )
        else:
            r_corr = np.nan

        peak_rho = res["delta_density"].max()
        peak_ipr = res["delta_local_ipr"].max()
        print(f"{sys_name:>8s}  {res['delta_ipr']:8.4f}  {res['mean_ipr']:8.4f}  "
              f"{r_corr:10.4f}  {peak_rho:10.4f}  {peak_ipr:10.4f}")

    # ── Key test: does IPR-δ scale differently from density-δ with cluster size? ──
    print(f"\n── Scaling with cluster size ──")
    for element in ["Li", "Na"]:
        sizes = []
        delta_iprs = []
        delta_rhos = []
        for sys_name, res in all_results.items():
            if element in sys_name:
                n = int(sys_name.split("₂")[0].split("₄")[0].split("₆")[0].replace(element, "").replace("₂", "2").replace("₄", "4").replace("₆", "6") or "0")
                # Extract size from name
                for char in sys_name:
                    if char in "₂₄₆":
                        n = {"₂": 2, "₄": 4, "₆": 6}[char]
                sizes.append(n)
                delta_iprs.append(res["delta_ipr"])
                # Use max density in central region as density-δ proxy
                z = res["z_grid"]
                center_mask = np.abs(z) < 1.0
                if center_mask.any():
                    delta_rhos.append(res["density"][center_mask].mean())
                else:
                    delta_rhos.append(res["density"].max())

        if len(sizes) >= 2:
            sizes = np.array(sizes)
            delta_iprs = np.array(delta_iprs)
            delta_rhos = np.array(delta_rhos)
            # Normalize
            delta_rhos_norm = delta_rhos / delta_rhos.max()
            delta_iprs_norm = delta_iprs / delta_iprs.max() if delta_iprs.max() > 0 else delta_iprs

            sort_idx = np.argsort(sizes)
            print(f"\n  {element} clusters:")
            print(f"    {'N':>4s}  {'δ_IPR':>10s}  {'δ_IPR/max':>10s}  {'ρ_center':>10s}  {'ρ/max':>10s}")
            for i in sort_idx:
                print(f"    {sizes[i]:4d}  {delta_iprs[i]:10.4f}  "
                      f"{delta_iprs_norm[i]:10.4f}  {delta_rhos[i]:10.6f}  "
                      f"{delta_rhos_norm[i]:10.4f}")

    # ── Verdict ──
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Check if density-δ and IPR-δ differ significantly
    all_corrs = []
    for sys_name, res in all_results.items():
        mask = res["density"] > res["density"].max() * 0.01
        if mask.sum() > 5:
            from scipy.stats import pearsonr
            r_corr, _ = pearsonr(
                res["delta_density"][mask],
                res["delta_local_ipr"][mask]
            )
            all_corrs.append(r_corr)

    if all_corrs:
        mean_corr = np.mean(all_corrs)
        if mean_corr > 0.95:
            print(f"  FAIL: δ_density and δ_IPR are highly correlated "
                  f"(mean r = {mean_corr:.3f})")
            print(f"        In these systems, IPR adds no information beyond density.")
        elif mean_corr > 0.7:
            print(f"  PARTIAL: δ_density and δ_IPR are moderately correlated "
                  f"(mean r = {mean_corr:.3f})")
            print(f"           IPR captures SOME additional information.")
        else:
            print(f"  PASS: δ_density and δ_IPR are distinct quantities "
                  f"(mean r = {mean_corr:.3f})")
            print(f"        IPR-based δ genuinely differs from density-based δ.")

    # ── Figure ──
    n_sys = len(all_results)
    fig, axes = plt.subplots(2, max(n_sys, 2), figsize=(5 * max(n_sys, 2), 9))
    fig.suptitle("Test 1: DFT IPR-based δ vs Density-based δ", fontsize=14, y=1.02)

    for idx, (sys_name, res) in enumerate(all_results.items()):
        # Top row: density and IPR profiles
        ax = axes[0, idx] if n_sys > 1 else axes[0]
        z = res["z_grid"]
        ax.plot(z, res["delta_density"], "b-", linewidth=2, label="δ_density = ρ/ρ_max")
        ax.plot(z, res["delta_local_ipr"], "r--", linewidth=2, label="δ_IPR (local)")
        ax.set_xlabel("z [Å]", fontsize=11)
        ax.set_ylabel("δ(z)", fontsize=11)
        ax.set_title(f"{sys_name}", fontsize=11)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)
        ax.set_ylim(-0.05, 1.2)

        # Bottom row: scatter of δ_density vs δ_IPR
        ax = axes[1, idx] if n_sys > 1 else axes[1]
        mask = res["density"] > res["density"].max() * 0.01
        ax.scatter(res["delta_density"][mask], res["delta_local_ipr"][mask],
                   s=10, c="steelblue", alpha=0.5)
        ax.plot([0, 1], [0, 1], "k--", alpha=0.3, label="y=x")
        ax.set_xlabel("δ_density", fontsize=11)
        ax.set_ylabel("δ_IPR", fontsize=11)
        if mask.sum() > 5:
            from scipy.stats import pearsonr
            r, _ = pearsonr(res["delta_density"][mask], res["delta_local_ipr"][mask])
            ax.set_title(f"{sys_name}: r = {r:.3f}", fontsize=11)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    # Hide unused axes
    for idx in range(len(all_results), axes.shape[1]):
        axes[0, idx].axis("off")
        axes[1, idx].axis("off")

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test1_dft_ipr.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test1_dft_ipr.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
