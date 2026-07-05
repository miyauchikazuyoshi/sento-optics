#!/bin/bash
# F-1 自走スクリプト（PLAN: simulation/resta_electronic/PLAN.md）
# 平衡化の残り127ステップ + 本計測200ステップを「区切り restart」で実行。
# 各区切り末に wfc を退避（z_elec の時間平均用、計6スナップ）。
# Claude のセッションが切れても走り続ける。進捗は F1_status.txt。
set -u
cd "$(dirname "$0")"
PW="$HOME/miniforge3/bin/pw.x"
SNAP=snapshots_F1
STATUS=F1_status.txt
mkdir -p "$SNAP" logs

# 区切り表（this-run ステップ数）: 64+63=127 平衡化 / 50x4=200 本計測
CHUNKS=(64 63 50 50 50 50)
echo "$(date '+%F %T') F1 START chunks=${CHUNKS[*]}" >> "$STATUS"

for i in "${!CHUNKS[@]}"; do
  n=${CHUNKS[$i]}
  tag=$(printf "chunk%02d" $((i + 1)))
  # 入力生成: nstep 差し替え + メモリ節約設定の挿入
  awk -v N="$n" '
    /nstep/ {print "    nstep         = " N; next}
    {print}
    /diagonalization/ {
      print "    mixing_ndim      = 4"
      print "    diago_david_ndim = 2"
    }
  ' Na_equil_md_cont.in > "F1_${tag}.in"

  echo "$(date '+%F %T') ${tag} start (nstep=${n})" >> "$STATUS"
  "$PW" -input "F1_${tag}.in" > "logs/F1_${tag}.out" 2>&1
  rc=$?
  steps=$(grep -c "Entering Dynamics" "logs/F1_${tag}.out" 2>/dev/null || echo 0)
  echo "$(date '+%F %T') ${tag} end rc=${rc} steps=${steps}" >> "$STATUS"
  if [ "$rc" -ne 0 ] || [ "$steps" -lt 1 ]; then
    echo "$(date '+%F %T') ABORT at ${tag}" >> "$STATUS"
    exit 1
  fi
  cp tmp/Na_liquid.save/wfc1.hdf5 "$SNAP/wfc_${tag}.hdf5"
  cp tmp/Na_liquid.save/data-file-schema.xml "$SNAP/xml_${tag}.xml"
  cp tmp/Na_liquid.mdtrj "$SNAP/mdtrj_after_${tag}.dat"
  echo "$(date '+%F %T') ${tag} snapshot saved" >> "$STATUS"
done
echo "$(date '+%F %T') F1 ALL DONE" >> "$STATUS"
