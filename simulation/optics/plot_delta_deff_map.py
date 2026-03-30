"""
δ×D_eff 光学応答マップ
=====================
公開データから取得したδ proxy（π帯バンド幅, 有効質量, バンドギャップ）を用いて、
δ×D_eff の2次元マップ上に炭素同素体+h-BNをプロットする。

出力: simulation/figures/ 以下にPNG画像を保存
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['font.family'] = ['Hiragino Sans', 'Arial Unicode MS', 'sans-serif']

# ============================================================
# データ定義（公開文献から取得）
# ============================================================

materials = {
    "Diamond": {
        "label_jp": "ダイヤモンド",
        "pi_bandwidth_eV": None,  # sp3, no π band
        "inv_eff_mass": 1 / 0.48,  # 伝導有効質量の逆数
        "bandgap_eV": 5.47,
        "D_eff": 0,
        "optical_category": "透明",
        "color": "#1E90FF",  # blue
        "marker": "D",
    },
    "C60": {
        "label_jp": "C60固体",
        "pi_bandwidth_eV": 0.45,
        "inv_eff_mass": 1 / 4.0,
        "bandgap_eV": 1.75,
        "D_eff": 0,
        "optical_category": "色（暗紫）",
        "color": "#9932CC",  # purple
        "marker": "p",
    },
    "SWCNT_sc": {
        "label_jp": "SWCNT\n(半導体型)",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 1 / 0.07,
        "bandgap_eV": 1.0,
        "D_eff": 1,
        "optical_category": "カイラリティ依存色",
        "color": "#FF8C00",  # orange
        "marker": "s",
    },
    "SWCNT_m": {
        "label_jp": "SWCNT\n(金属型)",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 30.0,  # 金属的→大きな値で代用
        "bandgap_eV": 0.0,
        "D_eff": 1,
        "optical_category": "黒-光沢",
        "color": "#FF4500",  # red-orange
        "marker": "s",
    },
    "Graphene": {
        "label_jp": "グラフェン",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 33.3,  # 1/0.03 (サイクロトロン質量)
        "bandgap_eV": 0.0,
        "D_eff": 2,
        "optical_category": "ほぼ透明\n(2.3%/層)",
        "color": "#228B22",  # green
        "marker": "^",
    },
    "Graphite": {
        "label_jp": "グラファイト",
        "pi_bandwidth_eV": 9.0,
        "inv_eff_mass": 1 / 0.039,
        "bandgap_eV": 0.0,
        "D_eff": 2,
        "optical_category": "黒+劈開面光沢",
        "color": "#2F4F4F",  # dark slate
        "marker": "o",
    },
    "hBN": {
        "label_jp": "h-BN",
        "pi_bandwidth_eV": 2.4,
        "inv_eff_mass": 1 / 0.26,
        "bandgap_eV": 5.95,
        "D_eff": 0,
        "optical_category": "白（透明）",
        "color": "#CCCCCC",  # light gray
        "marker": "h",
        "edgecolor": "#333333",
    },
}

# ============================================================
# Figure 1: δ (π帯バンド幅) vs D_eff マップ
# ============================================================

fig1, ax1 = plt.subplots(figsize=(10, 7))

for key, m in materials.items():
    bw = m["pi_bandwidth_eV"]
    if bw is None:
        # ダイヤモンドはπ帯なし → x=0に配置して注釈
        bw = 0.0
    ec = m.get("edgecolor", m["color"])
    ax1.scatter(
        bw, m["D_eff"],
        s=250, c=m["color"], marker=m["marker"],
        edgecolors=ec, linewidths=1.5, zorder=5,
    )
    # ラベル
    offset_x, offset_y = 0.3, 0.08
    if key == "Diamond":
        offset_x, offset_y = 0.3, -0.15
    elif key == "hBN":
        offset_x, offset_y = 0.3, 0.08
    elif key == "Graphite":
        offset_x, offset_y = 0.3, -0.15
    elif key == "SWCNT_m":
        offset_x, offset_y = 0.3, -0.15
    elif key == "C60":
        offset_x, offset_y = 0.3, 0.08

    ax1.annotate(
        f"{m['label_jp']}\n({m['optical_category']})",
        (bw, m["D_eff"]),
        xytext=(bw + offset_x, m["D_eff"] + offset_y),
        fontsize=8, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
    )

# 背景の領域分け
ax1.axhspan(-0.3, 0.5, color="#E6F3FF", alpha=0.4, zorder=0)  # D_eff≈0
ax1.axhspan(0.5, 1.5, color="#FFF3E6", alpha=0.4, zorder=0)   # D_eff=1
ax1.axhspan(1.5, 2.5, color="#E6FFE6", alpha=0.4, zorder=0)   # D_eff=2
ax1.axhspan(2.5, 3.3, color="#FFE6E6", alpha=0.4, zorder=0)   # D_eff=3

# 軸ラベルとD_eff領域ラベル
ax1.set_xlabel("δ proxy: π帯バンド幅 (eV)", fontsize=13)
ax1.set_ylabel("D_eff (有効伝導次元)", fontsize=13)
ax1.set_title("δ × D_eff 光学応答マップ（炭素同素体 + h-BN対照系）", fontsize=14, fontweight="bold")

ax1.set_xlim(-0.5, 12)
ax1.set_ylim(-0.3, 3.3)
ax1.set_yticks([0, 1, 2, 3])
ax1.set_yticklabels(["0\n(局在/絶縁)", "1\n(1D伝導)", "2\n(2D面内)", "3\n(3D金属)"])

# 右端にD_eff=3の参照点（金属）
ax1.scatter(11, 3, s=200, c="gold", marker="*", edgecolors="black", linewidths=1.0, zorder=5)
ax1.annotate("金属 (Au, Ag等)\n(金属光沢)", (11, 3),
             xytext=(8.5, 2.7), fontsize=8, ha="center",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
             arrowprops=dict(arrowstyle="->", color="gray"))

# 矢印：δ増大方向
ax1.annotate("", xy=(10, -0.15), xytext=(0.5, -0.15),
             arrowprops=dict(arrowstyle="->", lw=1.5, color="navy"))
ax1.text(5.25, -0.22, "δ 増大 → 電子非局在化", ha="center", fontsize=10, color="navy")

ax1.grid(True, alpha=0.3)
fig1.tight_layout()
fig1.savefig("simulation/figures/fig1_delta_deff_map.png", dpi=200, bbox_inches="tight")
print("Saved: simulation/figures/fig1_delta_deff_map.png")


# ============================================================
# Figure 2: δ proxy 相関図（バンド幅 vs バンドギャップ）
# ============================================================

fig2, ax2 = plt.subplots(figsize=(9, 6))

for key, m in materials.items():
    bw = m["pi_bandwidth_eV"]
    if bw is None:
        continue  # ダイヤモンドはπ帯バンド幅なし
    ec = m.get("edgecolor", m["color"])
    ax2.scatter(
        bw, m["bandgap_eV"],
        s=200, c=m["color"], marker=m["marker"],
        edgecolors=ec, linewidths=1.5, zorder=5,
    )
    ox = 0.3
    if key == "SWCNT_m":
        ox = -2.5
    ax2.annotate(
        m["label_jp"],
        (bw, m["bandgap_eV"]),
        xytext=(bw + ox, m["bandgap_eV"] + 0.2),
        fontsize=9, ha="left" if ox > 0 else "right",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8),
    )

# フィッティング線（π帯バンド幅 vs Eg の逆相関）
bw_data = []
eg_data = []
for key, m in materials.items():
    if m["pi_bandwidth_eV"] is not None:
        bw_data.append(m["pi_bandwidth_eV"])
        eg_data.append(m["bandgap_eV"])

bw_arr = np.array(bw_data)
eg_arr = np.array(eg_data)

# 相関係数
r = np.corrcoef(bw_arr, eg_arr)[0, 1]

# 線形フィット
coeffs = np.polyfit(bw_arr, eg_arr, 1)
x_fit = np.linspace(0, 10, 100)
y_fit = np.polyval(coeffs, x_fit)
y_fit = np.maximum(y_fit, 0)
ax2.plot(x_fit, y_fit, "--", color="gray", alpha=0.5, zorder=1)

ax2.set_xlabel("δ proxy: π帯バンド幅 (eV)", fontsize=13)
ax2.set_ylabel("バンドギャップ Eg (eV)", fontsize=13)
ax2.set_title(f"δ-Eg 逆相関（r = {r:.3f}）", fontsize=14, fontweight="bold")
ax2.set_xlim(-0.5, 11)
ax2.set_ylim(-0.5, 7)
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig("simulation/figures/fig2_delta_bandgap_correlation.png", dpi=200, bbox_inches="tight")
print(f"Saved: simulation/figures/fig2_delta_bandgap_correlation.png")
print(f"Correlation coefficient r = {r:.3f}")


# ============================================================
# Figure 3: 有効質量ベースのδ vs D_eff（ダイヤモンド含む）
# ============================================================

fig3, ax3 = plt.subplots(figsize=(10, 7))

for key, m in materials.items():
    inv_m = m["inv_eff_mass"]
    ec = m.get("edgecolor", m["color"])
    ax3.scatter(
        inv_m, m["D_eff"],
        s=250, c=m["color"], marker=m["marker"],
        edgecolors=ec, linewidths=1.5, zorder=5,
    )
    offset_x = inv_m * 0.05 + 0.5
    offset_y = 0.08
    if key == "Graphite":
        offset_y = -0.15
    elif key == "SWCNT_m":
        offset_y = -0.15
    elif key == "Diamond":
        offset_y = -0.15

    ax3.annotate(
        f"{m['label_jp']}\n({m['optical_category']})",
        (inv_m, m["D_eff"]),
        xytext=(inv_m + offset_x, m["D_eff"] + offset_y),
        fontsize=8, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
    )

# 背景領域
ax3.axhspan(-0.3, 0.5, color="#E6F3FF", alpha=0.4, zorder=0)
ax3.axhspan(0.5, 1.5, color="#FFF3E6", alpha=0.4, zorder=0)
ax3.axhspan(1.5, 2.5, color="#E6FFE6", alpha=0.4, zorder=0)
ax3.axhspan(2.5, 3.3, color="#FFE6E6", alpha=0.4, zorder=0)

ax3.set_xlabel("δ proxy: 1/m* (逆有効質量, m₀⁻¹)", fontsize=13)
ax3.set_ylabel("D_eff (有効伝導次元)", fontsize=13)
ax3.set_title("δ(1/m*) × D_eff 光学応答マップ（全物質比較）", fontsize=14, fontweight="bold")
ax3.set_xscale("log")
ax3.set_xlim(0.1, 50)
ax3.set_ylim(-0.3, 3.3)
ax3.set_yticks([0, 1, 2, 3])
ax3.set_yticklabels(["0\n(局在/絶縁)", "1\n(1D伝導)", "2\n(2D面内)", "3\n(3D金属)"])

ax3.scatter(40, 3, s=200, c="gold", marker="*", edgecolors="black", linewidths=1.0, zorder=5)
ax3.annotate("金属 (Au, Ag等)\n(金属光沢)", (40, 3),
             xytext=(15, 2.7), fontsize=8, ha="center",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
             arrowprops=dict(arrowstyle="->", color="gray"))

ax3.grid(True, alpha=0.3, which="both")
fig3.tight_layout()
fig3.savefig("simulation/figures/fig3_invmass_deff_map.png", dpi=200, bbox_inches="tight")
print("Saved: simulation/figures/fig3_invmass_deff_map.png")

plt.close("all")
print("\nDone.")
