# Surface Tension Theory: Research Map

## 1. Existing Theories and Their Scope

### First-Principles (Numerical)

**Lang-Kohn Jellium (1970)**
- Input: r_s only (Wigner-Seitz radius)
- Method: KS-DFT for semi-infinite jellium, LDA
- Accuracy: ±25% for alkali metals (Na, K, Rb, Cs)
- Fatal flaw: **negative surface energy for r_s < 2.5** (Al, Zn, Cu)
  - The jellium is not mechanically stable at all densities
  - High-density metals get unphysical results
- Cannot distinguish Al (r_s=2.07, γ=1140) from Zn (r_s=2.12, γ=782)
- Ref: Lang & Kohn, Phys. Rev. B 1, 4555 (1970)

**Stabilized Jellium (Perdew 1990)**
- Adds a constant pseudopotential to stabilize jellium at observed density
- Fixes negative γ problem
- Still r_s-only; still no d-band physics
- Ref: Perdew et al., Phys. Rev. B 42, 11627 (1990)

**Modern DFT Slab Calculations**
- Vitos et al. (1998): FCD-LMTO, 60 metals, LDA/GGA → ±10% for 4d series
- Singh-Miller & Marzari (2009): plane-wave PBE → neither LDA nor PBE is reliable default
- Tran et al. (2016): Sci. Data 3, 160080 — comprehensive database
- Peng et al. (2017): SCAN+rVV10 → improved, but still functional-dependent
- **Key limitation**: gives numbers, not understanding. No analytical formula.
  DFT can compute γ_Al ≠ γ_Zn, but cannot say *why* in terms of a descriptor.

### Semi-Empirical

**Miedema (1978)**
- Inputs: n_ws (boundary electron density) and φ* (adjusted electronegativity)
- Formula: γ ∝ n_ws^(5/3) / V_m^(2/3) (for pure metals)
- Accuracy: ±10-20% across periodic table including d-metals
- n_ws is **empirically calibrated**, not measured directly
- Physically: n_ws represents electron density at the Wigner-Seitz cell boundary
  - sp metals: electrons uniform → n_ws ≈ n_bar
  - d metals: d-electrons localized near nucleus → n_ws < n_bar
- Ref: Miedema, Z. Metallkd. 69, 287 (1978); de Boer et al., Cohesion in Metals (1988)

**Skapski Broken-Bond (1948)**
- γ ~ (Z_s/Z_b) × ΔH_sub / V^(2/3)
- Classical: count broken bonds per area
- No electronic structure
- Ref: Skapski, J. Chem. Phys. 16, 386 (1948)

### Empirical Rules
- **Eötvös (1886)**: γ V^(2/3) = k(T_c - T)
- **Guggenheim (1945)**: γ = γ₀(1 - T/T_c)^n, n ≈ 11/9

## 2. Open Problems (Gaps)

### Gap 1: Al/Zn Problem (No Analytical Descriptor)
- r_s: 2.07 vs 2.12 (2.4% difference)
- γ: 1140 vs 782 (46% difference)
- Jellium: cannot distinguish (same r_s → same γ)
- DFT: can compute, but gives no *reason*
- Miedema: n_ws(Al) > n_ws(Zn) helps, but n_ws is empirical
- **What's missing**: a descriptor from electronic structure that explains
  why Al's electrons contribute more to surface tension than Zn's

### Gap 2: d-Electron Effects
- d-band center (Hammer-Nørskov) → chemisorption energies, NOT surface energies
- No established descriptor separates d-electron contribution to γ
- Known that d-electrons are more localized → affect surface dipole, spillover
- But no quantitative measure exists

### Gap 3: IPR/Delocalization → γ (Unexplored)
- **No published work** connects IPR, delocalization index, or participation
  ratio to surface tension prediction
- ELF (electron localization function) has been used for bonding analysis
  at surfaces, but not for γ prediction
- This is genuinely unoccupied territory

### Gap 4: Optics ↔ Surface Tension
- Both depend on electronic structure
- ω_p ~ √n determines both Drude reflectivity and (via r_s) surface energy
- But **no theory formalizes this connection**
- Our Paper 1 (δ → optical classification) could bridge to γ if δ → n_ws

### Gap 5: γ(T) from First Principles
- Temperature dependence predicted only by empirical fits
- Surface entropy (dγ/dT) origin unknown: configurational? vibrational? electronic?
- DFT is T=0; AIMD too expensive to converge γ(T)

### Gap 6: Liquid Metal Surfaces Specifically
- Solid γ / liquid γ ≈ 1.0-1.25 (Tyson-Miller 1977) — empirical
- No microscopic derivation of this ratio
- Surface layering in liquid metals (2024 Acta Mater.) — connection to γ unclear

## 3. Where δ Fits

### What δ CANNOT Claim
- ~~"γ ∝ ∫(dδ/dz)²"~~ — falsified (Test 2: δ = n/n̄ → trivially = n_bar^(1/6))
- ~~"δ predicts γ"~~ — no, Miedema/DFT already predict γ better
- ~~"δ unifies everything"~~ — overreach with current evidence

### What δ CAN Claim
1. **δ_IPR ≠ n/n̄**: DFT confirms they are mathematically distinct (Test 1, mean r=0.10)
2. **δ_IPR explains n_ws**: delocalized electrons reach cell boundaries (Test 7, r=0.87 for dimers)
3. **δ bridges optics and surface tension**: Paper 1 shows δ → ε(ω); if δ → n_ws → γ,
   then the same electronic property governs both
4. **δ provides the "why" that DFT lacks**: why does Al have higher γ than Zn?
   Because Al's sp electrons are more delocalized (higher δ) → more electrons at
   the cell boundary (higher n_ws) → higher surface tension
5. **δ is the first electronic descriptor proposed for γ across sp and d metals**

### Proposed Paper 2 Structure (Revised)
1. **Introduction**: Surface tension is understood numerically (DFT) and empirically (Miedema)
   but lacks an analytical electronic descriptor → introduce δ
2. **Theory**: Review Lang-Kohn, Miedema, stabilized jellium. Show the gap.
3. **Methods**: DFT clusters → compute IPR-δ and boundary density simultaneously
4. **Results**:
   - δ_IPR correlates with n_ws (DFT evidence)
   - The causal chain: δ → n_ws → γ (via Miedema)
   - Al/Zn explained by δ (sp vs d delocalization)
   - Connection to Paper 1: same δ governs optical response
5. **Discussion**: δ reinterprets Miedema's n_ws, does not replace it.
   Analogy: Paper 1's δ×D_eff for optics ↔ Paper 2's δ→n_ws for γ.

## 4. Self-Criticism Test Results (2026-03-30)

| Test | Result | Implication |
|------|--------|-------------|
| 1. DFT IPR | PASS: δ_IPR ≠ n/n̄ | δ is a distinct quantity |
| 2. Monotonicity | FAIL: r=0.956 is spurious | Original jellium model is invalid |
| 3. d_fraction | Mixed: DOS-weighted works | d-band physics matters but needs proper basis |
| 4. Water literature | FAIL: T_max not predicted | Water model was curve fitting |
| 5. n_ws | n_ws >> n̄ (r=0.922 vs 0.690) | n_ws is the right variable |
| 6. n_ws×δ | Marginal improvement | 12-point data insufficient to separate |
| 7. δ→n_ws | r=0.87 (dimers) | Causal chain supported but needs more data |
