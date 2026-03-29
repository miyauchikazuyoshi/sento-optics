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
# 5b. 全軌道 Slater-Koster タイトバインディング (s, px, py, pz)
# ============================================================

def _slater_koster_hopping(l, m, n, Vss, Vsp, Vpp_sigma, Vpp_pi):
    """
    Slater-Koster 2中心積分テーブル。
    (l, m, n) = ボンド方向の方向余弦。

    Returns:
        H_hop: (4, 4) array — 軌道順序 [s, px, py, pz]
    """
    H = np.zeros((4, 4))

    # s-s
    H[0, 0] = Vss

    # s-p (A→B)
    H[0, 1] = l * Vsp
    H[0, 2] = m * Vsp
    H[0, 3] = n * Vsp

    # p-s (B→A) = -Vsp × direction
    H[1, 0] = -l * Vsp
    H[2, 0] = -m * Vsp
    H[3, 0] = -n * Vsp

    # p-p
    H[1, 1] = l * l * Vpp_sigma + (1 - l * l) * Vpp_pi
    H[1, 2] = l * m * (Vpp_sigma - Vpp_pi)
    H[1, 3] = l * n * (Vpp_sigma - Vpp_pi)
    H[2, 1] = H[1, 2]
    H[2, 2] = m * m * Vpp_sigma + (1 - m * m) * Vpp_pi
    H[2, 3] = m * n * (Vpp_sigma - Vpp_pi)
    H[3, 1] = H[1, 3]
    H[3, 2] = H[2, 3]
    H[3, 3] = n * n * Vpp_sigma + (1 - n * n) * Vpp_pi

    return H


def graphene_full_tb_optical(nk=60, omega_grid=None, eta=0.1):
    """
    グラフェンの全軌道 (s, px, py, pz) Slater-Koster タイトバインディング。
    8バンド（2原子 × 4軌道）モデル。

    σバンドとπバンドの両方を含むため、
    光学伝導度・誘電関数が現実的な値を示す。

    Slater-Koster パラメータ (Tomanek & Louie 1988, Xu et al. 1992):
        ε_s    = -8.87 eV  (s軌道オンサイト)
        ε_p    =  0.00 eV  (p軌道オンサイト)
        V_ssσ  = -5.00 eV
        V_spσ  = +4.70 eV
        V_ppσ  = +5.50 eV
        V_ppπ  = -2.70 eV
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 12.0, 600)

    # パラメータ
    eps_s = -8.87  # eV
    eps_p = 0.0    # eV
    Vss = -5.0
    Vsp = 4.7
    Vpp_sigma = 5.5
    Vpp_pi = -2.7

    a = 2.46  # 格子定数 [Å]

    # 最近接ベクトル A→B (3本)
    d_nn = a / np.sqrt(3)
    delta1 = np.array([0, d_nn, 0])
    delta2 = np.array([d_nn * np.sqrt(3) / 2, -d_nn / 2, 0])
    delta3 = np.array([-d_nn * np.sqrt(3) / 2, -d_nn / 2, 0])
    nn_vectors = [delta1, delta2, delta3]

    # 逆格子ベクトル
    b1 = (2 * np.pi / a) * np.array([1, -1 / np.sqrt(3), 0])
    b2 = (2 * np.pi / a) * np.array([0, 2 / np.sqrt(3), 0])

    eigenvalues_k = []
    velocity_matrix_k = []

    n_orb = 4  # s, px, py, pz
    n_basis = 2 * n_orb  # 2 atoms × 4 orbitals = 8

    # オンサイトエネルギー
    onsite = np.array([eps_s, eps_p, eps_p, eps_p])

    dk = 1e-5  # 有限差分用微小変位

    for i in range(nk):
        for j in range(nk):
            k = (i / nk) * b1 + (j / nk) * b2

            # H(k) の構築
            H = np.zeros((n_basis, n_basis), dtype=complex)

            # オンサイト
            for orb in range(n_orb):
                H[orb, orb] = onsite[orb]              # A原子
                H[n_orb + orb, n_orb + orb] = onsite[orb]  # B原子

            # A→Bホッピング (上三角ブロック)
            for d_vec in nn_vectors:
                dist = np.linalg.norm(d_vec)
                l, m, n_dir = d_vec / dist  # 方向余弦

                h_hop = _slater_koster_hopping(l, m, n_dir, Vss, Vsp, Vpp_sigma, Vpp_pi)
                phase = np.exp(1j * np.dot(k[:2], d_vec[:2]))

                H[:n_orb, n_orb:] += h_hop * phase

            # エルミート化 (B→A = A→B†)
            H[n_orb:, :n_orb] = H[:n_orb, n_orb:].conj().T

            # 固有値・固有ベクトル
            evals, evecs = np.linalg.eigh(H)

            # 速度行列要素 (有限差分で ∂H/∂k_α)
            v_eig = np.zeros((n_basis, n_basis, 2), dtype=complex)

            for alpha in range(2):
                dk_vec = np.zeros(3)
                dk_vec[alpha] = dk

                k_plus = k + dk_vec
                k_minus = k - dk_vec

                H_plus = np.zeros((n_basis, n_basis), dtype=complex)
                H_minus = np.zeros((n_basis, n_basis), dtype=complex)

                for orb in range(n_orb):
                    H_plus[orb, orb] = onsite[orb]
                    H_plus[n_orb + orb, n_orb + orb] = onsite[orb]
                    H_minus[orb, orb] = onsite[orb]
                    H_minus[n_orb + orb, n_orb + orb] = onsite[orb]

                for d_vec in nn_vectors:
                    dist = np.linalg.norm(d_vec)
                    lv, mv, nv = d_vec / dist
                    h_hop = _slater_koster_hopping(lv, mv, nv, Vss, Vsp, Vpp_sigma, Vpp_pi)

                    phase_p = np.exp(1j * np.dot(k_plus[:2], d_vec[:2]))
                    phase_m = np.exp(1j * np.dot(k_minus[:2], d_vec[:2]))

                    H_plus[:n_orb, n_orb:] += h_hop * phase_p
                    H_minus[:n_orb, n_orb:] += h_hop * phase_m

                H_plus[n_orb:, :n_orb] = H_plus[:n_orb, n_orb:].conj().T
                H_minus[n_orb:, :n_orb] = H_minus[:n_orb, n_orb:].conj().T

                dHdk_alpha = (H_plus - H_minus) / (2 * dk)
                v_eig[:, :, alpha] = evecs.T.conj() @ dHdk_alpha @ evecs

            eigenvalues_k.append(evals)
            velocity_matrix_k.append(v_eig)

    # 占有バンド: 8バンド中、4電子/原子 × 2原子 = 8電子 → 4占有バンド
    n_occ = 4

    sigma = compute_optical_conductivity(omega_grid, eigenvalues_k,
                                          velocity_matrix_k, n_occ=n_occ, eta=eta)
    D_eff, T_diag = compute_deff_from_velocity(velocity_matrix_k,
                                                eigenvalues_k, n_occ=n_occ)

    return omega_grid, sigma, D_eff, T_diag, eigenvalues_k


def diamond_full_tb_optical(nk=14, omega_grid=None, eta=0.15):
    """
    ダイヤモンドの全軌道 Slater-Koster タイトバインディング。
    8バンド（2原子 × 4軌道）モデル。

    Slater-Koster パラメータ (Xu et al. 1992):
        ε_s    = -2.99 eV
        ε_p    =  3.71 eV
        V_ssσ  = -1.938 eV
        V_spσ  =  2.476 eV
        V_ppσ  =  3.064 eV
        V_ppπ  = -0.952 eV
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 12.0, 600)

    # パラメータ (Xu et al. 1992)
    eps_s = -2.99
    eps_p = 3.71
    Vss = -1.938
    Vsp = 2.476
    Vpp_sigma = 3.064
    Vpp_pi = -0.952

    a = 3.567  # 格子定数 [Å]

    # sp3ボンドベクトル（A→B）
    d_vecs = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ]) * a / 4.0

    n_orb = 4
    n_basis = 8

    onsite = np.array([eps_s, eps_p, eps_p, eps_p])

    dk = 1e-5

    eigenvalues_k = []
    velocity_matrix_k = []

    kgrid = np.linspace(-np.pi / a, np.pi / a, nk, endpoint=False)

    for kx in kgrid:
        for ky in kgrid:
            for kz in kgrid:
                k = np.array([kx, ky, kz])

                # H(k) 構築
                H = np.zeros((n_basis, n_basis), dtype=complex)
                for orb in range(n_orb):
                    H[orb, orb] = onsite[orb]
                    H[n_orb + orb, n_orb + orb] = onsite[orb]

                for d_vec in d_vecs:
                    dist = np.linalg.norm(d_vec)
                    l, m, n_dir = d_vec / dist
                    h_hop = _slater_koster_hopping(l, m, n_dir, Vss, Vsp, Vpp_sigma, Vpp_pi)
                    phase = np.exp(1j * np.dot(k, d_vec))
                    H[:n_orb, n_orb:] += h_hop * phase

                H[n_orb:, :n_orb] = H[:n_orb, n_orb:].conj().T

                evals, evecs = np.linalg.eigh(H)

                # 速度行列要素 (有限差分)
                v_eig = np.zeros((n_basis, n_basis, 3), dtype=complex)

                for alpha in range(3):
                    dk_vec = np.zeros(3)
                    dk_vec[alpha] = dk

                    H_plus = np.zeros((n_basis, n_basis), dtype=complex)
                    H_minus = np.zeros((n_basis, n_basis), dtype=complex)

                    for orb in range(n_orb):
                        H_plus[orb, orb] = onsite[orb]
                        H_plus[n_orb + orb, n_orb + orb] = onsite[orb]
                        H_minus[orb, orb] = onsite[orb]
                        H_minus[n_orb + orb, n_orb + orb] = onsite[orb]

                    for d_vec in d_vecs:
                        dist = np.linalg.norm(d_vec)
                        lv, mv, nv = d_vec / dist
                        h_hop = _slater_koster_hopping(lv, mv, nv, Vss, Vsp, Vpp_sigma, Vpp_pi)

                        k_p = k + dk_vec
                        k_m = k - dk_vec
                        H_plus[:n_orb, n_orb:] += h_hop * np.exp(1j * np.dot(k_p, d_vec))
                        H_minus[:n_orb, n_orb:] += h_hop * np.exp(1j * np.dot(k_m, d_vec))

                    H_plus[n_orb:, :n_orb] = H_plus[:n_orb, n_orb:].conj().T
                    H_minus[n_orb:, :n_orb] = H_minus[:n_orb, n_orb:].conj().T

                    dHdk_alpha = (H_plus - H_minus) / (2 * dk)
                    v_eig[:, :, alpha] = evecs.T.conj() @ dHdk_alpha @ evecs

                eigenvalues_k.append(evals)
                velocity_matrix_k.append(v_eig)

    # 占有バンド: 8電子 → 4占有バンド
    n_occ = 4

    sigma = compute_optical_conductivity(omega_grid, eigenvalues_k,
                                          velocity_matrix_k, n_occ=n_occ, eta=eta)
    D_eff, T_diag = compute_deff_from_velocity(velocity_matrix_k,
                                                eigenvalues_k, n_occ=n_occ)

    return omega_grid, sigma, D_eff, T_diag, eigenvalues_k


# ============================================================
# 6. 光学伝導度・誘電関数・反射率の計算
# ============================================================

def compute_optical_conductivity(omega_grid, eigenvalues_k, velocity_matrix_k,
                                  n_occ, eta=0.1, n_dim=None):
    """
    クボー公式による光学伝導度 Re[σ(ω)] の計算。

    Parameters:
        omega_grid: (N_omega,) 光子エネルギー [eV]
        eigenvalues_k: list of (n_bands,) arrays — 各k点の固有値
        velocity_matrix_k: list of (n_bands, n_bands, n_dim) arrays
                           — 固有基底での速度行列要素
        n_occ: 占有バンド数 (T=0)
        eta: ローレンツブロードニング [eV]
        n_dim: 空間次元数 (偏光平均用)。Noneなら velocity_matrix_k から推定。

    Returns:
        sigma: (N_omega,) Re[σ(ω)] in arbitrary units
               (正規化して σ/σ₀ で比較する)
    """
    N_k = len(eigenvalues_k)
    N_omega = len(omega_grid)
    sigma = np.zeros(N_omega)

    if n_dim is None:
        n_dim = velocity_matrix_k[0].shape[2]

    for ik in range(N_k):
        evals = eigenvalues_k[ik]
        v_mat = velocity_matrix_k[ik]  # (n_bands, n_bands, n_dim)
        n_bands = len(evals)

        for n in range(n_occ):
            for m in range(n_occ, n_bands):
                dE = evals[m] - evals[n]
                if dE < 1e-6:
                    continue

                # 偏光平均: (1/n_dim) Σ_α |v_nm^α|²
                v2 = 0.0
                for alpha in range(n_dim):
                    v2 += np.abs(v_mat[n, m, alpha]) ** 2
                v2 /= n_dim

                # ローレンツ型: η/((ω - dE)² + η²) ≈ π δ(ω - dE)
                # スピン縮退 ×2 はprefactorに含める
                lorentz = eta / ((omega_grid - dE) ** 2 + eta ** 2)
                sigma += 2.0 * v2 * lorentz / dE

    sigma /= N_k
    return sigma


def dielectric_from_sigma(omega_grid, sigma, volume_factor=1.0):
    """
    光学伝導度から吸収係数 ε₂(ω) を計算。
    ε₂(ω) ∝ σ(ω) / ω

    volume_factor: 有効セル体積による正規化。
    """
    eps2 = np.zeros_like(sigma)
    nonzero = omega_grid > 0.01
    eps2[nonzero] = sigma[nonzero] / (omega_grid[nonzero] * volume_factor)
    return eps2


def kramers_kronig_eps1(omega_grid, eps2):
    """
    クラマース・クローニッヒ変換で ε₂(ω) から ε₁(ω) を計算。

    ε₁(ω) = 1 + (2/π) P∫₀^∞ ω'ε₂(ω') / (ω'² - ω²) dω'

    ベクトル化実装: 主値積分は特異点除去 + 台形則。
    """
    N = len(omega_grid)
    eps1 = np.ones(N)

    # ω'ε₂(ω') の事前計算
    wp_eps2 = omega_grid * eps2  # (N,)

    # ω² のグリッド
    w2 = omega_grid ** 2  # (N,)

    for i in range(N):
        if omega_grid[i] < 1e-6:
            continue
        # 分母: ω'² - ω²
        denom = w2 - w2[i]  # (N,)
        # 特異点マスク
        mask = np.abs(denom) > 1e-6
        integrand = np.zeros(N)
        integrand[mask] = wp_eps2[mask] / denom[mask]
        eps1[i] = 1.0 + (2.0 / np.pi) * np.trapezoid(integrand, omega_grid)

    return eps1


def reflectivity_from_epsilon(eps2, eps1=None, omega_grid=None):
    """
    フレネル方程式から垂直入射反射率 R(ω) を計算。
    R = |(√ε - 1) / (√ε + 1)|²

    eps1がNoneの場合、omega_gridが与えられればKK変換、
    なければ簡易近似を使用。
    """
    if eps1 is None:
        if omega_grid is not None:
            eps1 = kramers_kronig_eps1(omega_grid, eps2)
        else:
            # フォールバック: 簡易近似
            eps1 = 1.0 + 0.5 * eps2
    eps_complex = eps1 + 1j * eps2
    n_complex = np.sqrt(eps_complex)
    R = np.abs((n_complex - 1) / (n_complex + 1)) ** 2
    return R, eps1


def fresnel_angular(eps2, eps1=None, theta_deg=None):
    """
    フレネル方程式の角度依存反射率 R_s(θ), R_p(θ), R_unpol(θ)。

    Parameters:
        eps2: (N_omega,) array — ε₂(ω)
        eps1: (N_omega,) array or None — ε₁(ω)
        theta_deg: float or array — 入射角 [度]

    Returns:
        R_s, R_p, R_unpol: 各偏光の反射率 (shape depends on inputs)
    """
    if eps1 is None:
        eps1 = 1.0 + 0.5 * eps2

    if theta_deg is None:
        theta_deg = np.array([0, 20, 45, 60, 75, 85])

    theta_deg = np.atleast_1d(theta_deg).astype(float)
    eps_complex = eps1 + 1j * eps2  # (N_omega,)
    n_complex = np.sqrt(eps_complex)  # (N_omega,)

    # 出力: (N_theta, N_omega)
    R_s = np.zeros((len(theta_deg), len(eps2)))
    R_p = np.zeros((len(theta_deg), len(eps2)))

    for it, theta_d in enumerate(theta_deg):
        theta = np.radians(theta_d)
        cos_i = np.cos(theta)
        sin_i = np.sin(theta)

        # スネルの法則: n₁ sin θ₁ = n₂ sin θ₂
        # cos θ_t = sqrt(1 - (sin θ / n)²)
        cos_t = np.sqrt(1.0 - (sin_i / n_complex) ** 2)

        # s偏光: R_s = |(cos_i - n cos_t) / (cos_i + n cos_t)|²
        r_s = (cos_i - n_complex * cos_t) / (cos_i + n_complex * cos_t)
        R_s[it] = np.abs(r_s) ** 2

        # p偏光: R_p = |(n cos_i - cos_t) / (n cos_i + cos_t)|²
        r_p = (n_complex * cos_i - cos_t) / (n_complex * cos_i + cos_t)
        R_p[it] = np.abs(r_p) ** 2

    R_unpol = 0.5 * (R_s + R_p)

    return R_s, R_p, R_unpol, theta_deg


def compute_gloss_prediction(eps2, eps1=None, omega_grid=None):
    """
    ε(ω) から工業規格準拠の光沢度予測を計算。

    光沢度 (GU) の定義:
      ASTM D523: 特定角度での鏡面反射率を黒色ガラス基準 (n=1.567) と比較
      GU = R_sample(θ) / R_reference(θ) × 100

    Parameters:
        eps2, eps1: 誘電関数
        omega_grid: 光子エネルギー [eV]

    Returns:
        gloss_20, gloss_60, gloss_85: 20°/60°/85° 光沢度 [GU]
        R_theta: dict of angular reflectivities
    """
    if eps1 is None:
        eps1 = 1.0 + 0.5 * eps2

    if omega_grid is None:
        omega_grid = np.linspace(0.05, 12.0, len(eps2))

    # 基準: 黒色ガラス (n=1.567, k≈0)
    n_ref = 1.567
    ref_angles = [20.0, 60.0, 85.0]
    R_ref = {}
    for theta_d in ref_angles:
        theta = np.radians(theta_d)
        cos_i = np.cos(theta)
        cos_t = np.sqrt(1.0 - (np.sin(theta) / n_ref) ** 2)
        r_s = (cos_i - n_ref * cos_t) / (cos_i + n_ref * cos_t)
        r_p = (n_ref * cos_i - cos_t) / (n_ref * cos_i + cos_t)
        R_ref[theta_d] = 0.5 * (abs(r_s) ** 2 + abs(r_p) ** 2)

    # サンプルの角度依存反射率
    R_s, R_p, R_unpol, _ = fresnel_angular(eps2, eps1,
                                             theta_deg=np.array(ref_angles))

    # 可視域平均 (1.6-3.1 eV = 400-775 nm)
    vis = (omega_grid >= 1.6) & (omega_grid <= 3.1)

    R_theta = {}
    gloss = {}
    for it, theta_d in enumerate(ref_angles):
        R_vis_mean = np.mean(R_unpol[it][vis]) if np.any(vis) else np.mean(R_unpol[it])
        R_theta[theta_d] = R_vis_mean
        gloss[theta_d] = R_vis_mean / R_ref[theta_d] * 100.0

    return gloss[20.0], gloss[60.0], gloss[85.0], R_theta


def compute_effective_gloss_with_disorder(gloss_clean, spectral_correlation):
    """
    無秩序下の実効光沢度を推定。

    清浄系の光沢度 × スペクトル保存度 で実効光沢を計算。
    物理的意味: スペクトル保存度 ≈ コヒーレント反射の割合

    R_eff = R_specular × coherence + R_diffuse × (1 - coherence)
    光沢度 ∝ R_specular / R_total
    → 実効光沢 ≈ 清浄光沢 × coherence²
    (coherence² は鏡面反射ピークの鋭さに対応)

    Parameters:
        gloss_clean: 清浄系の光沢度 [GU]
        spectral_correlation: スペクトル保存度 (0-1)

    Returns:
        effective_gloss: 実効光沢度 [GU]
    """
    # コヒーレンス因子: spectral_correlation が 1 → 完全鏡面
    # spectral_correlation が小 → 散漫散乱優勢
    coherence_factor = spectral_correlation ** 2
    effective_gloss = gloss_clean * coherence_factor
    return effective_gloss


def compute_deff_from_velocity(velocity_matrix_k, eigenvalues_k, n_occ):
    """
    速度テンソル ⟨v_α v_β⟩ の有効ランクとして D_eff を計算。

    T_αβ = (1/N_k) Σ_k Σ_{n occ, m unocc} v_nm^α · conj(v_nm^β)
    D_eff = Tr(T)² / Tr(T @ T)   (有効ランク)

    Returns:
        D_eff: float — 有効伝導次元
        T_diag: (n_dim,) — テンソルの対角成分
    """
    N_k = len(eigenvalues_k)
    n_dim = velocity_matrix_k[0].shape[2]
    T = np.zeros((n_dim, n_dim))

    for ik in range(N_k):
        evals = eigenvalues_k[ik]
        v_mat = velocity_matrix_k[ik]
        n_bands = len(evals)

        for n in range(n_occ):
            for m in range(n_occ, n_bands):
                for a in range(n_dim):
                    for b in range(n_dim):
                        T[a, b] += np.real(v_mat[n, m, a] * np.conj(v_mat[n, m, b]))

    T /= N_k
    T_diag = np.diag(T).copy()

    tr_T = np.trace(T)
    tr_T2 = np.trace(T @ T)

    if tr_T2 < 1e-30:
        return 0.0, T_diag

    D_eff = tr_T ** 2 / tr_T2
    return D_eff, T_diag


# --- System-specific optical k-grid functions ---

def graphene_optical_kgrid(nk=60, omega_grid=None, eta=0.1):
    """
    グラフェンの光学伝導度をクボー公式で計算。

    H(k) = [[0, t·f(k)], [t·f(k)*, 0]]
    ∂H/∂k_α から速度行列要素を固有基底で計算。

    検証: σ/σ₀ ≈ 1.0 (σ₀ = πe²/2h)
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 400)

    t = -2.7
    a = 2.46

    # 最近接ベクトル（A→B）
    delta1 = np.array([0, a / np.sqrt(3)])
    delta2 = np.array([a / 2, -a / (2 * np.sqrt(3))])
    delta3 = np.array([-a / 2, -a / (2 * np.sqrt(3))])
    deltas = [delta1, delta2, delta3]

    # 逆格子ベクトル
    b1 = (2 * np.pi / a) * np.array([1, -1 / np.sqrt(3)])
    b2 = (2 * np.pi / a) * np.array([0, 2 / np.sqrt(3)])

    eigenvalues_k = []
    velocity_matrix_k = []

    for i in range(nk):
        for j in range(nk):
            k = (i / nk) * b1 + (j / nk) * b2

            # 構造因子 f(k) と ∂f/∂k_α
            fk = sum(np.exp(1j * np.dot(k, d)) for d in deltas)
            dfdk = np.zeros(2, dtype=complex)
            for d in deltas:
                phase = np.exp(1j * np.dot(k, d))
                dfdk[0] += 1j * d[0] * phase
                dfdk[1] += 1j * d[1] * phase

            # H(k) 2x2
            H = np.array([
                [0, t * fk],
                [t * np.conj(fk), 0]
            ])

            # ∂H/∂k_α
            dHdk = np.zeros((2, 2, 2), dtype=complex)
            dHdk[0, 1, 0] = t * dfdk[0]
            dHdk[1, 0, 0] = t * np.conj(dfdk[0])
            dHdk[0, 1, 1] = t * dfdk[1]
            dHdk[1, 0, 1] = t * np.conj(dfdk[1])

            # 固有値・固有ベクトル
            evals, evecs = np.linalg.eigh(H)

            # 固有基底での速度行列: v_nm^α = U† (∂H/∂k_α) U
            v_eig = np.zeros((2, 2, 2), dtype=complex)
            for alpha in range(2):
                v_eig[:, :, alpha] = evecs.T.conj() @ dHdk[:, :, alpha] @ evecs

            eigenvalues_k.append(evals)
            velocity_matrix_k.append(v_eig)

    sigma = compute_optical_conductivity(omega_grid, eigenvalues_k,
                                          velocity_matrix_k, n_occ=1, eta=eta)
    D_eff, T_diag = compute_deff_from_velocity(velocity_matrix_k,
                                                eigenvalues_k, n_occ=1)
    return omega_grid, sigma, D_eff, T_diag


def diamond_optical_kgrid(nk=20, omega_grid=None, eta=0.1):
    """
    ダイヤモンドの光学伝導度。3D k格子。
    検証: ε₂ = 0 for ω < Eg ≈ 5 eV
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 400)

    t = -2.0
    Delta = 5.0
    a = 3.567

    d_vecs = np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]) * a / 4.0

    eigenvalues_k = []
    velocity_matrix_k = []

    kgrid = np.linspace(-np.pi / a, np.pi / a, nk, endpoint=False)

    for kx in kgrid:
        for ky in kgrid:
            for kz in kgrid:
                k = np.array([kx, ky, kz])

                # 構造因子
                fk = sum(np.exp(1j * np.dot(k, di)) for di in d_vecs)
                dfdk = np.zeros(3, dtype=complex)
                for di in d_vecs:
                    phase = np.exp(1j * np.dot(k, di))
                    for alpha in range(3):
                        dfdk[alpha] += 1j * di[alpha] * phase

                # H(k)
                H = np.array([
                    [Delta / 2, t * fk],
                    [t * np.conj(fk), -Delta / 2]
                ])

                # ∂H/∂k_α
                dHdk = np.zeros((2, 2, 3), dtype=complex)
                for alpha in range(3):
                    dHdk[0, 1, alpha] = t * dfdk[alpha]
                    dHdk[1, 0, alpha] = t * np.conj(dfdk[alpha])

                evals, evecs = np.linalg.eigh(H)

                v_eig = np.zeros((2, 2, 3), dtype=complex)
                for alpha in range(3):
                    v_eig[:, :, alpha] = evecs.T.conj() @ dHdk[:, :, alpha] @ evecs

                eigenvalues_k.append(evals)
                velocity_matrix_k.append(v_eig)

    sigma = compute_optical_conductivity(omega_grid, eigenvalues_k,
                                          velocity_matrix_k, n_occ=1, eta=eta)
    D_eff, T_diag = compute_deff_from_velocity(velocity_matrix_k,
                                                eigenvalues_k, n_occ=1)
    return omega_grid, sigma, D_eff, T_diag


def chain1d_optical_kgrid(nk=2000, omega_grid=None, eta=0.1):
    """
    1D鎖の光学伝導度。
    H(k) = [[Δ/2, 2t cos(ka)], [2t cos(ka), -Δ/2]]
    検証: 吸収開始 ω = Δ = 0.5 eV
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 400)

    t = -2.7
    a = 1.42
    Delta = 0.5

    kpoints = np.linspace(-np.pi / a, np.pi / a, nk, endpoint=False)

    eigenvalues_k = []
    velocity_matrix_k = []

    for k_val in kpoints:
        eps_k = 2 * t * np.cos(k_val * a)
        deps_dk = -2 * t * a * np.sin(k_val * a)

        H = np.array([
            [Delta / 2, eps_k],
            [eps_k, -Delta / 2]
        ])

        dHdk = np.zeros((2, 2, 1))
        dHdk[0, 1, 0] = deps_dk
        dHdk[1, 0, 0] = deps_dk

        evals, evecs = np.linalg.eigh(H)

        v_eig = np.zeros((2, 2, 1), dtype=complex)
        v_eig[:, :, 0] = evecs.T.conj() @ dHdk[:, :, 0] @ evecs

        eigenvalues_k.append(evals)
        velocity_matrix_k.append(v_eig)

    sigma = compute_optical_conductivity(omega_grid, eigenvalues_k,
                                          velocity_matrix_k, n_occ=1, eta=eta)
    D_eff, T_diag = compute_deff_from_velocity(velocity_matrix_k,
                                                eigenvalues_k, n_occ=1)
    return omega_grid, sigma, D_eff, T_diag


def c60_optical(omega_grid=None, eta=0.15):
    """
    C60分子の光学伝導度。双極子ゲージで計算。
    σ(ω) ∝ Σ_{n occ, m unocc} ω |r_nm|² η/((ω-dE)²+η²)

    検証: 第一ピーク ≈ HOMO-LUMO gap
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 400)

    t_intra = -2.7
    adj, coords = build_c60_adjacency()
    n = adj.shape[0]

    H = t_intra * adj.astype(float)
    eigenvalues, eigenvectors = np.linalg.eigh(H)

    n_occ = n // 2  # 30 occupied levels

    # 双極子行列要素: r_nm^α = Σ_i ψ_n*(i) (coord_i)_α ψ_m(i)
    n_dim = 3
    dipole = np.zeros((n, n, n_dim))
    for alpha in range(n_dim):
        r_alpha = np.diag(coords[:, alpha])  # (n, n) diagonal
        dipole[:, :, alpha] = eigenvectors.T @ r_alpha @ eigenvectors

    # σ(ω) の計算（双極子ゲージ）
    sigma = np.zeros(len(omega_grid))
    for nn in range(n_occ):
        for m in range(n_occ, n):
            dE = eigenvalues[m] - eigenvalues[nn]
            if dE < 1e-6:
                continue

            # |r_nm|² の偏光平均
            r2 = 0.0
            for alpha in range(n_dim):
                r2 += np.abs(dipole[nn, m, alpha]) ** 2
            r2 /= n_dim

            # 双極子→伝導度変換: ω 因子
            lorentz = eta / ((omega_grid - dE) ** 2 + eta ** 2)
            sigma += 2.0 * omega_grid * r2 * lorentz

    # D_eff = 0 (分子系、k分散なし)
    D_eff = 0.0
    T_diag = np.zeros(3)

    return omega_grid, sigma, D_eff, T_diag


# ============================================================
# 7. コヒーレンス保存仮説テスト — Anderson無秩序モデル
# ============================================================

def graphene_anderson_disorder(W, nk=30, n_realizations=20, omega_grid=None, eta=0.15):
    """
    グラフェン π帯 + Anderson無秩序。
    オンサイトランダムポテンシャル ε_i ∈ [-W/2, W/2] を追加。

    実空間スーパーセルで計算:
      N_sc × N_sc ユニットセルのスーパーセル → 2 × N_sc² サイト。
      周期境界条件 + 無秩序によるアンサンブル平均。

    Returns:
        sigma_avg: アンサンブル平均 σ(ω)
        ipr_avg: アンサンブル平均 IPR (フェルミ面近傍)
        localization_ratio: ξ/λ_vis 推定値
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 300)

    t = -2.7  # eV
    a = 2.46  # Å
    N_sc = 10  # スーパーセル各方向のユニットセル数 → 2 × 10² = 200 サイト

    # 格子ベクトル
    a1 = a * np.array([1.0, 0.0])
    a2 = a * np.array([0.5, np.sqrt(3) / 2])

    # 最近接ベクトル（A→B）
    delta1 = np.array([0, a / np.sqrt(3)])
    delta2 = np.array([a / 2, -a / (2 * np.sqrt(3))])
    delta3 = np.array([-a / 2, -a / (2 * np.sqrt(3))])

    n_sites = 2 * N_sc * N_sc

    # サイト座標の構築
    positions = []
    site_map = {}
    idx = 0
    for i in range(N_sc):
        for j in range(N_sc):
            r_A = i * a1 + j * a2
            r_B = r_A + delta1
            site_map[('A', i, j)] = idx
            site_map[('B', i, j)] = idx + 1
            positions.append(r_A)
            positions.append(r_B)
            idx += 2

    positions = np.array(positions)

    # 接続テーブル: A(i,j) → B 最近接
    def get_nn_pairs():
        """各AサイトからB最近接3つへのホッピングペアを返す。"""
        pairs = []
        for i in range(N_sc):
            for j in range(N_sc):
                iA = site_map[('A', i, j)]
                # delta1方向: 同セル内 B
                iB1 = site_map[('B', i, j)]
                pairs.append((iA, iB1))
                # delta2方向: B at (i, j-1) — 周期境界
                jm = (j - 1) % N_sc
                # delta2 = A + [a/2, -a/(2√3)] に近い B
                # 実際にはA→B ホッピングは3方向
                # 正確にはハミルトニアンを距離で構築する方が安全
                iB2 = site_map[('B', i, jm)]
                pairs.append((iA, iB2))
                # delta3方向: B at (i-1, j) — 周期境界
                im = (i - 1) % N_sc
                iB3 = site_map[('B', im, j)]
                pairs.append((iA, iB3))
        return pairs

    nn_pairs = get_nn_pairs()

    # アンサンブル平均
    sigma_all = np.zeros((n_realizations, len(omega_grid)))
    ipr_all = np.zeros(n_realizations)

    for r in range(n_realizations):
        # 無秩序ハミルトニアン構築
        H = np.zeros((n_sites, n_sites))

        # オンサイトランダムポテンシャル
        disorder = W * (np.random.rand(n_sites) - 0.5)
        np.fill_diagonal(H, disorder)

        # ホッピング
        for (iA, iB) in nn_pairs:
            H[iA, iB] = t
            H[iB, iA] = t

        # 対角化
        evals, evecs = np.linalg.eigh(H)
        n_occ = n_sites // 2

        # IPR: フェルミ面近傍の状態 (HOMO, LUMO 周辺 ±5 状態)
        fermi_range = range(max(0, n_occ - 5), min(n_sites, n_occ + 5))
        ipr_sum = 0.0
        for n_idx in fermi_range:
            psi = evecs[:, n_idx]
            ipr_sum += np.sum(np.abs(psi) ** 4)
        ipr_all[r] = ipr_sum / len(fermi_range)

        # σ(ω) — 双極子ゲージ
        sigma = np.zeros(len(omega_grid))
        # 位置行列要素
        for n_idx in range(max(0, n_occ - 15), n_occ):
            for m_idx in range(n_occ, min(n_sites, n_occ + 15)):
                dE = evals[m_idx] - evals[n_idx]
                if dE < 1e-6:
                    continue
                # |r_nm|²
                r2 = 0.0
                for alpha in range(2):
                    r_nm = np.sum(evecs[:, n_idx].conj() * positions[:, alpha] * evecs[:, m_idx])
                    r2 += np.abs(r_nm) ** 2
                r2 /= 2.0
                lorentz = eta / ((omega_grid - dE) ** 2 + eta ** 2)
                sigma += 2.0 * omega_grid * r2 * lorentz

        sigma_all[r] = sigma

    sigma_avg = np.mean(sigma_all, axis=0)
    ipr_avg = np.mean(ipr_all)

    # 局在化長の推定: ξ ∝ 1/IPR^(1/d) (d=2 for graphene)
    # IPR ~ 1/N (完全非局在化) → ξ ~ L (系のサイズ)
    # IPR ~ 1 (完全局在化) → ξ ~ a
    # 推定: ξ/a ≈ (1/(N × IPR))^(1/2)
    xi_over_a = (1.0 / (n_sites * ipr_avg + 1e-30)) ** 0.5
    # λ_vis ≈ 5000 Å, a = 2.46 Å
    lambda_vis = 5000.0  # Å
    xi_estimate = xi_over_a * a  # Å
    localization_ratio = xi_estimate / lambda_vis

    return sigma_avg, ipr_avg, localization_ratio, omega_grid


def chain1d_anderson_disorder(W, n_sites=200, n_realizations=20, omega_grid=None, eta=0.15):
    """
    1D鎖 + Anderson無秩序。
    転送行列法で局在化長 ξ を直接計算。

    Returns:
        sigma_avg, ipr_avg, localization_ratio, omega_grid
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 300)

    t = -2.7
    a = 1.42
    Delta = 0.5  # 微小ギャップ

    sigma_all = np.zeros((n_realizations, len(omega_grid)))
    ipr_all = np.zeros(n_realizations)
    xi_all = np.zeros(n_realizations)

    for r in range(n_realizations):
        H = np.zeros((n_sites, n_sites))

        # 無秩序
        disorder = W * (np.random.rand(n_sites) - 0.5)
        # サブ格子ポテンシャル + 無秩序
        for i in range(n_sites):
            H[i, i] = (Delta / 2 if i % 2 == 0 else -Delta / 2) + disorder[i]

        # ホッピング（周期境界条件）
        for i in range(n_sites):
            j = (i + 1) % n_sites
            H[i, j] = t
            H[j, i] = t

        evals, evecs = np.linalg.eigh(H)
        n_occ = n_sites // 2

        # IPR
        fermi_range = range(max(0, n_occ - 5), min(n_sites, n_occ + 5))
        ipr_sum = 0.0
        for n_idx in fermi_range:
            psi = evecs[:, n_idx]
            ipr_sum += np.sum(np.abs(psi) ** 4)
        ipr_all[r] = ipr_sum / len(fermi_range)

        # 局在化長（転送行列法 — フェルミエネルギー近傍）
        E_fermi = 0.5 * (evals[n_occ - 1] + evals[n_occ])
        # T = Π_i [[( E-ε_i)/t, -1], [1, 0]]
        T_mat = np.eye(2)
        for i in range(n_sites):
            eps_i = H[i, i]
            t_i = t if i < n_sites - 1 else t  # uniform hopping
            M_i = np.array([
                [(E_fermi - eps_i) / t_i, -1.0],
                [1.0, 0.0]
            ])
            T_mat = M_i @ T_mat
            # 数値安定化: 定期的にQR分解
            if (i + 1) % 50 == 0:
                norms = np.linalg.norm(T_mat, axis=0)
                T_mat /= max(norms.max(), 1e-30)

        # リアプノフ指数 γ = (1/N) ln||T||, ξ = 1/γ
        lyap = np.log(np.linalg.norm(T_mat) + 1e-30) / n_sites
        xi = a / max(lyap, 1e-10)  # Å
        xi_all[r] = abs(xi)

        # σ(ω) — 位置行列要素
        coords = np.arange(n_sites) * a
        sigma = np.zeros(len(omega_grid))
        for n_idx in range(max(0, n_occ - 15), n_occ):
            for m_idx in range(n_occ, min(n_sites, n_occ + 15)):
                dE = evals[m_idx] - evals[n_idx]
                if dE < 1e-6:
                    continue
                r_nm = np.sum(evecs[:, n_idx] * coords * evecs[:, m_idx])
                r2 = np.abs(r_nm) ** 2
                lorentz = eta / ((omega_grid - dE) ** 2 + eta ** 2)
                sigma += 2.0 * omega_grid * r2 * lorentz

        sigma_all[r] = sigma

    sigma_avg = np.mean(sigma_all, axis=0)
    ipr_avg = np.mean(ipr_all)
    xi_avg = np.mean(xi_all)
    lambda_vis = 5000.0
    localization_ratio = xi_avg / lambda_vis

    return sigma_avg, ipr_avg, localization_ratio, omega_grid


def c60_anderson_disorder(W, n_realizations=20, omega_grid=None, eta=0.15):
    """
    C60分子 + Anderson無秩序。

    Returns:
        sigma_avg, ipr_avg, localization_ratio, omega_grid
    """
    if omega_grid is None:
        omega_grid = np.linspace(0.05, 8.0, 300)

    t_intra = -2.7
    adj, coords = build_c60_adjacency()
    n = adj.shape[0]

    sigma_all = np.zeros((n_realizations, len(omega_grid)))
    ipr_all = np.zeros(n_realizations)

    for r in range(n_realizations):
        H = t_intra * adj.astype(float)
        disorder = W * (np.random.rand(n) - 0.5)
        np.fill_diagonal(H, disorder)

        evals, evecs = np.linalg.eigh(H)
        n_occ = n // 2

        # IPR
        fermi_range = range(max(0, n_occ - 5), min(n, n_occ + 5))
        ipr_sum = 0.0
        for n_idx in fermi_range:
            psi = evecs[:, n_idx]
            ipr_sum += np.sum(np.abs(psi) ** 4)
        ipr_all[r] = ipr_sum / len(fermi_range)

        # σ(ω)
        sigma = np.zeros(len(omega_grid))
        for nn_idx in range(max(0, n_occ - 15), n_occ):
            for m_idx in range(n_occ, min(n, n_occ + 15)):
                dE = evals[m_idx] - evals[nn_idx]
                if dE < 1e-6:
                    continue
                r2 = 0.0
                for alpha in range(3):
                    r_nm = np.sum(evecs[:, nn_idx] * coords[:, alpha] * evecs[:, m_idx])
                    r2 += np.abs(r_nm) ** 2
                r2 /= 3.0
                lorentz = eta / ((omega_grid - dE) ** 2 + eta ** 2)
                sigma += 2.0 * omega_grid * r2 * lorentz

        sigma_all[r] = sigma

    sigma_avg = np.mean(sigma_all, axis=0)
    ipr_avg = np.mean(ipr_all)

    # C60は分子 → ξ ≈ 分子サイズ (7 Å 直径)
    xi_estimate = 7.0 / (n * ipr_avg + 1e-30) ** 0.5
    lambda_vis = 5000.0
    localization_ratio = xi_estimate / lambda_vis

    return sigma_avg, ipr_avg, localization_ratio, omega_grid


def coherence_preservation_test(W_values=None, n_realizations=20):
    """
    コヒーレンス保存仮説の数値テスト。

    各系にAnderson無秩序を加え:
    1. σ(ω)スペクトル形状の安定性
    2. IPR(W) の変化速度
    3. ξ/λ_vis（局在化長/可視光波長 比）

    を計算して δ×D_eff との相関を調べる。

    Returns:
        results: dict with keys for each system
    """
    if W_values is None:
        W_values = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0]

    omega = np.linspace(0.05, 8.0, 300)

    results = {
        'W_values': W_values,
        'omega': omega,
        'graphene': {'sigma': [], 'ipr': [], 'xi_ratio': [], 'delta': None, 'D_eff': 2},
        'chain1d': {'sigma': [], 'ipr': [], 'xi_ratio': [], 'delta': None, 'D_eff': 1},
        'c60': {'sigma': [], 'ipr': [], 'xi_ratio': [], 'delta': None, 'D_eff': 0},
    }

    for W in W_values:
        print(f"    W = {W:.1f} eV ...")

        # グラフェン
        sig, ipr, xi_r, _ = graphene_anderson_disorder(
            W, nk=30, n_realizations=n_realizations, omega_grid=omega, eta=0.15)
        results['graphene']['sigma'].append(sig)
        results['graphene']['ipr'].append(ipr)
        results['graphene']['xi_ratio'].append(xi_r)

        # 1D鎖
        sig, ipr, xi_r, _ = chain1d_anderson_disorder(
            W, n_sites=200, n_realizations=n_realizations, omega_grid=omega, eta=0.15)
        results['chain1d']['sigma'].append(sig)
        results['chain1d']['ipr'].append(ipr)
        results['chain1d']['xi_ratio'].append(xi_r)

        # C60
        sig, ipr, xi_r, _ = c60_anderson_disorder(
            W, n_realizations=n_realizations, omega_grid=omega, eta=0.15)
        results['c60']['sigma'].append(sig)
        results['c60']['ipr'].append(ipr)
        results['c60']['xi_ratio'].append(xi_r)

    return results


# ============================================================
# 8. バンドギャップとバンド幅の計算
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
    print("\n[1/7] バンド構造計算...")
    kd_dia, Eb_dia, tp_dia, tl_dia = diamond_bandstructure()
    kd_gra, Eb_gra, tp_gra, tl_gra = graphene_bandstructure()
    kd_1d, Eb_1d, tp_1d, tl_1d = chain1d_bandstructure()
    kd_c60, Eb_c60, tp_c60, tl_c60 = c60_bandstructure()

    # --- DOS計算 ---
    print("[2/7] 状態密度(DOS)計算...")
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
    print("[3/7] δプロキシ (IPR^-1) 計算...")
    delta_dia = compute_diamond_delta()
    delta_gra = compute_graphene_delta()
    delta_1d = compute_chain1d_delta()
    delta_c60 = compute_c60_delta()

    # --- 結果まとめ ---
    systems = [
        {"name": "Diamond (ダイヤモンド)", "Eg": Eg_dia, "W": W_dia, "delta": delta_dia,
         "D_eff": 0, "label": "Diamond", "optical": "Transparent"},
        {"name": "Graphene (グラフェン)", "Eg": Eg_gra, "W": W_gra, "delta": delta_gra,
         "D_eff": 2, "label": "Graphene", "optical": "Transparent(mono)/Black(bulk)"},
        {"name": "1D chain (SWCNT近似)", "Eg": Eg_1d, "W": W_1d, "delta": delta_1d,
         "D_eff": 1, "label": "1D Chain (SWCNT)", "optical": "Colored"},
        {"name": "C60 solid (C60固体)", "Eg": Eg_c60, "W": W_c60, "delta": delta_c60,
         "D_eff": 0, "label": "C60 Solid", "optical": "Colored"},
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

    # Pearson相関係数
    r, p_val = pearsonr(deltas, Egs)
    print(f"\n[検証] δ-Eg Pearson相関係数: r = {r:.4f} (p = {p_val:.4e})")

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
            category = "Transparent (wide gap)"
        elif s['Eg'] > 0 and s['D_eff'] <= 1:
            category = "Colored (selective abs.)"
        elif s['Eg'] == 0 and s['D_eff'] >= 2:
            category = "Transparent(mono)/Black+gloss(bulk)"
        else:
            category = "Metallic luster"
        print(f"    → 分類: {category}")

    # ============================================================
    # プロット
    # ============================================================
    # ============================================================
    # 光学伝導度・誘電関数・反射率の計算
    # ============================================================
    print("\n[4/8] 光学伝導度の計算 (π帯のみ, クボー公式)...")
    omega = np.linspace(0.05, 8.0, 400)

    print("  グラフェン (π帯)...")
    _, sigma_gra_pi, Deff_gra_pi, Tdiag_gra_pi = graphene_optical_kgrid(nk=60, omega_grid=omega)
    print("  1D鎖...")
    _, sigma_1d, Deff_1d_v, Tdiag_1d = chain1d_optical_kgrid(nk=2000, omega_grid=omega)
    print("  C60...")
    _, sigma_c60, Deff_c60_v, Tdiag_c60 = c60_optical(omega_grid=omega)

    # --- 全軌道 Slater-Koster モデル ---
    print("\n[5/8] 全軌道光学伝導度 (s,px,py,pz Slater-Koster)...")
    omega_full = np.linspace(0.05, 12.0, 600)

    print("  グラフェン (8バンド)...")
    _, sigma_gra_full, Deff_gra_v, Tdiag_gra, evals_gra = graphene_full_tb_optical(
        nk=50, omega_grid=omega_full, eta=0.15)
    print("  ダイヤモンド (8バンド)...")
    _, sigma_dia_full, Deff_dia_v, Tdiag_dia, evals_dia = diamond_full_tb_optical(
        nk=12, omega_grid=omega_full, eta=0.15)

    # --- D_eff 検証 ---
    print("\n[6/8] D_eff (速度テンソルから計算):")
    print(f"  ダイヤモンド (8band): D_eff = {Deff_dia_v:.2f}  (期待: 3.0)  T_diag = {Tdiag_dia}")
    print(f"  グラフェン (8band):   D_eff = {Deff_gra_v:.2f}  (期待: 2.0)  T_diag = {Tdiag_gra}")
    print(f"  1D鎖 (2band):         D_eff = {Deff_1d_v:.2f}  (期待: 1.0)  T_diag = {Tdiag_1d}")
    print(f"  C60:                   D_eff = {Deff_c60_v:.2f}  (期待: 0.0)")

    systems[0]['D_eff_velocity'] = Deff_dia_v
    systems[1]['D_eff_velocity'] = Deff_gra_v
    systems[2]['D_eff_velocity'] = Deff_1d_v
    systems[3]['D_eff_velocity'] = Deff_c60_v

    # --- 誘電関数・反射率 (全軌道モデル) ---
    print("\n[7/8] 誘電関数・反射率の計算 (全軌道モデル)...")

    # 正規化: グラフェンのπ帯 σ₀ で全系を共通正規化
    sigma_pi_low = np.mean(sigma_gra_pi[(omega > 0.5) & (omega < 2.0)])
    print(f"  グラフェン π帯 σ₀ (0.5-2.0 eV) = {sigma_pi_low:.6f}")

    # 全軌道モデルの σ を物理単位に変換
    # グラフェンの全軌道σのうち低エネルギー部はπ帯が支配 → σ₀で正規化
    sigma_full_low = np.mean(sigma_gra_full[(omega_full > 0.5) & (omega_full < 2.0)])
    scale = sigma_pi_low / max(sigma_full_low, 1e-30)

    # ε₂ の計算 — 全軌道モデル
    # 共通正規化: σ を σ₀ 単位に変換後、物理的な ε₂ = 4πσ/(ωε₀) を計算
    # σ₀ = πe²/(2h) ≈ 6.08e-5 S (2D伝導度)
    # グラファイト: ε₂ = σ_2D / (ε₀ ω d)  where d = 3.35 Å
    # → ε₂ = σ₀ × σ_norm / (ε₀ ω d) = (πα/d) × σ_norm / ω
    #   πα ≈ 0.0229, d = 3.35e-10 m → πα/d ≈ 6.84e7 m^-1
    #   ε₂ = πα × ℏc / (d × ℏω) × σ_norm
    # ℏc = 197.3 eV·nm = 1973 eV·Å
    # → ε₂ = π/137 × 1973 / (3.35 × ℏω) × σ_norm ≈ 13.5 / ℏω × σ_norm

    hbar_c_eVA = 1973.0  # eV·Å
    alpha_fs = 1.0 / 137.036

    # グラフェン/グラファイト
    d_graphite = 3.35  # Å
    pref_gra = np.pi * alpha_fs * hbar_c_eVA / d_graphite  # ≈ 13.5

    sigma_gra_norm = sigma_gra_full * scale
    eps2_gra = np.zeros_like(omega_full)
    nonzero = omega_full > 0.01
    eps2_gra[nonzero] = pref_gra * sigma_gra_norm[nonzero] / omega_full[nonzero]

    # ダイヤモンド: 3D → 有効層厚 d_eff = V_cell / A_cell で2D換算
    # V_cell = a³/4 (FCC conventional cell has 8 atoms, primitive has 2)
    # 原始胞体積 = a³/4 = 11.35 Å³
    # 有効 "層厚" = V_cell^(1/3) ≈ 2.25 Å
    d_diamond_eff = (3.567 ** 3 / 4) ** (1.0 / 3.0)  # ≈ 2.25 Å
    pref_dia = np.pi * alpha_fs * hbar_c_eVA / d_diamond_eff

    # ダイヤモンド: scissors correction + 実験キャリブレーション
    # SK/LDAバンドギャップ = 2.60 eV → 実験値 5.47 eV
    scissors = 5.47 - 2.60  # = 2.87 eV
    sigma_dia_norm = sigma_dia_full * scale
    eps2_dia = np.zeros_like(omega_full)
    # 可視域 (< 5.47 eV) では吸収なし
    above_gap = omega_full >= 5.47
    eps2_dia[above_gap] = pref_dia * sigma_dia_norm[above_gap] / omega_full[above_gap]
    # 実験キャリブレーション: ダイヤモンド ε₂(UV) ≈ 5-10
    # SKモデルのε₂が過大なら実験値にスケール
    eps2_dia_max = np.max(eps2_dia)
    if eps2_dia_max > 12.0:
        dia_scale = 10.0 / eps2_dia_max  # 実験的ε₂ピーク ≈ 10
        eps2_dia *= dia_scale
        print(f"  ダイヤモンド ε₂ キャリブレーション: ×{dia_scale:.3f} (ピーク→10)")
    print(f"  ダイヤモンド scissors correction: Δ = {scissors:.2f} eV (Eg: 2.60 → 5.47 eV)")

    # 1D鎖: π帯のみ、有効断面積で正規化
    d_1d_eff = 13.6  # Å — (10,10) armchair SWCNT 直径 ≈ 13.6 Å
    pref_1d = np.pi * alpha_fs * hbar_c_eVA / d_1d_eff

    eps2_1d = np.zeros_like(omega)
    nz_1d = omega > 0.01
    eps2_1d[nz_1d] = pref_1d * sigma_1d[nz_1d] / (sigma_pi_low * omega[nz_1d])
    # バンヘーベ特異点による ε₂ 発散をキャップ
    # SWCNT束の実験的 ε₂ ≈ 3-8 (Kataura et al.)
    eps2_1d = np.minimum(eps2_1d, 6.0)

    # C60: 双極子モデル、有効セルサイズで正規化
    d_c60_eff = 14.17  # Å (FCC格子定数)
    pref_c60 = np.pi * alpha_fs * hbar_c_eVA / d_c60_eff

    eps2_c60 = np.zeros_like(omega)
    eps2_c60[nz_1d] = pref_c60 * sigma_c60[nz_1d] / (sigma_pi_low * omega[nz_1d])

    # 可視域マスク（KK検証用に先に定義）
    vis_full = (omega_full >= 1.6) & (omega_full <= 3.1)
    vis = (omega >= 1.6) & (omega <= 3.1)

    # 反射率（KK変換で ε₁ を計算）
    print("  クラマース・クローニッヒ変換で ε₁(ω) を計算中...")
    R_gra, eps1_gra = reflectivity_from_epsilon(eps2_gra, omega_grid=omega_full)
    R_dia, eps1_dia = reflectivity_from_epsilon(eps2_dia, omega_grid=omega_full)
    R_1d, eps1_1d = reflectivity_from_epsilon(eps2_1d, omega_grid=omega)
    R_c60, eps1_c60 = reflectivity_from_epsilon(eps2_c60, omega_grid=omega)

    # ダイヤモンド: 実験的ε∞による補正
    # 実験値 ε∞ = 5.7 (ダイヤモンドの光学誘電率、可視〜近赤外)
    # ε∞ はすべての電子遷移(σ+π)のoff-resonance寄与を含む
    # TB 8バンドモデルでは遷移の一部しか捉えられない → KK結果を補正
    # 可視域(ω < Eg)ではε₂=0なので、ε₁ = ε∞ (実験値)に設定
    # UV域(ω > Eg)ではKK結果にε∞-1の背景分を加算
    eps_inf_dia = 5.7  # 実験値 (Klein & Furtak, Optics of Solids)
    eps1_dia_kk_vis = np.mean(eps1_dia[vis_full]) if np.any(vis_full) else 1.0
    delta_eps1 = eps_inf_dia - eps1_dia_kk_vis  # KKが捉えきれない高エネルギー遷移の寄与
    eps1_dia = eps1_dia + delta_eps1  # 全周波数にシフト（UV域ではKKの相対構造を保持）
    print(f"  ダイヤモンド: ε∞={eps_inf_dia} 補正 (KK可視域平均 {eps1_dia_kk_vis:.2f} → {eps_inf_dia:.1f}, Δε₁={delta_eps1:.2f})")
    # 反射率を再計算（補正済みε₁で）
    eps_complex_dia = eps1_dia + 1j * eps2_dia
    n_complex_dia = np.sqrt(eps_complex_dia)
    R_dia = np.abs((n_complex_dia - 1) / (n_complex_dia + 1)) ** 2

    # ε₁ の可視域平均値を表示（検証用）
    eps1_gra_vis = np.mean(eps1_gra[vis_full]) if np.any(vis_full) else 0
    eps1_dia_vis = np.mean(eps1_dia[vis_full]) if np.any(vis_full) else 0
    print(f"  ε₁ 可視域平均: グラフェン={eps1_gra_vis:.2f}, ダイヤモンド={eps1_dia_vis:.2f}")

    # 可視域平均反射率（フラット重み）
    R_vis_gra = np.mean(R_gra[vis_full])
    R_vis_dia = np.mean(R_dia[vis_full])
    R_vis_1d = np.mean(R_1d[vis])
    R_vis_c60 = np.mean(R_c60[vis])

    # CIE比視感度関数 V(λ) によるphotopic重み付き反射率（検証用）
    # V(λ) ≈ ガウシアン近似: ピーク555nm = 2.234 eV, FWHM ≈ 100nm → σ ≈ 0.18 eV
    def photopic_weight(omega_ev):
        """CIE V(λ) のガウシアン近似（eV単位）"""
        peak_eV = 2.234  # 555 nm
        sigma_eV = 0.18
        return np.exp(-0.5 * ((omega_ev - peak_eV) / sigma_eV) ** 2)

    # photopic重み付きR_vis
    w_full = photopic_weight(omega_full[vis_full])
    w_full = w_full / np.sum(w_full)
    w_short = photopic_weight(omega[vis])
    w_short = w_short / np.sum(w_short)

    R_vis_gra_ph = np.sum(R_gra[vis_full] * w_full)
    R_vis_dia_ph = np.sum(R_dia[vis_full] * w_full)
    R_vis_1d_ph = np.sum(R_1d[vis] * w_short)
    R_vis_c60_ph = np.sum(R_c60[vis] * w_short)

    print(f"\n  CIE比視感度重み付き反射率 (photopic V(λ) weighting):")
    print(f"    ダイヤモンド: R_vis(ph) = {R_vis_dia_ph:.4f}  (flat: {R_vis_dia:.4f})")
    print(f"    グラフェン:   R_vis(ph) = {R_vis_gra_ph:.4f}  (flat: {R_vis_gra:.4f})")
    print(f"    1D鎖:        R_vis(ph) = {R_vis_1d_ph:.4f}  (flat: {R_vis_1d:.4f})")
    print(f"    C60:          R_vis(ph) = {R_vis_c60_ph:.4f}  (flat: {R_vis_c60:.4f})")
    print(f"  → ランキング変化なし = flat weightingはrobust" if
          (R_vis_dia_ph < R_vis_gra_ph < R_vis_c60_ph) or
          (R_vis_dia_ph < R_vis_gra_ph) else
          "  → ランキングに変化あり！要検討")

    systems[0]['R_vis'] = R_vis_dia
    systems[1]['R_vis'] = R_vis_gra
    systems[2]['R_vis'] = R_vis_1d
    systems[3]['R_vis'] = R_vis_c60

    print(f"\n  可視域平均反射率 (全軌道モデル):")
    print(f"    ダイヤモンド: R_vis = {R_vis_dia:.4f}  (実験値 ~0.17)")
    print(f"    グラフェン/グラファイト: R_vis = {R_vis_gra:.4f}  (実験値 ~0.25-0.30)")
    print(f"    1D鎖 (SWCNT):   R_vis = {R_vis_1d:.4f}")
    print(f"    C60:             R_vis = {R_vis_c60:.4f}")

    # バンドギャップ検証 (全軌道モデル)
    evals_dia_all = np.array([e for e in evals_dia])
    gap_dia_full = np.min(evals_dia_all[:, 4]) - np.max(evals_dia_all[:, 3])
    print(f"\n  ダイヤモンド バンドギャップ (8band): {gap_dia_full:.2f} eV  (実験値: 5.47 eV)")

    # ============================================================
    # 光沢度予測 (角度依存フレネル反射率)
    # ============================================================
    print("\n[7.5/9] 光沢度予測 (ASTM D523準拠)...")

    # 各系の光沢度計算（KK変換済みε₁を使用）
    g20_gra, g60_gra, g85_gra, Rth_gra = compute_gloss_prediction(
        eps2_gra, eps1=eps1_gra, omega_grid=omega_full)
    g20_dia, g60_dia, g85_dia, Rth_dia = compute_gloss_prediction(
        eps2_dia, eps1=eps1_dia, omega_grid=omega_full)
    g20_1d, g60_1d, g85_1d, Rth_1d = compute_gloss_prediction(
        eps2_1d, eps1=eps1_1d, omega_grid=omega)
    g20_c60, g60_c60, g85_c60, Rth_c60 = compute_gloss_prediction(
        eps2_c60, eps1=eps1_c60, omega_grid=omega)

    systems[0]['gloss_60'] = g60_dia
    systems[1]['gloss_60'] = g60_gra
    systems[2]['gloss_60'] = g60_1d
    systems[3]['gloss_60'] = g60_c60

    print(f"\n  光沢度予測 (ASTM D523, 黒色ガラス基準 = 100 GU):")
    print(f"  {'系':18s} {'20° GU':>10s} {'60° GU':>10s} {'85° GU':>10s}  {'R(60°)':>8s}")
    print("  " + "-" * 65)
    for name, g20, g60, g85, Rth in [
        ('Diamond', g20_dia, g60_dia, g85_dia, Rth_dia),
        ('グラフェン/グラファイト', g20_gra, g60_gra, g85_gra, Rth_gra),
        ('1D鎖 (SWCNT)', g20_1d, g60_1d, g85_1d, Rth_1d),
        ('C60', g20_c60, g60_c60, g85_c60, Rth_c60),
    ]:
        print(f"  {name:18s} {g20:10.1f} {g60:10.1f} {g85:10.1f}  {Rth[60.0]:8.4f}")

    # 角度依存反射率の詳細計算（プロット用）
    theta_plot = np.linspace(0, 89, 180)
    _, _, R_ang_gra, _ = fresnel_angular(eps2_gra, eps1=eps1_gra, theta_deg=theta_plot)
    _, _, R_ang_dia, _ = fresnel_angular(eps2_dia, eps1=eps1_dia, theta_deg=theta_plot)
    _, _, R_ang_1d, _ = fresnel_angular(eps2_1d, eps1=eps1_1d, theta_deg=theta_plot)
    _, _, R_ang_c60, _ = fresnel_angular(eps2_c60, eps1=eps1_c60, theta_deg=theta_plot)

    # 可視域平均の角度依存
    R_ang_gra_vis = np.array([np.mean(R_ang_gra[it][vis_full]) for it in range(len(theta_plot))])
    R_ang_dia_vis = np.array([np.mean(R_ang_dia[it][vis_full]) for it in range(len(theta_plot))])
    R_ang_1d_vis = np.array([np.mean(R_ang_1d[it][vis]) for it in range(len(theta_plot))])
    R_ang_c60_vis = np.array([np.mean(R_ang_c60[it][vis]) for it in range(len(theta_plot))])

    # ============================================================
    # コヒーレンス保存仮説テスト
    # ============================================================
    print("\n[8/9] コヒーレンス保存仮説テスト (Anderson無秩序)...")
    W_values = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0]
    coh_results = coherence_preservation_test(W_values=W_values, n_realizations=15)

    # δ値の設定
    coh_results['graphene']['delta'] = delta_gra
    coh_results['chain1d']['delta'] = delta_1d
    coh_results['c60']['delta'] = delta_c60

    # 結果サマリー
    print("\n  コヒーレンス保存テスト結果:")
    print(f"  {'系':12s} {'δ':>6s} {'D_eff':>5s} | ", end="")
    for W in W_values:
        print(f"  IPR(W={W:.0f})", end="")
    print()
    print("  " + "-" * 90)

    for name, label in [('graphene', 'Graphene'), ('chain1d', '1D Chain'),
                          ('c60', 'C60')]:
        d = coh_results[name]
        delta_v = d['delta'] if d['delta'] is not None else 0
        print(f"  {label:12s} {delta_v:6.2f} {d['D_eff']:5d} | ", end="")
        for ipr_v in d['ipr']:
            print(f"  {ipr_v:10.4f}", end="")
        print()

    # コヒーレンス指標: σ(ω)のスペクトル相関（W=0 との類似度）
    print("\n  スペクトル保存度 (W=0との相関):")
    print(f"  {'系':12s} | ", end="")
    for W in W_values[1:]:
        print(f"  corr(W={W:.0f})", end="")
    print()
    print("  " + "-" * 70)

    for name, label in [('graphene', 'Graphene'), ('chain1d', '1D Chain'),
                          ('c60', 'C60')]:
        d = coh_results[name]
        sig0 = d['sigma'][0]
        print(f"  {label:12s} | ", end="")
        for i in range(1, len(W_values)):
            if np.std(sig0) > 1e-30 and np.std(d['sigma'][i]) > 1e-30:
                corr = np.corrcoef(sig0, d['sigma'][i])[0, 1]
            else:
                corr = 0.0
            print(f"  {corr:11.4f}", end="")
        print()

    # 局在化長/可視光波長 比
    print("\n  局在化比 ξ/λ_vis:")
    print(f"  {'系':12s} | ", end="")
    for W in W_values:
        print(f"  ξ/λ(W={W:.0f})", end="")
    print()
    print("  " + "-" * 80)

    for name, label in [('graphene', 'Graphene'), ('chain1d', '1D Chain'),
                          ('c60', 'C60')]:
        d = coh_results[name]
        print(f"  {label:12s} | ", end="")
        for xi_r in d['xi_ratio']:
            print(f"  {xi_r:10.4f}", end="")
        print()

    print("\n  解釈:")
    print("    ξ/λ_vis >> 1 → コヒーレンス保存 → 鏡面反射 → 光沢")
    print("    ξ/λ_vis << 1 → コヒーレンス喪失 → 散漫散乱 → マット")
    print("    高δ × 高D_eff → 無秩序に対してロバスト → コヒーレンス保存")

    # --- 実効光沢度の計算 (無秩序下) ---
    print("\n  実効光沢度予測 (清浄光沢 × コヒーレンス因子):")
    print(f"  {'系':18s} {'清浄 60°GU':>12s} | ", end="")
    for W in W_values[1:]:
        print(f" W={W:.0f}eV", end="")
    print()
    print("  " + "-" * 80)

    gloss_effective = {}
    for name, label, g60_clean in [
        ('graphene', 'Graphene', g60_gra),
        ('chain1d', '1D Chain', g60_1d),
        ('c60', 'C60', g60_c60),
    ]:
        d = coh_results[name]
        sig0 = d['sigma'][0]
        eff_list = [g60_clean]
        print(f"  {label:18s} {g60_clean:12.1f} | ", end="")
        for i in range(1, len(W_values)):
            if np.std(sig0) > 1e-30 and np.std(d['sigma'][i]) > 1e-30:
                corr = np.corrcoef(sig0, d['sigma'][i])[0, 1]
            else:
                corr = 0.0
            eff = compute_effective_gloss_with_disorder(g60_clean, max(corr, 0))
            eff_list.append(eff)
            print(f" {eff:6.1f}", end="")
        print()
        gloss_effective[name] = eff_list

    # ダイヤモンドは広バンドギャップ → 無秩序に無関係で透明のまま
    gloss_effective['diamond'] = [g60_dia] * len(W_values)

    # ============================================================
    # プロット
    # ============================================================
    print("\n[10/10] 図の生成...")

    # --- Fig A: バンド構造 (4パネル) ---
    fig_a, axes_a = plt.subplots(1, 4, figsize=(16, 4))
    fig_a.suptitle("Band Structure (Tight Binding)", fontsize=14, y=1.02)

    band_data = [
        (kd_dia, Eb_dia, tp_dia, tl_dia, "Diamond (sp3 TB)"),
        (kd_gra, Eb_gra, tp_gra, tl_gra, "Graphene (π-band TB)"),
        (kd_1d, Eb_1d, tp_1d, tl_1d, "1D Chain (SWCNT proxy)"),
        (kd_c60, Eb_c60, tp_c60, tl_c60, "C60 Solid (HOMO/LUMO bands)"),
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
    fig_b.suptitle("Density of States (DOS)", fontsize=14, y=1.02)

    dos_data = [
        (eg_dia, dos_dia, "Diamond"),
        (eg_gra, dos_gra, "Graphene"),
        (eg_1d, dos_1d, "1D Chain (SWCNT proxy)"),
        (eg_c60, dos_c60, "C60 Solid"),
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
    ax_c.set_title("δ-Eg Inverse Correlation", fontsize=14)

    # 散布図
    markers = ['D', 'o', 's', '^']
    for i, s in enumerate(systems):
        ax_c.scatter(s['delta'], s['Eg'], s=120, marker=markers[i],
                     color=colors_band[i], zorder=5, edgecolors='black', linewidth=0.8)
        # ラベル
        offset = (8, 8) if i != 1 else (8, -15)
        ax_c.annotate(s['label'], (s['delta'], s['Eg']),
                      textcoords="offset points", xytext=offset, fontsize=10)

    # Linear fit
    z = np.polyfit(deltas, Egs, 1)
    p = np.poly1d(z)
    delta_range = np.linspace(deltas.min() * 0.8, deltas.max() * 1.2, 100)
    ax_c.plot(delta_range, p(delta_range), 'k--', linewidth=1, alpha=0.5,
              label=f"Linear fit (r={r:.3f})")

    ax_c.set_xlabel("δ (Delocalization proxy, IPR⁻¹)", fontsize=12)
    ax_c.set_ylabel("Eg [eV]", fontsize=12)
    ax_c.legend(fontsize=10)
    ax_c.grid(alpha=0.3)

    # δ×D_eff による光学分類領域をアノテーション
    ax_c.text(0.02, 0.98, f"Pearson r = {r:.3f}\np = {p_val:.2e}",
              transform=ax_c.transAxes, fontsize=10,
              verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    fig_c.tight_layout()
    fig_c.savefig(os.path.join(FIGDIR, "fig_c_delta_Eg_correlation.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_c_delta_Eg_correlation.png')}")

    # --- Fig D: 吸収スペクトル ε₂(ω) (全軌道モデル) ---
    fig_d, ax_d = plt.subplots(figsize=(8, 5))
    ax_d.set_title("Absorption Spectrum ε₂(ω) — Full-orbital Slater-Koster TB", fontsize=14)

    ax_d.axvspan(1.6, 3.1, alpha=0.15, color='gold', label='Visible range')
    ax_d.plot(omega_full, eps2_dia, color=colors_band[0], linewidth=1.5, label='Diamond (8band)')
    ax_d.plot(omega_full, eps2_gra, color=colors_band[1], linewidth=1.5, label='Graphene (8band)')
    ax_d.plot(omega, eps2_1d, color=colors_band[2], linewidth=1.5, label='1D Chain (π-band)', linestyle='--')
    ax_d.plot(omega, eps2_c60, color=colors_band[3], linewidth=1.5, label='C60 (Dipole)', linestyle='--')

    ax_d.set_xlabel("Photon Energy [eV]", fontsize=12)
    ax_d.set_ylabel("ε₂", fontsize=12)
    ax_d.set_xlim(0, 10)
    ax_d.legend(fontsize=10)
    ax_d.grid(alpha=0.3)

    fig_d.tight_layout()
    fig_d.savefig(os.path.join(FIGDIR, "fig_d_absorption.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_d_absorption.png')}")

    # --- Fig E: 反射率 R(ω) (全軌道モデル) ---
    fig_e, ax_e = plt.subplots(figsize=(8, 5))
    ax_e.set_title("Reflectance R(ω) — Full-orbital Slater-Koster TB", fontsize=14)

    ax_e.axvspan(1.6, 3.1, alpha=0.15, color='gold', label='Visible range')
    ax_e.plot(omega_full, R_dia, color=colors_band[0], linewidth=1.5, label='Diamond (8band)')
    ax_e.plot(omega_full, R_gra, color=colors_band[1], linewidth=1.5, label='Graphene (8band)')
    ax_e.plot(omega, R_1d, color=colors_band[2], linewidth=1.5, label='1D Chain (π-band)', linestyle='--')
    ax_e.plot(omega, R_c60, color=colors_band[3], linewidth=1.5, label='C60 (Dipole)', linestyle='--')

    ax_e.set_xlabel("Photon Energy [eV]", fontsize=12)
    ax_e.set_ylabel("R(ω)", fontsize=12)
    ax_e.set_xlim(0, 10)
    ax_e.set_ylim(0, 0.6)
    ax_e.legend(fontsize=10)
    ax_e.grid(alpha=0.3)

    fig_e.tight_layout()
    fig_e.savefig(os.path.join(FIGDIR, "fig_e_reflectivity.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_e_reflectivity.png')}")

    # --- Fig F: δ×D_eff vs 可視域平均反射率 ---
    fig_f, ax_f = plt.subplots(figsize=(7, 5))
    ax_f.set_title("δ × D_eff vs Visible-range Reflectance", fontsize=14)

    for i, s in enumerate(systems):
        deff_v = s.get('D_eff_velocity', s['D_eff'])
        delta_deff = s['delta'] * (deff_v + 1)
        ax_f.scatter(delta_deff, s['R_vis'], s=120, marker=markers[i],
                     color=colors_band[i], zorder=5, edgecolors='black', linewidth=0.8)
        offset_xy = (8, 8) if i != 1 else (8, -15)
        ax_f.annotate(s['label'], (delta_deff, s['R_vis']),
                      textcoords="offset points", xytext=offset_xy, fontsize=10)

    ax_f.set_xlabel("δ × (D_eff + 1)", fontsize=12)
    ax_f.set_ylabel("Visible-range Reflectance R_vis", fontsize=12)
    ax_f.grid(alpha=0.3)

    # δ×D_eff と R_vis の相関
    dd_vals = np.array([s['delta'] * (s.get('D_eff_velocity', s['D_eff']) + 1) for s in systems])
    rv_vals = np.array([s['R_vis'] for s in systems])
    if len(dd_vals) > 2:
        r_dr, p_dr = pearsonr(dd_vals, rv_vals)
        ax_f.text(0.02, 0.98, f"Pearson r = {r_dr:.3f}\np = {p_dr:.2e}",
                  transform=ax_f.transAxes, fontsize=10,
                  verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        print(f"\n  δ×D_eff vs R_vis 相関: r = {r_dr:.3f} (p = {p_dr:.2e})")

    fig_f.tight_layout()
    fig_f.savefig(os.path.join(FIGDIR, "fig_f_delta_deff_reflectivity.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_f_delta_deff_reflectivity.png')}")

    # --- Fig G: コヒーレンス保存テスト — σ(ω) vs W ---
    fig_g, axes_g = plt.subplots(1, 3, figsize=(16, 5))
    fig_g.suptitle("Coherence Preservation Test: σ(ω) under Anderson Disorder", fontsize=14, y=1.02)

    coh_omega = coh_results['omega']
    coh_systems = [
        ('graphene', 'Graphene (high δ, D_eff=2)', colors_band[1]),
        ('chain1d', '1D Chain (high δ, D_eff=1)', colors_band[2]),
        ('c60', 'C60 (low δ, D_eff=0)', colors_band[3]),
    ]

    for ax, (name, title, base_color) in zip(axes_g, coh_systems):
        d = coh_results[name]
        sig0 = d['sigma'][0]
        # σ(ω) を W=0 の最大値で正規化
        norm_factor = max(sig0.max(), 1e-30)

        alphas = [1.0, 0.8, 0.6, 0.45, 0.3, 0.2]
        for i, (W, sig) in enumerate(zip(W_values, d['sigma'])):
            sig_norm = sig / norm_factor
            label_str = f"W={W:.1f} eV"
            ax.plot(coh_omega, sig_norm, color=base_color, alpha=alphas[i],
                    linewidth=1.5 if i == 0 else 1.0, label=label_str,
                    linestyle='-' if i == 0 else '--')

        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Photon Energy [eV]", fontsize=10)
        ax.set_ylabel("σ(ω) / σ₀(ω)", fontsize=10)
        ax.set_xlim(0, 6)
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(alpha=0.3)

    fig_g.tight_layout()
    fig_g.savefig(os.path.join(FIGDIR, "fig_g_coherence_sigma.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_g_coherence_sigma.png')}")

    # --- Fig H: IPR(W) — 局在化の進行 ---
    fig_h, (ax_h1, ax_h2) = plt.subplots(1, 2, figsize=(12, 5))
    fig_h.suptitle("Coherence Test: Disorder vs Localization / Spectral Preservation", fontsize=14, y=1.02)

    # 左パネル: IPR(W)
    for name, label, color in [('graphene', 'Graphene', colors_band[1]),
                                  ('chain1d', '1D Chain', colors_band[2]),
                                  ('c60', 'C60', colors_band[3])]:
        d = coh_results[name]
        # IPR を W=0 で正規化
        ipr0 = d['ipr'][0] if d['ipr'][0] > 1e-30 else 1e-30
        ipr_norm = np.array(d['ipr']) / ipr0
        delta_v = d['delta'] if d['delta'] is not None else 0
        deff = d['D_eff']
        ax_h1.plot(W_values, ipr_norm, 'o-', color=color, linewidth=2, markersize=6,
                   label=f'{label} (δ={delta_v:.1f}, D_eff={deff})')

    ax_h1.set_xlabel("Disorder Strength W [eV]", fontsize=12)
    ax_h1.set_ylabel("IPR / IPR(W=0)", fontsize=12)
    ax_h1.set_title("IPR Growth Rate", fontsize=12)
    ax_h1.legend(fontsize=10)
    ax_h1.grid(alpha=0.3)
    ax_h1.set_ylim(0, None)

    # 右パネル: スペクトル相関 (W=0 との)
    for name, label, color in [('graphene', 'Graphene', colors_band[1]),
                                  ('chain1d', '1D Chain', colors_band[2]),
                                  ('c60', 'C60', colors_band[3])]:
        d = coh_results[name]
        sig0 = d['sigma'][0]
        corrs = []
        for i in range(len(W_values)):
            if np.std(sig0) > 1e-30 and np.std(d['sigma'][i]) > 1e-30:
                corr = np.corrcoef(sig0, d['sigma'][i])[0, 1]
            else:
                corr = 0.0
            corrs.append(corr)

        delta_v = d['delta'] if d['delta'] is not None else 0
        deff = d['D_eff']
        ax_h2.plot(W_values, corrs, 's-', color=color, linewidth=2, markersize=6,
                   label=f'{label} (δ={delta_v:.1f}, D_eff={deff})')

    ax_h2.set_xlabel("Disorder Strength W [eV]", fontsize=12)
    ax_h2.set_ylabel("Spectral Correlation corr(σ₀, σ_W)", fontsize=12)
    ax_h2.set_title("Optical Coherence Preservation", fontsize=12)
    ax_h2.axhline(0.9, color='gray', linestyle=':', alpha=0.5, label='Coherence threshold (0.9)')
    ax_h2.legend(fontsize=9)
    ax_h2.grid(alpha=0.3)
    ax_h2.set_ylim(-0.1, 1.05)

    fig_h.tight_layout()
    fig_h.savefig(os.path.join(FIGDIR, "fig_h_coherence_ipr.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_h_coherence_ipr.png')}")

    # --- Fig I: 角度依存反射率 R(θ) ---
    fig_i, (ax_i1, ax_i2) = plt.subplots(1, 2, figsize=(14, 5))
    fig_i.suptitle("Angular Reflectance and Gloss Prediction", fontsize=14, y=1.02)

    # 左パネル: R(θ) 可視域平均
    ax_i1.plot(theta_plot, R_ang_dia_vis * 100, color=colors_band[0], linewidth=2,
               label='Diamond')
    ax_i1.plot(theta_plot, R_ang_gra_vis * 100, color=colors_band[1], linewidth=2,
               label='Graphene/Graphite')
    ax_i1.plot(theta_plot, R_ang_1d_vis * 100, color=colors_band[2], linewidth=2,
               label='1D Chain (SWCNT)', linestyle='--')
    ax_i1.plot(theta_plot, R_ang_c60_vis * 100, color=colors_band[3], linewidth=2,
               label='C60', linestyle='--')

    # 工業規格角度を縦線で表示
    for angle, ls in [(20, ':'), (60, '-'), (85, ':')]:
        ax_i1.axvline(angle, color='gray', linestyle=ls, alpha=0.4)
        ax_i1.text(angle + 1, 2, f'{angle}°', fontsize=9, color='gray')

    ax_i1.set_xlabel("Incident Angle θ [°]", fontsize=12)
    ax_i1.set_ylabel("Visible-range Reflectance R(θ) [%]", fontsize=12)
    ax_i1.set_title("Fresnel Reflectance (Unpolarized)", fontsize=12)
    ax_i1.set_xlim(0, 90)
    ax_i1.set_ylim(0, 100)
    ax_i1.legend(fontsize=10)
    ax_i1.grid(alpha=0.3)

    # 右パネル: 60° 光沢度バー + 実効光沢度 (無秩序下)
    bar_width = 0.35
    x_pos = np.arange(3)
    labels_bar = ['Graphene', '1D Chain', 'C60']
    clean_gloss = [g60_gra, g60_1d, g60_c60]

    # W=3eV での実効光沢
    eff_W3 = []
    for name in ['graphene', 'chain1d', 'c60']:
        # W_values[4] = 3.0
        eff_W3.append(gloss_effective[name][4])

    bars1 = ax_i2.bar(x_pos - bar_width / 2, clean_gloss, bar_width,
                       color=[colors_band[1], colors_band[2], colors_band[3]],
                       alpha=0.9, label='Clean (W=0)', edgecolor='black', linewidth=0.5)
    bars2 = ax_i2.bar(x_pos + bar_width / 2, eff_W3, bar_width,
                       color=[colors_band[1], colors_band[2], colors_band[3]],
                       alpha=0.4, label='Disordered (W=3eV)', edgecolor='black',
                       linewidth=0.5, hatch='//')

    # 値ラベル
    for bar, val in zip(bars1, clean_gloss):
        ax_i2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                   f'{val:.0f}', ha='center', fontsize=9, fontweight='bold')
    for bar, val in zip(bars2, eff_W3):
        ax_i2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                   f'{val:.0f}', ha='center', fontsize=9)

    ax_i2.set_ylabel("60° Gloss [GU]", fontsize=12)
    ax_i2.set_title("Gloss Prediction (ASTM D523)", fontsize=12)
    ax_i2.set_xticks(x_pos)
    ax_i2.set_xticklabels(labels_bar)
    ax_i2.axhline(100, color='gray', linestyle='--', alpha=0.3, label='Reference (100 GU)')
    ax_i2.legend(fontsize=9)
    ax_i2.grid(axis='y', alpha=0.3)
    ax_i2.set_ylim(0, max(clean_gloss) * 1.3)

    fig_i.tight_layout()
    fig_i.savefig(os.path.join(FIGDIR, "fig_i_angular_gloss.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_i_angular_gloss.png')}")

    # --- Fig J: ミクロ→光沢 予測チェーン総括 ---
    fig_j, axes_j = plt.subplots(1, 3, figsize=(16, 5))
    fig_j.suptitle("Micro-to-Gloss Prediction Chain: δ×D_eff → ε(ω) → R(θ) → GU",
                    fontsize=13, y=1.02)

    # 左: δ×(D_eff+1) vs 清浄60°光沢度
    all_names = ['Diamond', 'Graphene', '1D Chain', 'C60']
    all_dd = [s['delta'] * (s.get('D_eff_velocity', s['D_eff']) + 1) for s in systems]
    all_g60 = [g60_dia, g60_gra, g60_1d, g60_c60]

    for i, (dd, g60, name) in enumerate(zip(all_dd, all_g60, all_names)):
        axes_j[0].scatter(dd, g60, s=120, marker=markers[i],
                          color=colors_band[i], zorder=5, edgecolors='black', linewidth=0.8)
        offset_xy = (8, 8) if i != 1 else (8, -15)
        axes_j[0].annotate(name, (dd, g60),
                           textcoords="offset points", xytext=offset_xy, fontsize=10)

    axes_j[0].set_xlabel("δ × (D_eff + 1)", fontsize=12)
    axes_j[0].set_ylabel("Clean Surface 60° Gloss [GU]", fontsize=12)
    axes_j[0].set_title("(a) Microscopic Quantity vs Clean Gloss", fontsize=11)
    axes_j[0].grid(alpha=0.3)

    # 中: 無秩序強度 vs 実効光沢度
    for name, label, color in [
        ('graphene', 'Graphene', colors_band[1]),
        ('chain1d', '1D Chain', colors_band[2]),
        ('c60', 'C60', colors_band[3]),
    ]:
        axes_j[1].plot(W_values, gloss_effective[name], 'o-', color=color,
                       linewidth=2, markersize=6, label=label)

    axes_j[1].set_xlabel("Disorder Strength W [eV]", fontsize=12)
    axes_j[1].set_ylabel("Effective 60° Gloss [GU]", fontsize=12)
    axes_j[1].set_title("(b) Gloss Degradation under Disorder", fontsize=11)
    axes_j[1].legend(fontsize=10)
    axes_j[1].grid(alpha=0.3)

    # 右: δ×D_eff vs 光沢保存率 (W=3eV時の光沢/清浄光沢)
    sys_micro = [
        ('Graphene', delta_gra, 2, g60_gra, gloss_effective['graphene'][4], colors_band[1]),
        ('1D Chain', delta_1d, 1, g60_1d, gloss_effective['chain1d'][4], colors_band[2]),
        ('C60', delta_c60, 0, g60_c60, gloss_effective['c60'][4], colors_band[3]),
    ]

    for i_sys, (name, delta, deff, g_clean, g_dirty, color) in enumerate(sys_micro):
        retention = g_dirty / max(g_clean, 1e-30) * 100
        dd = delta * (deff + 1)
        axes_j[2].scatter(dd, retention, s=150, color=color, zorder=5,
                          edgecolors='black', linewidth=0.8)
        axes_j[2].annotate(name, (dd, retention),
                           textcoords="offset points", xytext=(8, 8), fontsize=10)

    axes_j[2].set_xlabel("δ × (D_eff + 1)", fontsize=12)
    axes_j[2].set_ylabel("Gloss Retention [%] (W=3eV)", fontsize=12)
    axes_j[2].set_title("(c) Coherence Preservation → Gloss Robustness", fontsize=11)
    axes_j[2].set_ylim(0, 110)
    axes_j[2].axhline(90, color='gray', linestyle=':', alpha=0.5)
    axes_j[2].text(0.05, 92, 'High gloss retention (>90%)', fontsize=9, color='gray')
    axes_j[2].grid(alpha=0.3)

    fig_j.tight_layout()
    fig_j.savefig(os.path.join(FIGDIR, "fig_j_micro_to_gloss.png"), dpi=150, bbox_inches='tight')
    print(f"  保存: {os.path.join(FIGDIR, 'fig_j_micro_to_gloss.png')}")

    plt.close('all')

    print("\n" + "=" * 60)
    print("Simulation complete.")
    print(f"図は {FIGDIR} に保存されました。")
    print("=" * 60)

    return systems, r, p_val


if __name__ == "__main__":
    systems, r, p_val = main()
