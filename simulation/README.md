# simulation/ — 数値検証

δ枠組みの主張を数値的に検証するコード・データ・結果。

## ディレクトリ構造

```
simulation/
├── optics/              Paper 1: 光学応答の分類
│   ├── delocalization_optics_v2.py   TB模型（グラフェン、ダイヤモンド、C60、1D鎖）
│   ├── classification_v2.py          決定木による分類検証
│   ├── plot_*.py                     図の生成
│   └── figures/                      生成済み図
│
├── surface_tension/     Paper 2: 表面張力とsp/d均一性
│   ├── test1-7_*.py                  自己批判テスト群
│   ├── test7_extended.py             15元素ダイマー + 価電子δ
│   ├── test_2var_regression.py       Phase 1: N_d 2変数回帰
│   ├── test_orbital_decomposed_delta.py  Phase 2: 軌道分解δ
│   ├── test_ws_boundary_density.py   Phase 3: WS境界密度 vs n_ws
│   ├── test_DEF_checks.py           構造/相対論/エネルギー窓チェック
│   ├── paper2_rethink.md            主張再構築メモ（Phase 1-3結果）
│   ├── qe_slab/                     QEスラブ計算（14金属）
│   │   ├── *_scf.in                 SCF入力ファイル
│   │   ├── *_val_avg.dat            価電子面平均データ
│   │   ├── analyze_15metals.py      14金属一括解析
│   │   └── wannier/                 バルクWannier計算（5金属）
│   └── DATA_SOURCES.md              データ出典一覧
│
├── ising_rg/            Ising RG: δのRGフロー変数検証
│   ├── ising_rg_delta_v2.py         v2: 磁化IPR（失敗→原因特定）
│   ├── ising_rg_delta_v3_pattern.py v3: ブロックパターンIPR（フロー反転確認）
│   └── README.md                    v1→v2→v3の実験記録
│
└── wannier_carbon/      Wannier計算: ダイヤモンド/グラファイトのΩ確認
    ├── diamond/, graphite/          各物質の計算
    ├── analyze_spreads.py           Ω解析
    └── README.md
```

## 検証のステータス

| 検証 | 結果 | Paper |
|------|------|-------|
| 炭素同素体の光学分類 | 6/7正答 (85.7%) | Paper 1 |
| δプロキシ間の相互相関 | r = 0.73-0.89 | Paper 1 |
| Anderson無秩序ロバストネス | フロー反転確認 | Paper 1 |
| ダイマーδ vs 中間点密度比 | **r = 0.89** | Paper 2 |
| 14金属スラブ sp/d分離 | **p = 0.00008** | Paper 2 |
| Wannier spread sp/d比 | 6-19倍 | Paper 2 |
| δ vs Miedema n_ws | r = 0.10（**無相関**） | Paper 2 |
| Ising RG v3フロー反転 | Tcで確認 | (探索的) |

## 環境

```bash
# Paper 1 (optics): Python のみ
pip install numpy scipy matplotlib

# Paper 2 (surface_tension): PySCF + QE
pip install pyscf numpy scipy matplotlib
# QE: conda activate qe (Quantum ESPRESSO 7.5)

# Ising RG: Python のみ
pip install numpy scipy matplotlib
```
