# sento-optics: Electronic Delocalization as a Unifying Descriptor for Interface Properties

> **"What is a liquid, really?"** — A question born in a Japanese *sentō* (public bathhouse), March 27, 2026.

## Origin

Staring at the bathwater surface, two observations:

1. **Liquids shine.** The water surface reflects light coherently, just like a metal mirror.
2. **Liquids have surface tension.** The water holds its shape against gravity, forming a meniscus.

Both are *interface properties* — they arise where one phase meets another.
Both are well-described macroscopically (Fresnel equations, Young-Laplace equation).
But neither has a satisfying *microscopic* explanation rooted in electronic structure.

Existing definitions of "liquid" are macroscopic: "a state that has definite volume but no definite shape." What is the microscopic definition? What *electronic* property makes a liquid a liquid?

### The Hypothesis

These interface properties can be unified through a single variable: the **spatial delocalization of constituent particles** — defined as an inter-particle interaction quantity that governs the existence probability of particles at interfaces.

- **Luster** = preservation of photon phase coherence at the interface. Delocalized particles (free electrons in metals, free molecules in liquids) respond collectively, maintaining coherence. Localized particles respond incoherently — no luster.
- **Surface tension** = the thermodynamic cost of creating an interface. How much charge reaches the cell boundary (Miedema's n_ws) is determined by how delocalized the valence electrons are.

Both chains start from the same electronic property **δ** (delocalization index):

```
Optical response:   δ × D_eff → ε(ω) → R(ω)
Surface tension:    δ → n_ws → γ
```

## Framework

Two variables classify the macroscopic optical response of materials — transparent, colored, black, or lustrous:

- **δ (delocalization index):** How freely electrons move (quantified via IPR, Wannier spread, band width, or inverse effective mass)
- **D_eff (effective optical conduction dimensionality):** In how many spatial directions those free electrons can respond to photons

Band gap *E*_g alone cannot explain why graphite (E_g ≈ 0) is black while metals (E_g = 0) are shiny. The δ × D_eff framework resolves this: graphite has D_eff = 2 (in-plane only), while metals have D_eff = 3.

### Important Positioning
- This framework is a **strong phenomenological unifying hypothesis**, not a universal theory
- δ is an **operationally defined** effective indicator (candidate proxies: IPR, Wannier spread, band width, inverse effective mass)
- D_eff is **not** crystallographic dimensionality but the effective conduction dimensionality contributing to low-energy optical response
- The framework **does not replace** band-gap theory but **subsumes** it: E_g is reinterpreted as an intermediate variable derivable from δ

## Status: Verified at Proof-of-Concept Level

| Milestone | Result |
|-----------|--------|
| E_g + D_eff decision tree → optical class | **6/7 correct** (85.7%) — 7/7 with layer count N as third variable |
| δ(1/m*) × D_eff machine classification | **3/7** (42.9%) — threshold-sensitive; graphene-graphite problem is a genuine limitation |
| δ proxy intercorrelation | **r = 0.73–0.89** (3 independent proxies) |
| δ–E_g inverse correlation | **r = −0.70** (literature data), **r = −0.86** (TB model) |
| Graphene–graphite distinction | Requires layer count N as additional parameter (Beer–Lambert) |
| Prior art search | **No existing unified framework found** (as of March 2026) |
| Paper 1 data from published literature | Paper 2 includes DFT slab and Wannier calculations |

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
├── README.md                           # This file
├── README_ja.md                        # Japanese README
├── theory/                             # Theoretical framework
│   ├── core/                           #   Cross-paper foundations
│   │   ├── 01_core_framework.md        #     δ × D_eff framework definition
│   │   ├── 04_falsification.md         #     Falsification conditions
│   │   └── glossary.md                 #     Symbol/term definitions
│   ├── optics/                         #   Paper 1: Optical theory
│   │   └── 02_glossiness_theory.md     #     Luster as phase-coherent interface response
│   ├── surface_tension/                #   Paper 2: Surface tension theory
│   │   └── surface_tension_theory.md   #     δ → n_ws origin explanation
│   ├── phase/                          #   Paper 3: Phase classification
│   │   ├── paper3_phase_diagram_theory.md  # (δ_nuc, δ_elec) phase diagram
│   │   └── renyi_entropy_memo.md       #     IPR = e^{-H₂} information-theoretic basis
│   └── connections/                    #   Cross-domain connections
│       ├── memo_delta_vs_density.md    #     δ vs density functional theory
│       └── 05_gedig_connection.md      #     geDIG connection
├── data/                               # Literature data
│   ├── carbon_allotropes.md
│   ├── dataset_v1.csv
│   └── delta_proxy_database.md
├── simulation/
│   ├── optics/                         # Paper 1: Optical response
│   │   ├── delocalization_optics_v2.py #   TB models (graphene, diamond, C60, 1D)
│   │   ├── classification_v2.py        #   Decision tree validation
│   │   ├── plot_*.py                   #   Figure generation
│   │   └── figures/                    #   Generated plots
│   └── surface_tension/               # Paper 2: Surface tension
│       ├── test1–7_*.py                #   Self-criticism tests
│       └── qe_slab/                    #   DFT slab calculations (QE)
│           ├── *_scf.in                #     5-metal slab inputs
│           ├── plot_valence_ablation.py #    Ablation: full vs valence
│           └── wannier/                #     MLWF spread calculations
│               ├── run_wannier_all.py  #       Wannier90 pipeline
│               └── plot_wannier_summary.py
├── drafts/
│   ├── paper1_optics/                  # Paper 1 manuscript
│   │   ├── main.tex                    #   Latest draft (v7)
│   │   └── references.bib
│   └── paper2_surface_tension/         # Paper 2 manuscript
│       ├── main.tex                    #   Latest draft (v6)
│       └── references.bib
└── review/                             # Reviewer responses & literature
    ├── stanford_reviewer_response_paper1.md
    ├── stanford_reviewer_response.md   #   Paper 2
    └── literature_survey_results.md
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

**Key results:**
- DFT calculations on 11 metal dimers: r = 0.84 (p = 0.001) between δ_IPR and boundary electron density
- **5-metal slab calculations** (Na, K, Al, Cu, Zn): valence electron decomposition shows sp metals have near-uniform interstitial density (Na: 1.09, K: 1.13, Al: 0.96) while d-metals show strong depletion (Cu: 0.33, Zn: 0.28) — a 3.5× ratio
- **Ablation study**: full-electron density *masks* this trend for alkali metals (core electron contamination); valence decomposition recovers the correct sp > d ordering for all five metals
- **Wannier spread** (MLWF, bulk calculations): sp metals (Al: 12.9, Na: 11.7 Å²) have 6–19× larger average spreads than d-metals (Cu: 1.9, Zn: 0.7 Å²), confirming the delocalization hierarchy without invoking surfaces

**Current limitations (honestly stated):**
- δ does not yet *predict* γ better than Miedema's established n_ws model — it is an *explanatory* descriptor, not a predictive one
- The "bridge" between optical response and surface tension is conceptual, not yet quantitative
- Several initial hypotheses were falsified by self-criticism tests (γ ∝ ∫(dδ/dz)², water density anomaly prediction)

**The bigger picture:** Both reflectivity R and surface tension γ are responses of the *same* electronic discontinuity at an interface — photons probe it electromagnetically, surface area changes probe it thermodynamically. No existing framework connects these two interface properties through a single electronic descriptor. δ is a candidate for that connection.

### Microscopic Redefinition of "Liquid" (Paper 3 — planned)

The original question: what *is* a liquid, microscopically?

Existing definitions are macroscopic ("definite volume, no definite shape"). We propose that the liquid state can be characterized microscopically through nuclear delocalization δ_nuc — the spatial freedom of nuclei/molecules — which determines interface coherence and surface tension simultaneously.

- **Liquid Ga**: reflectivity jumps at melting → nuclear delocalization onset
- **Water**: anomalous surface tension from hydrogen-bond network (δ_nuc constrained)
- **Liquid metals**: high γ from electronic delocalization + nuclear freedom

### Other future directions

- **Catalysis:** δ_surface as predictor of catalytic activity (connection to d-band center theory)
- **Interface phenomena:** Δδ at heterointerfaces as a driving force for novel optical response
- **Inverse design:** From desired optical response → required (δ, D_eff) → material structure

## AI Usage Disclosure

**Author's original intuition (steps 1–5):**
The origin question ("What is a liquid?"), the two observations at the bathhouse (luster + surface tension), the recognition that both are interface properties lacking microscopic explanations, and the hypothesis that particle delocalization δ unifies them — these were conceived entirely by the author.

**AI-assisted formalization (step 6 onward):**
The translation of these intuitions into a quantitative framework — tight-binding simulations, DFT slab calculations, valence electron decomposition, Wannier spread analysis, statistical validation, self-criticism tests, and manuscript drafting — was carried out collaboratively with Claude (Anthropic). The author independently verifies all datasets, code, and scientific claims. Full scientific responsibility rests with the author.

## How to Cite

> Miyauchi, K. (2026). *Phenomenological unification of optical response in carbon allotropes via electron delocalization index δ and effective conduction dimensionality D_eff.* Preprint. GitHub: [sento-optics](https://github.com/miyauchikazuyoshi/sento-optics)

## Feedback Welcome

This is work in progress by an independent researcher. Expert review, criticism, and pointed questions are not just welcome — they are actively sought. If you find a flaw in the logic, a missing reference, or a better way to test the hypothesis, please open an issue or reach out. The self-criticism tests in this repo exist because the author believes a hypothesis worth proposing is a hypothesis worth trying to break.

## License

This work is shared for academic discussion. Please cite appropriately if referencing this framework.
