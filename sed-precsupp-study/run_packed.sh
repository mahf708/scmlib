#!/bin/bash
#
# Run already-created cases inside one allocation, packing them onto the
# allocation's nodes.  Each case runs with ./case.submit --no-batch, so its
# srun becomes a job step on its own nodes (4 GPU ranks fill a node).
#
#   sbatch [...] run_packed.sh <caselist>
#
# <caselist>: one case name per line (under $SEDPS_ROOT); the node count of a
# case is NTASKS_ATM/4.  Cases that already finished (CASE.RUN HAS FINISHED in their
# submit log) are skipped, so the same list can be resubmitted.

ROOT=${SEDPS_ROOT:-$PSCRATCH/dp_screamxx_sedps}
list=$1
total=${SLURM_JOB_NUM_NODES:?run inside an allocation}
log=$ROOT/logs/packed.${SLURM_JOB_ID}.log
free=$total
declare -A used

echo "$(date +%T) start: $total nodes, list $list" >> "$log"

reap() {
    for pid in "${!used[@]}"; do
        if ! kill -0 "$pid" 2>/dev/null; then
            wait "$pid"
            free=$((free + used[$pid]))
            unset "used[$pid]"
        fi
    done
}

while read -r case; do
    [[ -z $case || $case == \#* ]] && continue
    cs=$ROOT/$case/case_scripts
    if grep -qs "CASE.RUN HAS FINISHED" "$cs/submit.packed.log" && ! grep -qs "RUN FAIL" "$cs/submit.packed.log"; then
        echo "$(date +%T) skip $case (done)" >> "$log"; continue
    fi
    ntasks=$(cd "$cs" && ./xmlquery --value NTASKS_ATM)
    need=$(( (ntasks + 3) / 4 ))
    while (( need > free )); do sleep 5; reap; done
    (
        cd "$cs" || exit 1
        start=$(date +%s)
        ./case.submit --no-batch > submit.packed.log 2>&1
        rc=$?
        echo "$(date +%T) end $case rc=$rc $(( $(date +%s) - start ))s" >> "$log"
    ) &
    used[$!]=$need
    free=$((free - need))
    echo "$(date +%T) launch $case on $need node(s), $free free" >> "$log"
    sleep 2
done < "$list"
wait
echo "$(date +%T) all done" >> "$log"
