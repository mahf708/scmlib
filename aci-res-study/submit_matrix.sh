#!/bin/bash
#
# Create, build and submit the ACI x resolution x 3D-turbulence matrix.
#
#   ./submit_matrix.sh                 # print the matrix only (dry run)
#   ./submit_matrix.sh go              # create/build/submit everything
#   ./submit_matrix.sh go 40km 20km    # only these resolutions
#
# 3D turbulence is only toggled at sub-km resolutions; everything else runs
# with it off.

cd "$(dirname "$0")"

ALL_RES=(40km 20km 10km 5km 2p5km 1p25km 625m 312m 156m)
SUBKM_RES=(625m 312m 156m)
ALL_ND=(20 50 100 200)

mode=${1:-dry}
shift
res_list=("${@:-${ALL_RES[@]}}")

runs=()
for res in "${res_list[@]}"; do
    for nd in "${ALL_ND[@]}"; do
        runs+=("$res $nd off")
        if [[ " ${SUBKM_RES[*]} " == *" $res "* ]]; then
            runs+=("$res $nd on")
        fi
    done
done

for run in "${runs[@]}"; do
    echo "$run"
done
echo "${#runs[@]} runs"

if [[ $mode != go ]]; then
    exit 0
fi

for run in "${runs[@]}"; do
    # shellcheck disable=SC2086
    ./run_dpxx_scream_DYCOMSrf02_aci.csh $run > "log.$(echo $run | tr ' ' '_')" 2>&1 &
    # stagger case creation/builds to avoid overloading the login node
    sleep 200
done
wait
