# Handoff: ACI x resolution study in DP-EAMxx (DYCOMS-II RF02)

This note gives you what you need to rebuild the setup, reproduce the test
runs, and carry the study forward. It covers the code and where it lives, how
to build and run, the pitfalls we already hit, what the results show so far,
and what is still open.

## The question

How does the response of drizzling stratocumulus LWP to droplet number
(Nd = 20, 50, 100, 200 cm-3) change as doubly periodic EAMxx (DP-EAMxx) goes
from ~40 km down to ~150 m? And does the new SHOC-HOMME 3D turbulence change
the sub-km answer? The case is the 6 h nocturnal DYCOMS-II RF02 IOP.

## Code

| what | where |
|---|---|
| scmlib (upstream) | https://github.com/E3SM-Project/scmlib, `master` |
| this study | branch `new-aci-study-oct0206` on https://github.com/mahf708/scmlib, directory `aci-res-study/` |
| E3SM | https://github.com/E3SM-Project/E3SM, `master` at or after `0f3298812a` (2026-10-26). It must include PR #8630 (3D turbulence, merged 2026-09-04). |
| optional E3SM speed-up | commit `66951b3838` on branch `mahf708/eamxx/fast-col-perturb` of https://github.com/mahf708/E3SM: cuts DP initialization by ~7 min per sub-km run, with bit-identical results (see below) |

The study branch sits on top of upstream scmlib `master`, and it also carries
the earlier `inverted-v-res-study/` work (rebased). Everything for this study is
in `aci-res-study/`:

| file | what |
|---|---|
| `README.md` | study design, every setting and why, measured costs, test results |
| `run_dpxx_scream_DYCOMSrf02_aci.csh` | one run: `./run_dpxx_scream_DYCOMSrf02_aci.csh <res> <nd> <on\|off>` |
| `submit_matrix.sh` | the 48-run matrix. Dry run by default; `go [res ...]` creates, builds and submits. |
| `compute_spa_factors.py` | derives the SPA activation factor for each target Nd |
| `yaml_file_example/` | output streams |
| `analysis/analyze_runs.py` | per-run diagnostics, giving `summary_h4-6.csv` and `timeseries.{nc,csv}` |
| `analysis/plot_runs.py`, `plot_maps.py`, `cell_scale.py` | figures, LWP maps, dominant cell size |

## Rebuilding the setup (Perlmutter GPU)

```bash
# E3SM
git clone git@github.com:E3SM-Project/E3SM.git E3SM-master
cd E3SM-master
git submodule update --init --recursive
# optional: the init speed-up
git remote add mahf708 git@github.com:mahf708/E3SM.git
git fetch mahf708 mahf708/eamxx/fast-col-perturb
git cherry-pick 66951b3838

# scmlib + study
git clone git@github.com:E3SM-Project/scmlib.git
cd scmlib
git remote add mahf708 git@github.com:mahf708/scmlib.git
git fetch mahf708 new-aci-study-oct0206
git checkout -b new-aci-study-oct0206 mahf708/new-aci-study-oct0206
```

Then set these at the top of `aci-res-study/run_dpxx_scream_DYCOMSrf02_aci.csh`:
`code_dir`/`code_tag` (your E3SM checkout), `casedirectory`, `yamlpath`, and
`projectname`. `submit_matrix.sh` assumes `casedirectory` is
`$PSCRATCH/dp_screamxx_aci_res`. Edit its `ACI_EXEROOT` line if you change that.

Run it:

```bash
cd scmlib/aci-res-study
./submit_matrix.sh                 # list the runs
./submit_matrix.sh go 40km 20km    # cheap end first: builds once, then submits
```

The first case builds (~15 min with `GMAKE_J=64`). Every other case reuses that
executable through `ACI_EXEROOT`. To reuse an existing build, export
`ACI_EXEROOT=<that case>/build` before running either script.

**Interactive testing in an `salloc`.** Replace `./case.submit` at the end of
the run script with nothing, then run `./case.submit --no-batch` in the case
directory. Use `setsid nohup` for anything you launch from a session that may
drop; we lost a run to that. `export SLURM_OVERLAP=1` lets a small run share
nodes with a build.

## Pitfalls we hit (all handled in the scripts)

- **Use stub sea ice (SICE), not CICE.** CICE compiles the column count into
  the executable (`-DNXGLOB=ICE_NX`, `components/cice/bld/configure`), so each
  resolution would need its own build. The run script uses
  `2010_SCREAM_ELM%SPBC_SICE_DOCN%DOM_SROF_SGLC_SWAV_SIAC_SESP%DP-EAMxx%IOP`.
  One executable then runs every resolution. Output is bit-for-bit identical to
  CICE here (no sea ice at 31.5N in July), and the cost is the same.
- **`GMAKE_J=64`.** The pm-gpu default of 6 makes a build take ~28 min.
- **DP needs `num_ne_x >= 5`.** `ne = 2` aborts in HOMME connectivity, and
  `ne < 5` aborts in planar semi-Lagrangian transport. This forces the domain
  choices below.
- **Sub-km time stepping** (carried over from `inverted-v-res-study`): from
  1.25 km down, `se_tstep = model_dtime/24` (not `/12`) and `nu_top` scaled
  down with dx. `dyn_ratio` must be a multiple of 6. At 5 km and coarser,
  `model_dtime` stays at 100 s. 1.25 km and 625 m are stable for 6 h with 3D
  turbulence off and on.
- **Run length.** With `rad_frequency = 3`, the number of steps must be a
  multiple of 3, or case setup fails.
- **GPU memory** (A100 40 GB, 128 levels, 3D turbulence on): ~11 GB fixed plus
  ~9 MB per element. 2,304 elements per GPU peaks at 78 % (comfortable),
  2,916 at 92 %, and 3,364 runs out of memory. Size runs at <= ~2,300 elements
  per GPU. Cost per element is flat between 1,600 and 2,500.
- **Slow DP initialization.** `scream::impl::perturb` applies the initial
  `T_mid` noise one (column, level) at a time on the GPU: ~9 min at 1,024
  elements per GPU. The optional E3SM commit does it in one host pass with the
  same random draws (bit-identical), and init drops 520 s -> 88 s at 625 m.
  It is not upstream yet. A device-side counter-based RNG would be cleaner, but
  would change answers.
- **SPA -> Nd.** With `spa_ccn_to_nc_exponent = 1`, in-cloud Nd = factor x
  CCN3 x rho, independent of cloud fraction. The factors (0.188, 0.471, 0.941,
  1.882) give medians 10-25 % above target, so analyse against the diagnosed
  Nd (`analyze_runs.py` does).
- **Entrainment rate.** The large-scale subsidence is an IOP forcing tendency,
  so the model's domain-mean omega does not contain it. `analyze_runs.py`
  takes w_subs from the IOP file.
- The `PBLEntrainmentBudget*` output fields on this branch's
  `DPxx_SCREAM_SCRIPTS` yamls are not on E3SM master, so the study yamls leave
  them out.

## Test runs so far

All runs are 6 h, on 4 pm-gpu nodes, with the study script and SICE
executable. Run directories are under
`/pscratch/sd/m/mahf708/dp_screamxx_aci_res/timing/` (`tt2_<res>_nd<Nd>_t3d<on|off>`,
plus older `tt_aci_*`). Analysis output is under
`/pscratch/sd/m/mahf708/dp_screamxx_aci_res/analysis/`. Pscratch is purged, so
copy anything you want to keep.

Domains: 600 km at 40 km and 300 km at 20 km (both ne 5); 240 km from 10 km
down. Hour 4-6 means, with Nd as diagnosed in-cloud medians:

| dx | Nd (target -> diagnosed) | LWP (g/m2) | cloud cover | rain (mm/day) | w_e (mm/s) |
|---|---|---|---|---|---|
| 5-40 km | 20 -> 26 | 134 | 1.00 | 1.14 | 2.9 |
| | 50 -> 59 | 157 | 1.00 | 0.12 | 5.0 |
| | 100 -> 111 | 182 | 1.00 | 0.04 | 4.9 |
| | 200 -> 232 | 203 | 1.00 | 0.01 | 4.8 |
| 2.5 km | 20 -> 23 | 79 | 0.78 | 1.66 | 4.2 |
| | 50 -> 56 | 132 | 0.96 | 0.68 | 5.9 |
| | 100 -> 122 | 158 | 0.99 | 0.14 | 6.4 |
| | 200 -> 247 | 164 | 1.00 | 0.02 | 6.6 |
| 1.25 km | 20 -> 22 | 78 | 0.80 | 1.30 | 3.5 |
| | 50 -> 55 | 132 | 0.96 | 0.52 | 4.8 |
| | 100 -> 118 | 152 | 0.99 | 0.08 | 6.0 |
| | 200 -> 235 | 152 | 0.99 | 0.01 | 6.6 |
| 625 m | 20 -> 20 | 62 | 0.71 | 0.84 | 4.7 |
| | 100 -> 112 | 138 | 0.97 | 0.05 | 7.2 |
| 625 m, 3D turbulence on | 100 -> 113 | 138 | 0.97 | 0.05 | 7.1 |

Still running when this was written: 625 m Nd 200 (3D turbulence off), and
Nd 20 and 200 with 3D turbulence on. Their output goes to the same place. Re-run
`analysis/analyze_runs.py` to add them.

Costs (stepping only, 6 h):

| dx | GPUs | time |
|---|---|---|
| 5-40 km | 4 | ~20 s |
| 2.5 km | 8 | 44 s |
| 1.25 km | 16 | 2.2 min |
| 625 m | 16 | 13.5 min |

3D turbulence adds 1-9 %. Extrapolated at the same per-GPU load: 312 m about
27 min on 64 GPUs, 156 m about 68 min on 256 GPUs.

## What we think we know (preliminary: one 6 h realization each)

1. **At >= 5 km, DP-EAMxx behaves like a single column.** The initial noise
   never grows, so all columns stay identical and SHOC carries all the
   turbulence. Results at 5-40 km agree within ~2 %.
2. **The switch to resolved dynamics happens between 5 and 2.5 km.**
   - At <= 2.5 km, cellular circulations develop.
   - SHOC's TKE, buoyancy flux and mixing length drop to ~60 %
     (936 -> 598 m). There is no explicit dx dependence in SHOC, beyond a cap
     at sqrt(dx dy).
   - Entrainment jumps from ~4.9 to 6-7 mm/s.
3. **The LWP response to Nd changes shape with resolution.**

   | dx | S, low Nd | S, high Nd |
   |---|---|---|
   | >= 5 km | 0.20 | 0.15 |
   | 2.5 km | 0.57 | 0.05 |
   | 1.25 km | 0.57 | ~0 |

   S = d ln LWP / d ln Nd, split at ~80 cm-3.
   - At >= 5 km the response is GCM-like: monotonic, with rain suppression
     dominant and entrainment flat in Nd.
   - At <= 2.5 km it starts to look like an inverted V. At low Nd the deck
     breaks up under drizzle. At high Nd, entrainment rising with Nd offsets
     rain suppression.
   - At 625 m the low-Nd branch steepens further (LWP 62 g/m2, cloud cover
     0.71 at Nd 20). Whether the high-Nd branch turns negative depends on the
     pending 625 m Nd 200 run.
4. **Km-scale cells are grid-controlled.** The dominant LWP wavelength is
   24 km (6.4 physics cells) at 2.5 km, 15 km (8) at 1.25 km and 12 km (13) at
   625 m. It does not depend on Nd. So the 2.5-1.25 km results are grey-zone,
   not converged, and the sub-km levels carry the weight.
5. **3D turbulence makes no difference at 625 m and Nd 100** (LWP, w_e, z_i
   and cell size all agree within 1 %). The horizontal diffusivity there is
   ~30 m2/s. Its effect at low and high Nd is pending.

Not yet established: the mechanism behind entrainment rising with Nd.
Sedimentation-evaporation at cloud top is the obvious candidate. A first
attempt using P3's `qc_sed` gave numbers that make no physical sense (probably
a units or sign convention), so check that diagnostic before using it.

## Open decisions and next steps

1. **Domain.** The current scripts use 240 km for dx <= 10 km plus larger
   domains at 20 and 40 km. A fixed domain is cleaner for mesoscale
   organization, which matters at low Nd. The options are in the `README.md`
   "Domain" section: A (600 km, all levels, ~4,500 node-hours), B (300 km,
   20 km -> 156 m, ~1,100 node-hours, the recommendation), or C (240 km,
   10 km -> 156 m, ~700 node-hours). Re-pack ranks at ~2,300 elements per GPU
   when you change it.
2. **Sub-km production.** 312 m and 156 m have not been run. Submit them in the
   batch queue (`./submit_matrix.sh go 312m 156m`) once the domain is fixed.
3. **Robustness.**
   - Repeat with 2-3 perturbation seeds (`generate_perturbation_random_seed=true`).
   - Try the 12 h RF02 forcing (`DYCOMSrf02_12hr_PMCnBLH_4scam.nc`), since LWP
     adjustment is slow.
   - Trim the SPA factors by ~0.83 if you want Nd on target.
4. **Mechanism diagnostics.**
   - Cloud-top sedimentation (verify `qc_sed`).
   - Cloud-top radiative cooling (`rad_heating_pdel`).
   - Resolved fluxes from the 3D snapshots.
   - Cloud-base vs surface rain.
5. **Upstreaming.** The `perturb` speed-up, and possibly a device-side
   counter-based RNG as a separate, non-bit-for-bit change.

## Reproducing the analysis

```bash
cd scmlib/aci-res-study/analysis
python3 analyze_runs.py <runroot> <outdir>   # needs xarray (Cray python3 + user site)
module load python
python plot_runs.py <outdir>                 # needs matplotlib (NERSC conda python)
python plot_maps.py <outdir>/maps.png 20,200 "<runroot>/tt2_2p5km_nd{nd}_t3doff" ...
python cell_scale.py <runroot>/tt2_625m_nd100_t3doff ...
```

`analyze_runs.py` picks up any `tt2_<res>_nd<Nd>_t3d<on|off>` case with a full
6 h of output. Rename the patterns in `find_runs()` if you name production
cases differently. Production cases from `submit_matrix.sh` are named
`scream_dpxx_DYCOMSrf02_aci_<res>_nd<Nd>_t3d<on|off>`.
