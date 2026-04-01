#!/bin/bash
# Download C pseudopotential from QE pslibrary
set -e
mkdir -p pseudo/
wget https://pseudopotentials.quantum-espresso.org/upf_files/C.pbe-n-kjpaw_psl.1.0.0.UPF -P pseudo/
echo "Pseudopotential downloaded to pseudo/"
