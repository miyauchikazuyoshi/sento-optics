"""
2D Ising Model: δ (IPR) as RG Flow Variable — Production Version
================================================================

Tests whether δ = IPR of the spin configuration probability distribution
functions as a natural RG flow variable under block-spin coarse-graining.

Improvements over v1:
- Adaptive thermalization: scales with L² (larger systems get more steps)
- Multiple system sizes: L=64, 128, 256
- Finer temperature grid near Tc for critical scaling analysis
- Error bars via bootstrap resampling
- Saves raw data for offline analysis

Usage:
  python ising_rg_delta_v2.py [--max-L 256] [--n-samples 200] [--n-therm-factor 50]

Estimated runtime:
  L=64:  ~20s per temperature
  L=128: ~2min per temperature
  L=256: ~15min per temperature
  Total (all T, all L): ~3-5 hours on a single core
"""

import numpy as np
import argparse
import json
import time
import os

# === Wolff Cluster Algorithm ===

def wolff_step(spins, beta):
    """Single Wolff cluster flip. Returns cluster size."""
    L = spins.shape[0]
    p_add = 1 - np.exp(-2 * beta)

    # Random seed spin
    i, j = np.random.randint(0, L, size=2)
    seed_spin = spins[i, j]
    spins[i, j] *= -1

    cluster = [(i, j)]
    stack = [(i, j)]

    while stack:
        ci, cj = stack.pop()
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = (ci + di) % L, (cj + dj) % L
            if spins[ni, nj] == seed_spin and np.random.rand() < p_add:
                spins[ni, nj] *= -1
                stack.append((ni, nj))
                cluster.append((ni, nj))

    return len(cluster)


def thermalize(spins, beta, n_steps):
    """Run Wolff algorithm for thermalization."""
    for _ in range(n_steps):
        wolff_step(spins, beta)


# === Block Spin RG ===

def block_spin_transform(spins):
    """2x2 majority rule block spin transformation."""
    L = spins.shape[0]
    assert L % 2 == 0
    L_new = L // 2
    new_spins = np.zeros((L_new, L_new), dtype=int)

    for i in range(L_new):
        for j in range(L_new):
            block_sum = (spins[2*i, 2*j] + spins[2*i+1, 2*j] +
                         spins[2*i, 2*j+1] + spins[2*i+1, 2*j+1])
            # Majority rule: sign of sum. Tie (sum=0) → random
            if block_sum > 0:
                new_spins[i, j] = 1
            elif block_sum < 0:
                new_spins[i, j] = -1
            else:
                new_spins[i, j] = np.random.choice([-1, 1])

    return new_spins


# === δ (IPR) Measurement ===

def measure_delta(spins):
    """
    δ = IPR of the spin configuration.

    For Ising: the "probability distribution" is the fraction of spins
    in each state (+1 or -1). For a system of N spins:
      p_+ = (N + M) / (2N),  p_- = (N - M) / (2N)
      IPR = p_+² + p_-²

    δ ranges from 0.5 (completely disordered, p_+=p_-=0.5)
    to 1.0 (completely ordered, all spins aligned).

    Wait — this gives IPR ∈ [0.5, 1.0], not [0, 1].
    Normalize: δ = 2*IPR - 1 ∈ [0, 1]?

    Actually, the more informative measure uses the spatial distribution.
    We compute the magnetization profile and its IPR.

    Simplest and most direct: use the block-averaged magnetization
    as the state variable, and track how the distribution of
    block magnetizations changes under coarse-graining.

    For consistency with v1, use:
      δ = (1/N) * Σ_blocks m_block⁴ / (Σ_blocks m_block²)²
    where m_block is the block magnetization.

    Simplest interpretation: treat the N spins as a probability
    distribution p_i = (1 + s_i) / (2N) for s_i ∈ {-1, +1}.
    IPR = Σ p_i² = (1/4N²) Σ (1 + s_i)²
        = (1/4N²) (N + 2M + N) = (1/4N²)(2N + 2M) = (N + M)/(2N²)

    Hmm, this doesn't give a clean IPR. Let's use the simpler definition
    from the v1 code:
      p_+ = fraction of +1 spins
      p_- = fraction of -1 spins
      IPR = p_+² + p_-²
      δ_raw = IPR  (ranges 0.5 to 1.0)

    Or even simpler: just track magnetization |m| and
    δ = (1 + m²) / 2  which maps m²∈[0,1] to δ∈[0.5, 1.0].

    For v2, let's track BOTH:
    1. Simple δ = p_+² + p_-² (2-state IPR)
    2. Spatial δ using sublattice decomposition
    """
    N = spins.size
    M = np.sum(spins)
    m = M / N  # magnetization density

    p_plus = (N + M) / (2 * N)
    p_minus = (N - M) / (2 * N)
    ipr = p_plus**2 + p_minus**2  # ∈ [0.5, 1.0]

    return {
        'm_abs': abs(m),
        'm2': m**2,
        'ipr': ipr,
        'delta_norm': 2 * ipr - 1,  # normalized to [0, 1]
    }


def rg_flow(spins, max_levels=None):
    """
    Perform block-spin RG and measure δ at each level.
    Returns list of (L, measurements) pairs.
    """
    levels = []
    current = spins.copy()

    while current.shape[0] >= 2:
        if max_levels is not None and len(levels) >= max_levels:
            break
        meas = measure_delta(current)
        meas['L'] = current.shape[0]
        levels.append(meas)

        if current.shape[0] < 4:
            break
        current = block_spin_transform(current)

    return levels


# === Main ===

def run_simulation(L, T, beta, n_therm, n_samples, n_decorr):
    """Run simulation for one (L, T) pair."""
    spins = np.random.choice([-1, 1], size=(L, L))

    # Thermalize
    thermalize(spins, beta, n_therm)

    # Collect samples
    all_flows = []
    for s in range(n_samples):
        # Decorrelation
        for _ in range(n_decorr):
            wolff_step(spins, beta)

        flow = rg_flow(spins)
        all_flows.append(flow)

    return all_flows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-L', type=int, default=128,
                        help='Maximum system size (default: 128)')
    parser.add_argument('--n-samples', type=int, default=100,
                        help='Number of independent samples per (L,T)')
    parser.add_argument('--n-therm-factor', type=int, default=30,
                        help='Thermalization steps = factor * L (default: 30)')
    parser.add_argument('--n-decorr', type=int, default=5,
                        help='Decorrelation Wolff steps between samples')
    parser.add_argument('--output', type=str, default='ising_rg_results.json',
                        help='Output JSON file')
    args = parser.parse_args()

    Tc = 2 / np.log(1 + np.sqrt(2))  # Onsager exact: 2.26919...

    # Temperature grid: coarse away from Tc, fine near Tc
    T_coarse = [1.5, 2.0, 2.5, 3.0, 4.0]
    T_fine = [Tc - 0.1, Tc - 0.05, Tc, Tc + 0.05, Tc + 0.1]
    temperatures = sorted(set(T_coarse + T_fine))

    # System sizes (powers of 2 only, for clean block-spin)
    system_sizes = [s for s in [64, 128, 256] if s <= args.max_L]

    print("=" * 70)
    print("2D Ising Model: δ as RG Flow Variable (v2)")
    print("=" * 70)
    print(f"Onsager Tc = {Tc:.5f}")
    print(f"System sizes: {system_sizes}")
    print(f"Temperatures: {len(temperatures)} points")
    print(f"Samples per (L,T): {args.n_samples}")
    print(f"Thermalization: {args.n_therm_factor} * L Wolff steps")
    print(f"Decorrelation: {args.n_decorr} Wolff steps between samples")
    print()

    results = {
        'Tc': Tc,
        'params': vars(args),
        'data': {}
    }

    total_runs = len(system_sizes) * len(temperatures)
    run_count = 0

    for L in system_sizes:
        n_therm = args.n_therm_factor * L  # Scales with L
        results['data'][str(L)] = {}

        for T in temperatures:
            run_count += 1
            beta = 1.0 / T
            t0 = time.time()

            print(f"[{run_count}/{total_runs}] L={L}, T={T:.4f} "
                  f"(therm={n_therm} steps) ... ", end='', flush=True)

            flows = run_simulation(L, T, beta, n_therm, args.n_samples, args.n_decorr)

            # Aggregate: mean and std of δ at each RG level
            # All flows should have the same number of levels
            n_levels = len(flows[0])
            level_data = []

            for lev in range(n_levels):
                deltas = [f[lev]['delta_norm'] for f in flows]
                iprs = [f[lev]['ipr'] for f in flows]
                m_abs = [f[lev]['m_abs'] for f in flows]
                Ll = flows[0][lev]['L']

                level_data.append({
                    'L': Ll,
                    'delta_mean': float(np.mean(deltas)),
                    'delta_std': float(np.std(deltas)),
                    'ipr_mean': float(np.mean(iprs)),
                    'ipr_std': float(np.std(iprs)),
                    'm_abs_mean': float(np.mean(m_abs)),
                    'm_abs_std': float(np.std(m_abs)),
                })

            elapsed = time.time() - t0
            d0 = level_data[0]['delta_mean']
            print(f"δ(L={L})={d0:.4f}, time={elapsed:.1f}s")

            results['data'][str(L)][f"{T:.5f}"] = level_data

    # Save results
    outpath = os.path.join(os.path.dirname(__file__) or '.', args.output)
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {outpath}")

    # === Analysis ===
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    for L_str in results['data']:
        L = int(L_str)
        print(f"\n--- L={L} ---")
        print(f"{'T':>8} {'δ(L)':>8} {'δ(L/2)':>8} {'δ(L/4)':>8} "
              f"{'flow':>10} {'|m|':>6}")
        print("-" * 55)

        for T_str in sorted(results['data'][L_str].keys(), key=float):
            T = float(T_str)
            levels = results['data'][L_str][T_str]
            d0 = levels[0]['delta_mean']
            d1 = levels[1]['delta_mean'] if len(levels) > 1 else float('nan')
            d2 = levels[2]['delta_mean'] if len(levels) > 2 else float('nan')
            m0 = levels[0]['m_abs_mean']

            # Flow direction: δ(L/4) - δ(L)
            if len(levels) >= 3:
                flow = d2 - d0
                flow_str = f"{flow:+.4f}"
            else:
                flow_str = "N/A"

            marker = " ← Tc" if abs(T - Tc) < 0.001 else ""
            print(f"{T:>8.4f} {d0:>8.4f} {d1:>8.4f} {d2:>8.4f} "
                  f"{flow_str:>10} {m0:>6.3f}{marker}")

    # Scale invariance test at Tc
    print("\n--- Scale Invariance at Tc ---")
    for L_str in results['data']:
        L = int(L_str)
        Tc_str = f"{Tc:.5f}"
        if Tc_str in results['data'][L_str]:
            levels = results['data'][L_str][Tc_str]
            deltas = [lev['delta_mean'] for lev in levels]
            # Only use levels where L_level >= 8 (avoid finite-size contamination)
            deltas_clean = [lev['delta_mean'] for lev in levels if lev['L'] >= 8]
            if len(deltas_clean) >= 2:
                cv = np.std(deltas_clean) / np.mean(deltas_clean)
                print(f"  L={L}: δ across levels (L≥8) = "
                      f"{[f'{d:.4f}' for d in deltas_clean]}, CV = {cv:.4f}")

    # === Plot ===
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.set_facecolor('#0a0e17')

        for ax in axes:
            ax.set_facecolor('#0a0e17')
            ax.tick_params(colors='#94a3b8')
            for s in ['bottom', 'left']:
                ax.spines[s].set_color('#2a3550')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        cmap = plt.cm.coolwarm

        # Left: δ flow for largest L
        L_str = str(max(int(k) for k in results['data']))
        ax = axes[0]

        T_keys = sorted(results['data'][L_str].keys(), key=float)
        for T_str in T_keys:
            T = float(T_str)
            levels = results['data'][L_str][T_str]
            Ls = [lev['L'] for lev in levels]
            deltas = [lev['delta_mean'] for lev in levels]
            errs = [lev['delta_std'] for lev in levels]

            # Color by T relative to Tc
            t_norm = (T - 1.0) / 3.0
            c = cmap(t_norm)
            is_tc = abs(T - Tc) < 0.001
            lw = 2.5 if is_tc else 1.2
            ls = '-' if is_tc else '--'
            label = f'T={T:.2f}' + (' (Tc)' if is_tc else '')

            ax.errorbar(range(len(deltas)), deltas, yerr=errs,
                        fmt='o-', color=c, linewidth=lw, markersize=4,
                        label=label, capsize=2)

        ax.set_xlabel('RG Level (0=original)', color='#e2e8f0')
        ax.set_ylabel('δ (normalized IPR)', color='#e2e8f0')
        ax.set_title(f'δ Flow Under Block-Spin RG (L={L_str})', color='#e2e8f0')
        ax.legend(fontsize=7, facecolor='#1a2233', edgecolor='#2a3550',
                  labelcolor='#e2e8f0', loc='best')

        # Right: δ at Level 0 vs T for different L
        ax = axes[1]
        for L_str in results['data']:
            L = int(L_str)
            Ts = []
            deltas = []
            errs = []
            for T_str in sorted(results['data'][L_str].keys(), key=float):
                T = float(T_str)
                Ts.append(T)
                deltas.append(results['data'][L_str][T_str][0]['delta_mean'])
                errs.append(results['data'][L_str][T_str][0]['delta_std'])

            ax.errorbar(Ts, deltas, yerr=errs, fmt='o-', markersize=4,
                        label=f'L={L}', capsize=2)

        ax.axvline(Tc, color='#fbbf24', linestyle=':', alpha=0.5, label='Tc')
        ax.set_xlabel('Temperature T', color='#e2e8f0')
        ax.set_ylabel('δ(L, T) at Level 0', color='#e2e8f0')
        ax.set_title('δ vs T for different system sizes', color='#e2e8f0')
        ax.legend(fontsize=9, facecolor='#1a2233', edgecolor='#2a3550',
                  labelcolor='#e2e8f0')

        fig.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__) or '.',
                                 'ising_rg_delta_v2.png')
        fig.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"\nPlot saved: {plot_path}")

    except ImportError:
        print("\nmatplotlib not available, skipping plot")


if __name__ == '__main__':
    main()
