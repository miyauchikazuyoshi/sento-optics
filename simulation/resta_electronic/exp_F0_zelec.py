"""
実験F-0: 液体 Na の電子側 Resta 位相 z_elec（既存 wfc の後処理）

方法: 平面波基底で e^{i b·r}（b = 最小逆格子ベクトル）は G シフト演算。
  M_ij = <psi_i| e^{i b·r} |psi_j> = Σ_G c_i*(G) c_j(G−b)
  z_elec = det(M_occ)          [独立電子系の Resta 位相]

事前判定基準 (PLAN.md):
  F0-1: 全占有 |z_elec| < 0.1（金属的）
  F0-2: semicore(下位256) の |z|^(1/N) >> 3s(上位32) の |z|^(1/N)
  F0-3: 占有数 ±2 で F0-1 の結論が不変

近似（明記）: PAW augmentation なし / 整数占有 / 単一スナップショット
"""
import json
import time
import numpy as np
import h5py

WFC = ("/Users/miyauchikazuyoshi/Documents/GitHub/sento-optics/"
       "simulation/surface_tension/aimd/tmp/Na_liquid.save/wfc1.hdf5")
L_ANG = 13.8133          # 立方セル (exp_A で確認済み)
NE_BANDS = 288           # 占有バンド: 9e/atom × 64 / 2 (spin縮退)
N_ELEC = 576

t0 = time.time()
with h5py.File(WFC, "r") as f:
    mill = f["MillerIndices"][:]            # (ngw, 3) int
    evc_raw = f["evc"][:]                   # (nbnd, 2*ngw) float64
    gamma_only = f.attrs["gamma_only"]
    nbnd = int(f.attrs["nbnd"])
ngw = mill.shape[0]
print(f"読込: nbnd={nbnd}, ngw={ngw}, gamma_only={gamma_only} "
      f"({time.time()-t0:.1f}s)")

# 複素化（占有+感度チェック分のみメモリに展開）
NB_KEEP = NE_BANDS + 2
c_half = evc_raw[:NB_KEEP, 0::2] + 1j * evc_raw[:NB_KEEP, 1::2]   # (NB, ngw)
del evc_raw

# ---------- gamma_only 展開: c(-G) = c(G)* ----------
mill_t = [tuple(m) for m in mill]
assert mill_t[0] == (0, 0, 0) or (0, 0, 0) in mill_t, "G=0 が見つからない"
# フル G リスト: stored + (-stored \ {0})
neg_mask = np.array([m != (0, 0, 0) for m in mill_t])
mill_full = np.concatenate([mill, -mill[neg_mask]])               # (nfull, 3)
c_full = np.concatenate([c_half, np.conj(c_half[:, neg_mask])], axis=1)
nfull = mill_full.shape[0]
norm = (np.abs(c_full) ** 2).sum(axis=1)
print(f"フル展開: nfull={nfull}, ノルム診断 min/max = "
      f"{norm.min():.4f}/{norm.max():.4f}（~1 なら正常, PAW擬WFなので≲1も可）")

index = {tuple(m): i for i, m in enumerate(mill_full)}

def z_block(band_slice, axis, normalize=False):
    """z = det(M) を指定バンドブロックで。M_ij = Σ_G ci*(G) cj(G−b)

    normalize=True: 擬WFノルムで各バンドを再規格化（PAW augmentation の
    対角近似補正。2p バンドはノルム 0.598 しかないため、未補正では
    det が PAW 欠損分だけ過小評価される）"""
    b = np.zeros(3, int)
    b[axis] = 1
    # cj_shift[G] = cj(G − b)
    src = np.full(nfull, -1)
    for i, m in enumerate(mill_full):
        j = index.get((m[0] - b[0], m[1] - b[1], m[2] - b[2]))
        if j is not None:
            src[i] = j
    C = c_full[band_slice]
    if normalize:
        C = C / np.sqrt((np.abs(C) ** 2).sum(axis=1, keepdims=True))
    Cs = np.zeros_like(C)
    ok = src >= 0
    Cs[:, ok] = C[:, src[ok]]
    M = np.conj(C) @ Cs.T
    sign, logdet = np.linalg.slogdet(M)
    return logdet          # log|det M|

labels = ["x", "y", "z"]
results = {"full": {}, "semicore": {}, "band3s": {}, "sensitivity": {}}
print(f"\n{'方向':>4} {'log|z|(全288)':>14} {'|z|':>10} "
      f"{'|z|^(1/N) semicore':>19} {'|z|^(1/N) 3s':>13}")
for ax in range(3):
    ld_full = z_block(slice(0, NE_BANDS), ax)
    ld_semi = z_block(slice(0, 256), ax)
    ld_3s = z_block(slice(256, 288), ax)
    gm_semi = np.exp(ld_semi / 256)
    gm_3s = np.exp(ld_3s / 32)
    results["full"][labels[ax]] = ld_full
    results["semicore"][labels[ax]] = gm_semi
    results["band3s"][labels[ax]] = gm_3s
    print(f"{labels[ax]:>4} {ld_full:>14.2f} {np.exp(ld_full):>10.2e} "
          f"{gm_semi:>19.4f} {gm_3s:>13.4f}")

# λ² 換算（全電子, spin込み: ln|z_N|² = 4*logdet）
lam2 = {labels[ax]: -L_ANG ** 2 * 4 * results["full"][labels[ax]]
        / (4 * np.pi ** 2 * N_ELEC) for ax in range(3)}
print(f"\nλ² (Å², 全電子換算): " +
      ", ".join(f"{k}={v:.2f}" for k, v in lam2.items()))

# 感度チェック: 占有 ±2 バンド
for ne in [NE_BANDS - 2, NE_BANDS + 2]:
    ld = z_block(slice(0, ne), 0)
    results["sensitivity"][str(ne)] = ld
    print(f"感度: 占有={ne} バンド → log|z_x| = {ld:.2f} (|z|={np.exp(ld):.2e})")

# PAW 対角近似補正（ノルム再規格化）版のブロック値
results["semicore_norm"] = {}
results["band3s_norm"] = {}
print("\n--- PAW 対角近似補正（ノルム再規格化）後 ---")
for ax in range(3):
    gm_semi_n = np.exp(z_block(slice(0, 256), ax, normalize=True) / 256)
    gm_3s_n = np.exp(z_block(slice(256, 288), ax, normalize=True) / 32)
    results["semicore_norm"][labels[ax]] = gm_semi_n
    results["band3s_norm"][labels[ax]] = gm_3s_n
    print(f"{labels[ax]}: semicore {gm_semi_n:.4f} vs 3s {gm_3s_n:.4f} "
          f"(比 {gm_semi_n/gm_3s_n:.2f}x)")

# ---------- 判定 ----------
zx = np.exp(results["full"]["x"])
f01 = all(np.exp(results["full"][a]) < 0.1 for a in labels)
f02 = all(results["semicore"][a] > 3 * results["band3s"][a] for a in labels)
f03 = all(np.exp(v) < 0.1 for v in results["sensitivity"].values())
print(f"\n=== 判定 ===")
print(f"F0-1 |z_elec| < 0.1 (金属的):        {'PASS' if f01 else 'FAIL'}")
print(f"F0-2 semicore局在 >> 3s非局在:       {'PASS' if f02 else 'FAIL'}")
print(f"F0-3 占有±2で頑健:                   {'PASS' if f03 else 'FAIL'}")

out = {"meta": {"date": "2026-07-05", "wfc": WFC, "L_ang": L_ANG,
                "n_occ_bands": NE_BANDS, "n_elec": N_ELEC,
                "approx": ["no PAW augmentation", "integer occupation",
                           "single snapshot"]},
       "log_z_full": results["full"],
       "geom_mean_semicore": results["semicore"],
       "geom_mean_3s": results["band3s"],
       "lambda2_A2": lam2,
       "sensitivity_logz_x": results["sensitivity"],
       "verdict": {"F0_1": bool(f01), "F0_2": bool(f02), "F0_3": bool(f03)}}
with open("exp_F0_results.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("保存: exp_F0_results.json")

# 図: semicore vs 3s のコントラスト
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))
xpos = np.arange(3)
ax.bar(xpos - 0.18, [results["semicore"][a] for a in labels], 0.36,
       label="semicore (2s2p, 256 bands)", color="tab:blue")
ax.bar(xpos + 0.18, [results["band3s"][a] for a in labels], 0.36,
       label="3s valence (32 bands)", color="tab:red")
ax.set_xticks(xpos); ax.set_xticklabels([f"|z|$^{{1/N}}$ ({a})" for a in labels])
ax.set_ylabel("per-band geometric mean of |z|")
ax.set_title("Liquid Na: core localized vs valence delocalized (Exp. F-0)")
ax.legend()
fig.tight_layout()
fig.savefig("exp_F0_zelec.png", dpi=150)
print("保存: exp_F0_zelec.png")
