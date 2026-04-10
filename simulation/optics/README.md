# optics/ — Paper 1: 光学応答の分類

δ × D_eff による炭素同素体の光学応答分類。

## 主要スクリプト

| ファイル | 内容 |
|---------|------|
| `delocalization_optics_v2.py` | タイトバインディング模型（グラフェン、ダイヤモンド、C60、1D鎖）。Kubo公式で光学伝導度を計算 |
| `classification_v2.py` | E_g + D_eff^vis 決定木による分類。6/7正答（85.7%） |
| `plot_delta_deff_map.py` | δ × D_eff マップの図生成 |
| `plot_figures_en.py` | 論文用英語図生成 |
| `quantitative_validation.py` | TB計算の誘電関数を実験値と照合 |

## 実行

```bash
pip install numpy scipy matplotlib
python delocalization_optics_v2.py    # TB模型 + 光学伝導度
python classification_v2.py           # 決定木分類
python plot_figures_en.py             # 論文図生成
```

## 検証結果

| テスト | 結果 |
|--------|------|
| E_g + D_eff^vis 決定木 | 6/7正答 (85.7%)。グラフェンのみ積層数Nが追加で必要 |
| δプロキシ間相関 | r = 0.73-0.89（3指標） |
| δ-E_g逆相関 | r = -0.70（文献）、r = -0.86（TB） |
| Anderson無秩序ロバストネス | δ×(D_eff+1)高い系がスペクトルを保存 |

## 理論的基盤

- `algorithm_spec.md` — アルゴリズム仕様と計算フロー
- `theory/optics/02_glossiness_theory.md` — 光沢の現象論的再記述
- `theory/core/01_core_framework.md` — δ × D_eff フレームワーク定義
