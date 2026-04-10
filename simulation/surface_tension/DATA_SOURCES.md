# Data Sources for Surface Tension Simulations

## jellium_surface.py

| Data | Values | Source |
|------|--------|--------|
| Al surface tension | 1050 mN/m | Keene (1993) Int. Mater. Rev. **38**, 157; Mills & Su (2006) |
| Zn surface tension | 782 mN/m | Keene (1993) |
| Mg surface tension | 559 mN/m | Keene (1993) |
| Li surface tension | 398 mN/m | Keene (1993) |
| Na surface tension | 191 mN/m | Keene (1993) |
| K surface tension | 101 mN/m | Keene (1993) |
| Cs surface tension | 67 mN/m | Keene (1993) |
| Wigner-Seitz radii (all metals) | Table 1.1 | Ashcroft & Mermin (1976) |
| Lang-Kohn jellium surface energies | Table II | Lang & Kohn (1970) Phys. Rev. B **1**, 4555 |
| PZ LDA correlation coefficients | Eq. (C1)-(C2) | Perdew & Zunger (1981) Phys. Rev. B **23**, 5048 |
| QMC electron gas data | | Ceperley & Alder (1980) Phys. Rev. Lett. **45**, 566 |
| Drude damping rates | Typical values | Ashcroft & Mermin (1976) Ch. 1; Iida & Guthrie (1988) |

## water_delta.py

| Data | Values | Source |
|------|--------|--------|
| Ice Ih density | 0.917 g/cm³ | Wagner & Pruss (2002) IAPWS-95 |
| Water density vs T (0-100°C) | 10 data points | Wagner & Pruss (2002); NIST WebBook |
| Water density max at 3.98°C | 0.99997 g/cm³ | Wagner & Pruss (2002) |
| Water surface tension at 20°C | 72.75 mN/m | Vargaftik et al. (1983) J. Phys. Chem. Ref. Data **12**, 817 |
| γ(T) linear approximation | 75.6 - 0.14(T-20) | Derived from Vargaftik (1983); IAPWS (2014) |
| H-bond energy (~0.2 eV per bond) | Literature consensus | Suresh & Naik (2000) J. Chem. Phys. **113**, 9727 |

## Key Results (from initial exploration, see paper2_rethink.md for latest)

| Correlation | r | p-value | Interpretation |
|-------------|---|---------|----------------|
| δ_val vs midpoint ratio (15 dimers) | **0.89** | < 0.001 | δ predicts uniformity (CURRENT) |
| sp/d slab separation (14 metals) | — | **0.00008** | sp(0.96) vs d(0.38) (CURRENT) |
| δ_val vs Miedema n_ws^{1/3} | 0.10 | 0.73 | **Uncorrelated** (CURRENT) |
| n_mid(abs) vs n_ws^{1/3} | 0.79 | 0.0007 | Absolute density matches n_ws (CURRENT) |
| ∫(dδ/dz)² vs γ_exp (7 metals) | 0.956 | 7.8e-4 | Initial exploration (superseded) |

## Full bibliography

See `references_surface_tension.bib` for complete BibTeX entries.
