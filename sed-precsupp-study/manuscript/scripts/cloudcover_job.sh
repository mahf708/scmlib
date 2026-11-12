#!/bin/bash
#SBATCH -A e3sm -C cpu -q debug -N 1 -t 00:30:00 -J sedps_ms_cc
R=/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h
S=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts
cases=$(ls -d $R/sedps_* | grep -v t3don)
NPROC=24 /opt/cray/pe/python/3.12.12/bin/python3 $S/cloudcover_3d.py $R/manuscript/tables/cloudcover_3d.csv $cases > $R/manuscript/cloudcover.log 2>&1
