#!/bin/bash
# Run QE slab calculations for 10 new elements
# Activate conda env first: conda activate qe
#
# Usage: bash run_all_new.sh 2>&1 | tee run_all_new.log

set -e
cd "$(dirname "$0")"

# Non-magnetic elements first (faster)
ELEMENTS_NONMAG="li be mg ca si ga ti ag"
# Magnetic elements (need nspin=2, slower)
ELEMENTS_MAG="fe ni"

run_element() {
    local elem=$1
    local scf_in=$(ls ${elem}*_scf.in 2>/dev/null | head -1)
    local pp_in=$(ls ${elem}*_pp.in 2>/dev/null | grep -v valence | head -1)
    local val_pp_in="${elem}_pp_valence.in"
    local val_avg_in="${elem}_val_avg.in"

    if [ -z "$scf_in" ]; then
        echo "ERROR: No SCF input for $elem"
        return 1
    fi

    local prefix=$(echo "$scf_in" | sed 's/_scf.in//')

    echo "=========================================="
    echo "  $elem: SCF ($scf_in)"
    echo "=========================================="
    mkdir -p tmp
    pw.x < "$scf_in" > "${prefix}_scf.out" 2>&1
    if grep -q "JOB DONE" "${prefix}_scf.out"; then
        echo "  SCF: OK"
    else
        echo "  SCF: FAILED"
        tail -5 "${prefix}_scf.out"
        return 1
    fi

    echo "  Post-processing (total density)..."
    pp.x < "$pp_in" > "${elem}_pp.out" 2>&1

    echo "  Post-processing (valence ILDOS)..."
    pp.x < "$val_pp_in" > "${elem}_pp_val.out" 2>&1

    echo "  Planar average..."
    average.x < "$val_avg_in" > "${elem}_avg.out" 2>&1

    echo "  DONE: $elem"
    echo ""
}

echo "Starting QE slab calculations for new elements"
echo "Date: $(date)"
echo ""

for elem in $ELEMENTS_NONMAG; do
    run_element "$elem" || echo "FAILED: $elem (continuing...)"
done

for elem in $ELEMENTS_MAG; do
    run_element "$elem" || echo "FAILED: $elem (continuing...)"
done

echo ""
echo "All calculations complete: $(date)"
echo "Check outputs: grep 'JOB DONE' *_scf.out"
