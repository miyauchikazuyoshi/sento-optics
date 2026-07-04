"""
実験C: SWM 不等式 ξ² ≤ ℏ²/(2m_e E_g) の飽和度マップ

背景 (memo_kohn_resta_swm_lineage.md §6.3 気付き⑥):
  SWM (2000) Eq. 52 は局在長の上界を光学ギャップで縛る。
  Paper 1 の δ-E_g 逆相関 (r=-0.86) は、この不等式の「飽和度」の
  系統性として定理の言葉で書き直せるはず。

データ:
  Ω/WF: simulation/wannier_carbon/README.md (2026-04-01, DFT+Wannier90)
  E_g:  実験値（間接・直接の両方で評価。SWM の導出は光学吸収の
        閾値なので、フォノン援用を無視すれば直接ギャップが原典に忠実）

換算 (RS 1999 Eq. 18, 立方晶):
  λ²_xx = Ω_I/(3 m_b)。MLWF 最小化後の絶縁体では Ω_total ≈ Ω_I とみなし
  ξ²_xx ≈ (Ω_total/num_wann)/3 = (Ω/WF)/3
"""
import json

HBAR2_2ME = 3.8100  # eV·Å²

# system: (Ω/WF [Å²], E_g indirect [eV], E_g direct [eV])
DATA = {
    "Diamond":  (0.954, 5.47, 7.3),
    "Si":       (3.049, 1.12, 3.4),
    "Ge":       (2.275, 0.66, 0.80),
    "Graphite": (6.375, 0.0, 0.0),   # semimetal: 上界∞、不等式は自明
    "K":        (3.748, 0.0, 0.0),   # metal: 同上
}

print("=== 実験C: SWM Eq. 52 飽和度マップ ===")
print(f"ξ²_xx ≈ (Ω/WF)/3,  上界 = ℏ²/2m_eE_g = {HBAR2_2ME}/E_g [Å²]")
print(f"\n{'System':<10} {'ξ²_xx':>7} {'E_g^ind':>8} {'E_g^dir':>8} "
      f"{'上界(dir)':>10} {'飽和度(ind)':>11} {'飽和度(dir)':>11}")
results = {}
for name, (om, egi, egd) in DATA.items():
    xi2 = om / 3
    if egd > 0:
        bound_d = HBAR2_2ME / egd
        s_ind = xi2 * egi / HBAR2_2ME
        s_dir = xi2 * egd / HBAR2_2ME
        ok = "✓" if s_dir <= 1 else "✗ 破れ!"
        print(f"{name:<10} {xi2:>7.3f} {egi:>8.2f} {egd:>8.2f} "
              f"{bound_d:>10.3f} {s_ind:>11.3f} {s_dir:>11.3f}  {ok}")
        results[name] = {"xi2_xx_A2": xi2, "Eg_indirect_eV": egi,
                         "Eg_direct_eV": egd, "saturation_indirect": s_ind,
                         "saturation_direct": s_dir, "inequality_holds": s_dir <= 1}
    else:
        print(f"{name:<10} {xi2:>7.3f} {'0 (metal)':>8} {'—':>8} "
              f"{'∞':>10} {'0 (自明)':>11} {'—':>11}")
        results[name] = {"xi2_xx_A2": xi2, "Eg_eV": 0,
                         "note": "metal/semimetal: bound is infinite, inequality trivially holds"}

print("""
解釈:
- 全ての絶縁体・半導体で不等式が成立していれば、Paper 1 の Ω 計算は
  SWM の定理と整合（サニティチェック）。
- 飽和度 s の序列に系統性（例: d 遮蔽の強い Ge で低い）があれば、
  s 自体が新しい記述子候補になる（どこまでギャップ律速か、の測度）。
- 金属側で上界が消えることは「ξ² 発散 = 金属」（脅威0）の言い換え。
""")

with open("exp_C_results.json", "w") as f:
    json.dump({"meta": {"date": "2026-07-04",
                        "formula": "s = xi2_xx * Eg / (hbar^2/2m_e); xi2_xx = (Omega/WF)/3",
                        "hbar2_2me_eVA2": HBAR2_2ME,
                        "omega_source": "simulation/wannier_carbon/README.md"},
               "results": results}, f, indent=2, ensure_ascii=False)
print("保存: exp_C_results.json")

# 図: ξ² vs 上界（両対数、y=x が不等式の境界）
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.5, 5))
for name, (om, egi, egd) in DATA.items():
    if egd > 0:
        ax.scatter(HBAR2_2ME / egd, om / 3, s=60, zorder=3)
        ax.annotate(name, (HBAR2_2ME / egd, om / 3),
                    textcoords="offset points", xytext=(8, 4))
lims = [0.1, 10]
ax.plot(lims, lims, "k--", label="ξ² = ℏ²/2m$_e$E$_g$ (SWM Eq. 52 bound)")
ax.fill_between(lims, lims, [lims[1]] * 2, alpha=0.12, color="red",
                label="forbidden")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("ℏ²/2m$_e$E$_g^{dir}$  (Å²)")
ax.set_ylabel("ξ²$_{xx}$ = (Ω/WF)/3  (Å²)")
ax.set_title("SWM localization–gap inequality (Exp. C)")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout()
fig.savefig("exp_C_saturation.png", dpi=150)
print("保存: exp_C_saturation.png")
