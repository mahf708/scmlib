#!/bin/bash
# Rebuild every table, figure and the PDF from the per-run products (login node; light work).
# Compute-node prerequisites (CPU debug queue): newruns_job.sh <cases> for runs that finished
# later, profiles_job.sh (mixed-layer time series), cloudcover_job.sh (subgrid cloud cover).
# Text that quotes run counts (288 + 70 runs, 34 of 36 pairs at 312 m) must be edited by hand.
type module >/dev/null 2>&1 || source /etc/profile
S=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/scripts
M=/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript
O=/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript
PY=/opt/cray/pe/python/3.12.12/bin/python3
cd $S
$PY build_tables.py
$PY ml_budget.py
$PY revision_analysis.py
$PY key_numbers.py > $O/tables/key_numbers.txt
$PY make_tables_tex.py > /dev/null
module load python
python make_figures_rev.py 2>&1 | grep -v -i warning || true
module load texlive/2024
cd $M
$PY $S/fetch_bib.py refs/dois.txt refs/extra.bib > refs/refs_raw.bib
pdflatex -interaction=nonstopmode sedps_acp_manuscript.tex > /dev/null || true
$PY $S/finalize_bib.py refs/refs_raw.bib sedps_acp_manuscript.aux sedps_refs.bib
bibtex sedps_acp_manuscript > /dev/null || true
pdflatex -interaction=nonstopmode sedps_acp_manuscript.tex > /dev/null || true
pdflatex -interaction=nonstopmode sedps_acp_manuscript.tex > /dev/null || true
$PY -c "
t=open('$M/sedps_acp_manuscript.log',errors='replace').read().splitlines()
print([l[:140] for l in t if any(k in l for k in ('Error','! ','Overfull','undefined','Output written'))])"
cp sedps_acp_manuscript.pdf $O/sedps_acp_manuscript.pdf
chmod -R a+rX $M $O
