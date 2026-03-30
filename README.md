# sento-optics: Phenomenological Unification of Optical Response via Electron Delocalization

> **"Why do liquids shine?"** — A question born in a Japanese *sentō* (public bathhouse), March 27, 2026.

## Core Thesis

The macroscopic optical response of materials — transparent, colored, black, or lustrous — can be phenomenologically unified using two variables:

- **δ (delocalization index):** How freely electrons move (quantified via band width, effective mass, or band gap as proxies)
- **D_eff (effective optical conduction dimensionality):** In how many spatial directions those free electrons can respond to photons

### Key Insight

**Luster is the preservation of photon phase coherence at an interface.** What preserves phase coherence? The freedom of constituent particles:
- In metals, free electrons (high δ_elec) respond collectively → coherent reflection
- In liquids, free molecules (high δ_nuc) self-smooth the interface → coherent reflection
- In insulators, localized particles respond incoherently → no luster

Band gap *E*_g alone cannot explain why graphite (E_g ≈ 0) is black while metals (E_g = 0) are shiny. The δ × D_eff framework resolves this: graphite has D_eff = 2 (in-plane only), while metals have D_eff = 3.

### Important Positioning
- This framework is a **strong phenomenological unifying hypothesis**, not a universal theory
- δ is an **operationally defined** effective indicator (candidate proxies: IPR, Wannier spread, band width, inverse effective mass)
- D_eff is **not** crystallographic dimensionality but the effective conduction dimensionality contributing to low-energy optical response
- The framework **does not replace** band-gap theory but **subsumes** it: E_g is reinterpreted as an intermediate variable derivable from δ

## Status: Verified at Proof-of-Concept Level

| Milestone | Result |
|-----------|--------|
| E_g + D_eff decision tree → optical class | **6/7 correct** (85.7%) — only graphene single-layer misclassified |
| δ(1/m*) × D_eff machine classification | **3/7 correct** (42.9%) — threshold-sensitive; see Sec. 4 |
| δ proxy intercorrelation | **r = 0.73–0.89** (3 independent proxies) |
| δ–E_g inverse correlation | **r = −0.70** (literature data), **r = −0.86** (TB model) |
| Graphene–graphite distinction | Requires layer count N as additional parameter (Beer–Lambert) |
| Prior art search | **No existing unified framework found** (as of March 2026) |
| All data from published literature | **No first-principles calculations required** |

## Validation System

**Primary: Carbon allotropes** (single element, structure as the only variable)

| Material | δ (π band width) | D_eff | E_g (eV) | Optical Response |
|----------|------------------|-------|----------|-----------------|
| Diamond | — (sp³, no π) | 0 | 5.47 | Transparent |
| C60 solid | 0.4–0.5 eV | 0 | 1.7–2.1 | Colored (dark purple) |
| SWCNT | 8–9 eV | 1 | 0–1.5 | Chirality-dependent |
| Graphene | ~9 eV | 2 | 0 | πα = 2.3%/layer |
| Graphite | ~9 eV (in-plane) | 2 | ~0 | Black + cleavage-plane luster |

**Control: h-BN** (same layered sp² crystal structure as graphite, but low δ due to B–N electronegativity difference → D_eff = 0, transparent/white)

## Repository Structure

```
sento-optics/
├── README.md                        # This file
├── README_ja.md                     # Japanese README
├── theory/
│   ├── 01_core_framework.md         # Core framework: δ × D_eff
│   ├── 02_glossiness_theory.md      # Phenomenological redescription of luster
│   ├── 04_falsification.md          # Falsification conditions
│   └── extensions/                  # Beyond main paper scope (future work)
│       ├── 03_phase_unification.md  # Continuous unification of phases
│       └── 05_gedig_connection.md   # Connection to geDIG
├── data/
│   ├── carbon_allotropes.md         # Carbon allotrope optical data
│   ├── dataset_v1.csv               # Quantitative dataset (open)
│   ├── delta_proxy_database.md      # δ proxy values from literature
│   └── supporting_evidence.md       # Supporting evidence (Ga, NH₃, etc.)
├── simulation/
│   ├── algorithm_spec.md            # Simulation algorithm specification
│   ├── delocalization_optics_v2.py  # Proof-of-concept TB models
│   ├── classification_v2.py         # Decision tree & statistical validation
│   ├── plot_delta_deff_map.py       # δ × D_eff map plotting
│   ├── plot_figures_en.py           # English figure generation
│   ├── quantitative_validation.py   # Quantitative validation scripts
│   └── figures/                     # Generated figures (9 total)
├── review/
│   └── reviewer_response.md         # Review feedback and responses
├── references/
│   └── bibliography.md              # Full bibliography
└── drafts/
    ├── main.tex                     # LaTeX manuscript draft
    ├── main.pdf                     # Compiled PDF
    ├── references.bib               # BibTeX references
    └── paper_skeleton.md            # Paper skeleton (Japanese)
```

## Key Predictions (Testable)

1. Optical properties of carbon allotropes are systematically organized by δ × D_eff
2. The linearity of graphene absorption with layer count is consistent with the δ × D_eff framework
3. The whiteness of h-BN is explained as "same D_eff, low δ" in the first approximation
4. Materials with similar δ × D_eff values fall into the same optical response category

## Future Directions

### Surface Tension via δ (Paper 2 — in progress)

Surface tension γ is another interface property governed by electronic structure. We propose a causal chain:

**δ_IPR → n_ws → γ**

where δ_IPR (inverse participation ratio of Kohn–Sham orbitals) determines how much charge reaches the Wigner–Seitz cell boundary (Miedema's n_ws), which in turn determines surface tension.

**Key results so far:**
- DFT calculations on 11 metal dimers show r = 0.84 (p = 0.001) between δ_IPR and boundary electron density
- δ_IPR is mathematically distinct from normalized density n/n̄ (mean r = 0.10, DFT verified)
- The Al/Zn problem (Δr_s = 2.4%, Δγ = 46%) is qualitatively explained by sp vs. d-electron delocalization

**Current limitations (honestly stated):**
- The δ_IPR → n_ws correlation uses isolated dimers as proxies for bulk metals — slab calculations are needed
- δ does not yet *predict* γ better than Miedema's established n_ws model
- The "bridge" between optical response and surface tension is conceptual, not yet quantitative
- Several initial hypotheses were falsified by self-criticism tests (γ ∝ ∫(dδ/dz)², water density anomaly prediction)
- See `drafts/paper2_surface_tension/THEORY_NOTES.md` for the full research map

**The bigger picture:** Both reflectivity R and surface tension γ are responses of the *same* electronic discontinuity at an interface — photons probe it electromagnetically, surface area changes probe it thermodynamically. No existing framework connects these two interface properties through a single electronic descriptor. δ is a candidate for that connection.

### Other future directions

- **Liquid luster:** Extension to nuclear delocalization δ_nuc (liquid Ga reflectivity jump at melting)
- **Catalysis:** δ_surface as predictor of catalytic activity (connection to d-band center theory)
- **Interface phenomena:** Δδ at heterointerfaces as a driving force for novel optical response
- **Inverse design:** From desired optical response → required (δ, D_eff) → material structure

## AI Usage Disclosure

The core hypothesis ("particle freedom determines photon coherence preservation") was conceived by the author. Experimental design, literature data collection, quantitative validation, code development, and manuscript drafting were conducted with substantial AI assistance (Claude, Anthropic). The author independently verifies all datasets and code. Full scientific responsibility rests with the author.

## How to Cite

> Miyauchi, K. (2026). *Phenomenological unification of optical response in carbon allotropes via electron delocalization index δ and effective conduction dimensionality D_eff.* Preprint. GitHub: [sento-optics](https://github.com/miyauchikazuyoshi/sento-optics)

## License

This work is shared for academic discussion. Please cite appropriately if referencing this framework.
