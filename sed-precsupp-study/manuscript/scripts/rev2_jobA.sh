#!/bin/bash
#SBATCH -A e3sm -C cpu -q debug -N 1 -t 00:30:00 -J sedps_r2A
PY=/opt/cray/pe/python/3.12.12/bin/python3
off=$(ls -d /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/sedps_* | grep -v t3don)
all=$(for d in /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/sedps_*; do f=$d/case_scripts/.sedps_done; if [ -f $f ] && [ "$(cat $f)" != "12" ]; then continue; fi; echo $d; done)
NPROC=40 $PY /pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts/rev2_cols.py /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/rev2/cols $off > /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/rev2/cols.log 2>&1 &
NPROC=40 $PY /pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts/profiles_ts2.py /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/tables/ml_timeseries2.csv $all > /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/rev2/prof2.log 2>&1 &
wait
