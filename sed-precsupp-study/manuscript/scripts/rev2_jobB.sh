#!/bin/bash
#SBATCH -A e3sm -C cpu -q debug -N 1 -t 00:30:00 -J sedps_r2B
PY=/opt/cray/pe/python/3.12.12/bin/python3
c=$(ls -d /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/sedps_* | grep -v t3don | grep -v 312m)
NPROC=32 $PY /pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts/rev2_3d.py /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/rev2/d3_a.csv $c > /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/rev2/d3_a.log 2>&1
