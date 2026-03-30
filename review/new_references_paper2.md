# Paper 2: 追加引用候補リスト

**文献調査 Phase 1 (2026-03-30) の結果に基づく**

---

## 1. 最重要：n_wsの物理的基盤への批判

### Williams, Gelatt & Moruzzi (1980) — Miedemaの微視的基盤批判 ⭐⭐⭐最重要
```bibtex
@article{WilliamsGelattMoruzzi1980,
  author  = {Williams, A. R. and Gelatt Jr., C. D. and Moruzzi, V. L.},
  title   = {Microscopic Basis of {M}iedema's Empirical Theory of Transition-Metal Compound Formation},
  journal = {Phys. Rev. Lett.},
  volume  = {44},
  pages   = {429--432},
  year    = {1980},
}
```
**概要**: 自己無撞着バンド計算により、Miedemaの物理描像（WS境界での電荷密度均一化）が「inappropriate」であることを示した。n_wsの経験的成功はd-band hybridizationのトレンドを暗黙に取り込んでいることに起因すると主張。**しかし、「正しい微視的変数は何か」は提案していない。**
**我々との関係**: **45年来の未解決問題**。我々はδ（電子非局在化指標）がその回答であると提案する。
**推奨フレーミング**:
> "Williams et al. showed that Miedema's physical picture of charge-density equalization at cell boundaries is inappropriate, and that the empirical success of n_ws arises from its implicit capture of d-bond hybridization trends. However, they did not propose a quantitative electronic-structure descriptor to replace n_ws. We argue that the delocalization index δ fills this 45-year-old gap."

### Williams et al. (1982) — 反論への応答
```bibtex
@article{WilliamsGelattMoruzzi1982,
  author  = {Williams, A. R. and Gelatt Jr., C. D. and Moruzzi, V. L.},
  title   = {Reply to ``{C}omment on `{M}icroscopic basis of {M}iedema's theory' ''},
  journal = {Phys. Rev. B},
  volume  = {25},
  pages   = {6509--6512},
  year    = {1982},
}
```
**概要**: Miedema側からの反論に対する応答。Williams et al.は立場を維持。
**我々との関係**: 論争が解決されていないことの証拠として引用可能。

---

## 2. 自由電子模型からの表面エネルギー

### Halas, Durakiewicz & Joyce (2002) — 非局在化電子数→表面エネルギー ⭐⭐引用必須
```bibtex
@article{Halas2002,
  author  = {Halas, S. and Durakiewicz, T. and Joyce, J. J.},
  title   = {Surface energy calculation -- metals with 1 and 2 delocalized electrons per atom},
  journal = {Chem. Phys.},
  volume  = {278},
  pages   = {111--117},
  year    = {2002},
  doi     = {10.1016/S0301-0104(02)00379-8},
}
```
**概要**: Sommerfeld自由電子モデルで表面エネルギーをr_sの関数として解析的に導出。「非局在化電子」=原子あたりの自由電子の整数カウント（Na=1, Mg=2）。s-block金属で実験値と良い一致。
**我々との関係**: 同じ直感（非局在化→表面エネルギー）だが完全に異なるレベルの洗練度。彼らは整数カウント、我々は連続的δ。彼らはs-block金属のみ、我々は遷移金属も含む。
**差別化ポイント**:
> "Halas et al. demonstrated that the free-electron model with an integer count of 'delocalized electrons per atom' successfully predicts surface energies of s-block metals. Our work extends this intuition to a continuous, first-principles delocalization index δ applicable to all metals, including transition metals where the free-electron picture fundamentally fails."
**IPR, ELF, Wannier spreadなど局在化指標は一切使用していない。**

---

## 3. ELF @ 表面（最近接の可視化研究）

### De Santis & Resta (2000) — 金属表面のELF ⭐引用推奨
```bibtex
@article{DeSantisResta2000,
  author  = {De Santis, L. and Resta, R.},
  title   = {Electron localization at metal surfaces},
  journal = {Surf. Sci.},
  volume  = {450},
  pages   = {126--132},
  year    = {2000},
}
```
**概要**: Al(110), Al(100), Al(111)表面でELFを計算。開いた表面ほど原子的、密な表面ほどjellium的。ELFは「metallicityの定量的推定」を提供すると主張。
**我々との関係**: ELFを金属表面に適用した唯一の論文。**しかし表面エネルギーとの相関は一切取っていない。**
**差別化ポイント**:
> "De Santis and Resta applied ELF to aluminum surfaces, demonstrating its utility as a qualitative bonding descriptor. However, they did not establish a quantitative relationship between ELF values and surface energy. Our δ-based approach fills this gap by correlating a delocalization measure with surface tension across multiple metals."

---

## 4. ELF ↔ エネルギーの定量的相関（分子系）

### Ylivainio, Sufyan & Larsson (2025) — ELF_min ↔ 結合エネルギー
```bibtex
@article{Ylivainio2025,
  author  = {Ylivainio, K.-J. and Sufyan, A. and Larsson, J. A.},
  title   = {A quantitative relationship between electron localization function and the strength of physical binding},
  journal = {J. Phys.: Condens. Matter},
  volume  = {37},
  pages   = {205001},
  year    = {2025},
}
```
**概要**: 92の二分子系でELF_min値と結合エネルギーの定量的相関を確認。van der Waals、水素結合、ハロゲン結合に適用。
**我々との関係**: ELFがエネルギーと定量的に相関し得ることの傍証。ただし対象は分子間結合で、金属表面ではない。
**引用の意義**: 「局在化指標→エネルギーの定量的接続」の先例があることを示し、我々のアプローチのもっともらしさを裏付ける。

---

## 5. WS格子内の電子局在化

### Rousseau & Ashcroft (2008) — 間隙電子局在化
```bibtex
@article{RousseauAshcroft2008,
  author  = {Rousseau, B. and Ashcroft, N. W.},
  title   = {Interstitial Electronic Localization},
  journal = {Phys. Rev. Lett.},
  volume  = {101},
  pages   = {046407},
  year    = {2008},
}
```
**概要**: r_c/r_s比が増すと、価電子が間隙領域に局在化することを示した。圧縮下でのバンド幅縮小と接続。
**我々との関係**: WS格子内の電子非局在化/局在化を研究。Miedemaやγへの接続はないが、物理メカニズム（非局在化→間隙密度）の裏付け。
**差別化ポイント**: 「Rousseau-Ashcroftは圧縮下の局在化を研究したが、表面エネルギーやMiedemaのn_wsとの接続は行っていない」

---

## 6. 固体の非局在化指標

### Baranov & Kohout (2011) — 固体の局在化/非局在化指標
```bibtex
@article{BaranovKohout2011,
  author  = {Baranov, A. I. and Kohout, M.},
  title   = {Electron localization and delocalization indices for solids},
  journal = {J. Comput. Chem.},
  volume  = {32},
  pages   = {2064--2076},
  year    = {2011},
}
```
**概要**: NaCl, ダイヤモンド, グラファイト, Na, Cuで固体の非局在化指標を実装。電子を「局在化」と「遊動性」に分割。
**主張**: QTAIMの分子用localization/delocalization indexを固体に拡張可能。金属Naでは大きな非局在化指標、NaClでは小さい値を得る。
**我々との関係**: 固体でδを計算する方法論の先行研究。我々のδ_IPRと概念的に近い量を固体で初めて計算。
**差別化ポイント**: 「Baranov-Kohoutは固体での非局在化指標を計算する方法論を確立したが、それを表面張力や表面エネルギーなどのマクロ物性と接続していない。我々はδを表面張力の予測子として使い、物性との定量的相関を初めて示す。」

---

## 7. ELFの基礎文献

### Becke & Edgecombe (1990) — ELF定義
```bibtex
@article{BeckeEdgecombe1990,
  author  = {Becke, A. D. and Edgecombe, K. E.},
  title   = {A simple measure of electron localization in atomic and molecular systems},
  journal = {J. Chem. Phys.},
  volume  = {92},
  pages   = {5397--5403},
  year    = {1990},
}
```
**概要**: ELFの原論文。同スピン対確率からlocalization measureを定義。
**主張**: 同スピン電子の対確率Dσ(r)を、均一電子ガスの値D⁰σで規格化し、ELF = 1/(1 + (Dσ/D⁰σ)²)を定義。ELF=1は完全局在化、ELF=0.5は均一電子ガス相当。原子殻構造や共有結合を可視化。
**我々との関係**: 最も確立された局在化指標。δ_IPRとの方法論的違いを論じる際に引用必須。
**差別化ポイント**: 「ELFは実空間での局在化を可視化する定性的ツールとして成功したが、(1) 表面エネルギーとの定量的相関に使われたことがない、(2) 値域が[0,1]に圧縮されるため金属間の微細な差を捉えにくい。δ_IPRはバンド構造から直接計算され、連続的な値を取るため定量的相関に適する。」

### Savin et al. (1992) — ELFの固体への拡張
```bibtex
@article{Savin1992,
  author  = {Savin, A. and Jepsen, O. and Flad, J. and Andersen, O. K. and Preuss, H. and von Schnering, H. G.},
  title   = {Electron Localization in Solid-State Structures of the Elements: the Diamond Structure},
  journal = {Angew. Chem. Int. Ed. Engl.},
  volume  = {31},
  pages   = {187--188},
  year    = {1992},
}
```
**概要**: ELFをDFT枠組みで固体に拡張。C, Si, Ge, α-Sn, β-Snで共有結合→金属結合への遷移を可視化。
**主張**: ELFはバルク固体の結合性質を分類できる。ダイヤモンド構造のC→Snで、ELFの結合領域の値が系統的に低下し、共有結合→金属結合への遷移を反映する。
**我々との関係**: ELFが固体の局在化を扱えることの先行研究。バルク結合解析のみ。
**差別化ポイント**: 「Savin et al.はELFで固体のバルク結合を分類したが、表面性質（表面エネルギー、表面張力）への接続は一切行っていない。我々はバルクの非局在化指標δがマクロな界面性質を予測することを示す。」

---

## 8. Miedemaモデルの表面への応用

### Chelikowsky (1984) — Miedema + 表面偏析
```bibtex
@article{Chelikowsky1984,
  author  = {Chelikowsky, J. R.},
  title   = {Predictions for surface segregation in intermetallic alloys},
  journal = {Surf. Sci. Lett.},
  volume  = {139},
  pages   = {L197--L203},
  year    = {1984},
}
```
**概要**: Miedemaパラメータ（n_ws含む）で合金の表面偏析を予測。n_wsに新しい物理的解釈は与えていない。
**主張**: 合金表面では、Miedemaの(n_ws, φ*)パラメータの差が小さい成分が表面に偏析する。経験則として有用だが、n_wsの物理的起源は議論せず、与えられた入力として扱う。
**我々との関係**: Miedemaモデルの表面応用の先行研究。n_wsを「使う」側の研究。
**差別化ポイント**: 「Chelikowskyはn_wsを入力パラメータとして表面偏析を予測したが、n_ws自体がなぜ元素ごとに異なるかは問わなかった。我々はn_wsの起源をδで説明する。」

---

## 9. 追加DFT表面エネルギー

### Skriver & Rosengaard (1992) — 初期のDFT表面エネルギー
```bibtex
@article{SkrieverRosengaard1992,
  author  = {Skriver, H. L. and Rosengaard, N. M.},
  title   = {Surface energy and work function of elemental metals},
  journal = {Phys. Rev. B},
  volume  = {46},
  pages   = {7157--7168},
  year    = {1992},
}
```
**概要**: 元素金属の表面エネルギーと仕事関数のDFT計算。電子局在化の議論なし。
**主張**: LMTO-ASA法で元素金属の表面エネルギーを系統的に計算。周期表全体でのトレンド（d-metal > sp-metal）を再現。物理的解釈としてd-band fillingとの相関を指摘するが、局在化指標は使わない。
**我々との関係**: DFTで表面エネルギーを「計算」する先行研究の代表。計算精度は高いが、予測子（descriptor）を提案していない。
**差別化ポイント**: 「Skriver-Rosengaardは表面エネルギーを個別元素ごとにDFTで計算した。我々の目的は異なり、電子構造からの単純な記述子δで表面張力のトレンドを説明・予測すること。彼らは"何が"ではなく"なぜ"を問わなかった。」

---

## 引用の優先順位

| 優先度 | 論文 | 理由 |
|-------|------|------|
| ⭐⭐⭐ | Williams et al. (1980) | 45年来の未解決問題。我々の動機付け |
| ⭐⭐⭐ | Halas et al. (2002) | 最も近い先行研究。引用して差別化が必須 |
| ⭐⭐ | De Santis & Resta (2000) | ELF@表面。γとの相関なしと明記 |
| ⭐⭐ | Rousseau & Ashcroft (2008) | 非局在化→間隙密度のメカニズム裏付け |
| ⭐ | Ylivainio et al. (2025) | ELF↔エネルギー相関の先例（分子系） |
| ⭐ | Baranov & Kohout (2011) | 固体δの方法論的先行研究 |
| ⭐ | Becke & Edgecombe (1990) | ELF定義。δ_IPRとの違い議論に必要 |
| ⭐ | Savin et al. (1992) | ELFの固体拡張 |
| △ | Williams et al. (1982) | 論争継続の証拠 |
| △ | Chelikowsky (1984) | Miedema+表面 |
| △ | Skriver & Rosengaard (1992) | DFT表面エネルギー（メカニズム不明の例） |

---

## Paper 2 Introduction への推奨追加フロー

```
既存: Lang-Kohn (1970) → jellium表面エネルギー → 単純金属OK, 遷移金属×
         ↓
既存: Miedema (1978) → n_ws経験パラメータ → 全金属OK, 物理的起源不明
         ↓
【NEW】 Williams et al. (1980) → n_wsの物理描像は "inappropriate"
         → 正しい微視的変数は？ → 45年間未解決
         ↓
【NEW】 Halas et al. (2002) → 自由電子カウントで s-block OK → 遷移金属×
         ↓
我々: δ（電子非局在化指標）→ n_wsの微視的起源 → 全金属で検証
```
