"""
Generate Wannier90 .win files using exact lattice vectors from QE XML.
Avoids floating-point mismatch between QE and Wannier90.
"""

import xml.etree.ElementTree as ET
import numpy as np
import os

metals = {
    'na': {
        'prefix': 'na_bulk', 'tmpdir': 'tmp_na',
        'element': 'Na', 'nat': 1,
        'num_wann': 1, 'nbnd': 12,
        'exclude_bands': '1-4',  # 2s, 2p semicore
        'projections': ['Na: s'],
        'dis_win_min': -5.0, 'dis_win_max': 20.0,
        'dis_froz_min': -5.0, 'dis_froz_max': 5.0,
    },
    'k': {
        'prefix': 'k_bulk', 'tmpdir': 'tmp_k',
        'element': 'K', 'nat': 1,
        'num_wann': 1, 'nbnd': 16,
        'exclude_bands': '1-4',  # 3s, 3p semicore
        'projections': ['K: s'],
        'dis_win_min': -5.0, 'dis_win_max': 20.0,
        'dis_froz_min': -5.0, 'dis_froz_max': 5.0,
    },
    'al': {
        'prefix': 'al_bulk', 'tmpdir': 'tmp_al',
        'element': 'Al', 'nat': 1,
        'num_wann': 4, 'nbnd': 10,
        'exclude_bands': None,  # no semicore
        'projections': ['Al: sp3'],
        'dis_win_min': -15.0, 'dis_win_max': 30.0,
        'dis_froz_min': -15.0, 'dis_froz_max': 10.0,
    },
    'cu': {
        'prefix': 'cu_bulk', 'tmpdir': 'tmp_cu',
        'element': 'Cu', 'nat': 1,
        'num_wann': 6, 'nbnd': 16,
        'exclude_bands': None,
        'projections': ['Cu: s', 'Cu: d'],
        'dis_win_min': -12.0, 'dis_win_max': 30.0,
        'dis_froz_min': -12.0, 'dis_froz_max': 15.0,
    },
    'zn': {
        'prefix': 'zn_bulk', 'tmpdir': 'tmp_zn',
        'element': 'Zn', 'nat': 2,
        'num_wann': 12, 'nbnd': 24,
        'exclude_bands': None,
        'projections': ['Zn: s', 'Zn: d'],
        'dis_win_min': -12.0, 'dis_win_max': 30.0,
        'dis_froz_min': -12.0, 'dis_froz_max': 15.0,
    },
}

# 4x4x4 k-grid
kgrid = []
for i in range(4):
    for j in range(4):
        for k in range(4):
            kgrid.append((i/4, j/4, k/4))

def get_lattice_from_xml(xmlfile):
    """Extract lattice vectors in bohr from QE XML."""
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    cell = root.find('.//atomic_structure/cell')
    vectors = []
    for tag in ['a1', 'a2', 'a3']:
        vals = cell.find(tag).text.split()
        vectors.append([float(v) for v in vals])
    return vectors

def get_atoms_from_xml(xmlfile):
    """Extract atomic positions in crystal coords from QE XML."""
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    atoms = []
    for atom in root.findall('.//atomic_structure/atomic_positions/atom'):
        name = atom.get('name')
        coords = [float(x) for x in atom.text.split()]
        atoms.append((name, coords))
    return atoms

bohr2ang = 0.529177249

for name, m in metals.items():
    xmlfile = f"{m['tmpdir']}/{m['prefix']}.xml"
    if not os.path.exists(xmlfile):
        print(f"{name}: XML not found ({xmlfile}), skipping")
        continue

    lat = get_lattice_from_xml(xmlfile)

    with open(f'{name}.win', 'w') as f:
        f.write(f"num_wann = {m['num_wann']}\n")
        f.write(f"num_bands = {m['nbnd']}\n\n")

        if m['exclude_bands']:
            f.write(f"exclude_bands = {m['exclude_bands']}\n\n")

        f.write(f"dis_win_min  = {m['dis_win_min']}\n")
        f.write(f"dis_win_max  = {m['dis_win_max']}\n")
        f.write(f"dis_froz_min = {m['dis_froz_min']}\n")
        f.write(f"dis_froz_max = {m['dis_froz_max']}\n")
        f.write(f"dis_num_iter = 200\n")
        f.write(f"dis_mix_ratio = 0.5\n\n")

        f.write(f"num_iter = 500\n")
        f.write(f"num_print_cycles = 100\n\n")

        f.write("begin projections\n")
        for proj in m['projections']:
            f.write(f"  {proj}\n")
        f.write("end projections\n\n")

        # Use BOHR to match QE exactly
        f.write("begin unit_cell_cart\nbohr\n")
        for v in lat:
            f.write(f"  {v[0]:.16E}  {v[1]:.16E}  {v[2]:.16E}\n")
        f.write("end unit_cell_cart\n\n")

        # Atoms in fractional coordinates
        f.write("begin atoms_frac\n")
        atoms = get_atoms_from_xml(xmlfile)
        for aname, coords in atoms:
            # Convert cartesian (bohr) to fractional
            lat_matrix = np.array(lat)
            frac = np.linalg.solve(lat_matrix.T, coords)
            f.write(f"  {aname}  {frac[0]:.8f}  {frac[1]:.8f}  {frac[2]:.8f}\n")
        f.write("end atoms_frac\n\n")

        f.write("mp_grid = 4 4 4\n\n")
        f.write("begin kpoints\n")
        for kx, ky, kz in kgrid:
            f.write(f"  {kx:.4f}  {ky:.4f}  {kz:.4f}\n")
        f.write("end kpoints\n")

    print(f"{name}: .win generated from {xmlfile}")

print("\nDone!")
