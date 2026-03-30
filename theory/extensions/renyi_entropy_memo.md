# Idea Memo: Information-Theoretic Grounding of δ via Rényi Entropy

**Status: Mathematical observation + speculative extension. Not a theory.**

---

## The Mathematical Identity

The inverse participation ratio (IPR) used to define δ_IPR is exactly related to the 2nd-order Rényi entropy:

$$\text{IPR} = \sum_i |\psi_i|^4 = e^{-H_2}$$

where $H_2 = -\ln \sum_i p_i^2$ is the Rényi entropy of order 2, with $p_i = |\psi_i|^2$.

**This is not a discovery.** It is a direct consequence of definitions. IPR and $H_2$ are related by a monotonic transformation ($-\ln$). Any statement about IPR is equivalently a statement about $H_2$, and vice versa.

## What This Buys

### For δ_IPR specifically
- δ_IPR inherits the full mathematical apparatus of Rényi entropy: additivity for independent systems, known inequalities ($H_2 \leq H_1$ where $H_1$ is Shannon entropy), connections to information geometry.
- The "delocalization" that δ_IPR measures is formally the **information content** of the wavefunction's probability distribution. More delocalized = higher entropy = more uncertainty about where the electron is.
- This provides a rigorous, basis-independent interpretation: δ_IPR measures how many sites "effectively participate" in the wavefunction (the exponential of the entropy).

### For the broader δ framework
- If δ is understood as a Rényi-2 entropy, then the question "what is the right δ?" becomes "what is the right entropy order?" This connects to the Rényi family $H_\alpha$ for $\alpha \in (0, \infty)$.
- Different orders weight the tails of the distribution differently: $H_0$ = log of support size, $H_1$ = Shannon, $H_2$ = collision entropy, $H_\infty$ = min-entropy. The "best" order for predicting a physical property is an empirical question.

## What This Does NOT Buy

### Other δ proxies are NOT $H_2$ estimators
The δ framework uses multiple proxies interchangeably:
- **δ_IPR**: Exactly $e^{-H_2}$. ✓
- **Wannier spread** $\Omega$: Measures spatial variance $\langle r^2 \rangle - \langle r \rangle^2$. This is a second moment, not an entropy. For a Gaussian, $\Omega \propto e^{H_2}$, but real wavefunctions are not Gaussian. The relationship is approximate at best.
- **Band width** $W$: Reciprocal-space property. No direct entropy interpretation.
- **Effective mass** $1/m^*$: Band curvature. No direct entropy interpretation.
- **ELF**: Measures kinetic energy density relative to uniform gas. Related to localization but not equivalent to any Rényi entropy.

**Claiming that "all δ proxies are Rényi-2 estimators" would be an overclaim.** Only IPR has the exact equivalence. The others correlate with IPR empirically but are not information-theoretically grounded.

## Speculative Extension: geDIG and Rényi

The generalized Diversity Index of Graphs (geDIG) framework defines graph-level diversity measures that reduce to Rényi entropies for specific parameter choices. If a crystal's tight-binding Hamiltonian is viewed as a weighted graph, then:

- geDIG could provide a family of δ-like descriptors parameterized by (α, β) — the Rényi order and graph-weighting scheme.
- The "optimal" descriptor for a given property (surface tension, reflectivity, etc.) might correspond to a specific (α, β) pair.

**This is purely structural analogy at present.** No calculation has been performed. The connection requires:
1. Defining the graph (adjacency = hopping integrals? overlap integrals?)
2. Choosing the vertex weights (electron density? orbital population?)
3. Computing geDIG for real materials
4. Checking correlation with physical properties

Without these steps, the geDIG connection is a mathematical curiosity, not a physical claim.

## Possible Paper 3 Direction

If verified, the Rényi grounding could support a "Paper 3: Microscopic Redefinition of Liquid" by:

1. **Defining "liquid" via entropy threshold**: A phase is "liquid" when $H_2$ of the valence wavefunction exceeds a critical value — electrons are delocalized enough to create a self-healing, optically smooth interface.
2. **Unifying the two papers**: Paper 1 (optics) and Paper 2 (surface tension) both use δ. If δ = $e^{-H_2}$, then both papers are about the same information-theoretic quantity applied to different properties.
3. **Predicting new correlations**: The Rényi framework suggests that other Rényi orders ($H_1$, $H_\infty$) might predict other properties, opening a family of descriptors.

### What Would Need to Be True

- δ_IPR (= $e^{-H_2}$) must be demonstrably superior to other δ proxies for at least one property. If Wannier spread or band width work just as well, the Rényi connection adds mathematical elegance but no predictive power.
- The "liquid threshold" in $H_2$ must be sharp enough to be useful. If the transition is gradual, a threshold definition is arbitrary.
- The connection must survive beyond tight-binding models — i.e., $H_2$ computed from DFT wavefunctions must still correlate with macroscopic properties.

## Known Weaknesses

- **Trivial identity dressed as insight**: The risk is that IPR = $e^{-H_2}$ sounds deep but adds nothing beyond relabeling. The value depends entirely on whether the Rényi framework enables new predictions or connections that IPR alone does not.
- **Basis dependence**: IPR (and thus $H_2$) depends on the basis. In a plane-wave basis, every Bloch state has uniform $|\psi|^2$ and IPR = 1/N regardless of localization. The tight-binding (atomic orbital) basis is physically motivated but not unique. This is a known issue for IPR in general, not specific to this memo.
- **Existing literature on Rényi entropy in condensed matter**: Rényi entropies are widely used in quantum information (entanglement entropy) and Anderson localization (multifractal analysis). We must check that nobody has already connected $H_2$ of Bloch states to macroscopic material properties. A preliminary search found no such work, but a thorough literature survey is required.

---

*This memo records an observation from discussion with GitHub Copilot (2026-03-30). The mathematical identity is exact; all physical implications are speculative and require verification. Included for intellectual honesty and to preserve the reasoning chain.*
