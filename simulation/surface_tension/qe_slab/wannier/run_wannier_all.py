"""
Generate Wannier90 .win files from QE XML and run Wannier90 for all metals.
Extracts MLWF spread as a measure of electronic delocalization.
"""

import xml.etree.ElementTree as ET
import numpy as np
import subprocess
import os

# Metal configurations after checking actual band energies
# Fermi energies: Na=1.67, K=1.95, Al=7.84, Cu=12.65
metals = {
    'na': {
        'prefix': 'na_bulk', 'tmpdir': 'tmp_na',
        'num_wann': 1, 'nbnd_calc': 12,
        'exclude_bands': '1-4',  # semicore 2s2p
        'nbnd_eff': 8,
        'projections': ['f=0.0,0.0,0.0:s'],  # single s at origin
        'dis_froz_max': 2.0,
    },
    'k': {
        'prefix': 'k_bulk', 'tmpdir': 'tmp_k',
        'num_wann': 1, 'nbnd_calc': 16,
        'exclude_bands': '1-4',  # semicore 3s3p
        'nbnd_eff': 12,
        'projections': ['f=0.0,0.0,0.0:s'],
        'dis_froz_max': None,  # no frozen window to avoid segfault
    },
    'al': {
        'prefix': 'al_bulk', 'tmpdir': 'tmp_al',
        'num_wann': 1, 'nbnd_calc': 10,
        'exclude_bands': None,
        'nbnd_eff': 10,
        'projections': ['f=0.0,0.0,0.0:s'],
        'dis_froz_max': 3.0,  # lowered: 2 bands at 3.27 eV at k-point 3
    },
    'cu': {
        'prefix': 'cu_bulk', 'tmpdir': 'tmp_cu',
        'num_wann': 6, 'nbnd_calc': 16,
        'exclude_bands': None,
        'nbnd_eff': 16,
        'projections': ['f=0.0,0.0,0.0:s;d'],
        'dis_froz_max': 13.0,
    },
    'zn': {
        'prefix': 'zn_bulk', 'tmpdir': 'tmp_zn',
        'num_wann': 12, 'nbnd_calc': 24,
        'exclude_bands': None,
        'nbnd_eff': 24,
        'projections': [
            'f=0.333333,0.666667,0.25:s;d',
            'f=0.666667,0.333333,0.75:s;d',
        ],
        'dis_froz_max': 7.0,  # 13 bands below 12eV, only 12 WFs
    },
}

# 4x4x4 k-grid
kgrid = []
for i in range(4):
    for j in range(4):
        for k in range(4):
            kgrid.append((i/4, j/4, k/4))

def get_lattice_from_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    cell = root.find('.//atomic_structure/cell')
    vectors = []
    for tag in ['a1', 'a2', 'a3']:
        vals = cell.find(tag).text.split()
        vectors.append([float(v) for v in vals])
    return vectors

def get_atoms_from_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    atoms = []
    for atom in root.findall('.//atomic_structure/atomic_positions/atom'):
        name = atom.get('name')
        coords = [float(x) for x in atom.text.split()]
        atoms.append((name, coords))
    return atoms

def write_win(name, m):
    xmlfile = f"{m['tmpdir']}/{m['prefix']}.xml"
    lat = get_lattice_from_xml(xmlfile)
    atoms = get_atoms_from_xml(xmlfile)
    lat_matrix = np.array(lat)

    with open(f'{name}.win', 'w') as f:
        f.write(f"num_wann = {m['num_wann']}\n")
        f.write(f"num_bands = {m['nbnd_eff']}\n\n")

        if m['exclude_bands']:
            f.write(f"exclude_bands = {m['exclude_bands']}\n\n")

        f.write(f"dis_win_min  = -30.0\n")
        f.write(f"dis_win_max  = 50.0\n")
        if m['dis_froz_max'] is not None:
            f.write(f"dis_froz_min = -30.0\n")
            f.write(f"dis_froz_max = {m['dis_froz_max']}\n")
        f.write(f"dis_num_iter = 1000\n")
        f.write(f"dis_conv_tol = 1.0e-3\n")
        f.write(f"dis_mix_ratio = 0.5\n\n")

        f.write(f"num_iter = 500\n")
        f.write(f"num_print_cycles = 100\n\n")

        f.write("begin projections\n")
        for proj in m['projections']:
            f.write(f"  {proj}\n")
        f.write("end projections\n\n")

        f.write("begin unit_cell_cart\nbohr\n")
        for v in lat:
            f.write(f"  {v[0]:.16E}  {v[1]:.16E}  {v[2]:.16E}\n")
        f.write("end unit_cell_cart\n\n")

        f.write("begin atoms_frac\n")
        for aname, coords in atoms:
            frac = np.linalg.solve(lat_matrix.T, coords)
            f.write(f"  {aname}  {frac[0]:.10f}  {frac[1]:.10f}  {frac[2]:.10f}\n")
        f.write("end atoms_frac\n\n")

        f.write("mp_grid = 4 4 4\n\n")
        f.write("begin kpoints\n")
        for kx, ky, kz in kgrid:
            f.write(f"  {kx:.4f}  {ky:.4f}  {kz:.4f}\n")
        f.write("end kpoints\n")

def run_wannier(name, m):
    print(f"\n{'='*50}")
    print(f"  {name.upper()}")
    print(f"{'='*50}")

    write_win(name, m)

    # Clean old files
    for ext in ['nnkp', 'amn', 'mmn', 'eig', 'chk', 'wout']:
        f = f'{name}.{ext}'
        if os.path.exists(f):
            os.remove(f)

    # Wannier90 -pp
    print("  wannier90 -pp...")
    r = subprocess.run(['wannier90.x', '-pp', name], capture_output=True, text=True)

    # pw2wannier90
    print("  pw2wannier90...")
    with open(f'{name}_pw2wan.in') as fin:
        r = subprocess.run(['pw2wannier90.x'], stdin=fin, capture_output=True, text=True)
    if 'Error' in r.stdout or 'Error' in r.stderr:
        print(f"  ERROR in pw2wannier90: {r.stdout[-200:]}")
        return None

    # Wannier90
    print("  wannier90...")
    r = subprocess.run(['wannier90.x', name], capture_output=True, text=True)

    # Extract spread
    try:
        with open(f'{name}.wout') as f:
            lines = f.readlines()
        spreads = []
        for line in lines:
            if 'WF centre and spread' in line:
                spread = float(line.strip().split()[-1])
                spreads.append(spread)
        if spreads:
            # Take the last set of spreads (after minimization)
            n = m['num_wann']
            final_spreads = spreads[-n:]
            avg_spread = np.mean(final_spreads)
            print(f"  Spreads: {final_spreads}")
            print(f"  Average spread: {avg_spread:.4f} Ang^2")
            return avg_spread, final_spreads
        else:
            print("  No spread values found in .wout")
            return None
    except Exception as e:
        print(f"  Error reading .wout: {e}")
        return None

# Run all metals
results = {}
for name, m in metals.items():
    xmlfile = f"{m['tmpdir']}/{m['prefix']}.xml"
    if not os.path.exists(xmlfile):
        print(f"\n{name}: XML not found, skipping")
        continue
    result = run_wannier(name, m)
    if result:
        results[name] = result

print(f"\n{'='*50}")
print("SUMMARY: MLWF Spreads")
print(f"{'='*50}")
for name, (avg, spreads) in results.items():
    m = metals[name]
    etype = 'sp' if name in ['na', 'k', 'al'] else 'd'
    print(f"  {name.upper():>3} ({etype}): avg spread = {avg:.4f} Ang^2, "
          f"per WF: {[f'{s:.3f}' for s in spreads]}")
