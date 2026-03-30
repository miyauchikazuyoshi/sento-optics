# 最新の関連研究：3つの観点からのギャップ分析

サーベイ実施日: 2026-03-30
検索エンジン: Google Scholar / Web検索

---

## 1. Penn モデルと光学応答の統一分類

### Penn (1962) の現在地

Penn の誘電関数モデルは「半導体で最も広く使われているモデル誘電関数」として現役。
最近の展開:

- **Breckenridge, Shaw, Sher** — Penn モデルが Kramers-Kronig 関係を満たさない問題を修正
- **arXiv:1501.07678 (2015)** — 励起子効果を含む Penn モデルの改良。実部・虚部の新しい表式を導出し、K-K関係を満足
- **Nature Sci. Rep. (2016)** — 2D半導体用の Penn 型モデル誘電関数。基板スクリーニングを含む拡張

### ギャップ（δが入る余地）

| 既存 | 未開拓 |
|------|--------|
| Penn は半導体の ε(q) を「平均ギャップ」1パラメータで記述 | **金属・半導体・絶縁体を横断する統一分類**は行っていない |
| Moss 則 (n⁴E_g = const) は屈折率-ギャップの経験則 | **なぜ**この関係が成り立つかの電子構造的説明がない |
| DFT で個々の物質の ε(ω) は計算可能 | 「何が光り何が光らないか」を**2変数で分類**する枠組みは存在しない |

### 最も近い競合論文

**見つからなかった。** 「optical properties unified framework metal insulator semiconductor classification」で 2020-2025 を検索したが、δ×D_eff に相当する枠組みの論文は**ゼロ**。教科書的な講義資料と個別デバイスの論文のみ。

**判定: Green flag (強い新規性)**

---

## 2. Ewald-Oseen 消滅定理とコヒーレンス

### 現在地

Ewald-Oseen 定理自体は1915-1916年以来確立。最近の展開:

- **Mansuripur (arXiv:1507.05234, 2015)** — 消滅定理の現代的な導出。平面波＋薄膜スライスのアプローチ
- **Cademix (2025)** — 消滅定理の簡略化された解説。教育目的

### ギャップ（δが入る余地）

| 既存 | 未開拓 |
|------|--------|
| 反射は媒質内の誘起双極子の集団的応答として理解されている | 「**どの程度**集団的なら光るか」の定量的基準がない |
| Drude: 自由電子密度 → プラズマ振動数 → 反射率 | 「自由」の定義が曖昧。バンドギャップ = 0 なのに黒い物質（グラファイト）を説明できない |
| Ewald-Oseen は誘電体/金属の両方に適用可能 | **電子非局在化の度合い**と**コヒーレント反射の閾値**の接続は誰もやっていない |

### 最も近い競合

**Physics Forums の質問 (2017)**: "Why does specular reflection occur in metals?" — 回答はすべて Drude/プラズマ振動数レベル。電子非局在化の観点での回答はゼロ。

**判定: Green flag（未開拓だが、直接検証がないことは弱点でもある）**

---

## 3. Miedema の n_ws の電子構造的起源

### 現在地

Miedema モデルは合金熱力学で現役。最近の展開:

- **Nature Sci. Rep. (2017)** — ML で Miedema の分類精度を検証。95%の合意
- **Nature Commun. (2025)** — 単純な電気陰性度ベースのモデルで安定化合物を予測。Miedema 的アプローチの現代版
- **ML 表面エネルギー予測 (2021)** — ガウス過程回帰で金属の表面エネルギーを予測。物理化学的プロパティとの統計的関係

### n_ws の物理的解釈の現状

Miedema 自身の説明:
> 「異なるセルが接触すると、境界の電子密度不連続を解消する必要がある。これは運動エネルギー的なコストを伴う。」

**しかし**: n_ws が**なぜ金属ごとに異なるか**の電子構造的説明（sp vs d の局在化）は、Miedema 自身も、その後の文献でも、**明示的には行われていない**。

### ギャップ（δが入る余地）

| 既存 | 未開拓 |
|------|--------|
| n_ws は Miedema でタブレートされている | n_ws の**起源**（なぜ Al > Zn か）の電子構造的説明がない |
| ML で表面エネルギーを予測するモデルはある | ML descriptor は数値的。**物理的洞察**（sp/d 非局在化）を提供しない |
| d-band center は吸着エネルギーを予測する | d-band center は**表面エネルギー**には適用されていない |

**判定: Green flag（明確な空白）**

---

## 4. ELF / IPR / Wannier spread と表面張力

### ELF + 表面

- **Vitos et al. (2000)** — Al 表面の ELF。バルクは jellium 的、表面はパッキング依存
- 結合解析に使われるが、**表面張力との定量的接続はゼロ**

### IPR + 表面張力

**検索結果: ゼロ。** "inverse participation ratio" AND "surface tension" で論文が見つからない。

### Wannier spread + 表面張力

**検索結果: ゼロ。** "Wannier spread" AND "surface tension" で論文が見つからない。

### 最も近い関連論文（要注意）

- **Halas, Durakiewicz & Joyce (2002)**: "Surface energy calculation – metals with 1 and 2 delocalized electrons per atom"
  - Sommerfeld自由電子モデルでSEをr_sの関数として導出。s-block金属で良い一致
  - 「非局在化電子」= 原子あたりの自由電子の**整数カウント**（Na=1, Mg=2）
  - **IPR, ELF, Wannier spreadなど局在化指標は一切使用していない**
  - 遷移金属には原理的に適用不可（d電子の部分的局在化を扱えない）
  - → **引用は必要だが、我々の連続的δとは本質的に異なる**

**判定: Strong green flag（空白地帯を確認。Halas 2002は整数カウントで我々の連続的δとは別物）**

---

## 5. 総合判定

### 新規性マップ

```
                        既存研究の密度
                    高い ←————————→ 低い（新規性が高い）
                     |                    |
Paper 1:             |                    |
  δ×D_eff分類        |              ●     |  ← 統一分類は未開拓
  コヒーレンス仮説   |            ●       |  ← 定性的議論はあるが定量化なし
  Penn との差分       |        ●           |  ← Penn は半導体のみ、差分は明確
                     |                    |
Paper 2:             |                    |
  n_ws の起源        |              ●     |  ← 誰も電子構造から説明していない
  ELF + γ            |                ●   |  ← ELF は結合分析のみ
  IPR + γ            |                  ● |  ← 完全に空白
  Wannier + γ        |                  ● |  ← 完全に空白
                     |                    |
```

### 要精読論文（最重要3本）

1. **Penn (1962)** — Paper 1 の最大の先行研究。δ×D_eff が Penn を**包含する**ことを示す必要がある
2. **"Surface energy with delocalized electrons" (2002)** — Paper 2 の主張に最も近い。引用して差分を明確にすべき
3. **Vitos et al. (2000) "Electron localization at metal surfaces"** — ELF で金属表面を分析。我々の valence decomposition との関連

### 要注意: 見つかっていない可能性

上記の検索はウェブ検索ベース。Google Scholar での追加検索を推奨:
- `"participation ratio" "surface energy"` （引用符付き完全一致）
- `"Wannier" "surface tension"` （引用符付き完全一致）
- `"delocalization" "surface tension" metal`

これらで**ゼロ**が確認できれば、新規性の主張はかなり強い。

---

## 参考リンク

### Penn モデル関連
- [Penn 1962 original](https://link.aps.org/doi/10.1103/PhysRev.128.2093)
- [Penn model with excitons (2015)](https://arxiv.org/abs/1501.07678)
- [2D semiconductor model dielectric (2016)](https://www.nature.com/articles/srep39844)

### Ewald-Oseen 関連
- [Mansuripur (2015)](https://arxiv.org/pdf/1507.05234)
- [Wikipedia](https://en.wikipedia.org/wiki/Ewald%E2%80%93Oseen_extinction_theorem)
- [Ballenegger (1999) extinction lengths](https://aapt.scitation.org/doi/10.1119/1.19330)

### Miedema / 表面エネルギー関連
- [Miedema model Wikipedia](https://en.wikipedia.org/wiki/Miedema's_model)
- [ML surface energy (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0254058421004053)
- [Nature Commun. electronegativity model (2025)](https://www.nature.com/articles/s41467-025-67658-9)
- [ML in surfaces and interfaces review (2025)](https://pubs.aip.org/aip/cpr/article/6/1/011309/3339760)

### ELF / 局在化 関連
- [Electron localization at metal surfaces (2000)](https://www.sciencedirect.com/science/article/abs/pii/S0039602800000571)
- [Surface energy with delocalized electrons (2002)](https://www.sciencedirect.com/science/article/abs/pii/S0301010402003798)
