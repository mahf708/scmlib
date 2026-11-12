#!/bin/bash
#SBATCH -A e3sm -C cpu -q debug -N 1 -t 00:20:00 -J sedps_ms_prof
# Mixed-layer time series (profiles_ts.py) for every complete 12 h run.
R=/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h
O=$R/manuscript
S=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts
cases=()
for d in $R/sedps_*; do
  f=$d/case_scripts/.sedps_done
  if [ -f $f ] && [ "$(cat $f)" != "12" ]; then continue; fi
  cases+=($d)
done
NPROC=64 /opt/cray/pe/python/3.12.12/bin/python3 $S/profiles_ts.py $O/tables/ml_timeseries.csv "${cases[@]}" > $O/profiles.log 2>&1
