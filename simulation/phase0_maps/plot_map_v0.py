"""(δ_nuc, q300) マップ v0 — delta_nuc_results.csv から散布図を描く"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("delta_nuc_results.csv")))
d = np.array([float(r["delta_nuc_300K"]) for r in rows])
q = np.array([float(r["q300"]) for r in rows])
names = [r["formula"] for r in rows]
print(f"{len(rows)} 材料")

fig, ax = plt.subplots(figsize=(8.5, 6))
sc = ax.scatter(d, q, s=14, alpha=0.55, c=q, cmap="coolwarm_r", vmin=0, vmax=1)
ax.set_xscale("log")
ax.set_xlabel("δ_nuc(300 K) = ⟨u²⟩ / d_min²   (log)")
ax.set_ylabel("q300 = ⟨u²⟩(0K) / ⟨u²⟩(300K)   (zero-point fraction)")
ax.set_title(f"Nuclear delocalization map v0 — {len(rows)} materials from phonondb")

# 注釈: q300 上位 8（量子固体側）と δ_nuc 上位 5（融けかけ側）
idx_q = np.argsort(q)[-8:]
idx_d = np.argsort(d)[-5:]
for i in set(idx_q) | set(idx_d):
    ax.annotate(names[i], (d[i], q[i]), fontsize=7,
                textcoords="offset points", xytext=(4, 3))
# 参照点
for ref, (dd, qq) in {"Si": (0.00125, 0.360), "NaCl": (0.00260, 0.233)}.items():
    ax.scatter([dd], [qq], marker="*", s=120, color="k", zorder=5)
    ax.annotate(ref, (dd, qq), fontsize=9, fontweight="bold",
                textcoords="offset points", xytext=(6, -10))

cb = fig.colorbar(sc, ax=ax)
cb.set_label("q300")
fig.tight_layout()
fig.savefig("map_v0.png", dpi=150)
print("保存: map_v0.png")

# 上位リスト（報告用）
order = np.argsort(q)[::-1]
print("\n量子固体側 (q300 上位10):")
for i in order[:10]:
    print(f"  {names[i]:<10} q300={q[i]:.3f}  δ_nuc={d[i]:.5f}")
order_d = np.argsort(d)[::-1]
print("\n大振幅側 (δ_nuc 上位10):")
for i in order_d[:10]:
    print(f"  {names[i]:<10} δ_nuc={d[i]:.5f}  q300={q[i]:.3f}")
