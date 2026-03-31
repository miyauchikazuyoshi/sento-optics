# Memo: Existing Field Theories, Entropy Connection, and δ's Position

**Status: Discussion notes — not yet incorporated into any paper draft.**

---

## 1. Surface Tension Response Timescale

The ns-scale response of surface tension is sometimes cited as evidence
for quantum-mechanical origins. A more precise statement:

- **Surface tension itself** is not "generated in ns." It is an
  equilibrium thermodynamic quantity — the free energy cost per unit
  area of interface.
- **The origin** of γ is electronic: the interface free energy gradient
  is determined by electron distribution and interatomic interactions.
  This part is ultrafast (fs-scale electronic response).
- **The observable shape response** (capillary waves, meniscus formation)
  occurs on ns–μs scales, governed by nuclear/molecular rearrangement,
  viscosity, and inertia.

In the δ framework:

- **δ_elec** determines the cohesive/response field at the interface
  (the "why" of surface tension)
- **δ_nuc** determines how fast nuclei/molecules rearrange in that
  energy landscape (the "how fast" of shape recovery)
- The experimentally observed ns response is the coupled mesoscale
  response of both

---

## 2. Existing Field Theories — Five Lineages

Many existing theories already treat interfaces and phases as fields.
The key insight is that they are **fragmented** — each uses a different
field variable.

### 2.1 Interface free energy field (Cahn-Hilliard, 1958)

- Field variable: density or concentration φ(r)
- Free energy: f(φ) + κ|∇φ|²
- Surface tension emerges as gradient energy
- **Strength**: Elegant, minimal. Widely used for phase separation.
- **Gap**: φ is a macroscopic order parameter; does not resolve
  electronic structure or delocalization.

### 2.2 Classical density functional theory (cDFT / DDFT)

- Field variable: one-body density ρ(r) or ρ(r,t)
- Surface tension, interface structure, relaxation dynamics
- **Strength**: Systematic, can include correlation.
- **Gap**: Still a density field — "where are particles?"
  Does not capture "how spread out?" (off-diagonal γ(r,r')).

### 2.3 Liquid crystal order field (Oseen-Frank, Landau-de Gennes)

- Field variable: director n̂(r) or Q-tensor Q_ij(r)
- Orientational order from quantum micro-origin, classical macro-equations
- **Strength**: Demonstrates quantum-origin → classical-description path.
- **Gap**: Specific to orientational order. No connection to
  electronic delocalization or surface tension of simple liquids.

### 2.4 Macroscopic quantum coherence field (Ginzburg-Landau, Gross-Pitaevskii)

- Field variable: complex order parameter ψ(r) = |ψ|e^{iθ}
- Phase coherence itself becomes a field
- **Strength**: Describes superconductivity, superfluidity, BEC.
- **Gap**: Only applies when macroscopic quantum coherence exists.
  Does not cover normal metals, liquids, or insulators.

### 2.5 Electronic stress / surface stress (Lang-Kohn, quantum stress)

- Field variable: electron density n(r) + ionic density
- Surface energy from DFT-level electron redistribution at surface
- **Strength**: First-principles, quantitative.
- **Gap**: System-specific numerical calculation, not a transferable
  descriptor.

### Summary table

| Theory | Field variable | Covers | Misses |
|--------|---------------|--------|--------|
| Cahn-Hilliard | φ(r) density/conc. | Phase separation, γ | Electronic structure |
| cDFT | ρ(r) one-body density | Interface structure | Off-diagonal spread |
| Landau-de Gennes | Q_ij(r) orientation | Liquid crystals | Simple liquids, metals |
| Ginzburg-Landau | ψ(r) complex OP | SC, SF, BEC | Normal states |
| Lang-Kohn | n(r) electron density | Metal surfaces | Transferability |

### Where δ sits

δ is **not** a new field theory competing with any of the above.
It is a candidate **meta-descriptor** that connects them:

- Cahn-Hilliard's φ → δ determines how uniformly charge fills the cell
- cDFT's ρ(r) → δ captures what ρ(r) alone misses (off-diagonal spread)
- Landau-de Gennes → δ_nuc relates to translational freedom;
  orientational order requires extension
- Ginzburg-Landau → δ in the "coherent" regime
- Lang-Kohn → δ_IPR explains *why* n_ws varies (Paper 2's result)

**Correct positioning**: δ is an upper-level mesoscale descriptor
that organizes when and why each field theory applies, not a
replacement for any of them.

---

## 3. δ as a Fundamental-like Variable

### Not like momentum (too strong)

Momentum p is a generator of translations — tied to symmetry,
defined as a unique operator. δ is not this.

### Like an order parameter (correct analogy)

δ is an **effective mesoscale quantity** that:
- Is not a single exact operator
- Has multiple proxies (IPR, Wannier spread, band width, 1/m*)
- Naturally organizes diverse phenomena
- Functions like free energy, correlation length, or order parameter

### What δ needs to become "fundamental"

1. **Clear domain**: δ_elec vs δ_nuc vs δ_orient (what distribution?)
2. **Scale dependence**: δ(ℓ) as function of coarse-graining scale
3. **Dynamical connection**: what does δ govern, and how does it evolve?

---

## 4. Entropy Connection: IPR = e^{-H₂}

This is potentially the deepest structural insight.

### The identity

For a probability distribution {p_i} over N states:

```
IPR = Σ_i p_i²
H₂  = -log(Σ_i p_i²)    (Rényi entropy of order 2)
IPR = e^{-H₂}
```

Therefore:

```
δ_IPR = 1/(N · IPR) = e^{H₂} / N
```

δ is essentially the **exponential of the Rényi-2 entropy**,
normalized by the system size. It counts "how many states the
particle effectively occupies."

### Why this matters

Entropy is the most universal quantity in statistical physics.
By connecting δ to H₂:

- δ inherits information-theoretic meaning
- The same formalism applies to any probability distribution
  (electron orbitals, nuclear positions, orientational distributions)
- No commitment to a specific physical system is needed

### Does entropy make δ scale-free?

**No.** Entropy always depends on:
- Which state space is partitioned
- Which basis defines {p_i}
- Which coarse-graining level is used

**But** entropy makes scale dependence **explicit and manageable**.
Instead of δ being "accidentally scale-dependent," it becomes
δ(ℓ) — a function of coarse-graining scale ℓ, with well-defined
transformation rules.

### The strong formulation

> The entropy connection does not eliminate scale dependence.
> It **absorbs scale into the theory** — making δ(ℓ) a controlled
> function rather than an uncontrolled artifact.

This is analogous to renormalization group thinking:
phases are classified not by the absolute value of a coupling
but by **how it flows** under scale change.

**Potential Paper 3 thesis**:

> States of matter can be classified by the flow of δ(ℓ)
> under coarse-graining, rather than by the absolute value of δ.
> Localized states have δ(ℓ) → 0 as ℓ grows; free states have
> δ(ℓ) ~ const; coherent states have δ(ℓ) → 1 at all scales.

---

## 5. Universality: What Kind?

### Wrong claim (too strong)

"δ gives the same number for every system" — false, and unnecessary.

### Right claim (strong enough)

"δ provides a common information-theoretic syntax for describing
delocalization across diverse many-body systems."

This is the same type of universality as:
- **Free energy**: different values for every system, but same
  formalism everywhere
- **Order parameter**: different for magnets, superfluids, and
  liquid crystals, but same Landau framework
- **Correlation length**: different numbers, same divergence structure

### How this unifies Papers 1-2-3

| Paper | System | δ measures | Consequence |
|-------|--------|-----------|-------------|
| 1 | Solid electrons | Orbital spread (IPR) | Optical classification |
| 2 | Metal surfaces | Valence delocalization (IPR, Wannier) | n_ws origin |
| 3 | All phases | (δ_nuc, δ_elec) | Phase classification |

Same syntax. Different numbers. Common structure.

---

## 6. Key Takeaways for Paper Writing

1. **Do not** claim δ is a new field theory → claim it is a
   meta-descriptor connecting existing field theories
2. **Do not** claim δ is scale-free → claim the entropy connection
   makes scale dependence explicit and controllable
3. **Do not** claim universality of values → claim universality
   of formalism (information-theoretic syntax)
4. **Do** cite existing field theories explicitly and show where
   δ complements rather than replaces them
5. **Do** use IPR = e^{-H₂} as the formal anchor for the
   entropy connection
