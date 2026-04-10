# Paper 2 n_ws修正計画

**日付: 2026-04-09**
**原因: MIEDEMA_NWS辞書がde Boer 1988と不整合。自己レビューで発覚。**

---

## 正しい値（de Boer 1988, Wikipedia/HandWiki cross-verified）

| Elem | 正しい n_ws^{1/3} | 旧辞書の n_ws | 旧辞書から計算した n_ws^{1/3} |
|------|-----------------|-------------|--------------------------|
| Li   | **0.98** | 2.85 | 1.42 |
| Be   | **1.67** | 7.55 | 1.96 |
| Na   | **0.82** | 1.65 | 1.18 |
| Mg   | **1.17** | 3.55 | 1.53 |
| Al   | **1.39** | 5.55 | 1.77 |
| Si   | **1.50** | 6.75 | 1.89 |
| K    | **0.65** | 0.95 | 0.98 |
| Ca   | **0.91** | 2.55 | 1.37 |
| Ti   | **1.52** | 4.25 | 1.62 |
| Fe   | **1.77** | 5.55 | 1.77 |
| Ni   | **1.75** | 5.55 | 1.77 |
| Cu   | **1.47** | 5.55 | 1.77 |
| Zn   | **1.32** | 4.05 | 1.59 |
| Ga   | **1.31** | 5.15 | 1.73 |
| Ag   | **1.36** | 4.35 | 1.63 |

## 正しい相関値

| 相関 | 正しい値 | 現Paper v9の値 |
|------|---------|--------------|
| δ_all vs n_ws^{1/3} | **r = -0.03** | r = 0.14 |
| δ_val vs n_ws^{1/3} | **r = 0.10** | r = 0.26 |
| n_mid(abs) vs n_ws^{1/3} | **r = 0.79** | r = 0.68 |

## 影響範囲

### 修正が必要
- [ ] Paper 2 main.tex: tab:delta_nws のn_ws^{1/3}列（15値全部）
- [ ] Paper 2 main.tex: 相関段落の数値（r=0.14→-0.03, r=0.26→0.10）
- [ ] Paper 2 main.tex: Abstract/Conclusionの主張書き直し
- [ ] Paper 2 main.tex: Discussion「Miedemaの再解釈」節の修正
- [ ] Paper 2 main_ja.tex: 上記と同じ修正を日本語版にも
- [ ] README.md / README_ja.md: Paper 2の記述更新
- [ ] docs/index.html: Paper 2カード
- [ ] simulation/surface_tension/test7_extended.py: MIEDEMA_NWS辞書修正
- [ ] Zenodo: 新バージョンアップロード

### 影響なし（確認済み）
- δ vs midpoint density ratio (r=0.89)
- 14金属スラブ sp/d分離 (p=0.00008)
- Wannier spread (6-19倍)
- Paper 1全体
- Ising RG
- 理論メモ群
- R vs γ cross-property分析

## 主張の修正

### 旧（v9）
> δ_IPRは価電子非局在化のproxy…n_wsとの相関r=0.14…支持する

### 新（v10）
> δ_IPRはsp/d電子構造の均一性を記述する（ratio r=0.89, スラブp=0.00008）。
> しかしδとMiedemaのn_wsは直接には無相関（r=0.10）。
> DFT計算による絶対的な中間点密度はn_wsと強く対応する（r=0.79）。
> δはn_wsの「量的な予測子」ではなく「質的な起源の一部」を説明する。
> Williams (1980)の問いに対しては、sp/d電子構造の均一性差が
> 境界密度差を生む機構を提案するが、定量的な回答ではない。

## 実行手順

1. test7_extended.pyのMIEDEMA_NWS辞書を正しい値に修正
2. Paper 2 EN: テーブル→相関→Abstract→Discussion→Conclusion
3. Paper 2 JA: 同上
4. README EN/JA: Paper 2記述
5. LP: Paper 2カード
6. LaTeXコンパイル
7. commit + push
8. Zenodo新バージョン

予想所要時間: 1-2時間
