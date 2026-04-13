# δの位置づけ: 既存理論・類似物理量・自己批判の統合マップ

**日付**: 2026-04-13（統合版）
**元メモ**: memo_sp_d_existing_theories.md, memo_delta_threats_and_limits.md, memo_knudsen_particle_continuum_duality.md, memo_cg_liquid_surface_tension.md, 新規サーベイ

---

## 1. δとは何か（一文定義）

既存の物理量（IPR / Wannier spread）を、光学応答・表面張力・相分類を横断する**統一的記述子**として再解釈したもの。新しい物理量の発明ではない。

---

## 2. 表面張力の既存理論とδの関係

| 既存理論 | 何がわかるか | 何が足りないか | δが加えるもの |
|---------|-----------|-------------|-------------|
| **ジェリウム** (Lang-Kohn 1970) | sp金属で表面エネルギー正しい | d金属で負の表面エネルギー | d電子の局在化（低δ）が均一ガス近似を破る理由を説明 |
| **Miedema** (1978) | n_wsで表面張力を±10-20%予測 | n_wsの物理的起源が不明 | δ_elecがn_wsの起源を部分的に説明 |
| **Williams-Gelatt-Moruzzi** (1980) | n_wsの物理的描像が"inappropriate" | 代替descriptorを提案せず | **45年間未回答の問いへの回答を試みる** |
| **Friedel** (1969) | d充填→凝集エネルギーの放物線 | 界面密度との接続なし | Ti(d²)>Fe(d⁶)>Cu(d¹⁰)の傾向とδが整合 |
| **d-band center** (Hammer-Nørskov 1995) | dバンド位置→触媒活性 | 表面張力と無関係 | d位置（どこにあるか）vs δ（どれだけ広がるか）= 相補的 |
| **DFTスラブ** (Vitos 1998等) | 各金属のγを±10%精度で計算 | どの電子的性質がγを駆動するか不明 | δが「価電子の均一性」を駆動変数として同定 |

---

## 3. 「粒子の自由度」を測る物理量の包括的比較

δと類似の概念を測る既存物理量を分野横断でサーベイした。

### 3.1 全量の比較表

| 量 | 領域 | 固液気区別 | 物質固有? | DB利用 | 何を測るか |
|---|---|:---:|:---:|:---:|---|
| **IPR** | 凝縮系 | ❌ | ❌ | 限定 | 波動関数の空間拡がり |
| **ELF** | 量子化学 | ❌ | ✅ | 部分的 | 電子対の局在度 |
| **DI** | 量子化学 | ❌ | ✅ | 限定 | 原子間電子共有 |
| **Wannier Spread Ω** | 凝縮系 | ❌ | ✅ | 限定 | 電子軌道の空間拡がり |
| **Drude Weight** | 凝縮系 | 金属/絶縁体 | ❌ | 部分的 | キャリア非局在化 |
| **Penn Gap** | 凝縮系 | 金属/絶縁体 | ✅ | ✅(JARVIS) | 集団的電子応答 |
| **Steinhardt Q₆** | 統計力学 | 固液✅ | ❌ | ✅(pyscal) | 結合配向秩序 |
| **Lindemann δ_L** | 統計力学 | 固液✅ | ❌ | 部分的 | 原子変位の自由度 |
| **S₂ (excess entropy)** | 統計力学 | 連続✅ | ❌ | 限定 | 構造情報量 |
| **S_conf** | ガラス | 液体/ガラス | ❌ | 限定 | 配位空間の探索度 |
| **Shannon / Rényi entropy** | 情報理論 | ❌ | ❌ | ❌ | 分布の拡がり |
| **Multifractal D_q** | 情報理論 | ❌ | ❌ | ❌ | Fractal的占有度 |
| **tan δ (loss tangent)** | レオロジー | 固液✅ | ❌ | ✅ | 粘弾性バランス |
| **Deborah De** | レオロジー | 概念的✅ | ❌ | ❌ | 時間スケール依存流動性 |
| **f_q (non-ergodicity)** | ガラス/MCT | 液体/ガラス | ❌ | 限定 | エルゴード性 |
| **MSD** | ソフトマター | 固液気✅ | ❌ | ✅(MD) | 粒子拡散自由度 |
| **Frenkel τ** | 超臨界 | 液体的/気体的 | ❌ | 限定 | 緩和時間 |
| **Kn (Knudsen)** | 流体力学 | ❌(固液不可) | ❌ | ❌ | 衝突までの距離 |

### 3.2 三つの要件とギャップ

以下の三要件を**同時に**満たす確立された物理量は存在しない:

1. **一粒子の確率分布**から計算される情報理論的変数
2. **固体・液体・気体を連続的に**パラメトライズする
3. **物質固有**（外的条件に依存しない内的性質）

パターン:
- 「相を区別できる」量（Q₆, Lindemann, tan δ, MSD）→ **物質固有でない**
- 「物質固有」の量（ELF, Wannier, Penn Gap, DI）→ **相を区別できない**
- 「情報理論的」な量（Shannon, Rényi, IPR）→ **電子にしか適用されてない**

### 3.3 δが埋める空白

- IPR/Rényiを**原子位置分布に適用**（要件1）
- MSD/a²でδ_nucとし全相を連続パラメトリゼーション（要件2）
- δ_elec（Wannier spread）は電子構造から決定（要件3: 物質固有）

**空白は「情報理論的量を原子位置に適用する」という一歩。道具は全部あった。組み合わせ方が新しい。**

---

## 4. 最も近い先行研究5件との差分

| 先行研究 | 何を先取り | δとの差分 |
|---------|----------|---------|
| **Rosenfeld S₂** (1977) | 液体の単一パラメータ記述 | S₂は対相関（集団的）。δは一粒子。「どう動くか」vs「なぜ液体か」|
| **Zaanen gauge duality** (2004) | 固液の理論的接続 | 転位凝縮。確率的変数なし。測定不能。2+1次元限定 |
| **Lindemann √⟨u²⟩/a** (1910) | δ_nucの概念的先祖 | 融解点の閾値のみ。情報理論的定式化なし |
| **Trachenko τ** (2016) | 液体の単一パラメータ | 時間領域。δは空間領域。**相補的**（競合ではない）|
| **PIMD ring polymer** | 量子的位置の広がり | リングポリマーのIPR計算は前例なし |

---

## 5. Kn vs δ: 古典的自由度 vs 確率論的自由度

| | クヌーセン数 Kn | 非局在化度 δ |
|---|---|---|
| **定義** | λ(平均自由行程) / L(系サイズ) | 1/(N·IPR) or MSD/a² |
| **前提** | 粒子は点 | 粒子は確率分布 |
| **固体と液体** | 区別不可（どちらもKn << 1） | 区別可能（δ_nucの値域で分離）|
| **物質固有？** | **No**（系サイズLに依存） | **Yes** |
| **materials informatics** | descriptorとして不使用 | descriptorになりうる |

Knが材料探索に使えないのは「外的条件（L）に依存するプロセス変数」だから。
δは「内的電子構造・核運動で決まる物質固有の量」だから、材料descriptorになれる。

---

## 6. 脅威と限界の自己批判

### 6.1 脅威一覧

| 脅威 | 種類 | δの有効性への影響 |
|------|------|----------------|
| 先行研究の重複（IPRは既知） | **新規性の主張**の問題 | 有効性には無関係 |
| Anderson vs Mott転移 | メカニズム区別の限界 | δの値は両方で有効 |
| 一次相転移でのδ不連続 | 連続性の仮定の限界 | ジャンプするだけ |
| Ga異常（融解で導電率上昇） | 当初脅威に見えた | **スラブデータで説明できた** |
| 不均一構造（fluctuons） | 空間平均の限界 | ∇δで拡張可能 |
| 超臨界相の曖昧さ | 定義の問題 | Frenkel線と整合 |

### 6.2 脅威の再評価

**δの有効性を否定する脅威は1つもない。** 全て「新規性の主張の仕方」か「使い方の注意」に関するもの。

### 6.3 正しい主張の仕方

> ❌ 「我々はδという新しい物理量を発見した」
>
> ✅ 「既存の物理量（IPR / Wannier spread）を、光学・表面張力・相分類を横断する統一的記述子として再解釈する。数値解析により、14金属のスラブ計算（p = 0.00008）および炭素同素体の光学分類で支持されることを示す。」

### 6.4 δの強み

1. **数学的に自然**: IPR = Rényi-2エントロピーの指数関数
2. **測定可能**: Wannier spread（DFT）、Debye-Waller因子（X線回折）、拡散係数（実験）
3. **射程が広い**: 光学・表面張力・相分類を一つの変数で接続

### 6.5 δの弱み

- 定量検証がまだ少ない（炭素同素体 + Al/Znの2系）
- Rosenfeldは数百の系で40年以上検証済み
- δからγの定量予測はできない（質的記述子）

---

## 7. CGシミュレーションとの接続

CGの液体表面張力処理は、δ_nucとδ_elecを**無意識に分離処理**している:

| CGの処理 | δの言語 |
|----------|---------|
| γ = 定数（ユーザー入力） | δ_elec由来の凝集力を外部入力 |
| 粒子が動ける | δ_nuc > 0 が暗黙の前提 |
| 表面修復 | δ_nucが適切な値 → 拡散で穴を埋める |
| Level Set φ=0面 | δ_nucの空間勾配が急な等値面 |

CGのヒューリスティックが物理と一致するのは、人間の視覚的直感が物理法則の表出を捉えているから。

---

## 8. 量子-古典接続の最先端研究との関係（2026-04-13追記）

δが「量子っぽい」のはなぜか。そして最先端研究のどこに着地しうるか。

### 8.1 最重要接続: von Weizsäcker ≡ Fisher information ≡ quantum potential ≡ 表面張力

以下の4つの量は**数学的に同一の構造**を持つ:

```
Q (quantum potential)        = -(ℏ²/2m)(∇²√ρ)/√ρ       [Madelung 1926, Bohm 1952]
T_W (von Weizsäcker KE)      = (ℏ²/8m) ∫ |∇ρ|²/ρ dr    [von Weizsäcker 1935]
I_F (Fisher information)     ∝ T_W                       [Nagy 2022, 2025]
γ (DFT surface tension)      ∝ gradient expansion 第1項 ∝ T_W  [PRB 28, 4374, 1983]
```

全て「密度勾配の鋭さ」を測っている。δ_IPR（密度分布の均一性）はこの勾配構造の逆数的な量。

**この接続の意味**: 表面張力のDFT計算で使われるgradient項が、量子力学のquantum potentialと同じ数学だという事実は、「表面張力が量子力学的な電子の非局在化から生じる」というδ枠組みの主張に**数学的基盤**を与える。

**先行状況**: 各等号は個別に既知（Nagy 2022がFisher-DFT接続を証明）。しかし「IPR/δ → Fisher information → 表面張力」の因果連鎖を明示的に述べた論文は**調査した限り存在しない**。

**引用**: Nagy, Int. J. Quantum Chem. (2022); J. Comput. Chem. (2025)

### 8.2 Quantum Chaos: IPRの出自と古典系への拡張

IPRの本来の文脈はAnderson localization（Wegner 1980, Evers & Mirlin RMP 2008）。波動関数がHilbert空間上でどれだけ広がるかを測る。

**δとの関係**: δ_IPRはこの道具を「波動関数」ではなく「原子位置の確率分布」に適用する。Hilbert空間上の広がり → 実空間上の広がり。道具は同じ、適用対象が新しい。

**注意点**: IPRをHilbert空間外（古典的確率分布）に適用する場合、物理的正当化が必要。正当化の根拠は: (1) IPR = exp(-H₂) はRényi-2 entropyの指数関数であり、**任意の確率分布**に定義可能、(2) ガラス物理学ではphononの振動モードのIPRが標準的に使われている（ただし固有ベクトルのIPR）。

**完全に新規な一歩**: 原子位置分布そのもの（固有状態ではなく、実空間確率分布）にIPRを適用して相を分類する — これは先行例がほぼない。

**引用**: Evers & Mirlin, Rev. Mod. Phys. 80, 1355 (2008); Wegner, Z. Physik B 36, 209 (1980)

### 8.3 Classical Entanglement: 非分離性の古典版

Konrad & Forbes (2024) がquantum entanglementとclassical non-separabilityの**操作的区別**を初めて明確化:
- Quantum: 複数測定の統計的相関（realism破れ）
- Classical: 単一測定の条件付き結果（realism保存）
- 数学的non-separabilityは共通

**δとの関係**: 液体中の(δ_nuc, δ_elec)は、核自由度と電子自由度の間のnon-separabilityを記述していると解釈可能。電子の広がり方が核の配置に依存し、核の運動が電子構造に影響する — Born-Oppenheimer近似が破れる極限ではこれが顕在化する。

**ただし**: この接続は**投機的**。entanglement witnessを古典統計力学に体系的に適用した研究は存在しない。論文に書くなら「future direction」としてのみ。

**引用**: Konrad & Forbes, Phil. Trans. R. Soc. A 382, 20230342 (2024)

### 8.4 Pilot Wave Hydrodynamics (Bush/Couder)

MITのBushグループがbouncing droplet実験で量子アナログを再現（回折、干渉、Anderson localization等）。

**δとの関係**: pilot wave系では、液滴（粒子）と表面波（連続場）が結合して量子的振る舞いを生む。これは「粒子-連続体のクロスオーバー」の実験的デモンストレーション。δが中間値をとる液体でこのクロスオーバーが起きる、というδ枠組みの主張と**概念的に整合**。

**ただし**: pilot wave系は1粒子の量子力学アナログであり、多体系（液体）への拡張は行われていない。

**引用**: Bush, Frumkin, Saenz, Appl. Phys. Lett. 125, 030503 (2024)

### 8.5 Nelson Stochastic Mechanics: 古典拡散からSchrödinger方程式

Nelson (1966) は拡散係数 ℏ/(2m) のBrownian motionからSchrödinger方程式を導出した。Born ruleが独立公理ではなく、確率過程の分布として内包される。

**δ_nucとの直接接続**: δ_nuc = MSD/a² は拡散方程式が支配方程式。Nelsonの枠組みでは、拡散方程式が量子力学の基盤。つまりδ_nucの支配方程式と量子力学の支配方程式が**同一の数学的構造**を持つ。

この接続は「液体のδ_nucが量子っぽい」という直感に**最も直接的な数学的根拠**を与える。液体中の原子拡散（古典的）と量子力学の確率振幅の拡散（量子的）が同じ方程式で記述される。

**ただし**: Nelsonの理論自体が物理学コミュニティでは議論が分かれる（解釈問題）。引用する場合は慎重に。

### 8.6 Trachenkoの液体理論: k-gap と部分的局在化

Trachenko (Cambridge UP, 2023) はFrenkel緩和時間τで液体を記述。液体のtransverse phononはある波数以上でのみ伝播（k-gap）。

**δとの関係**: k-gapは「液体のcollective modeが部分的にlocalizeする」ことを意味する。IPRはまさにこの部分的局在化を定量する道具。k-gap（周波数/波数領域）とδ（実空間）の橋渡しが可能かもしれない。

**Trachenkoのτとδの関係**: τ（時間的）とδ（空間的）は独立な情報を持つ。τ × δ の結合変数がありうる。**AIMDデータで検証可能**。

### 8.7 最先端との距離マップ

| 最先端研究 | δとの距離 | 接続の強さ | 論文に書けるか |
|-----------|----------|----------|-------------|
| **von Weizsäcker ≡ Fisher ≡ γ gradient** | 数学的に直接 | ★★★★★ | Discussion: 数式レベルで引用可能 |
| **Quantum chaos IPR** | 道具が同一 | ★★★★ | Methods: IPRの出自として引用 |
| **Nelson stochastic mechanics** | 支配方程式が同一 | ★★★★ | Discussion: 拡散方程式の二重の意味 |
| **Trachenko k-gap** | 相補的 | ★★★ | Discussion: τ vs δ の比較 |
| **Pilot wave (Bush)** | 概念的アナログ | ★★ | Introduction: 動機づけとして |
| **Classical entanglement** | 投機的 | ★ | Future work としてのみ |
| **ML softness** | 相補的（data-driven vs first-principles）| ★★ | Related work として |

### 8.8 「δが量子っぽい」の精密な意味

「量子っぽい」は以下の3つの意味で正当化できる:

1. **数学的**: IPR = exp(-H₂) はRényi entropy。情報理論的量は量子/古典の区別なく定義可能
2. **構造的**: δ_nucの支配方程式（拡散方程式）がSchrödinger方程式と同じ数学（Nelson 1966）
3. **物理的**: 表面張力のgradient項がquantum potentialと同一構造（von Weizsäcker ≡ Fisher）

「量子っぽい」のではなく、**量子力学と古典液体が同じ数学的構造を共有している**。δはその共有構造を顕在化させる変数。

**注意**: 「古典液体が量子力学的に振る舞う」とは主張していない。「同じ数学が両方に現れ、δがその数学を測る」と主張している。この区別は論文で明確にすべき。

---

## 9. Paper 2.1 Discussionへの反映案

> "Unlike the Knudsen number, which depends on the extrinsic system
> size L, δ is determined by intrinsic electronic structure and nuclear
> dynamics, making it suitable as a materials descriptor. Among existing
> measures of particle freedom (Table X), none simultaneously satisfies
> three requirements: (1) information-theoretic computation from
> single-particle distributions, (2) continuous parameterization across
> all phases, and (3) material-intrinsic character. The (δ_nuc, δ_elec)
> pair proposed here fills this gap."

---

## 9. 元メモへの参照

この統合マップは以下のメモから構成した。各メモは思考の軌跡として保持する。

| メモ | 主な内容 | 作成日 |
|------|---------|--------|
| `memo_sp_d_existing_theories.md` | 表面張力理論7件との比較 + 14金属データ | 2026-04-04 |
| `memo_delta_threats_and_limits.md` | 6つの脅威の自己批判 | 2026-04-05 |
| `memo_knudsen_particle_continuum_duality.md` | Kn vs δ、粒子-連続体クロスオーバー | 2026-04-13 |
| `memo_cg_liquid_surface_tension.md` | CG液体シミュレーションとδの対応 | 2026-04-12 |
| `memo_literature_and_sum_rule.md` | Cardenas-Castillo総和則、先行文献 | (earlier) |
| `memo_remsing_klein_liquid_si.md` | Remsing & Klein液体SiのMLWF | (earlier) |

---

*統合版 2026-04-13。個別メモの思考の軌跡を1枚のマップに集約。*
*2026-04-13 追記: セクション8（量子-古典接続の最先端研究）を追加。*
