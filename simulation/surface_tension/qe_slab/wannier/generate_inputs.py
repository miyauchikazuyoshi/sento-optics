"""
Generate QE + Wannier90 input files for bulk metals.
Computes MLWFs to quantify electronic delocalization (spread Ω).
"""

import numpy as np

# 4x4x4 uniform k-grid for Wannier90
def gen_kgrid(n):
    """Generate uniform k-grid in crystal coordinates."""
    kpts = []
    w = 1.0 / n**3
    for i in range(n):
        for j in range(n):
            for k in range(n):
                kpts.append((i/n, j/n, k/n, w))
    return kpts

kgrid = gen_kgrid(4)
nk = len(kgrid)  # 64

# ====== Metal definitions ======
metals = {
    'na': {
        'element': 'Na', 'mass': 22.9898,
        'pseudo': 'Na.pbe-spn-kjpaw_psl.1.0.0.UPF',
        'structure': 'bcc', 'a_bohr': 7.9839,  # 4.225 Ang
        'ecutwfc': 30, 'ecutrho': 240,
        'nbnd': 12,
        # Na PP has 2s2p6 3s = 9 valence electrons.
        # We want 3s Wannier only, but need to include semicore for completeness.
        # Wannierize 5 bands: 2s(1) + 2p(3) + 3s(1) = 5
        # Use disentanglement with frozen window around occupied states
        'num_wann': 5,
        'projections': ['Na:s', 'Na:s', 'Na:p'],
        # semicore 2p at ~-25 eV, 3s at ~-3 to +3 eV relative to Ef
        'dis_win_min': -30.0, 'dis_win_max': 15.0,
        'dis_froz_min': -30.0, 'dis_froz_max': 3.0,
    },
    'k': {
        'element': 'K', 'mass': 39.0983,
        'pseudo': 'K.pbe-spn-kjpaw_psl.1.0.0.UPF',
        'structure': 'bcc', 'a_bohr': 9.8724,  # 5.225 Ang
        'ecutwfc': 30, 'ecutrho': 240,
        'nbnd': 16,
        # K PP: 3s2 3p6 4s1 = 9 valence electrons
        # Wannierize 5: 3s(1) + 3p(3) + 4s(1) = 5
        'num_wann': 5,
        'projections': ['K:s', 'K:s', 'K:p'],
        'dis_win_min': -20.0, 'dis_win_max': 15.0,
        'dis_froz_min': -20.0, 'dis_froz_max': 3.0,
    },
    'al': {
        'element': 'Al', 'mass': 26.9815,
        'pseudo': 'Al.pbe-n-kjpaw_psl.1.0.0.UPF',
        'structure': 'fcc', 'a_bohr': 7.6535,  # 4.05 Ang
        'ecutwfc': 30, 'ecutrho': 240,
        'nbnd': 10,
        # Al PP: 3s2 3p1 = 3 valence electrons, no semicore
        # Wannierize 4: s(1) + p(3)
        'num_wann': 4,
        'projections': ['Al:s', 'Al:p'],
        'dis_win_min': -15.0, 'dis_win_max': 25.0,
        'dis_froz_min': -15.0, 'dis_froz_max': 8.0,
    },
    'cu': {
        'element': 'Cu', 'mass': 63.546,
        'pseudo': 'Cu.pbe-dn-kjpaw_psl.1.0.0.UPF',
        'structure': 'fcc', 'a_bohr': 6.8310,  # 3.615 Ang
        'ecutwfc': 40, 'ecutrho': 320,
        'nbnd': 16,
        # Cu PP: 3d9.5 4s1.5 = 11 valence electrons
        # Wannierize 6: d(5) + s(1)
        'num_wann': 6,
        'projections': ['Cu:s', 'Cu:d'],
        'dis_win_min': -12.0, 'dis_win_max': 25.0,
        'dis_froz_min': -12.0, 'dis_froz_max': 12.0,
    },
    'zn': {
        'element': 'Zn', 'mass': 65.38,
        'pseudo': 'Zn.pbe-dn-kjpaw_psl.1.0.0.UPF',
        'structure': 'hcp',
        'ecutwfc': 40, 'ecutrho': 320,
        'nbnd': 24,
        # Zn PP: 3d9.7 4s2 = ~12 valence electrons, 2 atoms/cell
        # Wannierize 12: (d(5) + s(1)) x 2 atoms
        'num_wann': 12,
        'projections': ['Zn:s', 'Zn:d'],
        'dis_win_min': -12.0, 'dis_win_max': 25.0,
        'dis_froz_min': -12.0, 'dis_froz_max': 12.0,
    },
}

def get_cell_vectors_ang(m):
    """Get primitive cell vectors in Angstrom."""
    if m['structure'] == 'bcc':
        a = m['a_bohr'] * 0.529177
        # QE ibrav=3 convention
        v1 = (a/2, a/2, a/2)
        v2 = (-a/2, a/2, a/2)
        v3 = (-a/2, -a/2, a/2)
    elif m['structure'] == 'fcc':
        a = m['a_bohr'] * 0.529177
        # QE ibrav=2 convention
        v1 = (-a/2, 0, a/2)
        v2 = (0, a/2, a/2)
        v3 = (-a/2, a/2, 0)
    else:  # hcp
        a = 2.665
        c = 4.947
        v1 = (a, 0, 0)
        v2 = (-a/2, a*np.sqrt(3)/2, 0)
        v3 = (0, 0, c)
    return v1, v2, v3

def write_cell_block(f, m):
    """Write CELL_PARAMETERS block."""
    v1, v2, v3 = get_cell_vectors_ang(m)
    f.write("CELL_PARAMETERS angstrom\n")
    f.write(f"  {v1[0]:.10f}  {v1[1]:.10f}  {v1[2]:.10f}\n")
    f.write(f"  {v2[0]:.10f}  {v2[1]:.10f}  {v2[2]:.10f}\n")
    f.write(f"  {v3[0]:.10f}  {v3[1]:.10f}  {v3[2]:.10f}\n")

def write_scf(name, m):
    """Write SCF input."""
    nat = 2 if m['structure'] == 'hcp' else 1
    with open(f'{name}_scf.in', 'w') as f:
        f.write(f"""&CONTROL
  calculation = 'scf'
  prefix      = '{name}_bulk'
  outdir      = './tmp_{name}/'
  pseudo_dir  = '../pseudo/'
/
&SYSTEM
  ibrav       = 0
  nat         = {nat}
  ntyp        = 1
  ecutwfc     = {m['ecutwfc']}.0
  ecutrho     = {m['ecutrho']}.0
  occupations = 'smearing'
  smearing    = 'mp'
  degauss     = 0.02
  nosym       = .true.
/
&ELECTRONS
  conv_thr = 1.0d-8
/
ATOMIC_SPECIES
  {m['element']}  {m['mass']}  {m['pseudo']}

""")
        write_cell_block(f, m)
        f.write("\n")
        if m['structure'] == 'hcp':
            f.write(f"ATOMIC_POSITIONS crystal\n")
            f.write(f"  Zn  0.333333  0.666667  0.25\n")
            f.write(f"  Zn  0.666667  0.333333  0.75\n")
        else:
            f.write(f"ATOMIC_POSITIONS crystal\n")
            f.write(f"  {m['element']}  0.0  0.0  0.0\n")
        f.write(f"\nK_POINTS automatic\n  8 8 8 0 0 0\n")


def write_nscf(name, m):
    """Write NSCF input with explicit k-grid."""
    nat = 2 if m['structure'] == 'hcp' else 1
    with open(f'{name}_nscf.in', 'w') as f:
        f.write(f"""&CONTROL
  calculation = 'bands'
  prefix      = '{name}_bulk'
  outdir      = './tmp_{name}/'
  pseudo_dir  = '../pseudo/'
/
&SYSTEM
  ibrav       = 0
  nat         = {nat}
  ntyp        = 1
  ecutwfc     = {m['ecutwfc']}.0
  ecutrho     = {m['ecutrho']}.0
  occupations = 'smearing'
  smearing    = 'mp'
  degauss     = 0.02
  nosym       = .true.
  nbnd        = {m['nbnd']}
/
&ELECTRONS
  conv_thr = 1.0d-8
/
ATOMIC_SPECIES
  {m['element']}  {m['mass']}  {m['pseudo']}

""")
        write_cell_block(f, m)
        f.write("\n")
        if m['structure'] == 'hcp':
            f.write(f"ATOMIC_POSITIONS crystal\n")
            f.write(f"  Zn  0.333333  0.666667  0.25\n")
            f.write(f"  Zn  0.666667  0.333333  0.75\n")
        else:
            f.write(f"ATOMIC_POSITIONS crystal\n")
            f.write(f"  {m['element']}  0.0  0.0  0.0\n")
        # Write explicit k-points
        f.write(f"\nK_POINTS crystal\n{nk}\n")
        for kx, ky, kz, w in kgrid:
            f.write(f"  {kx:.4f}  {ky:.4f}  {kz:.4f}  {w:.8f}\n")


def write_wannier_win(name, m):
    """Write wannier90.win file."""
    with open(f'{name}.win', 'w') as f:
        f.write(f"num_wann = {m['num_wann']}\n")
        f.write(f"num_bands = {m['nbnd']}\n\n")

        # Disentanglement
        f.write(f"dis_win_min  = {m['dis_win_min']}\n")
        f.write(f"dis_win_max  = {m['dis_win_max']}\n")
        f.write(f"dis_froz_min = {m['dis_froz_min']}\n")
        f.write(f"dis_froz_max = {m['dis_froz_max']}\n")
        f.write(f"dis_num_iter = 200\n")
        f.write(f"dis_mix_ratio = 0.5\n\n")

        f.write(f"num_iter = 200\n")
        f.write(f"num_print_cycles = 50\n\n")

        # Projections
        f.write("begin projections\n")
        for proj in m['projections']:
            f.write(f"  {proj}\n")
        f.write("end projections\n\n")

        # Unit cell - must match QE exactly
        v1, v2, v3 = get_cell_vectors_ang(m)
        f.write("begin unit_cell_cart\nang\n")
        f.write(f"  {v1[0]:.10f}  {v1[1]:.10f}  {v1[2]:.10f}\n")
        f.write(f"  {v2[0]:.10f}  {v2[1]:.10f}  {v2[2]:.10f}\n")
        f.write(f"  {v3[0]:.10f}  {v3[1]:.10f}  {v3[2]:.10f}\n")
        f.write("end unit_cell_cart\n\n")

        # Atoms
        nat = 2 if m['structure'] == 'hcp' else 1
        f.write("begin atoms_frac\n")
        if m['structure'] == 'hcp':
            f.write(f"  {m['element']}  0.333333  0.666667  0.25\n")
            f.write(f"  {m['element']}  0.666667  0.333333  0.75\n")
        else:
            f.write(f"  {m['element']}  0.0  0.0  0.0\n")
        f.write("end atoms_frac\n\n")

        # K-points
        f.write(f"mp_grid = 4 4 4\n\n")
        f.write("begin kpoints\n")
        for kx, ky, kz, w in kgrid:
            f.write(f"  {kx:.4f}  {ky:.4f}  {kz:.4f}\n")
        f.write("end kpoints\n")


def write_pw2wannier(name, m):
    """Write pw2wannier90 input."""
    with open(f'{name}_pw2wan.in', 'w') as f:
        f.write(f"""&inputpp
  outdir   = './tmp_{name}/'
  prefix   = '{name}_bulk'
  seedname = '{name}'
  write_mmn = .true.
  write_amn = .true.
  write_unk = .false.
/
""")


# Generate all inputs
for name, m in metals.items():
    write_scf(name, m)
    write_nscf(name, m)
    write_wannier_win(name, m)
    write_pw2wannier(name, m)
    print(f"{name}: all input files generated")

print("\nDone! Run: bash run_all_wannier.sh")
