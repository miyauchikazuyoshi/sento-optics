# sento-optics: Electronic Delocalization as a Unifying Descriptor for Interface Properties

> **"What is a liquid, really?"** — A question born in a Japanese *sentō* (public bathhouse), March 27, 2026.

## What This Repository Is

This is the **thinking trail** of a research program — from a bathhouse observation to quantitative physics.

The idea is simple: the **spatial delocalization of constituent particles** (δ) governs interface properties — luster, surface tension, and ultimately the definition of what a "liquid" is. Everyday intuitions are recorded as memos, tested numerically, and the claims that survive are written into papers.

```
Everyday question             →  Theoretical memo              →  Numerical test        →  Paper
"Why does water shine?"       →  theory/optics/                →  simulation/optics/    →  Paper 1
"Why does metal have γ?"      →  theory/surface_tension/       →  simulation/surface_tension/ → Paper 2
"What IS a liquid?"           →  theory/phase/                 →  (planned)             →  Paper 3
```

## The Idea

Staring at the bathwater surface:

1. **Liquids shine.** The water surface reflects light coherently, like a metal mirror.
2. **Liquids have surface tension.** The water holds its shape against gravity.

Both are *interface properties*. Both lack a microscopic explanation rooted in electronic structure. Both can be traced back to a single variable:

**δ (delocalization index)** — how freely constituent particles spread across space.

```
Optical response:   δ × D_eff → ε(ω) → R(ω)
Surface tension:    δ → n_ws → γ
Phase identity:     (δ_nuc, δ_elec) → solid / liquid / gas / plasma / ...
```

The deeper insight: quantum mechanics uses the **second moment** of probability distributions (variance, spread, uncertainty) as a fundamental descriptor because the first moment is inherently uncertain. The δ framework extends this strategy to classical systems — wherever "how much particles spread" matters more than "where particles are," δ is the natural variable.

## Symbol Map

The framework uses a family of delocalization measures. Minimal orientation:

| Symbol | Meaning | Where | Status |
|--------|---------|-------|--------|
| δ | Umbrella: "how far particles spread" | everywhere | framework concept |
| δ_elec | Electronic delocalization | Papers 1–3 | core proposal; operational proxies cross-validated (r = 0.73–0.89) |
| δ_nuc | Nuclear delocalization | Paper 3, melting | coth-unified quantum↔classical (theory); for validation see z_nuc |
| z_nuc | Nuclear Resta phase (= translational order parameter, reinterpreted) | "solid / non-solid" axis | **validated in classical MD** (4/4 pre-registered criteria; melting detected as a 2-decade signal); AIMD pending |
| z_elec, λ² | Electronic Resta phase / localization length (Kohn–Resta–SWM lineage) | "metal / insulator" axis | computed: liquid Na (metallic, \|z\| ~ 10⁻⁵⁷) vs NaCl crystal (λ² = 1.03 Å², isotropic) |
| Ω, Ω_I | (Gauge-invariant) Wannier spread | optics sum rule | computed for C, Si, Ge, graphite, K |
| IPR | Inverse participation ratio | early proxy | superseded by the Ω/λ² route (fails to discriminate within identical structures) |
| D_eff | Effective conduction dimensionality | Paper 1 | validated on the carbon set; shown numerically = number of diverging-λ directions (TB) |
| s | Saturation index 2m_eE_gξ²/ℏ² | ML-descriptor map | computed for C/Si/Ge: separates gap-limited (Si 0.91) from core-screening-limited (Ge 0.16) |
| q300, f_ZP | Zero-point fraction of nuclear spread | isotope calibration; phase-0 map | calibrated from isotope shifts (H₂ 54% > Ne 12% > H₂O ~5%); 10k-material map in progress |

Full definitions: [`theory/core/glossary.md`](theory/core/glossary.md)

## Papers

Claims that have been numerically verified and survived self-criticism are written into papers.

### Paper 1: Optical Classification beyond the Band Gap

> *Classifying Optical Appearance beyond the Band Gap: Effective Conduction Dimensionality and Electronic Delocalization in Carbon Allotropes*

**Claim**: δ × D_eff classifies optical appearance (transparent / colored / black / lustrous) where band gap alone fails. Graphite and metals both have E_g ≈ 0, but D_eff distinguishes them (2 vs 3).

| Result | Value |
|--------|-------|
| E_g + D_eff decision tree accuracy | **6/7** (85.7%) |
| δ proxy intercorrelation | **r = 0.73–0.89** |
| δ–E_g inverse correlation | **r = −0.70** (lit.), **r = −0.86** (TB) |

Status: Preprint v8. **DOI: [10.5281/zenodo.19425523](https://zenodo.org/records/19425523)**

- Theory: [`theory/optics/02_glossiness_theory.md`](theory/optics/02_glossiness_theory.md)
- Code: [`simulation/optics/`](simulation/optics/)
- Draft: [`drafts/paper1_optics/main.tex`](drafts/paper1_optics/main.tex)

### Paper 2: Why Does Miedema's n_ws Work?

> *What Does Miedema's Boundary Electron Density Measure? Valence Electron Delocalization as the Physical Origin of n_ws*

**Claim**: Miedema's n_ws — the empirical predictor of surface tension for 45 years — is a proxy for valence electron delocalization δ_elec. This answers the question raised by Williams, Gelatt & Moruzzi (PRL, 1980): *why* does n_ws predict γ?

| Result | Value |
|--------|-------|
| δ_IPR (valence) vs midpoint density (15 dimers) | **r = 0.89** (p < 0.001) |
| sp/d interstitial density ratio (14-metal slabs) | **2.5×** (p = 0.00008) |
| Wannier spread sp/d ratio (5 metals) | **6–19×** |

Status: Preprint v8. **DOI: [10.5281/zenodo.19425541](https://zenodo.org/records/19425541)**

- Theory: [`theory/surface_tension/surface_tension_theory.md`](theory/surface_tension/surface_tension_theory.md)
- Code: [`simulation/surface_tension/`](simulation/surface_tension/)
- Draft: [`drafts/paper2_surface_tension/main.tex`](drafts/paper2_surface_tension/main.tex)

### Paper 3: A Phase-Descriptor Plane for Matter — What Is a Liquid? (planned)

**Hypothesis** (proposed, under numerical test): the (δ_nuc, δ_elec) plane — nuclear delocalization ("solid/non-solid" axis, via the nuclear Resta phase) × electronic delocalization ("metal/insulator" axis, via the localization length) — organizes solid, liquid, gas, metal and insulator in one coordinate system. The liquid–gas distinction is carried not by δ_nuc (both have mobile particles) but by δ_elec (electronic overlap → cohesion → fixed volume). Whether this *descriptor plane* can be upgraded to a *definition* of the liquid state is exactly what the numerical program is testing.

Status: Framework + methods validated on model systems (classical MD: 4/4 pre-registered criteria, melting detected; liquid-Na vs NaCl electronic contrast computed). Full liquid-state AIMD in progress.

- Theory: [`theory/phase/paper3_phase_diagram_theory.md`](theory/phase/paper3_phase_diagram_theory.md)

## Thinking Trail

The `theory/` directory records the reasoning process — how everyday questions land on existing mathematical structures.

### Core Framework
- [`theory/core/01_core_framework.md`](theory/core/01_core_framework.md) — δ × D_eff definition and optical classification
- [`theory/core/04_falsification.md`](theory/core/04_falsification.md) — What would break this framework (specific, quantitative)
- [`theory/core/glossary.md`](theory/core/glossary.md) — All symbols and definitions

### Key Connections (where ideas landed on existing physics)

| Memo | What it connects |
|------|-----------------|
| [`memo_quantum_classical_melting_crossover.md`](theory/connections/memo_quantum_classical_melting_crossover.md) | coth formula unifies quantum/classical δ_nuc; diffusion equation as δ_nuc's governing equation; why the 2nd moment is the right physical variable |
| [`memo_liquid_definition_via_omega.md`](theory/connections/memo_liquid_definition_via_omega.md) | Wannier spread Ω + diffusion → microscopic liquid definition (no prior work found) |
| [`memo_literature_and_sum_rule.md`](theory/connections/memo_literature_and_sum_rule.md) | Cardenas-Castillo (2024) sum rule makes δ→optics a theorem for frequency-integrated quantities |
| [`memo_remsing_klein_liquid_si.md`](theory/connections/memo_remsing_klein_liquid_si.md) | Remsing & Klein (2020) AIMD on liquid Si — closest prior work, 4 novelties remain |
| [`renyi_entropy_memo.md`](theory/phase/renyi_entropy_memo.md) | IPR = e^{−H₂} (Rényi entropy) — information-theoretic grounding of δ |
| [`05_gedig_connection.md`](theory/connections/05_gedig_connection.md) | Structural isomorphism between phase transitions and geDIG cognitive framework |
| [`memo_delta_vs_density.md`](theory/connections/memo_delta_vs_density.md) | δ (quantum: "how many sites?") vs n(r) (classical: "where?") — why the gap existed |
| [`memo_periodic_table_and_refractive_index.md`](theory/connections/memo_periodic_table_and_refractive_index.md) | δ alone fails for refractive index; three-factor correction n²−1 ∝ δ × α / E_g² |

### Other Connections
- [`memo_classical_uncertainty_and_coherence.md`](theory/connections/memo_classical_uncertainty_and_coherence.md) — Classical uncertainty as analog of quantum uncertainty
- [`memo_field_theories_and_entropy.md`](theory/connections/memo_field_theories_and_entropy.md) — δ as meta-descriptor across 5 existing field theories
- [`memo_mesoscale_quantum_classical.md`](theory/connections/memo_mesoscale_quantum_classical.md) — δ as effective mesoscale descriptor
- [`memo_dynamic_equilibrium_and_verification.md`](theory/connections/memo_dynamic_equilibrium_and_verification.md) — One-input three-output verification strategy
- [`liquid_lens_conjecture.md`](theory/connections/liquid_lens_conjecture.md) — Speculative: δ for variable-focus lens design

## Validation System

**Primary test bed: Carbon allotropes** (single element, structure as the only variable)

| Material | δ (π band width) | D_eff | E_g (eV) | Optical Response |
|----------|------------------|-------|----------|-----------------|
| Diamond | — (sp³, no π) | 0 | 5.47 | Transparent |
| C60 solid | 0.4–0.5 eV | 0 | 1.7–2.1 | Colored (dark purple) |
| SWCNT | 8–9 eV | 1 | 0–1.5 | Chirality-dependent |
| Graphene | ~9 eV | 2 | 0 | πα = 2.3%/layer |
| Graphite | ~9 eV (in-plane) | 2 | ~0 | Black + cleavage-plane luster |

**Control: h-BN** (same sp² structure as graphite, but low δ → transparent/white)

## Repository Structure

```
sento-optics/
├── theory/                             # Thinking trail
│   ├── core/                           #   Foundations (cross-paper)
│   ├── optics/                         #   Paper 1 theory
│   ├── surface_tension/                #   Paper 2 theory
│   ├── phase/                          #   Paper 3 theory
│   └── connections/                    #   Cross-domain connections
├── simulation/                         # Numerical verification
│   ├── optics/                         #   TB models, decision tree
│   └── surface_tension/                #   DFT slabs, Wannier, self-tests
├── data/                               # Literature data, datasets
├── drafts/                             # Paper manuscripts (LaTeX)
│   ├── paper1_optics/
│   └── paper2_surface_tension/
├── zenodo/                             # Preprint submission metadata
└── review/                             # Literature surveys, reviewer responses
```

## Theory's Job, Redefined

For most of the 20th century, theory's task ran all the way from principles to concrete predictions — *this compound, this structure, this property*. That last stretch is becoming machine work: universal ML potentials and generative models now explore material space faster and wider than any human theorist.

What remains — and grows — is what machines cannot supply:

1. **Inventing variables.** ML interpolates within a given representation; deciding *which quantity to see the world through* (the d-band center, topological invariants, δ) is still theory's job.
2. **Supplying constraints.** ML predictions break silently outside the training distribution. Inequalities and sum rules (e.g., ξ² ≤ ℏ²/2m_eE_g) are walls that survive extrapolation.
3. **Inventing questions.** "What is a liquid?" does not emerge from a dataset.
4. **Understanding.** Compressing ten thousand predictions into one sentence — *luster is the divergence of a localization length* — is not a by-product of prediction.

This program is built on that division of labor: theory's deliverable here is the *definition* of (δ_nuc, δ_elec) — parameter-free, automatable, self-diagnosing — and the downstream exploration of material space is a numbers game for machines (see [`drafts/strategy_ml_descriptor_2026-07-05.md`](drafts/strategy_ml_descriptor_2026-07-05.md)). The workflow of this repository — human intuition upstream, AI-assisted formalization and mass verification downstream — is itself a small-scale rehearsal of that future.

## AI Usage Disclosure

**Author's original intuition:** The origin question ("What is a liquid?"), the bathhouse observations (luster + surface tension as interface properties), and the hypothesis that particle delocalization δ unifies them — these were conceived entirely by the author.

**AI-assisted formalization:** Translation of intuitions into a quantitative framework — tight-binding simulations, DFT calculations, Wannier analysis, statistical validation, self-criticism tests, and manuscript drafting — was carried out collaboratively with Claude (Anthropic) and ChatGPT (OpenAI). The author independently verifies all datasets, code, and scientific claims. Full scientific responsibility rests with the author.

## How to Cite

> Miyauchi, K. (2026). *Phenomenological unification of optical response in carbon allotropes via electron delocalization index δ and effective conduction dimensionality D_eff.* Preprint. GitHub: [sento-optics](https://github.com/miyauchikazuyoshi/sento-optics)

## Feedback Welcome

This is work in progress by an independent researcher. Expert review, criticism, and pointed questions are actively sought. If you find a flaw in the logic, a missing reference, or a better way to test the hypothesis, please open an issue. The self-criticism tests in this repo exist because a hypothesis worth proposing is a hypothesis worth trying to break.

## License

This work is shared for academic discussion. Please cite appropriately if referencing this framework.
