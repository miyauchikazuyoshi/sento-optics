# Paper 2.1: sp/d Electron Uniformity as the Electronic Origin of Surface Tension Variation in Metals

**旧Paper 2からの再構築。n_wsを因果連鎖から外し、sp/d均一性差を核心に据える。**

---

## タイトル案

> sp/d Electron Uniformity as the Electronic Origin of Surface Tension Variation in Metals

または

> Why Do Metals with Similar Densities Have Different Surface Tensions? Valence Electron Uniformity across 14 Metals

---

## Abstract（案）

Metals with similar bulk electron densities can have vastly different
surface tensions (e.g., Al and Zn: Δr_s = 2.4%, Δγ = 46%).
Jellium models fail for d-metals, and DFT slab calculations can
compute γ numerically but do not identify a single descriptor
explaining the systematic variation.

Here we show that the sp/d uniformity of valence electron distribution
—quantified by the interstitial density ratio n_mid/n_bulk from
periodic DFT slab calculations—cleanly separates sp and d metals.
Across 14 metals (8 sp-type, 6 d-type including Fe, Ti, Ag),
sp metals show near-uniform valence density (mean ratio = 0.96)
while d metals show strong depletion (mean = 0.38), a 2.5× difference
(t = 5.84, p = 0.00008).

The progression Ti(d²: 0.67) > Fe(d⁶: 0.37) > Cu(d¹⁰: 0.33)
is consistent with Friedel's d-band filling picture: as d-electrons
fill, they localize and deplete the interstitial region.

A dimer-level delocalization index δ_IPR, based on the inverse
participation ratio of Kohn-Sham orbitals, predicts the midpoint
density ratio at r = 0.89 (15 dimers, p < 0.001), providing an
electronic-structure origin for the uniformity difference.
Maximally localized Wannier function spreads independently confirm
the sp > d hierarchy (6–19× ratio).

We note that δ_IPR does not correlate with Miedema's empirical
n_ws^{1/3} (r = 0.10), indicating that δ measures electron
uniformity (a normalized ratio) while n_ws reflects absolute
boundary density (which depends on both uniformity and total
electron count). The sp/d uniformity difference identified here
provides a qualitative mechanistic interpretation—but not a
quantitative predictor—of why surface tension varies systematically
across the periodic table.

---

## 構成

### 1. Introduction

**問い**: なぜバルク密度（r_s）がほぼ同じ金属でγが大きく違うか？

- Al/Zn問題: Δr_s=2.4%, Δγ=46%
- ジェリウムの限界（Lang-Kohn: d金属で破綻）
- DFTは計算できるが「なぜ」を説明しない
- Miedemaのn_wsは経験的に成功（Williams 1980の問い）
- **本研究**: sp/d電子の均一性差が表面張力変動の電子的起源

歴史的文脈としてMiedemaに触れるが、n_wsとの直接相関は主張しない。

### 2. Framework

**核心主張**: 表面張力の金属間変動は、価電子がWigner-Seitzセル内で
どれだけ均一に分布するかで系統的に整理できる。

- sp電子: 等方的非局在化 → セル全体に均一に広がる → 界面で平坦
- d電子: 指向性局在 → 原子上に集中 → 界面で枯渇

因果連鎖:
```
軌道対称性 (s,p vs d) → 波動関数の空間均一性 (δ)
    → セル間領域の電子密度 (n_mid/n_bulk)
    → 表面エネルギー（界面での電子の再配置コスト）
    → 表面張力 γ
```

### 3. Methods

#### 3.1 ダイマーδ_IPR計算
- PySCF, B3LYP/def2-SVP, 15元素
- 全電子δ_IPR + 価電子δ_val（コア除外）
- 中間点密度比の計算

#### 3.2 周期DFTスラブ計算
- Quantum ESPRESSO 7.5, PAW-PBE
- 14金属（Na,K,Al,Li,Be,Mg,Ca,Si,Ga,Ti,Fe,Cu,Zn,Ag）
- 7層スラブ + 15Å真空
- 価電子分解（ILDOS, plot_num=10）
- n_mid/n_bulkの操作的定義（中央3層平均、内部中間点）
- **追加9元素の完全な計算条件**

#### 3.3 Wannier spread計算
- Wannier90, 5金属バルク
- MLWF spread Ω

#### 3.4 統計解析
- Pearson相関、t検定、2変数回帰

### 4. Results

#### 4.1 ダイマーδ_IPRは中間点密度比を予測する
- 15元素: r = 0.89 (p < 0.001)
- 価電子版が改善: r = 0.86 → 0.89
- **核心結果**: δが高いほど電子が均一に広がる

#### 4.2 14金属スラブ: sp/d分離
- sp平均0.96 vs d平均0.38: **2.5倍差、p=0.00008**
- 全sp金属(Li,Be,Na,Mg,Al,K,Ca): 0.94-1.13
- d充填度依存: Ti(0.67) > Fe(0.37) > Cu(0.33) > Zn(0.28)
- アブレーション: 全電子ではsp/d差が隠れ、価電子分解で回復

#### 4.3 Wannier spreadの独立確認
- sp: Al 12.9, Na 11.7 Å² >> d: Cu 1.9, Zn 0.7 Å²
- 6-19倍差

#### 4.4 δとMiedema n_wsの非相関
- δ_val vs n_ws^{1/3}: r = 0.10（無相関）
- しかしn_mid(abs) vs n_ws^{1/3}: r = 0.79
- **δは均一性（ratio）を測り、n_wsは絶対密度を測る**

### 5. Discussion

#### 5.1 なぜsp金属とd金属で表面張力が系統的に異なるか
- sp: 電子が均一 → 表面を作っても電子再配置が少ない → γが密度に比例
- d: 電子が原子上に局在 → 表面で電子環境が大きく変わる → γがr_sだけでは予測不能
- Friedelのd充填模型との整合

#### 5.2 Miedema n_wsとの関係
- n_wsは境界の「絶対密度」に対応（r=0.79）
- δは境界の「均一性」に対応（ratio r=0.89）
- 両者は同じ物理の異なる側面を測る
- Williams (1980)の問いへの部分的機構解釈

#### 5.3 Paper 1（光学応答）との接続
- 同じδが光学分類と表面張力の均一性差を横断的に記述
- 光学: δ × D_eff → 反射率の質
- 表面: δ → n_mid/n_bulk → 電子再配置コスト

#### 5.4 液体金属への含意
- 固体スラブの結果は液体表面張力の議論に転用できるか？
- 軌道対称性は融解でも保存（sp/d差は温度に鈍感）

### 6. Limitations
- ダイマーδとバルクn_wsの相関はない（r=0.10）
- δは質的記述子であり、γの定量予測はMiedemaに劣る
- Wannier計算は5金属のみ
- Ni未収束
- 5d金属(Au,Pt,W)は相対論が必要

### 7. Conclusion

sp/d電子の均一性差が金属表面張力の系統的変動の電子的起源であることを
14金属のDFTスラブ計算で実証した。
δ（IPRに基づく非局在化指標）はこの均一性差を定量化し、
ダイマーレベルで中間点密度比を予測する（r=0.89）。
δはMiedema n_wsの直接予測子ではないが（r=0.10）、
n_wsの背後にあるsp/d電子構造の質的差異を記述する。

---

## 旧Paper 2からの変更点

| 項目 | 旧 | 新 |
|------|-----|-----|
| タイトル | What Does Miedema's n_ws Measure? | sp/d Electron Uniformity... |
| 核心主張 | δ → n_ws → γ | δ → sp/d均一性 → 界面電子パターン |
| n_wsの位置 | 因果連鎖の中間変数 | Discussion内の歴史的文脈 |
| δ vs n_ws | r=0.10を隠す | r=0.10を正直に報告、理由を説明 |
| 最強の証拠 | δ vs n_ws相関（旧r=0.84、誤り） | sp/dスラブ分離 p=0.00008 |
| Williams問題 | 「答えた」 | 「部分的機構解釈を提案」 |

---

## この構成の強み

1. **最強の証拠が核心にある**: p=0.00008とr=0.89が論文の柱
2. **弱い結果を隠さない**: δ vs n_ws = 0.10は正直にdiscuss
3. **n_wsに依存しない**: n_ws値の出典問題が論文の核心に影響しない
4. **Paper 1との接続が自然**: 同じδが光学と表面張力を横断
5. **Friedel模型との整合**: Ti>Fe>Cu>Znの系統性が理論的文脈を持つ
