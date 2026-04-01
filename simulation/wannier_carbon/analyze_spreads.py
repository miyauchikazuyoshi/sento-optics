#!/usr/bin/env python3
"""
Analyze Wannier function spreads for diamond and graphite carbon allotropes.

Parses .wout files, computes per-orbital spread (Omega / num_wann),
and compares against Paper II metal correlation K = 3.748.
"""

import re
import sys
import os


def parse_wout(filepath):
    """Parse a Wannier90 .wout file to extract final WF spreads and total Omega."""
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found. Run calculations first.")
        return None

    with open(filepath) as f:
        text = f.read()

    # Extract individual WF spreads from the final state
    # Pattern: "WF centre and target spread" section at end
    wf_spreads = []
    # Look for lines like: "    1    -0.000000   0.000000   0.000000   1.234567"
    # in the "Final State" section
    in_final = False
    for line in text.split('\n'):
        if 'Final State' in line:
            in_final = True
            continue
        if in_final:
            # Match WF spread lines: "WF centre ... ( spread_value )"
            m = re.match(
                r'\s*WF\s+centre\s+and\s+spread\s+(\d+)\s+'
                r'\(\s*([\d.Ee+-]+)\s*,\s*([\d.Ee+-]+)\s*,\s*([\d.Ee+-]+)\s*\)\s+'
                r'([\d.Ee+-]+)',
                line
            )
            if m:
                wf_spreads.append(float(m.group(5)))
            # Also try simpler format
            m2 = re.match(
                r'\s+(\d+)\s+([\d.Ee+-]+)\s+([\d.Ee+-]+)\s+([\d.Ee+-]+)\s+([\d.Ee+-]+)',
                line
            )
            if m2 and not m:
                wf_spreads.append(float(m2.group(5)))

    # Extract Omega Total from final iteration
    omega_total = None
    omega_matches = re.findall(r'Omega Total\s+=\s+([\d.Ee+-]+)', text)
    if omega_matches:
        omega_total = float(omega_matches[-1])  # last occurrence = final

    # Extract Omega components
    omega_i = None
    omega_d = None
    omega_od = None
    oi_matches = re.findall(r'Omega I\s+=\s+([\d.Ee+-]+)', text)
    od_matches = re.findall(r'Omega D\s+=\s+([\d.Ee+-]+)', text)
    ood_matches = re.findall(r'Omega OD\s+=\s+([\d.Ee+-]+)', text)
    if oi_matches:
        omega_i = float(oi_matches[-1])
    if od_matches:
        omega_d = float(od_matches[-1])
    if ood_matches:
        omega_od = float(ood_matches[-1])

    # Extract num_wann
    num_wann = None
    m = re.search(r'Number of Wannier Functions\s*:\s*(\d+)', text)
    if m:
        num_wann = int(m.group(1))

    return {
        'wf_spreads': wf_spreads,
        'omega_total': omega_total,
        'omega_i': omega_i,
        'omega_d': omega_d,
        'omega_od': omega_od,
        'num_wann': num_wann,
    }


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    diamond_wout = os.path.join(base, 'diamond', 'diamond.wout')
    graphite_wout = os.path.join(base, 'graphite', 'graphite.wout')

    # Paper II metal correlation constant
    K_metal = 3.748  # Ang^2

    print("=" * 70)
    print("  Wannier Spread Analysis: Carbon Allotropes")
    print("=" * 70)

    results = {}
    for name, path in [('Diamond', diamond_wout), ('Graphite', graphite_wout)]:
        print(f"\n--- {name} ---")
        data = parse_wout(path)
        if data is None:
            results[name] = None
            continue

        results[name] = data
        num_wann = data['num_wann']
        omega = data['omega_total']

        print(f"  num_wann    = {num_wann}")
        print(f"  Omega Total = {omega:.6f} Ang^2" if omega else "  Omega Total = N/A")
        if data['omega_i']:
            print(f"  Omega I     = {data['omega_i']:.6f} Ang^2")
        if data['omega_d']:
            print(f"  Omega D     = {data['omega_d']:.6f} Ang^2")
        if data['omega_od']:
            print(f"  Omega OD    = {data['omega_od']:.6f} Ang^2")

        if data['wf_spreads']:
            print(f"  Individual WF spreads (Ang^2):")
            for i, s in enumerate(data['wf_spreads']):
                print(f"    WF {i+1:3d}: {s:.6f}")

        if omega and num_wann:
            omega_per_wf = omega / num_wann
            print(f"  Omega/WF    = {omega_per_wf:.6f} Ang^2")

    # Comparison table
    print("\n" + "=" * 70)
    print("  Comparison Table")
    print("=" * 70)
    print(f"  {'System':<12} {'num_wann':>8} {'Omega_total':>12} {'Omega/WF':>10} {'vs K_metal':>10}")
    print(f"  {'-'*12} {'-'*8} {'-'*12} {'-'*10} {'-'*10}")

    all_ok = True
    for name in ['Diamond', 'Graphite']:
        data = results.get(name)
        if data is None or data['omega_total'] is None:
            print(f"  {name:<12} {'N/A':>8} {'N/A':>12} {'N/A':>10} {'N/A':>10}")
            all_ok = False
            continue

        nw = data['num_wann']
        ot = data['omega_total']
        opw = ot / nw if nw else 0
        ratio = opw / K_metal if K_metal else 0
        print(f"  {name:<12} {nw:>8d} {ot:>12.4f} {opw:>10.4f} {ratio:>10.4f}")

    print(f"\n  K_metal (Paper II) = {K_metal:.3f} Ang^2")
    print()

    # PASS/FAIL logic
    # Diamond (insulator): expect Omega/WF < K_metal (localized sp3 bonds)
    # Graphite (semimetal): expect Omega/WF between diamond and metals
    diamond_data = results.get('Diamond')
    graphite_data = results.get('Graphite')

    if diamond_data and diamond_data['omega_total'] and diamond_data['num_wann']:
        d_opw = diamond_data['omega_total'] / diamond_data['num_wann']
        if d_opw < K_metal:
            print("  Diamond: PASS  (Omega/WF < K_metal => insulator is more localized)")
        else:
            print("  Diamond: FAIL  (Omega/WF >= K_metal => unexpected for insulator)")
            all_ok = False
    else:
        print("  Diamond: SKIP  (no data)")
        all_ok = False

    if graphite_data and graphite_data['omega_total'] and graphite_data['num_wann']:
        g_opw = graphite_data['omega_total'] / graphite_data['num_wann']
        if diamond_data and diamond_data['omega_total'] and diamond_data['num_wann']:
            d_opw = diamond_data['omega_total'] / diamond_data['num_wann']
            if g_opw > d_opw:
                print("  Graphite: PASS  (Omega/WF > Diamond => semimetal more delocalized)")
            else:
                print("  Graphite: FAIL  (Omega/WF <= Diamond => unexpected)")
                all_ok = False
        else:
            print("  Graphite: SKIP  (no diamond reference)")
            all_ok = False
    else:
        print("  Graphite: SKIP  (no data)")
        all_ok = False

    print()
    if all_ok:
        print("  OVERALL: PASS")
    else:
        print("  OVERALL: INCOMPLETE or FAIL (check results above)")

    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
