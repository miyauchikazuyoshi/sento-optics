#!/bin/bash
# Dielectric function calculation for Group 14 elements
# Pipeline: (existing SCF) → NSCF (dense k-grid, more bands) → epsilon.x → ε(ω), n(ω)
set -e

export PATH="$HOME/miniconda3/envs/qe/bin:$PATH"

PW=pw.x
EPS=epsilon.x

for system in diamond silicon germanium; do
    echo "=== ${system^^}: NSCF (optical) ==="
    cd $system
    $PW < nscf_optical.in > nscf_optical.out 2>&1
    echo "  NSCF done."

    echo "=== ${system^^}: epsilon.x ==="
    $EPS < epsilon.in > epsilon.out 2>&1
    echo "  epsilon.x done."

    # Show static dielectric constant (ω → 0 limit)
    echo "  Output files:"
    ls -la epsr*.dat epsi*.dat 2>/dev/null || echo "  (no output files found)"
    cd ..
    echo ""
done

echo "=== DONE ==="
echo "Output files: {diamond,silicon,germanium}/epsr*.dat, epsi*.dat"
echo "Columns: energy(eV)  eps_xx  eps_yy  eps_zz"
