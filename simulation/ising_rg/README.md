# Ising RG: δ as RG Flow Variable（予備的数値実験）

**Status: 2026-04-03。予備的な数値実験。結果は promising だが不十分。**

## 目的

2D Ising模型のブロックスピン繰り込み群（RG）変換において、
δ（確率分布のIPR）がRGフロー変数として機能するかを検証する。

## 予測（δ枠組み）

1. T < Tc: δ は粗視化で秩序固定点（δ→1）に流れる
2. T > Tc: δ は粗視化で無秩序固定点（δ→0）に流れる
3. T = Tc: δ はスケール不変（RG固定点）

## 結果（v2, L=64,128）

| テスト | 結果 |
|--------|------|
| フロー方向 | **PASS** — T < Tcで→秩序、T > Tcで→無秩序 |
| L=64 vs L=128 一致 | **PASS** — T ≤ Tcで差 < 0.03（熱平衡化成功） |
| Tcでのスケール不変性 | **未確定** — CV = 0.20-0.23、有限サイズ効果の可能性 |

## 未解決

- L=256以上でTcのδスケール不変性を確認する必要あり
- δのRG固定点値（もし存在すれば）の数値的同定
- 臨界指数との関係

## ファイル

- `ising_rg_delta_v2.py` — シミュレーションコード
- `ising_rg_results.json` — 生データ（L=64,128 × 10温度点 × 80サンプル）
- `ising_rg_delta_v2.png` — δフロー図

## 使い方

```bash
# 標準（~15分）
python ising_rg_delta_v2.py --max-L 128 --n-samples 80

# フル（数時間、L=256）
python ising_rg_delta_v2.py --max-L 256 --n-samples 200 --n-therm-factor 50
```

## 関連メモ

- `theory/connections/memo_pauli_rg_unification.md` — Pauli + RG によるδの階層的統一（未検証）
