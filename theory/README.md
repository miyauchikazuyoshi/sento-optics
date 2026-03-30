# theory/ — 理論メモの構成

## ディレクトリ構造

```
theory/
├── core/                    # 基盤（Paper 横断）
│   ├── 01_core_framework.md   # δ×D_eff フレームワークの定義
│   ├── 04_falsification.md    # 反証条件一覧
│   └── glossary.md            # 用語・記号の定義
│
├── optics/                  # 光沢理論（Paper 1）
│   └── 02_glossiness_theory.md  # 位相保存的界面応答としての光沢
│
├── surface_tension/         # 表面張力理論（Paper 2）
│   └── surface_tension_theory.md  # δ による Miedema n_ws の起源解明
│
├── phase/                   # 相分類・液体再定義（Paper 3）
│   ├── 03_phase_unification.md        # 相の連続的統一記述（初期メモ）
│   ├── paper3_phase_diagram_theory.md # (δ_nuc, δ_elec) 相図の完全版
│   └── renyi_entropy_memo.md          # IPR = e^{-H₂} の情報理論的基盤
│
└── connections/             # 他分野・概念との接続
    ├── memo_delta_vs_density.md    # δ vs 密度汎関数: 古典 vs 量子
    ├── 05_gedig_connection.md      # geDIG との接続
    └── liquid_lens_conjecture.md   # 可変焦点レンズへの応用（推測）
```

## 論文との対応

| Paper | 対象 | 主要メモ |
|-------|------|---------|
| Paper 1 | 光学応答 | `optics/`, `core/` |
| Paper 2 | 表面張力 | `surface_tension/`, `core/` |
| Paper 3 | 相の再定義 | `phase/`, `connections/` |
