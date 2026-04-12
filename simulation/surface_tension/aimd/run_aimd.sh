#!/bin/bash
# =============================================================
# run_aimd.sh -- Sequential AIMD runs for liquid-metal systems
#
# Usage:
#   ./run_aimd.sh              # Run all elements
#   ./run_aimd.sh Na Al        # Run selected elements only
#
# Requirements:
#   - pw.x from Quantum ESPRESSO must be in PATH
#   - Adjust NPROCS and MPI launcher for your cluster
# =============================================================

set -euo pipefail

# ---------- User-configurable parameters ----------
NPROCS=${NPROCS:-16}
PW_CMD="mpirun -np ${NPROCS} pw.x"
# For SLURM clusters, use instead:
# PW_CMD="srun pw.x"

ALL_ELEMENTS="Na Al Cu Zn"
ELEMENTS="${@:-$ALL_ELEMENTS}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Create output and tmp directories
mkdir -p tmp logs

echo "=============================================="
echo "  Liquid-metal AIMD calculations"
echo "  Elements: ${ELEMENTS}"
echo "  NPROCS: ${NPROCS}"
echo "  Date: $(date)"
echo "=============================================="

for EL in $ELEMENTS; do
    echo ""
    echo "----------------------------------------------"
    echo "  Starting ${EL} calculations"
    echo "----------------------------------------------"

    SCF_IN="${EL}_liquid_scf.in"
    SCF_OUT="logs/${EL}_liquid_scf.out"
    MD_IN="${EL}_liquid_md.in"
    MD_OUT="logs/${EL}_liquid_md.out"

    # Check input files exist
    if [ ! -f "$SCF_IN" ]; then
        echo "ERROR: $SCF_IN not found. Skipping ${EL}."
        continue
    fi
    if [ ! -f "$MD_IN" ]; then
        echo "ERROR: $MD_IN not found. Skipping ${EL}."
        continue
    fi

    # --- Step 1: Initial SCF ---
    echo "[$(date +%H:%M:%S)] ${EL}: Running SCF..."
    $PW_CMD -input "$SCF_IN" > "$SCF_OUT" 2>&1
    SCF_STATUS=$?

    if [ $SCF_STATUS -ne 0 ]; then
        echo "ERROR: ${EL} SCF failed (exit code $SCF_STATUS). Check $SCF_OUT"
        continue
    fi
    echo "[$(date +%H:%M:%S)] ${EL}: SCF converged."

    # --- Step 2: Born-Oppenheimer MD ---
    # Modify MD input to restart from SCF wavefunctions
    sed 's/restart_mode.*=.*/restart_mode  = '\''restart'\''/' \
        "$MD_IN" > "${MD_IN}.restart"

    echo "[$(date +%H:%M:%S)] ${EL}: Starting BO-MD (this will take a while)..."
    $PW_CMD -input "${MD_IN}.restart" > "$MD_OUT" 2>&1
    MD_STATUS=$?

    if [ $MD_STATUS -ne 0 ]; then
        echo "WARNING: ${EL} MD exited with code $MD_STATUS. Check $MD_OUT"
    else
        echo "[$(date +%H:%M:%S)] ${EL}: MD completed successfully."
    fi

    # Clean up restart-modified input
    rm -f "${MD_IN}.restart"

    echo "----------------------------------------------"
done

echo ""
echo "=============================================="
echo "  All calculations finished at $(date)"
echo "=============================================="
