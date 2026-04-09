"""
Phase 2: Orbital-decomposed δ (δ_s, δ_p, δ_d)

Question: Does separating δ into orbital components improve
the correlation with Miedema's n_ws?

Method: For each occupied KS orbital in the dimer, determine
its dominant angular momentum character (s, p, or d) from the
AO basis composition. Compute IPR separately for each class.
"""

import numpy as np
import os
import json

try:
    from pyscf import gto, dft
    HAS_PYSCF = True
except ImportError:
    HAS_PYSCF = False
    print("PySCF not available.")

# Element data (same as test7_extended.py)
ELEMENTS = {
    'Li':  {'bond': 2.673, 'n_core': 2,  'spin': 0},
    'Na':  {'bond': 3.079, 'n_core': 10, 'spin': 0},
    'K':   {'bond': 3.924, 'n_core': 18, 'spin': 0},
    'Be':  {'bond': 2.460, 'n_core': 2,  'spin': 0},
    'Mg':  {'bond': 3.891, 'n_core': 10, 'spin': 0},
    'Ca':  {'bond': 4.277, 'n_core': 18, 'spin': 0},
    'Al':  {'bond': 2.701, 'n_core': 10, 'spin': 2},
    'Si':  {'bond': 2.246, 'n_core': 10, 'spin': 2},
    'Ga':  {'bond': 2.750, 'n_core': 28, 'spin': 2},
    'Cu':  {'bond': 2.220, 'n_core': 18, 'spin': 0},
    'Zn':  {'bond': 4.190, 'n_core': 28, 'spin': 0},
    'Fe':  {'bond': 2.020, 'n_core': 18, 'spin': 6},
    'Ni':  {'bond': 2.155, 'n_core': 18, 'spin': 2},
    'Ag':  {'bond': 2.530, 'n_core': 36, 'spin': 0},
    'Ti':  {'bond': 1.942, 'n_core': 18, 'spin': 4},
}

NWS = {
    'Li': 2.85, 'Na': 1.65, 'K': 0.95, 'Be': 7.55, 'Mg': 3.55,
    'Ca': 2.55, 'Al': 5.55, 'Si': 6.75, 'Ga': 5.15, 'Cu': 5.55,
    'Zn': 4.05, 'Fe': 5.55, 'Ni': 5.55, 'Ag': 4.35, 'Ti': 4.25,
}


def get_ao_angular_momentum(mol):
    """Get angular momentum (l) for each AO basis function."""
    ao_labels = mol.ao_labels()
    l_values = []
    for label in ao_labels:
        # label format: '0 Li 1s' or '0 Li 2px' etc.
        parts = label.split()
        orbital_str = parts[-1]  # e.g., '1s', '2px', '3dxy'
        if 's' in orbital_str and 'p' not in orbital_str and 'd' not in orbital_str:
            l_values.append(0)  # s orbital
        elif 'p' in orbital_str and 'd' not in orbital_str:
            l_values.append(1)  # p orbital
        elif 'd' in orbital_str and 'f' not in orbital_str:
            l_values.append(2)  # d orbital
        elif 'f' in orbital_str:
            l_values.append(3)  # f orbital
        else:
            l_values.append(-1)  # unknown
    return np.array(l_values)


def compute_orbital_decomposed_delta(element, info, basis="def2-svp", xc="b3lyp"):
    """
    Compute δ decomposed by orbital angular momentum.
    For each occupied MO, determine dominant character (s/p/d) and
    accumulate IPR into corresponding bin.
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
        return None

    mo_coeff_raw = mf.mo_coeff
    mo_occ_raw = mf.mo_occ
    mo_energy_raw = mf.mo_energy

    is_unrestricted = (isinstance(mo_coeff_raw, (list, tuple))
                       or (isinstance(mo_coeff_raw, np.ndarray)
                           and mo_coeff_raw.ndim == 3))

    S = mol.intor("int1e_ovlp")
    n_ao = S.shape[0]
    l_ao = get_ao_angular_momentum(mol)

    # Collect orbital data
    all_data = []  # (energy, ipr, dominant_l, is_valence)

    n_core_total = 2 * n_core_per_atom

    def process_spin(mc, mo, me, n_skip):
        data = []
        n_occ = int(np.sum(mo > 0))
        for n in range(n_occ):
            c_n = mc[:, n]
            p_mu = np.abs(c_n * (S @ c_n))
            p_sum = p_mu.sum()
            if p_sum > 1e-10:
                ipr = np.sum(p_mu**2) / p_sum**2
            else:
                ipr = 1.0

            # Determine dominant angular momentum
            # Weight of each AO: |c_n * (S @ c_n)|
            weights = np.abs(c_n * (S @ c_n))
            w_s = np.sum(weights[l_ao == 0])
            w_p = np.sum(weights[l_ao == 1])
            w_d = np.sum(weights[l_ao == 2])
            w_total = w_s + w_p + w_d
            if w_total > 0:
                frac_s = w_s / w_total
                frac_p = w_p / w_total
                frac_d = w_d / w_total
            else:
                frac_s = frac_p = frac_d = 0

            # Dominant character
            dominant = max((frac_s, 's'), (frac_p, 'p'), (frac_d, 'd'))[1]

            is_valence = (n >= n_skip)
            data.append({
                'energy': me[n],
                'ipr': ipr,
                'dominant_l': dominant,
                'frac_s': frac_s,
                'frac_p': frac_p,
                'frac_d': frac_d,
                'is_valence': is_valence,
            })
        return data

    if is_unrestricted:
        n_skip = n_core_per_atom  # per spin channel
        for s in range(2):
            all_data.extend(process_spin(
                mo_coeff_raw[s], mo_occ_raw[s], mo_energy_raw[s], n_skip))
    else:
        n_skip = n_core_total // 2
        all_data.extend(process_spin(
            mo_coeff_raw, mo_occ_raw, mo_energy_raw, n_skip))

    # Compute δ by orbital type (valence only)
    valence = [d for d in all_data if d['is_valence']]

    iprs_s = [d['ipr'] for d in valence if d['dominant_l'] == 's']
    iprs_p = [d['ipr'] for d in valence if d['dominant_l'] == 'p']
    iprs_d = [d['ipr'] for d in valence if d['dominant_l'] == 'd']
    iprs_all = [d['ipr'] for d in valence]

    def compute_delta(iprs):
        if not iprs:
            return 0.0
        mean_ipr = np.mean(iprs)
        return 1.0 / (n_ao * mean_ipr) if mean_ipr > 0 else 0.0

    delta_s = compute_delta(iprs_s)
    delta_p = compute_delta(iprs_p)
    delta_d = compute_delta(iprs_d)
    delta_sp = compute_delta(iprs_s + iprs_p)
    delta_all = compute_delta(iprs_all)

    # Fraction of valence orbitals by type
    n_val = len(valence)
    n_s = len(iprs_s)
    n_p = len(iprs_p)
    n_d = len(iprs_d)

    return {
        'element': element,
        'delta_s': float(delta_s),
        'delta_p': float(delta_p),
        'delta_d': float(delta_d),
        'delta_sp': float(delta_sp),
        'delta_val': float(delta_all),
        'n_val': n_val,
        'n_s': n_s, 'n_p': n_p, 'n_d': n_d,
        'frac_d': n_d / n_val if n_val > 0 else 0,
    }


def main():
    if not HAS_PYSCF:
        return

    from scipy import stats

    print("=" * 65)
    print("Phase 2: Orbital-decomposed δ (δ_s, δ_p, δ_d)")
    print("=" * 65)

    results = {}
    for elem in sorted(ELEMENTS.keys()):
        info = ELEMENTS[elem]
        print(f"Computing {elem}2...", end=' ', flush=True)
        try:
            r = compute_orbital_decomposed_delta(elem, info)
            if r:
                results[elem] = r
                print(f"δ_s={r['delta_s']:.4f} δ_p={r['delta_p']:.4f} "
                      f"δ_d={r['delta_d']:.4f} δ_sp={r['delta_sp']:.4f} "
                      f"(n_s={r['n_s']} n_p={r['n_p']} n_d={r['n_d']})")
            else:
                print("FAILED")
        except Exception as e:
            print(f"ERROR: {e}")

    # Correlations
    print("\n" + "=" * 65)
    print("CORRELATIONS with n_ws^{1/3}")
    print("=" * 65)

    elems_ok = [e for e in results if e in NWS]
    nws13 = np.array([NWS[e]**(1/3) for e in elems_ok])

    for name, key in [
        ('δ_val (all valence)', 'delta_val'),
        ('δ_s (s-character only)', 'delta_s'),
        ('δ_p (p-character only)', 'delta_p'),
        ('δ_d (d-character only)', 'delta_d'),
        ('δ_sp (s+p only)', 'delta_sp'),
    ]:
        vals = np.array([results[e][key] for e in elems_ok])
        # Remove zeros for correlation
        mask = vals > 0
        if mask.sum() >= 3:
            r, p = stats.pearsonr(vals[mask], nws13[mask])
            print(f"  {name:<30} r = {r:+.3f}, p = {p:.4f} (n={mask.sum()})")
        else:
            print(f"  {name:<30} insufficient data (n={mask.sum()})")

    # 2-variable: δ_sp + frac_d
    print("\n--- 2-variable: n_ws^{1/3} ~ δ_sp + frac_d ---")
    dsp = np.array([results[e]['delta_sp'] for e in elems_ok])
    fd = np.array([results[e]['frac_d'] for e in elems_ok])
    n = len(elems_ok)

    X = np.column_stack([dsp, fd, np.ones(n)])
    beta, _, _, _ = np.linalg.lstsq(X, nws13, rcond=None)
    pred = X @ beta
    ss_res = np.sum((nws13 - pred)**2)
    ss_tot = np.sum((nws13 - np.mean(nws13))**2)
    r2 = 1 - ss_res / ss_tot
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - 3)
    print(f"  R² = {r2:.3f}, R²_adj = {r2_adj:.3f}")

    # Save
    outpath = os.path.join(os.path.dirname(__file__) or '.',
                           'test_orbital_decomposed_results.json')
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {outpath}")


if __name__ == '__main__':
    main()
