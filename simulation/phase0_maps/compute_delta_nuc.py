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
import gc
import io
import lzma
import os
import subprocess
import sys
import tempfile
import time
import zipfile

import numpy as np
import phonopy

INDEX = os.path.join(os.path.dirname(__file__), "phonondb_index.csv")
OUT = os.path.join(os.path.dirname(__file__), "delta_nuc_results.csv")
FAIL = os.path.join(os.path.dirname(__file__), "failures.log")
T_PROBE = (0.0, 300.0)


def pick_mesh(natom):
    """eigenvector 配列 ~ n_q·(3N)²·16B を ~500MB 以下に保つ適応メッシュ。
    大きい結晶 (Dy(BO2)3 等) で mesh 24³ 固定だと数GBに達し jetsam に
    殺される（2026-07-06 実測）。natom ≤ 14 では従来通り 24（既存379件と一貫）。"""
    nq_max = 5e8 / ((3 * natom) ** 2 * 16)
    return max(8, min(24, int(nq_max ** (1 / 3))))


def download(url, timeout=30):
    """curl でダウンロード。urllib は dead URL（mp-3261 等、データセット
    非公開化の名残り）で timeout 指定が効かず永久ハングするため
    （2026-07-06 実測）、全体時間制限つきの curl に委譲する。"""
    fd, tmppath = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    try:
        r = subprocess.run(["curl", "-sL", "-f", "-m", str(timeout),
                            "-o", tmppath, url], capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f"curl rc={r.returncode} (dead/timeout URL)")
        with open(tmppath, "rb") as f:
            return f.read()
    finally:
        os.remove(tmppath)


def process_one(mp_id, formula, zip_url):
    zdata = download(zip_url)
    with zipfile.ZipFile(io.BytesIO(zdata)) as z:
        name = next(n for n in z.namelist() if n.endswith("phonopy_params.yaml.xz"))
        yaml_bytes = lzma.decompress(z.read(name))
    tmp = f"/tmp/ph_{mp_id}.yaml"
    with open(tmp, "wb") as f:
        f.write(yaml_bytes)
    try:
        ph = phonopy.load(tmp, log_level=0)
        mesh = pick_mesh(len(ph.primitive))
        ph.run_mesh([mesh] * 3, with_eigenvectors=True, is_mesh_symmetry=False)
        # freq_min=0.1 THz: ソフト/不安定モードの 1/ω² 発散を除外
        # （phonondb には虚数・極低周波モードを持つ構造が含まれ、
        #  下限なしでは δ_nuc ~ 10⁷ 級の発散が出る — 2026-07-06 実測）。
        # 正当な音響寄与の下限は mesh 24, L~5Å, v~3km/s で ~0.25 THz なので
        # 0.1 THz は物理を保ちつつ病的モードだけ落とす。
        ph.run_thermal_displacements(temperatures=T_PROBE, freq_min=0.1)
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
            gc.collect()   # phonopy の mesh eigenvectors はデカい: 蓄積防止
            time.sleep(0.7)


if __name__ == "__main__":
    main()
