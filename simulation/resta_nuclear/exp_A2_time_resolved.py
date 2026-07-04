"""
実験A-2: |z1(n)| の時間分解 — 液体Naの残留構造は初期配置の記憶か？

仮説: 平衡液体では一体量 z1 は並進対称性により厳密にゼロ。
      exp_A で見えた n=4-6 の残留が時間とともに減衰していれば、
      それは「平衡化不足の検出」であり、z_nuc は平衡化モニタとして機能している。
"""
import numpy as np

TRJ = "../surface_tension/aimd/tmp/Na_liquid.mdtrj"
NAT = 64
rows = [list(map(float, l.split())) for l in open(TRJ) if len(l.split()) == 204]
data = np.array(rows)
L = data[0, 3]
pos = data[:, 12:204].reshape(-1, NAT, 3)
nstep = len(pos)
t_ps = data[:, 0]
print(f"steps={nstep}, t = {t_ps[0]*1e3:.2f} .. {t_ps[-1]*1e3:.2f} fs*1000? -> 最終 {t_ps[-1]:.4f} ps")

NBLOCK = 8
blocks = np.array_split(np.arange(nstep), NBLOCK)
print(f"\n|z1(n)| を {NBLOCK} 時間ブロックで追跡（3方向平均）:")
print(f"{'block':>6} {'t中心(ps)':>10} " + " ".join(f"{'n='+str(n):>8}" for n in [1, 4, 5, 6]))
series = {n: [] for n in [1, 4, 5, 6]}
for b, idx in enumerate(blocks):
    tc = t_ps[idx].mean()
    vals = []
    for n in [1, 4, 5, 6]:
        z = np.exp(1j * 2 * np.pi * n * pos[idx] / L).mean(axis=(0, 1))
        v = np.abs(z).mean()
        series[n].append(v)
        vals.append(v)
    print(f"{b:>6} {tc:>10.4f} " + " ".join(f"{v:>8.4f}" for v in vals))

for n in [4, 5, 6]:
    first, last = np.mean(series[n][:2]), np.mean(series[n][-2:])
    trend = "減衰" if last < first * 0.7 else ("横ばい" if last < first * 1.3 else "増加")
    print(f"n={n}: 前半 {first:.4f} → 後半 {last:.4f} ({trend})")

# 初期スナップショット単体の z1 スペクトル（初期配置の記憶の直接確認）
print("\n初期スナップショット(step1)単体の |z1(n)|（時間平均なし・3方向平均）:")
for n in range(1, 11):
    z = np.abs(np.exp(1j * 2 * np.pi * n * pos[0] / L).mean(axis=0)).mean()
    print(f"  n={n}: {z:.4f}")
print(f"(一様ランダム64原子の期待値 ~{1/np.sqrt(NAT):.3f})")
