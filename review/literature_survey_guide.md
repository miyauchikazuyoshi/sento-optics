# Literature Survey Guide

Copilot reviewer's criticism #8: "No existing unified framework found" needs stronger literature backing.
Goal: Identify prior art, differentiate clearly, or acknowledge overlap honestly.

---

## Paper 1: Optical Response

### A. Unified optical classification frameworks

**Search terms:**
- `"optical classification" metal insulator semiconductor`
- `"optical response" "electronic structure" unifying framework`
- `"dielectric function" classification "band structure"`
- `Penn model dielectric`
- `Moss rule optical`

**Must-read:**
- [ ] Penn, D. R. (1962). "Wave-Number-Dependent Dielectric Function of Semiconductors." *Phys. Rev.* 128, 2093.
  - Why: Derives ε(ω) from E_g. Our framework subsumes E_g into δ — need to show what δ×D_eff adds beyond Penn.
- [ ] Moss, T. S. (1985). "Relations between the Refractive Index and Energy Gap of Semiconductors." *Phys. Status Solidi B* 131, 415.
  - Why: n⁴ × E_g = const. Empirical rule connecting optics to band gap. δ reinterprets this.
- [ ] Harrison, W. A. (1980). *Electronic Structure and the Properties of Solids.* Freeman.
  - Why: Systematic connection of electronic structure to material properties. Check if δ-like concept exists.
- [ ] Dressel & Gruner (2002). *Electrodynamics of Solids.* Cambridge.
  - Why: Modern treatment of optical properties from electronic structure. Standard reference.

### B. Luster / coherence physics

**Search terms:**
- `"specular reflection" "electronic structure" mechanism`
- `"metallic luster" origin electron`
- `Bennett Porteus surface scattering reflectance`
- `Ewald Oseen extinction theorem reflection`
- `"coherent reflection" "free electron"`

**Must-read:**
- [ ] Bennett, H. E. & Porteus, J. O. (1961). "Relation Between Surface Roughness and Specular Reflectance at Normal Incidence." *JOSA* 51, 123.
  - Why: Quantifies when a surface is "smooth enough" to reflect coherently. Our claim is that δ determines this microscopically.
- [ ] Born & Wolf, *Principles of Optics* — Ewald-Oseen extinction theorem (Ch. 2).
  - Why: Microscopic theory of how reflection arises from induced dipoles. δ governs the collective response strength.
- [ ] Wooten, F. (1972). *Optical Properties of Solids.* Academic Press.
  - Why: Standard textbook. Check Chapter 5 (free electron metals) and Chapter 6 (interband transitions).
- [ ] de Groot, S. R. & Vlieger, J. (1971). "Derivation of Maxwell's equations: the method of induced sources."
  - Why: Rigorous derivation of Fresnel equations from microscopic theory. Relevant to coherence argument.

### C. Dimensionality and optical properties

**Search terms:**
- `"dimensionality" "optical properties" "low-dimensional"`
- `"anisotropic" "dielectric tensor" graphite`
- `"optical conductivity" carbon allotrope`

**Must-read:**
- [ ] Dresselhaus, M. S. et al. — Review articles on carbon nanotubes / graphite optical properties.
  - Why: D_eff is essentially "effective conduction dimensionality" — Dresselhaus's work implicitly uses this concept for carbon.
- [ ] Mak, K. F. et al. (2008). "Measurement of the Optical Conductivity of Graphene." *Phys. Rev. Lett.* 101, 196405.
  - Why: The πα = 2.3% per layer result. Our framework should reproduce/explain this.
- [ ] Nair, R. R. et al. (2008). "Fine Structure Constant Defines Visual Transparency of Graphene." *Science* 320, 1308.
  - Why: Same result, different group. The "fine structure constant" interpretation is what our framework reinterprets in terms of δ×D_eff.

---

## Paper 2: Surface Tension

### D. Electronic origin of surface tension/energy

**Search terms:**
- `"surface tension" "electronic structure" metal`
- `"surface energy" "electron density" metal DFT`
- `Lang Kohn surface energy jellium`
- `Vitos surface energy DFT metals`
- `Skriver Rosengaard surface energy`

**Must-read:**
- [ ] Lang, N. D. & Kohn, W. (1970). "Theory of Metal Surfaces: Charge Density and Surface Energy." *Phys. Rev. B* 1, 4555.
  - Why: Foundation of all jellium surface theory. Our δ-gradient idea was inspired by this but falsified — need to cite and explain why.
- [ ] Lang, N. D. & Kohn, W. (1971). "Theory of Metal Surfaces: Work Function." *Phys. Rev. B* 3, 1215.
  - Why: Companion paper. Work function is another interface property — potential connection to δ.
- [ ] Vitos, L. et al. (1998). "The surface energy of metals." *Surf. Sci.* 411, 186.
  - Why: DFT surface energies for 28 metals. Already cited. Confirm we're not claiming something they already showed.
- [ ] Skriver, H. L. & Rosengaard, N. M. (1992). "Surface energy and work function of elemental metals." *Phys. Rev. B* 46, 7157.
  - Why: Same type of calculation, earlier. Check if they discuss electron localization.
- [ ] Tran, F. et al. (2016). "Surface energies of elemental crystals." *Sci. Data* 3, 160080.
  - Why: Modern comprehensive DFT dataset. Already cited.

### E. Miedema model — physical basis

**Search terms:**
- `Miedema model "physical basis" OR "microscopic origin"`
- `"boundary density" "electron density" Wigner-Seitz`
- `"charge density" "cell boundary" metal alloy`
- `Chelikowsky Miedema`

**Must-read:**
- [ ] de Boer, F. R. et al. (1988). *Cohesion in Metals.* North-Holland.
  - Why: Already cited. The bible of Miedema model. Re-read Chapter 1 for physical justification of n_ws.
- [ ] Chelikowsky, J. R. (1979). "Predictions for surface segregation in intermetallic alloys." *Surf. Sci.* 139, L197.
  - Why: Uses Miedema parameters for surfaces. Check if n_ws is given physical interpretation.
- [ ] Alonso, J. A. & Girifalco, L. A. (1978). "Nonlocal approximation to the exchange potential and kinetic energy of an inhomogeneous electron gas." *Phys. Rev. B* 17, 3735.
  - Why: Theoretical justification for Miedema-like models.

### F. Localization measures and material properties

**Search terms:**
- `"electron localization function" ELF surface energy`
- `"inverse participation ratio" metal OR solid state`
- `"Wannier spread" OR "Wannier function" localization physical property`
- `"d-band center" surface energy OR surface tension`
- `Becke Edgecombe ELF`

**Must-read:**
- [ ] Becke, A. D. & Edgecombe, K. E. (1990). "A simple measure of electron localization in atomic and molecular systems." *J. Chem. Phys.* 92, 5397.
  - Why: ELF is the most established localization measure. We must explain how δ_IPR differs and why ELF hasn't been connected to γ.
- [ ] Savin, A. et al. (1992). "Electron Localization in Solid-State Structures of the Elements: the Diamond Structure." *Angew. Chem. Int. Ed.* 31, 187.
  - Why: ELF applied to solids. Check if surface properties were discussed.
- [ ] Hammer, B. & Norskov, J. K. (1995). "Why gold is the noblest of all the metals." *Nature* 376, 238.
  - Why: d-band center theory. Already cited. Key differentiation: d-band center → adsorption, δ → surface tension.
- [ ] Marzari, N. & Vanderbilt, D. (1997). "Maximally localized generalized Wannier functions..." *Phys. Rev. B* 56, 12847.
  - Why: Foundation of MLWF. We use Wannier spread — need to cite the original.

---

## Survey Strategy

### Phase 1: Google Scholar quick scan (1-2 hours)
1. Search each keyword set above
2. For each result: read title + abstract only
3. Star anything that looks relevant
4. Pay special attention to review articles — they map the landscape

### Phase 2: Citation chain (2-3 hours)
1. For each must-read paper: check "cited by" list
2. For our own papers: check if any cited paper already does something similar
3. Look for the phrase "to our knowledge, no..." in related papers — if they say it too, it's a good sign

### Phase 3: Write the differentiation (1-2 hours)
For each relevant prior work found, write one paragraph:
1. What they did
2. What we do differently
3. Why the difference matters

### Red flags to watch for
- Someone already connected IPR/ELF/Wannier spread to surface tension → major overlap
- Someone already classified optical response with a 2-variable framework → direct competitor
- Someone already explained metallic luster microscopically beyond Fresnel → weakens our novelty claim

### Green flags
- Papers that compute surface energy numerically (DFT) but explicitly say "the physical mechanism is unclear" → validates our niche
- Papers that use ELF for bonding but not for surface tension → confirms the gap we fill
- Review articles that list "open questions" matching our claims → strong positioning
