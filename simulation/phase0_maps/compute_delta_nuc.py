"""
フェーズ0: phonondb (NIMS MDR, CC-BY 4.0) から δ_nuc を抽出するパイプライン

戦略: drafts/strategy_ml_descriptor_2026-07-05.md §5
  結晶の δ_nuc は既存フォノンDBの後処理のみで出る（新規DFT計算ゼロ）。

各材料について保存する量:
  u2_0K, u2_300K [Å², 1方向平均]  — 熱変位の対角平均
  d_min [Å]                        — 最近接原子間距離（Lindemann 規格化）
  delta_nuc_300K = u2_300K / d_min²
  q300 = u2_0K / u2_300K           — 300K での量子(ゼロ点)成分比
                                     （coth 構造: 高温で→0、量子固体で→1）

使い方:
  python compute_delta_nuc.py test       # Si + NaCl の2件で検証
  python compute_delta_nuc.py N          # インデックス先頭 N 件を処理
  python compute_delta_nuc.py all        # 全 10034 件（~一晩、要マシン空き）

出力: delta_nuc_results.csv（追記式・再開可能）、失敗は failures.log
サーバー礼儀: 1件ごとに 0.7s スリープ。
"""
import csv
import io
import lzma
import os
import sys
import time
import urllib.request
import zipfile

import numpy as np
import phonopy

INDEX = os.path.join(os.path.dirname(__file__), "phonondb_index.csv")
OUT = os.path.join(os.path.dirname(__file__), "delta_nuc_results.csv")
FAIL = os.path.join(os.path.dirname(__file__), "failures.log")
MESH = 24
T_PROBE = (0.0, 300.0)


def process_one(mp_id, formula, zip_url):
    with urllib.request.urlopen(zip_url, timeout=120) as r:
        zdata = r.read()
    with zipfile.ZipFile(io.BytesIO(zdata)) as z:
        name = next(n for n in z.namelist() if n.endswith("phonopy_params.yaml.xz"))
        yaml_bytes = lzma.decompress(z.read(name))
    tmp = f"/tmp/ph_{mp_id}.yaml"
    with open(tmp, "wb") as f:
        f.write(yaml_bytes)
    try:
        ph = phonopy.load(tmp, log_level=0)
        ph.run_mesh([MESH] * 3, with_eigenvectors=True, is_mesh_symmetry=False)
        ph.run_thermal_displacements(temperatures=T_PROBE)
        # (n_T, natom*3) の ⟨u_i²⟩ 成分 → 全原子・全方向平均
        td = np.array(ph.thermal_displacements.thermal_displacements)
        u2_0, u2_300 = td[0].mean(), td[1].mean()
        # 最近接距離（プリミティブセル、周期像込み）
        cell = ph.primitive
        pos = cell.positions
        lat = cell.cell
        dmin = np.inf
        for i in range(len(pos)):
            for j in range(len(pos)):
                for sx in (-1, 0, 1):
                    for sy in (-1, 0, 1):
                        for sz in (-1, 0, 1):
                            if i == j and sx == sy == sz == 0:
                                continue
                            d = np.linalg.norm(
                                pos[j] + sx * lat[0] + sy * lat[1] + sz * lat[2]
                                - pos[i])
                            dmin = min(dmin, d)
        return {"mp_id": mp_id, "formula": formula, "natom_prim": len(pos),
                "u2_0K_A2": u2_0, "u2_300K_A2": u2_300, "d_min_A": dmin,
                "delta_nuc_300K": u2_300 / dmin ** 2,
                "q300": u2_0 / u2_300}
    finally:
        os.remove(tmp)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "test"
    with open(INDEX) as f:
        index = list(csv.DictReader(f))
    if arg == "test":
        targets = [r for r in index if r["mp_id"] in ("149", "22862")]
    elif arg == "all":
        targets = index
    else:
        targets = index[: int(arg)]

    done = set()
    if os.path.exists(OUT):
        with open(OUT) as f:
            done = {r["mp_id"] for r in csv.DictReader(f)}
    fields = ["mp_id", "formula", "natom_prim", "u2_0K_A2", "u2_300K_A2",
              "d_min_A", "delta_nuc_300K", "q300"]
    new_file = not os.path.exists(OUT)
    with open(OUT, "a", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=fields)
        if new_file:
            w.writeheader()
        for k, row in enumerate(targets):
            if row["mp_id"] in done:
                continue
            try:
                t0 = time.time()
                res = process_one(row["mp_id"], row["formula"], row["zip_url"])
                w.writerow(res)
                fo.flush()
                print(f"[{k+1}/{len(targets)}] mp-{res['mp_id']} {res['formula']}: "
                      f"u2(300K)={res['u2_300K_A2']:.5f} Å², d_min={res['d_min_A']:.3f}, "
                      f"δ_nuc={res['delta_nuc_300K']:.5f}, q300={res['q300']:.3f} "
                      f"({time.time()-t0:.0f}s)", flush=True)
            except Exception as e:
                with open(FAIL, "a") as ff:
                    ff.write(f"{row['mp_id']}\t{row['formula']}\t{e}\n")
                print(f"[{k+1}/{len(targets)}] mp-{row['mp_id']} FAILED: {e}",
                      flush=True)
            time.sleep(0.7)


if __name__ == "__main__":
    main()
