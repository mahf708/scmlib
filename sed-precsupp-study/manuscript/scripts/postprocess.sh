#!/bin/bash
# Rebuild every table, figure and the PDF from the per-run products (login node; light work).
# To add runs that finished later, first run on a compute node:
#   sbatch newruns_job.sh CASE [CASE ...]   (summary, timeseries, explore npz, column fields)
#   sbatch profiles_job.sh                  (mixed-layer time series for all complete runs)
# then run this script.  Text that quotes run counts (358 runs, 70 of 72, 34 of 36) must be edited by hand.
set -e
type module >/dev/null 2>&1 || source /etc/profile
S=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts
M=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript
O=/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript
PY=/opt/cray/pe/python/3.12.12/bin/python3
cd $S
$PY build_tables.py
$PY ml_budget.py
$PY key_numbers.py > $O/tables/key_numbers.txt
$PY make_tables_tex.py > /dev/null
module load python
python make_figures.py 2>&1 | grep -v -i warning || true
module load texlive/2024
cd $M
pdflatex -interaction=nonstopmode sedps_acp_manuscript.tex > /dev/null || true
bibtex sedps_acp_manuscript > /dev/null || true
pdflatex -interaction=nonstopmode sedps_acp_manuscript.tex > /dev/null || true
pdflatex -interaction=nonstopmode sedps_acp_manuscript.tex > /dev/null || true
grep -E "^!|undefined" sedps_acp_manuscript.log || true
cp sedps_acp_manuscript.pdf $O/sedps_acp_manuscript.pdf
chmod -R a+rX $M $O
