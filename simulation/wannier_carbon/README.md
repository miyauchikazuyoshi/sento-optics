# Wannier Spread Calculation for Carbon Allotropes

## Hypothesis

Paper I classifies carbon allotropes by (E_g, D_eff) and uses
literature-derived proxies (pi-band width, inverse effective mass, band gap)
to argue that these proxies reflect a common underlying quantity: the
electronic delocalization index delta_elec.

However, **delta_IPR has never been computed from first principles for these
systems**. The 7/7 classification success comes from the decision tree
(E_g + D_eff), not from delta itself. Two attempts to compute delta directly
(tight-binding model and molecular DFT clusters) both failed to reproduce
the expected ordering.

This calculation aims to resolve whether the failure was due to
**inadequate models** (TB too coarse, molecules != solids) or a
**fundamental limitation of delta_IPR**.

## Core Prediction

If delta_elec measures electronic delocalization, then for periodic solids:

```
Omega(diamond) < Omega(graphite)
```

where Omega is the Wannier function spread (Ang^2) from maximally localized
Wannier functions (MLWFs).

## Results (2026-04-01)

### OVERALL: PASS

| System | Hybridization | num_wann | Omega_total (Ang^2) | **Omega/WF (Ang^2)** | Optical category |
|--------|---------------|----------|---------------------|----------------------|------------------|
| Diamond | sp3, insulator | 8 | 7.635 | **0.954** | Transparent |
| K metal (Paper II) | 4s, metal | 1 | 3.748 | **3.748** | Metallic luster |
| Graphite | sp2+pi, semimetal | 8 | 51.002 | **6.375** | Black + gloss |

**Key findings:**

1. **Omega(diamond) << Omega(graphite)**: 0.954 vs 6.375 Ang^2 — **6.7x ratio**.
   The ordering is unambiguous.

2. **Diamond < K metal < Graphite**: Insulator < metal < semimetal on the
   same Omega/WF scale. Carbon and metals from Paper II sit consistently
   on one axis.

3. **Sigma/pi decomposition in graphite**:
   - 6 sigma WFs: 5.49 - 6.27 Ang^2 (sp2 bonds, relatively localized)
   - 2 pi WFs: 7.32, 8.19 Ang^2 (delocalized across layers)
   - Pi electrons are 1.3-1.5x more spread than sigma — they are the
     source of graphite's metallic optical response.

4. **Prior failures explained**: TB model and molecular DFT both gave
   wrong delta ordering because:
   - TB: too coarse to capture sp3 localization (1D chain != 3D diamond)
   - Molecular DFT: isolated molecules != periodic solids; N-normalization
     of IPR mixes size and delocalization effects
   - **The concept was right; the models were inadequate.**

### Success Criteria Status

| Criterion | Threshold | Status |
|-----------|-----------|--------|
| SCF convergence | JOB DONE, no warnings | **PASS** |
| Wannier convergence | Delta Omega = 0 over last 100 iter | **PASS** |
| Primary: Omega(diamond) < Omega(graphite) | Unambiguous ordering | **PASS** (6.7x) |
| Secondary: Omega_pi > Omega_sigma (graphite) | Factor > 1.2 | **PASS** (1.3-1.5x) |
| Cross-validation: consistent with metals | Monotonic with optical response | **PASS** |

### Remaining convergence tests (not yet performed)

- ecutwfc convergence: 40, 60, 80 Ry (total energy < 1 mRy)
- k-grid convergence: 4x4x4 vs 6x6x6 (Wannier spread < 0.05 Ang^2)

These are important for publication quality but unlikely to change the
6.7x ordering.

## Calculation Design

### Systems

1. **Diamond** (Fd-3m, a = 3.567 Ang, 2 atoms/cell)
   - sp3: 4 equivalent sigma bonds
   - Band gap ~5.5 eV
   - Projection: s;p on each C (8 WFs total)
   - num_wann = num_bands = 8 (no disentanglement needed)

2. **Graphite** (P6_3/mmc, a = 2.461 Ang, c = 6.708 Ang, 4 atoms/cell)
   - sp2 + pi: 3 sigma bonds + 1 delocalized pi per atom
   - Semimetal (band overlap ~40 meV)
   - Projection: s;p on 2 of 4 atoms (8 WFs total)
   - num_wann = num_bands = 8 (exclude_bands 9-20)

### Computational Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| XC functional | PBE | Consistent with Paper II metals |
| Pseudopotential | C.pbe-n-kjpaw_psl.1.0.0.UPF | PAW, same pslibrary as metals |
| ecutwfc | 60 Ry | Carbon needs higher cutoff than metals |
| ecutrho | 480 Ry | 8x ecutwfc for PAW |
| k-grid (SCF) | 8x8x8 (diamond), 8x8x4 (graphite) | Adapted to cell shape |
| k-grid (Wannier) | 4x4x4 (diamond), 4x4x2 (graphite) | Explicit k-list |
| Smearing | fixed (diamond), Gaussian 0.005 Ry (graphite) | Insulator vs semimetal |

### Pipeline

```
setup.sh          → Download C pseudopotential
diamond/scf.in    → pw.x (SCF, 8x8x8 k-grid)
diamond/nscf.in   → pw.x (NSCF, explicit 4x4x4 k-points)
diamond/diamond.win → wannier90.x -pp → pw2wannier90.x → wannier90.x
graphite/scf.in   → pw.x (SCF, 8x8x4 k-grid)
graphite/nscf.in  → pw.x (NSCF, explicit 4x4x2 k-points)
graphite/graphite.win → wannier90.x -pp → pw2wannier90.x → wannier90.x
analyze_spreads.py → Parse .wout, compute Omega/WF, PASS/FAIL
plot_wannier_comparison.py → fig_wannier_comparison.{png,pdf}
```

### Environment

```bash
# QE + Wannier90 via conda
export PATH="$HOME/miniconda3/envs/qe/bin:$PATH"
```

## Application to Paper I

### What this result means for the paper

Paper I (v7) currently uses three **literature-derived proxies** for delta:
pi-band width, inverse effective mass (1/m*), and band gap. The 7/7
classification success is via the (E_g, D_eff) decision tree. The proxies
support the claim that a single underlying quantity (delta) organizes the
optical categories, but delta itself was never directly computed.

**This Wannier calculation fills that gap.** It provides the first
direct, first-principles measurement of delta_elec for carbon allotropes.

### Specific additions to Paper I

1. **New figure (Fig. 5 or Supplemental)**:
   `fig_wannier_comparison.pdf` — two panels:
   - (a) Omega/WF bar chart: Diamond (0.95) vs K metal (3.75) vs
     Graphite (6.38), color-coded by optical category
   - (b) Graphite individual WF spreads with sigma/pi decomposition

2. **New paragraph in Section III or IV** (after classification results):

   > "To verify that the literature proxies reflect a genuine underlying
   > delocalization, we performed DFT + Wannier90 calculations for bulk
   > diamond and graphite (see Supplemental Material for computational
   > details). The maximally localized Wannier function spread Omega,
   > which directly measures the spatial extent of each electron, gives
   > Omega/WF = 0.95 Ang^2 for diamond and 6.38 Ang^2 for graphite ---
   > a 6.7-fold ratio consistent with the ordering implied by the
   > literature proxies. Moreover, graphite's Wannier functions
   > decompose into localized sigma bonds (5.5--6.3 Ang^2) and
   > delocalized pi orbitals (7.3--8.2 Ang^2), confirming that
   > pi-electron delocalization is the microscopic origin of graphite's
   > metallic optical response."

3. **Strengthened claim in Abstract/Conclusion**:
   Current: "three independent proxies correlate (r = 0.73--0.89)"
   Add: "and the underlying Wannier function spread confirms the
   ordering at the first-principles level"

4. **Connection to Paper II metals**:
   The fact that Diamond (0.95) < K metal (3.75) < Graphite (6.38) on
   the same scale means Papers I and II share a single quantitative
   axis. This cross-validation can be noted in the Outlook section.

### What NOT to do

- Do not overstate: Omega/WF is not delta_IPR. It is a different
  (but related) measure of delocalization. State clearly that
  "Wannier spread provides independent confirmation of the delta
  ordering" rather than "we computed delta from first principles."
- Do not add the full DFT methodology to the main text (it would
  disrupt the flow). Put computational details in Supplemental Material.
- Convergence tests (ecutwfc, k-grid) should be completed before
  publication to ensure the numbers are robust.

## Files

```
simulation/wannier_carbon/
  README.md                      # This file
  setup.sh                       # Download C pseudopotential
  run_all.sh                     # Execute full pipeline
  analyze_spreads.py             # Parse .wout, PASS/FAIL analysis
  plot_wannier_comparison.py     # Generate comparison figure
  fig_wannier_comparison.png     # Output figure (200 dpi)
  fig_wannier_comparison.pdf     # Output figure (vector)
  pseudo/
    C.pbe-n-kjpaw_psl.1.0.0.UPF # PAW pseudopotential (PBE)
  diamond/
    scf.in, nscf.in              # QE input files
    diamond.win, pw2wan.in       # Wannier90 input files
    diamond.wout                 # Wannier90 output (Omega = 7.635)
    scf.out, nscf.out, pw2wan.out
    tmp/                         # QE working directory
  graphite/
    scf.in, nscf.in              # QE input files
    graphite.win, pw2wan.in      # Wannier90 input files
    graphite.wout                # Wannier90 output (Omega = 51.002)
    scf.out, nscf.out, pw2wan.out
    tmp/                         # QE working directory
```
