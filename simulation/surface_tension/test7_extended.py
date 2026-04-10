#!/usr/bin/env python3
"""
Test 7 Extended: Expanded element set + valence-only δ_IPR

Addresses reviewer concerns:
1. Expand from 11 to 16+ elements (add Fe, Ni, Ag, Au, Pt, W, Ti)
2. Compute valence-only δ_IPR (energy-windowed) alongside all-electron δ_IPR
3. Report both and compare correlations with boundary density

Valence-only δ_IPR: exclude states below a core-valence threshold.
The threshold is element-specific (e.g., for Cu: exclude 1s,2s,2p,3s,3p core).
We use orbital energy to separate: states with ε < ε_threshold are core.

Author: K. Miyauchi
"""

import numpy as np
import os
import json

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)

try:
    from pyscf import gto, dft
    HAS_PYSCF = True
except ImportError:
    HAS_PYSCF = False
    print("PySCF not available. Cannot run calculations.")

# === Element data ===
# bond_length in Angstrom (experimental dimer bond lengths)
# n_core: number of core electrons per atom (for valence-only IPR)
# spin: ground state spin of dimer (0=singlet, 1=doublet, etc.)
ELEMENTS = {
    # Original 11
    'Li':  {'bond': 2.673, 'n_core': 2,  'spin': 0, 'type': 'sp'},
    'Na':  {'bond': 3.079, 'n_core': 10, 'spin': 0, 'type': 'sp'},
    'K':   {'bond': 3.924, 'n_core': 18, 'spin': 0, 'type': 'sp'},
    'Be':  {'bond': 2.460, 'n_core': 2,  'spin': 0, 'type': 'sp'},
    'Mg':  {'bond': 3.891, 'n_core': 10, 'spin': 0, 'type': 'sp'},
    'Ca':  {'bond': 4.277, 'n_core': 18, 'spin': 0, 'type': 'sp'},
    'Al':  {'bond': 2.701, 'n_core': 10, 'spin': 2, 'type': 'sp'},
    'Si':  {'bond': 2.246, 'n_core': 10, 'spin': 2, 'type': 'sp'},
    'Ga':  {'bond': 2.750, 'n_core': 28, 'spin': 2, 'type': 'sp'},
    'Cu':  {'bond': 2.220, 'n_core': 18, 'spin': 0, 'type': 'd'},
    'Zn':  {'bond': 4.190, 'n_core': 28, 'spin': 0, 'type': 'd'},
    # New additions (reviewer request)
    'Fe':  {'bond': 2.020, 'n_core': 18, 'spin': 6, 'type': 'd'},
    'Ni':  {'bond': 2.155, 'n_core': 18, 'spin': 2, 'type': 'd'},
    'Ag':  {'bond': 2.530, 'n_core': 36, 'spin': 0, 'type': 'd'},
    'Au':  {'bond': 2.472, 'n_core': 68, 'spin': 0, 'type': 'd'},
    'Ti':  {'bond': 1.942, 'n_core': 18, 'spin': 4, 'type': 'd'},
}

# Miedema n_ws^{1/3} values (de Boer et al. 1988, in (d.u.)^{1/3})
# Source: Wikipedia/HandWiki "Miedema's model", cross-verified
# WARNING: Previous version had WRONG values (n_ws in different units).
# These are the correct n_ws^{1/3} as tabulated by de Boer.
MIEDEMA_NWS13 = {
    'Li': 0.98, 'Na': 0.82, 'K': 0.65, 'Be': 1.67, 'Mg': 1.17,
    'Ca': 0.91, 'Al': 1.39, 'Si': 1.50, 'Ga': 1.31, 'Cu': 1.47,
    'Zn': 1.32, 'Fe': 1.77, 'Ni': 1.75, 'Ag': 1.36, 'Au': 1.57,
    'Ti': 1.52,
}

# Surface tension (mN/m) at melting
GAMMA = {
    'Li': 398, 'Na': 191, 'K': 101, 'Be': 1145, 'Mg': 559,
    'Ca': 361, 'Al': 1050, 'Si': 865, 'Ga': 718, 'Cu': 1285,
    'Zn': 782, 'Fe': 1872, 'Ni': 1778, 'Ag': 903, 'Au': 1169,
    'Ti': 1650,
}


def compute_dimer(element, info, basis="def2-svp", xc="b3lyp"):
    """
    Compute all-electron and valence-only δ_IPR + boundary density for a dimer.
    """
    bond = info['bond']
    spin = info['spin']
    n_core_per_atom = info['n_core']

    atom_str = f"{element} 0 0 {-bond/2:.6f}; {element} 0 0 {bond/2:.6f}"

    mol = gto.M(atom=atom_str, basis=basis, spin=spin, charge=0, verbose=0)

    if spin > 0:
        mf = dft.UKS(mol)
    else:
        mf = dft.RKS(mol)
    mf.xc = xc
    mf.max_cycle = 200
    mf.conv_tol = 1e-9
    mf.kernel()

    if not mf.converged:
        print(f"  WARNING: SCF not converged for {element}2")
        return None

    # Get MO info
    mo_coeff_raw = mf.mo_coeff
    mo_occ_raw = mf.mo_occ
    mo_energy_raw = mf.mo_energy

    is_unrestricted = (isinstance(mo_coeff_raw, (list, tuple))
                       or (isinstance(mo_coeff_raw, np.ndarray)
                           and mo_coeff_raw.ndim == 3))

    S = mol.intor("int1e_ovlp")
    n_ao = S.shape[0]

    # Collect all occupied orbital data (both spins)
    all_iprs = []
    all_energies = []
    valence_iprs = []
    valence_energies = []

    # Total core electrons in dimer
    n_core_total = 2 * n_core_per_atom

    def process_spin(mc, mo, me):
        """Process one spin channel."""
        iprs_out = []
        energies_out = []
        n_occ = int(np.sum(mo > 0))
        for n in range(n_occ):
            c_n = mc[:, n]
            p_mu = np.abs(c_n * (S @ c_n))
            p_sum = p_mu.sum()
            if p_sum > 1e-10:
                ipr = np.sum(p_mu**2) / p_sum**2
            else:
                ipr = 1.0
            iprs_out.append(ipr)
            energies_out.append(me[n])
        return iprs_out, energies_out

    if is_unrestricted:
        for s in range(2):
            iprs_s, ens_s = process_spin(mo_coeff_raw[s], mo_occ_raw[s], mo_energy_raw[s])
            all_iprs.extend(iprs_s)
            all_energies.extend(ens_s)
    else:
        iprs_s, ens_s = process_spin(mo_coeff_raw, mo_occ_raw, mo_energy_raw)
        all_iprs.extend(iprs_s)
        all_energies.extend(ens_s)

    # All-electron δ_IPR
    mean_ipr_all = np.mean(all_iprs) if all_iprs else 1.0
    delta_all = 1.0 / (n_ao * mean_ipr_all) if mean_ipr_all > 0 else 0.0

    # Valence-only δ_IPR: sort by energy, skip lowest n_core_total/2 per spin
    # For UKS: skip n_core_per_atom states per spin channel
    # Simpler approach: sort all states by energy, skip the lowest n_core_total
    paired = list(zip(all_energies, all_iprs))
    paired.sort(key=lambda x: x[0])

    # For RKS, each "state" is doubly occupied, so n_core_total states to skip
    # For UKS, each state is singly occupied, skip n_core_total states
    if is_unrestricted:
        n_skip = n_core_total
    else:
        n_skip = n_core_total // 2  # RKS: each orbital holds 2 electrons

    valence_pairs = paired[n_skip:]
    if valence_pairs:
        valence_iprs = [p[1] for p in valence_pairs]
        mean_ipr_val = np.mean(valence_iprs)
        delta_val = 1.0 / (n_ao * mean_ipr_val) if mean_ipr_val > 0 else 0.0
    else:
        delta_val = 0.0

    # Boundary density at midpoint (z=0)
    grid_pt = np.array([[0.0, 0.0, 0.0]])
    ao_vals = mol.eval_gto("GTOval_sph", grid_pt)

    density_mid = 0.0
    if is_unrestricted:
        for s in range(2):
            mc = mo_coeff_raw[s]
            mo = mo_occ_raw[s]
            for n in range(mc.shape[1]):
                if mo[n] > 0:
                    psi = ao_vals @ mc[:, n]
                    density_mid += mo[n] * psi[0]**2
    else:
        mc = mo_coeff_raw
        mo = mo_occ_raw
        for n in range(mc.shape[1]):
            if mo[n] > 0:
                psi = ao_vals @ mc[:, n]
                density_mid += mo[n] * psi[0]**2

    # Density at atom position (z = -bond/2)
    grid_atom = np.array([[0.0, 0.0, -bond/2]])
    ao_atom = mol.eval_gto("GTOval_sph", grid_atom)
    density_atom = 0.0
    if is_unrestricted:
        for s in range(2):
            mc = mo_coeff_raw[s]
            mo = mo_occ_raw[s]
            for n in range(mc.shape[1]):
                if mo[n] > 0:
                    psi = ao_atom @ mc[:, n]
                    density_atom += mo[n] * psi[0]**2
    else:
        mc = mo_coeff_raw
        mo = mo_occ_raw
        for n in range(mc.shape[1]):
            if mo[n] > 0:
                psi = ao_atom @ mc[:, n]
                density_atom += mo[n] * psi[0]**2

    boundary_ratio = density_mid / density_atom if density_atom > 0 else 0.0

    return {
        'element': element,
        'delta_all': float(delta_all),
        'delta_valence': float(delta_val),
        'n_states_all': len(all_iprs),
        'n_states_valence': len(valence_iprs),
        'boundary_density': float(density_mid),
        'boundary_ratio': float(boundary_ratio),
        'converged': True,
    }


def main():
    if not HAS_PYSCF:
        return

    from scipy import stats

    print("=" * 70)
    print("Test 7 Extended: Expanded elements + valence-only δ_IPR")
    print("=" * 70)

    results = {}
    for elem in ELEMENTS:
        info = ELEMENTS[elem]
        print(f"Computing {elem}2 (spin={info['spin']}, core={info['n_core']})...",
              end=' ', flush=True)
        try:
            r = compute_dimer(elem, info)
            if r:
                results[elem] = r
                print(f"δ_all={r['delta_all']:.4f}, δ_val={r['delta_valence']:.4f}, "
                      f"ratio={r['boundary_ratio']:.4f}")
            else:
                print("FAILED (not converged)")
        except Exception as e:
            print(f"ERROR: {e}")

    # === Analysis ===
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\n{'Elem':>4} {'Type':>4} {'δ_all':>8} {'δ_val':>8} {'ratio':>8} "
          f"{'n_ws':>6} {'γ':>6}")
    print("-" * 52)

    elems_ok = [e for e in results if e in MIEDEMA_NWS13]
    for e in sorted(elems_ok, key=lambda x: ELEMENTS[x]['type']):
        r = results[e]
        nws = MIEDEMA_NWS13.get(e, 0)
        gamma = GAMMA.get(e, 0)
        print(f"{e:>4} {ELEMENTS[e]['type']:>4} {r['delta_all']:>8.4f} "
              f"{r['delta_valence']:>8.4f} {r['boundary_ratio']:>8.4f} "
              f"{nws:>6.2f} {gamma:>6}")

    # Correlations
    delta_all = np.array([results[e]['delta_all'] for e in elems_ok])
    delta_val = np.array([results[e]['delta_valence'] for e in elems_ok])
    ratios = np.array([results[e]['boundary_ratio'] for e in elems_ok])
    nws = np.array([MIEDEMA_NWS13[e] for e in elems_ok])
    gamma = np.array([GAMMA[e] for e in elems_ok])

    print("\n=== Correlations (Pearson r) ===")
    tests = [
        ('δ_all vs boundary_ratio', delta_all, ratios),
        ('δ_val vs boundary_ratio', delta_val, ratios),
        ('δ_all vs n_ws', delta_all, nws),
        ('δ_val vs n_ws', delta_val, nws),
        ('δ_all vs γ', delta_all, gamma),
        ('δ_val vs γ', delta_val, gamma),
    ]
    for name, x, y in tests:
        if len(x) >= 3:
            r, p = stats.pearsonr(x, y)
            print(f"  {name:<30} r = {r:+.3f}, p = {p:.4f} (n={len(x)})")

    print("\n=== Key comparison: all-electron vs valence-only ===")
    r_all, _ = stats.pearsonr(delta_all, ratios)
    r_val, _ = stats.pearsonr(delta_val, ratios)
    print(f"  δ_all vs boundary_ratio:    r = {r_all:+.3f}")
    print(f"  δ_val vs boundary_ratio:    r = {r_val:+.3f}")
    if abs(r_val) > abs(r_all):
        print(f"  → Valence-only IMPROVES correlation by {abs(r_val)-abs(r_all):.3f}")
    else:
        print(f"  → Valence-only does not improve (Δr = {abs(r_val)-abs(r_all):+.3f})")

    # Save results
    outpath = os.path.join(os.path.dirname(__file__), "test7_extended_results.json")
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {outpath}")

    # === Plot ===
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.set_facecolor('#0a0e17')
        for ax in axes:
            ax.set_facecolor('#0a0e17')
            ax.tick_params(colors='#94a3b8')
            for s in ['bottom', 'left']:
                ax.spines[s].set_color('#2a3550')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        colors = {'sp': '#38bdf8', 'd': '#818cf8'}

        for i, (xdata, xlabel, title) in enumerate([
            (delta_all, 'δ_IPR (all electron)', 'All-electron δ vs boundary ratio'),
            (delta_val, 'δ_IPR (valence only)', 'Valence-only δ vs boundary ratio'),
            (delta_val, 'δ_IPR (valence only)', 'Valence-only δ vs Miedema n_ws'),
        ]):
            ax = axes[i]
            ydata = ratios if i < 2 else nws

            for e in elems_ok:
                r = results[e]
                x = r['delta_all'] if i == 0 else r['delta_valence']
                y = r['boundary_ratio'] if i < 2 else MIEDEMA_NWS13[e]
                c = colors[ELEMENTS[e]['type']]
                ax.scatter(x, y, c=c, s=60, zorder=3, edgecolors='w', linewidths=0.5)
                ax.annotate(e, (x, y), xytext=(4, 4), textcoords='offset points',
                            fontsize=7, color='#cbd5e1')

            rv, pv = stats.pearsonr(xdata, ydata)
            ax.set_xlabel(xlabel, color='#e2e8f0')
            ax.set_ylabel('Boundary ratio' if i < 2 else 'n_ws', color='#e2e8f0')
            ax.set_title(f'{title}\nr={rv:.2f}, p={pv:.3f}', color='#94a3b8', fontsize=10)

        fig.tight_layout()
        figpath = os.path.join(FIGDIR, 'test7_extended.png')
        fig.savefig(figpath, dpi=150, bbox_inches='tight')
        print(f"Plot saved: {figpath}")
    except ImportError:
        print("matplotlib not available")


if __name__ == '__main__':
    main()
