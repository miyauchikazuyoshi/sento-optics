"""
δ×D_eff 光学応答分類のためのタイトバインディング概念実証シミュレーション
=======================================================================

目的:
  炭素同素体（ダイヤモンド, グラフェン, 1D鎖(SWCNT近似), C60固体）に対して
  タイトバインディングモデルでバンド構造・DOS・IPR(δプロキシ)を計算し、
  δ-Eg 逆相関と δ×D_eff 光学分類を検証する。

手法:
  - Diamond: sp3 2サイト基底 + ホッピング t_sp3 = -2.0 eV
  - Graphene: π帯 最近接ホッピング t = -2.7 eV (ハニカム格子)
  - 1D chain: 最近接ホッピング t = -2.7 eV (SWCNT簡易モデル)
  - C60固体: 分子内 t = -2.7 eV (切頂二十面体接続) + 分子間 t_inter = -0.04 eV

著者: sento-optics project
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os

# ============================================================
# フォント設定（日本語対応）
# ============================================================
matplotlib.rcParams['font.family'] = ['Hiragino Sans', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

# 出力ディレクトリ
FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGDIR, exist_ok=True)


# ============================================================
# 1. ダイヤモンド: sp3 タイトバインディング (2サイト FCC基底)
# ============================================================
def diamond_bandstructure(nk=200):
    """
    ダイヤモンド構造の最小タイトバインディングモデル。
    FCC格子上の2原子基底（A, B）にオンサイトエネルギー差Δを導入し、
    sp3混成による間接バンドギャップを再現する。

    ハミルトニアン:
        H(k) = [[+Δ/2,    f(k)*t],
                 [f(k)*t,  -Δ/2  ]]
    f(k) = Σ_i exp(i k・d_i), d_i = sp3ボンドベクトル
    t_sp3 = -2.0 eV, Δ = 5.0 eV (ギャップ調整用)

    物理的背景: 実際のダイヤモンドではs/p軌道のエネルギー差がバンドギャップを生む。
    ここでは2バンドモデルで有効的にΔパラメータとして取り込む。
    """
    t = -2.0   # sp3ホッピング積分 [eV]
    Delta = 5.0  # オンサイトエネルギー差 [eV] → 実効バンドギャップ生成
    a = 3.567  # ダイヤモンド格子定数 [Å]

    # sp3ボンドベクトル（FCC慣例、a/4単位）
    d = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ]) * a / 4.0

    # 高対称点 (Γ-X-W-L-Γ-K) を2π/a単位で定義
    G = np.array([0, 0, 0])
    X = np.array([1, 0, 0]) * 2 * np.pi / a
    W = np.array([1, 0.5, 0]) * 2 * np.pi / a
    L = np.array([0.5, 0.5, 0.5]) * 2 * np.pi / a
    K = np.array([0.75, 0.75, 0]) * 2 * np.pi / a

    # k経路の構築
    segments = [(G, X, "Γ-X"), (X, W, "X-W"), (W, L, "W-L"), (L, G, "L-Γ"), (G, K, "Γ-K")]
    kpoints = []
    tick_positions = [0]
    tick_labels = ["Γ"]
    dist = 0.0

    for start, end, label in segments:
        for i in range(nk):
            frac = i / nk
            kpoints.append(start + frac * (end - start))
        seg_len = np.linalg.norm(end - start)
        dist += seg_len
        tick_positions.append(dist)
        tick_labels.append(label.split("-")[1])

    kpoints = np.array(kpoints)

    # k距離の計算
    kdist = np.zeros(len(kpoints))
    for i in range(1, len(kpoints)):
        kdist[i] = kdist[i - 1] + np.linalg.norm(kpoints[i] - kpoints[i - 1])

    # バンド計算: 2x2行列の対角化
    E_bands = np.zeros((len(kpoints), 2))
    for ik, k in enumerate(kpoints):
        # 構造因子 f(k) = Σ exp(i k・d_i)
        fk = sum(np.exp(1j * np.dot(k, di)) for di in d)
        V = abs(t * fk)  # ホッピングの大きさ
        # 固有値: ±sqrt((Δ/2)^2 + V^2)
        E_bands[ik, 0] = -np.sqrt((Delta / 2) ** 2 + V ** 2)  # 価電子帯
        E_bands[ik, 1] = np.sqrt((Delta / 2) ** 2 + V ** 2)    # 伝導帯

    return kdist, E_bands, tick_positions, tick_labels


def diamond_dos(ne=500, nbroad=0.15):
    """ダイヤモンドのDOSを3D k空間サンプリングで計算。"""
    t = -2.0
    Delta = 5.0
    a = 3.567
    d = np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]) * a / 4.0

    nk = 30  # 各方向のkメッシュ数
    energies = []
    kgrid = np.linspace(-np.pi / a, np.pi / a, nk)

    for kx in kgrid:
        for ky in kgrid:
            for kz in kgrid:
                k = np.array([kx, ky, kz])
                fk = sum(np.exp(1j * np.dot(k, di)) for di in d)
                V = abs(t * fk)
                E = np.sqrt((Delta / 2) ** 2 + V ** 2)
                energies.append(-E)
                energies.append(E)

    energies = np.array(energies)
    emin, emax = energies.min() - 1, energies.max() + 1
    egrid = np.linspace(emin, emax, ne)
    dos = np.zeros(ne)
    for e in energies:
        dos += np.exp(-0.5 * ((egrid - e) / nbroad) ** 2) / (nbroad * np.sqrt(2 * np.pi))
    dos /= len(energies)

    return egrid, dos, energies


# ============================================================
# 2. グラフェン: π帯タイトバインディング (ハニカム格子)
# ============================================================
def graphene_bandstructure(nk=200):
    """
    グラフェンのπ帯最近接ホッピングモデル。
    ハニカム格子の2原子基底、t = -2.7 eV。
    E(k) = ±|t| |f(k)|, f(k) = 1 + exp(ik・a1) + exp(ik・a2)
    """
    t = -2.7  # ホッピング積分 [eV]
    a = 2.46  # 格子定数 [Å]

    # 格子ベクトル
    a1 = a * np.array([1, 0])
    a2 = a * np.array([0.5, np.sqrt(3) / 2])

    # 逆格子ベクトル
    b1 = (2 * np.pi / a) * np.array([1, -1 / np.sqrt(3)])
    b2 = (2 * np.pi / a) * np.array([0, 2 / np.sqrt(3)])

    # 高対称点
    G = np.array([0, 0])
    K = (2 * b1 + b2) / 3
    M = b1 / 2

    # k経路
    segments = [(G, K, "Γ-K"), (K, M, "K-M"), (M, G, "M-Γ")]
    kpoints = []
    tick_positions = [0]
    tick_labels = ["Γ"]
    dist = 0.0

    for start, end, label in segments:
        for i in range(nk):
            frac = i / nk
            kpoints.append(start + frac * (end - start))
        seg_len = np.linalg.norm(end - start)
        dist += seg_len
        tick_positions.append(dist)
        tick_labels.append(label.split("-")[1])

    kpoints = np.array(kpoints)

    kdist = np.zeros(len(kpoints))
    for i in range(1, len(kpoints)):
        kdist[i] = kdist[i - 1] + np.linalg.norm(kpoints[i] - kpoints[i - 1])

    # 最近接ベクトル（A→B）
    delta1 = np.array([0, a / np.sqrt(3)])
    delta2 = np.array([a / 2, -a / (2 * np.sqrt(3))])
    delta3 = np.array([-a / 2, -a / (2 * np.sqrt(3))])

    E_bands = np.zeros((len(kpoints), 2))
    for ik, k in enumerate(kpoints):
        fk = (np.exp(1j * np.dot(k, delta1))
              + np.exp(1j * np.dot(k, delta2))
              + np.exp(1j * np.dot(k, delta3)))
        E = abs(t) * abs(fk)
        E_bands[ik, 0] = -E  # π帯
        E_bands[ik, 1] = E    # π*帯

    return kdist, E_bands, tick_positions, tick_labels


def graphene_dos(ne=500, nbroad=0.1):
    """グラフェンのDOSを2D k空間サンプリングで計算。"""
    t = -2.7
    a = 2.46
    delta1 = np.array([0, a / np.sqrt(3)])
    delta2 = np.array([a / 2, -a / (2 * np.sqrt(3))])
    delta3 = np.array([-a / 2, -a / (2 * np.sqrt(3))])

    nk = 100
    b1 = (2 * np.pi / a) * np.array([1, -1 / np.sqrt(3)])
    b2 = (2 * np.pi / a) * np.array([0, 2 / np.sqrt(3)])

    energies = []
    for i in range(nk):
        for j in range(nk):
            k = (i / nk) * b1 + (j / nk) * b2
            fk = (np.exp(1j * np.dot(k, delta1))
                  + np.exp(1j * np.dot(k, delta2))
                  + np.exp(1j * np.dot(k, delta3)))
            E = abs(t) * abs(fk)
            energies.append(-E)
            energies.append(E)

    energies = np.array(energies)
    emin, emax = energies.min() - 1, energies.max() + 1
    egrid = np.linspace(emin, emax, ne)
    dos = np.zeros(ne)
    for e in energies:
        dos += np.exp(-0.5 * ((egrid - e) / nbroad) ** 2) / (nbroad * np.sqrt(2 * np.pi))
    dos /= len(energies)

    return egrid, dos, energies


# ============================================================
# 3. 1D鎖: SWCNT簡易モデル (最近接ホッピング)
# ============================================================
def chain1d_bandstructure(nk=400):
    """
    1次元タイトバインディング鎖。
    分散関係: E(k) = -2t cos(ka)
    t = -2.7 eV, a = 1.42 Å (C-C結合長)

    SWCNT半導体型の簡易モデルとして、
    小さなギャップ Δ = 0.5 eV を手動で導入。
    E(k) = ±sqrt((2t cos(ka))^2 + (Δ/2)^2)
    """
    t = -2.7
    a = 1.42
    Delta = 0.5  # 半導体型SWCNTのバンドギャップ近似 [eV]

    kpoints = np.linspace(-np.pi / a, np.pi / a, nk)
    kdist = kpoints - kpoints[0]

    eps_k = 2 * t * np.cos(kpoints * a)
    E_val = -np.sqrt(eps_k ** 2 + (Delta / 2) ** 2)
    E_con = np.sqrt(eps_k ** 2 + (Delta / 2) ** 2)
    E_bands = np.column_stack([E_val, E_con])

    tick_positions = [kdist[0], kdist[nk // 2], kdist[-1]]
    tick_labels = ["-π/a", "0", "π/a"]

    return kdist, E_bands, tick_positions, tick_labels


def chain1d_dos(ne=500, nbroad=0.08):
    """1D鎖のDOS計算。Van Hove特異性を含む。"""
    t = -2.7
    a = 1.42
    Delta = 0.5
    nk = 2000

    kpoints = np.linspace(-np.pi / a, np.pi / a, nk)
    eps_k = 2 * t * np.cos(kpoints * a)
    energies_val = -np.sqrt(eps_k ** 2 + (Delta / 2) ** 2)
    energies_con = np.sqrt(eps_k ** 2 + (Delta / 2) ** 2)
    energies = np.concatenate([energies_val, energies_con])

    emin, emax = energies.min() - 1, energies.max() + 1
    egrid = np.linspace(emin, emax, ne)
    dos = np.zeros(ne)
    for e in energies:
        dos += np.exp(-0.5 * ((egrid - e) / nbroad) ** 2) / (nbroad * np.sqrt(2 * np.pi))
    dos /= len(energies)

    return egrid, dos, energies


# ============================================================
# 4. C60固体: 分子軌道 + 弱い分子間ホッピング
# ============================================================
def build_c60_adjacency():
    """
    C60 切頂二十面体の隣接行列を構築。
    60原子、各原子は3つの最近接原子と結合（sp2）。

    構築方法: 座標ベースで最近接を判定。
    C60の座標は黄金比を用いて生成。
    """
    phi = (1 + np.sqrt(5)) / 2  # 黄金比

    # C60の60頂点座標（切頂二十面体）
    coords = []

    # 3つの長方形面の順列による頂点生成
    # Type 1: (0, ±1, ±3φ) の偶数順列
    # Type 2: (±2, ±(1+2φ), ±φ) の偶数順列
    # Type 3: (±1, ±(2+φ), ±2φ) の偶数順列

    # 実用的には既知の座標セットを使用
    # ここでは正二十面体の頂点から切頂操作で生成

    # 正二十面体の12頂点
    ico_verts = []
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            ico_verts.append([0, s1, s2 * phi])
            ico_verts.append([s1, s2 * phi, 0])
            ico_verts.append([s2 * phi, 0, s1])
    ico_verts = np.array(ico_verts)

    # 正二十面体の30辺を見つけ、各辺の1/3点と2/3点で切頂
    # 辺の長さは2.0（正二十面体の辺長）
    edge_len = 2.0
    edges = []
    for i in range(12):
        for j in range(i + 1, 12):
            d = np.linalg.norm(ico_verts[i] - ico_verts[j])
            if d < edge_len * 1.05:  # 辺の判定
                edges.append((i, j))

    # 各辺の1/3, 2/3点が切頂二十面体の頂点
    for i, j in edges:
        p1 = ico_verts[i] + (ico_verts[j] - ico_verts[i]) / 3.0
        p2 = ico_verts[i] + 2 * (ico_verts[j] - ico_verts[i]) / 3.0
        coords.append(p1)
        coords.append(p2)

    coords = np.array(coords)

    # 重複を除去（丸め誤差を考慮）
    unique = [coords[0]]
    for c in coords[1:]:
        is_dup = False
        for u in unique:
            if np.linalg.norm(c - u) < 0.01:
                is_dup = True
                break
        if not is_dup:
            unique.append(c)
    coords = np.array(unique)

    # 60頂点にならない場合は球面上に均等配置で代替
    if len(coords) != 60:
        # フィボナッチ球面配置で60点を生成（代替手法）
        n = 60
        coords = np.zeros((n, 3))
        golden_angle = np.pi * (3 - np.sqrt(5))
        for i in range(n):
            y = 1 - (i / (n - 1)) * 2
            radius = np.sqrt(1 - y * y)
            theta = golden_angle * i
            coords[i] = [radius * np.cos(theta), y, radius * np.sin(theta)]
        # スケーリング
        coords *= 3.55  # C60半径 ≈ 3.55 Å

    # 隣接行列の構築（各原子が3つの最近接を持つよう距離閾値を調整）
    n = len(coords)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i, j] = np.linalg.norm(coords[i] - coords[j])

    # 各原子の最近接3原子を見つける
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        dists_i = distances[i].copy()
        dists_i[i] = np.inf
        nearest_3 = np.argsort(dists_i)[:3]
        for j in nearest_3:
            adj[i, j] = 1
            adj[j, i] = 1

    return adj, coords


def c60_eigenvalues():
    """
    C60分子の固有値を計算。
    分子内ホッピング t = -2.7 eV。
    """
    t_intra = -2.7  # 分子内ホッピング [eV]

    adj, coords = build_c60_adjacency()
    n = adj.shape[0]

    # ハミルトニアン構築
    H = t_intra * adj.astype(float)
    eigenvalues = np.linalg.eigvalsh(H)

    return eigenvalues, n


def c60_solid_dos(ne=500, nbroad=0.15):
    """
    C60固体のDOS。
    分子準位 + 弱い分子間ホッピングによるバンド幅の広がり。
    分子間ホッピング t_inter = -0.04 eV による各準位のブロードニング。
    """
    eigenvalues, n = c60_eigenvalues()
    t_inter = -0.04  # 分子間ホッピング [eV]

    # 各分子準位が±2*|t_inter|*z (z=12, FCC配位数) の幅に広がる
    # FCC格子上のC60: 各分子準位が狭いバンドを形成
    z = 12  # FCC配位数
    band_width_inter = 2 * abs(t_inter) * z  # ~ 0.96 eV

    # DOSの構築: 各分子準位の周りにガウシアンブロードニング
    # 分子間ホッピングによる追加ブロードニングを加える
    total_broad = np.sqrt(nbroad ** 2 + (band_width_inter / 4) ** 2)

    emin = eigenvalues.min() - 2
    emax = eigenvalues.max() + 2
    egrid = np.linspace(emin, emax, ne)
    dos = np.zeros(ne)

    for e in eigenvalues:
        dos += np.exp(-0.5 * ((egrid - e) / total_broad) ** 2) / (total_broad * np.sqrt(2 * np.pi))
    dos /= n

    return egrid, dos, eigenvalues


def c60_bandstructure(nk=200):
    """
    C60固体の「バンド構造」。
    FCC格子上のホッピングで分子準位が分散を持つ。
    簡略化: HOMO/LUMO近傍の2準位のみを示す。

    HOMO: hu (5重縮退、E ≈ 0 eV付近)
    LUMO: t1u (3重縮退、E ≈ Eg 上)

    各準位がFCC格子上で cos(k) 型の分散を持つ。
    """
    eigenvalues, n = c60_eigenvalues()
    eigenvalues_sorted = np.sort(eigenvalues)

    # HOMO, LUMO準位の特定
    # 60原子、各1つのπ電子 → 30個の占有状態
    n_occ = n // 2
    E_homo = eigenvalues_sorted[n_occ - 1]
    E_lumo = eigenvalues_sorted[n_occ]

    t_inter = -0.04
    z_eff = 6  # 有効配位数（簡略化）

    # 高対称経路 (Γ-X-L-Γ, FCC BZ簡略版)
    kpoints = np.linspace(0, np.pi, nk)
    kdist = kpoints / kpoints[-1]  # 正規化

    # HOMO帯: E_homo + 2*t_inter*z_eff * cos(k) （簡略化された分散）
    E_homo_band = E_homo + 2 * t_inter * z_eff * np.cos(kpoints)
    E_lumo_band = E_lumo + 2 * t_inter * z_eff * np.cos(kpoints)

    E_bands = np.column_stack([E_homo_band, E_lumo_band])

    tick_positions = [kdist[0], kdist[nk // 2], kdist[-1]]
    tick_labels = ["Γ", "X", "L"]

    return kdist, E_bands, tick_positions, tick_labels


# ============================================================
# 5. IPR (Inverse Participation Ratio) の計算 → δプロキシ
# ============================================================
def compute_ipr_from_eigenvectors(H):
    """
    ハミルトニアン行列Hの固有ベクトルからIPRを計算。
    IPR = Σ_i |ψ_i|^4 / (Σ_i |ψ_i|^2)^2
    完全非局在化: IPR = 1/N（最小値）
    完全局在化: IPR = 1（最大値）

    δプロキシとしては正規化IPR逆数を使用:
    δ_norm = 1/(N * <IPR>) → [0, 1] に正規化
    δ_norm = 1 は完全非局在化
    δ_norm → 0 は強い局在化
    """
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    n = H.shape[0]
    iprs = []

    for i in range(n):
        psi = eigenvectors[:, i]
        prob = np.abs(psi) ** 2
        ipr = np.sum(prob ** 2) / (np.sum(prob)) ** 2
        iprs.append(ipr)

    # フェルミ準位近傍の状態のIPRを使用（バンドギャップ付近）
    mean_ipr = np.mean(iprs)
    # 正規化: 完全非局在化ではIPR=1/N → N*IPR=1 → δ_norm=1
    delta_norm = 1.0 / (n * mean_ipr)

    return mean_ipr, delta_norm, iprs


def compute_diamond_delta():
    """
    ダイヤモンドのδプロキシ。3D TBモデルからIPRを計算。
    オンサイトエネルギー差Δを含むモデル。
    大きなΔにより波動関数が各サイトに局在しやすくなる → δが小さい。
    """
    t = -2.0
    Delta = 5.0  # バンド構造と同じオンサイトエネルギー差
    a = 3.567
    d_vecs = np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]) * a / 4.0

    # 3x3x3 スーパーセル = 54原子
    nsc = 3
    sites = []
    site_types = []  # 0=A, 1=B
    for ix in range(nsc):
        for iy in range(nsc):
            for iz in range(nsc):
                pos_a = np.array([ix, iy, iz]) * a
                sites.append(pos_a)
                site_types.append(0)
                pos_b = pos_a + d_vecs[0]
                sites.append(pos_b)
                site_types.append(1)
    sites = np.array(sites)
    site_types = np.array(site_types)
    n = len(sites)

    # ハミルトニアン構築（周期境界条件付き）
    H = np.zeros((n, n))
    L = nsc * a

    # オンサイトエネルギー
    for i in range(n):
        H[i, i] = Delta / 2 if site_types[i] == 0 else -Delta / 2

    # ホッピング
    for i in range(n):
        for j in range(i + 1, n):
            dr = sites[j] - sites[i]
            for dim in range(3):
                dr[dim] -= L * np.round(dr[dim] / L)
            dist = np.linalg.norm(dr)
            bond_length = a * np.sqrt(3) / 4
            if abs(dist - bond_length) < 0.2:
                H[i, j] = t
                H[j, i] = t

    _, delta_proxy, _ = compute_ipr_from_eigenvectors(H)
    return delta_proxy


def compute_graphene_delta():
    """グラフェンのδプロキシ。2Dハニカム格子からIPRを計算。"""
    t = -2.7
    a = 2.46

    # 格子ベクトル
    a1 = a * np.array([1, 0])
    a2 = a * np.array([0.5, np.sqrt(3) / 2])

    # 6x6 スーパーセル = 72原子
    nsc = 6
    sites = []
    for ix in range(nsc):
        for iy in range(nsc):
            # A原子
            pos_a = ix * a1 + iy * a2
            sites.append(pos_a)
            # B原子
            delta = np.array([0, a / np.sqrt(3)])
            pos_b = pos_a + delta
            sites.append(pos_b)
    sites = np.array(sites)
    n = len(sites)

    # ハミルトニアン構築（周期境界条件）
    H = np.zeros((n, n))
    L1 = nsc * a1
    L2 = nsc * a2

    for i in range(n):
        for j in range(i + 1, n):
            # 最小イメージ
            dr = sites[j] - sites[i]
            # 格子座標に変換して最小イメージ適用
            best_dist = np.inf
            for n1 in [-1, 0, 1]:
                for n2 in [-1, 0, 1]:
                    dr_try = dr - n1 * L1 - n2 * L2
                    d_try = np.linalg.norm(dr_try)
                    if d_try < best_dist:
                        best_dist = d_try

            # C-C結合長 ≈ 1.42 Å
            if abs(best_dist - 1.42) < 0.15:
                H[i, j] = t
                H[j, i] = t

    _, delta_proxy, _ = compute_ipr_from_eigenvectors(H)
    return delta_proxy


def compute_chain1d_delta():
    """1D鎖のδプロキシ。"""
    t = -2.7
    n = 60  # 60サイトの鎖

    # 周期境界条件付きのハミルトニアン
    H = np.zeros((n, n))
    for i in range(n):
        H[i, (i + 1) % n] = t
        H[(i + 1) % n, i] = t

    _, delta_proxy, _ = compute_ipr_from_eigenvectors(H)
    return delta_proxy


def compute_c60_delta():
    """C60固体のδプロキシ。"""
    t_intra = -2.7
    adj, coords = build_c60_adjacency()
    n = adj.shape[0]
    H = t_intra * adj.astype(float)

    _, delta_proxy, _ = compute_ipr_from_eigenvectors(H)
    return delta_proxy


# ============================================================
# 6. バンドギャップとバンド幅の計算
# ============================================================
def compute_bandgap_and_width(E_bands):
    """バンド構造からバンドギャップとバンド幅を計算。"""
    val_band = E_bands[:, 0]
    con_band = E_bands[:, 1]

    Eg = np.min(con_band) - np.max(val_band)
    if Eg < 0:
        Eg = 0.0  # バンドが重なる場合はゼロギャップ

    W_val = np.max(val_band) - np.min(val_band)
    W_con = np.max(con_band) - np.min(con_band)
    W = max(W_val, W_con)

    return Eg, W


# ============================================================
# メイン計算・プロット
# ============================================================
def main():
    print("=" * 60)
    print("δ×D_eff 光学応答分類: タイトバインディング概念実証")
    print("=" * 60)

    # --- バンド構造計算 ---
    print("\n[1/4] バンド構造計算...")
    kd_dia, Eb_dia, tp_dia, tl_dia = diamond_bandstructure()
    kd_gra, Eb_gra, tp_gra, tl_gra = graphene_bandstructure()
    kd_1d, Eb_1d, tp_1d, tl_1d = chain1d_bandstructure()
    kd_c60, Eb_c60, tp_c60, tl_c60 = c60_bandstructure()

    # --- DOS計算 ---
    print("[2/4] 状態密度(DOS)計算...")
    eg_dia, dos_dia, en_dia = diamond_dos()
    eg_gra, dos_gra, en_gra = graphene_dos()
    eg_1d, dos_1d, en_1d = chain1d_dos()
    eg_c60, dos_c60, en_c60 = c60_solid_dos()

    # --- バンドギャップ・バンド幅 ---
    Eg_dia, W_dia = compute_bandgap_and_width(Eb_dia)
    Eg_gra, W_gra = compute_bandgap_and_width(Eb_gra)
    Eg_1d, W_1d = compute_bandgap_and_width(Eb_1d)
    Eg_c60, W_c60 = compute_bandgap_and_width(Eb_c60)

    # --- δプロキシ計算 ---
    print("[3/4] δプロキシ (IPR^-1) 計算...")
    delta_dia = compute_diamond_delta()
    delta_gra = compute_graphene_delta()
    delta_1d = compute_chain1d_delta()
    delta_c60 = compute_c60_delta()

    # --- 結果まとめ ---
    systems = [
        {"name": "Diamond (ダイヤモンド)", "Eg": Eg_dia, "W": W_dia, "delta": delta_dia,
         "D_eff": 0, "label": "ダイヤモンド", "optical": "透明"},
        {"name": "Graphene (グラフェン)", "Eg": Eg_gra, "W": W_gra, "delta": delta_gra,
         "D_eff": 2, "label": "グラフェン", "optical": "透明(単層)/黒(多層)"},
        {"name": "1D chain (SWCNT近似)", "Eg": Eg_1d, "W": W_1d, "delta": delta_1d,
         "D_eff": 1, "label": "1D鎖(SWCNT)", "optical": "色"},
        {"name": "C60 solid (C60固体)", "Eg": Eg_c60, "W": W_c60, "delta": delta_c60,
         "D_eff": 0, "label": "C60固体", "optical": "色"},
    ]

    print("\n" + "=" * 80)
    print(f"{'系':20s} {'Eg [eV]':>10s} {'W [eV]':>10s} {'δ (IPR⁻¹)':>12s} {'D_eff':>6s} {'光学応答':>10s}")
    print("-" * 80)
    for s in systems:
        print(f"{s['name']:20s} {s['Eg']:10.3f} {s['W']:10.3f} {s['delta']:12.2f} {s['D_eff']:6d} {s['optical']:>10s}")
    print("=" * 80)

    # --- δ-Eg 相関 ---
    deltas = np.array([s['delta'] for s in systems])
    Egs = np.array([s['Eg'] for s in systems])
    labels = [s['label'] for s in systems]

    # ピアソン相関係数
    r, p_val = pearsonr(deltas, Egs)
    print(f"\n[検証] δ-Eg ピアソン相関係数: r = {r:.4f} (p = {p_val:.4e})")

    if r < 0:
        print("  → δとEgの逆相関を確認: 非局在化度が大きいほどバンドギャップが小さい")
    else:
        print("  → 注意: 逆相関が見られず。モデルパラメータの確認が必要。")

    # --- δ×D_eff 光学分類の検証 ---
    print("\n[δ×D_eff 光学分類]")
    for s in systems:
        delta_Deff = s['delta'] * (s['D_eff'] + 1)  # D_eff=0でもゼロにならないよう+1
        print(f"  {s['label']:12s}: δ×(D_eff+1) = {delta_Deff:8.2f}, Eg = {s['Eg']:.2f} eV")
        if s['Eg'] > 3.1:
            category = "透明（広バンドギャップ）"
        elif s['Eg'] > 0 and s['D_eff'] <= 1:
            category = "色（選択吸収）"
        elif s['Eg'] == 0 and s['D_eff'] >= 2:
            category = "透明的（単層）/黒+光沢（多層）"
        else:
            category = "金属的光沢"
        print(f"    → 分類: {category}")

    # ============================================================
    # プロット
    # ============================================================
    print("\n[4/4] 図の生成...")

    # --- Fig A: バンド構造 (4パネル) ---
    fig_a, axes_a = plt.subplots(1, 4, figsize=(16, 4))
    fig_a.suptitle("バンド構造 (タイトバインディング)", fontsize=14, y=1.02)

    band_data = [
        (kd_dia, Eb_dia, tp_dia, tl_dia, "ダイヤモンド (sp3 TB)"),
        (kd_gra, Eb_gra, tp_gra, tl_gra, "グラフェン (π帯 TB)"),
        (kd_1d, Eb_1d, tp_1d, tl_1d, "1D鎖 (SWCNT近似)"),
        (kd_c60, Eb_c60, tp_c60, tl_c60, "C60固体 (HOMO/LUMO帯)"),
    ]
    colors_band = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"]

    for ax, (kd, Eb, tp, tl, title), color in zip(axes_a, band_data, colors_band):
        for band_idx in range(Eb.shape[1]):
            ax.plot(kd, Eb[:, band_idx], color=color, linewidth=1.5)
        ax.set_title(title, fontsize=10)
        ax.set_ylabel("E [eV]")
        ax.set_xlim(kd[0], kd[-1])
        ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')

        # 高対称点ティック
        ax.set_xticks(tp)
        ax.set_xticklabels(tl)
        for t_pos in tp:
            ax.axvline(t_pos, color='gray', linewidth=0.3, linestyle='-')
        ax.grid(axis='y', alpha=0.3)

    fig_a.tight_layout()
    fig_a.savefig(os.path.join(FIGDIR, "fig_a_bandstructure.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_a_bandstructure.png')}")

    # --- Fig B: DOS (4パネル) ---
    fig_b, axes_b = plt.subplots(1, 4, figsize=(16, 4))
    fig_b.suptitle("状態密度 (DOS)", fontsize=14, y=1.02)

    dos_data = [
        (eg_dia, dos_dia, "ダイヤモンド"),
        (eg_gra, dos_gra, "グラフェン"),
        (eg_1d, dos_1d, "1D鎖 (SWCNT近似)"),
        (eg_c60, dos_c60, "C60固体"),
    ]

    for ax, (egrid, dos, title), color in zip(axes_b, dos_data, colors_band):
        ax.fill_betweenx(egrid, 0, dos, alpha=0.3, color=color)
        ax.plot(dos, egrid, color=color, linewidth=1.2)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("DOS [a.u.]")
        ax.set_ylabel("E [eV]")
        ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
        ax.set_xlim(0, None)
        ax.grid(alpha=0.3)

    fig_b.tight_layout()
    fig_b.savefig(os.path.join(FIGDIR, "fig_b_dos.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_b_dos.png')}")

    # --- Fig C: δ vs Eg 散布図 + 相関直線 ---
    fig_c, ax_c = plt.subplots(figsize=(7, 5))
    ax_c.set_title("δ-Eg 逆相関の検証", fontsize=14)

    # 散布図
    markers = ['D', 'o', 's', '^']
    for i, s in enumerate(systems):
        ax_c.scatter(s['delta'], s['Eg'], s=120, marker=markers[i],
                     color=colors_band[i], zorder=5, edgecolors='black', linewidth=0.8)
        # ラベル
        offset = (8, 8) if i != 1 else (8, -15)
        ax_c.annotate(s['label'], (s['delta'], s['Eg']),
                      textcoords="offset points", xytext=offset, fontsize=10)

    # 線形フィット
    z = np.polyfit(deltas, Egs, 1)
    p = np.poly1d(z)
    delta_range = np.linspace(deltas.min() * 0.8, deltas.max() * 1.2, 100)
    ax_c.plot(delta_range, p(delta_range), 'k--', linewidth=1, alpha=0.5,
              label=f"線形フィット (r={r:.3f})")

    ax_c.set_xlabel("δ (非局在化プロキシ, IPR⁻¹)", fontsize=12)
    ax_c.set_ylabel("Eg [eV]", fontsize=12)
    ax_c.legend(fontsize=10)
    ax_c.grid(alpha=0.3)

    # δ×D_eff による光学分類領域をアノテーション
    ax_c.text(0.02, 0.98, f"ピアソン r = {r:.3f}\np = {p_val:.2e}",
              transform=ax_c.transAxes, fontsize=10,
              verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    fig_c.tight_layout()
    fig_c.savefig(os.path.join(FIGDIR, "fig_c_delta_Eg_correlation.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_c_delta_Eg_correlation.png')}")

    plt.close('all')

    print("\n" + "=" * 60)
    print("シミュレーション完了。")
    print(f"図は {FIGDIR} に保存されました。")
    print("=" * 60)

    return systems, r, p_val


if __name__ == "__main__":
    systems, r, p_val = main()
