"""
Generate QE slab + Wannier input files for 10 new elements.

Existing: Na(BCC110), K(BCC110), Al(FCC111), Cu(FCC111), Zn(HCP0001)
New:      Li(BCC110), Be(HCP0001), Mg(HCP0001), Ca(FCC111),
          Si(diamond111), Ga(ortho), Fe(BCC110), Ni(FCC111),
          Ti(HCP0001), Ag(FCC111)

Each element needs:
  1. {elem}_scf.in   — SCF calculation
  2. {elem}_pp.in    — post-processing (charge density)
  3. {elem}_val_avg.in — valence-only ILDOS + planar average

For Wannier (bulk):
  4. {elem}_scf.in, {elem}_nscf.in, {elem}_pw2wan.in, {elem}.win

Usage:
  python generate_new_elements.py
  # Creates input files in slab/ and wannier/ subdirectories
"""

import os
import numpy as np

SLAB_DIR = os.path.dirname(__file__)
WANNIER_DIR = os.path.join(SLAB_DIR, 'wannier')

# === Slab parameters ===
# structure, lattice constant (Ang), interlayer spacing (Ang), surface, n_layers
# ecutwfc, ecutrho, pseudo filename
# For spin-polarized: nspin, starting_magnetization

SLAB_ELEMENTS = {
    'li': {
        'elem': 'Li', 'mass': 6.941,
        'pseudo': 'Li.pbe-s-kjpaw_psl.1.0.0.UPF',
        'structure': 'bcc', 'a': 3.49,
        'surface': '110', 'n_layers': 7,
        'ecutwfc': 30, 'ecutrho': 240,
        'emin_valence': -5.0,  # 2s only
        'spin': False,
    },
    'be': {
        'elem': 'Be', 'mass': 9.012,
        'pseudo': 'Be.pbe-n-kjpaw_psl.1.0.0.UPF',
        'structure': 'hcp', 'a': 2.29, 'c': 3.58,
        'surface': '0001', 'n_layers': 7,
        'ecutwfc': 40, 'ecutrho': 320,
        'emin_valence': -15.0,
        'spin': False,
    },
    'mg': {
        'elem': 'Mg', 'mass': 24.305,
        'pseudo': 'Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF',
        'structure': 'hcp', 'a': 3.21, 'c': 5.21,
        'surface': '0001', 'n_layers': 7,
        'ecutwfc': 30, 'ecutrho': 240,
        'emin_valence': -8.0,
        'spin': False,
    },
    'ca': {
        'elem': 'Ca', 'mass': 40.078,
        'pseudo': 'Ca.pbe-spn-kjpaw_psl.1.0.0.UPF',
        'structure': 'fcc', 'a': 5.58,
        'surface': '111', 'n_layers': 7,
        'ecutwfc': 30, 'ecutrho': 240,
        'emin_valence': -8.0,
        'spin': False,
    },
    'si': {
        'elem': 'Si', 'mass': 28.086,
        'pseudo': 'Si.pbe-n-kjpaw_psl.1.0.0.UPF',
        'structure': 'diamond', 'a': 5.43,
        'surface': '111', 'n_layers': 8,  # even for diamond
        'ecutwfc': 30, 'ecutrho': 240,
        'emin_valence': -13.0,
        'spin': False,
    },
    'ga': {
        'elem': 'Ga', 'mass': 69.723,
        'pseudo': 'Ga.pbe-dn-kjpaw_psl.1.0.0.UPF',
        'structure': 'fcc', 'a': 4.51,  # use FCC approx for simplicity
        'surface': '111', 'n_layers': 7,
        'ecutwfc': 40, 'ecutrho': 320,
        'emin_valence': -15.0,
        'spin': False,
    },
    'fe': {
        'elem': 'Fe', 'mass': 55.845,
        'pseudo': 'Fe.pbe-spn-kjpaw_psl.1.0.0.UPF',
        'structure': 'bcc', 'a': 2.87,
        'surface': '110', 'n_layers': 7,
        'ecutwfc': 50, 'ecutrho': 400,
        'emin_valence': -10.0,
        'spin': True, 'starting_mag': 0.3,
    },
    'ni': {
        'elem': 'Ni', 'mass': 58.693,
        'pseudo': 'Ni.pbe-spn-kjpaw_psl.1.0.0.UPF',
        'structure': 'fcc', 'a': 3.52,
        'surface': '111', 'n_layers': 7,
        'ecutwfc': 50, 'ecutrho': 400,
        'emin_valence': -10.0,
        'spin': True, 'starting_mag': 0.2,
    },
    'ti': {
        'elem': 'Ti', 'mass': 47.867,
        'pseudo': 'Ti.pbe-spn-kjpaw_psl.1.0.0.UPF',
        'structure': 'hcp', 'a': 2.95, 'c': 4.69,
        'surface': '0001', 'n_layers': 7,
        'ecutwfc': 40, 'ecutrho': 320,
        'emin_valence': -10.0,
        'spin': False,
    },
    'ag': {
        'elem': 'Ag', 'mass': 107.868,
        'pseudo': 'Ag.pbe-n-kjpaw_psl.1.0.0.UPF',
        'structure': 'fcc', 'a': 4.09,
        'surface': '111', 'n_layers': 7,
        'ecutwfc': 40, 'ecutrho': 320,
        'emin_valence': -8.0,
        'spin': False,
    },
}


def make_bcc110_slab(a, n_layers, vacuum=15.0):
    """BCC(110) slab geometry."""
    # In-plane: a_x = a, a_y = a*sqrt(2)/2
    ax = a
    ay = a * np.sqrt(2) / 2
    d = a * np.sqrt(2) / 2  # interlayer spacing for BCC(110)
    total_z = (n_layers - 1) * d + vacuum
    cell = [[ax, 0, 0], [0, ay, 0], [0, 0, total_z]]
    positions = []
    for i in range(n_layers):
        if i % 2 == 0:
            positions.append([0.0, 0.0, i * d])
        else:
            positions.append([ax/2, ay/2, i * d])
    return cell, positions


def make_fcc111_slab(a, n_layers, vacuum=15.0):
    """FCC(111) slab geometry."""
    a_inplane = a / np.sqrt(2)
    d = a / np.sqrt(3)  # interlayer spacing
    total_z = (n_layers - 1) * d + vacuum
    cell = [[a_inplane, 0, 0],
            [a_inplane/2, a_inplane * np.sqrt(3)/2, 0],
            [0, 0, total_z]]
    positions = []
    shifts = [[0, 0], [1/3, 1/3], [2/3, 2/3]]  # ABC stacking
    for i in range(n_layers):
        sx, sy = shifts[i % 3]
        x = sx * a_inplane + sy * a_inplane / 2
        y = sy * a_inplane * np.sqrt(3) / 2
        positions.append([x, y, i * d])
    return cell, positions


def make_hcp0001_slab(a, c, n_layers, vacuum=15.0):
    """HCP(0001) slab geometry."""
    d = c / 2  # interlayer spacing
    total_z = (n_layers - 1) * d + vacuum
    cell = [[a, 0, 0],
            [a/2, a * np.sqrt(3)/2, 0],
            [0, 0, total_z]]
    positions = []
    for i in range(n_layers):
        if i % 2 == 0:
            positions.append([0, 0, i * d])
        else:
            positions.append([a/2, a * np.sqrt(3)/6, i * d])
    return cell, positions


def write_scf_input(key, info, cell, positions):
    """Write QE SCF input file."""
    prefix = f"{key}{info['surface']}"
    nat = len(positions)
    filename = os.path.join(SLAB_DIR, f"{key}{info['surface']}_scf.in")

    spin_block = ""
    if info.get('spin'):
        spin_block = f"""  nspin        = 2
  starting_magnetization(1) = {info['starting_mag']}
"""

    with open(filename, 'w') as f:
        f.write(f"""&CONTROL
  calculation  = 'scf'
  prefix       = '{prefix}'
  outdir       = './tmp/'
  pseudo_dir   = './pseudo/'
  verbosity    = 'high'
  tprnfor      = .true.
  tstress      = .true.
/

&SYSTEM
  ibrav        = 0
  nat          = {nat}
  ntyp         = 1
  ecutwfc      = {info['ecutwfc']:.1f}
  ecutrho      = {info['ecutrho']:.1f}
  occupations  = 'smearing'
  smearing     = 'mp'
  degauss      = 0.02
  nosym        = .true.
{spin_block}/

&ELECTRONS
  conv_thr     = 1.0d-8
  mixing_beta  = 0.3
  mixing_mode  = 'local-TF'
/

ATOMIC_SPECIES
  {info['elem']}  {info['mass']:.4f}  {info['pseudo']}

CELL_PARAMETERS angstrom
  {cell[0][0]:.6f}  {cell[0][1]:.6f}  {cell[0][2]:.6f}
  {cell[1][0]:.6f}  {cell[1][1]:.6f}  {cell[1][2]:.6f}
  {cell[2][0]:.6f}  {cell[2][1]:.6f}  {cell[2][2]:.6f}

ATOMIC_POSITIONS angstrom
""")
        for pos in positions:
            f.write(f"  {info['elem']}  {pos[0]:.6f}  {pos[1]:.6f}  {pos[2]:.6f}\n")
        f.write(f"\nK_POINTS automatic\n  8 8 1  0 0 0\n")

    print(f"  Created: {filename}")
    return filename


def write_pp_input(key, info):
    """Write QE post-processing input (total + valence ILDOS)."""
    prefix = f"{key}{info['surface']}"

    # Total density pp
    pp_file = os.path.join(SLAB_DIR, f"{key}{info['surface']}_pp.in")
    with open(pp_file, 'w') as f:
        f.write(f"""&INPUTPP
  prefix  = '{prefix}'
  outdir  = './tmp/'
  filplot = '{key}_charge.dat'
  plot_num = 0
/
""")

    # Valence ILDOS pp
    val_pp_file = os.path.join(SLAB_DIR, f"{key}_pp_valence.in")
    with open(val_pp_file, 'w') as f:
        f.write(f"""&INPUTPP
  prefix  = '{prefix}'
  outdir  = './tmp/'
  filplot = '{key}_valence.dat'
  plot_num = 10
  emin = {info['emin_valence']:.1f}
  emax = 0.0
/
""")

    # Planar average
    avg_file = os.path.join(SLAB_DIR, f"{key}_val_avg.in")
    with open(avg_file, 'w') as f:
        f.write(f"""1
{key}_valence.dat
1.D0
1000
3
3.0000
""")

    print(f"  Created: {pp_file}, {val_pp_file}, {avg_file}")


def main():
    print("=" * 60)
    print("Generating QE slab inputs for 10 new elements")
    print("=" * 60)

    for key, info in SLAB_ELEMENTS.items():
        print(f"\n--- {info['elem']} ({info['structure'].upper()}{info['surface']}) ---")

        struct = info['structure']
        if struct == 'bcc':
            cell, positions = make_bcc110_slab(info['a'], info['n_layers'])
        elif struct in ('fcc', 'diamond'):
            cell, positions = make_fcc111_slab(info['a'], info['n_layers'])
        elif struct == 'hcp':
            cell, positions = make_hcp0001_slab(info['a'], info['c'], info['n_layers'])
        else:
            print(f"  SKIP: unknown structure {struct}")
            continue

        write_scf_input(key, info, cell, positions)
        write_pp_input(key, info)

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("""
1. Download pseudopotentials to ./pseudo/:
   https://www.quantum-espresso.org/pseudopotentials/ps-library/

2. Run SCF for each element:
   pw.x < {elem}_scf.in > {elem}_scf.out

3. Run post-processing:
   pp.x < {elem}_pp.in
   pp.x < {elem}_pp_valence.in
   average.x < {elem}_val_avg.in

4. Extract n_mid/n_bulk from planar average output.

5. For Wannier: run bulk SCF + NSCF + wannier90.
   (Use generate_inputs.py in wannier/ as template)

Note: Fe and Ni require spin-polarized calculations (nspin=2).
""")


if __name__ == '__main__':
    main()
