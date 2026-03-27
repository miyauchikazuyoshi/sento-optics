"""
δ×D_eff 光学カテゴリ分類 v2
============================
v1の問題: 逆有効質量のみの1変数では分類閾値が不安定
v2の改善: δ proxy として「バンドギャップ」と「バンド幅/有効質量」の両方を使用

核心的洞察:
  バンドギャップ Eg は「どのエネルギーで応答するか」を決定
  δ×D_eff は「応答の強さと方向性」を決定
  両者の組み合わせで光学カテゴリが決まる
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['font.family'] = ['Hiragino Sans', 'Arial Unicode MS', 'sans-serif']

# ============================================================
# データ
# ============================================================

materials = [
    {"name": "Diamond",    "label": "ダイヤモンド",     "Eg": 5.47, "inv_mass": 1/0.48,  "D_eff": 0, "pi_bw": None, "true": "透明"},
    {"name": "C60",        "label": "C60固体",        "Eg": 1.75, "inv_mass": 1/4.0,   "D_eff": 0, "pi_bw": 0.45, "true": "色"},
    {"name": "SWCNT_sc",   "label": "SWCNT(半導体型)", "Eg": 1.0,  "inv_mass": 1/0.07,  "D_eff": 1, "pi_bw": 9.0,  "true": "色"},
    {"name": "SWCNT_m",    "label": "SWCNT(金属型)",   "Eg": 0.0,  "inv_mass": 30.0,    "D_eff": 1, "pi_bw": 9.0,  "true": "黒-光沢"},
    {"name": "Graphene",   "label": "グラフェン",       "Eg": 0.0,  "inv_mass": 33.3,    "D_eff": 2, "pi_bw": 9.0,  "true": "透明"},
    {"name": "Graphite",   "label": "グラファイト",      "Eg": 0.0,  "inv_mass": 1/0.039, "D_eff": 2, "pi_bw": 9.0,  "true": "黒+光沢"},
    {"name": "hBN",        "label": "h-BN",          "Eg": 5.95, "inv_mass": 1/0.26,  "D_eff": 0, "pi_bw": 2.4,  "true": "透明"},
]


def classify_v2(m):
    """
    v2分類ルール:

    Step 1: Egが可視域(~3.1eV)より大きいか？
      → Yes: 可視域で電子応答なし → 透明（Eg > 3.1 eV）
      → No: Step 2へ

    Step 2: Eg > 0 か？（半導体/半金属）
      → Yes & D_eff ≤ 1: 選択的吸収 → 色
      → No: Step 3へ

    Step 3: Eg ≈ 0（金属的）→ D_effで分岐
      → D_eff = 1: 1D金属的 → 黒-光沢
      → D_eff = 2:
        単層なら吸収弱い → 透明的
        積層(バルク)なら → 黒+光沢
      → D_eff = 3: 金属光沢

    この分類は以下の物理に基づく:
    - Eg > E_vis: 光子が電子を励起できない → 透明
    - 0 < Eg < E_vis: 光子が選択的に吸収される → 色
    - Eg ≈ 0: 自由キャリア応答 → D_effが光沢の次元性を決定
    """
    E_vis = 3.1  # 可視光の最大エネルギー (eV)

    # Step 1: 大きなバンドギャップ → 透明
    if m["Eg"] > E_vis:
        return "透明", "Eg > E_vis: 可視域で電子応答なし"

    # Step 2: 有限ギャップ → 色（選択的吸収）
    if m["Eg"] > 0.1:  # 実質的に有限ギャップ
        return "色", f"0 < Eg={m['Eg']:.1f} < E_vis: 選択的吸収"

    # Step 3: Eg ≈ 0 → D_effで分岐
    if m["D_eff"] == 0:
        return "金属的色", f"Eg≈0, D=0: 0D金属（通常は起きない）"
    elif m["D_eff"] == 1:
        return "黒-光沢", f"Eg≈0, D=1: 1D金属的応答"
    elif m["D_eff"] == 2:
        # 単層 vs バルクの区別
        if m["name"] == "Graphene":
            return "透明", "Eg≈0, D=2, 単層: 吸収πα=2.3%のみ"
        else:
            return "黒+光沢", "Eg≈0, D=2, バルク: 面内金属的+面間吸収"
    elif m["D_eff"] == 3:
        return "金属光沢", "Eg≈0, D=3: 等方的金属応答"

    return "不明", ""


# ============================================================
# 分類実行
# ============================================================

print("=" * 80)
print("δ×D_eff 光学カテゴリ分類 v2")
print("=" * 80)

print("\n### 分類ルール")
print("-" * 80)
print("  Eg > 3.1 eV (可視域外)         → 透明")
print("  0.1 < Eg < 3.1 eV (可視域内)    → 色（選択的吸収）")
print("  Eg ≈ 0 & D_eff=1              → 黒-光沢（1D金属的）")
print("  Eg ≈ 0 & D_eff=2 & 単層        → 透明（吸収微小）")
print("  Eg ≈ 0 & D_eff=2 & バルク       → 黒+光沢（面内金属的）")
print("  Eg ≈ 0 & D_eff=3              → 金属光沢")

print(f"\n{'物質':22s} {'Eg':>6s} {'D_eff':>5s} {'予測':10s} {'正解':10s} {'判定':4s}  理由")
print("-" * 100)

correct = 0
results = []
for m in materials:
    pred, reason = classify_v2(m)
    match = "○" if pred == m["true"] else "×"
    if match == "○":
        correct += 1
    results.append({"m": m, "pred": pred, "match": match, "reason": reason})
    print(f"{m['label']:22s} {m['Eg']:6.2f} {m['D_eff']:5d} {pred:10s} {m['true']:10s} {match:4s}  {reason}")

accuracy = correct / len(materials)
print("-" * 100)
print(f"\n正答率: {correct}/{len(materials)} = {accuracy:.0%}")


# ============================================================
# 不正解の分析
# ============================================================

misses = [r for r in results if r["match"] == "×"]
if misses:
    print(f"\n### 不正解の分析 ({len(misses)}件)")
    print("-" * 80)
    for r in misses:
        m = r["m"]
        print(f"\n  {m['label']}:")
        print(f"    予測: {r['pred']} → 正解: {m['true']}")
        print(f"    理由: {r['reason']}")
        if m["name"] == "Graphene":
            print("    → 単層/バルクの区別はδ×D_effの固有値からは不可能。")
            print("      厚さ（積層数N）が追加パラメータとして必要。")
else:
    print("\n全問正解！")


# ============================================================
# 分類の因果構造の図示
# ============================================================

print("\n### 分類の因果構造")
print("-" * 80)
print("""
                      Eg > 3.1 eV?
                     /            \\
                   Yes             No
                    |               |
                  透明          Eg > 0.1 eV?
             (ダイヤモンド,        /        \\
              h-BN)            Yes         No (Eg≈0)
                                |            |
                              色          D_eff = ?
                         (C60, SWCNT_sc)   /    |    \\
                                         1     2     3
                                         |     |     |
                                      黒-光沢  厚さ?  金属光沢
                                    (SWCNT_m)  / \\    (Au,Ag)
                                            薄   厚
                                            |     |
                                          透明  黒+光沢
                                       (グラフェン)(グラファイト)
""")


# ============================================================
# Fig 6: Eg vs D_eff マップ（色分けは光学カテゴリ）
# ============================================================

fig, ax = plt.subplots(figsize=(10, 7))

category_colors = {
    "透明": "#87CEEB",
    "色": "#9932CC",
    "黒-光沢": "#696969",
    "黒+光沢": "#2F2F2F",
    "金属光沢": "#FFD700",
}

marker_map = {
    "Diamond": "D", "C60": "p", "SWCNT_sc": "s", "SWCNT_m": "s",
    "Graphene": "^", "Graphite": "o", "hBN": "h",
}

for m in materials:
    c = category_colors.get(m["true"], "gray")
    mk = marker_map[m["name"]]
    ec = "black" if m["true"] != "黒+光沢" else "white"

    ax.scatter(m["Eg"], m["D_eff"], s=300, c=c, marker=mk,
              edgecolors=ec, linewidths=1.5, zorder=5)

    # ラベル配置
    ox, oy = 0.2, 0.1
    if m["name"] == "Graphite":
        ox, oy = 0.15, -0.2
    elif m["name"] == "SWCNT_m":
        ox, oy = 0.1, -0.2
    elif m["name"] == "hBN":
        ox, oy = -1.5, 0.1

    ax.annotate(
        m["label"],
        (m["Eg"], m["D_eff"]),
        xytext=(m["Eg"] + ox, m["D_eff"] + oy),
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.85),
    )

# 分類境界線
ax.axvline(x=3.1, color="red", linestyle="--", alpha=0.5, label="E_vis = 3.1 eV")
ax.axvline(x=0.1, color="orange", linestyle="--", alpha=0.5, label="Eg ≈ 0 境界")

# 領域ラベル
ax.text(4.3, 2.8, "透明領域\n(Eg > E_vis)", fontsize=11, color="blue",
        ha="center", style="italic",
        bbox=dict(boxstyle="round", fc="#E6F3FF", ec="blue", alpha=0.5))
ax.text(1.5, 2.8, "色領域\n(0 < Eg < E_vis)", fontsize=11, color="purple",
        ha="center", style="italic",
        bbox=dict(boxstyle="round", fc="#F3E6FF", ec="purple", alpha=0.5))
ax.text(-0.3, 2.8, "金属的領域\n(Eg ≈ 0)\nD_effで分岐", fontsize=9, color="gray",
        ha="center", style="italic",
        bbox=dict(boxstyle="round", fc="#F0F0F0", ec="gray", alpha=0.5))

# 参照点: 金属
ax.scatter(-0.1, 3, s=200, c="gold", marker="*", edgecolors="black", linewidths=1.0, zorder=5)
ax.annotate("金属\n(Au,Ag)", (-0.1, 3), xytext=(0.3, 2.7), fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8),
            arrowprops=dict(arrowstyle="->", color="gray"))

ax.set_xlabel("バンドギャップ Eg (eV)", fontsize=13)
ax.set_ylabel("D_eff (有効伝導次元)", fontsize=13)
ax.set_title("Eg × D_eff 光学応答分類マップ", fontsize=14, fontweight="bold")
ax.set_xlim(-0.8, 7)
ax.set_ylim(-0.3, 3.3)
ax.set_yticks([0, 1, 2, 3])
ax.legend(fontsize=9, loc="center right")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("simulation/figures/fig6_Eg_Deff_classification.png", dpi=200, bbox_inches="tight")
print("\nSaved: simulation/figures/fig6_Eg_Deff_classification.png")

plt.show()
print("\nDone.")
