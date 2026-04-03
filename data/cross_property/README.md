# Cross-Property Correlation: R vs γ（予備的文献データ分析）

**Status: 2026-04-03。文献データによる予備的検証。直接測定値ではない推定を含む。**

## 目的

δ枠組みの独自予言「Rとγは同じδ_elecに支配されるため相関するはず」を
文献データで検証する。R vs γ の直接相関を示した先行研究は見つかっていない。

## 結果

### 全元素（13金属）
- Pearson r = −0.53, p = 0.06（**負の相関**）
- 素朴な予言（R ∝ γ）は棄却

### NaK合金（sp金属のみ — コントロール）
- Pearson r = **+0.97**, p = 0.0001
- sp内ではδ_elec ↑ → R ↑ かつ γ ↑

### CuZn合金（sp-d混合 — 軌道遷移テスト）
- Pearson r = **−0.85**, p = 0.008（500nm）
- d電子のinterband吸収がRを下げつつ、n_wsを上げてγを維持

### 解釈
**符号の反転（NaK: +0.97 → CuZn: −0.85）が「軌道遷移=ミクロ相転移」の定量的証拠。**
ただしCuZnのR値は文献からの推定であり、直接測定値ではない。

## 注意

- NaKのR変動幅は0.982→0.984と極めて小さい（ランキング一致は完璧だが絶対変化量が小さい）
- CuZnのγはButler模型推定、Rは複数文献からの推定値。定性的符号反転は堅いが定量的信頼性は低い
- 直接測定による確認が必要

## ファイル

- `reflectivity_surface_tension.py` — 全元素 R vs γ 分析
- `R_vs_gamma.png` — 全元素スキャッタープロット
- `nak_cross_property.py` — NaK合金 Drude計算
- `NaK_R_vs_gamma.png` — NaK R vs γ プロット
- `cuzn_cross_property.py` — CuZn合金分析
- `NaK_vs_CuZn_comparison.png` — NaK/CuZn比較図

## 関連メモ

- `theory/connections/memo_orbital_micro_phase_transition.md` — 軌道遷移=ミクロ相転移仮説
