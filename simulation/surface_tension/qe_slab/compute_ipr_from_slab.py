"""
Compute orbital-resolved IPR and layer-resolved δ_IPR(z) from QE slab wavefunctions.

This script reads the KS wavefunctions from a QE calculation and computes:
1. IPR for each KS orbital on the real-space grid
2. Layer-resolved δ_IPR(z) profile
3. Charge density n(z) profile (for comparison with boundary density)
4. s/p/d orbital character per layer (via projected DOS)

Usage:
    python compute_ipr_from_slab.py <prefix> <outdir>

Requirements:
    - numpy, scipy, matplotlib
    - QE must have been run with verbosity='high'
    - pp.x (post-processing) must be available for charge density extraction
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import sys
import struct

def read_charge_density_1d(prefix, outdir='./tmp/'):
    """
    Use pp.x to extract planar-averaged charge density n(z).
    Creates input for pp.x, runs it, then reads the output.
    """
    # Step 1: Extract 3D charge density with pp.x
    pp_input = f"""&INPUTPP
  prefix = '{prefix}'
  outdir = '{outdir}'
  filplot = '{prefix}_charge.dat'
  plot_num = 0
/
"""
    with open(f'{prefix}_pp.in', 'w') as f:
        f.write(pp_input)

    # Step 2: Average along z with average.x
    avg_input = f"""1
{prefix}_charge.dat
1.0
1000
3
1.0
"""
    with open(f'{prefix}_avg.in', 'w') as f:
        f.write(avg_input)

    return pp_input, avg_input


def compute_ipr_from_cube(cube_file):
    """
    Compute IPR from a Gaussian cube file containing |ψ|² on a grid.

    IPR = ∫|ψ(r)|⁴ d³r / (∫|ψ(r)|² d³r)²

    For a discrete grid: IPR = Σ|ψᵢ|⁴ Δv / (Σ|ψᵢ|² Δv)²
    """
    # Read cube file
    with open(cube_file, 'r') as f:
        # Skip 2 comment lines
        f.readline()
        f.readline()

        # Number of atoms and origin
        parts = f.readline().split()
        natom = int(parts[0])
        origin = np.array([float(x) for x in parts[1:4]])

        # Grid dimensions and vectors
        nx_line = f.readline().split()
        nx = int(nx_line[0])
        dx = np.array([float(x) for x in nx_line[1:4]])

        ny_line = f.readline().split()
        ny = int(ny_line[0])
        dy = np.array([float(x) for x in ny_line[1:4]])

        nz_line = f.readline().split()
        nz = int(nz_line[0])
        dz_vec = np.array([float(x) for x in nz_line[1:4]])

        # Skip atom lines
        for _ in range(natom):
            f.readline()

        # Read volumetric data
        data = []
        for line in f:
            data.extend([float(x) for x in line.split()])

    psi2 = np.array(data).reshape((nx, ny, nz))

    # Volume element
    dv = abs(np.dot(dx, np.cross(dy, dz_vec)))

    # IPR = ∫ρ² dv / (∫ρ dv)²
    integral_rho2 = np.sum(psi2**2) * dv
    integral_rho = np.sum(psi2) * dv

    ipr = integral_rho2 / (integral_rho**2)

    # z-profile: average over xy planes
    z_coords = origin[2] + np.arange(nz) * dz_vec[2]
    rho_z = np.mean(psi2, axis=(0, 1))

    return ipr, z_coords, rho_z


def compute_layer_delta(z_coords, rho_z, layer_positions, layer_width=1.0):
    """
    Compute δ_IPR resolved by layer.

    For each layer, integrate IPR over a slab centered at the layer position.
    """
    delta_per_layer = []

    for z_layer in layer_positions:
        mask = np.abs(z_coords - z_layer) < layer_width
        if np.sum(mask) == 0:
            delta_per_layer.append(np.nan)
            continue

        rho_layer = rho_z[mask]
        # IPR within this layer
        ipr_layer = np.sum(rho_layer**2) / (np.sum(rho_layer)**2 + 1e-30)
        n_points = np.sum(mask)
        delta_layer = 1.0 / (n_points * ipr_layer + 1e-30)
        delta_per_layer.append(delta_layer)

    return np.array(delta_per_layer)


def run_analysis(prefix, outdir='./tmp/', n_layers=7, layer_spacing=2.338,
                 element='Al'):
    """
    Full analysis pipeline:
    1. Generate pp.x and average.x inputs
    2. Run them (if executables available)
    3. Parse output and compute δ_IPR(z)
    """

    print(f"=" * 60)
    print(f"IPR Analysis for {element} slab ({n_layers} layers)")
    print(f"=" * 60)

    # Generate input files
    pp_in, avg_in = read_charge_density_1d(prefix, outdir)

    print(f"\nGenerated post-processing inputs:")
    print(f"  {prefix}_pp.in  — run with: pp.x < {prefix}_pp.in")
    print(f"  {prefix}_avg.in — run with: average.x < {prefix}_avg.in")

    # Check if pp.x exists
    pp_exists = os.system("which pp.x > /dev/null 2>&1") == 0
    avg_exists = os.system("which average.x > /dev/null 2>&1") == 0

    if pp_exists and avg_exists:
        print("\nRunning pp.x...")
        subprocess.run(f"pp.x < {prefix}_pp.in > {prefix}_pp.out 2>&1",
                       shell=True, check=True)

        print("Running average.x...")
        subprocess.run(f"average.x < {prefix}_avg.in > {prefix}_avg.out 2>&1",
                       shell=True, check=True)

        # Parse average.x output
        avg_file = f"avg.dat"
        if os.path.exists(avg_file):
            data = np.loadtxt(avg_file)
            z_ang = data[:, 0]  # z in Angstrom
            rho_z = data[:, 1]  # planar-averaged density

            print(f"\nCharge density profile loaded: {len(z_ang)} points")

            # Layer positions
            layer_positions = np.array([i * layer_spacing for i in range(n_layers)])

            # Compute boundary densities
            print(f"\nBoundary densities (at midpoints between layers):")
            for i in range(n_layers - 1):
                z_mid = (layer_positions[i] + layer_positions[i+1]) / 2
                idx = np.argmin(np.abs(z_ang - z_mid))
                rho_mid = rho_z[idx]
                rho_max = np.max(rho_z)
                print(f"  Layer {i+1}-{i+2} midpoint (z={z_mid:.2f} A): "
                      f"rho = {rho_mid:.4f}, ratio = {rho_mid/rho_max:.4f}")

            # Plot
            fig, axes = plt.subplots(2, 1, figsize=(10, 8))

            ax1 = axes[0]
            ax1.plot(z_ang, rho_z, 'b-', lw=1.5)
            for zl in layer_positions:
                ax1.axvline(zl, color='gray', ls='--', alpha=0.5)
            ax1.set_xlabel('z (Angstrom)')
            ax1.set_ylabel('Planar-averaged charge density')
            ax1.set_title(f'{element} slab: charge density profile')

            # Surface region zoom
            ax2 = axes[1]
            # Focus on the surface region (last 2 layers + vacuum)
            z_surface_start = layer_positions[-3]
            mask_surface = z_ang > z_surface_start
            ax2.plot(z_ang[mask_surface], rho_z[mask_surface], 'b-', lw=1.5)
            for zl in layer_positions:
                if zl > z_surface_start:
                    ax2.axvline(zl, color='gray', ls='--', alpha=0.5)
            ax2.set_xlabel('z (Angstrom)')
            ax2.set_ylabel('Charge density (surface region)')
            ax2.set_title(f'{element} slab: surface charge spillover')

            plt.tight_layout()
            fig_path = f'../figures/fig_slab_{element.lower()}_density.png'
            plt.savefig(fig_path, dpi=200, bbox_inches='tight')
            print(f"\nFigure saved: {fig_path}")
            plt.close()

            return z_ang, rho_z
    else:
        print("\npp.x or average.x not found.")
        print("After running QE, execute:")
        print(f"  pp.x < {prefix}_pp.in > {prefix}_pp.out")
        print(f"  average.x < {prefix}_avg.in > {prefix}_avg.out")
        print("Then re-run this script.")
        return None, None


def generate_orbital_ipr_input(prefix, outdir='./tmp/', n_bands=None):
    """
    Generate pp.x inputs to extract individual KS orbital densities |ψ_n(r)|²
    for IPR calculation.

    This creates one pp.x input per band, extracting |ψ_n|² as a cube file.
    """
    if n_bands is None:
        # Read from QE output to determine number of bands
        out_file = f"{prefix}.out"
        if os.path.exists(out_file):
            with open(out_file) as f:
                for line in f:
                    if 'number of Kohn-Sham states' in line:
                        n_bands = int(line.split('=')[1].strip())
                        break

    if n_bands is None:
        n_bands = 20  # default

    print(f"\nGenerating pp.x inputs for {n_bands} bands...")

    inputs = []
    for i_band in range(1, n_bands + 1):
        pp_input = f"""&INPUTPP
  prefix = '{prefix}'
  outdir = '{outdir}'
  filplot = '{prefix}_psi2_band{i_band}.dat'
  plot_num = 7
  kpoint(1) = 1
  kband(1) = {i_band}
/

&PLOT
  iflag = 3
  output_format = 6
  fileout = '{prefix}_psi2_band{i_band}.cube'
/
"""
        fname = f'{prefix}_pp_band{i_band}.in'
        with open(fname, 'w') as f:
            f.write(pp_input)
        inputs.append(fname)

    print(f"Created {len(inputs)} input files.")
    print(f"Run with: for f in {prefix}_pp_band*.in; do pp.x < $f; done")

    return inputs


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compute_ipr_from_slab.py <element>")
        print("  element: 'al' or 'zn'")
        sys.exit(1)

    element = sys.argv[1].lower()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('tmp', exist_ok=True)

    if element == 'al':
        z, rho = run_analysis('al111', n_layers=7, layer_spacing=2.338,
                              element='Al')
        generate_orbital_ipr_input('al111')

    elif element == 'zn':
        z, rho = run_analysis('zn0001', n_layers=7, layer_spacing=2.474,
                              element='Zn')
        generate_orbital_ipr_input('zn0001')
    else:
        print(f"Unknown element: {element}")
        print("Supported: al, zn")
        sys.exit(1)
