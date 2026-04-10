# surface_tension/ — Paper 2: 表面張力とsp/d電子均一性

価電子の空間均一性（δ）がsp/d金属の表面張力変動を支配することの検証。

## 主張の構造（Paper 2.1再構築後）

```
δ → sp/d均一性差 → 界面電子密度パターン → 表面張力の系統性
     r=0.89         p=0.00008
```

**注意**: δとMiedemaのn_wsは直接には無相関（r=0.10）。
δは「均一性」（正規化ratio）を測り、n_wsは「絶対密度」を測る。
詳細は `paper2_rethink.md` を参照。

## 主要スクリプト

### 初期探索（test1-7）
| ファイル | 内容 |
|---------|------|
| `test1_dft_ipr.py` | DFTクラスターのIPR計算 |
| `test2_monotonicity.py` | δの単調性テスト |
| `test5_nws_miedema.py` | Miedema n_wsとの比較 |
| `test7_delta_causes_nws.py` | 11元素ダイマー: δ → 中間点密度 |

### 拡張検証
| ファイル | 内容 |
|---------|------|
| `test7_extended.py` | **15元素ダイマー + 価電子δ_val** |
| `test_2var_regression.py` | Phase 1: δ + N_d 2変数回帰 (R²=0.40) |
| `test_orbital_decomposed_delta.py` | Phase 2: 軌道分解δ (**改善せず** R²=0.28) |
| `test_ws_boundary_density.py` | Phase 3: DFT n_mid(abs) vs n_ws (r=0.79) |
| `test_DEF_checks.py` | 構造/相対論/エネルギー窓チェック（全て二次的） |

### QEスラブ計算
| ファイル | 内容 |
|---------|------|
| `qe_slab/analyze_15metals.py` | 14金属一括解析（sp/d分離 p=0.00008） |
| `qe_slab/generate_new_elements.py` | 10新元素の入力ファイル生成 |
| `qe_slab/run_all_new.sh` | バッチ実行スクリプト |
| `qe_slab/wannier/` | 5金属バルクWannier計算 |

## ドキュメント
| ファイル | 内容 |
|---------|------|
| `paper2_rethink.md` | **Phase 1-3 + D,E,F結果。δ vs n_wsギャップの解明** |
| `DATA_SOURCES.md` | データ出典（γ値、r_s等） |

## 検証結果サマリ

| テスト | 結果 | 解釈 |
|--------|------|------|
| δ_val vs midpoint ratio (15 dimers) | **r = 0.89** | δが均一性を強く予測 |
| sp/d分離 (14 slabs) | **p = 0.00008** | sp(0.96) vs d(0.38) |
| Wannier sp/d比 (5 metals) | **6-19×** | 独立確認 |
| δ vs Miedema n_ws^{1/3} | r = 0.10 | **無相関** |
| n_mid(abs) vs n_ws^{1/3} | r = 0.79 | 絶対密度は対応する |
| δ + N_d 回帰 | R² = 0.40 | d電子数が部分的因子 |
| 軌道分解δ | R² = 0.28 | **改善しない** |
| 構造効果 | r = 0.986 (sp内) | 二次的 |
| 相対論 (Ag) | Δδ = +1.5% | 二次的 |
| エネルギー窓 | < 3% | 二次的 |

## 実行

```bash
# ダイマー計算
pip install pyscf numpy scipy matplotlib
python test7_extended.py

# QEスラブ（要Quantum ESPRESSO）
conda activate qe
cd qe_slab && bash run_all_new.sh
python analyze_15metals.py

# Phase 1-3チェック
python test_2var_regression.py
python test_orbital_decomposed_delta.py
python test_ws_boundary_density.py
python test_DEF_checks.py
```
