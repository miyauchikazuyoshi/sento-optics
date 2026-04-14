# AIMD中断状態の記録（再開用）

**中断日時**: 2026-04-14 18:09

## 進捗

- 系: 64原子Na液体、471K、rescaling thermostat、dt=20 a.u.
- 完了ステップ: **173 / 300**（元run: 168 + 継続run: 5）
- 最終温度: 449.6 K
- 最終エネルギー: -6969.39759416 Ry

## 中断理由

システムメモリ圧迫（swap 56GB/57GB）でAIMDが大幅に減速（8分/step → 52分/step）。他プロジェクト優先のため一旦停止。

## 保存されているデータ

`tmp/Na_liquid.save/`:
- `charge-density.hdf5` (15MB) — 最新のcharge density
- `wfc1.hdf5` (134MB) — 最新の波動関数
- `data-file-schema.xml` — run情報

`tmp/Na_liquid.*`:
- `Na_liquid.md` — MDメタデータ
- `Na_liquid.mdtrj` — トラジェクトリ（173ステップ分）
- `Na_liquid.msd.dat` — MSDデータ
- `Na_liquid.update` — restart用（削除してはいけない）

## ログファイル

- `logs/Na_equil_scf.out` — 初期SCF
- `logs/Na_equil_md.out` — 168ステップのMD
- `logs/Na_equil_md_cont.out` — 継続分5ステップ（途中）

## 再開手順

```bash
# 1. メモリに余裕があることを確認
sysctl vm.swapusage
vm_stat | head -5

# 2. 残り127ステップを指定した継続run入力を作成
cd simulation/surface_tension/aimd
cp Na_equil_md.in Na_equil_md_resume.in
sed -i '' 's/nstep         = 300/nstep         = 127/' Na_equil_md_resume.in

# 3. restart_modeが'restart'になっていることを確認
grep restart_mode Na_equil_md_resume.in
# → restart_mode  = 'restart'

# 4. 実行
export PATH=$HOME/miniforge3/bin:$PATH
nohup pw.x -input Na_equil_md_resume.in > logs/Na_equil_md_resume.out 2>&1 &
PID=$!
echo "Resumed PID: $PID"
nohup caffeinate -i -w $PID &>/dev/null &
```

## 次のフェーズ

平衡化300ステップ完了後:
1. 本番MD（Andersen thermostat、1200ステップ、dt=20）
2. MSD → δ_nuc 抽出
3. Wannier spread → δ_elec 抽出
4. Paper 2.1 Part II の実証

## 得られたもの（現段階で）

- 173ステップの平衡化データ（1-2ps相当）
- 液体構造の初期緩和（初期ランダム配置 → 液体的配置へ）
- 温度制御の確認（rescalingが機能）
- エネルギーの安定化を確認
- **計算パイプラインの動作確認完了**
