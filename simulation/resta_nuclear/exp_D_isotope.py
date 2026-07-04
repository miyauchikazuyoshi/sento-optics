"""
実験D: 同位体プローブ — 融点シフトから非局在性の量子成分を較正する

背景 (memo_delocalization_as_primary_variable.md §3):
  δ_nuc = δ_cl(T) + ゼロ点成分。ゼロ点は 1/√M_eff、古典項は質量非依存
  （equipartition で Mω² = k）。よって同位体置換は量子成分だけを動かすノブ。

モデル（1パラメータ較正）:
  融解条件: δ_c = A·T_m + B/√M_eff
  同位体対から B/A を逆算 → ゼロ点寄与率 f_ZP = (B/√M_l)/(A·T_m + B/√M_l)

事前判定基準:
  D1: 全系で ΔT_m > 0（重い同位体ほど高融点 — ゼロ点が融解を助ける向き）
  D2: 抽出した f_ZP が物理的範囲 (0-100%) で、量子性の強い系ほど大きい
      （de Boer Λ* の序列 H2 > Ne > 重い系 と単調）
  D3: H2O/D2O の表面張力: 絶対温度比較では素朴予測と逆符号でも、
      対応状態 (Guggenheim) 補正後に「D2O の方が凝集的」が回復する

注意（誠実さ）: 同位体効果の NQE 解釈自体は確立分野（de Boer 1948 対応状態、
Markland-Ceriotti 系）。ここでの新規性は発見ではなく「δ 言語の較正」。
文献値は CRC/NIST/IAPWS 系の代表値 — 論文使用前に一次出典で要再確認。
"""
import json
import numpy as np

# (系, T_m_light [K], T_m_heavy [K], M_light, M_heavy, 量子性メモ)
SYSTEMS = [
    # H2/D2: 三重点 (NIST)。de Boer Λ*: H2 1.73, D2 1.22 — 最強の量子固体系
    ("H2/D2",           13.96, 18.73,  2.0,  4.0, "Λ*(H2)=1.73"),
    # Ne-20/Ne-22: 三重点差 ~0.15 K (要文献確認: Furukawa 1972 系)
    ("Ne20/Ne22",       24.54, 24.69, 20.0, 22.0, "Λ*(Ne)=0.59"),
    # H2O/D2O: 融点 (CRC)。M_eff はライブレーション解釈 (H/D 質量)
    ("H2O/D2O (libr.)", 273.15, 276.97, 1.0, 2.0, "libration ~600 cm⁻¹"),
    # 同、並進解釈 (分子質量)
    ("H2O/D2O (transl.)", 273.15, 276.97, 18.0, 20.0, "transl. ~50-200 cm⁻¹"),
]

print("=== 実験D: 融点同位体シフト → ゼロ点寄与率 f_ZP の較正 ===\n")
print(f"{'系':<20} {'ΔT_m (K)':>9} {'ΔT/T':>7} {'B/A (K)':>9} {'f_ZP':>7}")
res = {}
d1 = True
fzps = []
for name, tl, th, ml, mh, note in SYSTEMS:
    dT = th - tl
    d1 &= dT > 0
    denom = 1 / np.sqrt(ml) - 1 / np.sqrt(mh)
    BA = dT / denom
    fzp = (BA / np.sqrt(ml)) / (tl + BA / np.sqrt(ml))
    fzps.append((name, fzp, note))
    print(f"{name:<20} {dT:>9.2f} {dT/tl:>6.1%} {BA:>9.2f} {fzp:>7.1%}   ({note})")
    res[name] = {"Tm_light_K": tl, "Tm_heavy_K": th, "dT_K": dT,
                 "M_light": ml, "M_heavy": mh, "B_over_A_K": BA,
                 "f_ZP": fzp, "note": note}

# D2: 量子性の序列と f_ZP の単調性（libration 解釈を水の代表とする）
f_h2 = res["H2/D2"]["f_ZP"]
f_ne = res["Ne20/Ne22"]["f_ZP"]
f_w = res["H2O/D2O (libr.)"]["f_ZP"]
d2 = (0 < f_w < f_ne < f_h2 < 1)
print(f"\nD2 単調性: H2 {f_h2:.0%} > Ne {f_ne:.0%} > H2O(libr.) {f_w:.0%} "
      f"→ {'PASS' if d2 else 'FAIL'}")
print("  （H2 の融解は過半がゼロ点駆動 = de Boer の量子固体描像と整合。")
print("   水は ~5%(libration解釈)〜21%(並進解釈) — どの質量が効くかは")
print("   HDO や同位体熱容量で判別可能、Paper 4 の設計対象）")

# ---------- D3: 表面張力の符号チェック ----------
# γ(25°C): H2O 71.98, D2O 71.87 mN/m (IAPWS/Vinš 系の代表値)
# T_c: H2O 647.10 K, D2O 643.85 K
g_h, g_d = 71.98, 71.87
tc_h, tc_d = 647.10, 643.85
T = 298.15
mu = 1.256  # Guggenheim-Katayama 指数
tau_h, tau_d = 1 - T / tc_h, 1 - T / tc_d
g0_h = g_h / tau_h ** mu
g0_d = g_d / tau_d ** mu
print(f"\nD3 表面張力 (25°C):")
print(f"  絶対比較:   γ_D2O − γ_H2O = {g_d - g_h:+.2f} mN/m "
      f"({(g_d-g_h)/g_h:+.2%}) ← 素朴予測(D2O凝集↑)と逆符号")
print(f"  対応状態:   γ = γ0(1−T/Tc)^{mu}, Tc_D2O={tc_d} < Tc_H2O={tc_h}")
print(f"  補正後 γ0:  H2O {g0_h:.1f}, D2O {g0_d:.1f} → γ0_D2O/γ0_H2O − 1 = "
      f"{g0_d/g0_h - 1:+.2%}")
d3 = g0_d > g0_h
print(f"  → 対応状態では『D2O の方が凝集的に強い』が回復（符号整合）: "
      f"{'PASS' if d3 else 'FAIL'}")
print("  （絶対温度比較の逆符号は Tc の同位体差 (D2O が低い) の反映。")
print("   ゼロ点寄与 ~数% と γ0 差 ~0.4% はオーダー整合の範囲）")

print(f"\n=== 判定: D1 {'PASS' if d1 else 'FAIL'} / "
      f"D2 {'PASS' if d2 else 'FAIL'} / D3 {'PASS' if d3 else 'FAIL'} ===")

with open("exp_D_results.json", "w") as f:
    json.dump({"meta": {"date": "2026-07-05",
                        "model": "delta_c = A*T_m + B/sqrt(M_eff)",
                        "caveat": "literature values need primary-source check"},
               "systems": res,
               "surface_tension": {"gamma_H2O": g_h, "gamma_D2O": g_d,
                                   "Tc_H2O": tc_h, "Tc_D2O": tc_d,
                                   "gamma0_H2O": g0_h, "gamma0_D2O": g0_d,
                                   "corresponding_states_ratio": g0_d / g0_h - 1},
               "verdict": {"D1": bool(d1), "D2": bool(d2), "D3": bool(d3)}},
              f, indent=2, ensure_ascii=False)
print("保存: exp_D_results.json")

# 図: f_ZP 系列
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6.5, 4))
names = [n for n, _, _ in fzps]
vals = [f * 100 for _, f, _ in fzps]
colors = ["tab:red", "tab:orange", "tab:blue", "tab:cyan"]
ax.barh(names, vals, color=colors)
for i, v in enumerate(vals):
    ax.text(v + 1, i, f"{v:.1f}%", va="center")
ax.set_xlabel("zero-point fraction of nuclear delocalization at melting  f$_{ZP}$  (%)")
ax.set_title("Isotope shift calibration (Exp. D)")
ax.set_xlim(0, 70)
fig.tight_layout()
fig.savefig("exp_D_isotope.png", dpi=150)
print("保存: exp_D_isotope.png")
