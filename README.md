# sento-optics: 電子非局在化の有効指標による光学応答の現象論的統一記述

## Origin
2026年3月27日、銭湯にて「液体はなぜ光るのか？」という問いから出発。

## Core Thesis
物質の光学応答（透明・色・黒・光沢）の主要な傾向は、電子非局在化の**有効指標δ**と**有効伝導次元D_eff**の二変数で現象論的に統一整理できる可能性がある。

### 重要な位置づけ
- 本枠組みは「普遍理論」ではなく「**強い現象論的統一仮説**」
- δは厳密な物理量定義ではなく**操作的定義**（IPR, Wannier広がり等の候補群から最適なものを比較検証）
- D_effは結晶学的次元ではなく**低エネルギー光学応答に寄与する有効伝導次元**
- 第1近似としてδ×D_effを提案し、必要に応じ第2補正（極性/イオン性パラメータp等）を導入

## Status: 仮線（検証可能段階）
- 既存データとの矛盾なし（反証不能段階到達）
- 概念実証レベルのTBシミュレーション済（δ-Gap逆相関 r=-0.634確認）
- 先行研究で同一枠組みは未発見（2026年3月時点の検索結果）

## Repository Structure

```
sento-optics/
├── README.md                        # 本ファイル
├── theory/
│   ├── 01_core_framework.md         # 核心枠組み：δ×D_eff
│   ├── 02_glossiness_theory.md      # 光沢の現象論的再記述
│   ├── 04_falsification.md          # 反証条件
│   └── extensions/                  # 主論文スコープ外（別稿用）
│       ├── 03_phase_unification.md  # 相の連続的統一記述
│       └── 05_gedig_connection.md   # geDIGとの接続
├── data/
│   ├── carbon_allotropes.md         # 炭素同素体の光学データ集
│   └── supporting_evidence.md       # 補助的証拠（ガリウム、アンモニア等）
├── simulation/
│   ├── algorithm_spec.md            # シミュレーションアルゴリズム仕様
│   └── delocalization_optics_v2.py  # 概念実証コード
├── review/
│   └── reviewer_response.md         # レビュー指摘と対応
├── references/
│   └── bibliography.md
└── drafts/
    └── paper_skeleton.md            # 論文骨格（修正版）
```

## Scope（主論文）
**主戦場：炭素同素体 + h-BN対照系**
- ダイヤモンド、C60、SWCNT、グラフェン、グラファイト
- h-BN（同D_eff・低δの対照、第2補正として極性pの必要性を検討）
- ガリウム融解点反射率（補助的証拠として最小限）

**別稿に分離（extensions/）：**
- 相の連続的統一記述と液体再定義
- geDIG接続
- 超伝導・超流動への拡張
- 周期表再解釈

## Key Predictions (検証待ち)
1. 炭素同素体の光学特性がδ×D_effで系統的に整理できる
2. グラフェン積層数と吸収率の線形性がδ×D_eff枠組みと整合する
3. h-BNの白さが第1近似で「同D_eff・低δ」として説明可能
4. 同一δ×D_eff値の異なる物質が類似の光学応答カテゴリに分類される
