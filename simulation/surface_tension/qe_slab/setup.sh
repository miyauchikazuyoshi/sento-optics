#!/bin/bash
# Setup script for QE slab calculations
# Downloads pseudopotentials and creates working directories

set -e

cd "$(dirname "$0")"

# Create directories
mkdir -p pseudo tmp

# Download PAW pseudopotentials from QE website
# Using PBE PAW from pslibrary 1.0.0
BASE_URL="https://pseudopotentials.quantum-espresso.org/upf_files"

echo "Downloading pseudopotentials..."

# Aluminum
if [ ! -f pseudo/Al.pbe-n-kjpaw_psl.1.0.0.UPF ]; then
  curl -L -o pseudo/Al.pbe-n-kjpaw_psl.1.0.0.UPF \
    "${BASE_URL}/Al.pbe-n-kjpaw_psl.1.0.0.UPF"
  echo "  Al pseudopotential downloaded."
else
  echo "  Al pseudopotential already exists."
fi

# Zinc
if [ ! -f pseudo/Zn.pbe-dn-kjpaw_psl.1.0.0.UPF ]; then
  curl -L -o pseudo/Zn.pbe-dn-kjpaw_psl.1.0.0.UPF \
    "${BASE_URL}/Zn.pbe-dn-kjpaw_psl.1.0.0.UPF"
  echo "  Zn pseudopotential downloaded."
else
  echo "  Zn pseudopotential already exists."
fi

# Sodium (for comparison)
if [ ! -f pseudo/Na.pbe-spn-kjpaw_psl.1.0.0.UPF ]; then
  curl -L -o pseudo/Na.pbe-spn-kjpaw_psl.1.0.0.UPF \
    "${BASE_URL}/Na.pbe-spn-kjpaw_psl.1.0.0.UPF"
  echo "  Na pseudopotential downloaded."
else
  echo "  Na pseudopotential already exists."
fi

echo ""
echo "Setup complete. To run calculations:"
echo "  1. pw.x < al111_scf.in > al111_scf.out"
echo "  2. python compute_ipr_from_slab.py al"
echo ""
echo "For parallel execution:"
echo "  mpirun -np 4 pw.x < al111_scf.in > al111_scf.out"
