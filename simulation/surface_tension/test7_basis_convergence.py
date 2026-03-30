#!/usr/bin/env python3
"""
Test 7 supplement: Basis set sensitivity analysis for δ_IPR.

Reviewer request: verify that δ_IPR is robust across basis sets.
Runs 11 homonuclear dimers with def2-SVP, def2-TZVP, and def2-QZVP.
Also computes δ_IPR vs Miedema n_ws correlation for Issue 8.

Author: K. Miyauchi
"""

import numpy as np
import sys
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGDIR, exist_ok=True)

from test7_delta_causes_nws import compute_cluster_delta_and_boundary

# 11 dimer systems (same as main test7)
DIMERS = [
    ("Li", 2, 2.67, {}),
    ("Na", 2, 3.08, {}),
    ("Be", 2, 2.45, {}),
    ("Mg", 2, 3.89, {}),
    ("Al", 2, 2.70, {"spin": 2, "max_cycle": 300, "conv_tol": 1e-8}),
    ("K",  2, 3.92, {}),
    ("Ca", 2, 4.28, {}),
    ("Cu", 2, 2.22, {"spin": 0, "max_cycle": 200, "conv_tol": 1e-8}),
    ("Zn", 2, 4.19, {"max_cycle": 200, "conv_tol": 1e-8}),
    ("Si", 2, 2.25, {"spin": 2, "max_cycle": 300, "conv_tol": 1e-8}),
    ("Ga", 2, 2.75, {"spin": 2, "max_cycle": 300, "conv_tol": 1e-8}),
]

BASIS_SETS = ["def2-svp", "def2-tzvp", "def2-qzvp"]

# Miedema n_ws^(1/3) values from de Boer et al. 1988
# (same data used in test5_nws_miedema.py)
MIEDEMA_NWS_CUBERT = {
    "Li": 1.30, "Na": 1.10, "K": 0.95, "Be": 1.67,
    "Mg": 1.33, "Al": 1.39, "Ca": 1.07, "Cu": 1.47,
    "Zn": 1.32, "Ga": 1.31, "Si": 1.50,
    # "In": 1.17, "Sn": 1.24, "Cs": 0.83  # not in dimer set
}

# Experimental surface tension (mN/m)
GAMMA_EXP = {
    "Li": 400, "Na": 191, "K": 110, "Be": 1100,
    "Mg": 559, "Al": 1140, "Ca": 361, "Cu": 1330,
    "Zn": 782, "Ga": 718, "Si": 865,
}


def main():
    print("=" * 70)
    print("BASIS SET CONVERGENCE TEST FOR δ_IPR")
    print("=" * 70)

    all_results = {}  # basis -> list of results

    for basis in BASIS_SETS:
        print(f"\n{'─' * 50}")
        print(f"  Basis: {basis}")
        print(f"{'─' * 50}")
        results = []
        for item in DIMERS:
            elem, n, bl = item[0], item[1], item[2]
            kwargs = item[3].copy() if len(item) > 3 else {}
            label = f"{elem}₂"
            try:
                res = compute_cluster_delta_and_boundary(
                    elem, n, bl, basis=basis, **kwargs
                )
                results.append(res)
                print(f"    {label:6s}  δ={res['delta_ipr']:.4f}  "
                      f"ratio={res['boundary_ratio']:.4f}  "
                      f"N_AO={res['n_ao']}")
            except Exception as e:
                print(f"    {label:6s}  FAILED: {e}")
                results.append(None)
        all_results[basis] = results

    # ── Summary table ──
    print("\n" + "=" * 70)
    print("CONVERGENCE SUMMARY")
    print("=" * 70)
    print(f"{'Element':>8s}", end="")
    for basis in BASIS_SETS:
        print(f"  {basis:>12s}", end="")
    print(f"  {'n_ws^1/3':>8s}  {'γ(mN/m)':>8s}")
    print("-" * 70)

    for i, item in enumerate(DIMERS):
        elem = item[0]
        print(f"{elem+'₂':>8s}", end="")
        for basis in BASIS_SETS:
            r = all_results[basis][i]
            if r is not None:
                print(f"  {r['delta_ipr']:12.4f}", end="")
            else:
                print(f"  {'FAIL':>12s}", end="")
        nws = MIEDEMA_NWS_CUBERT.get(elem, float('nan'))
        gamma = GAMMA_EXP.get(elem, float('nan'))
        print(f"  {nws:8.2f}  {gamma:8.0f}")

    # ── Cross-element correlations for each basis ──
    from scipy import stats

    print("\n" + "=" * 70)
    print("CROSS-ELEMENT CORRELATIONS (dimers only)")
    print("=" * 70)
    print(f"{'Basis':>12s}  {'r(δ,ratio)':>10s}  {'p':>8s}  "
          f"{'r(δ,n_ws)':>10s}  {'p':>8s}  "
          f"{'r(δ,γ)':>10s}  {'p':>8s}  {'N':>3s}")

    for basis in BASIS_SETS:
        results = all_results[basis]
        valid = [(i, r) for i, r in enumerate(results) if r is not None]
        if len(valid) < 3:
            print(f"{basis:>12s}  insufficient data")
            continue

        deltas = np.array([r['delta_ipr'] for _, r in valid])
        ratios = np.array([r['boundary_ratio'] for _, r in valid])
        elems = [DIMERS[i][0] for i, _ in valid]

        # δ vs boundary ratio
        r_ratio, p_ratio = stats.pearsonr(deltas, ratios)

        # δ vs Miedema n_ws
        nws_vals = np.array([MIEDEMA_NWS_CUBERT[e]**3 for e in elems])
        r_nws, p_nws = stats.pearsonr(deltas, nws_vals)

        # δ vs γ
        gamma_vals = np.array([GAMMA_EXP[e] for e in elems])
        r_gamma, p_gamma = stats.pearsonr(deltas, gamma_vals)

        print(f"{basis:>12s}  {r_ratio:10.3f}  {p_ratio:8.4f}  "
              f"{r_nws:10.3f}  {p_nws:8.4f}  "
              f"{r_gamma:10.3f}  {p_gamma:8.4f}  {len(valid):3d}")

    # ── Spearman rank correlations ──
    print(f"\n{'Basis':>12s}  {'ρ(δ,ratio)':>10s}  {'ρ(δ,n_ws)':>10s}  {'ρ(δ,γ)':>10s}")
    for basis in BASIS_SETS:
        results = all_results[basis]
        valid = [(i, r) for i, r in enumerate(results) if r is not None]
        if len(valid) < 3:
            continue
        deltas = np.array([r['delta_ipr'] for _, r in valid])
        ratios = np.array([r['boundary_ratio'] for _, r in valid])
        elems = [DIMERS[i][0] for i, _ in valid]
        nws_vals = np.array([MIEDEMA_NWS_CUBERT[e]**3 for e in elems])
        gamma_vals = np.array([GAMMA_EXP[e] for e in elems])

        rho_ratio, _ = stats.spearmanr(deltas, ratios)
        rho_nws, _ = stats.spearmanr(deltas, nws_vals)
        rho_gamma, _ = stats.spearmanr(deltas, gamma_vals)

        print(f"{basis:>12s}  {rho_ratio:10.3f}  {rho_nws:10.3f}  {rho_gamma:10.3f}")

    # ── δ_IPR vs n_ws detailed table (Issue 8) ──
    print("\n" + "=" * 70)
    print("δ_IPR vs MIEDEMA n_ws (Issue 8 — 11 elements)")
    print("Using def2-SVP (primary) and def2-TZVP (verification)")
    print("=" * 70)
    print(f"{'Element':>8s}  {'δ(SVP)':>8s}  {'δ(TZVP)':>8s}  "
          f"{'n_ws':>8s}  {'n_ws^1/3':>8s}  {'γ':>8s}")

    for i, item in enumerate(DIMERS):
        elem = item[0]
        d_svp = all_results["def2-svp"][i]
        d_tzvp = all_results["def2-tzvp"][i]
        nws_cb = MIEDEMA_NWS_CUBERT.get(elem, float('nan'))
        gamma = GAMMA_EXP.get(elem, float('nan'))
        ds = d_svp['delta_ipr'] if d_svp else float('nan')
        dt = d_tzvp['delta_ipr'] if d_tzvp else float('nan')
        print(f"{elem:>8s}  {ds:8.4f}  {dt:8.4f}  "
              f"{nws_cb**3:8.3f}  {nws_cb:8.2f}  {gamma:8.0f}")

    # ── Save results for paper ──
    output_file = os.path.join(FIGDIR, "basis_convergence_results.txt")
    with open(output_file, "w") as f:
        f.write("Basis set convergence for δ_IPR (11 homonuclear dimers)\n")
        f.write("=" * 60 + "\n\n")
        for basis in BASIS_SETS:
            results = all_results[basis]
            valid = [(i, r) for i, r in enumerate(results) if r is not None]
            deltas = np.array([r['delta_ipr'] for _, r in valid])
            ratios = np.array([r['boundary_ratio'] for _, r in valid])
            r_val, p_val = stats.pearsonr(deltas, ratios)
            f.write(f"{basis}: r(δ,boundary_ratio) = {r_val:.3f} (p={p_val:.4f}), "
                    f"N={len(valid)}\n")
            for idx, r in valid:
                elem = DIMERS[idx][0]
                f.write(f"  {elem:4s}: δ={r['delta_ipr']:.4f}, "
                        f"ratio={r['boundary_ratio']:.4f}, "
                        f"N_AO={r['n_ao']}\n")
            f.write("\n")
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()
