#!/bin/bash
set -e

# Activate QE conda environment
export PATH="$HOME/miniconda3/envs/qe/bin:$PATH"

PW=pw.x
W90=wannier90.x
PW2WAN=pw2wannier90.x

echo "=== DIAMOND ==="
cd diamond
$PW < scf.in > scf.out 2>&1
$PW < nscf.in > nscf.out 2>&1
$W90 -pp diamond
$PW2WAN < pw2wan.in > pw2wan.out 2>&1
$W90 diamond
echo "Diamond Omega:"
grep "Omega Total" diamond.wout
cd ..

echo "=== GRAPHITE ==="
cd graphite
$PW < scf.in > scf.out 2>&1
$PW < nscf.in > nscf.out 2>&1
$W90 -pp graphite
$PW2WAN < pw2wan.in > pw2wan.out 2>&1
$W90 graphite
echo "Graphite Omega:"
grep "Omega Total" graphite.wout
cd ..

echo "=== COMPARISON ==="
echo "Diamond:"
grep "Omega Total" diamond/diamond.wout
echo "Graphite:"
grep "Omega Total" graphite/graphite.wout
