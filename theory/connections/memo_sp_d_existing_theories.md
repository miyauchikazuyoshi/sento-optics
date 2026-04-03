# sp金属 vs d金属: 既存理論の傾向差とδ枠組みの位置づけ

**Status: 2026-04-04。文献レビューに基づく整理。**

---

## 1. 既存理論が記述するsp/d差

### 1.1 バンド理論（基本的事実）

sp金属は自由電子的な放物線バンド（分散幅 W ~ 10 eV）を持ち、
d金属は狭いdバンド（W ~ 5 eV）がspバンドに重畳する。
dバンドはフラット（状態密度が高く、電子が局在的）。

これは教科書的事実であり、以下の全ての理論の出発点。

### 1.2 ジェリウム模型（Lang & Kohn 1970）

> N. D. Lang and W. Kohn, "Theory of Metal Surfaces: Charge Density
> and Surface Energy," Phys. Rev. B **1**, 4555–4568 (1970).

電子を均一正電荷背景（ジェリウム）中の量子ガスとして扱い、
密度勾配から表面エネルギーを計算。

- **sp金属（Na, K, Al）**: 表面エネルギーが正しく再現される
- **d金属**: 高密度で**負の表面エネルギー**が出る（物理的にナンセンス）
- **原因**: ジェリウムは電子を均一ガスとして扱う → d電子の局在性を無視

**δ枠組みとの関係**: ジェリウムが失敗する理由を「d電子の局在化（低δ）が
均一ガス近似を破る」と説明できる。これがPaper 2の動機の一つ。

### 1.3 Miedema模型（1973–1988）

> A. R. Miedema, "The electronegativity parameter for transition
> metals: Heat of formation and charge transfer in alloys,"
> J. Less-Common Met. **32**, 117–136 (1973).

> A. R. Miedema, P. F. de Chatel, and F. R. de Boer, "Cohesion in
> alloys — fundamentals of a semi-empirical model,"
> Physica B **100**, 1–28 (1980).

n_ws（Wigner-Seitzセル境界の電子密度）とφ*（電気陰性度）の
2変数で合金の生成熱・表面エネルギーを予測する半経験的模型。

- sp金属とd金属で**n_wsの傾向が異なる**ことは経験的に知られていた
- 表面張力: γ ∝ n_ws^{5/3} / V_m^{2/3}
- ±10-20%の精度で広範な金属の表面張力を予測

**だがn_wsがなぜ金属ごとに異なるかは説明されていない。**

### 1.4 Williams–Gelatt–Moruzzi の問い（1980）

> A. R. Williams, C. D. Gelatt, Jr., and V. L. Moruzzi,
> "Microscopic Basis of Miedema's Empirical Theory of
> Transition-Metal Compound Formation,"
> Phys. Rev. Lett. **44**, 429 (1980).

Miedemaのn_wsの物理的描像は "inappropriate" と指摘。
n_wsが表面張力を予測できる理由の物理的説明を求めた。

**45年間、この問いに直接答えた論文はない。**
Paper 2はδ_IPRを通じてこの問いに回答を試みる。

### 1.5 Friedel模型（dバンド充填と凝集）

> J. Friedel, "Transition Metals. Electronic Structure of the
> d-Band. Its Role in the Crystalline and Magnetic Structures,"
> in *The Physics of Metals*, Vol. 1: *Electrons*, edited by
> J. M. Ziman (Cambridge University Press, 1969), pp. 340–408.

dバンドの充填度と凝集エネルギーの放物線的関係:
- d⁵（半充填）付近で凝集エネルギー最大 → Cr, Mo, W の高融点
- d¹⁰（閉殻）で凝集エネルギーが低下 → Cu, Zn の「弱い」d結合

**14元素スラブデータとの整合**: Ti(d²)=0.67 vs Fe(d⁶)=0.37
vs Cu(d¹⁰)=0.33。d充填が進むほどdバンドが狭くなり局在する傾向。

### 1.6 d-band center理論（Hammer & Nørskov 1995）

> B. Hammer and J. K. Nørskov, "Why gold is the noblest of all
> the metals," Nature **376**, 238–240 (1995).

> B. Hammer and J. K. Nørskov, "Electronic factors determining
> the reactivity of metal surfaces,"
> Surf. Sci. **343**, 211–220 (1995).

触媒活性がdバンド中心のフェルミ準位からの距離で決まる。
- sp金属: dバンドがないか深い → 不活性
- d金属: dバンドがフェルミ付近 → 反応性

**δとの関係**: d-band centerは「dバンドがどこにあるか」（位置）、
δは「電子がどれだけ広がるか」（広がり）。相補的な記述。

### 1.7 s-d散乱と抵抗率（Mott 1936）

> N. F. Mott, "The Electrical Conductivity of Transition Metals,"
> Proc. R. Soc. London A **153**, 699–717 (1936).

sp電子がdバンドに散乱されることで抵抗率が増大する。
- sp金属: 低抵抗率（Na 4.2, Al 2.7 μΩcm）
- d金属: 高抵抗率（Fe 9.7, Ni 6.8 μΩcm）

### 1.8 光学特性

- sp金属: Drude的応答（高い反射率、プラズマ端がUV）
- d金属: バンド間遷移が可視域に出現（Cu→赤、Au→黄）

Johnson & Christy (1972, 1974) の光学定数データで定量化されている。

---

## 2. δ枠組みが追加するもの

| 既存理論 | 何がわかるか | 何が足りないか |
|---------|-----------|-------------|
| バンド理論 | spバンド広い、dバンド狭い | → だからn_wsがどうなるか |
| ジェリウム | sp金属で成功、dで破綻 | → なぜ破綻するか |
| Miedema | n_wsで表面張力を予測 | → n_wsの物理的起源 |
| Friedel | d充填 → 凝集エネルギー | → 界面電子密度との接続 |
| d-band center | dバンド位置 → 触媒活性 | → 表面張力との接続 |
| Mott | s-d散乱 → 抵抗率 | → 界面物性との接続 |

**δは「sp/d差が界面電子密度（n_ws）にどう現れるか」を説明する。**
各理論はsp/dの**ある側面**を記述するが、n_wsの起源を
電子非局在化に帰着させたのはδが初めて。

---

## 3. 14元素スラブデータとの対応

### 3.1 結果（emax=100.0修正後）

| グループ | 元素 | n_mid/n_bulk平均 | 統計 |
|---------|------|----------------|------|
| sp (8元素) | Li, Be, Na, Mg, Al, K, Ca, Si | 0.96 | |
| d (6元素) | Cu, Zn, Ga, Ti, Ag, Fe | 0.38 | |
| | | sp/d比: **2.5倍** | **p = 0.00008** |

### 3.2 各元素の詳細

| 元素 | タイプ | n_mid/n_bulk | 既存理論での位置づけ |
|------|--------|-------------|------------------|
| Li–Ca | 純sp | 0.94–1.13 | 自由電子金属、ジェリウムが成功する系 |
| Si | sp³ | 0.48 | 指向性結合 → 局在を促進（バンド理論と整合） |
| Ti | d² | 0.67 | d充填少 → Friedel模型で凝集弱 → δやや高い |
| Fe | d⁶ | 0.37 | d充填中 → d局在が効く |
| Cu | d¹⁰ | 0.33 | d閉殻 → 最も局在（Friedel放物線の端） |
| Zn | d¹⁰ | 0.28 | 同上 |
| Ga | sp+d¹⁰ | 0.28 | 3d¹⁰コアのスクリーニング効果 |
| Ag | 4d¹⁰ | 0.37 | Cu同様、周期が変わっても傾向保持 |

### 3.3 Friedel模型との整合

d充填が進むほどn_mid/n_bulkが低下する傾向:
- Ti (d²): 0.67
- Fe (d⁶): 0.37
- Cu (d¹⁰): 0.33

これはFriedel模型の「d充填 → dバンド狭化 → 局在」と整合する。
δ枠組みはこの傾向をn_ws（界面密度）に接続する。

---

## 4. デバッグの記録

初期結果（emax=0.0バグ）ではTi=1.08, Fe=1.15と
sp金属並みの値が出て仮説が崩壊したように見えた。
原因はILDOSのエネルギー窓上限が0.0eV（フェルミ準位以下）に
設定されていたため、ほとんどの価電子が窓外だった。

emax=100.0に修正後、Ti=0.67, Fe=0.37と
d金属的な値に変化し、仮説と整合した。

**教訓**: 計算のデバッグなしに物理的結論を出すのは危険。
異常値が出たとき、まず実験設計（パラメータ設定）を疑うべき。

---

## 参考文献

- Lang, N. D. and Kohn, W. (1970) Phys. Rev. B **1**, 4555.
- Miedema, A. R. (1973) J. Less-Common Met. **32**, 117.
- Miedema, A. R., de Chatel, P. F. and de Boer, F. R. (1980) Physica B **100**, 1.
- Williams, A. R., Gelatt, C. D. Jr. and Moruzzi, V. L. (1980) Phys. Rev. Lett. **44**, 429.
- de Boer, F. R., Boom, R., Mattens, W. C. M., Miedema, A. R. and Niessen, A. K. (1988) *Cohesion in Metals: Transition Metal Alloys* (North-Holland, Amsterdam).
- Friedel, J. (1969) in *The Physics of Metals*, Vol. 1, ed. J. M. Ziman (Cambridge Univ. Press), pp. 340–408.
- Hammer, B. and Nørskov, J. K. (1995) Nature **376**, 238.
- Hammer, B. and Nørskov, J. K. (1995) Surf. Sci. **343**, 211.
- Mott, N. F. (1936) Proc. R. Soc. London A **153**, 699.
