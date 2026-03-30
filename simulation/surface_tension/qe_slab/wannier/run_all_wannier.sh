#!/bin/bash
# Run Wannier90 for 5 bulk metals: Na, K, Al, Cu, Zn
# Compute MLWF spreads to quantify electronic delocalization

set -e
source ~/miniconda3/etc/profile.d/conda.sh
conda activate qe

PSEUDO="../pseudo/"

run_metal() {
    local name=$1
    echo "============================================"
    echo "  Running $name"
    echo "============================================"

    # Step 1: SCF
    echo "  SCF..."
    pw.x < ${name}_scf.in > ${name}_scf.out 2>&1

    # Step 2: NSCF with uniform k-grid
    echo "  NSCF..."
    pw.x < ${name}_nscf.in > ${name}_nscf.out 2>&1

    # Step 3: Wannier90 preprocessing (-pp)
    echo "  Wannier90 -pp..."
    wannier90.x -pp ${name} 2>&1

    # Step 4: pw2wannier90
    echo "  pw2wannier90..."
    pw2wannier90.x < ${name}_pw2wan.in > ${name}_pw2wan.out 2>&1

    # Step 5: Wannier90 minimization
    echo "  Wannier90 minimize..."
    wannier90.x ${name} 2>&1

    # Extract spread
    echo "  Result:"
    grep "Omega Total" ${name}.wout | tail -1
    echo ""
}

# Run all metals
for metal in na k al cu zn; do
    run_metal $metal
done

echo "All done! Extracting final spreads..."
for metal in na k al cu zn; do
    echo "=== $metal ==="
    grep -A2 "Final State" ${metal}.wout | head -5
    grep "Omega Total" ${metal}.wout | tail -1
    echo ""
done
