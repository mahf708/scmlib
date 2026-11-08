#!/bin/bash
#
# Keep the interactive (2 x 4 nodes, 4 h) and debug (8 nodes, 30 min) slots
# busy with the sub-km 12 h cases until all are done.  625 m first (any GPU
# node), then 312 m (16 ranks: needs 80 GB nodes).  Restartable: all state is
# in the case directories (.sedps_done, .sedps_lock).
#
#   setsid nohup ./sedps_daemon.sh > $ROOT/logs/daemon.out 2>&1 &
#   touch $ROOT/STOP_DAEMON      # to stop it (running jobs finish their segment)

S=$(cd "$(dirname "$0")" && pwd)
export SEDPS_ROOT=${SEDPS_ROOT:-$PSCRATCH/dp_screamxx_sedps_12h}
R=$SEDPS_ROOT
L=$R/logs/daemon.log
MAX_DEBUG=${MAX_DEBUG:-3}           # leave debug submit slots for other work
MAX_INT=${MAX_INT:-2}               # interactive allocations to hold (the QOS allows 2)
cat $R/lists/625m.txt $R/lists/625m_t3don.txt > $R/lists/sub_625m.txt
cat $R/lists/312m.txt $R/lists/312m_t3don.txt > $R/lists/sub_312m.txt
log() { echo "$(date '+%m-%d %T') $*" >> "$L"; }

remaining() {   # cases in a list not yet complete
    local n=0 c cs
    while read -r c; do
        cs=$R/$c/case_scripts
        [[ -f $cs/.sedps_done && -f $cs/.sedps_target ]] && (( $(cat $cs/.sedps_done) >= $(cat $cs/.sedps_target) )) && continue
        n=$((n + 1))
    done < "$1"
    echo $n
}

start_runner() {   # $1 jobid, $2 list, $3 seg, $4 seg_min
    ( export SLURM_JOB_ID=$1 SLURM_JOBID=$1 SLURM_JOB_NUM_NODES=4 SLURM_NNODES=4 \
             SEDPS_SEG=$3 SEDPS_SEG_MIN=$4
      exec "$S/run_segmented.sh" "$2" ) > "$R/logs/runner.$1.out" 2>&1 &
    echo $! > "$R/logs/runner.$1.pid"
    log "runner on interactive $1: $(basename "$2") seg $3 h"
}

log "daemon start"
while [[ ! -f $R/STOP_DAEMON ]]; do
    n625=$(remaining $R/lists/sub_625m.txt)
    n312=$(remaining $R/lists/sub_312m.txt)
    (( n625 + n312 == 0 )) && { log "all sub-km cases complete"; break; }

    # ---- interactive allocations ----
    for j in $(squeue -h -u "$USER" -q gpu_interactive -t R -o "%i %j" | awk '$2 ~ /^sedps_int/ {print $1}'); do
        pidf=$R/logs/runner.$j.pid
        if [[ -f $pidf ]] && kill -0 "$(cat $pidf)" 2>/dev/null; then continue; fi
        feat=$(squeue -h -j "$j" -o %f)
        if (( n625 > 0 )); then start_runner "$j" $R/lists/sub_625m.txt 12 40
        elif [[ $feat == *hbm80g* ]] && (( n312 > 0 )); then start_runner "$j" $R/lists/sub_312m.txt 3 60
        else scancel "$j"; log "released interactive $j (no work for it)"; fi
    done
    nint=$(squeue -h -u "$USER" -q gpu_interactive -o "%j" | grep -c '^sedps_int')
    if (( nint < MAX_INT )) && ! pgrep -f "salloc.*sedps_int" > /dev/null; then
        if (( n625 > 0 )); then c=gpu; else c='gpu&hbm80g'; fi
        ( timeout 900 salloc -N 4 -q interactive -t 04:00:00 -C "$c" -A e3sm_g --gpus-per-node=4 \
              --no-shell -J sedps_int_$(date +%H%M) >> "$R/logs/salloc.out" 2>&1 ) &
        log "requested interactive allocation ($c)"
    fi

    # ---- debug jobs ----
    ndbg=$(squeue -h -u "$USER" -q gpu_debug -o "%j" | grep -c '^sedps_dbg')
    if (( ndbg < MAX_DEBUG )); then
        if (( n625 > 0 )); then
            sbatch -A e3sm_g -C gpu -q debug -N 8 --gpus-per-node=4 -t 30 -J sedps_dbg625 \
                -o $R/logs/slurm-%j.out --export=ALL,SEDPS_SEG=6,SEDPS_SEG_MIN=17 \
                $S/run_segmented.sh $R/lists/sub_625m.txt >> "$L" 2>&1
        elif (( n312 > 0 )); then
            sbatch -A e3sm_g -C 'gpu&hbm80g' -q debug -N 8 --gpus-per-node=4 -t 30 -J sedps_dbg312 \
                -o $R/logs/slurm-%j.out --export=ALL,SEDPS_SEG=1,SEDPS_SEG_MIN=20 \
                $S/run_segmented.sh $R/lists/sub_312m.txt >> "$L" 2>&1
        fi
    fi
    log "remaining 625m=$n625 312m=$n312, interactive=$nint, debug=$ndbg"
    sleep 120
done
log "daemon exit"
