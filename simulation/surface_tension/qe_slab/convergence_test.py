#!/usr/bin/env python3
"""
Convergence tests for slab calculations (Stanford reviewer Issues 6 & 7).

Issue 6: ecutwfc convergence (30→50→70 Ry) and slab thickness (7→9→11 layers)
Issue 7: ILDOS energy window sensitivity (emin ±2, ±3 eV)

Tests Al(111) and Cu(111).

Usage: activate QE conda env first, then run this script.
"""

import os
import subprocess
import re
import numpy as np

QE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(QE_DIR, "..", "figures")
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_qe(program, input_file, output_file):
    """Run a QE program."""
    with open(input_file) as fin:
        result = subprocess.run(
            [program], stdin=fin, capture_output=True, text=True, timeout=7200
        )
    with open(output_file, "w") as fout:
        fout.write(result.stdout)
        if result.stderr:
            fout.write("\n--- STDERR ---\n" + result.stderr)
    return result.returncode == 0


def run_average(avg_input, avg_output):
    """Run average.x."""
    with open(avg_input) as fin:
        result = subprocess.run(
            ["average.x"], stdin=fin, capture_output=True, text=True, timeout=300
        )
    with open(avg_output, "w") as fout:
        fout.write(result.stdout)
    return result.returncode == 0


def extract_nmid_nbulk(avg_dat_file, n_layers, interlayer_d, cell_z):
    """Extract n_mid/n_bulk from planar averaged density."""
    data = np.loadtxt(avg_dat_file)
    z = data[:, 0]  # in bohr
    rho = data[:, 1]

    bohr2ang = 0.529177
    z_ang = z * bohr2ang

    # Slab region: from first layer to last layer
    slab_start = 0.0
    slab_end = (n_layers - 1) * interlayer_d

    # Bulk-like region: middle layers
    bulk_start = interlayer_d * 1.5
    bulk_end = slab_end - interlayer_d * 1.5

    # Midpoint positions between layers
    midpoints = [(i + 0.5) * interlayer_d for i in range(n_layers - 1)]

    # Interior midpoints (exclude surface midpoints)
    interior_mids = [m for m in midpoints if bulk_start < m < bulk_end]
    if not interior_mids:
        interior_mids = midpoints[1:-1] if len(midpoints) > 2 else midpoints

    # Get density at midpoints
    mid_densities = []
    for m in interior_mids:
        idx = np.argmin(np.abs(z_ang - m))
        mid_densities.append(rho[idx])

    # Get bulk density (average in bulk region)
    bulk_mask = (z_ang > bulk_start) & (z_ang < bulk_end)
    if np.sum(bulk_mask) > 10:
        bulk_density = np.mean(rho[bulk_mask])
    else:
        # Fallback: peak density in slab region
        slab_mask = (z_ang > slab_start) & (z_ang < slab_end)
        bulk_density = np.max(rho[slab_mask])

    mean_mid = np.mean(mid_densities) if mid_densities else 0.0
    ratio = mean_mid / bulk_density if bulk_density > 0 else 0.0

    return ratio, mean_mid, bulk_density


def generate_slab_input(element, prefix, ecutwfc, ecutrho, n_layers,
                        a_lat, outdir, pseudo_file):
    """Generate SCF input for FCC(111) slab."""
    in_plane = a_lat / np.sqrt(2)
    interlayer_d = a_lat / np.sqrt(3)
    vacuum = 15.0
    total_z = (n_layers - 1) * interlayer_d + vacuum

    lines = []
    lines.append("&CONTROL")
    lines.append(f"  calculation  = 'scf'")
    lines.append(f"  prefix       = '{prefix}'")
    lines.append(f"  outdir       = '{outdir}'")
    lines.append(f"  pseudo_dir   = './pseudo/'")
    lines.append(f"  verbosity    = 'high'")
    lines.append("/\n")
    lines.append("&SYSTEM")
    lines.append(f"  ibrav        = 0")
    lines.append(f"  nat          = {n_layers}")
    lines.append(f"  ntyp         = 1")
    lines.append(f"  ecutwfc      = {ecutwfc:.1f}")
    lines.append(f"  ecutrho      = {ecutrho:.1f}")
    lines.append(f"  occupations  = 'smearing'")
    lines.append(f"  smearing     = 'mp'")
    lines.append(f"  degauss      = 0.02")
    lines.append(f"  nosym        = .true.")
    lines.append("/\n")
    lines.append("&ELECTRONS")
    lines.append(f"  conv_thr     = 1.0d-8")
    lines.append(f"  mixing_beta  = 0.3")
    lines.append(f"  mixing_mode  = 'local-TF'")
    lines.append("/\n")

    mass = {"Al": 26.9815, "Cu": 63.546}
    lines.append("ATOMIC_SPECIES")
    lines.append(f"  {element}  {mass[element]:.4f}  {pseudo_file}\n")

    lines.append("CELL_PARAMETERS angstrom")
    lines.append(f"  {in_plane:.4f}  0.0000  0.0000")
    lines.append(f"  {in_plane/2:.4f}  {in_plane*np.sqrt(3)/2:.4f}  0.0000")
    lines.append(f"  0.0000  0.0000  {total_z:.4f}\n")

    lines.append("ATOMIC_POSITIONS angstrom")
    # ABC stacking
    shifts = [
        (0.0, 0.0),
        (in_plane / 2, in_plane * np.sqrt(3) / 6),
        (0.0, in_plane * np.sqrt(3) / 3),
    ]
    for i in range(n_layers):
        sx, sy = shifts[i % 3]
        z = i * interlayer_d
        lines.append(f"  {element}  {sx:.4f}  {sy:.4f}  {z:.4f}")

    lines.append("\nK_POINTS automatic")
    lines.append("  8 8 1  0 0 0")

    return "\n".join(lines), interlayer_d, total_z


def generate_pp_input(prefix, outdir, filplot, emin, emax=100.0):
    """Generate pp.x input for ILDOS."""
    return f"""&INPUTPP
  prefix  = '{prefix}'
  outdir  = '{outdir}'
  filplot = '{filplot}'
  plot_num = 10
  emin = {emin:.1f}
  emax = {emax:.1f}
/
"""


def generate_avg_input(filplot):
    """Generate average.x input."""
    return f"""1
{filplot}
1.0
1000
3
1.0
"""


# =====================================================================
# ISSUE 6: Ecutwfc convergence
# =====================================================================
def test_ecutwfc_convergence():
    print("=" * 70)
    print("ISSUE 6a: ECUTWFC CONVERGENCE TEST")
    print("=" * 70)

    configs = {
        "Al": {
            "a_lat": 4.05, "pseudo": "Al.pbe-n-kjpaw_psl.1.0.0.UPF",
            "ecutwfc_list": [30, 50, 70],
            "ecutrho_ratio": 8,
            "emin_valence": -15.0,
            "n_layers": 7,
        },
        "Cu": {
            "a_lat": 3.615, "pseudo": "Cu.pbe-dn-kjpaw_psl.1.0.0.UPF",
            "ecutwfc_list": [40, 60, 80],
            "ecutrho_ratio": 8,
            "emin_valence": -10.0,
            "n_layers": 7,
        },
    }

    results = {}

    for elem, cfg in configs.items():
        print(f"\n--- {elem}(111) ecutwfc convergence ---")
        elem_results = []

        for ecut in cfg["ecutwfc_list"]:
            ecutrho = ecut * cfg["ecutrho_ratio"]
            prefix = f"{elem.lower()}_ecut{ecut}"
            outdir = f"./tmp_conv/{prefix}/"
            os.makedirs(os.path.join(QE_DIR, f"tmp_conv/{prefix}"), exist_ok=True)

            # Generate and run SCF
            scf_text, interlayer_d, cell_z = generate_slab_input(
                elem, prefix, ecut, ecutrho, cfg["n_layers"],
                cfg["a_lat"], outdir, cfg["pseudo"]
            )
            scf_in = os.path.join(QE_DIR, f"{prefix}_scf.in")
            scf_out = os.path.join(QE_DIR, f"{prefix}_scf.out")
            with open(scf_in, "w") as f:
                f.write(scf_text)

            print(f"  ecutwfc={ecut} Ry, ecutrho={ecutrho} Ry ... ", end="", flush=True)
            success = run_qe("pw.x", scf_in, scf_out)
            if not success:
                print("SCF FAILED")
                elem_results.append((ecut, None, None, None))
                continue

            # Run pp.x for valence ILDOS
            pp_text = generate_pp_input(prefix, outdir,
                                         f"{prefix}_valence.dat",
                                         cfg["emin_valence"])
            pp_in = os.path.join(QE_DIR, f"{prefix}_pp.in")
            pp_out = os.path.join(QE_DIR, f"{prefix}_pp.out")
            with open(pp_in, "w") as f:
                f.write(pp_text)
            run_qe("pp.x", pp_in, pp_out)

            # Run average.x
            avg_text = generate_avg_input(f"{prefix}_valence.dat")
            avg_in = os.path.join(QE_DIR, f"{prefix}_avg.in")
            avg_out = os.path.join(QE_DIR, f"{prefix}_avg.out")
            with open(avg_in, "w") as f:
                f.write(avg_text)
            run_average(avg_in, avg_out)

            # Extract n_mid/n_bulk
            avg_dat = os.path.join(QE_DIR, "avg.dat")
            if os.path.exists(avg_dat):
                ratio, mid, bulk = extract_nmid_nbulk(
                    avg_dat, cfg["n_layers"], interlayer_d, cell_z
                )
                print(f"n_mid/n_bulk = {ratio:.4f}")
                elem_results.append((ecut, ratio, mid, bulk))
            else:
                print("avg.dat not found")
                elem_results.append((ecut, None, None, None))

        results[elem] = elem_results

    return results


# =====================================================================
# ISSUE 6b: Slab thickness convergence
# =====================================================================
def test_slab_thickness():
    print("\n" + "=" * 70)
    print("ISSUE 6b: SLAB THICKNESS CONVERGENCE TEST")
    print("=" * 70)

    configs = {
        "Al": {
            "a_lat": 4.05, "pseudo": "Al.pbe-n-kjpaw_psl.1.0.0.UPF",
            "ecutwfc": 30, "ecutrho": 240,
            "emin_valence": -15.0,
            "layer_list": [7, 9, 11],
        },
        "Cu": {
            "a_lat": 3.615, "pseudo": "Cu.pbe-dn-kjpaw_psl.1.0.0.UPF",
            "ecutwfc": 40, "ecutrho": 320,
            "emin_valence": -10.0,
            "layer_list": [7, 9, 11],
        },
    }

    results = {}

    for elem, cfg in configs.items():
        print(f"\n--- {elem}(111) slab thickness convergence ---")
        elem_results = []

        for n_layers in cfg["layer_list"]:
            prefix = f"{elem.lower()}_L{n_layers}"
            outdir = f"./tmp_conv/{prefix}/"
            os.makedirs(os.path.join(QE_DIR, f"tmp_conv/{prefix}"), exist_ok=True)

            scf_text, interlayer_d, cell_z = generate_slab_input(
                elem, prefix, cfg["ecutwfc"], cfg["ecutrho"], n_layers,
                cfg["a_lat"], outdir, cfg["pseudo"]
            )
            scf_in = os.path.join(QE_DIR, f"{prefix}_scf.in")
            scf_out = os.path.join(QE_DIR, f"{prefix}_scf.out")
            with open(scf_in, "w") as f:
                f.write(scf_text)

            print(f"  {n_layers} layers ... ", end="", flush=True)
            success = run_qe("pw.x", scf_in, scf_out)
            if not success:
                print("SCF FAILED")
                elem_results.append((n_layers, None, None, None))
                continue

            pp_text = generate_pp_input(prefix, outdir,
                                         f"{prefix}_valence.dat",
                                         cfg["emin_valence"])
            pp_in = os.path.join(QE_DIR, f"{prefix}_pp.in")
            pp_out = os.path.join(QE_DIR, f"{prefix}_pp.out")
            with open(pp_in, "w") as f:
                f.write(pp_text)
            run_qe("pp.x", pp_in, pp_out)

            avg_text = generate_avg_input(f"{prefix}_valence.dat")
            avg_in = os.path.join(QE_DIR, f"{prefix}_avg.in")
            avg_out = os.path.join(QE_DIR, f"{prefix}_avg.out")
            with open(avg_in, "w") as f:
                f.write(avg_text)
            run_average(avg_in, avg_out)

            avg_dat = os.path.join(QE_DIR, "avg.dat")
            if os.path.exists(avg_dat):
                ratio, mid, bulk = extract_nmid_nbulk(
                    avg_dat, n_layers, interlayer_d, cell_z
                )
                print(f"n_mid/n_bulk = {ratio:.4f}")
                elem_results.append((n_layers, ratio, mid, bulk))
            else:
                print("avg.dat not found")
                elem_results.append((n_layers, None, None, None))

        results[elem] = elem_results

    return results


# =====================================================================
# ISSUE 7: ILDOS window sensitivity
# =====================================================================
def test_ildos_window():
    print("\n" + "=" * 70)
    print("ISSUE 7: ILDOS ENERGY WINDOW SENSITIVITY")
    print("=" * 70)

    # Use existing SCF data (7-layer slabs already computed)
    configs = {
        "Al": {
            "prefix": "al111", "outdir": "./tmp/",
            "interlayer_d": 4.05 / np.sqrt(3), "n_layers": 7,
            "emin_base": -15.0,
            "emin_shifts": [-3, -2, 0, +2, +3],
        },
        "Cu": {
            "prefix": "cu111", "outdir": "./tmp_cu/",
            "interlayer_d": 3.615 / np.sqrt(3), "n_layers": 7,
            "emin_base": -10.0,
            "emin_shifts": [-3, -2, 0, +2, +3],
        },
        "Na": {
            "prefix": "na110", "outdir": "./tmp/",
            "interlayer_d": 3.0,  # approximate for BCC(110)
            "n_layers": 7,
            "emin_base": -5.0,
            "emin_shifts": [-3, -2, 0, +2, +3],
        },
        "Zn": {
            "prefix": "zn0001", "outdir": "./tmp/",
            "interlayer_d": 2.665,  # HCP c/2
            "n_layers": 7,
            "emin_base": -10.0,
            "emin_shifts": [-3, -2, 0, +2, +3],
        },
    }

    results = {}

    for elem, cfg in configs.items():
        # Check if SCF data exists
        save_dir = os.path.join(QE_DIR, cfg["outdir"].strip("./"), f"{cfg['prefix']}.save")
        if not os.path.exists(save_dir):
            # Also try without the prefix
            save_dir2 = os.path.join(QE_DIR, "tmp", f"{cfg['prefix']}.save")
            if not os.path.exists(save_dir2):
                print(f"\n--- {elem}: SCF data not found at {save_dir}, skipping ---")
                continue

        print(f"\n--- {elem} ILDOS window sensitivity ---")
        elem_results = []

        for shift in cfg["emin_shifts"]:
            emin = cfg["emin_base"] + shift
            tag = f"{elem.lower()}_emin{emin:+.0f}"

            pp_text = generate_pp_input(cfg["prefix"], cfg["outdir"],
                                         f"{tag}_valence.dat", emin)
            pp_in = os.path.join(QE_DIR, f"{tag}_pp.in")
            pp_out = os.path.join(QE_DIR, f"{tag}_pp.out")
            with open(pp_in, "w") as f:
                f.write(pp_text)

            print(f"  emin={emin:.0f} eV (shift={shift:+d}) ... ", end="", flush=True)
            run_qe("pp.x", pp_in, pp_out)

            avg_text = generate_avg_input(f"{tag}_valence.dat")
            avg_in = os.path.join(QE_DIR, f"{tag}_avg.in")
            avg_out = os.path.join(QE_DIR, f"{tag}_avg.out")
            with open(avg_in, "w") as f:
                f.write(avg_text)
            run_average(avg_in, avg_out)

            avg_dat = os.path.join(QE_DIR, "avg.dat")
            if os.path.exists(avg_dat):
                ratio, mid, bulk = extract_nmid_nbulk(
                    avg_dat, cfg["n_layers"], cfg["interlayer_d"],
                    (cfg["n_layers"] - 1) * cfg["interlayer_d"] + 15.0
                )
                print(f"n_mid/n_bulk = {ratio:.4f}")
                elem_results.append((emin, shift, ratio, mid, bulk))
            else:
                print("avg.dat not found")
                elem_results.append((emin, shift, None, None, None))

        results[elem] = elem_results

    return results


def main():
    # Run all tests
    ecut_results = test_ecutwfc_convergence()
    thick_results = test_slab_thickness()
    ildos_results = test_ildos_window()

    # ── Summary ──
    print("\n" + "=" * 70)
    print("FULL CONVERGENCE SUMMARY")
    print("=" * 70)

    print("\n--- Ecutwfc convergence ---")
    for elem, results in ecut_results.items():
        print(f"  {elem}(111):")
        for ecut, ratio, mid, bulk in results:
            if ratio is not None:
                print(f"    ecutwfc={ecut:3d} Ry: n_mid/n_bulk = {ratio:.4f}")
            else:
                print(f"    ecutwfc={ecut:3d} Ry: FAILED")

    print("\n--- Slab thickness convergence ---")
    for elem, results in thick_results.items():
        print(f"  {elem}(111):")
        for nl, ratio, mid, bulk in results:
            if ratio is not None:
                print(f"    {nl:2d} layers: n_mid/n_bulk = {ratio:.4f}")
            else:
                print(f"    {nl:2d} layers: FAILED")

    print("\n--- ILDOS window sensitivity ---")
    for elem, results in ildos_results.items():
        print(f"  {elem}:")
        for emin, shift, ratio, mid, bulk in results:
            if ratio is not None:
                print(f"    emin={emin:+6.0f} eV (shift={shift:+d}): "
                      f"n_mid/n_bulk = {ratio:.4f}")
            else:
                print(f"    emin={emin:+6.0f} eV: FAILED")

    # Save to file
    outfile = os.path.join(RESULTS_DIR, "convergence_test_results.txt")
    with open(outfile, "w") as f:
        f.write("Slab Convergence Tests (Stanford Reviewer Issues 6 & 7)\n")
        f.write("=" * 60 + "\n\n")

        f.write("Issue 6a: Ecutwfc convergence\n")
        for elem, results in ecut_results.items():
            f.write(f"  {elem}(111):\n")
            for ecut, ratio, mid, bulk in results:
                if ratio is not None:
                    f.write(f"    ecutwfc={ecut} Ry: n_mid/n_bulk = {ratio:.4f}\n")
        f.write("\n")

        f.write("Issue 6b: Slab thickness convergence\n")
        for elem, results in thick_results.items():
            f.write(f"  {elem}(111):\n")
            for nl, ratio, mid, bulk in results:
                if ratio is not None:
                    f.write(f"    {nl} layers: n_mid/n_bulk = {ratio:.4f}\n")
        f.write("\n")

        f.write("Issue 7: ILDOS window sensitivity\n")
        for elem, results in ildos_results.items():
            f.write(f"  {elem}:\n")
            for emin, shift, ratio, mid, bulk in results:
                if ratio is not None:
                    f.write(f"    emin={emin:+.0f} eV (shift={shift:+d}): "
                            f"n_mid/n_bulk = {ratio:.4f}\n")
        f.write("\n")

    print(f"\nResults saved to {outfile}")


if __name__ == "__main__":
    main()
