# sento-optics 文献サーベイ結果

サーベイ実施日: 2026-07-04（初版）/ 2026-07-05 独立再検証で改訂  
検索: arXiv API / Crossref API（OpenAlex はキー未設定のため不使用、Semantic Scholar はレート制限で部分的）  
対象: Paper 1（光学分類）/ Paper 2.1（表面張力）/ Paper 3（液体の定義）の各新規性主張

---

## 判定サマリ

| 論文 | 中核の新規性主張 | サーベイ判定 | 根拠 |
|------|------------------|--------------|------|
| **Paper 3** | Wannier spread Ω で「液体」を定義 | 🟢 **強い新規性（直接競合なし）** | 「MLWF × liquid」は液体Siの分光・双極子計算ばかり。Ω を相の**定義**に使う論文は arXiv/Crossref に不在 |
| **Paper 1** | δ × D_eff で光学カテゴリを横断分類 | 🟢 **新規性あり（要監視）** | 炭素同素体の光学は個別研究多数だが、金属/半導体/絶縁体を跨ぐ2変数分類の枠組みは見当たらず。2026年に記述子ベース分類論文が増加傾向 |
| **Paper 2.1** | Miedema n_ws の起源＝価電子非局在化 | 🟡 **新規性あるが先行文脈が濃い** | Williams-Gelatt-Moruzzi (1980) が実在の直接的問いの出所。表面張力×電子密度は1978年以降の蓄積が厚く、位置づけを丁寧に |

---

## Paper 3: 液体の Wannier-spread 定義 — 最も強い新規性

「Wannier spread で液体を定義した論文はゼロ」という著者の 2026-04-01 時点の主張は、**今回の独立サーベイでも支持された**。

- `MLWF AND liquid` でヒットするのは、液体水の赤外スペクトル計算、双極子モーメントの機械学習、液体Siの共有結合ダイナミクス — いずれも **Ω を分析ツールとして使う**もので、**相の定義変数として使う**ものではない。
- 最近接の先行研究 **Remsing & Klein (2020) は実在を確認**: "Molecular Simulation of Covalent Bond Dynamics in Liquid Silicon", *J. Phys. Chem. B* — DOI: 10.1021/acs.jpcb.0c01798（7被引用）。液体Siの MLWF 分類はやっているが、Ω 総量の固液比較や「液体の定義」への昇華はしていない — 著者の位置づけ（memo_remsing_klein_liquid_si.md）と整合。
  - **訂正（2026-07-05 再検証）**: 本レポート初版で「PRL 2020, 30 cites」としたのは誤帰属。その PRL は Dharma-wardana, Klug & Remsing "Liquid-liquid Phase Transitions in Silicon"（別論文, Physical Review Letters, 30被引用 — DOI は未取得のため引用時に要確認）。Remsing & Klein 本体は上記 JPCB 論文。
- **確認済み（2026-07-05 再検証で解決）**: Cardenas-Castillo 型総和則の出典は **Cárdenas-Castillo, Zhang, Freire & Kochan, "Detecting the spread of valence-band Wannier functions by optical sum rules", Phys. Rev. B 110, 075203 (2024)** — DOI: 10.1103/physrevb.110.075203（10被引用）。実在を著者名検索で確認。方向は「光学スペクトル→Ω の検出」であり、sento の「Ω→光学の予測」とは逆向き — memo の位置づけどおり。なお 2024年の PRB が既に10被引用という事実は、Ω↔光学接続が**温まりつつある領域**であることを示す（Paper 3 を急ぐ根拠が1つ増えた）。
- **追加ギャップ確認（2026-07-05）**: 最も確立された既存の非局在化記述子である **ELF（electron localization function）**についても `ELF × liquid metal` / `ELF × surface energy` を arXiv で検索 — ヒットゼロ。既存記述子側からも sento の空白地帯が侵食されていないことを確認。`Wannier × melting × spread` もゼロ（融解での Ω ジャンプというテスト3の角度は完全に空白）。

**含意**: Paper 3 は3本の中で最も「誰もやっていない」度が高い。ただし新規性は**応用**にあり（Ω 自体は Marzari-Vanderbilt 1997 の既存量）、査読で「何が新しいか」を問われたら「Ω を液体の定義に使った初の試み」と即答できる準備が要る — 戦略メモの認識どおり。

## Paper 1: バンドギャップを超える光学分類

- `carbon allotropes optical properties electronic structure` では個別同素体の光学研究（2015年の新規炭素同素体の電子・光学特性など）はあるが、**δ × D_eff に相当する横断的2変数分類フレームは不在**。
- 注意信号: 2026年に「記述子ベースの界面電子カップリング分類」「ドメイン直接バンドギャップの分類」など、**記述子で物性をカテゴリ分けする論文が増えている**。方法論的トレンドが sento に近づいており、投稿は早いほど有利。
- `effective dimensionality AND optical response` は arXiv でヒットゼロ — D_eff という切り口自体はまだ空白地帯。

## Paper 2.1: Miedema n_ws の物理的起源

- 直接の問いの出所 **Williams, Gelatt & Moruzzi (1980, PRL "Microscopic Basis of Miedema's Empirical Theory", 139 cites)** は実在を確認。関連の Gelatt-Williams-Moruzzi (1983, PRB, 390 cites) も存在。sento の「45年前の問いへの回答」という枠組みは史実に基づく。
- ただし `surface tension + electron density + liquid metals` は **1978年以降の蓄積が厚い**（Int. J. Mater. 1978 ほか）。ここは「未開拓」ではなく「古典的問題への新解釈」として位置づけるのが安全。
- `Wannier AND surface energy AND metal` や `IPR surface energy` は arXiv でほぼ空白 — **δ_IPR / Wannier spread を表面エネルギーの起源に結びつける角度は新しい**。固体sp/d の実証（p=0.00008）と組み合わせれば差別化できる。

---

## サーベイの限界（正直な記載）

- **OpenAlex 未使用**: API キー未設定のため、被引用ネットワーク解析はできていない。設定すれば競合の網羅性が上がる。
- **Semantic Scholar 部分的**: レート制限（HTTP 429）で 2024–2026 のスクープ・リスク検索が未完。特に Paper 1 の「記述子ベース分類」トレンドは、後日 S2/OpenAlex で追跡する価値あり。
- **arXiv 依存**: Paper 2 系の材料科学は arXiv 収録が薄く、Crossref で補ったが古い文献が中心。ECOSS/材料系ジャーナルの直近号は手動確認が望ましい。

## 推奨アクション

1. **Paper 3 を優先的に前進**（新規性が最も明確、ただし液体AIMDの実証が必須 — 中断中の液体Na計算をリモートに載せる価値が高い）。
2. **Paper 1 は投稿を急ぐ**（記述子ベース分類の方法論トレンドが接近中）。
3. **Paper 2.1 は「古典問題への電子構造的新解釈」フレーム**で、Williams(1980)への回答という史的文脈を前面に。
4. OpenAlex キーを設定できれば、被引用解析でスクープ・リスクを定量化できる。
