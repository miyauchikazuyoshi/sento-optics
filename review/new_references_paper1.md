# Paper 1: 追加引用候補リスト

**文献調査 Phase 1 (2026-03-30) の結果に基づく**

---

## 1. 最近接先行研究（差別化が必要）

### Levine & Louie (1982) — gap→金属の連続的誘電関数 ⭐重要
```bibtex
@article{LevineLouie1982,
  author  = {Levine, Z. H. and Louie, S. G.},
  title   = {New model dielectric function and exchange-correlation potential for semiconductors and insulators},
  journal = {Phys. Rev. B},
  volume  = {25},
  pages   = {6310--6316},
  year    = {1982},
}
```
**概要**: Penn模型を改良し、gap→0でLindhard自由電子誘電関数に連続的に接続するモデル誘電関数を構築。Kramers-Kronig関係と粒子数和則を満たす。
**我々との関係**: δ×D_effの概念的祖先。ただし1パラメータ（gapのみ）で、光学分類ではなく交換相関ポテンシャルの構築が目的。
**差別化ポイント**: 「Levine-Louieはgapの1変数でε(q)を半導体→金属に接続したが、金属間の差異（なぜAlは光りCuは色がつくか）は区別できない。δ×D_effは2変数により物質分類を可能にする。」

---

### Raza, Thygesen & Naik (2026) — Super-Mossian 2Dマップ ⭐重要
```bibtex
@article{RazaThygesenNaik2026,
  author  = {Raza, Sajjad and Thygesen, Kristian S. and Naik, Gururaj V.},
  title   = {Breaking the {M}oss rule},
  journal = {arXiv preprint},
  eprint  = {2602.16247},
  year    = {2026},
}
```
**概要**: Moss則 n⁴×E_g = 95 eV を超える「super-Mossian」誘電体を体系的に分類。(n, E_g)の2次元空間で材料をマッピング。Joint density of statesがMoss上限を決定すると主張。
**我々との関係**: 最新の2変数光学分類の試み。ただし半導体/誘電体のみ、金属は対象外。
**差別化ポイント**: 「Raza et al.は(n, E_g)空間で誘電体を分類したが、金属を同一フレームワークに含めていない。我々のδ×D_effは金属・半導体・絶縁体を統一的に扱う。」

---

### Moss (1985) — n⁴×E_g経験則
```bibtex
@article{Moss1985,
  author  = {Moss, T. S.},
  title   = {Relations between the Refractive Index and Energy Gap of Semiconductors},
  journal = {Phys. Status Solidi B},
  volume  = {131},
  pages   = {415--427},
  year    = {1985},
}
```
**概要**: 半導体の屈折率とバンドギャップの経験則 n⁴×E_g ≈ 95 eV。Penn模型から理論的根拠を与えた。
**主張**: 半導体では屈折率とバンドギャップの間に普遍的な関係が存在する。
**我々との関係**: δがE_gを包含するため、Moss則はδフレームワークの特殊ケースとして理解可能。
**差別化ポイント**: 「Moss則は(n, E_g)の1次元拘束条件であり、半導体内の1パラメータ相関。金属（E_g=0）では定義不能。δ×D_effは金属も含む2次元空間での分類を可能にし、E_g=0同士の金属間の差異も記述する。」

---

## 2. Penn模型の改良（背景として引用）

### Penn (1962) — 原論文 ※既にサーベイガイドにあるが未引用
```bibtex
@article{Penn1962,
  author  = {Penn, D. R.},
  title   = {Wave-Number-Dependent Dielectric Function of Semiconductors},
  journal = {Phys. Rev.},
  volume  = {128},
  pages   = {2093--2100},
  year    = {1962},
}
```
**概要**: 「平均ギャップ」E_gからε(q)を導出。半導体で最も広く使われるモデル誘電関数。
**主張**: 半導体の誘電関数は、バンド構造の詳細によらず「平均ギャップ」の1パラメータで良く近似できる。均一電子ガスの遮蔽にギャップ効果を加えた解析的表式を導出。
**我々との関係**: Paper 1の最大の先行研究。δ×D_effがPennを「包含する」ことを示す必要がある。Penn模型ではE_g→0で金属、E_g→∞で絶縁体だが、金属間の差異（光沢の度合い）を区別できない。δがその次元を追加する。
**差別化ポイント**: 「Pennは1パラメータ（E_g）で半導体のε(q)を記述したが、(1) 金属ではE_g=0となり全金属が縮退する、(2) 有効次元性D_effの効果（グラファイトvs.ダイヤモンド）を捉えられない。δ×D_effの2変数はこれらの限界を解消する。」

---

### Ravindra et al. (2007) — n-E_g関係のレビュー
```bibtex
@article{Ravindra2007,
  author  = {Ravindra, N. M. and Ganapathy, P. and Choi, J.},
  title   = {Energy gap-refractive index relations in semiconductors -- An overview},
  journal = {Infrared Phys. Technol.},
  volume  = {50},
  pages   = {21--29},
  year    = {2007},
}
```
**概要**: Moss則、Ravindra線形則、Herve-Vandamme、Penn、Wemple-DiDomenicoの網羅的レビュー。すべて半導体限定。
**我々との関係**: 「既存のn-E_g関係はすべて半導体に限定されている」ことのレビュー証拠として引用。

---

## 3. 光学側のWannier接続（新しい展開）

### Wannier spread ↔ 光学和則 (2024)
```bibtex
@article{WannierOptical2024,
  author  = {(要確認)},
  title   = {Detecting {W}annier spread via optical sum rules in disordered 2{D} semiconductors},
  journal = {arXiv preprint},
  eprint  = {2405.06146},
  year    = {2024},
}
```
**概要**: 2D半導体でWannier spreadが光学和則（吸光度の積分値）に直接現れることを示した。
**主張**: 乱れた2D半導体において、Wannier関数の広がり（spread）が吸光度の積分和則に直接寄与する。Wannier spreadが測定可能な光学量に結びつく理論的根拠を確立。
**我々との関係**: 「Wannier spread → 光学応答」という接続を理論的に示した最新の先行研究。Paper 1でδの一つとしてWannier spreadを使う正当性を裏付ける。
**差別化ポイント**: 「彼らは2D半導体に限定し、和則の形式的導出が主題。我々はδ（Wannier spread含む）を3D金属・半導体・絶縁体にまたがる物質分類に応用する。光学和則ではなく、マクロな反射率・光沢の予測が目的。」
**注意**: 著者名・正確なタイトルを確認する必要あり。

---

## 4. 光沢の微視的理論（存在しないことの証拠）

### Bennett & Porteus (1961) — 表面粗さと鏡面反射
```bibtex
@article{BennettPorteus1961,
  author  = {Bennett, H. E. and Porteus, J. O.},
  title   = {Relation Between Surface Roughness and Specular Reflectance at Normal Incidence},
  journal = {J. Opt. Soc. Am.},
  volume  = {51},
  pages   = {123--129},
  year    = {1961},
}
```
**概要**: 表面粗さと鏡面反射率の定量的関係。「どの程度滑らかなら光るか」のマクロ基準を確立。
**主張**: 表面粗さσがλ/4πn以下であれば鏡面反射が支配的。RMS粗さと反射率の指数関数的関係を実験的に確立。
**我々との関係**: マクロ側の「光る条件」（表面形態）。我々はミクロ側（電子構造が何を決めるか）を提供。
**差別化ポイント**: 「Bennett-Porteusはマクロな表面形態が鏡面反射の必要条件であることを示した。我々の問いは異なる：十分に平坦な表面を持つ物質のうち、なぜある物質は光り、別の物質は光らないのか。それを電子構造（δ×D_eff）で説明する。」

---

## 5. 教科書的引用

### Dressel & Grüner (2002)
```bibtex
@book{DresselGruner2002,
  author    = {Dressel, M. and Gr{\"u}ner, G.},
  title     = {Electrodynamics of Solids: Optical Properties of Electrons in Matter},
  publisher = {Cambridge University Press},
  year      = {2002},
}
```
**概要**: 固体の光学特性の現代的教科書。金属・半導体・超伝導体を統一的に扱うが、2変数分類フレームワークは提示していない。
**主張**: 固体の光学応答はDrudeモデル（金属）、ローレンツモデル（絶縁体）、バンド間遷移の3つの枠組みで理解される。
**我々との関係**: 教科書的標準アプローチの代表。物質クラスごとに異なるモデルを使い分ける従来手法。
**差別化ポイント**: 「Dressel-Grünerは金属・半導体・絶縁体にそれぞれ異なるモデルを適用する。我々のδ×D_effはこれらを1つの2変数フレームワークで統一する。」

---

## 引用の優先順位

| 優先度 | 論文 | 理由 |
|-------|------|------|
| ⭐⭐⭐ | Penn (1962) | 最大の先行研究。差別化が必須 |
| ⭐⭐⭐ | Levine-Louie (1982) | 概念的最近接。1変数 vs 2変数の差を明記 |
| ⭐⭐ | Raza et al. (2026) | 最新の2Dマップ。金属なしとの差別化 |
| ⭐⭐ | Moss (1985) | 経験則。δで包含可能と主張 |
| ⭐ | Ravindra et al. (2007) | レビュー。既存手法が半導体限定の証拠 |
| ⭐ | arXiv:2405.06146 (2024) | Wannier-光学接続の最新理論 |
| △ | Bennett-Porteus (1961) | マクロ粗さ基準。背景として |
