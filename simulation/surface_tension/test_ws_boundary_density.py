"""
Phase 3: Direct comparison of DFT-computed boundary density with Miedema n_ws.

We extract the absolute valence electron density at the interlayer
midpoint from slab calculations and compare with Miedema's tabulated
n_ws values.

Key question: Does the DFT midpoint density correlate with Miedema n_ws?
If yes → n_ws IS boundary density, and δ predicts it (indirectly via sp/d).
If no → n_ws is something else entirely (fitting artifact).
"""

import numpy as np
import os
from scipy import stats

bohr2ang = 0.529177
QE_DIR = os.path.join(os.path.dirname(__file__), 'qe_slab')

# Miedema n_ws (d.u.) from de Boer 1988
NWS = {
    'Li': 2.85, 'Na': 1.65, 'K': 0.95, 'Be': 7.55, 'Mg': 3.55,
    'Ca': 2.55, 'Al': 5.55, 'Si': 6.75, 'Ga': 5.15, 'Cu': 5.55,
    'Zn': 4.05, 'Fe': 5.55, 'Ti': 4.25, 'Ag': 4.35,
}

# Metal slab parameters (same as analyze_15metals.py)
metals = {
    'Na': {'val': 'na_val_avg.dat', 'd': 2.988, 'n_layers': 7, 'type': 'sp'},
    'K':  {'val': 'k_val_avg.dat',  'd': 3.694, 'n_layers': 7, 'type': 'sp'},
    'Al': {'val': 'al_val_avg.dat', 'd': 2.338, 'n_layers': 7, 'type': 'sp'},
    'Cu': {'val': 'cu_val_avg.dat', 'd': 2.087, 'n_layers': 7, 'type': 'd'},
    'Zn': {'val': 'zn_val_avg.dat', 'd': 2.474, 'n_layers': 7, 'type': 'd'},
    'Li': {'val': 'li_val_avg.dat', 'd': 3.49*np.sqrt(2)/2, 'n_layers': 7, 'type': 'sp'},
    'Be': {'val': 'be_val_avg.dat', 'd': 3.58/2, 'n_layers': 7, 'type': 'sp'},
    'Mg': {'val': 'mg_val_avg.dat', 'd': 5.21/2, 'n_layers': 7, 'type': 'sp'},
    'Ca': {'val': 'ca_val_avg.dat', 'd': 5.58/np.sqrt(3), 'n_layers': 7, 'type': 'sp'},
    'Si': {'val': 'si_val_avg.dat', 'd': 5.43/np.sqrt(3), 'n_layers': 8, 'type': 'sp'},
    'Ga': {'val': 'ga_val_avg.dat', 'd': 4.51/np.sqrt(3), 'n_layers': 7, 'type': 'd'},
    'Ti': {'val': 'ti_val_avg.dat', 'd': 4.69/2, 'n_layers': 7, 'type': 'd'},
    'Ag': {'val': 'ag_val_avg.dat', 'd': 4.09/np.sqrt(3), 'n_layers': 7, 'type': 'd'},
    'Fe': {'val': 'fe_val_avg.dat', 'd': 2.87*np.sqrt(2)/2, 'n_layers': 7, 'type': 'd'},
}


def extract_midpoint_density(datafile, d, n_layers):
    """
    Extract ABSOLUTE valence electron density at interlayer midpoints.
    Returns n_mid (absolute, in e/bohr³) and n_bulk (for normalization).
    """
    filepath = os.path.join(QE_DIR, datafile)
    data = np.loadtxt(filepath)
    z = data[:, 0] * bohr2ang  # bohr -> angstrom
    rho = data[:, 1]  # electron density in e/bohr³

    layers = np.array([i * d for i in range(n_layers)])

    # Bulk density: central 3 layers average
    c_start = layers[2] - d/2
    c_end = layers[4] + d/2
    mask = (z > c_start) & (z < c_end)
    if mask.sum() == 0:
        mask = (z > layers[1]) & (z < layers[5])
    n_bulk = np.mean(rho[mask]) if mask.sum() > 0 else 1.0

    # Absolute midpoint densities (interior only)
    midpoints = []
    for i in range(1, n_layers - 2):
        z_mid = (layers[i] + layers[i+1]) / 2
        idx = np.argmin(np.abs(z - z_mid))
        midpoints.append(rho[idx])

    n_mid_abs = np.mean(midpoints) if midpoints else 0.0
    ratio = n_mid_abs / n_bulk if n_bulk > 0 else 0.0

    return n_mid_abs, n_bulk, ratio


def main():
    print("=" * 70)
    print("Phase 3: DFT boundary density vs Miedema n_ws")
    print("=" * 70)

    print(f"\n{'Elem':>4} {'Type':>4} {'n_mid(abs)':>12} {'n_bulk':>12} "
          f"{'ratio':>8} {'n_ws':>6} {'n_ws^1/3':>8}")
    print("-" * 60)

    results = {}
    for name in ['Li','Be','Na','Mg','Al','Si','K','Ca','Ti','Fe','Cu','Zn','Ga','Ag']:
        p = metals[name]
        try:
            n_mid, n_bulk, ratio = extract_midpoint_density(p['val'], p['d'], p['n_layers'])
            nws = NWS[name]
            nws13 = nws**(1/3)
            results[name] = {
                'n_mid': n_mid, 'n_bulk': n_bulk, 'ratio': ratio,
                'nws': nws, 'nws13': nws13, 'type': p['type']
            }
            print(f"{name:>4} {p['type']:>4} {n_mid:>12.6f} {n_bulk:>12.6f} "
                  f"{ratio:>8.3f} {nws:>6.2f} {nws13:>8.2f}")
        except Exception as e:
            print(f"{name:>4} ERROR: {e}")

    # === Correlations ===
    elems = list(results.keys())
    n_mid_arr = np.array([results[e]['n_mid'] for e in elems])
    n_bulk_arr = np.array([results[e]['n_bulk'] for e in elems])
    ratio_arr = np.array([results[e]['ratio'] for e in elems])
    nws_arr = np.array([results[e]['nws'] for e in elems])
    nws13_arr = np.array([results[e]['nws13'] for e in elems])

    print("\n" + "=" * 70)
    print("CORRELATIONS")
    print("=" * 70)

    tests = [
        ('n_mid(abs) vs n_ws', n_mid_arr, nws_arr),
        ('n_mid(abs) vs n_ws^{1/3}', n_mid_arr, nws13_arr),
        ('n_bulk vs n_ws', n_bulk_arr, nws_arr),
        ('n_bulk vs n_ws^{1/3}', n_bulk_arr, nws13_arr),
        ('ratio vs n_ws^{1/3}', ratio_arr, nws13_arr),
    ]

    for name, x, y in tests:
        r, p = stats.pearsonr(x, y)
        print(f"  {name:<30} r = {r:+.3f}, p = {p:.4f}")

    # === Key test: does DFT boundary density match Miedema? ===
    print("\n" + "=" * 70)
    print("KEY TEST: Does DFT midpoint density match Miedema n_ws?")
    print("=" * 70)

    r_mid_nws, p_mid_nws = stats.pearsonr(n_mid_arr, nws_arr)
    r_bulk_nws, p_bulk_nws = stats.pearsonr(n_bulk_arr, nws_arr)

    print(f"\n  n_mid(abs) vs n_ws: r = {r_mid_nws:.3f}, p = {p_mid_nws:.4f}")
    print(f"  n_bulk vs n_ws:     r = {r_bulk_nws:.3f}, p = {p_bulk_nws:.4f}")

    if abs(r_mid_nws) > 0.7:
        print("\n  → n_mid CORRELATES with n_ws: Miedema's n_ws IS boundary density.")
        print("    δ → n_mid → n_ws chain is supported.")
    elif abs(r_bulk_nws) > 0.7:
        print("\n  → n_bulk (not n_mid) correlates with n_ws.")
        print("    Miedema's n_ws may be bulk-averaged, not boundary-specific.")
    else:
        print("\n  → Neither n_mid nor n_bulk correlates strongly with n_ws.")
        print("    Miedema's n_ws may NOT be a simple electron density.")
        print("    It may encode additional information (atomic volume, d-band width, etc.)")

    # === sp/d separated ===
    print("\n--- sp/d separated ---")
    sp_mask = np.array([results[e]['type'] == 'sp' for e in elems])
    d_mask = ~sp_mask

    if sp_mask.sum() >= 3:
        r_sp, p_sp = stats.pearsonr(n_mid_arr[sp_mask], nws_arr[sp_mask])
        print(f"  sp metals: n_mid vs n_ws: r = {r_sp:.3f} (n={sp_mask.sum()})")
    if d_mask.sum() >= 3:
        r_d, p_d = stats.pearsonr(n_mid_arr[d_mask], nws_arr[d_mask])
        print(f"  d metals:  n_mid vs n_ws: r = {r_d:.3f} (n={d_mask.sum()})")


if __name__ == '__main__':
    main()
