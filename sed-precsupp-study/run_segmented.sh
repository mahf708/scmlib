#!/bin/bash
#
# Like run_packed.sh, but each case runs as a chain of restart segments, so
# runs longer than a debug (30 min) or interactive (4 h) job can be spread
# over several jobs.  Re-run the same list in a new allocation to continue.
#
#   SEDPS_ROOT=... SEDPS_SEG=<model hours per segment> run_packed... :
#   sbatch [...] run_segmented.sh <caselist>       (or inside salloc, see README)
#
# Per case (in case_scripts/):  .sedps_target  total model hours (from STOP_N at
# first use);  .sedps_done  model hours completed;  segments.log  timings.
# A segment starts only if the allocation has time left for it (estimated from
# the case's previous segment, or SEDPS_SEG_MIN minutes, times 1.2 plus 3 min).

ROOT=${SEDPS_ROOT:-$PSCRATCH/dp_screamxx_sedps}
SEG=${SEDPS_SEG:?set SEDPS_SEG (model hours per segment)}
list=$1
total=${SLURM_JOB_NUM_NODES:?run inside an allocation}
log=$ROOT/logs/segmented.${SLURM_JOB_ID}.log
mkdir -p "$ROOT/logs"
end=$(date -d "$(squeue -h -j "$SLURM_JOB_ID" -o %e)" +%s)
free=$total
declare -A used

echo "$(date +%T) start: $total nodes, seg ${SEG} h, ends $(date -d @$end +%T), list $list" >> "$log"

reap() {
    for pid in "${!used[@]}"; do
        if ! kill -0 "$pid" 2>/dev/null; then
            wait "$pid"; free=$((free + used[$pid])); unset "used[$pid]"
        fi
    done
}

lock() {    # take the case's lock unless a live job holds it
    local l=$1/.sedps_lock
    if mkdir "$l" 2>/dev/null; then echo "$SLURM_JOB_ID" > "$l/job"; return 0; fi
    local j; j=$(cat "$l/job" 2>/dev/null)
    if [[ -n $j ]] && squeue -h -j "$j" 2>/dev/null | grep -q .; then return 1; fi
    echo "$SLURM_JOB_ID" > "$l/job"; return 0      # stale lock from a finished job
}

chain() {   # run segments of one case until done or out of time
    local case=$1 cs=$ROOT/$1/case_scripts
    trap 'rm -rf "'"$cs"'/.sedps_lock"' EXIT
    cd "$cs" || return 1
    [[ -f .sedps_target ]] || ./xmlquery --value STOP_N < /dev/null > .sedps_target
    [[ -f .sedps_done ]] || echo 0 > .sedps_done
    local target done est
    target=$(cat .sedps_target)
    while :; do
        done=$(cat .sedps_done)
        (( done >= target )) && { echo "$(date +%T) $case complete" >> "$log"; return 0; }
        est=$(tail -1 segments.log 2>/dev/null | awk '{print $4}')
        est=${est:-$(( ${SEDPS_SEG_MIN:-25} * 60 ))}
        if (( $(date +%s) + est * 12 / 10 + 180 > end )); then
            echo "$(date +%T) $case stop at ${done}/${target} h (not enough time left)" >> "$log"; return 0
        fi
        local seg=$(( target - done < SEG ? target - done : SEG ))
        if (( done == 0 )); then
            ./xmlchange CONTINUE_RUN=FALSE,STOP_OPTION=nhours,STOP_N=$seg,REST_OPTION=nhours,REST_N=$seg < /dev/null
        else
            ./xmlchange CONTINUE_RUN=TRUE,STOP_OPTION=nhours,STOP_N=$seg,REST_OPTION=nhours,REST_N=$seg < /dev/null
        fi
        local t0=$(date +%s)
        ./case.submit --no-batch > submit.seg$done.log 2>&1 < /dev/null
        if grep -q "CASE.RUN HAS FINISHED" submit.seg$done.log && ! grep -q "RUN FAIL" submit.seg$done.log; then
            echo $(( done + seg )) > .sedps_done
            echo "seg $done-$((done + seg)) h $(( $(date +%s) - t0 )) s" >> segments.log
            echo "$(date +%T) $case seg $done->$((done + seg)) h ok $(( $(date +%s) - t0 ))s" >> "$log"
        else
            echo "$(date +%T) $case seg $done FAILED, see $cs/submit.seg$done.log" >> "$log"; return 1
        fi
    done
}

while read -r case; do
    [[ -z $case || $case == \#* ]] && continue
    cs=$ROOT/$case/case_scripts
    if [[ -f $cs/.sedps_done && -f $cs/.sedps_target ]] && (( $(cat "$cs/.sedps_done") >= $(cat "$cs/.sedps_target") )); then
        continue
    fi
    ntasks=$(cd "$cs" && ./xmlquery --value NTASKS_ATM < /dev/null)
    need=$(( (ntasks + 3) / 4 ))
    (( need > total )) && continue
    while (( need > free )); do sleep 5; reap; done
    (( $(date +%s) + 600 > end )) && break
    lock "$cs" || continue
    ( chain "$case" ) &
    used[$!]=$need; free=$((free - need))
    echo "$(date +%T) launch $case on $need node(s), $free free" >> "$log"
    sleep 2
done < "$list"
wait
echo "$(date +%T) all done" >> "$log"
