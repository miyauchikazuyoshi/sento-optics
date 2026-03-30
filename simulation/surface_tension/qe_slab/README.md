# QE Slab Calculations

DFT slab calculations using Quantum ESPRESSO to compute
δ_IPR(z) profiles at metal–vacuum interfaces.

## Requirements

- **Quantum ESPRESSO v7.5+**: `conda install -c conda-forge qe`
- **Python**: numpy, scipy, matplotlib (in `.venv/`)
- **PySCF** (for cluster IPR comparison, in `.venv/`)

## Setup

```bash
conda create -n qe python=3.10
conda install -n qe -c conda-forge qe
bash setup.sh  # downloads pseudopotentials
```

## Running

```bash
# Activate QE environment
export PATH=$HOME/miniconda3/envs/qe/bin:$PATH

# Al(111) slab
pw.x < al111_scf.in > al111_scf.out
pp.x < al111_pp.in > al111_pp.out
average.x < al111_avg.in > al111_avg.out
python plot_density_profile.py

# Zn(0001) slab (after fixing pseudopotential)
pw.x < zn0001_scf.in > zn0001_scf.out
```

## Status

- [x] Al(111) SCF converged (19 iterations, E = -276.46 Ry)
- [x] Charge density profile extracted
- [ ] Zn(0001) pseudopotential needs re-download
- [ ] Orbital-resolved IPR calculation
- [ ] Al vs Zn boundary density comparison
