"""
実験E-2: E3 FAIL の追試 — kz 分散が k 解像度を超える t_z=0.5 での確認

E3 の FAIL 診断: t_z=0.05 では kz バンド幅 (~2t_z=0.1) が有限系の
k 間隔 (2π/12≈0.52) より小さく、kz 方向の金属性が解像できない
（シェル効果で λ_z² が非単調に振れる）。
t_z=0.5 なら kz バンド幅 ~1.0 > 0.52 で解像可能のはず。

改訂判定 E3': t_z=0.5 で λ_z²(N) が単調増大（面直も発散側に転じる）
"""
import json
import numpy as np

TWIST = np.array([0.1234, 0.4321, 0.7891])


def lambda2(C, coords, Lvec, axis, Ne):
    phase = np.exp(1j * 2 * np.pi * coords[:, axis] / Lvec[axis])
    M = C.conj().T @ (phase[:, None] * C)
    sign, logdet = np.linalg.slogdet(M)
    ln_z2 = 2 * logdet
    if not np.isfinite(ln_z2):
        return np.inf
    return -Lvec[axis] ** 2 * ln_z2 / (4 * np.pi ** 2 * Ne)


def aniso3d(N, tz, dimer=0.5):
    idx = lambda x, y, z: (x * N + y) * N + z
    Ns = N ** 3
    H = np.zeros((Ns, Ns), complex)
    for x in range(N):
        for y in range(N):
            for z in range(N):
                i = idx(x, y, z)
                for axis, (dx, dy) in enumerate([(1, 0), (0, 1)]):
                    j = idx((x + dx) % N, (y + dy) % N, z)
                    ph = np.exp(1j * TWIST[axis] / N)
                    H[i, j] += -1.0 * ph
                    H[j, i] += -1.0 * np.conj(ph)
                if tz != 0:
                    t = tz * (1 + dimer * (-1) ** z)
                    j = idx(x, y, (z + 1) % N)
                    ph = np.exp(1j * TWIST[2] / N)
                    H[i, j] += -t * ph
                    H[j, i] += -t * np.conj(ph)
    w, v = np.linalg.eigh(H)
    Ne = Ns // 2
    C = v[:, :Ne]
    coords = np.array([[x, y, z] for x in range(N)
                       for y in range(N) for z in range(N)], float)
    return lambda2(C, coords, [N, N, N], 0, Ne), \
        lambda2(C, coords, [N, N, N], 2, Ne)


print("=== E-2: t_z=0.5 (kz バンド幅 ~1.0 > k間隔 0.52) ===")
rows = []
for N in [6, 8, 10, 12]:
    lx, lz = aniso3d(N, 0.5)
    rows.append((N, lx, lz))
    print(f"N={N}: λ_x²={lx:.4f}, λ_z²={lz:.4f}", flush=True)

lzs = [r[2] for r in rows]
e3p = all(lzs[i] < lzs[i + 1] for i in range(len(lzs) - 1))
print(f"\nE3' (t_z=0.5 で λ_z² 単調増大): "
      f"{[f'{v:.3f}' for v in lzs]} → {'PASS' if e3p else 'FAIL'}")

with open("exp_E2_results.json", "w") as f:
    json.dump({"meta": {"date": "2026-07-05", "tz": 0.5,
                        "purpose": "resolve E3 FAIL (kz shell effect)"},
               "rows": [[int(n), lx, lz] for n, lx, lz in rows],
               "verdict": {"E3_prime": bool(e3p)}}, f, indent=2)
print("保存: exp_E2_results.json")
