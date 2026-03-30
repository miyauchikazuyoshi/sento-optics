# Paper 2: Testable Predictions from δ_IPR Framework

## Prediction 1: Ce volume collapse → γ discontinuity

Cerium undergoes α→γ phase transition under pressure where f-electrons
localize. δ decreases discontinuously.

**Prediction**: Surface tension γ should show a discontinuous DROP at
the α→γ transition, because f-electron localization reduces boundary
density.

**Why Miedema can't predict this**: n_ws is tabulated as a single static
value per element. It has no mechanism for phase-dependent changes.

**How to test**: Literature search for Ce surface tension measurements
near the phase transition, or DFT slab calculation at two volumes
(α and γ phases).

## Prediction 2: Al-Zn alloy γ vs composition is concave

Miedema predicts γ(Al₁₋ₓZnₓ) via linear interpolation of n_ws.

**Prediction**: γ should decrease NONLINEARLY (concave downward) with
Zn fraction x, because even small amounts of d-electrons concentrate
charge near nuclei and deplete the boundary disproportionately.

**How to test**: Experimental alloy surface tension data (literature),
or VCA/CPA DFT calculations.

## Prediction 3: Systematic slab boundary densities (IN PROGRESS)

| Metal | Type | Prediction: n_mid/n_bulk | Prediction: γ rank |
|-------|------|--------------------------|-------------------|
| Na | sp (3s¹) | > 0.9 (high, like Al) | low (low n_bulk) |
| K | sp (4s¹) | > 0.9 (similar to Na) | lower than Na |
| Cu | d¹⁰s¹ | < 0.3 (like Zn) | high (high n_bulk compensates) |
| Al | sp (done) | 0.975 ✓ | high ✓ |
| Zn | d¹⁰s² (done) | 0.186 ✓ | medium ✓ |

**Key test**: If Cu shows low n_mid/n_bulk like Zn, it confirms that
d-electron localization (not just Zn-specific properties) is responsible.

**Status**: QE calculations for Na, K, Cu are next.

## Prediction 4: Liquid Ga reflectivity jump ↔ γ anomaly

Ga has a large reflectivity increase at melting (solid → liquid).
If R and γ are both projections of δ, then liquid Ga's surface tension
should also show an anomaly near the melting point.

**How to test**: Literature search for Ga surface tension temperature
dependence near 29.8°C melting point.

## Priority

1. **Prediction 3**: Can be done NOW with existing QE setup. Goes directly
   into Paper 2.
2. **Prediction 4**: Literature search only. Quick to check.
3. **Prediction 1**: Requires Ce pseudopotential + f-electron DFT (hard).
4. **Prediction 2**: Requires alloy calculations or literature data.
