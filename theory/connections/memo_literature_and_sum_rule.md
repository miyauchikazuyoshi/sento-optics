# Memo: 先行研究調査と光学 sum rule による実験設計の見直し

**Status: Literature review — directly impacts experiment design.**
**Date: 2026-04-01**

---

## 1. 引用すべき先行研究

### 核となる理論（必須引用）

| 論文 | 内容 | 我々との関係 |
|------|------|------------|
| Penn (1962) PRev 128, 2093 | ε∞ = 1 + (ℏωp/Eg)² | 三因子モデルの理論的祖先 |
| Phillips (1968) PRL 20, 550 | 平均ギャップの共有結合/イオン分解 | δ が homopolar gap E_h を記述 |
| Van Vechten (1969) PRev 182, 891 | 68 結晶で定量検証 | 異元素比較の先駆 |
| Moss (1950) Proc Phys Soc B 63, 167 | n⁴·Eg = const（経験則） | ベンチマーク |
| Ravindra et al. (2007) IPT 50, 21 | n-Eg 関係のレビュー | 先行全体像の一括引用 |

### Wannier 関数の方法論（必須引用）

| 論文 | 内容 | 我々との関係 |
|------|------|------------|
| Marzari & Vanderbilt (1997) PRB 56, 12847 | MLWF の定式化 | Ω 計算の基盤 |
| Souza, Marzari, Vanderbilt (2001) PRB 65, 035109 | Disentanglement | Ge 計算で使用 |
| Yates et al. (2007) PRB 75, 195121 | Wannier 補間光学伝導度 | postw90 の基盤 |

### 最重要：Wannier spread と誘電関数の恒等式

| 論文 | 内容 | 我々との関係 |
|------|------|------------|
| **Cardenas-Castillo et al. (2024) PRB 110, 075203** | **Ω_I = ∫ Im[ε(ω)] dω の証明** | **我々の仮説の数学的基盤** |
| **Rhim & Kim (2025) PRB 111, 085202** | 量子計量 → 誘電マーカー | Ω が quantum metric の運動量積分 |

### 古典的不確定性と量子-古典クロスオーバー

| 論文 | 内容 | 我々との関係 |
|------|------|------------|
| Usha Devi & Karthik (2012) Am. J. Phys. 80, 708 | 古典アンサンブルの不確定性積が量子と同一構造 | δ_nuc の古典-量子対応の数学的基盤 |
| Mandelbrot (1956) IRE Trans. IT-2, 190 | ΔU·Δ(1/T) ≥ k_B 熱力学的不確定性 | k_B が ℏ の役割を果たす対応 |
| Uffink & van Lith (1999) Found. Phys. 29, 655 | Mandelbrot 関係の批判的レビュー | 「古典的不確定性原理」の限界明確化 |
| Zhu & Wang (2024) arXiv:2407.06715 | Δp ≥ √(2π)ℏ/λ_th ボルツマン下限 | 熱揺らぎが ℏ/2 より厳しい下限を課す |
| Magomedov (2024) Solid State Commun. 391 | T_m/Θ_D で量子/古典融解を分類 | Lindemann 条件の量子-古典境界 — Paper III に直接関連 |
| Ullrich, Singh & Vopson (2017) AIP Adv. 7, 045109 | Θ_D = T₀·exp(γ·E_g) 経験則 | Θ_D-E_g-Ω 連鎖の一環。δ_elec と δ_nuc の非独立性 |
| Ackland et al. (2017) Science | Li の量子核効果、再入融解 | 加圧下の量子-古典クロスオーバーの実験的検証例 |
| Chiatti (2024) Entropy 26, 692 | de Broglie の kT = hν; 熱時間 h/kT | 温度-振動数対応の歴史的先行 |

### d 電子遮蔽

| 論文 | 内容 | 我々との関係 |
|------|------|------------|
| Pyykko (1988) Chem Rev 88, 563 | d 遮蔽・相対論効果 | 光学への接続は先行研究なし |

---

## 2. Cardenas-Castillo の sum rule が意味すること

### 恒等式

```
Ω_I = (ℏ²e² / 2πm²) ∫₀^∞ Im[ε(ω)] / ω dω
```

ここで Ω_I は Wannier spread のゲージ不変部分
（Marzari-Vanderbilt 分解の Ω = Ω_I + Ω̃ の第一項）。

### 物理的意味

- Wannier spread（電子の空間的広がり）は、
  全周波数にわたる光学吸収の重みつき積分と**数学的に等しい**
- δ → 光学応答 の接続は「仮説」ではなく「定理」
- ただし sum rule は**積分量**（全周波数の合計）であって、
  **特定の周波数での応答**（n at 589 nm とか）を予測するものではない

### 我々の三因子モデルとの関係

```
n² - 1 ∝ δ × α / E_g²     ← 我々の近似（Penn model ベース）
Ω_I = ∫ ε₂(ω)/ω dω        ← 正確な恒等式（Cardenas-Castillo 2024）
```

三因子モデルは sum rule の**粗い離散化**:
- δ (Ω/WF) ≈ Ω_I/N_wf
- α / E_g² ≈ ∫ の重みの近似（単一遷移近似）

三因子モデルの比例定数が 180x ばらつく理由:
Penn model は単一の「平均ギャップ」で ε₂ の周波数構造を
丸めてしまう。実際の ε₂(ω) は複雑なスペクトル構造を持ち、
元素ごとに形が異なる。積分量（Ω_I）は一致しても、
ω=0 の切片（ε∞, n）は一致しない。

---

## 3. 実験設計の見直し

### 変更前の優先順位

```
Level 1: δ + 実験値（三因子モデル）  ← 序列は合うが定量 ×
Level 2: HSE06 + DFPT               ← Ge 問題を解決
Level 3: GW + BSE                   ← スペクトル予測
Level 4: postw90                    ← δ→ε(ω) 直接接続
```

### 変更後の優先順位

```
Priority 1: postw90 (Wannier 補間光学伝導度)
  → sum rule Ω_I = ∫ε₂/ω dω を直接検証
  → 同じ計算から δ も ε(ω) も出る
  → 新規性が最も高い（Cardenas-Castillo の逆方向）

Priority 2: sum rule の数値検証
  → Wannier90 の Ω_I と postw90 の ∫ε₂/ω dω が一致するか
  → C, Si, Ge（Ge は smearing でも σ(ω) は計算可能）
  → 一致すれば δ↔光学の接続が定理レベルで検証される

Priority 3: scissors + postw90
  → PBE ε₂(ω) に scissors 補正をかけて n を改善
  → HSE06 不要（scissors で十分な場合が多い）

Priority 4: HSE06 / GW+BSE（将来課題）
  → 定量精度の最終検証
```

### 変更の理由

1. **postw90 が最優先になった**: Cardenas-Castillo の恒等式を
   「逆方向」（Ω → ε₂ の予測）で検証する初めての試み。
   これが成功すれば Paper III の核になる。

2. **HSE06 の優先度が下がった**: sum rule は PBE でも成立する
  （ε₂ の形が変わっても積分は保存）。PBE レベルで
   sum rule を検証した後に、必要なら HSE06 で精密化。

3. **Ge が計算可能になった**: DFPT (epsil) は金属に使えないが、
   postw90 の光学伝導度は smearing ありでも計算できる。
   Ge の ε₂(ω) スペクトルが得られる。

4. **三因子モデルの位置づけが明確になった**:
   sum rule の粗い離散化であり、「定性的に正しいが定量的に
   不十分」なのは近似の限界として自然に説明できる。

### 新しい検証チェックリスト

```
[ ] postw90 で C, Si, Ge の σ(ω) → ε₂(ω) を計算
[ ] Ω_I (Wannier90 出力) と ∫ε₂(ω)/ω dω (postw90 出力) が一致するか
[ ] ε₂(ω) スペクトルの形状：C（5eV以下ゼロ）、Si（1eV~）、Ge（0.7eV~）
[ ] scissors 補正で n(ω=0) = √(ε∞) を実験値と比較
[ ] δ が大きい WF ほど光学遷移行列要素が大きいか（分解分析）
```

---

## 4. 我々のアプローチの新規性の明確化

### Cardenas-Castillo との対比

```
彼ら (2024):  ε(ω) の測定 → Ω を抽出   （分析ツール）
我々:         Ω（δ）を計算 → ε(ω) を予測  （設計ツール）
```

同じ恒等式の**逆方向**の利用。

彼らは「Wannier spread は光学 sum rule で検出できる」と言っている。
我々は「Wannier spread から光学応答を分類・予測できる」と言いたい。

数学的には同値だが、科学的な問いが異なる:
- 彼ら: 量子幾何の実験的検出法
- 我々: 材料設計の記述子としての δ

### 先行研究で**ない**こと

1. Ω を**材料記述子**として n や R を予測する試み
2. d 電子遮蔽 → Wannier spread → 光学応答 の接続
3. δ × D_eff による光学カテゴリ分類
4. sum rule の「逆方向」利用（Ω → ε₂ の形状予測）

---

## 5. 論文化への示唆

### Paper I（炭素同素体の光学分類）

追加引用:
- Cardenas-Castillo (2024): δ↔光学の数学的基盤として
- Moss/Ravindra: n-Eg 関係の先行として

追加テキスト（Discussion）:
> "Recently, Cardenas-Castillo et al. (2024) proved that the
> gauge-invariant Wannier spread Ω_I equals the frequency-weighted
> integral of Im[ε(ω)], establishing a rigorous mathematical link
> between electronic delocalization and optical absorption.
> Our classification of carbon allotropes by δ×D_eff can be
> understood as exploiting this identity in the forward direction:
> using Ω as a predictor of optical response, rather than extracting
> it from measured spectra."

### Paper III（新規、異元素間の定量予測）

核となる主張:
1. Cardenas-Castillo の sum rule を forward direction で検証
2. postw90 で Ω → ε₂(ω) の直接接続を実証
3. 三因子モデルは sum rule の Penn 近似として位置づけ
4. d 電子遮蔽の Wannier spread への影響を定量化
