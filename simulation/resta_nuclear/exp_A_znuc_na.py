"""
実験A: 液体Na AIMDトラジェクトリからの z_nuc 試算

仮説 (memo_nuclear_resta_phase.md):
  核版 Resta 位相 z1(k) = <exp(i k x_I)> は
  - 液体ではすべての k≠0 でノイズフロアまで落ちる（一様密度、Bragg消失）
  - 固体では Bragg 波数で有限に残る（Debye-Waller 因子）

事前判定基準:
  |z1|_solid(G_Bragg) / |z1|_liquid(同波数帯) > 10 で合格

データ: simulation/surface_tension/aimd/tmp/Na_liquid.mdtrj
  172 ステップ, 64 Na 原子, 立方セル L=13.813 Å, T=471 K (rescaling)
対照: モック bcc 固体 (3x3x3 bcc = 54原子, a=4.29 Å, ガウス熱変位)
"""

import json
import numpy as np

rng = np.random.default_rng(20260704)  # 再現性のためシード固定

TRJ = "../surface_tension/aimd/tmp/Na_liquid.mdtrj"
NAT = 64

# ---------- 1. パース ----------
rows = []
with open(TRJ) as f:
    for line in f:
        vals = line.split()
        if len(vals) == 204:
            rows.append([float(v) for v in vals])
data = np.array(rows)                     # (172, 204)
nstep = data.shape[0]
time_ps = data[:, 0]
temp = data[:, 1]
cell = data[0, 3:12].reshape(3, 3)
L = cell[0, 0]                            # 立方セルを仮定
coords_raw = data[:, 12:204]              # (172, 192)

print(f"steps={nstep}, L={L:.4f} (単位は密度チェックで判定), T range: "
      f"{temp.min():.0f}-{temp.max():.0f} K")

# 密度チェック: L が Å なら n=64/L^3 ~ 0.024 /Å^3 (液体Na 471K の実測 0.927 g/cm3 と整合)
n_density = NAT / L**3
rho_gcc = n_density * 22.99 / 6.02214e23 * 1e24
print(f"密度チェック: {rho_gcc:.3f} g/cm3 (L=Å 仮定; 液体Na@471K 実測 ~0.927)")

# ---------- 2. 座標並び順の自己検証 ----------
def min_dist(pos):
    d = pos[None, :, :] - pos[:, None, :]
    d -= L * np.round(d / L)              # 最小イメージ
    r = np.sqrt((d**2).sum(-1))
    np.fill_diagonal(r, 1e9)
    return r.min()

interp_A = coords_raw[0].reshape(NAT, 3)        # (x1,y1,z1, x2,y2,z2, ...)
interp_B = coords_raw[0].reshape(3, NAT).T      # (all x, all y, all z)
dA, dB = min_dist(interp_A), min_dist(interp_B)
print(f"最近接距離: 解釈A(xyz交互)={dA:.3f}, 解釈B(座標別)={dB:.3f}  "
      f"(液体Naの物理値 ~3.2-3.7 Å)")
reshape_mode = "A" if abs(dA - 3.4) < abs(dB - 3.4) else "B"
if reshape_mode == "A":
    pos = coords_raw.reshape(nstep, NAT, 3)
else:
    pos = coords_raw.reshape(nstep, 3, NAT).transpose(0, 2, 1)
print(f"採用: 解釈{reshape_mode}")

# ---------- 3. 重心ドリフト（多体 z_N の有効性チェック） ----------
com = pos.sum(axis=1)                     # (nstep, 3) 重心×N
com_drift = np.abs(com - com[0]).max()
print(f"Σx_I の最大ドリフト: {com_drift:.4f} Å "
      f"({'重心ほぼ固定 → 多体z_Nは初期値を保持し情報なし' if com_drift < 0.5 else '重心が動く → 多体z_Nも有効'})")

# ---------- 4. 単粒子 z1(n) スペクトル ----------
NMAX = 10
half = nstep // 2
windows = {"全区間": slice(0, nstep), "後半のみ": slice(half, nstep)}
results = {}
for wname, sl in windows.items():
    p = pos[sl]
    ns_w = p.shape[0]
    z1 = {}
    for n in range(1, NMAX + 1):
        phase = np.exp(1j * 2 * np.pi * n * p / L)   # (steps, NAT, 3)
        # 方向ごとに全原子・全ステップ平均
        zvec = phase.mean(axis=(0, 1))               # (3,) complex
        # ブロック平均で標準誤差（時間相関対策: 4ブロック）
        nb = 4
        blocks = np.array_split(np.arange(ns_w), nb)
        zb = np.array([phase[b].mean(axis=(0, 1)) for b in blocks])  # (4,3)
        err = np.abs(zb).std(axis=0) / np.sqrt(nb)
        z1[n] = (np.abs(zvec), err)
    results[wname] = z1

# ノイズフロア: 一様分布での |z1| 期待値 ~ 1/sqrt(N_eff)
# 有効サンプル数: 64原子 × ブロック数(独立と見なせる時間区間 ~4-8)
noise_floor = 1 / np.sqrt(NAT * 8)
print(f"\nノイズフロア推定 ~{noise_floor:.3f}")

# S(k)第一ピーク相当: 液体Na k1 ~ 2.0 /Å → n = k1 L / 2π
n_peak = round(2.0 * L / (2 * np.pi))
print(f"S(k)第一ピーク相当の n = {n_peak} (k = {2*np.pi*n_peak/L:.2f} /Å)")

print(f"\n--- 液体Na: |z1(n)| (x,y,z方向, 後半のみ) ---")
print(f"{'n':>3} {'k(/Å)':>7} {'|z1|_x':>9} {'|z1|_y':>9} {'|z1|_z':>9}")
for n in range(1, NMAX + 1):
    a, e = results["後半のみ"][n]
    k = 2 * np.pi * n / L
    print(f"{n:>3} {k:>7.3f} {a[0]:>9.4f} {a[1]:>9.4f} {a[2]:>9.4f}")

# ---------- 5. モック bcc 固体対照 ----------
a_bcc = 4.29                              # bcc Na 格子定数 (Å)
ncell = 3
L_mock = ncell * a_bcc
base = []
for i in range(ncell):
    for j in range(ncell):
        for k_ in range(ncell):
            base.append([i, j, k_])
            base.append([i + 0.5, j + 0.5, k_ + 0.5])
base = np.array(base) * a_bcc             # (54, 3)
NMOCK = len(base)
sigma2 = 0.05                             # ⟨u_x²⟩ ~0.05 Å² (Na, 融点近傍の熱変位)
mock_steps = nstep
mock = base[None] + rng.normal(0, np.sqrt(sigma2), (mock_steps, NMOCK, 3))

z1_mock = {}
for n in range(1, NMAX + 1):
    ph = np.exp(1j * 2 * np.pi * n * mock / L_mock)
    z1_mock[n] = np.abs(ph.mean(axis=(0, 1)))        # (3,)

# bcc の x 射影は周期 a/2 → Bragg は n = 2*ncell = 6
n_bragg = 2 * ncell
dw_theory = np.exp(-0.5 * (2 * np.pi * n_bragg / L_mock) ** 2 * sigma2)
print(f"\n--- モックbcc固体: |z1(n)| (σ²={sigma2} Å²) ---")
print(f"{'n':>3} {'k(/Å)':>7} {'|z1|_x':>9}   注")
for n in range(1, NMAX + 1):
    k = 2 * np.pi * n / L_mock
    note = f"← Bragg (DW理論値 {dw_theory:.3f})" if n == n_bragg else ""
    print(f"{n:>3} {k:>7.3f} {z1_mock[n][0]:>9.4f}   {note}")

# ---------- 6. 判定 ----------
z_solid = z1_mock[n_bragg].mean()
z_liq_at_peak = results["後半のみ"][n_peak][0].mean()
# 液体側は「Braggに相当する波数帯」での値: n_peak と n_bragg 換算波数が近いことを確認
ratio = z_solid / max(z_liq_at_peak, 1e-12)
verdict = "PASS" if ratio > 10 else "FAIL"
print(f"\n=== 事前判定基準: |z1|_solid(Bragg) / |z1|_liquid(k~2Å⁻¹) > 10 ===")
print(f"固体(Bragg) {z_solid:.4f} / 液体 {z_liq_at_peak:.4f} = {ratio:.1f} → {verdict}")
print(f"(液体値はノイズフロア {noise_floor:.3f} と比較: "
      f"{'ゼロと整合' if z_liq_at_peak < 2*noise_floor else '有限の残留構造あり'})")

# ---------- 7. 保存 ----------
out = {
    "meta": {"date": "2026-07-04", "steps": nstep, "L_ang": float(L),
             "T_K": [float(temp.min()), float(temp.max())],
             "reshape_mode": reshape_mode, "com_drift_ang": float(com_drift),
             "noise_floor": float(noise_floor)},
    "liquid_z1_second_half": {
        str(n): {"k_invA": 2 * np.pi * n / L,
                 "abs_xyz": results["後半のみ"][n][0].tolist(),
                 "err_xyz": results["後半のみ"][n][1].tolist()}
        for n in range(1, NMAX + 1)},
    "mock_bcc": {"sigma2_A2": sigma2, "n_bragg": n_bragg,
                 "dw_theory": float(dw_theory),
                 "z1_x": {str(n): float(z1_mock[n][0]) for n in range(1, NMAX + 1)}},
    "verdict": {"ratio": float(ratio), "criterion": "ratio > 10",
                "result": verdict},
}
with open("exp_A_results.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("\n保存: exp_A_results.json")

# ---------- 8. 図 ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4.5))
ks = [2 * np.pi * n / L for n in range(1, NMAX + 1)]
liq = [results["後半のみ"][n][0].mean() for n in range(1, NMAX + 1)]
liq_err = [results["後半のみ"][n][1].mean() for n in range(1, NMAX + 1)]
ks_m = [2 * np.pi * n / L_mock for n in range(1, NMAX + 1)]
sol = [z1_mock[n].mean() for n in range(1, NMAX + 1)]
ax.errorbar(ks, liq, yerr=liq_err, fmt="o-", label="liquid Na (AIMD, 471 K)", color="tab:red")
ax.plot(ks_m, sol, "s--", label=f"mock bcc solid (σ²={sigma2} Å²)", color="tab:blue")
ax.axhline(noise_floor, ls=":", color="gray", label="noise floor")
ax.set_xlabel("k = 2πn/L  (Å$^{-1}$)")
ax.set_ylabel("|z$_1$(k)|")
ax.set_title("Nuclear Resta phase: liquid vs solid Na (Exp. A)")
ax.set_yscale("log")
ax.legend()
fig.tight_layout()
fig.savefig("exp_A_znuc.png", dpi=150)
print("保存: exp_A_znuc.png")
