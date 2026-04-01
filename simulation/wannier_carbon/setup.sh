#!/bin/bash
# Download pseudopotentials from QE pslibrary
set -e
mkdir -p pseudo/

BASE_URL="https://pseudopotentials.quantum-espresso.org/upf_files"

# Carbon (diamond, graphite)
wget -nc "$BASE_URL/C.pbe-n-kjpaw_psl.1.0.0.UPF" -P pseudo/

# Silicon (diamond cubic)
wget -nc "$BASE_URL/Si.pbe-n-kjpaw_psl.1.0.0.UPF" -P pseudo/

# Germanium (diamond cubic, -dn- includes d electrons in valence)
wget -nc "$BASE_URL/Ge.pbe-dn-kjpaw_psl.1.0.0.UPF" -P pseudo/

echo "All pseudopotentials downloaded to pseudo/"
ls -l pseudo/
