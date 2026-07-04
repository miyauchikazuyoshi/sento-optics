# Kohn–Resta–SWM 系譜: 欠落していた理論的祖先と5つの気付き

**Status: 2026-07-04。Claude (Fable 5) との議論に基づく。同日 Claude が原典を精読し検証済み（Resta & Sorella 1999 全文 / SWM 2000 pp. 1–3, 7–11 / Resta 2011 レビュー冒頭）。式は原典の式番号つきで確認。Kohn 1964 本文のみ二次資料（SWM Intro, Resta 2011 Intro）経由 — 検証結果は §6。**

---

## 0. 発見: 系譜の欠落

リポジトリ全体（.bib / .tex / .md）を検索した結果、以下が未引用と確認（2026-07-04）:

| 論文 | 内容 | リンク | 状態 |
|------|------|--------|------|
| Kohn (1964) Phys. Rev. 133, A171 | "Theory of the Insulating State" — 局在で相を定義するプログラムの原点 | [DOI](https://doi.org/10.1103/PhysRev.133.A171) | 未引用 |
| Resta & Sorella (1999) PRL 82, 370 | 周期系の局在長 λ²。絶縁体で有限、**金属で発散** | [arXiv](https://arxiv.org/abs/cond-mat/9808151) / [DOI](https://doi.org/10.1103/PhysRevLett.82.370) | 未引用 |
| Souza, Wilkens & Martin (2000) PRB 62, 1666 | 局在テンソル ⟨r²⟩_c と σ(ω) を結ぶ sum rule | [arXiv](https://arxiv.org/abs/cond-mat/9911007) / [DOI](https://doi.org/10.1103/PhysRevB.62.1666) | 未引用 |
| Resta (2002) J. Phys.: Condens. Matter 14, R625 | レビュー: 機構横断の絶縁性理論 | [DOI](https://doi.org/10.1088/0953-8984/14/20/201)（ペイウォール） | 未引用 |
| Resta (2011) "The Insulating State of Matter: A Geometrical Theory" | 幾何学的定式化のレビュー。2002 の後継で **arXiv で全文入手可** | [arXiv](https://arxiv.org/abs/1012.5776) | 未引用 |
| Sgiarovello, Peressi & Resta (2001) PRB 64, 115202 | λ² の結晶半導体への実計算（応用編） | [arXiv](https://arxiv.org/abs/cond-mat/0101440) | 未引用 |

（Resta は De Santis & Resta 2000（Al 表面の ELF）のみ引用済み — 別系統の仕事）

### なぜ重大か

1. **系譜**: Kohn 1964 は「電子の局在性で相（金属/絶縁体）を定義する」プログラムの原点であり、δ_elec はその直系。引けば「正統な系譜の液体への拡張」、引かなければ「孤立した思いつき」に見える。
2. **優先権**: Cardenas-Castillo (2024) の sum rule は SWM (2000) の系譜（バンド分解版）。「δ→光学が定理になった」（memo_literature_and_sum_rule.md）の定理は実質 2000 年から存在する。Vanderbilt / Resta 学派の査読者は一目で気づく。Paper 1/3 では SWM を先に引き、Cardenas-Castillo は「バンド分解・現代版」として位置づけ直す。
3. **物理**: **Resta の局在長は金属で発散する。それが金属の定義そのもの。** 液体 Na（金属）の Ω は熱力学極限で収束せず、有限セル・Γ点 AIMD で得る値はセルサイズの関数になる。一方、水（絶縁体）の Ω は有限に収束する。「液体金属 vs 水で δ_elec の大小を比較」は厳密には「発散量 vs 収束量」の比較。**memo_delta_threats_and_limits.md の6脅威のどれより大きい脅威が、脅威リストに載っていなかった（脅威0と呼ぶ）。**

### 危険であり機会

「金属で Ω 発散」はバグではなく足場にできる: **δ_elec の発散＝金属性、有限＝絶縁性**という厳密な区別として枠組みの中心に据える（→ §3 の2枚看板）。

**具体的アクション**: AIMD 計画（simulation/surface_tension/aimd/RESUME_STATE.md）に「64 vs 128/216 原子で Ω のサイズスケーリングを測る」を最優先チェック項目として追加する。

---

## 1. 気付き①: 相の定義は「配置空間の幾何」にある（Kohn 1964）

Kohn の核心: 絶縁体と金属の違いはギャップや励起スペクトルではなく、基底状態波動関数が**多体配置空間で切断（disconnected）されているか連結か**にある。

これは電子に限った話ではない:

- 固体 = 核系が配置空間の一つの盆地（Stillinger の inherent structure）に閉じ込められている = **切断**
- 液体 = 盆地間をエルゴード的に渡り歩く = **連結**

**効果**: δ_elec と δ_nuc が「実空間分布の2次モーメント」という類推（memo_liquid_definition_via_omega.md）を超えて、**同一概念（配置空間の局在/非局在）の電子版と核版**になる。「Resta 軸 × Lindemann 軸の直積」という言い方（memo_liquid_definition_gap_defense.md §4）よりさらに強く、「同じ定義の2つの実現」と書ける。Paper 3 Introduction の格が一段上がる。

---

## 2. 気付き②: 核の Resta 位相（→ 独立メモ）

Resta & Sorella の位相量 z を核位置に適用すると、時間窓に依存しない静的な「固体/非固体」指標が定義でき、Debye-Waller 因子・Bragg ピーク消失と直結する。Paper 3 の方法論の柱になりうるため独立メモに展開:

→ **memo_nuclear_resta_phase.md**

---

## 3. 気付き③: 金属では「発散の速さ」が記述子 — δ_elec の2枚看板化（SWM 2000）

SWM の fluctuation-dissipation sum rule（**原典確認済み**、SWM Eq. 30 + 49。σ̄ は twisted 境界条件平均）:

```
ξ_i² ≡ lim_{N→∞} (1/N)⟨ΔX_i²⟩ = (ℏ / π e² n₀) ∫₀^∞ (dω/ω) Re σ̄_ii(ω)     [n₀ = N/V]
```

**(a) 「光沢 = 電子局在長の発散」という恒等式的な言い換えが書ける。**
金属光沢 ⇔ 低周波スペクトル重み（σ(ω→0) > 0） ⇔ ∫σ/ω の対数発散 ⇔ ξ² 発散。
Paper 1 の「δ 高 → 光沢」が相関ではなく恒等式のレベルになる。銭湯の原観察は「局在長の発散が可視域下端までスペクトル重みを押し出す現象」と書き直せる。

**(b) 金属側の正しい記述子（精読で修正）。** SWM Eq. 50 は T=0 の固体を3分類する:

```
絶縁体:     lim_{ω→0} Re σ(ω) = 0                       → ξ 有限
理想導体:   Re σ(ω) = (2πe²/ℏ²) D δ(ω) + σ_reg(ω)       → D = Drude weight
非理想導体: lim_{ω→0} Re σ(ω) = σ₀（散乱で δ(ω) がローレンツ化、D=0） → ξ 発散（対数）
```

**散乱だらけの実在の液体金属は「非理想導体」であり、Drude weight はゼロ。物質固有の情報は dc 伝導度 σ₀ が担う。** よって2枚看板は:

| 液体の種類 | 正しい記述子 | 例 |
|----------|------------|-----|
| 絶縁性液体 | ξ²（有限値） | H₂O, EtOH |
| 金属性液体 | dc 伝導度 σ₀（ξ² の対数発散の源） | Na, Al, Hg |

これは枠組みにとって朗報: **液体金属の σ₀ は実測データが豊富**で、Hg の金属-非金属転移はまさに σ₀ で追跡されてきた（Hensel — memo_delta_threats_and_limits.md 脅威5-6）。転移は「σ₀ → 0 かつ ξ² が有限化する点」として2枚看板の切り替わりそのもの。Ω の有限サイズ依存（脅威0）も「発散を σ₀ で読む」ことで欠陥から物理に変わる。SWM 自身が「Drude weight 単独では絶縁体/導体の普遍的判定にならず、ξ との併用で3分類できる」と明記している。

---

## 4. 気付き④: 機構非依存は欠陥ではなく特徴（Resta 2002）

memo_delta_threats_and_limits.md の脅威2「δ は Anderson 型と Mott 型を区別できない」は limitation として書く方針だった。しかし Resta 理論の存在意義そのものが「バンド絶縁体・Anderson 絶縁体・Mott 絶縁体を、**機構によらず**基底状態の局在という単一の幾何的性質で統一する」ことにある。

**機構非依存性は Kohn–Resta プログラムの誇るべき特徴であり、δ はそれを正統に継承している。** 脅威リストから strengths へ移動できる。

---

## 5. 気付き⑤: Wannier 最小化は不要かもしれない（MV97 の Ω_I 再読）

Marzari & Vanderbilt (1997) の分解 Ω = Ω_I + Ω̃ で、sum rule に現れるのはゲージ不変部分 Ω_I のみ。Ω_I は quantum metric の BZ 積分であり、**Wannier 化（最小化ループ）なしに Bloch / Kohn-Sham 状態から直接計算できる**。

AIMD の各スナップショットに対して Wannier90 の最小化を回す代わりに、Γ点での quantum metric 評価で済む可能性がある。メモリ圧迫で中断した現計算環境（RESUME_STATE.md: swap 56/57 GB）では、後処理コストの削減は死活的に効く。

---

## 6. 原典精読の検証結果（同日追記、Claude 精読）

### 6.1 確認できたこと（式番号つき）

| 主張 | 原典での裏付け |
|------|--------------|
| z_N = ⟨Ψ\|e^{i(2π/L)X̂}\|Ψ⟩, X̂ = Σxᵢ | RS Eq. (10) ✓ |
| λ² = −(L/2π)² ln\|z\|²（単粒子・1D） | RS Eq. (8) ✓ |
| 多体規格化 D = −lim_{N→∞} N ln\|z_N\|²（絶縁体で有限、金属で発散）、λ = √D/(2πn₀) | RS Eq. (11) ✓ |
| λ² = Ω_I/(3m_b) — Resta 局在長と MV の Ω_I の同一性（気付き⑤の根拠） | RS Eq. (18) ✓ |
| 金属で z_N → 0（消失） | RS 本文 ✓ |
| Kohn の「多体配置空間の切断」: 絶縁体の Ψ は disconnected regions R_M に局在する Ψ_M の和 | SWM Intro Eq. (1) 周辺、Resta 2011 Intro ✓ |
| 機構横断性: band / Mott / Anderson / 量子Hall / Chern / topological を統一 | Resta 2011 abstract に明文 ✓（気付き④の裏付け） |
| RS 1999 + SWM 2000 = 「modern theory of the insulating state」の基礎、2002 に初期レビュー | Resta 2011 Intro の歴史記述 ✓ |

### 6.2 修正したこと

- **2枚看板の金属側**: 当初「Drude weight D」と書いたが、SWM Eq. (50) の3分類により、散乱のある実在の液体金属は非理想導体（D = 0、σ₀ 有限）。正しい記述子は **dc 伝導度 σ₀**（§3 は修正済み）。理想導体（散乱なし）の場合のみ D。

### 6.3 新しい気付き（精読の収穫）

**⑥ ξ² ≤ ℏ²/(2m_e E_g)（SWM Eq. 52）— Paper 1 の δ–E_g 逆相関の厳密な根拠。**
Paper 1 は δ と E_g の逆相関（r = −0.86）を経験的相関として示した。SWM はオシレータ強度 sum rule から局在長の**上界**をギャップで縛る不等式を証明済み。Paper 1 の相関は「不等式 Eq. 52 の飽和度の測定」として語り直せる — 経験則から定理の系へ格上げ。

**⑦ λ の方向分解 = D_eff の厳密版（RS 一般化ノート (i)）。**
RS は明文で「グラファイトでは λ は基底面法線方向に有限、面内方向に発散」と書いている。つまり Paper 1 の D_eff（操作的な有効伝導次元）は「**λ が発散する方向の数**」として第一原理的に定義し直せる可能性がある。δ と D_eff の両方が同一の理論（局在テンソル）から出る — 二変数枠組みの統一的基盤。

**⑧ 更なる先行（誠実さのため記録）:**
- Kudinov (1991) Sov. Phys. Solid State 33, 1299 — 双極子揺らぎで絶縁体/導体を区別する発想の先行（RS の ref [16]、SWM も引用）
- Selloni, Carnevali, Car & Parrinello (1987) PRL 59, 823 — z の**位相**で無秩序系中の単一量子粒子（溶融塩中の電子）の断熱時間発展を追跡（RS の ref [6]）。位相量を無秩序・液体系に使った直接の先行 — z_nuc 提案（memo_nuclear_resta_phase.md）の新規性照合に必須

---

## 7. 読む順番（ユーザー精読用・リンクつき）

1. **[Resta (2011) arXiv:1012.5776](https://arxiv.org/abs/1012.5776)** — 全体の地図。arXiv で全文入手可。2002 レビューはペイウォールなのでこちらを推奨
2. **[Resta & Sorella (1999) arXiv:cond-mat/9808151](https://arxiv.org/abs/cond-mat/9808151)** — 5ページの PRL。核版 z_nuc（memo_nuclear_resta_phase.md）の直接の源泉。Eq. (8), (10), (11), (18) が核心
3. **[SWM (2000) arXiv:cond-mat/9911007](https://arxiv.org/abs/cond-mat/9911007)** — 28ページ。最重要は Eq. (30), (49), (50), (52)。Sec. IV–V だけでも可
4. **[Kohn (1964)](https://doi.org/10.1103/PhysRev.133.A171)** — 最後に。技術は古いが、Introduction に書く「哲学の系譜」の源泉

---

## 関連メモ

| メモ | 関係 |
|------|------|
| memo_nuclear_resta_phase.md | 気付き②の展開（δ_nuc の静的再定義・提案） |
| memo_liquid_definition_gap_defense.md | 「液体定義の空白」の防御可能な形 |
| memo_literature_and_sum_rule.md | Cardenas-Castillo の位置づけ — SWM 系譜として要修正 |
| memo_delta_threats_and_limits.md | 脅威2の解消（§4）、脅威0（金属 Ω 発散）の追加（§0） |
| memo_liquid_definition_via_omega.md | Paper 3 の元定義 — 本メモで精密化 |
| positioning_map.md | 統合マップ（§8 系列に本系譜を接続すべき） |

---

*2026-07-04 作成。Claude (Fable 5) との議論より。全ての式・主張は原典精読で検証してから論文に使うこと。*
