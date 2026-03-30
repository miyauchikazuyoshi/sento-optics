#!/usr/bin/env python3
"""
Test 7: Does δ_IPR determine n_ws? (Causal chain: δ → n_ws → γ)

Hypothesis: n_ws is not an independent variable but the REAL-SPACE
CONSEQUENCE of delocalization δ.

  - δ measures wavefunction spread (Hilbert space)
  - n_ws measures density at the cell boundary (real space)
  - If electrons are delocalized → density is uniform → n_ws/n_bar → 1
  - If electrons are localized → density peaks at nuclei → n_ws/n_bar → 0

This test:
  1. For DFT clusters (Li, Na): compute both IPR-δ and boundary density
     → Do they correlate? Does δ predict boundary density?
  2. Analytical model: for simple wavefunctions, derive n_ws from IPR
  3. Across metals: can we predict n_ws from electronic structure
     without Miedema tables?

If δ → n_ws is confirmed, Paper 2's narrative becomes:
  "δ (delocalization) determines how much electron density reaches
   the cell boundary (n_ws), and this boundary density controls
   surface tension through the Miedema mechanism."

This unifies with Paper 1:
  Paper 1: δ → velocity matrix elements → optical response
  Paper 2: δ → boundary electron density → surface tension

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


def compute_cluster_delta_and_boundary(element, n_atoms, bond_length,
                                        basis="def2-svp", xc="pbe",
                                        spin=None, charge=0,
                                        max_cycle=150, conv_tol=1e-9):
    """
    Compute both IPR-δ and boundary density for a linear cluster.

    "Boundary density" = electron density at the midpoint between atoms.
    This is the cluster analog of Miedema's n_ws.

    For open-shell systems (odd electron count or transition metals),
    unrestricted KS (UKS) is used automatically.
    """
    atoms = [element] * n_atoms
    coords = np.zeros((n_atoms, 3))
    for i in range(n_atoms):
        coords[i, 2] = i * bond_length - (n_atoms - 1) * bond_length / 2

    atom_str = "; ".join(
        f"{a} {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}"
        for a, c in zip(atoms, coords)
    )

    # Determine spin: if not given, auto-detect from total electrons
    if spin is None:
        mol_tmp = gto.M(atom=atom_str, basis=basis, charge=charge, verbose=0)
        n_elec = mol_tmp.nelectron
        spin = n_elec % 2  # 0 for even, 1 for odd

    mol = gto.M(atom=atom_str, basis=basis, spin=spin, charge=charge, verbose=0)

    # Use UKS for open-shell, RKS for closed-shell
    if spin > 0:
        mf = dft.UKS(mol)
    else:
        mf = dft.RKS(mol)
    mf.xc = xc
    mf.max_cycle = max_cycle
    mf.conv_tol = conv_tol
    mf.kernel()

    if not mf.converged:
        raise RuntimeError(f"SCF did not converge for {element}{n_atoms}")

    # Handle both RKS (single array) and UKS (tuple/list of alpha/beta)
    mo_coeff_raw = mf.mo_coeff
    mo_occ_raw = mf.mo_occ
    # UKS returns tuple/list, or ndarray with ndim=3
    is_unrestricted = (isinstance(mo_coeff_raw, (list, tuple))
                       or (isinstance(mo_coeff_raw, np.ndarray)
                           and mo_coeff_raw.ndim == 3))

    if is_unrestricted:
        # Combine alpha and beta for IPR analysis (use alpha channel)
        mo_coeff = mo_coeff_raw[0]
        mo_occ = mo_occ_raw[0]
    else:
        mo_coeff = mo_coeff_raw
        mo_occ = mo_occ_raw

    n_occ = int(np.sum(mo_occ > 0))
    n_ao = mo_coeff.shape[0]
    S = mol.intor("int1e_ovlp")

    # IPR in AO basis (alpha channel for UKS)
    iprs = []
    for n in range(n_occ):
        c_n = mo_coeff[:, n]
        p_mu = np.abs(c_n * (S @ c_n))
        p_sum = p_mu.sum()
        if p_sum > 1e-10:
            ipr = np.sum(p_mu**2) / p_sum**2
        else:
            ipr = 1.0
        iprs.append(ipr)

    # For UKS, also include beta IPR values
    if is_unrestricted:
        mo_coeff_b = mo_coeff_raw[1]
        mo_occ_b = mo_occ_raw[1]
        n_occ_b = int(np.sum(mo_occ_b > 0))
        for n in range(n_occ_b):
            c_n = mo_coeff_b[:, n]
            p_mu = np.abs(c_n * (S @ c_n))
            p_sum = p_mu.sum()
            if p_sum > 1e-10:
                ipr = np.sum(p_mu**2) / p_sum**2
            else:
                ipr = 1.0
            iprs.append(ipr)

    mean_ipr = np.mean(iprs)
    delta_ipr = 1.0 / (n_ao * mean_ipr) if mean_ipr > 0 else 0.0

    # Density along z-axis
    z_range = np.linspace(coords[:, 2].min() - 4.0,
                          coords[:, 2].max() + 4.0, 500)
    grid_points = np.zeros((len(z_range), 3))
    grid_points[:, 2] = z_range
    ao_vals = mol.eval_gto("GTOval_sph", grid_points)

    # Compute total density from all occupied MOs (both spins)
    density = np.zeros(len(z_range))
    if is_unrestricted:
        for s, (mc, mo) in enumerate(zip(mo_coeff_raw, mo_occ_raw)):
            for n in range(mc.shape[1]):
                if mo[n] > 0:
                    psi_n = ao_vals @ mc[:, n]
                    density += mo[n] * psi_n**2
    else:
        for n in range(mo_coeff.shape[1]):
            if mo_occ[n] > 0:
                psi_n = ao_vals @ mo_coeff[:, n]
                density += mo_occ[n] * psi_n**2

    # Boundary density: density at midpoints between atoms
    boundary_densities = []
    for i in range(n_atoms - 1):
        z_mid = (coords[i, 2] + coords[i + 1, 2]) / 2.0
        idx = np.argmin(np.abs(z_range - z_mid))
        boundary_densities.append(density[idx])
    mean_boundary = np.mean(boundary_densities) if boundary_densities else 0.0

    # Nuclear density: density at atomic positions
    nuclear_densities = []
    for i in range(n_atoms):
        idx = np.argmin(np.abs(z_range - coords[i, 2]))
        nuclear_densities.append(density[idx])
    mean_nuclear = np.mean(nuclear_densities)

    # Boundary ratio: n_boundary / n_nuclear (analog of n_ws/n_bar)
    boundary_ratio = mean_boundary / mean_nuclear if mean_nuclear > 0 else 0.0

    # Average density
    mean_density = np.mean(density[density > density.max() * 0.01])

    return {
        "element": element,
        "n_atoms": n_atoms,
        "bond_length": bond_length,
        "delta_ipr": delta_ipr,
        "mean_ipr": mean_ipr,
        "n_ao": n_ao,
        "n_occ": n_occ,
        "mean_boundary": mean_boundary,
        "mean_nuclear": mean_nuclear,
        "boundary_ratio": boundary_ratio,
        "mean_density": mean_density,
        "z_grid": z_range,
        "density": density,
        "atom_coords": coords,
        "total_energy": mf.e_tot,
    }


def main():
    print("=" * 70)
    print("TEST 7: Does δ Determine Boundary Density?")
    print("Causal chain: δ → n_ws → γ")
    print("=" * 70)

    if not HAS_PYSCF:
        print("PySCF not available.")
        return

    # Test systems: vary element and cluster size
    # Format: (element, n_atoms, bond_length_Angstrom, kwargs_dict)
    # Bond lengths from NIST/CRC dimer data (re values)
    systems = [
        # Original elements
        ("Li", 2, 2.67, {}),
        ("Li", 4, 2.67, {}),
        ("Li", 6, 2.67, {}),
        ("Na", 2, 3.08, {}),
        ("Na", 4, 3.08, {}),
        ("Na", 6, 3.08, {}),
        ("Be", 2, 2.45, {}),   # More tightly bound
        ("Be", 4, 2.45, {}),
        ("Mg", 2, 3.89, {}),   # sp metal, larger
        ("Mg", 4, 3.89, {}),
        # New elements — dimers only (N=2 is most reliable)
        ("Al", 2, 2.70, {"spin": 2, "max_cycle": 300, "conv_tol": 1e-8}),  # Al2: triplet, re ~ 2.70 Å
        ("K",  2, 3.92, {}),           # K2:  re ~ 3.92 Å
        ("Ca", 2, 4.28, {}),           # Ca2: re ~ 4.28 Å
        ("Cu", 2, 2.22, {"spin": 0, "max_cycle": 200, "conv_tol": 1e-8}),  # Cu2: re ~ 2.22 Å
        ("Zn", 2, 4.19, {"max_cycle": 200, "conv_tol": 1e-8}),  # Zn2: re ~ 4.19 Å (van der Waals)
        ("Si", 2, 2.25, {"spin": 2, "max_cycle": 300, "conv_tol": 1e-8}),  # Si2: triplet ground state
        ("Ga", 2, 2.75, {"spin": 2, "max_cycle": 300, "conv_tol": 1e-8}),  # Ga2: triplet, re ~ 2.75 Å
    ]

    results = []
    failed = []
    for item in systems:
        elem, n, bl = item[0], item[1], item[2]
        kwargs = item[3] if len(item) > 3 else {}
        label = f"{elem}{n}"
        print(f"  Computing {label}...")
        try:
            res = compute_cluster_delta_and_boundary(elem, n, bl, **kwargs)
            results.append(res)
            print(f"    δ_IPR = {res['delta_ipr']:.4f}, "
                  f"n_boundary = {res['mean_boundary']:.6f}, "
                  f"n_nuclear = {res['mean_nuclear']:.6f}, "
                  f"ratio = {res['boundary_ratio']:.4f}")
        except Exception as e:
            print(f"    FAILED: {e}")
            failed.append((label, str(e)))

    if failed:
        print(f"\n  --- Failed systems ({len(failed)}) ---")
        for label, err in failed:
            print(f"    {label}: {err}")

    if len(results) < 3:
        print("Too few calculations succeeded.")
        return

    # ── Analysis ──
    delta_vals = np.array([r["delta_ipr"] for r in results])
    boundary_vals = np.array([r["mean_boundary"] for r in results])
    nuclear_vals = np.array([r["mean_nuclear"] for r in results])
    ratio_vals = np.array([r["boundary_ratio"] for r in results])
    labels = [f"{r['element']}{r['n_atoms']}" for r in results]
    elements = [r["element"] for r in results]

    from scipy.stats import pearsonr, spearmanr

    print(f"\n--- Correlation: δ_IPR vs Boundary Quantities ---")
    for name, vals in [("n_boundary", boundary_vals),
                       ("n_nuclear", nuclear_vals),
                       ("boundary_ratio (n_ws/n_nuc)", ratio_vals)]:
        rp, pp = pearsonr(delta_vals, vals)
        rs, _ = spearmanr(delta_vals, vals)
        print(f"  δ vs {name:>30s}: r = {rp:+.4f} (p = {pp:.4f}), ρ = {rs:+.4f}")

    # ── Per-element scaling ──
    print(f"\n--- Per-Element Scaling ---")
    unique_elements = list(dict.fromkeys(elements))
    for elem in unique_elements:
        mask = [e == elem for e in elements]
        d = delta_vals[mask]
        b = ratio_vals[mask]
        n_atoms = [r["n_atoms"] for r, m in zip(results, mask) if m]
        print(f"\n  {elem}:")
        print(f"    {'N':>4s}  {'δ_IPR':>8s}  {'boundary_ratio':>15s}")
        sort_idx = np.argsort(n_atoms)
        for i in sort_idx:
            print(f"    {n_atoms[i]:4d}  {d[i]:8.4f}  {b[i]:15.4f}")
        if len(d) >= 2:
            r_elem, _ = pearsonr(d, b)
            print(f"    r(δ, boundary_ratio) = {r_elem:.4f}")

    # ── Key question: does δ predict WHICH element has higher n_ws? ──
    print(f"\n--- Cross-Element Comparison (fixed N=2) ---")
    dimers = [r for r in results if r["n_atoms"] == 2]
    if len(dimers) >= 2:
        d_dimer = np.array([r["delta_ipr"] for r in dimers])
        b_dimer = np.array([r["boundary_ratio"] for r in dimers])
        n_dimer = np.array([r["mean_boundary"] for r in dimers])
        l_dimer = [f"{r['element']}₂" for r in dimers]

        print(f"  {'System':>8s}  {'δ_IPR':>8s}  {'n_boundary':>12s}  {'ratio':>8s}")
        for i in range(len(dimers)):
            print(f"  {l_dimer[i]:>8s}  {d_dimer[i]:8.4f}  "
                  f"{n_dimer[i]:12.6f}  {b_dimer[i]:8.4f}")

        if len(dimers) >= 3:
            r_cross, p_cross = pearsonr(d_dimer, b_dimer)
            print(f"\n  r(δ_IPR, boundary_ratio) across elements: {r_cross:.4f} (p={p_cross:.4f})")
            r_cross_n, p_cross_n = pearsonr(d_dimer, n_dimer)
            print(f"  r(δ_IPR, n_boundary) across elements: {r_cross_n:.4f} (p={p_cross_n:.4f})")

    # ── Verdict ──
    print(f"\n{'='*70}")
    print("VERDICT: Does δ determine boundary density?")
    print(f"{'='*70}")

    r_overall, p_overall = pearsonr(delta_vals, ratio_vals)
    r_boundary, p_boundary = pearsonr(delta_vals, boundary_vals)

    if r_overall > 0.7:
        print(f"  ✓ STRONG: δ_IPR correlates with boundary ratio (r = {r_overall:.3f})")
        print(f"    → δ determines n_ws: delocalized electrons reach the boundary")
    elif r_overall > 0.4:
        print(f"  △ MODERATE: δ_IPR correlates with boundary ratio (r = {r_overall:.3f})")
        print(f"    → Some connection, but other factors also matter")
    else:
        print(f"  ✗ WEAK: δ_IPR and boundary ratio poorly correlated (r = {r_overall:.3f})")
        print(f"    → δ and n_ws may be more independent than hypothesized")

    print(f"\n  δ vs n_boundary (absolute): r = {r_boundary:.3f} (p = {p_boundary:.4f})")
    print(f"  δ vs boundary_ratio (relative): r = {r_overall:.3f} (p = {p_overall:.4f})")

    # ── Figure ──
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("Test 7: Does Delocalization (δ) Determine Boundary Density (n_ws)?",
                 fontsize=14, y=1.02)

    # Color by element
    elem_colors = {"Li": "steelblue", "Na": "orange", "Be": "green",
                   "Mg": "purple", "Al": "red", "K": "brown",
                   "Ca": "darkviolet", "Cu": "darkorange", "Zn": "teal",
                   "Si": "crimson", "Ga": "olive"}

    # (a) Density profiles for dimers
    ax = axes[0, 0]
    for r in dimers:
        c = elem_colors.get(r["element"], "gray")
        z = r["z_grid"]
        rho = r["density"]
        ax.plot(z, rho / rho.max(), color=c, linewidth=2,
                label=f"{r['element']}₂ (δ={r['delta_ipr']:.3f})")
        # Mark boundary midpoint
        z_mid = 0.0  # midpoint of dimer
        idx_mid = np.argmin(np.abs(z - z_mid))
        ax.plot(z_mid, rho[idx_mid] / rho.max(), "ko", markersize=8, zorder=5)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_xlabel("z [Å]", fontsize=11)
    ax.set_ylabel("ρ(z) / ρ_max", fontsize=11)
    ax.set_title("(a) Density profiles (dimers)\nDots = boundary midpoints", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) δ vs boundary ratio (all systems)
    ax = axes[0, 1]
    for i, r in enumerate(results):
        c = elem_colors.get(r["element"], "gray")
        ax.scatter(r["delta_ipr"], r["boundary_ratio"],
                   s=80 + r["n_atoms"] * 15, c=c,
                   edgecolors="black", linewidth=0.5, zorder=5)
        ax.annotate(f"{r['element']}{r['n_atoms']}", (r["delta_ipr"], r["boundary_ratio"]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlabel("δ_IPR (delocalization)", fontsize=11)
    ax.set_ylabel("Boundary ratio (n_boundary / n_nuclear)", fontsize=11)
    ax.set_title(f"(b) δ vs boundary ratio: r = {r_overall:.3f}", fontsize=10)
    ax.grid(alpha=0.3)

    # (c) δ vs absolute boundary density
    ax = axes[0, 2]
    for i, r in enumerate(results):
        c = elem_colors.get(r["element"], "gray")
        ax.scatter(r["delta_ipr"], r["mean_boundary"],
                   s=80 + r["n_atoms"] * 15, c=c,
                   edgecolors="black", linewidth=0.5, zorder=5)
        ax.annotate(f"{r['element']}{r['n_atoms']}", (r["delta_ipr"], r["mean_boundary"]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.set_xlabel("δ_IPR", fontsize=11)
    ax.set_ylabel("n_boundary (absolute) [a.u.⁻³]", fontsize=11)
    ax.set_title(f"(c) δ vs n_boundary: r = {r_boundary:.3f}", fontsize=10)
    ax.grid(alpha=0.3)

    # (d) Per-element trends: δ vs boundary ratio
    ax = axes[1, 0]
    for elem in unique_elements:
        mask = [e == elem for e in elements]
        d = delta_vals[mask]
        b = ratio_vals[mask]
        n_at = [r["n_atoms"] for r, m in zip(results, mask) if m]
        c = elem_colors.get(elem, "gray")
        sort_idx = np.argsort(n_at)
        ax.plot(np.array(d)[sort_idx], np.array(b)[sort_idx],
                "o-", color=c, markersize=8, linewidth=2, label=elem)
        for i in sort_idx:
            ax.annotate(f"N={n_at[i]}", (d[i], b[i]),
                        textcoords="offset points", xytext=(5, -10), fontsize=7)
    ax.set_xlabel("δ_IPR", fontsize=11)
    ax.set_ylabel("Boundary ratio", fontsize=11)
    ax.set_title("(d) Per-element: δ vs boundary ratio", fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # (e) Cross-element dimers
    ax = axes[1, 1]
    if len(dimers) >= 2:
        for r in dimers:
            c = elem_colors.get(r["element"], "gray")
            ax.scatter(r["delta_ipr"], r["boundary_ratio"],
                       s=150, c=c, edgecolors="black", linewidth=1, zorder=5)
            ax.annotate(f"{r['element']}₂", (r["delta_ipr"], r["boundary_ratio"]),
                        textcoords="offset points", xytext=(8, 5), fontsize=11,
                        fontweight="bold")
        if len(dimers) >= 3:
            c_fit = np.polyfit(d_dimer, b_dimer, 1)
            x_fit = np.linspace(d_dimer.min() * 0.8, d_dimer.max() * 1.2, 100)
            ax.plot(x_fit, np.polyval(c_fit, x_fit), "k--", alpha=0.3)
    ax.set_xlabel("δ_IPR", fontsize=11)
    ax.set_ylabel("Boundary ratio", fontsize=11)
    ax.set_title("(e) Dimers: cross-element comparison", fontsize=10)
    ax.grid(alpha=0.3)

    # (f) Conceptual diagram
    ax = axes[1, 2]
    ax.axis("off")
    ax.text(0.5, 0.92, "Proposed Causal Chain", fontsize=13,
            ha="center", fontweight="bold", transform=ax.transAxes)

    # Draw chain
    boxes = [
        (0.5, 0.72, "δ (IPR)\nWavefunction spread\n(Hilbert space)"),
        (0.5, 0.45, "n_ws\nBoundary electron density\n(Real space)"),
        (0.5, 0.18, "γ\nSurface tension\n(Thermodynamics)"),
    ]
    for x, y, text in boxes:
        ax.add_patch(plt.Rectangle((x - 0.2, y - 0.08), 0.4, 0.16,
                                     facecolor="lightyellow", edgecolor="black",
                                     linewidth=1.5, transform=ax.transAxes))
        ax.text(x, y, text, ha="center", va="center", fontsize=9,
                transform=ax.transAxes)

    # Arrows
    for y_start, y_end, label in [(0.64, 0.53, "determines"),
                                    (0.37, 0.26, "Miedema")]:
        ax.annotate("", xy=(0.5, y_end), xytext=(0.5, y_start),
                    xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops=dict(arrowstyle="->", lw=2, color="darkblue"))
        ax.text(0.72, (y_start + y_end) / 2, label, fontsize=9,
                color="darkblue", ha="left", transform=ax.transAxes)

    # Paper 1 parallel
    ax.text(0.5, 0.02,
            "Paper 1: δ → velocity matrix → ε(ω)\n"
            "Paper 2: δ → boundary density → γ",
            ha="center", va="bottom", fontsize=9,
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig_test7_delta_causes_nws.png"),
                dpi=150, bbox_inches="tight")
    print(f"\nSaved: {os.path.join(FIGDIR, 'fig_test7_delta_causes_nws.png')}")
    plt.close("all")


if __name__ == "__main__":
    main()
