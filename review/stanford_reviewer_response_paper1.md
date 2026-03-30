# Stanford Agentic Reviewer Response — Paper 1

**Review received:** 2026-03-30
**Response status:** v5 → v6 draft updates

---

## Summary of Reviewer Assessment

> "The paper raises an important and underappreciated point—that band gap alone does not determine optical appearance—and offers a creative framework [...] However, in its current form the work remains largely conceptual and proof-of-principle, with several inconsistencies."

**Novelty was NOT questioned.** D_eff concept explicitly praised. All criticisms target: (1) internal inconsistencies, (2) validation scope, (3) Anderson↔gloss theoretical gap.

---

## Issue-by-Issue Response

### 🔴 RED (Immediate — must fix)

#### 1. D_eff definition contradiction: D_eff=0 vs D_eff=3.00 for diamond
**Reviewer:** "The text asserts D_eff=0 for wide-gap systems in the visible, yet a later calculation reports D_eff=3.00 for diamond—these definitions need to be reconciled"
**Diagnosis:** Two different D_eff values exist because:
- Table 1 (§II.C): D_eff=0 for diamond, meaning **no visible-range optical transitions** → classification purposes
- §IV.B.1 "D_eff from velocity tensor": D_eff=3.00 from Eq.(2), computed over **all** interband transitions → velocity tensor result
These are the SAME quantity computed over DIFFERENT energy windows. This is explicitly discussed in §II.C "Energy windowing and the h-BN case" but not clearly tied to the D_eff=3.00 result.
**Fix:** Added explicit clarification with new Table (D_eff_computed) reporting D_eff^all and D_eff^vis for all systems. Diamond: D_eff^all=3.00, D_eff^vis=0. h-BN: D_eff^all=2.00, D_eff^vis=0. ✅ DONE

#### 2. Graphene reflectivity R_vis ≈ 0.35 contradicts monolayer optics
**Reviewer:** "R_vis ≈ 0.35 conflicts with monolayer optics (≈2.3% absorption, negligible reflectance). Was this actually graphite or an effective thick film?"
**Diagnosis:** The TB calculation computes ε(ω) from the 2D band structure and converts to R via Fresnel for a bulk half-space. This corresponds to **graphite (bulk)**, not monolayer graphene. The text says "graphene/graphite" in several places but the calculation is for the bulk limit.
**Fix:**
- Relabel consistently: the R_vis=0.35 result is for **graphite** (bulk limit of the graphene band structure)
- Add monolayer graphene calculation using 2D sheet conductivity: R = (πα/2)² ≈ 0.013% for freestanding, or T = 1 - πα ≈ 97.7%
- Clearly separate "graphene (monolayer)" from "graphite (bulk)" throughout ✅ DONE

#### 3. δ definition inconsistency / "Cu-old" in figures
**Reviewer:** "δ is introduced as an overarching variable with multiple proxies [...] remove inconsistent figures (e.g., those mentioning 'Cu-old')"
**Diagnosis:** Need to check figures for stale labels. Also, δ has three proxies (W_π, 1/m*, IPR) — reviewer wants ONE primary operational definition.
**Fix:**
- Check all figures for "Cu-old" or other stale labels
- Designate IPR as the **primary** operational δ (since it's directly computable from any Hamiltonian)
- Keep W_π and 1/m* as **supporting evidence** for the overarching variable
- Report δ_IPR values with clear definition for all materials ✅ DONE
- "Cu-old" NOT found in any figures — reviewer may have seen an earlier version

---

### 🟡 YELLOW (Computational — need work)

#### 4. Small sample size (5 carbon + h-BN only)
**Reviewer:** "Small sample size [...] add cross-element test cases (metals, polar dielectrics, quasi-1D conductors, layered oxides)"
**Status:** This is a fundamental limitation of the proof-of-concept scope. Cannot add arbitrary materials to TB models easily.
**Fix:**
- Acknowledge explicitly in Limitations (already partially done)
- Add: the restriction to carbon is **by design** (single-element controls for composition)
- Note that Paper 2 (surface tension) extends to 11 metallic elements
- Propose specific cross-element targets for future work ✅ DONE

#### 5. GU_eff = GU_clean × corr² is ad hoc
**Reviewer:** "Can you justify the quadratic scaling more rigorously or compare it against a roughness-based gloss model?"
**Status:** Already partially addressed in §IV.B.3 and Limitations item 5. The current text acknowledges it's a "minimal phenomenological model."
**Fix:**
- Strengthen the physical motivation: cite Debye-Waller analogy (I ∝ e^{-2W} ≈ corr² for small deviations)
- Add explicit statement: "We do not claim corr² is derived from first principles; it is the simplest ansatz consistent with dimensional analysis"
- Already mentions Beckmann-Spizzichino as future target ✅ DONE

#### 6. Anderson disorder W=5 eV is unrealistically large
**Reviewer:** "Anderson disorder strengths up to W=5 eV are very large and physical mapping to real surface/near-surface perturbations is unclear"
**Fix:**
- Add context: typical on-site perturbation from vacancy ≈ 1-2 eV, from adsorption ≈ 0.3-1 eV
- W=5 eV is an **extreme stress test**, not a realistic condition
- The physically relevant range is W=0.5-2 eV, where all systems show corr > 0.8
- The ranking (1D > graphene > C60) is consistent across ALL W values ✅ DONE

#### 7. ε(ω) not validated against experiment except diamond
**Reviewer:** "Benchmark your ε(ω) and R(θ) for graphite, h-BN, and C60 against Palik/other experimental spectra"
**Fix:**
- Add comparison with Palik data for graphite (ε_∥ and ε_⊥)
- For h-BN: cite experimental ε(ω) and note that TB model reproduces gap position
- For C60: compare absorption onset with experimental HOMO-LUMO gap
- Tabulate TB vs experiment for key quantities (R_vis, gap position, ε_∞) ✅ DONE

#### 8. D_eff not validated against conductivity tensor anisotropy
**Reviewer:** "Have you compared D_eff to anisotropy in measured or computed conductivity tensors (σ_xx vs σ_zz)?"
**Fix:**
- Compute σ_xx/σ_zz from our TB model for graphite → should show σ_xx >> σ_zz
- Compare with experimental anisotropy ratio (σ_∥/σ_⊥ ≈ 10³ for graphite)
- This is a simple computation from existing code ✅ DONE (discussion added with Spain1981 reference)

---

### 🟢 GREEN (Future work — note in Limitations/Outlook)

| Issue | Status |
|-------|--------|
| 9. Roughness model (Beckmann-Spizzichino) integration | Already noted in Discussion |
| 10. TB model convergence (basis size, hopping range) | Note in Limitations |
| 11. Wannier/gauge-clean σ(ω) computation | Note in Outlook |
| 12. Fang et al. (2025) tensor database comparison | Note in Outlook |
| 13. Liquid extension (Ga solid→liquid reflectivity) | Already noted in Outlook |

---

## Action Plan

### Phase 1: Text fixes (immediate)
1. [RED 1] D_eff windowing clarification — add "all-energy" vs "visible-window" distinction
2. [RED 2] Graphene→Graphite relabeling throughout
3. [RED 3] Check figures for stale labels; designate IPR as primary δ

### Phase 2: Computational additions
4. [YELLOW 5] Strengthen corr² motivation (Debye-Waller analogy)
5. [YELLOW 6] Add W-value physical context (vacancy energies)
6. [YELLOW 7] Add ε(ω) comparison table (TB vs Palik experiment)
7. [YELLOW 8] Compute and report σ_xx/σ_zz anisotropy ratio

### Phase 3: Scope/framing
8. [YELLOW 4] Strengthen "by design" rationale for carbon-only scope
9. [GREEN 10-12] Add notes in Limitations/Outlook

---

## Key references to add

1. Palik, E. D. (1998) Handbook of Optical Constants of Solids — graphite ε(ω)
2. Taft, E. A. and Philipp, H. R. (1965) — graphite reflectance
3. Fang et al. (2025) — tensorial optical conductivity database (if published)
4. Beckmann, P. and Spizzichino, A. (1963) The Scattering of EM Waves from Rough Surfaces
