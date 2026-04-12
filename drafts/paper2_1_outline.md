# Paper 2.1: Electronic Delocalization and Surface Tension: From sp/d Uniformity in Solids to the (δ_nuc, δ_elec) Description of Liquids

**旧Paper 2からの再構築。固体→液体への展開を一本の論文に。**

---

## 論旨の核心

δ_elecだけでは表面張力を予測できない（r=-0.18）。
なぜなら**表面張力は液体の性質**であり、液体ではδ_nucも有限だから。
(δ_nuc, δ_elec)の組で初めて液体の界面特性が記述できる。

```
固体でδ_elecを検証（前半）
    ↓
「でもγは液体の量。固体だけでは足りない」（転換点）
    ↓
δ_nucを導入して液体を記述（後半）
    ↓
銭湯の問いへの回答
```

---

## タイトル案

> Electronic Delocalization and Surface Tension:
> From sp/d Uniformity in Solids to the (δ_nuc, δ_elec) Description of Liquids

---

## Abstract（案）

Why do metals with similar bulk densities have vastly different
surface tensions? And why do all liquids—metallic or not—exhibit
surface luster?

We address both questions through a single framework based on
particle delocalization. First, using periodic DFT slab calculations
on 14 metals, we show that the valence electron uniformity ratio
n_mid/n_bulk cleanly separates sp metals (mean 0.96) from d metals
(mean 0.38; t=5.84, p=0.00008). A dimer-level delocalization
index δ_IPR predicts this ratio at r=0.89 (15 elements), and
Wannier spreads confirm the hierarchy independently (6–19× ratio).
The d-band filling progression Ti(0.67) > Fe(0.37) > Cu(0.33)
is consistent with Friedel's model.

However, δ_elec alone does not predict surface tension γ (r=−0.18),
because γ is a property of liquids, where nuclei are also
delocalized (δ_nuc > 0). We propose that the liquid–gas distinction
in surface tension requires both variables: electronic delocalization
(δ_elec, governing cohesive strength) and nuclear delocalization
(δ_nuc, enabling surface self-healing). Liquid metals combine
high δ_elec with finite δ_nuc, producing both high γ and strong
luster. Water has lower δ_elec but similar δ_nuc, yielding
moderate γ and weak luster. Gases have δ_nuc ≫ 0 but δ_elec ≈ 0,
yielding γ = 0 and no luster.

This two-variable description connects the optical response
framework of Paper 1 (δ × D_eff for luster) with the
thermodynamic interface property (γ), providing a unified
electronic-structure interpretation of the original bathhouse
observation: liquids shine because δ_elec enables coherent
optical response, and they have surface tension because
δ_nuc enables surface self-repair while δ_elec maintains cohesion.

---

## 構成

### Part I: 固体における δ_elec の検証（実証済みデータ）

#### 1. Introduction

問い1: なぜバルク密度が同じ金属でγが違うか？（Al/Zn問題）
問い2: なぜ全ての液体は光るのか？（銭湯の問い）

→ 両方とも「粒子の非局在化度δ」で統一的に議論できるという提案。
→ Paper 1（光学）との接続を明示。

#### 2. δ_elec の定義と既存理論との位置づけ

- δ_IPR（操作的定義）、Wannier spread Ω
- 既存理論の盲点: ジェリウム（d金属で破綻）、DFT（数値は出るが「なぜ」がない）
- Miedema n_ws: 歴史的文脈として紹介（δの検証先にはしない）
- Williams (1980)の問い: 部分的機構解釈として位置づけ

#### 3. Methods（固体）

- ダイマーδ_IPR: PySCF, 15元素
- スラブ: QE, 14金属, 価電子分解
- Wannier: 5金属バルク

#### 4. Results（固体）

- ダイマーδ vs midpoint ratio: r = 0.89
- 14金属スラブ sp/d分離: p = 0.00008
- d充填度依存: Ti > Fe > Cu > Zn（Friedel整合）
- アブレーション: 価電子分解の必要性
- Wannier独立確認: 6-19倍

### 転換点: 「でもγは液体の性質」

- δ_elec vs γ: r = -0.18（予測できない）
- 固体スラブでは δ_nuc = 0（核が凍結）
- 表面張力の測定温度は融点以上（液体）
- → 液体を記述するには δ_nuc が必要

### Part II: (δ_nuc, δ_elec) による液体の記述（仮説+文献データ）

#### 5. δ_nuc の導入

- δ_nuc = ⟨r²(t)⟩/a²（MSD / 格子定数²）
- 固体: δ_nuc ≈ 0 → 核が格子点に局在
- 液体: δ_nuc > 0 → 核が拡散（拡散方程式がδ_nucの支配方程式）
- coth公式: δ_nuc(T) = δ_ZP · coth(Θ_D/2T) で量子-古典を統一

#### 6. (δ_nuc, δ_elec) による界面特性の整理

| 系 | δ_nuc | δ_elec | γ | 光沢 |
|---|-------|--------|---|------|
| 固体金属 | ≈ 0 | 高い | —（液体で測定） | 研磨で光沢 |
| 液体金属（Hg, Ga） | > 0 | 高い | 高い | 強い光沢 |
| 水 | > 0 | 低い | 中 | 弱い光沢 |
| 気体 | ≫ 0 | ≈ 0 | 0 | なし |

光沢 = δ_elec（コヒーレント応答） × δ_nucによる表面自己修復
表面張力 = δ_elec（凝集力） × δ_nuc（表面の流動性）

#### 7. 文献データによる支持

- Ga固液比較: 融解でγが変化 + 光沢がジャンプ
  → δ_nuc: 0 → 有限、δ_elec: ほぼ保存
- 水銀臨界点: δ_elecが連続低下 → γ → 0, 光沢消失
  → (δ_nuc, δ_elec) 相図上のL字型軌跡
- 液体金属の「二重のδ」:
  δ_elec → R（反射率）を高める
  δ_elec → γ（表面張力）を高める → 表面を自己平滑化
  → 条件A（材質）と条件B（形状）が同じδから同時に満たされる

#### 8. Discussion

- Paper 1との統一: δ_elec × D_eff → 光学、(δ_nuc, δ_elec) → 表面張力
- 既存理論との関係（Friedel, Lang-Kohn, Miedema）
- δ vs n_ws: 均一性（ratio）vs 絶対密度（quantity）の区別
- Williams (1980)への部分的回答

#### 9. Limitations

- 液体のAIMD計算はまだ実施していない（文献データのみ）
- δ_nucの操作的定義は提案段階
- δからγの定量予測はできない（質的記述子）
- 固体: 実証済み / 液体: 仮説提案

#### 10. Conclusion

sp/d電子均一性差が金属表面張力変動の電子的起源であることを
固体14金属で実証した。しかしδ_elecだけでは表面張力を
予測できない。液体の表面張力を記述するには(δ_nuc, δ_elec)の
両方が必要であり、この2変数は光沢と表面張力を
「粒子の非局在化」という単一の概念から統一的に導出する。

---

## この構成の強み

1. **δが「不要な物理量」にならない** — 液体を記述するために必要
2. **固体の実証（p=0.00008）が論文の土台** — 仮説だけの論文ではない
3. **銭湯の問いに直接回答** — 液体の光沢と表面張力の統一記述
4. **Paper 1との接続が自然** — δ_elec × D_eff（光学）+ (δ_nuc, δ_elec)（表面張力）
5. **正直** — 固体は実証、液体は仮説と明確に分離

---

## 実験・シミュレーションで検証すべき項目

以下はPart II（液体）の仮説を検証するために必要な計算/実験。

### 最高優先（Paper 2.1に必須）

#### S1. 液体金属のAIMD + Wannier spread
- **系**: 液体Na, Al, Cu, Zn（固体で比較データがある4元素）
- **手法**: QE AIMD（Born-Oppenheimer MD, PBE, 64-128原子, T=T_m+100K）
- **計算量**: Wannier90で各MDスナップショットのΩを計算
- **得られるもの**:
  - δ_elec(liquid): 液体状態のWannier spread
  - δ_elec(solid) vs δ_elec(liquid) の比較
  - 融解でΩがどう変わるか → Remsing & Klein (2020)の液体Siと比較
- **検証**: δ_elec(liquid)がsp/d差を保つか？ 保てばδの液体への転用が正当化

#### S2. 液体金属のMSD → δ_nuc
- **同じAIMDから計算可能**
- **得られるもの**: δ_nuc = ⟨r²(t)⟩/a² の時間発展
- **検証**: δ_nucが全液体で有限（>0）になることを確認
  各金属のδ_nucの大きさを比較

#### S3. (δ_nuc, δ_elec) vs γ の相関
- **S1+S2の結果から直接計算**
- **検証**: (δ_nuc, δ_elec)の組がγの系統性を説明するか
  2変数回帰: γ = f(δ_nuc, δ_elec) のR²

### 高優先（Paper 2.1を強化）

#### S4. Ga固液比較
- **系**: 固体Ga(ortho) + 液体Ga（融点29.8°C, 室温AIMD可能）
- **手法**: 固体SCF + 液体AIMD, 各状態でΩを計算
- **得られるもの**: 融解前後のδ_elec変化
- **検証**: Gaは融解で導電率が上がる異常金属。δ_elecも上がるか？

#### S5. 水のAIMD + 電子構造
- **系**: 液体水（64-128分子, T=300K, PBE+D3）
- **手法**: AIMD + Wannier90（水の場合はMLWFがO孤立電子対に対応）
- **得られるもの**: 水のδ_elec（分子間電子重なり）
- **検証**: δ_elec(water) << δ_elec(liquid metal) を定量確認
  → γ差の電子的起源

### 中優先（Paper 2.1のDiscussionを補強）

#### S6. 温度依存性: δ_elec(T) の追跡
- **系**: 液体Naを T_m → T_m+500K で温度走査
- **手法**: 各温度でAIMD → Ω計算
- **得られるもの**: δ_elec(T) の温度依存性
- **検証**: 温度上昇でδ_elecは変わるか？ γ(T)の温度係数と対応するか？

#### S7. 水銀の密度依存 δ_elec
- **系**: Hg（液体, 密度を連続変化: 13.6 → 9 g/cm³）
- **手法**: Kresse & Hafner (1997) のAIMDパイプラインにΩ計算を追加
- **得られるもの**: δ_elec(ρ) — 密度とともに連続的に変化するか
- **検証**: 金属-非金属転移でδ_elecがゼロに近づくか
  3レジーム（弱散乱/強散乱/非金属）がδの連続変化で統一できるか

### 低優先（将来課題として記述）

#### S8. 合金系: NaK, CuZn の液体AIMD
- 文献データ（R vs γ相関）の直接検証

#### S9. δ_nucのcoth公式検証
- 固体→液体の転移でδ_nucがcoth公式から外れるか
- δ_nuc(固体) = coth値、δ_nuc(液体) = MSD値の比較

---

## コスト見積もり

| 計算 | 系 | 原子数 | MD steps | 所要時間 |
|------|---|--------|----------|---------|
| S1+S2 液体Na | 64 | 5000 | 1-2日 |
| S1+S2 液体Al | 64 | 5000 | 1-2日 |
| S1+S2 液体Cu | 64 | 10000 | 2-4日 |
| S4 液体Ga | 64 | 5000 | 1-2日 |
| S5 液体水 | 64分子 | 10000 | 3-5日 |

合計: **2-3週間**（1 GPU/CPUノード）。
ローカル環境でのQE AIMDが可能かは要確認。

---

*旧Paper 2.1アウトラインを全面改訂。2026-04-09。*
