# Memo: δ vs Density — Classical vs Quantum Description of Matter

**Status: Conceptual note. Records the author's insight on why δ may be
a more natural variable than n(r) for phase classification.**

---

## The Observation

Electron density n(r) asks: **"Where is the electron?"**

This is a fundamentally classical question. It treats the electron as
an object that has a position, and measures the probability of finding
it at each point. DFT's triumph was showing that this classical-looking
quantity is sufficient to determine all ground-state properties
(Hohenberg-Kohn theorem).

δ_IPR asks a different question: **"How many sites does the electron
span?"**

This is a fundamentally quantum question. It does not ask where the
electron is, but how much of the system it occupies simultaneously.
A delocalized electron does not have a position — it exists across
many sites at once. δ quantifies the degree to which this
superposition extends.

## Why This Matters

### The classical bias of n(r)

n(r) is the **diagonal** of the one-body density matrix γ(r,r'):

```
n(r) = γ(r, r)     ← "electron at r, asking about r"
```

This is the classical limit: you probe the system at one point and
ask what's there. It discards all information about quantum coherence
between different points.

The **off-diagonal** elements γ(r,r') for r ≠ r' encode:

```
γ(r, r')            ← "quantum connection between r and r'"
```

This is the quantum information: how much does the electron at r
"know about" the electron at r'? A localized electron has
γ(r,r') ≈ 0 for |r-r'| > localization length. A delocalized
electron has γ(r,r') ≠ 0 over macroscopic distances.

**δ captures the off-diagonal spread of γ.** It measures what n(r)
throws away.

### Why DFT needs orbitals

The Hohenberg-Kohn theorem guarantees that n(r) is sufficient
**in principle**. But in practice, nobody can construct the kinetic
energy functional T[n] from n(r) alone — the Thomas-Fermi attempt
fails catastrophically (no shell structure, no chemical bonds, no
band gaps).

Kohn and Sham's solution: reintroduce orbitals {ψ_i(r)}, compute
kinetic energy from their gradients, and recover n(r) = Σ|ψ_i|² at
the end. This is an acknowledgment that **the orbital structure
(i.e., how electrons spread across space) contains essential physics
that n(r) alone cannot efficiently access**.

δ_IPR extracts precisely this orbital-level information: the IPR of
each ψ_i tells you how many sites it spans.

### The quantum perspective is more general

In classical mechanics, a particle has a definite position. The
density n(r) is the natural description.

In quantum mechanics, a particle does not have a definite position.
It has a state |ψ⟩ that is a superposition across the system. The
natural description is not "where" but "how spread out."

| Question | Framework | Variable |
|----------|-----------|----------|
| Where is the electron? | Classical | n(r) |
| How spread out is the electron? | Quantum | δ (IPR, Rényi entropy) |

The classical question is a special case of the quantum question:
if the electron is perfectly localized (δ → 0), then "where" is
well-defined and n(r) captures everything. But when the electron is
delocalized (δ > 0), asking "where" loses information — the answer
"it's everywhere" is technically correct but uninformative. δ tells
you *how much* of "everywhere" the electron occupies.

### Implication for phase classification

Conventional phase classification uses thermodynamic variables
(T, P, V) and structural quantities (order parameters, density).
These are all "position-based" or "classical" descriptions.

The δ framework suggests that phases are more naturally classified
by **delocalization** — a quantum property:

- **Solid**: δ_nuc = 0 (nuclei localized → "where" is well-defined)
- **Liquid**: δ_nuc > 0 (nuclei delocalized → "where" loses meaning)
- **Superfluid**: δ_nuc → MAX (all nuclei in one state → "where" is maximally undefined)

For liquids, asking "where is the atom?" misses the point. The atom
is not anywhere in particular — it is free to be anywhere in the
volume. The liquid's macroscopic properties (flow, self-healing,
luster) are consequences of this delocalization, not of any specific
atomic arrangement.

This is why a density-based description of liquids is awkward: the
density of a liquid is nearly uniform (n(r) ≈ const), so n(r) carries
almost no structural information. But δ_nuc carries the essential
information: how free are the atoms to rearrange?

## Connection to Existing Physics

### Position vs momentum (complementarity)

In quantum mechanics, sharp position means uncertain momentum, and
vice versa. A localized electron (δ → 0) has well-defined position
but uncertain momentum → insulating. A delocalized electron (δ → 1)
has uncertain position but well-defined crystal momentum k → metallic
(Bloch waves).

δ sits on the position-uncertainty side of this complementarity.
High δ = high position uncertainty = the electron "doesn't have a
position" = it is quantum-mechanically spread across the system.

### Entanglement and many-body δ

In many-body quantum mechanics, entanglement entropy measures
"how much one part of the system knows about another." This is
closely related to the off-diagonal γ(r,r'). The Rényi-2 entropy
connection (IPR = e^{-H₂}) noted in renyi_entropy_memo.md may
provide a bridge to entanglement-based descriptions of phases
(topological order, quantum spin liquids, etc.).

## Summary

> n(r) is the classical question: "where?"
> δ is the quantum question: "how spread out?"
>
> For localized systems (crystals, insulators), "where" is informative.
> For delocalized systems (metals, liquids, superfluids), "how spread
> out" is more informative.
>
> The δ framework proposes that "how spread out" is the more general
> and more useful question for classifying phases of matter, because
> the macroscopic properties that distinguish phases (flow, cohesion,
> luster, conductivity) are consequences of delocalization, not of
> specific positions.

---

*This memo records the author's insight (2026-03-31): the conceptual
distinction between n(r) as a classical variable and δ as a quantum
variable. The claim that δ is "more natural" is a physical intuition,
not a theorem.*
