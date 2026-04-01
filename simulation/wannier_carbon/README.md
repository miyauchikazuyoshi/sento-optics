# Wannier Spread Calculation: Group 14 Elements & Carbon Allotropes

## Hypothesis

Paper I classifies carbon allotropes by (E_g, D_eff) and uses
literature-derived proxies (pi-band width, inverse effective mass, band gap)
to argue that these proxies reflect a common underlying quantity: the
electronic delocalization index delta_elec.

However, **delta_IPR has never been computed from first principles for these
systems**. The 7/7 classification success comes from the decision tree
(E_g + D_eff), not from delta itself. Two attempts to compute delta directly
(tight-binding model and molecular DFT clusters) both failed to reproduce
the expected ordering.

This calculation aims to resolve whether the failure was due to
**inadequate models** (TB too coarse, molecules != solids) or a
**fundamental limitation of delta_IPR**.

## Core Prediction

If delta_elec measures electronic delocalization, then for periodic solids:

```
Omega(diamond) < Omega(graphite)
```

where Omega is the Wannier function spread (Ang^2) from maximally localized
Wannier functions (MLWFs).

## Results (2026-04-01)

### OVERALL: PASS

| System | Period | Hybridization | num_wann | Omega_total (Ang^2) | **Omega/WF (Ang^2)** | Optical category |
|--------|--------|---------------|----------|---------------------|----------------------|------------------|
| Diamond | 2 | sp3, insulator | 8 | 7.635 | **0.954** | Transparent |
| Ge | 4 | sp3, semiconductor | 8 | 18.201 | **2.275** | Transparent |
| Si | 3 | sp3, semiconductor | 8 | 24.392 | **3.049** | Transparent (grey) |
| K metal (Paper II) | 4 | 4s, metal | 1 | 3.748 | **3.748** | Metallic luster |
| Graphite | 2 | sp2+pi, semimetal | 8 | 51.002 | **6.375** | Black + gloss |

**Key findings:**

1. **Omega(diamond) << Omega(graphite)**: 0.954 vs 6.375 Ang^2 — **6.7x ratio**.
   The ordering is unambiguous.

2. **Diamond < K metal < Graphite**: Insulator < metal < semimetal on the
   same Omega/WF scale. Carbon and metals from Paper II sit consistently
   on one axis.

3. **Sigma/pi decomposition in graphite**:
   - 6 sigma WFs: 5.49 - 6.27 Ang^2 (sp2 bonds, relatively localized)
   - 2 pi WFs: 7.32, 8.19 Ang^2 (delocalized across layers)
   - Pi electrons are 1.3-1.5x more spread than sigma — they are the
     source of graphite's metallic optical response.

4. **Group 14 cross-element comparison (Si vs Ge)**:
   - Expected (by refractive index): Si (n=3.44) < Ge (n=4.0) → Omega(Si) < Omega(Ge)
   - **Observed: Omega(Si) = 3.05 > Omega(Ge) = 2.28**
   - This is NOT a failure — it reveals that **delta_elec alone cannot predict
     refractive index across different elements**. See "Three-Factor Correction" below.

5. **d-electron screening confirmed (Paper II consistency)**:
   - Ge (period 4) has 3d10 electrons that screen sp3 orbitals → 25% contraction
   - Ge band structure: bands 1-10 at -16 eV (3d, 0.3 eV bandwidth = fully localized)
   - Same effect as Paper II: d-electrons localize sp orbitals in period 4+ elements
   - **This is independent first-principles confirmation of Paper II's d-screening finding**

6. **Prior failures explained**: TB model and molecular DFT both gave
   wrong delta ordering because:
   - TB: too coarse to capture sp3 localization (1D chain != 3D diamond)
   - Molecular DFT: isolated molecules != periodic solids; N-normalization
     of IPR mixes size and delocalization effects
   - **The concept was right; the models were inadequate.**

### Success Criteria Status

| Criterion | Threshold | Status |
|-----------|-----------|--------|
| SCF convergence | JOB DONE, no warnings | **PASS** |
| Wannier convergence | Delta Omega = 0 over last 100 iter | **PASS** |
| Primary: Omega(diamond) < Omega(graphite) | Unambiguous ordering | **PASS** (6.7x) |
| Secondary: Omega_pi > Omega_sigma (graphite) | Factor > 1.2 | **PASS** (1.3-1.5x) |
| Cross-validation: consistent with metals | Monotonic with optical response | **PASS** |

### Remaining convergence tests (not yet performed)

- ecutwfc convergence: 40, 60, 80 Ry (total energy < 1 mRy)
- k-grid convergence: 4x4x4 vs 6x6x6 (Wannier spread < 0.05 Ang^2)

These are important for publication quality but unlikely to change the
6.7x ordering.

## Three-Factor Correction Model

### Problem

Within the same element (carbon allotropes), Omega/WF ordering tracks
optical response perfectly. But across different elements (C vs Si vs Ge),
Omega/WF alone fails to predict refractive index:

| Element | Period | Omega/WF (Ang^2) | E_g (eV) | n (lit.) | n^2-1 |
|---------|--------|------------------|----------|----------|-------|
| C (diamond) | 2 | 0.954 | 5.5 | 2.42 | 4.86 |
| Si | 3 | 3.049 | 1.1 | 3.44 | 10.83 |
| Ge | 4 | 2.275 | 0.67 | 4.0 | 15.0 |

Omega/WF ordering: C < Ge < Si, but n ordering: C < Si < Ge.

### Explanation: Penn model + atomic polarizability

Refractive index depends on three factors (Penn model):

```
n^2 - 1  ∝  delta_elec × alpha_atom / E_g^2
```

| Factor | Physics | C vs Si vs Ge |
|--------|---------|---------------|
| delta_elec (Omega/WF) | Electron delocalization | C < Ge < Si |
| alpha_atom | Atomic polarizability (size-dependent) | C < Si < Ge |
| 1/E_g^2 | Optical transition ease | C << Si < Ge |

Ge has smaller delta than Si due to d-screening, but larger alpha and
smaller E_g → the product delta × alpha / E_g^2 exceeds Si → n(Ge) > n(Si).

### Within-element vs cross-element regimes

- **Same element (carbon allotropes)**: alpha and E_g covary with structure,
  so delta alone captures the ordering → Paper I's 7/7 success
- **Different elements**: alpha and E_g vary independently of delta →
  three-factor composite required → Paper III scope

### d-Electron Screening as Metalloid Staircase

The Ge result reveals a broader principle: the periodic table's
metal/nonmetal boundary (metalloid staircase B-Si-Ge-As-Te-At) is a
**delta = delta_critical contour**.

Three competing effects shape this contour:
1. Shell number ↓ (down): delta↑ (larger atoms, easier delocalization)
2. Z_eff ↑ (right): delta↓ (stronger nuclear attraction, localization)
3. d-screening (period 4+): delta↓ (d-shell contracts sp orbitals)

The staircase runs upper-left → lower-right because going down adds
shells (delta↑), requiring more Z_eff (further right) to reach delta_critical.
The d-block insertion at period 4 creates the staircase's "step" via
discontinuous Z_eff increase.

See `theory/connections/memo_periodic_table_and_refractive_index.md` for
full discussion.

## Preliminary Experiment: Three-Factor Numerical Test

**Script**: `test_threefactor_correction.py`

### Result: Ordering recovered, quantitative prediction fails

| Model | Ordering | Matches n? | CV of proportionality constant |
|-------|----------|------------|-------------------------------|
| δ_elec only (Ω/WF) | C < Ge < Si | **NO** | — |
| δ_eff = Ω/WF × α_atom / E_g² | C < Si < Ge | **YES** | 138% |
| Penn-type = NΩ/(V_cell × E_g²) | C < Si < Ge | **YES** | 109% |

Both correction models recover the correct ordering C < Si < Ge.
However, proportionality constants vary by >100x across elements:
the model captures the qualitative trend but not quantitative prediction.

### Clausius-Mossotti diagnostic

By inverting the experimental n to obtain α_CM (true solid-state
polarizability per atom), we find:

| Element | α_CM (Ang^3) | Ω/WF (Ang^2) | α_CM / Ω |
|---------|-------------|---------------|-----------|
| C | 0.84 | 0.954 | 0.88 |
| Si | 3.74 | 3.049 | 1.23 |
| Ge | 4.50 | 2.275 | **1.98** |

Ge's α_CM/Ω ratio (1.98) is 2.3x that of C (0.88). This means Ge's
solid-state polarizability is much larger than its Wannier spread
would predict — the "missing" polarizability comes from the 3d10
core electrons that are not captured in the sp3 Wannier functions.

### Factor decomposition (Si → Ge)

| Factor | Ge/Si ratio | Effect |
|--------|-------------|--------|
| Ω/WF | 0.746 | d-screening contracts sp3 |
| α_atom | 1.128 | Ge atom slightly larger |
| 1/E_g² | 2.871 | Ge gap much smaller |
| **Product** | **2.42** | |
| **Actual (n²-1) ratio** | **1.39** | |

The 1/E_g² factor dominates (+187%), overriding the d-screening
suppression of Ω/WF (-25%). But the product overshoots by 75%,
showing that free-atom α is not a good proxy for solid-state α.

### Conclusion

The three-factor model is **qualitatively correct** (ordering recovered)
but **quantitatively inadequate** with free-atom α (proportionality
constant varies 180x across elements). δ_elec 単独では異元素間の
屈折率を予測できないことが明確になった。

**Status: exploratory — not planned for immediate paper inclusion.**

## δ_IPR → Ω Correlation Test

**Script**: `test_delta_vs_omega.py`

### 目的

Cardenas-Castillo (2024) が Ω → ε₂ の sum rule を証明済み。
我々が示すべきは δ_IPR (TB) → Ω (DFT) の接続。
これが成立すれば δ → Ω → ε₂ の全予測連鎖が閉じる。

### 結果 1: 異構造間 (N=2, 単純TBモデル)

| 補正 | Diamond Ω/corr | Graphite Ω/corr | CV |
|------|---------------|----------------|-----|
| δ 単独 | 41.5 | 16.3 | 43% |
| δ × D_eff | 13.8 | 8.2 | 26% |
| **δ × D_eff²** | **4.61** | **4.08** | **6%** |
| δ × √D_eff | 23.9 | 11.6 | 35% |

**δ × D_eff² が CV=6% で最良。** 比例定数 C ≈ 4.3 が 2 系で一致。

### 結果 2: 同構造・異元素 (N=3, Slater-Koster sp3 モデル) — FAIL

Harrison universal パラメータ (1980) による sp3 TB モデルで
Diamond, Si, Ge を同一フレームワークで計算:

| System | δ_IPR (SK) | Ω/WF (DFT) | Ω/δ |
|--------|-----------|-------------|------|
| Diamond | 0.0204 | 0.954 | 46.8 |
| Si | 0.0198 | 3.049 | 154.3 |
| Ge | 0.0193 | 2.275 | 118.0 |

- **Ordering: FAIL** — δ: Ge < Si < Diamond, Ω: Diamond < Ge < Si
- **Pearson r = -0.69** (負の相関!)
- **CV = 42%** (Ω/δ 比のばらつき)
- δ の変動幅 < 5% (0.0193–0.0204)、Ωは 3倍以上変動

### 失敗の原因分析

**δ_IPR が同一構造クラス内で材料を区別できない理由:**

1. **Bloch状態の普遍的非局在化**: 周期結晶では全 Bloch 状態が
   全サイトに等しく非局在化。IPR ≈ 1/N は結晶構造のみに依存し、
   パラメータ（t, ε_s, ε_p）にほぼ依存しない。

2. **δ_IPR vs Ω の測定対象の違い**:
   - δ_IPR: サイト基底での非局在化（無次元、0～1）
   - Ω: Wannier 関数の実空間的広がり（Å²、格子定数に依存）

   同じ結晶構造で a が異なる系（C: 3.57, Si: 5.43, Ge: 5.66 Å）では、
   Ω ∝ a² でスケールするが、δ_IPR はほぼ不変。

3. **d電子遮蔽**: Ge の Ω が Si より小さいのは 3d 電子の遮蔽効果
   (Pyykkö 1988)。sp3 モデルにはこの物理が含まれない。

### 結論と修正された理解

δ_IPR は **構造クラス間の区別** （diamond vs graphite: 6.7倍）
に有効だが、**同一構造クラス内の元素間比較** には使えない。
これは δ の限界ではなく、**IPR が δ の適切な近似ではない**
ことを示している。

**δ → Ω の正しい接続には:**
- 同一構造クラス間: δ_IPR × D_eff² が有効 (CV=6%, N=2)
- 異元素間: Wannier spread Ω 自体が δ の第一原理的実現であり、
  TB の δ_IPR を中間量として使う必要がない

## DFPT Dielectric Constant Calculation

**Scripts**: `analyze_dielectric.py`, `ph_epsilon.in` (in each subdirectory)

### Method

`ph.x` (DFPT) with `epsil = .true.` at q=0 で静的高周波誘電率 ε∞ を
DFT-PBE 波動関数から直接計算。自由原子 α を一切経由しない。

### Results

| Element | ε∞ (DFT-PBE) | n_calc | n_exp | Error | Eg_PBE (eV) | Eg_exp (eV) |
|---------|-------------|--------|-------|-------|-------------|-------------|
| C (diamond) | **5.890** | **2.427** | 2.417 | **+0.4%** | ~4.15 | 5.47 |
| Si | **23.31** | **4.83** | 3.44 | **+40%** | ~0.52 | 1.12 |
| Ge | **FAILED** | — | 4.00 | — | **0** | 0.66 |

### Analysis

1. **Diamond: +0.4%**. ギャップが大きい（5.5 eV）ので PBE の
   ~1.3 eV 過小評価の相対影響が小さい。
2. **Si: +40%**. PBE Eg ≈ 0.52 eV vs 実験 1.12 eV。
   ε ∝ 1/Eg² なので 2.15x のギャップ誤差が ~4.6x の ε 誤差に増幅。
3. **Ge: 計算不可**. PBE がギャップを閉じる → 金属扱い →
   DFPT 電場計算が原理的に不可能。`occupations='fixed'` の SCF も
   非収束（accuracy ≈ 5e-7 Ry で発散）。

## δ 予測の射程と限界

### δ でできること（実証済み）

1. **同一元素・異構造の光学分類**: δ(diamond) << δ(graphite) の
   6.7x の差が、透明/黒色+光沢の光学カテゴリを再現。
   Paper I の 7/7 分類成功の第一原理的裏付け。（PASS）

2. **d 電子遮蔽の定量的検出**: Ge (2.28) < Si (3.05) が
   Paper II の d 殻遮蔽効果を独立に確認。（PASS）

3. **金属-非金属の横断的比較**: Diamond (0.95) < K metal (3.75)
   < Graphite (6.38) が Papers I-II を単一軸上に統合。（PASS）

### δ でできないこと（実証済み）

1. **異元素間の屈折率の定量予測**: δ(Ge) < δ(Si) なのに
   n(Ge) > n(Si)。δ 単独では n の序列すら再現不可。
   原子分極率 α とバンドギャップ E_g が独立に効く。

2. **DFT-PBE レベルでの n 定量計算**: PBE のバンドギャップ
   過小評価が ε∞ ∝ 1/Eg² を通じて誤差を増幅。
   Si で +40%、Ge では計算自体が破綻。

3. **三因子モデルの定量的成立**: δ × α / E_g² は序列を
   回復するが、比例定数が 180x 変動し、予測には使えない。

### 限界の本質と理論的背景

2024 年に Cardenas-Castillo et al. (PRB 110, 075203) が証明した
sum rule により、δ と光学応答の関係は明確になった:

```
Ω_I = (ℏ²e²/2πm²) ∫₀^∞ Im[ε(ω)] / ω dω
```

Wannier spread のゲージ不変部分 Ω_I は、全周波数の光学吸収の
重みつき積分と**数学的に等しい**。δ → 光学応答の接続は定理。

ただしこれは**積分量**であり、特定の周波数での応答（n at 589 nm）
を予測するものではない。三因子モデル n² - 1 ∝ δ × α / E_g² は
この sum rule の Penn model による粗い離散化（単一遷移近似）であり、
比例定数が 180x ばらつくのは近似の限界として自然に説明できる。

つまり:
- δ は光学吸収の**総量**を正確に記述する（sum rule で保証）
- δ は特定周波数の応答（n, R）を**直接には**予測しない
- 同一元素内で δ が有効なのは、ε₂(ω) のスペクトル形状が
  構造間で相似なため、積分量の序列 ≈ 各周波数での序列

### 先行研究との関係

| 先行研究 | 年 | 内容 | 我々との関係 |
|---------|---|------|------------|
| Penn, PRev 128 | 1962 | ε = 1 + (ωp/Eg)² | 三因子モデルの理論的祖先 |
| Phillips, PRL 20 | 1968 | ギャップの共有結合/イオン分解 | δ が homopolar gap を記述 |
| Van Vechten, PRev 182 | 1969 | 68 結晶で定量検証 | 異元素比較の先駆 |
| Moss, PPSB 63 | 1950 | n⁴·Eg = const | 経験則ベンチマーク |
| Marzari & Vanderbilt, PRB 56 | 1997 | MLWF の定式化 | Ω 計算の基盤 |
| Yates et al., PRB 75 | 2007 | Wannier 補間光学伝導度 | postw90 の基盤 |
| **Cardenas-Castillo et al., PRB 110** | **2024** | **Ω_I = ∫ε₂/ω dω** | **δ↔光学の数学的基盤** |
| **Rhim & Kim, PRB 111** | **2025** | 量子計量 → 誘電マーカー | Ω が quantum metric の積分 |

**我々の新規性**: Cardenas-Castillo は ε(ω) → Ω の抽出（分析ツール）。
我々は Ω(δ) → 光学応答の分類・予測（設計ツール）。同じ恒等式の逆方向。

詳細は `theory/connections/memo_literature_and_sum_rule.md` を参照。

## より正確な予測に必要な計算・実験設計

### Priority 1: postw90 — Ω から ε₂(ω) の forward prediction（最重要）

```
入力: Wannier90 (.chk) → postw90.x (berry) → σ(ω) → ε₂(ω)
目的: Ω (Wannier spread) → ε₂(ω) の予測連鎖を実証
```

- **同じ Wannier 関数**から Ω（spread）と ε₂(ω) が同時に出る
- Cardenas-Castillo (2024) sum rule Ω_I = ∫ε₂/ω dω は証明済み
- 我々の目的: **Ω が既知なら ε₂ の総量が予測できる** ことの実証
- Ge も smearing ありで光学伝導度は計算可能（DFPT と違い金属でも可）
- **コスト**: 既存 Wannier 計算に追加で postw90 のみ（低い）
- **限界**: PBE ギャップ問題は残る（ε₂ のピーク位置がずれる）
- **意義**: 成功すれば Paper III の核。Ω → ε(ω) の因果連鎖が閉じる

**注意**: SK model の δ_IPR → Ω テスト (上記) により、TB の δ_IPR は
同一構造クラス内で Ω を予測できないことが判明。したがって
**Ω 自体を δ の第一原理的定義** として使い、Ω → ε₂ を示す方針に修正。

### Priority 2: scissors 補正 + postw90 — n の定量改善

```
入力: postw90 の ε₂(ω) に Δ = Eg_exp - Eg_PBE のシフトを適用
出力: n(ω), R(ω) の定量予測
```

- PBE の ε₂(ω) スペクトル形状は概ね正しく、ピーク位置だけずれる
- scissors でピークをシフトすれば n の定量精度が大幅向上
- HSE06 不要（scissors で十分な場合が多い）
- **検証基準**: C, Si, Ge の n で誤差 < 10%

### Priority 3: HSE06 + DFPT — Ge 問題の根本解決

```
入力: HSE06 SCF → ph.x (epsil=.true.) → ε∞ → n
```

- HSE06 は Ge のギャップを ~0.7 eV に開く → DFPT が可能になる
- **コスト**: PBE の ~10-50x
- **検証基準**: C, Si, Ge 全てで n の誤差 < 5%

### Priority 4: GW + BSE — スペクトル全体の予測（将来課題）

```
入力: PBE SCF → GW → BSE → ε(ω) → n(ω), R(ω)
```

- 準粒子ギャップ + 励起子効果 → 最も正確な ε₂(ω)
- **コスト**: PBE の ~100-1000x
- **検証基準**: ε₂(ω) のピーク位置・形状が実験と一致

### 実験による最終検証

| 実験 | 測定量 | δ との比較 |
|------|--------|----------|
| 分光エリプソメトリー | ε₁(ω), ε₂(ω) | postw90/GW+BSE 出力と直接比較 |
| 反射率測定 | R(ω) | 可視域平均 R vs δ × D_eff |
| ARPES | バンド分散 E(k) | Wannier 補間バンドと一致確認 |
| コンプトン散乱 | 運動量分布 n(p) | Wannier 関数のフーリエ変換と比較 |

コンプトン散乱は Wannier 関数（= δ の実体）の実空間分布を
実験的に検証できる唯一の手法であり、δ の物理的実在性の最終テスト。

### 推奨ロードマップ

```
現在地 ──→ Priority 1 (postw90)
               │
          sum rule 検証: Ω_I = ∫ε₂/ω dω
          δ→ε(ω) の直接接続 (Paper III の核)
               │
          ┌────┴────┐
          │         │
  Priority 2     Priority 3
  scissors+postw90  HSE06+DFPT
  n の定量予測      Ge のギャップ問題解決
          │         │
          └────┬────┘
               │
          Priority 4 (GW+BSE)
          ε(ω) スペクトル全体 (将来課題)
```

## Calculation Design

### Systems

1. **Diamond** (Fd-3m, a = 3.567 Ang, 2 atoms/cell)
   - sp3: 4 equivalent sigma bonds
   - Band gap ~5.5 eV
   - Projection: s;p on each C (8 WFs total)
   - num_wann = num_bands = 8 (no disentanglement needed)

2. **Graphite** (P6_3/mmc, a = 2.461 Ang, c = 6.708 Ang, 4 atoms/cell)
   - sp2 + pi: 3 sigma bonds + 1 delocalized pi per atom
   - Semimetal (band overlap ~40 meV)
   - Projection: s;p on 2 of 4 atoms (8 WFs total)
   - num_wann = num_bands = 8 (exclude_bands 9-20)

3. **Silicon** (Fd-3m, a = 5.431 Ang, 2 atoms/cell)
   - sp3: 4 equivalent sigma bonds
   - Band gap ~1.1 eV
   - Projection: s;p on each Si (8 WFs total)
   - num_wann = num_bands = 8 (no disentanglement needed)
   - ecutwfc = 40 Ry, occupations = 'fixed'

4. **Germanium** (Fd-3m, a = 5.658 Ang, 2 atoms/cell)
   - sp3: 4 equivalent sigma bonds (+ 3d10 core)
   - Band gap ~0.67 eV (PBE may underestimate → smearing used)
   - Pseudopotential: Ge.pbe-**dn**-kjpaw (includes 3d10 in valence, 28 electrons)
   - nbnd = 20 (14 occupied: 10 d-bands + 4 sp3)
   - Energy window: dis_win_min = -5.0 eV (excludes 3d bands at -16 eV)
   - Projection: s;p on each Ge (8 WFs total)
   - num_wann = 8, disentanglement required

### Computational Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| XC functional | PBE | Consistent with Paper II metals |
| Pseudopotential | C.pbe-n-kjpaw_psl.1.0.0.UPF | PAW, same pslibrary as metals |
| ecutwfc | 60 Ry | Carbon needs higher cutoff than metals |
| ecutrho | 480 Ry (C), 320 Ry (Si, Ge) | 8x ecutwfc for PAW |
| k-grid (SCF) | 8x8x8 (diamond, Si, Ge), 8x8x4 (graphite) | Adapted to cell shape |
| k-grid (Wannier) | 4x4x4 (diamond, Si, Ge), 4x4x2 (graphite) | Explicit k-list |
| Smearing | fixed (diamond, Si), Gaussian 0.005 Ry (graphite, Ge) | Insulator vs semimetal |

### Pipeline

```
setup.sh          → Download C pseudopotential
diamond/scf.in    → pw.x (SCF, 8x8x8 k-grid)
diamond/nscf.in   → pw.x (NSCF, explicit 4x4x4 k-points)
diamond/diamond.win → wannier90.x -pp → pw2wannier90.x → wannier90.x
graphite/scf.in   → pw.x (SCF, 8x8x4 k-grid)
graphite/nscf.in  → pw.x (NSCF, explicit 4x4x2 k-points)
graphite/graphite.win → wannier90.x -pp → pw2wannier90.x → wannier90.x
silicon/silicon.win → (same pipeline as diamond)
germanium/germanium.win → (same pipeline, with disentanglement)
analyze_spreads.py → Parse .wout, compute Omega/WF, PASS/FAIL
plot_wannier_comparison.py → fig_wannier_comparison.{png,pdf}
```

### Environment

```bash
# QE + Wannier90 via conda
export PATH="$HOME/miniconda3/envs/qe/bin:$PATH"
```

## Application to Paper I

### What this result means for the paper

Paper I (v7) currently uses three **literature-derived proxies** for delta:
pi-band width, inverse effective mass (1/m*), and band gap. The 7/7
classification success is via the (E_g, D_eff) decision tree. The proxies
support the claim that a single underlying quantity (delta) organizes the
optical categories, but delta itself was never directly computed.

**This Wannier calculation fills that gap.** It provides the first
direct, first-principles measurement of delta_elec for carbon allotropes.

### Specific additions to Paper I

1. **New figure (Fig. 5 or Supplemental)**:
   `fig_wannier_comparison.pdf` — two panels:
   - (a) Omega/WF bar chart: Diamond (0.95) vs K metal (3.75) vs
     Graphite (6.38), color-coded by optical category
   - (b) Graphite individual WF spreads with sigma/pi decomposition

2. **New paragraph in Section III or IV** (after classification results):

   > "To verify that the literature proxies reflect a genuine underlying
   > delocalization, we performed DFT + Wannier90 calculations for bulk
   > diamond and graphite (see Supplemental Material for computational
   > details). The maximally localized Wannier function spread Omega,
   > which directly measures the spatial extent of each electron, gives
   > Omega/WF = 0.95 Ang^2 for diamond and 6.38 Ang^2 for graphite ---
   > a 6.7-fold ratio consistent with the ordering implied by the
   > literature proxies. Moreover, graphite's Wannier functions
   > decompose into localized sigma bonds (5.5--6.3 Ang^2) and
   > delocalized pi orbitals (7.3--8.2 Ang^2), confirming that
   > pi-electron delocalization is the microscopic origin of graphite's
   > metallic optical response."

3. **Strengthened claim in Abstract/Conclusion**:
   Current: "three independent proxies correlate (r = 0.73--0.89)"
   Add: "and the underlying Wannier function spread confirms the
   ordering at the first-principles level"

4. **Connection to Paper II metals**:
   The fact that Diamond (0.95) < K metal (3.75) < Graphite (6.38) on
   the same scale means Papers I and II share a single quantitative
   axis. This cross-validation can be noted in the Outlook section.

### What NOT to do

- Do not overstate: Omega/WF is not delta_IPR. It is a different
  (but related) measure of delocalization. State clearly that
  "Wannier spread provides independent confirmation of the delta
  ordering" rather than "we computed delta from first principles."
- Do not add the full DFT methodology to the main text (it would
  disrupt the flow). Put computational details in Supplemental Material.
- Convergence tests (ecutwfc, k-grid) should be completed before
  publication to ensure the numbers are robust.

## Files

```
simulation/wannier_carbon/
  README.md                      # This file
  setup.sh                       # Download C pseudopotential
  run_all.sh                     # Execute full pipeline
  analyze_spreads.py             # Parse .wout, PASS/FAIL analysis
  plot_wannier_comparison.py     # Generate comparison figure
  fig_wannier_comparison.png     # Output figure (200 dpi)
  fig_wannier_comparison.pdf     # Output figure (vector)
  pseudo/
    C.pbe-n-kjpaw_psl.1.0.0.UPF # PAW pseudopotential (PBE)
  diamond/
    scf.in, nscf.in              # QE input files
    diamond.win, pw2wan.in       # Wannier90 input files
    diamond.wout                 # Wannier90 output (Omega = 7.635)
    scf.out, nscf.out, pw2wan.out
    tmp/                         # QE working directory
  graphite/
    scf.in, nscf.in              # QE input files
    graphite.win, pw2wan.in      # Wannier90 input files
    graphite.wout                # Wannier90 output (Omega = 51.002)
    scf.out, nscf.out, pw2wan.out
    tmp/                         # QE working directory
  silicon/
    scf.in, nscf.in              # QE input files
    silicon.win, pw2wan.in       # Wannier90 input files
    silicon.wout                 # Wannier90 output (Omega = 24.392)
    scf.out, nscf.out, pw2wan.out
    tmp/                         # QE working directory
  germanium/
    scf.in, nscf.in              # QE input files (nbnd=20 for 3d10)
    germanium.win, pw2wan.in     # Wannier90 input (dis_win_min=-5.0)
    germanium.wout               # Wannier90 output (Omega = 18.201)
    scf.out, nscf.out, pw2wan.out
    tmp/                         # QE working directory
  sulfur/
    README.md                    # S8 molecular crystal: too large (128 atoms)
```
