#!/bin/bash
#
# Create (not run) the cases of the matrix, reusing one build.
#
#   SEDPS_EXEROOT=<case>/build ./create_cases.sh [res ...]
#   SEDPS_HOURS=12 ...                 (12 h runs, in $PSCRATCH/dp_screamxx_sedps_12h)
#   SEDPS_ND="500 1000" SEDPS_LIST_SUFFIX=_hiNd ...   (other Nd levels, separate lists)
#
# Writes one case-list file per resolution to $SEDPS_ROOT/lists/, for
# run_packed.sh.  Sub-km resolutions are on hold (see README.md).

cd "$(dirname "$0")"
if [[ ${SEDPS_HOURS:-6} == 6 ]]; then
    ROOT=${SEDPS_ROOT:-$PSCRATCH/dp_screamxx_sedps}
else
    ROOT=${SEDPS_ROOT:-$PSCRATCH/dp_screamxx_sedps_${SEDPS_HOURS}h}
fi
: "${SEDPS_EXEROOT:?set SEDPS_EXEROOT to a finished build}"
export SEDPS_EXEROOT
mkdir -p "$ROOT/logs" "$ROOT/lists"

res_list=("${@:-40km 20km 10km 5km 2p5km 1p25km}")
# shellcheck disable=SC2206
res_list=(${res_list[*]})
par=${SEDPS_PAR:-6}

for res in "${res_list[@]}"; do
    lst=$ROOT/lists/$res${SEDPS_LIST_SUFFIX}.txt
    : > "$lst"
    for nd in ${SEDPS_ND:-20 50 100 200}; do
        for sed in 0p5 1 2; do
            for ps in on off; do
                case=sedps_${res}_nd${nd}_sed${sed}_ps${ps}$([[ ${SEDPS_TURB3D:-off} == on ]] && echo _t3don)
                echo "$case" >> "$lst"
                if [[ -d $ROOT/$case/case_scripts ]]; then continue; fi
                while (( $(jobs -rp | wc -l) >= par )); do sleep 3; done
                ./run_dpxx_scream_DYCOMSrf02_sedps.csh "$res" "$nd" "$sed" "$ps" \
                    > "$ROOT/logs/create.$case.log" 2>&1 &
                sleep 2
            done
        done
    done
done
wait
for res in "${res_list[@]}"; do
    n=0
    while read -r c; do
        grep -qs "^ERROR\|Exception" "$ROOT/logs/create.$c.log" && { echo "FAILED: $c"; continue; }
        n=$((n+1))
    done < "$ROOT/lists/$res${SEDPS_LIST_SUFFIX}.txt"
    echo "$res: $n cases ok"
done
