#!/bin/bash
#SBATCH -A e3sm -C cpu -q debug -N 1 -t 00:30:00 -J sedps_ms_fields
# Column statistics (extract_fields.py) for every complete 12 h run.
R=/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h
O=$R/manuscript
S=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts
cases=()
for d in $R/sedps_*; do
  f=$d/case_scripts/.sedps_done
  if [ -f $f ] && [ "$(cat $f)" != "12" ]; then continue; fi
  ls $d/run/*.aci2d.INSTANT.*.nc >/dev/null 2>&1 || continue
  cases+=($d)
done
echo "${#cases[@]} cases" > $O/fields.log
NPROC=64 /opt/cray/pe/python/3.12.12/bin/python3 $S/extract_fields.py $O/fields "${cases[@]}" >> $O/fields.log 2>&1
