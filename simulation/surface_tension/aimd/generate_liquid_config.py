#!/usr/bin/env python3
"""
Generate random liquid-metal configurations for AIMD supercells.

Places N atoms in a cubic cell with periodic boundary conditions,
enforcing a minimum inter-atomic distance. Uses a simple random
sequential placement with rejection sampling.

Usage:
    python generate_liquid_config.py

Outputs ATOMIC_POSITIONS (crystal) blocks for each element to stdout,
and also writes individual position files: {element}_positions.dat
"""

import numpy as np
from typing import Optional


def minimum_image_distance(
    r1: np.ndarray, r2: np.ndarray, box: float
) -> float:
    """Minimum-image distance in a cubic cell of side `box` (angstrom)."""
    dr = r1 - r2
    dr -= box * np.round(dr / box)
    return np.linalg.norm(dr)


def generate_config(
    n_atoms: int,
    box_ang: float,
    d_min: float = 2.0,
    max_attempts: int = 500_000,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate random atomic positions in a cubic box.

    Parameters
    ----------
    n_atoms : int
        Number of atoms.
    box_ang : float
        Cubic cell side length in angstrom.
    d_min : float
        Minimum allowed inter-atomic distance in angstrom.
    max_attempts : int
        Maximum rejection-sampling attempts per atom.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    positions : np.ndarray, shape (n_atoms, 3)
        Fractional coordinates in [0, 1).
    """
    rng = np.random.default_rng(seed)
    positions_cart = []  # cartesian, angstrom

    for i in range(n_atoms):
        placed = False
        for _ in range(max_attempts):
            trial = rng.random(3) * box_ang
            ok = True
            for existing in positions_cart:
                if minimum_image_distance(trial, existing, box_ang) < d_min:
                    ok = False
                    break
            if ok:
                positions_cart.append(trial)
                placed = True
                break
        if not placed:
            raise RuntimeError(
                f"Could not place atom {i+1}/{n_atoms} after "
                f"{max_attempts} attempts. Try increasing box size "
                f"or decreasing d_min."
            )

    positions_cart = np.array(positions_cart)
    # Convert to fractional coordinates
    positions_frac = positions_cart / box_ang
    return positions_frac


def format_qe_positions(
    symbol: str, positions_frac: np.ndarray
) -> str:
    """Format positions as QE ATOMIC_POSITIONS (crystal) block."""
    lines = ["ATOMIC_POSITIONS (crystal)"]
    for pos in positions_frac:
        lines.append(f"  {symbol}  {pos[0]:.10f}  {pos[1]:.10f}  {pos[2]:.10f}")
    return "\n".join(lines)


# --------------- Element parameters ---------------
ELEMENTS = {
    "Na": {
        "M": 22.990,
        "rho_liquid": 0.927,   # g/cm^3
        "d_min": 2.8,          # angstrom (approx. hard-core)
        "seed": 42,
    },
    "Al": {
        "M": 26.982,
        "rho_liquid": 2.375,
        "d_min": 2.2,
        "seed": 43,
    },
    "Cu": {
        "M": 63.546,
        "rho_liquid": 8.02,
        "d_min": 2.0,
        "seed": 44,
    },
    "Zn": {
        "M": 65.38,
        "rho_liquid": 6.57,
        "d_min": 2.2,
        "seed": 45,
    },
}

N_ATOMS = 64
N_A = 6.02214076e23


def compute_box_ang(M: float, rho: float, n: int) -> float:
    """Compute cubic box side in angstrom from density."""
    V_cm3 = n * M / (rho * N_A)
    a_cm = V_cm3 ** (1.0 / 3.0)
    return a_cm * 1e8  # angstrom


if __name__ == "__main__":
    for el, params in ELEMENTS.items():
        box = compute_box_ang(params["M"], params["rho_liquid"], N_ATOMS)
        print(f"\n{'='*60}")
        print(f"  {el}: box = {box:.4f} Ang, d_min = {params['d_min']} Ang")
        print(f"{'='*60}")

        frac = generate_config(
            N_ATOMS, box, d_min=params["d_min"], seed=params["seed"]
        )
        block = format_qe_positions(el, frac)
        print(block)

        # Write to file
        outfile = f"{el}_positions.dat"
        with open(outfile, "w") as f:
            f.write(f"# {el} liquid config: {N_ATOMS} atoms, box = {box:.4f} Ang\n")
            f.write(f"# density = {params['rho_liquid']} g/cm^3\n")
            f.write(block + "\n")
        print(f"  -> Written to {outfile}")
