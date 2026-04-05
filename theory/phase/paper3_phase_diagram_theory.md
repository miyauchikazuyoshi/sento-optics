# Paper 3 Theory Draft: Phase Classification via (delta_nuc, delta_elec)

**Status: Intuitive hypothesis with physical motivation. NOT a proven theory.**
**All claims below are conjectures unless explicitly marked as established physics.**

---

## 1. Motivation: What Observation Started This

At a public bathhouse (sento), liquid water exhibits two simultaneous
macroscopic properties:

1. **Luster** --- the liquid surface reflects light specularly.
2. **Surface tension** --- the liquid surface resists deformation
   (water drops are spherical, meniscus forms at walls).

Conventional physics explains these two phenomena separately:
luster via Fresnel optics, surface tension via intermolecular cohesion.
No unified framework derives both from a single underlying variable.

The intuition: both phenomena are consequences of the **freedom of
constituent particles**. If particles are free enough to rearrange at
an interface, the interface self-heals (luster) and resists expansion
(surface tension). This led to the definition of a delocalization
index delta, which was tested in two companion papers:

- **Paper 1**: delta_elec governs optical response in solids
  (classification accuracy 85.7% for carbon allotropes)
- **Paper 2**: delta_elec correlates with interstitial charge density
  at metallic surfaces (r = 0.72--0.84 across basis sets)

The present document asks: can the same variable delta, decomposed into
nuclear and electronic components, **classify all phases of matter**?

> **Caveat**: This is an intuitive hypothesis motivated by the internal
> consistency of Papers 1 and 2. It has not been computationally
> verified beyond the solid-state and liquid-metal regimes treated in
> those papers. The extension to gas, plasma, superconducting, and
> superfluid phases is conjectural.

---

## 2. Two-Component Delocalization Index

### 2.1 Definition (hypothesis)

We postulate that any macroscopic material state can be characterized
by two delocalization indices:

- **delta_nuc**: the degree to which constituent nuclei (or atoms/
  molecules) are delocalized from fixed positions. delta_nuc = 0 for
  a perfect crystal; delta_nuc > 0 for a liquid; delta_nuc >> 0 for
  a gas.

- **delta_elec**: the degree to which electrons are delocalized across
  multiple atomic sites. delta_elec approx 0 for a noble gas atom;
  delta_elec > 0 for a metal; delta_elec -> MAX for a superconductor.

> **Caveat**: "degree of delocalization" is operationally defined via
> the inverse participation ratio (IPR) in Papers 1 and 2. For
> delta_nuc, the corresponding IPR would require the nuclear
> wavefunction or its classical proxy (e.g., Lindemann ratio, mean
> free path / system size). A rigorous operational definition of
> delta_nuc is an open problem; the discussion below treats it as a
> qualitative ordering parameter.

### 2.2 Three regimes of delta

For each component (nuc or elec), we distinguish three qualitative
regimes:

| Regime | delta value | Physical meaning |
|--------|-------------|------------------|
| Localized | approx 0 | Particles bound to fixed positions/sites |
| Free | 0 < delta < 1 | Particles mobile but incoherent (classical or thermal) |
| Coherent | delta -> 1 (MAX) | Macroscopic quantum coherence (single wavefunction) |

The distinction between "free" and "coherent" is crucial: in a normal
metal, electrons are individually delocalized (each occupying a Bloch
state) but thermally distributed across many k-states. In a
superconductor, Cooper pairs condense into a single macroscopic
quantum state --- the electrons are not merely free but phase-coherent
across the entire sample.

> **Established physics**: The distinction between thermal delocalization
> and quantum coherence is well established (BEC theory, BCS theory).
> What is new here is the claim that this distinction maps naturally
> onto the delta framework as a "third regime" of the same variable.

---

## 3. Phase Diagram in (delta_nuc, delta_elec) Space

### 3.1 The four classical states of matter

**Hypothesis**: the four classical states of matter correspond to
four quadrants of the (delta_nuc, delta_elec) plane:

```
       delta_elec
    high |
         |  Metal (solid)        Liquid metal
         |  delta_nuc=0          delta_nuc>0
         |  delta_elec=high      delta_elec>0
         |
         |  Insulating solid     Liquid (insulating)
         |  delta_nuc=0          delta_nuc>0
         |  delta_elec=low       delta_elec>0
    low  |
       0 +----------------------------> delta_nuc
              Solid      Liquid     Gas
```

Wait --- where does gas fit? Gas has delta_nuc high (particles move
freely) but delta_elec approx 0 (electrons localized on individual
atoms/molecules, no interatomic orbital overlap). This places gas in
the **lower-right** of the diagram:

```
       delta_elec
    high |
         |  Metal solid      Liquid metal      Plasma
         |
    med  |
         |  Insulator        Liquid             Gas*
         |
    low  |                                     Gas
         |
       0 +-------------------------------------------> delta_nuc
              Solid          Liquid             Free
```

> *Note: "normal" liquid (water) has delta_elec > 0 due to
> intermolecular overlap of electron clouds (van der Waals,
> hydrogen bonding). This is what maintains cohesion and
> distinguishes liquid from gas. The liquid-gas distinction
> is therefore determined primarily by delta_elec, NOT delta_nuc.
> Both liquid and gas have delta_nuc > 0 (particles are mobile);
> what differs is whether electrons participate in collective
> cohesion.

### 3.2 The key insight: liquid vs gas

**Hypothesis**: The physical difference between liquid and gas is
not the degree of nuclear freedom (both have delta_nuc > 0), but
the degree of electronic cohesion:

| | delta_nuc | delta_elec | Consequence |
|--|-----------|------------|-------------|
| Liquid | > 0 | > 0 | Electron clouds overlap -> cohesion -> fixed volume |
| Gas | >> 0 | approx 0 | No electronic overlap -> no cohesion -> fills container |

This immediately explains:

| Property | Liquid (delta_elec > 0) | Gas (delta_elec approx 0) |
|----------|------------------------|---------------------------|
| Volume | Fixed | Indefinite |
| Surface tension | gamma > 0 | gamma = 0 |
| Luster | Present | Absent |
| Density | High | Low |
| Compressibility | Low | High |

All five macroscopic differences between liquid and gas follow from
a single variable distinction (delta_elec > 0 vs approx 0).

> **Caveat**: This is a qualitative argument. The quantitative
> question --- at what value of delta_elec does the liquid-gas
> transition occur? --- is not addressed here and would require
> connecting delta_elec to a concrete order parameter (e.g.,
> pair correlation function, electronic overlap integral).

### 3.3 Plasma as the fourth state

**Hypothesis**: Plasma occupies the upper-right corner of the
(delta_nuc, delta_elec) diagram:

| State | delta_nuc | delta_elec |
|-------|-----------|------------|
| Solid | 0 | varies |
| Liquid | > 0 | > 0 |
| Gas | high | approx 0 |
| **Plasma** | **high** | **high** |

The gas-to-plasma transition (ionization) corresponds to a sudden
increase in delta_elec: electrons that were bound to individual
atoms become free. In the delta language, ionization is the event
where delta_elec jumps from approx 0 to a high value.

Plasma properties follow naturally:

| Property | delta explanation |
|----------|------------------|
| High conductivity | delta_elec high -> free electrons -> current |
| Light emission | delta_elec high -> collective electromagnetic response |
| Magnetic field response | delta_elec high -> free charged particles |
| No fixed volume | delta_nuc high -> same as gas |
| Debye shielding | delta_elec high -> free electrons screen applied fields |

> **Established physics**: Plasma physics is a mature field. The
> delta description does not add new predictions about plasma
> behavior; it provides a **classification** that places plasma
> alongside the other three states in a unified two-variable scheme.

### 3.4 The critical point

**Hypothesis**: The liquid-gas critical point is the temperature
at which the difference in delta_elec between the liquid and gas
phases vanishes continuously.

At subcritical temperatures, liquid (delta_elec > 0) and gas
(delta_elec approx 0) coexist as distinct phases. As temperature
increases toward T_c:
- The liquid expands (density decreases, intermolecular distances grow)
- Electronic overlap decreases continuously
- delta_elec(liquid) decreases toward delta_elec(gas)

At T_c, the two values merge: delta_elec(liquid) = delta_elec(gas).
There is no longer a variable that distinguishes the two phases,
so the distinction disappears. Above T_c, a single supercritical
phase exists.

This is consistent with the known critical behavior of surface
tension: gamma propto (T_c - T)^mu -> 0 as T -> T_c. In the delta
framework, gamma arises from the spatial gradient of delta at the
interface; when the bulk delta values of liquid and gas become equal,
the gradient vanishes, and gamma -> 0.

> **Caveat**: The critical exponent mu (approx 1.26 in 3D Ising
> universality) reflects universal fluctuation physics. The delta
> framework as stated does not predict mu; it provides a qualitative
> narrative consistent with the existence of a critical point, not
> a quantitative theory of critical phenomena.

---

## 4. Extension to Quantum Phases

### 4.1 Superconductivity: delta_elec -> MAX

**Hypothesis**: The superconducting transition corresponds to
delta_elec entering the "coherent" regime --- not merely high
(many delocalized electrons) but maximal (all electrons
participating in a single macroscopic quantum state).

| State | delta_elec regime | Physical description |
|-------|-------------------|---------------------|
| Insulator | Low | Electrons localized on atoms |
| Normal metal | High (free) | Electrons delocalized but in many k-states |
| Superconductor | MAX (coherent) | Cooper pairs in a single macroscopic wavefunction |

In the language of Bose-Einstein condensation (BEC/BCS crossover):
Cooper pairs are composite bosons, and the superconducting ground state
is their BEC. BEC is precisely the state where all particles occupy a
single quantum state, which minimizes the IPR and maximizes delta.

**Connection to Paper 1 (luster)**:

The superconductor is the ultimate test of the coherence-preservation
hypothesis. If delta_elec -> MAX implies perfect phase coherence of
the electronic response, then the optical reflectivity should be
R = 1 (perfect mirror). This is exactly what the Meissner effect
produces: superconductors are perfect reflectors for electromagnetic
radiation below the gap frequency (2Delta/hbar).

> **Established physics**: The Meissner effect and London equations
> are well established. The delta framework does not derive them;
> it observes that they are consistent with the extreme limit of
> the delta-luster hypothesis. This consistency check is non-trivial:
> Paper 1's hypothesis, developed from carbon allotropes, correctly
> predicts the optical behavior of the most extreme metallic state
> without any additional assumptions.

### 4.2 Superfluidity: delta_nuc -> MAX

**Hypothesis**: The superfluid transition corresponds to
delta_nuc entering the "coherent" regime.

| State | delta_nuc regime | Physical description |
|-------|------------------|---------------------|
| Solid | 0 (localized) | Nuclei frozen on lattice sites |
| Normal liquid | > 0 (free) | Nuclei mobile but classical/incoherent |
| Superfluid | MAX (coherent) | All atoms in a single macroscopic wavefunction |

For He-4: below T_lambda = 2.17 K, the bosonic atoms undergo
BEC. The condensate fraction represents the portion of atoms
in the delta_nuc -> MAX regime; the normal fraction remains in
the "free" regime. The two-fluid model of superfluidity maps
directly onto a bimodal distribution of delta_nuc.

Superfluid properties follow:

| Property | delta_nuc -> MAX explanation |
|----------|-----------------------------|
| Zero viscosity | All particles in one state -> no internal scattering |
| Creeping film | Macroscopic wavefunction extends beyond container boundaries |
| Second sound | Density oscillation between condensed (delta_nuc=MAX) and thermal (delta_nuc=free) components |
| Quantized vortices | Phase of macroscopic wavefunction must be single-valued -> circulation quantized |

> **Caveat**: Superfluidity is fully explained by existing theory
> (Landau two-fluid model, Gross-Pitaevskii equation, BEC theory).
> The delta_nuc description is a re-parametrization that adds no
> new predictions. Its value, if any, lies in placing superfluidity
> on the same conceptual map as ordinary phases and superconductivity.

### 4.3 The upper-right corner: delta_nuc -> MAX AND delta_elec -> MAX

The (delta_nuc -> MAX, delta_elec -> MAX) corner of the phase diagram
represents a state that is simultaneously superfluid AND
superconducting: nuclei and electrons both in macroscopic quantum
coherence.

This is not purely hypothetical:
- **Neutron star interiors**: Neutron superfluidity coexists with
  proton superconductivity in the inner crust and core.
- **Metallic hydrogen** (predicted): At extreme pressures, hydrogen
  is predicted to become a superconducting superfluid.
- **Ultracold atomic gases**: Fermionic condensates with tunable
  interactions can explore this regime.

> **Caveat**: These are extreme conditions far from the everyday
> materials that motivated this framework. Including them here
> illustrates the logical completeness of the (delta_nuc, delta_elec)
> classification, not a practical prediction.

---

## 5. Complete Phase Diagram

### 5.1 Full classification table

| State | delta_nuc | delta_elec | Examples |
|-------|-----------|------------|----------|
| Insulating solid | 0 | Low | Diamond, NaCl, h-BN |
| Metallic solid | 0 | High | Cu, Fe, Al |
| Superconductor | 0 | MAX (coherent) | Nb, YBCO, MgB2 |
| Glass | approx 0 | Low--High | SiO2 glass, metallic glass |
| Normal liquid | > 0 | > 0 | Water, ethanol |
| Liquid metal | > 0 | High | Hg, Ga(l), Na(l) |
| Gas | High | approx 0 | N2, Ar, H2O(g) |
| Plasma | High | High | Solar corona, neon sign |
| Superfluid | MAX (coherent) | Low | He-4 below T_lambda |
| Superfluid + superconductor | MAX | MAX | Neutron star interior (?) |

### 5.2 Phase transitions as delta trajectories

| Transition | What changes | delta trajectory |
|------------|-------------|------------------|
| Melting | delta_nuc: 0 -> > 0 | Horizontal rightward |
| Vaporization | delta_elec: > 0 -> approx 0 | Vertical downward |
| Ionization | delta_elec: approx 0 -> high | Vertical upward |
| Superconducting | delta_elec: high -> MAX | Vertical upward (qualitative jump) |
| Superfluid | delta_nuc: > 0 -> MAX | Horizontal rightward (qualitative jump) |
| Glass transition | delta_nuc: > 0 -> approx 0 | Horizontal leftward (continuous) |
| Critical point | delta_elec(liquid) - delta_elec(gas) -> 0 | Liquid and gas merge on vertical axis |

### 5.3 Heating path of water

The familiar heating trajectory of water maps onto a characteristic
L-shaped path in (delta_nuc, delta_elec) space:

```
Ice -> Water -> Steam -> (ionized plasma at extreme T)

delta_nuc:  0  ->  >0  ->  high  ->  high     (increases monotonically)
delta_elec: >0 ->  >0  ->  ~0    ->  high     (non-monotonic!)
```

The non-monotonicity of delta_elec is physically meaningful:
in ice and water, hydrogen bonding creates significant electronic
overlap (delta_elec > 0). Upon vaporization, molecules separate and
delta_elec drops. Upon ionization, electrons are freed and delta_elec
rises again. This L-shaped (or U-shaped in delta_elec) trajectory
is a distinctive prediction of the two-variable framework.

---

## 6. Relation to Established Concepts

### 6.1 What delta ADDS to existing phase classification

| Existing concept | What it classifies | What it misses |
|------------------|--------------------|----------------|
| Long-range order (Landau) | Solid vs non-solid | Glass; liquid vs gas distinction unclear at critical point |
| Equation of state (van der Waals) | Gas, liquid, critical point | No electronic structure; no connection to luster or conductivity |
| Band theory | Metal vs insulator | Applies only to crystalline solids; no nuclear degrees of freedom |

The delta framework does not replace any of these. It provides a
**two-variable map** that connects electronic structure (Paper 1, 2)
to thermodynamic phase identity, offering a unified perspective that
these separate theories do not individually provide.

### 6.2 What delta does NOT do

1. **It does not predict phase transition temperatures.**
   Knowing delta does not tell you T_m, T_b, T_c, or T_BEC.
   These require free-energy calculations, which delta does not
   provide.

2. **It does not replace order parameters.**
   Landau theory's order parameter (e.g., magnetization, density
   difference) is a thermodynamic variable with well-defined
   transformation properties. delta is a microscopic descriptor,
   not a thermodynamic potential.

3. **It does not predict critical exponents.**
   Critical phenomena are governed by universality classes
   determined by symmetry and dimensionality, not by microscopic
   descriptors.

4. **delta_nuc lacks a rigorous operational definition.**
   For electrons, delta_elec = delta_IPR is precisely defined
   via the IPR of Kohn-Sham orbitals (Paper 2) or tight-binding
   eigenstates (Paper 1). For nuclei, no analogous wavefunction
   is readily available in the classical regime. A candidate
   operational definition might use:
   - Lindemann ratio (u_rms / a): delta_nuc propto u_rms / a
   - Mean free path / system size: delta_nuc propto lambda_mfp / L
   - Velocity autocorrelation decay time

   Establishing a rigorous delta_nuc is a central open problem
   for Paper 3.

5. **The coherent regime (delta -> MAX) is qualitatively different
   from the free regime (delta > 0).** The current framework
   treats them as points on a continuous axis, but BEC/BCS involve
   a genuine phase transition (symmetry breaking of the U(1) phase).
   Whether delta can capture this discontinuity within a continuous
   variable, or whether an additional "coherence flag" is needed,
   is unresolved.

---

## 7. Occam's Razor: What the Framework Achieves

The conventional definition of each phase requires a separate
description:

- Solid: "has long-range order and resists shear"
- Liquid: "has no long-range order, flows, has fixed volume"
- Gas: "fills its container, compressible"
- Plasma: "ionized gas, conducts electricity"
- Superconductor: "zero resistance, Meissner effect"
- Superfluid: "zero viscosity, quantized vortices"

These are six separate descriptive statements. The delta framework
proposes that all six are consequences of two variables:

> **(delta_nuc, delta_elec), each taking values in {0, free, coherent}**

This yields 3 x 3 = 9 cells, of which at least 6 correspond to
known phases. The remaining cells either represent extreme/exotic
states (superfluid + superconductor) or physically forbidden
combinations.

The economy of description is the framework's primary claim:
**not that it predicts new phenomena, but that it unifies known
phenomena under a minimal variable set.** Whether this economy
carries predictive power beyond classification remains to be
demonstrated.

> **Self-critique**: Occam's razor rewards simplicity only when
> predictive power is preserved. If the delta framework merely
> relabels known physics without enabling new predictions or
> quantitative calculations, its value is pedagogical rather
> than scientific. The test is whether delta enables predictions
> that existing frameworks cannot make independently --- e.g.,
> correlations between optical properties and surface tension
> (Papers 1 + 2 combined), or identification of new materials
> with unusual phase behavior based on their (delta_nuc, delta_elec)
> position.

---

## 8. Testable Predictions and Open Questions

### 8.1 Predictions already tested (Papers 1 and 2)

1. High delta_elec -> high luster: confirmed for carbon allotropes
   (Paper 1, 85.7% classification accuracy)
2. delta_elec correlates with interstitial charge density at metal
   surfaces: confirmed for 11 elements (Paper 2, r = 0.72--0.84)

### 8.2 Predictions testable with existing data

3. **Liquid metals with higher delta_elec should have both higher
   surface tension AND higher luster.** Cross-checking reflectivity
   data (Palik) against surface tension (Keene 1993) for the same
   liquid metals would test whether delta_elec governs both
   simultaneously.

4. **The critical point should coincide with delta_elec(liquid) ->
   delta_elec(gas).** Molecular dynamics simulations near T_c could
   track a delta-like quantity (e.g., electronic overlap integral
   or pair correlation function at metallic distances) and check
   whether it vanishes at T_c.

5. **Glass transition should be a continuous decrease of delta_nuc
   without a sharp jump.** This is consistent with the known
   absence of a sharp thermodynamic phase transition at T_g,
   but could be made quantitative by computing delta_nuc
   (e.g., from Lindemann ratio) across T_g in MD simulations.

### 8.3 Predictions requiring new experiments or simulations

6. **Superconductors should show R = 1 for omega < 2Delta,
   consistent with delta_elec -> MAX.** (Already known; serves
   as a consistency check, not a new prediction.)

7. **Materials near the liquid-metal / plasma boundary should show
   anomalous optical properties** (rapid change in reflectivity
   with temperature as delta_elec transitions between "high" and
   "free" regimes).

8. **Quantitative delta_nuc for He-4 across T_lambda** should show
   a sharp increase at the superfluid transition, measurable via
   the condensate fraction.

### 8.4 Open theoretical questions

9. How to rigorously define delta_nuc in the classical regime?
10. Is the "coherent" regime (delta -> MAX) continuously connected
    to the "free" regime, or is an additional variable needed?
11. Can the Renyi entropy identity (IPR = e^{-H2}) be extended to
    delta_nuc, providing an information-theoretic unification?
12. Does the path-integral formalism provide a natural framework
    for treating thermal and quantum delocalization on equal footing?
    (See 03_phase_unification.md, Section 4.)

---

## 9. Metal Vaporization: L-shaped Trajectory and the Mercury Critical Point

**Added 2026-04-04, based on discussion of vaporized metal free electrons.**

### 9.1 What happens to free electrons when metals vaporize?

In solid metals, free electrons form bands delocalized across the
crystal (delta_elec high). Upon vaporization, the crystal structure
is destroyed and band structure vanishes. Each electron is re-bound
to its parent atom: Na vapor is a collection of isolated Na atoms
with electrons localized in 3s orbitals. delta_elec drops sharply.

The metal vaporization trajectory in (delta_nuc, delta_elec) space:

```
Solid metal:  delta_nuc low,  delta_elec high
Liquid metal: delta_nuc high, delta_elec high (metallic bonding maintained)
Metal vapor:  delta_nuc very high, delta_elec LOW (isolated atoms)
```

This is NOT a diagonal trajectory. It is an **L-shaped path**:
delta_nuc rises while delta_elec drops. The two variables move
in opposite directions during vaporization.

**Experimental confirmation**: Metal vapor does not exhibit metallic
luster. Sodium lamp emits yellow line spectra (atomic transitions)
but no specular reflection. Electrons are not delocalized, so
photon phase coherence is not preserved.

### 9.2 The mercury critical point: continuous metal-nonmetal transition

Mercury provides the most studied example of the continuous
delta_elec transition. At the critical point (Tc approx 1750 K,
Pc approx 1670 atm), density changes continuously and a
metal-to-nonmetal transition occurs.

**Existing theories** describe this as:

- Density decrease -> band overlap vanishes -> gap opens -> nonmetal
- Three conduction regimes identified (Hensel & Warren 1999):
  - Weak-scattering metal (13.6-11 g/cm3)
  - Strong-scattering metal (11.0-9.2 g/cm3)
  - Nonmetal (< 9.2 g/cm3)
- Ab initio MD (Desjarlais 2003, Phys. Rev. B 68, 064204) shows
  the 6s-6p gap opening at density approx 8.8 g/cm3, corresponding
  to optical gap formation
- The metal-nonmetal transition is NOT a first-order phase transition
  but a continuous crossover (contrary to early predictions by
  Landau and Zeldovich)
- "Fluctuons" model proposes mesoscopic inhomogeneity with coexisting
  metallic, semiconducting, and gas-like domains near the critical point

**The key difficulty**: reliable theoretical methods do not exist for
the intermediate region. Effective potentials become state-dependent,
and no single framework covers the full density range.

### 9.3 delta_elec as the missing continuous variable

In the delta framework, the mercury critical point is described as:

- Density decrease -> interatomic distance increase -> wavefunction
  overlap decrease -> delta_elec decrease -> conductivity and
  reflectivity decrease

This is the same phenomenon described by existing theories, but with
delta_elec as a continuous interpolating variable. The advantage:

1. **No regime boundaries**: Existing theory needs three separate
   regimes (weak-scattering, strong-scattering, nonmetal) with
   different effective descriptions. delta_elec varies smoothly
   across all three.

2. **Continuous crossover is natural**: Since delta_elec is a
   continuous variable, the metal-nonmetal transition being a
   continuous crossover (not first-order) is the default prediction.

3. **Fluctuons as spatial delta fluctuations**: The mesoscopic
   inhomogeneity near the critical point can be described as
   spatial fluctuations of delta_elec --- some regions have
   high delta (metallic domains), others low (nonmetallic domains),
   with the correlation length diverging at the critical point.

### 9.4 Candidate for Paper III verification

The mercury critical point is an ideal test system for Paper III:

- **Existing ab initio MD data**: Desjarlais (2003) and others
  have computed electronic structure across the density range.
  Adding Wannier spread Omega as an analysis variable to existing
  trajectories requires no new simulations.

- **Experimental data**: Conductivity, reflectivity, and optical
  gap as functions of density are well measured (Hensel & Warren 1999).

- **Testable prediction**: delta_elec (Wannier spread) should
  decrease continuously with density and correlate with the
  measured conductivity/reflectivity at each density point.

- **What delta adds**: A single continuous descriptor that
  interpolates the three existing regimes without regime boundaries.

> **Caveat**: "Smoothly interpolating" and "quantitatively
> reproducing" are different. Existing researchers have struggled
> with quantitative reproduction for decades. If delta merely
> provides a qualitative narrative without improving quantitative
> predictions, its value in this context is limited.

### 9.5 Connection to the (delta_nuc, delta_elec) phase diagram

The vaporization trajectories of different materials differ:

| Material | Solid | Liquid | Vapor | Trajectory shape |
|----------|-------|--------|-------|-----------------|
| Metal (Na) | (low, high) | (high, high) | (v.high, low) | L-shaped |
| Water | (low, med) | (high, med) | (v.high, low) | Gradual descent |
| Noble gas | (low, 0) | N/A | (v.high, 0) | Horizontal |

The non-monotonicity of delta_elec during metal vaporization
(high -> high -> low) is a distinctive feature of the two-variable
framework. It explains why liquid metals retain metallic properties
(luster, conductivity) while their vapors do not.

The heating path of water (Section 5.3) already noted this
non-monotonicity. The metal vaporization case makes it more dramatic:
delta_elec(solid) approx delta_elec(liquid) >> delta_elec(vapor).

---

*This document records the theoretical framework discussed on
2026-03-30/31, with additions from 2026-04-03/04.
All extensions beyond Papers 1 and 2 are hypotheses.
The framework's value will be determined by whether it generates
testable predictions that existing theories cannot make independently.*
