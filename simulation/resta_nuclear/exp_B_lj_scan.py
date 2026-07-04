"""
実験B: LJ 古典MDによる z_nuc の本検証（融解スキャン＋サイズスケーリング）

z_nuc は核位置だけの量なので ab initio 不要 — 古典MDで十分（メモリ制約回避）。

事前判定基準:
  B1: 固体点で |z1(Bragg)| > 0.5
  B2: 平衡液体点で |z1(n)| < 2×ノイズフロア (全n)  ← 実験Aの未決着に決着
  B3: 融解スキャンで |z1(Bragg)| が固液間で1桁以上落ちる
  B4: 液体の |z1| は 1/√N スケーリング（N=108 vs 500）

系: LJ (ε=σ=1), fcc 初期配置, Langevin (BAOAB), dt*=0.005, rc=2.5
状態点:
  固体対照   ρ*=1.05, T*=0.5
  液体対照   ρ*=0.80, T*=1.00
  融解スキャン ρ*=0.95, T* ∈ {0.5, 0.8, 1.1, 1.4, 1.7}
  サイズ     液体対照を N=108, 256, 500 で
"""
import json
import time
import numpy as np

rng = np.random.default_rng(20260704)
RC2 = 2.5 ** 2
DT = 0.005
GAMMA = 1.0
N_EQ = 10000
N_PROD = 20000
SNAP_EVERY = 100


def fcc(ncell, rho):
    a = (4 / rho) ** (1 / 3)
    L = ncell * a
    base = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]])
    pos = np.concatenate([(base + [i, j, k]) * a
                          for i in range(ncell) for j in range(ncell)
                          for k in range(ncell)])
    return pos, L, a


def forces(pos, L):
    d = pos[None, :, :] - pos[:, None, :]
    d -= L * np.round(d / L)
    r2 = (d ** 2).sum(-1)
    np.fill_diagonal(r2, np.inf)
    mask = r2 < RC2
    inv2 = np.where(mask, 1.0 / r2, 0.0)
    inv6 = inv2 ** 3
    fmag = 24 * inv2 * inv6 * (2 * inv6 - 1)          # (N,N)
    # F_i = -dU/dr_i = -fmag * d_ij  (d_ij = r_j - r_i)
    f = -(fmag[:, :, None] * d).sum(axis=1)
    pe = 4 * (inv6 ** 2 - inv6)[mask].sum() / 2
    return f, pe


def run_point(ncell, rho, T, label):
    pos, L, a = fcc(ncell, rho)
    N = len(pos)
    vel = rng.normal(0, np.sqrt(T), (N, 3))
    vel -= vel.mean(axis=0)
    f, _ = forces(pos, L)
    c1 = np.exp(-GAMMA * DT)
    c2 = np.sqrt((1 - c1 ** 2) * T)
    snaps = []
    t0 = time.time()
    for step in range(N_EQ + N_PROD):
        vel += 0.5 * DT * f
        pos += 0.5 * DT * vel
        vel = c1 * vel + c2 * rng.normal(size=vel.shape)   # O (Langevin)
        pos += 0.5 * DT * vel
        pos %= L
        f, _ = forces(pos, L)
        vel += 0.5 * DT * f
        if step >= N_EQ and (step - N_EQ) % SNAP_EVERY == 0:
            snaps.append(pos.copy())
    snaps = np.array(snaps)                                # (S, N, 3)
    # unwrap: 連続スナップ間の最小イメージ変位を累積
    # (スナップ間隔 100 step で粒子は L/2 以上動かない前提)
    dstep = np.diff(snaps, axis=0)
    dstep -= L * np.round(dstep / L)
    traj_u = np.concatenate([snaps[:1],
                             snaps[:1] + np.cumsum(dstep, axis=0)])  # (S,N,3)
    # Langevin は運動量非保存 → 系全体が重心拡散し、その位相回転が
    # z1 の時間平均を偽って減衰させる。重心ドリフトを除去する。
    com_u = traj_u.mean(axis=1, keepdims=True)             # (S,1,3)
    snaps_c = snaps - (com_u - com_u[0])                   # z1 用（位相補正と等価）
    rel = traj_u - com_u                                   # MSD 用（相対座標）
    i0 = len(rel) // 3
    disp = rel[-1] - rel[i0]
    msd = (disp ** 2).sum(-1).mean()
    # z1(n) スペクトル
    z1, z1err = {}, {}
    nb = 5
    for n in range(1, 13):
        ph = np.exp(1j * 2 * np.pi * n * snaps_c / L)
        z1[n] = float(np.abs(ph.mean(axis=(0, 1))).mean())
        blocks = np.array_split(np.arange(len(snaps)), nb)
        zb = [np.abs(ph[b].mean(axis=(0, 1))).mean() for b in blocks]
        z1err[n] = float(np.std(zb) / np.sqrt(nb))
    n_bragg = 2 * ncell                                    # fcc x射影周期 a/2
    elapsed = time.time() - t0
    print(f"[{label}] N={N} rho={rho} T={T}: |z1(Bragg n={n_bragg})|="
          f"{z1[n_bragg]:.4f}±{z1err[n_bragg]:.4f}, MSD(prod後半)={msd:.2f}σ², "
          f"{elapsed:.0f}s", flush=True)
    return {"label": label, "N": N, "ncell": ncell, "rho": rho, "T": T,
            "L": L, "n_bragg": n_bragg, "msd_late": float(msd),
            "z1": z1, "z1err": z1err,
            "noise_floor": 1 / np.sqrt(N * len(snaps))}


results = []
results.append(run_point(4, 1.05, 0.5, "solid_ref"))
results.append(run_point(4, 0.80, 1.0, "liquid_ref_N256"))
for T in [0.5, 1.1, 1.7]:
    results.append(run_point(4, 0.95, T, f"scan_T{T}"))
results.append(run_point(3, 0.80, 1.0, "liquid_ref_N108"))
results.append(run_point(5, 0.80, 1.0, "liquid_ref_N500"))

# ---------- 判定 ----------
def get(lbl):
    return next(r for r in results if r["label"] == lbl)

sol = get("solid_ref")
liq = get("liquid_ref_N256")
b1 = sol["z1"][sol["n_bragg"]] > 0.5
b2 = all(liq["z1"][n] < 2 * liq["noise_floor"] for n in liq["z1"])
scan = [get(f"scan_T{T}") for T in [0.5, 1.1, 1.7]]
zb_scan = [r["z1"][r["n_bragg"]] for r in scan]
b3 = max(zb_scan) / max(min(zb_scan), 1e-12) > 10
l108, l500 = get("liquid_ref_N108"), get("liquid_ref_N500")
mean108 = np.mean([l108["z1"][n] for n in l108["z1"]])
mean500 = np.mean([l500["z1"][n] for n in l500["z1"]])
size_ratio = mean108 / mean500
b4 = 1.2 < size_ratio < 4.0        # 期待 √(500/108)≈2.15 のオーダー

print("\n=== 事前判定 ===")
print(f"B1 固体 |z1(Bragg)|>0.5:        {sol['z1'][sol['n_bragg']]:.4f} → {'PASS' if b1 else 'FAIL'}")
print(f"B2 平衡液体 全n<2×ノイズフロア: floor={liq['noise_floor']:.4f}, "
      f"max|z1|={max(liq['z1'].values()):.4f} → {'PASS' if b2 else 'FAIL'}")
print(f"B3 融解スキャンで1桁降下:       {[f'{z:.3f}' for z in zb_scan]} → {'PASS' if b3 else 'FAIL'}")
print(f"B4 1/√N スケーリング:           N108/N500 = {size_ratio:.2f} (期待~2.15) → {'PASS' if b4 else 'FAIL'}")

with open("exp_B_results.json", "w") as f:
    json.dump({"meta": {"date": "2026-07-04", "dt": DT, "gamma": GAMMA,
                        "n_eq": N_EQ, "n_prod": N_PROD},
               "points": results,
               "verdict": {"B1": bool(b1), "B2": bool(b2),
                           "B3": bool(b3), "B4": bool(b4)}},
              f, indent=2, ensure_ascii=False)
print("保存: exp_B_results.json")

# ---------- 図 ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
Ts = [0.5, 1.1, 1.7]
axes[0].errorbar(Ts, zb_scan,
                 yerr=[r["z1err"][r["n_bragg"]] for r in scan],
                 fmt="o-", color="tab:purple")
axes[0].axhline(scan[0]["noise_floor"], ls=":", color="gray", label="noise floor")
axes[0].set_xlabel("T*"); axes[0].set_ylabel("|z$_1$(Bragg)|")
axes[0].set_title("Melting scan (ρ*=0.95, N=256)")
axes[0].set_yscale("log"); axes[0].legend()
msds = [r["msd_late"] for r in scan]
ax2 = axes[0].twinx()
ax2.plot(Ts, msds, "^--", color="tab:green", alpha=0.6)
ax2.set_ylabel("MSD (late, σ²)", color="tab:green")

for r, c in [(sol, "tab:blue"), (liq, "tab:red")]:
    ns = sorted(int(n) for n in r["z1"])
    axes[1].plot(ns, [r["z1"][n] for n in ns], "o-", color=c, label=r["label"])
axes[1].axhline(liq["noise_floor"], ls=":", color="gray")
axes[1].set_xlabel("n"); axes[1].set_ylabel("|z$_1$(n)|")
axes[1].set_title("Solid vs equilibrated liquid (LJ)")
axes[1].set_yscale("log"); axes[1].legend()
fig.tight_layout()
fig.savefig("exp_B_lj.png", dpi=150)
print("保存: exp_B_lj.png")
