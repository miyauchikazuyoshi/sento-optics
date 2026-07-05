# sento-optics: 電子非局在化による界面物性の統一記述

> **「液体とは何か？」** — 2026年3月27日、銭湯にて。

## このリポジトリについて

これは研究プログラムの**思考の軌跡**です — 銭湯での観察から定量的物理学へ。

アイデアはシンプル: **構成粒子の空間的非局在化**（δ）が界面物性 — 光沢、表面張力、そして究極的には「液体とは何か」の定義 — を支配する。日常の直感をメモとして記録し、数値検証にかけ、生き残った主張を論文にする。

```
日常の疑問                    →  理論メモ                       →  数値検証              →  論文
「なぜ水面は光る？」          →  theory/optics/                →  simulation/optics/    →  Paper 1
「なぜ金属にγがある？」       →  theory/surface_tension/       →  simulation/surface_tension/ → Paper 2
「液体とは何か？」            →  theory/phase/                 →  （計画中）            →  Paper 3
```

## アイデア

湯船の水面を眺めていて:

1. **液体は光る。** 水面は金属鏡のように光をコヒーレントに反射する。
2. **液体は表面張力を持つ。** 水は重力に逆らって形を保つ。

どちらも*界面現象*であり、どちらも電子構造に根ざしたミクロな説明を欠いている。どちらも単一の変数に帰着できる:

**δ（非局在化指標）** — 構成粒子がどれだけ自由に空間に広がるか。

```
光学応答:    δ × D_eff → ε(ω) → R(ω)
表面張力:    δ → n_ws → γ
相の分類:    (δ_nuc, δ_elec) → 固体 / 液体 / 気体 / プラズマ / ...
```

より深い洞察: 量子力学は確率分布の**第2モーメント**（分散、広がり、不確定性）を基本的記述量として使う。第1モーメントが原理的に不確定だからだ。δ枠組みはこの戦略を古典系にも拡張する — 「粒子がどこにあるか」より「粒子がどれだけ広がっているか」が物性を決める場面では、δが自然な変数になる。

## 記号対応表

この枠組みは非局在化測度のファミリーを使う。最小限の道案内:

| 記号 | 意味 | 登場場所 | ステータス |
|------|------|---------|-----------|
| δ | 傘概念:「粒子がどれだけ広がるか」 | 全体 | フレームワークの中心概念 |
| δ_elec | 電子の非局在化 | Papers 1–3 | 中核提案。操作的プロキシ間で相互検証済み (r = 0.73–0.89) |
| δ_nuc | 核の非局在化 | Paper 3・融解 | coth 公式で量子↔古典を統一（理論）。検証は z_nuc の行 |
| z_nuc | 核の Resta 位相（= translational order parameter の再解釈） | 「固体/非固体」軸 | **古典MDで検証済み**（事前登録4判定PASS、融解を2桁シグナルで検出）。AIMD実証待ち |
| z_elec, λ² | 電子の Resta 位相／局在長（Kohn–Resta–SWM 系譜） | 「金属/絶縁体」軸 | 計算済み: 液体Na（金属的、\|z\| ~ 10⁻⁵⁷）vs NaCl結晶（λ² = 1.03 Å²、等方） |
| Ω, Ω_I | （ゲージ不変）Wannier spread | 光学 sum rule | C, Si, Ge, graphite, K で計算済み |
| IPR | 逆参加率 | 初期のプロキシ | Ω/λ² 路線に更新（同一構造内の区別に失敗するため） |
| D_eff | 有効伝導次元 | Paper 1 | 炭素系で検証済み。「λ が発散する方向の数」に等しいことを TB で数値実証 |
| s | 飽和度 2m_eE_gξ²/ℏ² | ML記述子マップ | C/Si/Ge で計算済み: ギャップ律速（Si 0.91）とコア遮蔽律速（Ge 0.16）を分離 |
| q300, f_ZP | 核の広がりのゼロ点比 | 同位体較正・フェーズ0マップ | 同位体シフトから較正済み（H₂ 54% > Ne 12% > H₂O ~5%）。1万材料マップ進行中 |

完全な定義: [`theory/core/glossary.md`](theory/core/glossary.md)

## 論文

数値検証を経て、自己批判テストに耐えた主張を論文にしている。

### Paper 1: バンドギャップを超える光学分類

> *Classifying Optical Appearance beyond the Band Gap: Effective Conduction Dimensionality and Electronic Delocalization in Carbon Allotropes*

**主張**: δ × D_effはバンドギャップ単独では不可能な光学分類（透明/有色/黒/光沢）を可能にする。グラファイトと金属はどちらもE_g ≈ 0だが、D_effが異なる（2 vs 3）。

| 結果 | 値 |
|------|-----|
| E_g + D_eff 決定木の正答率 | **6/7** (85.7%) |
| δプロキシ間の相互相関 | **r = 0.73–0.89** |
| δ–E_g 逆相関 | **r = −0.70**（文献）, **r = −0.86**（TB） |

ステータス: プレプリント v8。**DOI: [10.5281/zenodo.19425523](https://zenodo.org/records/19425523)**

- 理論: [`theory/optics/02_glossiness_theory.md`](theory/optics/02_glossiness_theory.md)
- コード: [`simulation/optics/`](simulation/optics/)
- 原稿: [`drafts/paper1_optics/main.tex`](drafts/paper1_optics/main.tex)

### Paper 2: Miedemaのn_wsはなぜ機能するか？

> *What Does Miedema's Boundary Electron Density Measure? Valence Electron Delocalization as the Physical Origin of n_ws*

**主張**: Miedemaのn_ws — 45年間使われてきた表面張力の経験的予測子 — は価電子非局在化δ_elecのプロキシである。これはWilliams, Gelatt & Moruzzi (PRL, 1980) が提起した問い「n_wsは*なぜ*γを予測できるのか？」への回答。

| 結果 | 値 |
|------|-----|
| δ_IPR（価電子）vs 中間点密度（15ダイマー） | **r = 0.89** (p < 0.001) |
| sp/d 間隙密度比（14金属スラブ） | **2.5倍** (p = 0.00008) |
| Wannier spread sp/d比（5金属） | **6–19倍** |

ステータス: プレプリント v8。**DOI: [10.5281/zenodo.19425541](https://zenodo.org/records/19425541)**

- 理論: [`theory/surface_tension/surface_tension_theory.md`](theory/surface_tension/surface_tension_theory.md)
- コード: [`simulation/surface_tension/`](simulation/surface_tension/)
- 原稿: [`drafts/paper2_surface_tension/main.tex`](drafts/paper2_surface_tension/main.tex)

### Paper 3: 物質の相記述子平面 — 液体とは何か？（計画中）

**仮説**（提案段階・数値検証中）: (δ_nuc, δ_elec) 平面 — 核の非局在化（「固体/非固体」軸、核Resta位相）× 電子の非局在化（「金属/絶縁体」軸、局在長）— が、固体・液体・気体・金属・絶縁体を一つの座標系で整理する。液体と気体を分けるのはδ_nuc（どちらも粒子は動く）ではなくδ_elec（電子の重なり → 凝集力 → 一定体積）。この*記述子平面*を液体の*定義*へ格上げできるかどうかこそが、数値プログラムの検証対象である。

ステータス: 枠組みと方法論はモデル系で検証済み（古典MD: 事前登録4判定PASS・融解検出、液体Na vs NaCl の電子側対照も計算済み）。液体本番の AIMD は進行中。

- 理論: [`theory/phase/paper3_phase_diagram_theory.md`](theory/phase/paper3_phase_diagram_theory.md)

## 思考の軌跡

`theory/` ディレクトリは思考過程を記録している — 日常の疑問がどのように既存の数学的構造に着地していくか。

### 基盤
- [`theory/core/01_core_framework.md`](theory/core/01_core_framework.md) — δ × D_effの定義と光学分類
- [`theory/core/04_falsification.md`](theory/core/04_falsification.md) — この枠組みを壊す条件（具体的・定量的）
- [`theory/core/glossary.md`](theory/core/glossary.md) — 全記号・用語の定義

### 主要な接続（アイデアが既存の物理に着地した場所）

| メモ | 何を接続しているか |
|------|-------------------|
| [`memo_quantum_classical_melting_crossover.md`](theory/connections/memo_quantum_classical_melting_crossover.md) | coth公式で量子/古典のδ_nucを統一; 拡散方程式がδ_nucの支配方程式; なぜ第2モーメントが正しい物理変数か |
| [`memo_liquid_definition_via_omega.md`](theory/connections/memo_liquid_definition_via_omega.md) | Wannier spread Ω + 拡散 → 液体のミクロ定義（先行研究なし） |
| [`memo_literature_and_sum_rule.md`](theory/connections/memo_literature_and_sum_rule.md) | Cardenas-Castillo (2024) 総和則でδ→光学が定理に（周波数積分量に対して） |
| [`memo_remsing_klein_liquid_si.md`](theory/connections/memo_remsing_klein_liquid_si.md) | Remsing & Klein (2020) 液体Si AIMD — 最近接の先行研究、4つのノベルティが残存 |
| [`renyi_entropy_memo.md`](theory/phase/renyi_entropy_memo.md) | IPR = e^{−H₂}（Rényiエントロピー）— δの情報理論的基盤 |
| [`05_gedig_connection.md`](theory/connections/05_gedig_connection.md) | 相転移とgeDIG認知フレームワークの構造的同型性 |
| [`memo_delta_vs_density.md`](theory/connections/memo_delta_vs_density.md) | δ（量子的:「何サイトに広がる？」）vs n(r)（古典的:「どこにある？」）— なぜギャップが存在したか |
| [`memo_periodic_table_and_refractive_index.md`](theory/connections/memo_periodic_table_and_refractive_index.md) | δ単独では屈折率を予測できない; 3因子補正 n²−1 ∝ δ × α / E_g² |

### その他の接続
- [`memo_classical_uncertainty_and_coherence.md`](theory/connections/memo_classical_uncertainty_and_coherence.md) — 古典的不確定性と量子的不確定性の類似
- [`memo_field_theories_and_entropy.md`](theory/connections/memo_field_theories_and_entropy.md) — 既存の5つの場の理論に対するδのメタ記述子としての位置づけ
- [`memo_mesoscale_quantum_classical.md`](theory/connections/memo_mesoscale_quantum_classical.md) — δをメソスケールの有効記述子として位置づける
- [`memo_dynamic_equilibrium_and_verification.md`](theory/connections/memo_dynamic_equilibrium_and_verification.md) — 1入力3出力の検証戦略
- [`liquid_lens_conjecture.md`](theory/connections/liquid_lens_conjecture.md) — 推測: 可変焦点レンズ設計へのδの応用

## 検証系

**主要検証系: 炭素同素体**（単一元素、構造のみが変数）

| 物質 | δ（πバンド幅） | D_eff | E_g (eV) | 光学応答 |
|------|----------------|-------|----------|---------|
| ダイヤモンド | —（sp³, πなし） | 0 | 5.47 | 透明 |
| C60固体 | 0.4–0.5 eV | 0 | 1.7–2.1 | 有色（暗紫） |
| SWCNT | 8–9 eV | 1 | 0–1.5 | カイラリティ依存 |
| グラフェン | ~9 eV | 2 | 0 | πα = 2.3%/層 |
| グラファイト | ~9 eV（面内） | 2 | ~0 | 黒 + 劈開面光沢 |

**対照系: h-BN**（グラファイトと同じsp²構造だが、δが低い → 透明/白色）

## リポジトリ構造

```
sento-optics/
├── theory/                             # 思考の軌跡
│   ├── core/                           #   基盤（論文横断）
│   ├── optics/                         #   Paper 1 理論
│   ├── surface_tension/                #   Paper 2 理論
│   ├── phase/                          #   Paper 3 理論
│   └── connections/                    #   他分野との接続
├── simulation/                         # 数値検証
│   ├── optics/                         #   TBモデル、決定木
│   └── surface_tension/                #   DFTスラブ、Wannier、自己テスト
├── data/                               # 文献データ、データセット
├── drafts/                             # 論文原稿（LaTeX）
│   ├── paper1_optics/
│   └── paper2_surface_tension/
├── zenodo/                             # プレプリント投稿メタデータ
└── review/                             # 文献調査、査読対応
```

## 理論の仕事の再定義

20世紀の理論のタスクは、原理から具体的な予測まで — *この化合物、この構造、この物性* — の全行程だった。その最後の区間は機械の仕事になりつつある。ユニバーサル機械学習ポテンシャルや生成モデルは、人間の理論家より速く広く物質空間を探索する。

残る — そして重要性を増す — のは、機械が供給できないものだ:

1. **変数の発明。** MLは与えられた表現の中を補間する。*どの量で世界を見るか*（d-band center、トポロジカル不変量、δ）を決めるのは今も理論の仕事。
2. **拘束の供給。** MLの予測は訓練分布の外で静かに壊れる。不等式や総和則（例: ξ² ≤ ℏ²/2m_eE_g）は外挿に耐える壁になる。
3. **問いの発明。** 「液体とは何か」はデータセットからは出てこない。
4. **理解。** 1万件の予測を一行 — *光沢とは局在長の発散である* — に圧縮することは、予測の副産物ではない。

この研究プログラムはこの分業の上に設計されている。ここでの理論の成果物は (δ_nuc, δ_elec) の*定義* — パラメータフリーで、自動化可能で、自己診断つき — であり、その先の物質空間の探索は機械の物量戦に渡す（[`drafts/strategy_ml_descriptor_2026-07-05.md`](drafts/strategy_ml_descriptor_2026-07-05.md)）。このリポジトリのワークフロー — 上流に人間の直感、下流にAIによる形式化と大量検証 — は、その未来の小規模なリハーサルでもある。

## AI利用開示

**著者の直感:** 「液体とは何か？」という問い、銭湯での観察（光沢＋表面張力が界面現象であること）、粒子の非局在化δがこれらを統一するという仮説 — ここまでは著者の着想による。

**AIによる形式化:** 直感を定量的枠組みに翻訳するプロセス — タイトバインディングシミュレーション、DFT計算、Wannier解析、統計的検証、自己批判テスト、論文執筆 — はClaude（Anthropic）およびChatGPT（OpenAI）との協働で実施した。著者はすべてのデータセット、コード、科学的主張を独自に検証している。科学的責任はすべて著者に帰する。

## 引用

> Miyauchi, K. (2026). *Phenomenological unification of optical response in carbon allotropes via electron delocalization index δ and effective conduction dimensionality D_eff.* Preprint. GitHub: [sento-optics](https://github.com/miyauchikazuyoshi/sento-optics)

## フィードバック歓迎

独立研究者による進行中の研究です。専門家によるレビュー、批判、鋭い指摘を積極的に求めています。論理の欠陥、見落とされた先行研究、より良い検証方法を見つけた方は、issueを立てるかご連絡ください。このリポジトリに自己批判テストが存在するのは、提案に値する仮説は破壊を試みる価値のある仮説だと考えるからです。

## ライセンス

本研究は学術的議論のために共有されています。本枠組みを参照する場合は適切に引用してください。
