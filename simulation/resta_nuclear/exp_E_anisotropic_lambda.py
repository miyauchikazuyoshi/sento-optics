"""
実験E: 方向分解 Resta 局在長 λ_α — 「D_eff = λ が発散する方向の数」の数値実証

背景 (memo_kohn_resta_swm_lineage.md §6.3 気付き⑦):
  RS (1999) は「グラファイトでは λ は面直方向に有限、面内方向に発散」と
  予想を書いたが計算していない。TB モデルで初の明示的数値化を試みる。

モデル:
  (1) 1D 検証: 二量化鎖（絶縁体）vs 一様鎖（金属）— RS Fig.2 の定性再現
  (2) 3D 異方モデル（理想化グラファイト）: 面内一様ホッピング t=1（金属）、
      面直は二量化 t_z(1±0.5)。t_z = 0 / 0.05 / 0.2 を比較。

独立電子の Resta 位相: z_α = det(C† diag(e^{i2πx_s/L_α}) C), C = 占有固有ベクトル
局在長:               λ_α² = −L_α² ln|z_α|² / (4π² N_e)     [RS Eq. 8/11 系]

事前判定基準:
  E1: 1D 二量化鎖の λ²(L) は収束（最大2サイズ間 <10%）、一様鎖は単調増大
  E2: 3D t_z=0 で λ_z² ≈ 0 かつ λ_x²(N) 増大 → D_eff = 2 の厳密実証
  E3: t_z を上げると λ_z² の増大率が単調に増える
      → D_eff は整数でなく「方向別の発散係数」で連続化される（精密化）

注意: 方法（RS/SWM の独立電子公式）は確立。新規なのは D_eff との対応の
明示化。異方的局在テンソルの先行計算は要文献照合。
"""
import json
import time
import numpy as np

TWIST = np.array([0.1234, 0.4321, 0.7891])   # generic twist（縮退回避）


def lambda2(C, coords, Lvec, axis, Ne):
    phase = np.exp(1j * 2 * np.pi * coords[:, axis] / Lvec[axis])
    M = C.conj().T @ (phase[:, None] * C)
    sign, logdet = np.linalg.slogdet(M)
    ln_z2 = 2 * logdet                        # log|z|^2
    if not np.isfinite(ln_z2):
        return np.inf
    return -Lvec[axis] ** 2 * ln_z2 / (4 * np.pi ** 2 * Ne)


# ---------- (1) 1D 検証 ----------
def chain(L, delta, twist=0.0):
    """二量化鎖: t_i = 1 + delta*(-1)^i。周期境界 + twist。"""
    H = np.zeros((L, L), complex)
    for i in range(L):
        t = 1 + delta * (-1) ** i
        j = (i + 1) % L
        ph = np.exp(1j * twist / L) if j == 0 or True else 1.0
        H[i, j] += -t * np.exp(1j * twist / L)
        H[j, i] += -t * np.exp(-1j * twist / L)
    w, v = np.linalg.eigh(H)
    Ne = L // 2
    C = v[:, :Ne]
    coords = np.arange(L, dtype=float).reshape(-1, 1)
    return lambda2(C, coords, [L], 0, Ne)


print("=== (1) 1D 検証: 二量化鎖 vs 一様鎖 ===")
Ls = [22, 42, 82, 122, 202, 302]
res1d = {}
for delta in [0.25, 0.10, 0.0]:
    lam = [chain(L, delta, twist=0.3) for L in Ls]
    res1d[delta] = lam
    tag = "絶縁体" if delta > 0 else "金属"
    print(f"delta={delta} ({tag}): λ² = " +
          ", ".join("inf" if np.isinf(x) else f"{x:.3f}" for x in lam))

conv = abs(res1d[0.25][-1] - res1d[0.25][-2]) / res1d[0.25][-2] < 0.10
grow = (np.isinf(res1d[0.0][-1]) or res1d[0.0][-1] > 2 * res1d[0.0][1])
e1 = conv and grow
print(f"E1: 二量化収束 {conv} & 一様増大 {grow} → {'PASS' if e1 else 'FAIL'}")

# ---------- (2) 3D 異方モデル ----------
def aniso3d(N, tz, dimer=0.5):
    """単純立方 N^3。面内 t=1 一様、z 方向 tz*(1±dimer) 交互。generic twist。"""
    idx = lambda x, y, z: (x * N + y) * N + z
    Ns = N ** 3
    H = np.zeros((Ns, Ns), complex)
    for x in range(N):
        for y in range(N):
            for z in range(N):
                i = idx(x, y, z)
                # 面内
                for axis, (dx, dy) in enumerate([(1, 0), (0, 1)]):
                    j = idx((x + dx) % N, (y + dy) % N, z)
                    ph = np.exp(1j * TWIST[axis] / N)
                    H[i, j] += -1.0 * ph
                    H[j, i] += -1.0 * np.conj(ph)
                # 面直（二量化）
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
    lx = lambda2(C, coords, [N, N, N], 0, Ne)
    lz = lambda2(C, coords, [N, N, N], 2, Ne)
    return lx, lz


print("\n=== (2) 3D 異方モデル: λ_x (面内) vs λ_z (面直) ===")
Nlist = [6, 8, 10, 12]
res3d = {}
for tz in [0.0, 0.05, 0.2]:
    rows = []
    for N in Nlist:
        t0 = time.time()
        lx, lz = aniso3d(N, tz)
        rows.append((N, lx, lz))
        print(f"tz={tz}, N={N}: λ_x²={lx:.4f}, λ_z²={lz:.6f}  "
              f"({time.time()-t0:.0f}s)", flush=True)
    res3d[tz] = rows

# 判定
r0 = res3d[0.0]
e2 = (r0[-1][2] < 1e-6) and (r0[-1][1] > 1.3 * r0[0][1])
lz_growth = {tz: res3d[tz][-1][2] - res3d[tz][0][2] for tz in res3d}
e3 = lz_growth[0.0] <= lz_growth[0.05] <= lz_growth[0.2]
print(f"\nE2 (t_z=0): λ_z²(N=12)={r0[-1][2]:.2e} ≈0 & λ_x² 増大 "
      f"({r0[0][1]:.3f}→{r0[-1][1]:.3f}) → {'PASS' if e2 else 'FAIL'}")
print(f"E3 λ_z² の増大量の単調性: " +
      ", ".join(f"tz={tz}: {g:.4f}" for tz, g in lz_growth.items()) +
      f" → {'PASS' if e3 else 'FAIL'}")

with open("exp_E_results.json", "w") as f:
    json.dump({"meta": {"date": "2026-07-05", "twist": TWIST.tolist(),
                        "model": "in-plane uniform t=1 (metallic), "
                                 "out-of-plane dimerized tz*(1±0.5)"},
               "oneD": {str(k): ["inf" if np.isinf(x) else x for x in v]
                        for k, v in res1d.items()},
               "threeD": {str(tz): [[int(n), lx, lz] for n, lx, lz in rows]
                          for tz, rows in res3d.items()},
               "verdict": {"E1": bool(e1), "E2": bool(e2), "E3": bool(e3)}},
              f, indent=2, ensure_ascii=False)
print("保存: exp_E_results.json")

# 図
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for delta, marker in [(0.25, "o"), (0.10, "s"), (0.0, "^")]:
    lam = [min(x, 1e4) for x in res1d[delta]]
    axes[0].plot(Ls, lam, marker + "-",
                 label=f"δ_dim={delta}" + (" (metal)" if delta == 0 else ""))
axes[0].set_xlabel("L (sites)"); axes[0].set_ylabel("λ²")
axes[0].set_yscale("log")
axes[0].set_title("1D: insulator converges, metal diverges (RS Fig.2 analog)")
axes[0].legend()
for tz, c in [(0.0, "tab:blue"), (0.05, "tab:orange"), (0.2, "tab:red")]:
    rows = res3d[tz]
    axes[1].plot([r[0] for r in rows], [r[1] for r in rows], "o-", color=c,
                 label=f"λ_x² (tz={tz})")
    axes[1].plot([r[0] for r in rows], [max(r[2], 1e-9) for r in rows], "s--",
                 color=c, alpha=0.6, label=f"λ_z² (tz={tz})")
axes[1].set_xlabel("N (cells per side)"); axes[1].set_ylabel("λ²")
axes[1].set_yscale("log")
axes[1].set_title("3D anisotropic: in-plane diverges, out-of-plane finite")
axes[1].legend(fontsize=7, ncol=2)
fig.tight_layout()
fig.savefig("exp_E_lambda.png", dpi=150)
print("保存: exp_E_lambda.png")
