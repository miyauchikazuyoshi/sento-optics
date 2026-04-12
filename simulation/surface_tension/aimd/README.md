# AIMD Liquid Metal Simulations

Ab initio molecular dynamics (Born-Oppenheimer MD) simulations of liquid metals
using Quantum ESPRESSO `pw.x`. These calculations provide the liquid-state
electronic structure needed to evaluate the electronic delocalization descriptor
delta for the surface tension study.

## Systems

| Element | T (K) | Density (g/cm^3) | Box (Ang) | Box (bohr) | N_atoms | ecutwfc (Ry) | dt (a.u.) | nstep |
|---------|--------|-------------------|-----------|------------|---------|--------------|-----------|-------|
| Na      | 471    | 0.927             | 13.81     | 26.10      | 64      | 30           | 40        | 5000  |
| Al      | 1033   | 2.375             | 10.65     | 20.12      | 64      | 40           | 20        | 5000  |
| Cu      | 1458   | 8.02              | 9.44      | 17.84      | 64      | 50           | 20        | 10000 |
| Zn      | 793    | 6.57              | 10.19     | 19.25      | 64      | 50           | 20        | 5000  |

All temperatures are approximately T_m + 100 K (well above melting point).

## File Structure

```
generate_liquid_config.py   # Python script to generate random liquid configs
run_aimd.sh                 # Master run script (sequential SCF -> MD)
{El}_liquid_scf.in          # Initial SCF to obtain wavefunctions
{El}_liquid_md.in           # Born-Oppenheimer MD production run
{El}_positions.dat          # Generated atomic positions (fractional coords)
```

## Calculation Protocol

1. **Generate initial configuration**: `python generate_liquid_config.py`
   - Places 64 atoms randomly in a cubic cell
   - Enforces minimum inter-atomic distances (element-dependent)
   - Outputs fractional coordinates

2. **Initial SCF** (`{El}_liquid_scf.in`):
   - `calculation = 'scf'` with the random liquid configuration
   - Produces converged wavefunctions and charge density
   - Output saved in `./tmp/`

3. **BO-MD production** (`{El}_liquid_md.in`):
   - `calculation = 'md'`, `ion_dynamics = 'verlet'`
   - Andersen thermostat (`ion_temperature = 'andersen'`)
   - `nraise = 50` controls collision frequency
   - Restarts from SCF wavefunctions

## Computational Details

- **Functional**: PBE (GGA)
- **Pseudopotentials**: PAW (from pslibrary), located in `../qe_slab/pseudo/`
- **K-points**: Gamma-only (justified by large 64-atom supercell)
- **Smearing**: Marzari-Vanderbilt (cold smearing), degauss = 0.02 Ry
- **SCF convergence**: conv_thr = 1.0e-6 Ry (relaxed for MD efficiency)
- **Symmetry**: Disabled (nosym = .true., noinv = .true.)
- **Electron solver**: Davidson diagonalization, mixing_beta = 0.3

## Running

```bash
# Generate random liquid configurations (already done)
python generate_liquid_config.py

# Run all elements sequentially
./run_aimd.sh

# Run selected elements only
./run_aimd.sh Na Al

# Adjust parallelism
NPROCS=32 ./run_aimd.sh Cu
```

## Expected Outputs

- `tmp/{El}_liquid.save/` -- Wavefunctions and charge density
- `logs/{El}_liquid_md.out` -- MD trajectory, energies, forces
- From the MD output, extract:
  - Pair distribution function g(r)
  - Mean-square displacement (diffusion)
  - Electronic density of states at each snapshot
  - IPR / Omega delocalization measures from wavefunctions

## Resource Estimates

| Element | Wall time per SCF step | Total MD wall time (est.) |
|---------|----------------------|--------------------------|
| Na      | ~1 min (16 cores)    | ~3-4 days                |
| Al      | ~2 min               | ~7 days                  |
| Cu      | ~10 min              | ~70 days (GPU recommended)|
| Zn      | ~8 min               | ~28 days                 |

Cu and Zn are computationally expensive due to d-electrons. Consider:
- Using GPU-accelerated QE
- Reducing nstep for initial tests
- Running on HPC clusters

## Notes

- The initial random configuration is NOT equilibrated. The first ~500-1000
  MD steps should be treated as equilibration and discarded from analysis.
- For better initial configs, consider using classical MD (e.g., LAMMPS with
  EAM potentials) to pre-equilibrate, then use those positions as QE input.
- Andersen thermostat disrupts dynamics; for transport properties (diffusion),
  switch to NVE after equilibration or use Nose-Hoover.
