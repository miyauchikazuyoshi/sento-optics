# phase0_maps: (δ_nuc, δ_elec) マテリアルマップ — フェーズ0

**戦略**: [drafts/strategy_ml_descriptor_2026-07-05.md](../../drafts/strategy_ml_descriptor_2026-07-05.md) §4–5
**日付**: 2026-07-05 開始

## δ_nuc 側（新規DFT計算ゼロ）

**データ源**: [phonondb](https://github.com/atztogo/phonondb)（Togo, NIMS MDR ホスト、
**CC-BY 4.0**、VASP/PBEsol + phonopy）— **10,034 材料**、認証不要の直リンク zip。

- `phonondb_index.csv` — インデックス（mp_id / 組成 / 空間群 / zip URL）。
  atztogo/phonondb の README テーブルをパースしたもの。
- `compute_delta_nuc.py` — zip 取得 → phonopy_params.yaml.xz → 熱変位
  ⟨u²⟩(0K, 300K) → δ_nuc(300K) = ⟨u²⟩/d_min² と量子成分比 q300 = ⟨u²⟩(0)/⟨u²⟩(300)。
  追記式 CSV で再開可能、1件 0.7s のサーバー礼儀スリープ付き。

```bash
python compute_delta_nuc.py test   # Si + NaCl 検証（既知値と照合）
python compute_delta_nuc.py 100    # 先頭100件
python compute_delta_nuc.py all    # 全件（~一晩、マシンが空いている時に）
```

検証基準（test）: Si の ⟨u²⟩(300K) ≈ 0.006 Å²/方向
（実験 Debye-Waller B ≈ 0.46–0.53 Å² → B/8π² との整合）。

### 運用ノート（2026-07-06、500件掃引のデバッグ記録）

1. **適応メッシュ規則**: eigenvector 配列 ~ n_q·(3N)²·16B を ~500MB 以下に保つ
   `mesh = clip(int((5e8/((3N)²·16))^{1/3}), 8, 24)`。大結晶で mesh 24³ 固定だと
   数GBに達し jetsam（macOS OOM）に**無言で**殺される（exit 0 に見えるのは
   パイプ後段の exit code。教訓: パイプの終了コードは犯人を隠す）。
2. **一貫性**: natom ≤ 14 は従来通り mesh 24。初回 run の natom > 14 の141件は
   mesh 24 の値（当時はメモリに余裕があり完走）。⟨u²⟩ の BZ 積分は mesh に
   ロバスト（12³ vs 24³ で ~1–2%）なので統計用途には混在を許容。
   v1 で厳密統一の再計算候補。
3. **ダウンロードは curl 委譲**（`-f -m 30`）: MDR は一時的に個別 URL が
   応答しなくなることがあり（mp-3261 で HTTP 000 → 数時間後 200 を実測）、
   urllib はその状態でハングし得る。
4. 障害の実記録: 初回 run は 378 件目で OOM 死 →「dead URL 説」で誤診
   （MDR 一時不調と重なったため）→ `sample` によるスタック採取で
   phonors/rayon の大計算と特定 → 適応メッシュで解決。

## δ_elec 側（SCF 1発/材料 — マシンが空いたら）

1. 一般セル対応の z_elec コード（resta_electronic/exp_F0 の立方限定を
   逆格子基底のテンソル形式に一般化）— 開発中
2. 対象選定: 既知の半導体・絶縁体 ~50 件（キュレーション、実験 E_g つき）
   → 将来 MP API（要キー）で1万件級へ
3. 飽和度 s = 2m_eE_gξ²/ℏ² マップ v0

## 成果物（予定）

- `delta_nuc_results.csv` — 10k 材料の δ_nuc / q300 テーブル
- (δ_nuc, q300) 平面のマップ（量子固体・古典固体の分離、de Boer 系列の大規模版）
- 飽和度 s マップ v0（数十材料）→ 光学材料設計チャートの雛形
