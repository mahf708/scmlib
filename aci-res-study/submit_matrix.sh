#!/bin/bash
#
# Create, build and submit the ACI x resolution x 3D-turbulence matrix.
#
#   ./submit_matrix.sh                 # print the matrix only (dry run)
#   ./submit_matrix.sh go              # create/build/submit everything
#   ./submit_matrix.sh go 40km 20km    # only these resolutions
#
# 3D turbulence is only toggled at sub-km resolutions; everything else runs
# with it off.  The first case is built; every other case reuses that
# executable (the SICE compset makes the build resolution independent).
# To reuse an existing build instead, export ACI_EXEROOT before running.

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

log() { echo "log.$(echo "$1" | tr ' ' '_')"; }

if [[ -z $ACI_EXEROOT ]]; then
    # build with the first case, then share its executable
    first=${runs[0]}
    runs=("${runs[@]:1}")
    # shellcheck disable=SC2086
    ./run_dpxx_scream_DYCOMSrf02_aci.csh $first > "$(log "$first")" 2>&1 || {
        echo "first case ($first) failed, see $(log "$first")"; exit 1; }
    read -r res nd turb3d <<< "$first"
    export ACI_EXEROOT=$PSCRATCH/dp_screamxx_aci_res/scream_dpxx_DYCOMSrf02_aci_${res}_nd${nd}_t3d${turb3d}/build
fi

for run in "${runs[@]}"; do
    # shellcheck disable=SC2086
    ./run_dpxx_scream_DYCOMSrf02_aci.csh $run > "$(log "$run")" 2>&1 &
    # stagger case creation to avoid overloading the login node
    sleep 20
done
wait
