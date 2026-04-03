"""
2D Ising Model: Block-Pattern IPR as RG Flow Variable (v3)
==========================================================

v2 used δ_norm = m² (magnetization IPR), which is structurally
unable to show scale invariance at Tc because |m| ~ L^{-β/ν}.

v3 uses the IPR of the LOCAL BLOCK PATTERN DISTRIBUTION:
- Divide the lattice into 2×2 blocks
- Each block has one of 16 possible spin patterns
- Count the frequency p_i of each pattern (i=1..16)
- IPR = Σ p_i²

This measures local structural diversity, not global order.
At Tc, the pattern distribution may be self-similar under RG.

Predictions:
  1. T → 0: One pattern dominates → IPR → 1
  2. T → ∞: All 16 patterns equal → IPR → 1/16 = 0.0625
  3. T < Tc, coarse-graining: IPR increases (→ ordered fixed point)
  4. T > Tc, coarse-graining: IPR decreases (→ disordered fixed point)
  5. T = Tc: IPR is scale-invariant (RG fixed point)

Usage:
  python ising_rg_delta_v3_pattern.py [--max-L 128] [--n-samples 100]
"""

import numpy as np
import argparse
import json
import time
import os


# === Wolff Cluster Algorithm (same as v2) ===

def wolff_step(spins, beta):
    L = spins.shape[0]
    p_add = 1 - np.exp(-2 * beta)
    i, j = np.random.randint(0, L, size=2)
    seed_spin = spins[i, j]
    spins[i, j] *= -1
    stack = [(i, j)]
    size = 1
    while stack:
        ci, cj = stack.pop()
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = (ci + di) % L, (cj + dj) % L
            if spins[ni, nj] == seed_spin and np.random.rand() < p_add:
                spins[ni, nj] *= -1
                stack.append((ni, nj))
                size += 1
    return size


def thermalize(spins, beta, n_steps):
    for _ in range(n_steps):
        wolff_step(spins, beta)


# === Block Spin RG (same as v2) ===

def block_spin_transform(spins):
    L = spins.shape[0]
    L_new = L // 2
    new_spins = np.zeros((L_new, L_new), dtype=int)
    for i in range(L_new):
        for j in range(L_new):
            s = (spins[2*i, 2*j] + spins[2*i+1, 2*j] +
                 spins[2*i, 2*j+1] + spins[2*i+1, 2*j+1])
            new_spins[i, j] = 1 if s > 0 else (-1 if s < 0 else np.random.choice([-1, 1]))
    return new_spins


# === Block Pattern IPR ===

def pattern_to_index(s00, s01, s10, s11):
    """Convert 2×2 block of ±1 spins to index 0..15."""
    # Map -1→0, +1→1, then binary: b0*8 + b1*4 + b2*2 + b3
    b0 = (s00 + 1) // 2
    b1 = (s01 + 1) // 2
    b2 = (s10 + 1) // 2
    b3 = (s11 + 1) // 2
    return b0 * 8 + b1 * 4 + b2 * 2 + b3


def measure_block_pattern_ipr(spins):
    """
    Compute IPR of the 2×2 block pattern distribution.

    Returns dict with:
      - ipr: Σ p_i² (ranges 1/16 to 1)
      - delta_norm: (ipr - 1/16) / (1 - 1/16), normalized to [0, 1]
      - n_patterns: number of distinct patterns observed
      - m_abs: |magnetization| for comparison
    """
    L = spins.shape[0]
    if L < 2:
        m = abs(np.mean(spins))
        return {'ipr': 1.0, 'delta_norm': 1.0, 'n_patterns': 1, 'm_abs': m, 'L': L}

    n_blocks = (L // 2) ** 2
    counts = np.zeros(16, dtype=int)

    for i in range(0, L - 1, 2):
        for j in range(0, L - 1, 2):
            idx = pattern_to_index(spins[i, j], spins[i, j+1],
                                   spins[i+1, j], spins[i+1, j+1])
            counts[idx] += 1

    freq = counts / n_blocks
    ipr = np.sum(freq ** 2)

    # Normalize: IPR ∈ [1/16, 1] → δ ∈ [0, 1]
    ipr_min = 1.0 / 16
    delta_norm = (ipr - ipr_min) / (1.0 - ipr_min)

    m = abs(np.mean(spins))
    n_patterns = np.sum(counts > 0)

    return {
        'ipr': float(ipr),
        'delta_norm': float(delta_norm),
        'n_patterns': int(n_patterns),
        'm_abs': float(m),
        'L': L,
    }


def rg_flow_pattern(spins):
    """Perform block-spin RG, measure pattern IPR at each level."""
    levels = []
    current = spins.copy()

    while current.shape[0] >= 4:  # Need at least 4×4 for 2×2 blocks
        meas = measure_block_pattern_ipr(current)
        levels.append(meas)
        current = block_spin_transform(current)

    return levels


# === Main ===

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-L', type=int, default=128)
    parser.add_argument('--n-samples', type=int, default=100)
    parser.add_argument('--n-therm-factor', type=int, default=30)
    parser.add_argument('--n-decorr', type=int, default=5)
    parser.add_argument('--output', type=str, default='ising_rg_v3_pattern_results.json')
    args = parser.parse_args()

    Tc = 2 / np.log(1 + np.sqrt(2))

    T_coarse = [1.5, 2.0, 2.5, 3.0, 4.0]
    T_fine = [Tc - 0.1, Tc - 0.05, Tc, Tc + 0.05, Tc + 0.1]
    temperatures = sorted(set(T_coarse + T_fine))

    system_sizes = [s for s in [64, 128, 256] if s <= args.max_L]

    print("=" * 70)
    print("2D Ising: Block-Pattern IPR as RG Flow Variable (v3)")
    print("=" * 70)
    print(f"Onsager Tc = {Tc:.5f}")
    print(f"System sizes: {system_sizes}")
    print(f"Temperatures: {len(temperatures)} points")
    print(f"Samples: {args.n_samples}, Therm: {args.n_therm_factor}*L, Decorr: {args.n_decorr}")
    print(f"IPR limits: ordered=1.0, disordered=1/16={1/16:.4f}")
    print()

    results = {'Tc': Tc, 'params': vars(args), 'data': {}}

    total = len(system_sizes) * len(temperatures)
    count = 0

    for L in system_sizes:
        n_therm = args.n_therm_factor * L
        results['data'][str(L)] = {}

        for T in temperatures:
            count += 1
            beta = 1.0 / T
            t0 = time.time()
            print(f"[{count}/{total}] L={L}, T={T:.4f} (therm={n_therm}) ... ",
                  end='', flush=True)

            spins = np.random.choice([-1, 1], size=(L, L))
            thermalize(spins, beta, n_therm)

            all_flows = []
            for _ in range(args.n_samples):
                for __ in range(args.n_decorr):
                    wolff_step(spins, beta)
                flow = rg_flow_pattern(spins)
                all_flows.append(flow)

            # Aggregate
            n_levels = len(all_flows[0])
            level_data = []
            for lev in range(n_levels):
                iprs = [f[lev]['ipr'] for f in all_flows]
                deltas = [f[lev]['delta_norm'] for f in all_flows]
                m_abs = [f[lev]['m_abs'] for f in all_flows]
                Ll = all_flows[0][lev]['L']
                level_data.append({
                    'L': Ll,
                    'ipr_mean': float(np.mean(iprs)),
                    'ipr_std': float(np.std(iprs)),
                    'delta_mean': float(np.mean(deltas)),
                    'delta_std': float(np.std(deltas)),
                    'm_abs_mean': float(np.mean(m_abs)),
                })

            elapsed = time.time() - t0
            ipr0 = level_data[0]['ipr_mean']
            print(f"IPR={ipr0:.4f}, time={elapsed:.1f}s")

            results['data'][str(L)][f"{T:.5f}"] = level_data

    # Save
    outpath = os.path.join(os.path.dirname(__file__) or '.', args.output)
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {outpath}")

    # === Analysis ===
    print("\n" + "=" * 70)
    print("ANALYSIS: Block-Pattern IPR Flow")
    print("=" * 70)

    for L_str in results['data']:
        L = int(L_str)
        print(f"\n--- L={L} ---")
        print(f"{'T':>8} {'IPR(L)':>8} {'IPR(L/2)':>8} {'IPR(L/4)':>8} "
              f"{'flow':>10} {'|m|':>6}")
        print("-" * 58)

        for T_str in sorted(results['data'][L_str].keys(), key=float):
            T = float(T_str)
            levels = results['data'][L_str][T_str]
            ipr0 = levels[0]['ipr_mean']
            ipr1 = levels[1]['ipr_mean'] if len(levels) > 1 else float('nan')
            ipr2 = levels[2]['ipr_mean'] if len(levels) > 2 else float('nan')
            m0 = levels[0]['m_abs_mean']

            if len(levels) >= 3:
                flow = ipr2 - ipr0
                flow_dir = "→ ordered" if flow > 0.001 else ("→ disordered" if flow < -0.001 else "≈ fixed")
                flow_str = f"{flow:+.4f}"
            else:
                flow_str = "N/A"
                flow_dir = ""

            marker = " ← Tc" if abs(T - Tc) < 0.001 else ""
            print(f"{T:>8.4f} {ipr0:>8.4f} {ipr1:>8.4f} {ipr2:>8.4f} "
                  f"{flow_str:>10} {m0:>6.3f}{marker}")

    # Scale invariance test
    print("\n--- Scale Invariance at Tc (Pattern IPR) ---")
    for L_str in results['data']:
        Tc_str = f"{Tc:.5f}"
        if Tc_str in results['data'][L_str]:
            levels = results['data'][L_str][Tc_str]
            iprs = [lev['ipr_mean'] for lev in levels if lev['L'] >= 8]
            if len(iprs) >= 2:
                cv = np.std(iprs) / np.mean(iprs)
                print(f"  L={L_str}: IPR across levels (L≥8) = "
                      f"{[f'{x:.4f}' for x in iprs]}, CV = {cv:.4f}")

    # === Plot ===
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.set_facecolor('#0a0e17')
        for ax in axes:
            ax.set_facecolor('#0a0e17')
            ax.tick_params(colors='#94a3b8')
            for s in ['bottom', 'left']:
                ax.spines[s].set_color('#2a3550')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        cmap = plt.cm.coolwarm

        # 1: IPR flow for largest L
        L_str = str(max(int(k) for k in results['data']))
        ax = axes[0]
        for T_str in sorted(results['data'][L_str].keys(), key=float):
            T = float(T_str)
            levels = results['data'][L_str][T_str]
            iprs = [lev['ipr_mean'] for lev in levels]
            errs = [lev['ipr_std'] for lev in levels]
            t_norm = (T - 1.0) / 3.0
            is_tc = abs(T - Tc) < 0.001
            lw = 2.5 if is_tc else 1.2
            label = f'T={T:.2f}' + (' (Tc)' if is_tc else '')
            ax.errorbar(range(len(iprs)), iprs, yerr=errs, fmt='o-',
                        color=cmap(t_norm), linewidth=lw, markersize=4,
                        label=label, capsize=2)

        ax.axhline(1/16, color='#475569', linestyle=':', alpha=0.5, label='1/16 (disorder)')
        ax.set_xlabel('RG Level', color='#e2e8f0')
        ax.set_ylabel('Block-Pattern IPR', color='#e2e8f0')
        ax.set_title(f'Pattern IPR Flow (L={L_str})', color='#e2e8f0')
        ax.legend(fontsize=6, facecolor='#1a2233', edgecolor='#2a3550',
                  labelcolor='#e2e8f0')

        # 2: IPR at Level 0 vs T
        ax = axes[1]
        for L_str in results['data']:
            Ts, iprs, errs = [], [], []
            for T_str in sorted(results['data'][L_str].keys(), key=float):
                Ts.append(float(T_str))
                iprs.append(results['data'][L_str][T_str][0]['ipr_mean'])
                errs.append(results['data'][L_str][T_str][0]['ipr_std'])
            ax.errorbar(Ts, iprs, yerr=errs, fmt='o-', markersize=4,
                        label=f'L={L_str}', capsize=2)
        ax.axvline(Tc, color='#fbbf24', linestyle=':', alpha=0.5, label='Tc')
        ax.axhline(1/16, color='#475569', linestyle=':', alpha=0.3)
        ax.set_xlabel('Temperature T', color='#e2e8f0')
        ax.set_ylabel('Pattern IPR at Level 0', color='#e2e8f0')
        ax.set_title('IPR vs T (different L)', color='#e2e8f0')
        ax.legend(fontsize=9, facecolor='#1a2233', edgecolor='#2a3550',
                  labelcolor='#e2e8f0')

        # 3: Compare v2 (magnetization) vs v3 (pattern) at Tc
        ax = axes[2]
        Tc_str = f"{Tc:.5f}"
        for L_str in results['data']:
            if Tc_str in results['data'][L_str]:
                levels = results['data'][L_str][Tc_str]
                Ls = [lev['L'] for lev in levels]
                iprs = [lev['ipr_mean'] for lev in levels]
                ax.plot(range(len(iprs)), iprs, 'o-', markersize=5,
                        label=f'Pattern IPR, L={L_str}')
        ax.axhline(1/16, color='#475569', linestyle=':', alpha=0.5)
        ax.set_xlabel('RG Level', color='#e2e8f0')
        ax.set_ylabel('IPR at Tc', color='#e2e8f0')
        ax.set_title('Scale Invariance Test at Tc', color='#e2e8f0')
        ax.legend(fontsize=9, facecolor='#1a2233', edgecolor='#2a3550',
                  labelcolor='#e2e8f0')

        fig.tight_layout()
        plot_path = os.path.join(os.path.dirname(__file__) or '.',
                                 'ising_rg_delta_v3_pattern.png')
        fig.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"\nPlot saved: {plot_path}")

    except ImportError:
        print("\nmatplotlib not available")


if __name__ == '__main__':
    main()
