#!/bin/bash
#SBATCH -A e3sm -C cpu -q debug -N 1 -t 00:30:00 -J sedps_ms_new
# Process runs that finished after analysis_report5 was built:
#   sbatch newruns_job.sh CASE [CASE ...]
# Writes summary/timeseries rows to $O/newruns/<case>/ and the explore npz to
# the shared explore/npz dir, and the column statistics to $O/fields/.
R=/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h
O=$R/manuscript
A=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/analysis
S=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts
PY=/opt/cray/pe/python/3.12.12/bin/python3
export SEDPS_TEND=12
for c in "$@"; do
  W=$O/newruns/$c; mkdir -p $W/root
  ln -sfn $R/$c $W/root/$c
  (cd $A && $PY analyze_sedps.py $W/root $W > $W/analyze.out 2>&1) &
  (cd $A && $PY timeseries_csv.py $W/root $W/timeseries_15min.csv > $W/ts.out 2>&1) &
done
(cd $A && NPROC=4 $PY explore.py $R/explore/npz $(for c in "$@"; do echo $R/$c; done) > $O/newruns/explore_$(date +%s).log 2>&1) &
NPROC=8 $PY $S/extract_fields.py $O/fields $(for c in "$@"; do echo $R/$c; done) > $O/newruns/fields_$(date +%s).log 2>&1 &
wait
