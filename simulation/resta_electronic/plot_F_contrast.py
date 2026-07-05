"""F-0/F-2 の結果 JSON から「2枚看板」対照図を生成"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("exp_F0_results.json") as f:
    f0 = json.load(f)
with open("exp_F2_results.json") as f:
    f2 = json.load(f)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))

# 左: λ² の対照
lam_liq = np.mean(list(f0["lambda2_A2"].values()))
lam_nacl = np.mean(list(f2["lambda2"].values()))
bars = axes[0].bar(["liquid Na\n(metal)", "NaCl crystal\n(insulator)"],
                   [lam_liq, lam_nacl], color=["tab:red", "tab:blue"], width=0.5)
axes[0].bind = None
axes[0].annotate("diverges with N\n(finite-size value at N=64)",
                 xy=(0, lam_liq), xytext=(0.35, lam_liq * 0.92),
                 fontsize=9, color="tab:red",
                 arrowprops=dict(arrowstyle="->", color="tab:red"))
axes[0].annotate("finite & isotropic\n(converged)",
                 xy=(1, lam_nacl), xytext=(0.62, lam_nacl + 1.2),
                 fontsize=9, color="tab:blue",
                 arrowprops=dict(arrowstyle="->", color="tab:blue"))
axes[0].set_ylabel("λ²  (Å²)")
axes[0].set_title("Electronic localization length: the two-sided signboard")

# 右: バンドブロックの幾何平均（PAW 対角補正後）
groups = [
    ("Na semicore\n(in liquid Na)", np.mean(list(f0["geom_mean_semicore"].values())
                                            ) / 0.680,  # 補正換算: 0.6745/0.680≈0.992
     "tab:blue"),
    ("3s valence\n(liquid Na)", np.mean(list(f0["geom_mean_3s"].values())), "tab:red"),
    ("Na semicore\n(in NaCl)", (f2["blocks_norm_corrected"]["Na 2s"]
                                + 3 * f2["blocks_norm_corrected"]["Na 2p"]) / 4,
     "tab:blue"),
    ("Cl 3p valence\n(NaCl)", f2["blocks_norm_corrected"]["Cl 3p"], "tab:cyan"),
]
axes[1].bar([g[0] for g in groups], [g[1] for g in groups],
            color=[g[2] for g in groups], width=0.55)
for i, g in enumerate(groups):
    axes[1].text(i, g[1] + 0.02, f"{g[1]:.2f}", ha="center", fontsize=9)
axes[1].axhline(1.0, ls=":", color="gray", lw=0.8)
axes[1].set_ylim(0, 1.15)
axes[1].set_ylabel("per-band |z|$^{1/N}$ (PAW diag-corrected)")
axes[1].set_title("Core stays localized everywhere; only the metallic valence sea melts")
fig.tight_layout()
fig.savefig("exp_F_contrast.png", dpi=150)
print("保存: exp_F_contrast.png")
