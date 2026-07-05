"""
実験F-2: NaCl 結晶（絶縁対照）の z_elec — 「2枚看板」の絶縁側

事前判定基準 (PLAN.md, 実行前に精密化済み):
  F2-1: λ²(NaCl) < λ²(液体Na)/2 (< 2.2 Å²)
  F2-2: Cl 3p 価電子帯（上位96バンド）の PAW補正後幾何平均 |z|^(1/N) > 0.8
  F2-3: Na semicore は液体 Na と同値（補正後 ~0.99）— コア局在の系非依存性

バンド構成（エネルギー順の想定・ノルムで間接確認）:
  [0:32] Na 2s / [32:128] Na 2p / [128:160] Cl 3s / [160:256] Cl 3p
"""
import json
import numpy as np
import h5py

WFC = "./tmp/NaCl.save/wfc1.hdf5"
L_ANG = 11.28
NE_BANDS = 256
N_ELEC = 512

with h5py.File(WFC, "r") as f:
    mill = f["MillerIndices"][:]
    evc_raw = f["evc"][:NE_BANDS + 2]
    nbnd = int(f.attrs["nbnd"])
ngw = mill.shape[0]
print(f"読込: nbnd={nbnd}, ngw={ngw}")

c_half = evc_raw[:, 0::2] + 1j * evc_raw[:, 1::2]
del evc_raw
neg_mask = ~np.all(mill == 0, axis=1)
mill_full = np.concatenate([mill, -mill[neg_mask]])
c_full = np.concatenate([c_half, np.conj(c_half[:, neg_mask])], axis=1)
nfull = mill_full.shape[0]

# ノルム診断（バンドブロックの同定を兼ねる）
norm = (np.abs(c_full) ** 2).sum(axis=1)
blocks = {"Na 2s": slice(0, 32), "Na 2p": slice(32, 128),
          "Cl 3s": slice(128, 160), "Cl 3p": slice(160, 256)}
print("擬WFノルム（ブロック同定の診断）:")
for name, sl in blocks.items():
    print(f"  {name:6}: {norm[sl].mean():.3f} ± {norm[sl].std():.3f}")

index = {tuple(m): i for i, m in enumerate(mill_full)}

def z_block(band_slice, axis, normalize=False):
    b = np.zeros(3, int)
    b[axis] = 1
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
    sign, logdet = np.linalg.slogdet(np.conj(C) @ Cs.T)
    return logdet

labels = ["x", "y", "z"]
res = {"logz_full": {}, "lambda2": {}, "blocks_norm_corrected": {}}
print(f"\n{'方向':>4} {'log|z|(全256)':>14} {'λ² (Å²)':>10}")
for ax in range(3):
    ld = z_block(slice(0, NE_BANDS), ax)
    lam2 = -L_ANG ** 2 * 4 * ld / (4 * np.pi ** 2 * N_ELEC)
    res["logz_full"][labels[ax]] = ld
    res["lambda2"][labels[ax]] = lam2
    print(f"{labels[ax]:>4} {ld:>14.2f} {lam2:>10.3f}")

print("\nPAW対角補正後のブロック幾何平均 |z|^(1/N) (x方向):")
for name, sl in blocks.items():
    n = sl.stop - sl.start
    gm = np.exp(z_block(sl, 0, normalize=True) / n)
    res["blocks_norm_corrected"][name] = gm
    print(f"  {name:6}: {gm:.4f}")

# ---------- 判定（液体Naとの対照込み） ----------
try:
    with open("exp_F0_results.json") as f:
        f0 = json.load(f)
    lam2_liq = float(np.mean(list(f0["lambda2_A2"].values())))
except FileNotFoundError:
    lam2_liq = 4.39
lam2_nacl = float(np.mean(list(res["lambda2"].values())))
gm_cl3p = res["blocks_norm_corrected"]["Cl 3p"]
gm_semicore = (res["blocks_norm_corrected"]["Na 2s"] * 1 +
               res["blocks_norm_corrected"]["Na 2p"] * 3) / 4  # バンド数比の重み

f21 = lam2_nacl < lam2_liq / 2
f22 = gm_cl3p > 0.8
f23 = abs(gm_semicore - 0.99) < 0.03
print(f"\n=== 判定 ===")
print(f"F2-1 λ²(NaCl)={lam2_nacl:.2f} < λ²(液体Na)/2={lam2_liq/2:.2f}: "
      f"{'PASS' if f21 else 'FAIL'}")
print(f"F2-2 Cl3p 幾何平均 {gm_cl3p:.3f} > 0.8:  {'PASS' if f22 else 'FAIL'}")
print(f"F2-3 Na semicore {gm_semicore:.3f} ≈ 0.99: {'PASS' if f23 else 'FAIL'}")
print(f"\n2枚看板の対照: 液体Na λ²={lam2_liq:.2f} Å² (発散量のN=64値) vs "
      f"NaCl λ²={lam2_nacl:.2f} Å² (有限・収束量)")

with open("exp_F2_results.json", "w") as f:
    json.dump({"meta": {"date": "2026-07-05", "L_ang": L_ANG,
                        "n_occ_bands": NE_BANDS,
                        "approx": ["no PAW augmentation (diag-corrected blocks)",
                                   "single crystal snapshot (T=0)"]},
               **res,
               "contrast": {"lambda2_liquid_Na": lam2_liq,
                            "lambda2_NaCl": lam2_nacl},
               "verdict": {"F2_1": bool(f21), "F2_2": bool(f22),
                           "F2_3": bool(f23)}},
              f, indent=2, ensure_ascii=False)
print("保存: exp_F2_results.json")
