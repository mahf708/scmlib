# ACI x resolution x 3D-turbulence study (DYCOMS-II RF02, DP-EAMxx)

How does the Nd-LWP relationship of drizzling stratocumulus change as DP-EAMxx
goes from 40 km to ~150 m, and does the new SHOC-HOMME 3D turbulence change
the sub-km answer?

| factor | levels |
|---|---|
| Nd (in-cloud, #/cm3) | 20, 50, 100, 200 |
| dx (dynamics) | 40, 20, 10, 5, 2.5, 1.25 km, 625, 312.5, 156.25 m |
| 3D turbulence | off everywhere; on *and* off at 625, 312.5, 156.25 m |
| domain | 240 km x 240 km for dx <= 10 km; 300 km at 20 km, 600 km at 40 km |

That is 4 x 9 = 36 runs with 3D turbulence off plus 4 x 3 = 12 with it on:
48 runs. Each one is the 6 h nocturnal RF02 case (SW off, T/q nudged above
650 hPa, the same as upstream `DPxx_SCREAM_SCRIPTS`).

## Files

| file | what |
|---|---|
| `run_dpxx_scream_DYCOMSrf02_aci.csh` | one run: `./run_dpxx_scream_DYCOMSrf02_aci.csh <res> <nd> <on\|off>` |
| `submit_matrix.sh` | prints the matrix; `./submit_matrix.sh go [res ...]` launches it |
| `compute_spa_factors.py` | derives the SPA factor for each Nd from the SPA and IOP files |
| `yaml_file_example/` | output streams (profiles, column 2D, trimmed 3D, 3D-turb fields) |

Before running, set `code_dir`/`code_tag` (E3SM master **at or after PR #8630**,
merged 2026-09-04, for the 3D turbulence switch) and `yamlpath` at the top of
the run script. Start with the cheap end, e.g. `./submit_matrix.sh go 40km 20km`.

**One build for everything.** The study uses the DP compset with stub sea ice
(`..._SICE_...` instead of `CICE%PRES`). CICE compiles the column count into
the executable (`-DNXGLOB=ICE_NX`, `components/cice/bld/configure`), so with
CICE every resolution needs its own build. With SICE, one executable runs
every resolution. This was tested by building for 312 m and running at 40 km.
There is no sea ice at 31.5N in July, and the SICE and CICE runs cost the same.
`submit_matrix.sh` builds the first case and points all the others at its
executable (`ACI_EXEROOT`).

## Domain and the element-count constraints

Resolution follows the scmlib convention `dx = L / (3 * num_ne_x)` (unique
dynamics GLL points), with `num_ne_x` an integer. Two more limits were found by
running:

- `num_ne_x = 2` aborts in HOMME (`Connectivity::setup_ucon: Element's first
  four connections are not edges in S, N, W, E order`). On a periodic plane,
  an element's east and west neighbours are the same element.
- `num_ne_x < 5` aborts in tracer transport (`SL transport for planar geometry
  does not support min(ne_x, ne_y) < 5`).

So **num_ne_x >= 5**. A single fixed domain from 40 km to 156 m would need
600 km at 156 m (~6.5M physics columns), which is not practical. The domain is
therefore 240 km from 10 km down (`num_ne_x` = 8 ... 512, exact halvings) and
grows at the coarse end: 300 km at 20 km and 600 km at 40 km (`num_ne_x` = 5).
The forcing is horizontally uniform, so domain size mainly sets the number of
columns available for statistics.

The physics grid is 1.5x coarser than the label: `dx_phys = L / (2 *
num_ne_x)`. SHOC's horizontal length scale, and so the 3D turbulence
diffusivities, use the physics-grid spacing.

## Time steps and the sub-800 m CFL fix

`inverted-v-res-study/` was stable below 800 m because of two changes to the
upstream rule of thumb (dt halves with dx, `se_tstep = model_dtime/12`,
`nu_top` halves with dx):

1. **More dynamics substeps.** `se_tstep = model_dtime / 24`, not `/12`. The
   physics step stays relatively long (40 s at ~833 m, 20 s at ~417 m, 10 s at
   200 m, 5 s at 100 m) and the dynamics step comes out to ~2.0 s per km of dx,
   below the 2.5 s/km of the 3.33 km default.
2. **Lower `nu_top`.** 1111 m2/s at ~833 m, then halved with each halving of dx
   (555.6, 277.8, 138.9). That is more conservative than the linear rule from
   1e4 at 3.33 km.

`nu` (0.216784) was left alone. HOMME's tensor hyperviscosity
(`hypervis_scaling = 3`) already scales with element size.

This study applies the same recipe below 1 km (`dyn_ratio` = `model_dtime/se_tstep`):

| res | L (km) | num_ne_x | dx_phys (km) | physics cols | model_dtime (s) | dyn_ratio | se_tstep (s) | se_tstep per km dx | nu_top (m2/s) | 6 h phys steps | ranks (pm-gpu) | 6 h cost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40km   | 600 | 5   | 60    | 100       | 100 | 12 | 8.333 | 0.21 | 1.2e5 | 216   | 4 (1 node)     | ~20 s (as 20 km) |
| 20km   | 300 | 5   | 30    | 100       | 100 | 12 | 8.333 | 0.42 | 6e4   | 216   | 4 (1 node)     | measured 20 s |
| 10km   | 240 | 8   | 15    | 256       | 100 | 12 | 8.333 | 0.83 | 3e4   | 216   | 4 (1 node)     | measured 21 s |
| 5km    | 240 | 16  | 7.5   | 1,024     | 100 | 12 | 8.333 | 1.67 | 1.5e4 | 216   | 4 (1 node)     | measured 24 s |
| 2p5km  | 240 | 32  | 3.75  | 4,096     | 75  | 12 | 6.25  | 2.50 | 7500  | 288   | 8 (2 nodes)    | measured 44 s |
| 1p25km | 240 | 64  | 1.875 | 16,384    | 60  | 24 | 2.5   | 2.00 | 1667  | 360   | 16 (4 nodes)   | measured 2.2 min |
| 625m   | 240 | 128 | 0.94  | 65,536    | 30  | 24 | 1.25  | 2.00 | 833   | 720   | 16 (4 nodes)   | measured 13.5 min (13.6 min with 3D turbulence) |
| 312m   | 240 | 256 | 0.47  | 262,144   | 15  | 24 | 0.625 | 2.00 | 417   | 1,440 | 64 (16 nodes)  | ~27 min, extrapolated |
| 156m   | 240 | 512 | 0.23  | 1,048,576 | 6   | 24 | 0.25  | 1.60 | 208   | 3,600 | 256 (64 nodes) | ~68 min, extrapolated |

The cost column is model stepping only (CIME "Run Time"). Initialization adds
about 1.5 min at 1024 elements per GPU, or ~9 min on E3SM master without the
`perturb` fix described below. The 312 m and 156 m estimates keep 1024 elements
(4096 physics columns) per GPU, the 625 m load, so they scale with the number
of physics steps. 4096 elements per GPU does not fit: 312 m on 16 GPUs runs out
of A100 memory in RRTMGP init, even with `rrtmgp::pool_size_multiplier=0.25`,
while 1600 elements per GPU runs fine (2.5 km and 1.25 km on a 600 km domain).

Rough budget for the 48 runs:

| res | node-hours |
|---|---|
| 156 m (8 runs x 64 nodes x ~1.2 h) | ~600 |
| 312 m (8 runs x 16 nodes x ~0.55 h) | ~70 |
| everything else | ~15 |

Choices worth knowing about:

- **dx >= 5 km keeps `model_dtime` = 100 s** (the 3.33 km default) instead of
  growing it. SHOC and P3 are time-step sensitive, so this keeps the physics step
  from co-varying with dx across the coarse half of the sweep. The dynamics is
  far from its CFL limit there.
- **156 m uses 6 s**, not 7.5 s, because `model_dtime` must be an integer that
  divides 86400.
- `dyn_ratio` must be a multiple of 6, which is lcm(`dt_remap_factor` = 2,
  pg2 `dt_tracer_factor` = 6).
- `physics::mac_aero_mic::number_of_subcycles=1` is set explicitly, so the
  SHOC/P3 step is exactly `model_dtime`.
- The physics step still changes from 100 s to 6 s across the sweep. To separate
  dx from dt, add a 625 m or 312 m run at the next-coarser dt (e.g. 312m with
  dt = 30 s, ratio 48).

## Getting Nd from SPA

P3 activates SPA CCN in every cloudy cell
(`components/eamxx/src/physics/p3/impl/p3_main_impl_part1.hpp`):

```
nc = max(nc, spa_ccn_to_nc_factor * (CCN3 * cld_frac_l) ** spa_ccn_to_nc_exponent)     # nc, CCN3 in #/kg
```

With exponent = 1, the in-cloud Nd is `factor * CCN3 * rho`. It does **not**
depend on the liquid cloud fraction, which changes a lot between 40 km and
156 m. (Exponent 0 would give a grid-mean floor, so in-cloud Nd would be inflated
by 1/cld_frac at coarse resolution.)

`compute_spa_factors.py` reads the default SPA file
(`spa_from_v3LRamip_CMIP6_2010_clim_ne30pg2_c20260928.nc`, nearest column
31.28N 239.25E, interpolated to 11 July) and the IOP cloud layer (926-967 hPa,
rho = 1.15 kg/m3):

| setting | Nd at DYCOMS (#/cm3) |
|---|---|
| master default (factor 2000, exponent 0.55) | ~55 |
| raw SPA CCN3 (factor 1, exponent 1) | ~106 |

| target Nd | `spa_ccn_to_nc_factor` (exponent 1) |
|---|---|
| 20  | 0.1882 |
| 50  | 0.4706 |
| 100 | 0.9412 |
| 200 | 1.8824 |

CCN3 changes by about +/-25 % across the cloud layer (7.4e7 to 1.17e8 #/kg,
higher near cloud base). Nd therefore inherits SPA's vertical shape around these
means. `nccn_horiz_avg` and `LiqNumberPath` are in the output so you can check.

Test runs gave this median in-cloud Nd (#/cm3), computed as
`nc * rho / cldfrac_liq` where qc > 1e-5:

| run | target | 2 h | 4 h | 6 h | 10th-90th pct at 6 h | domain LWP at 6 h (g/m2) |
|---|---|---|---|---|---|---|
| 40 km  | 100 | 105 | 111 | 112 | 82-162  | 194 |
| 2.5 km | 20  | 24  | 24  | 23  | 17-33   | 71 |
| 2.5 km | 50  | 54  | 58  | 55  | 40-75   | 128 |
| 2.5 km | 100 | 106 | 123 | 122 | 82-145  | 163 |
| 2.5 km | 200 | 215 | 247 | 247 | 173-283 | 172 |

The factors scale linearly. The medians come out 10-25 % high, settling after
~2 h as Nd mixes up from the higher-CCN layers near cloud base. Multiply all
four factors by ~0.83 if you want the medians on target, or keep them and
analyse against the diagnosed Nd. Either way, the 2.5 km runs already show
the LWP response the study is after: 71 g/m2 at Nd 20 (drizzle depletion) to
172 g/m2 at Nd 200.

## Where the settings are

All of these are in `run_dpxx_scream_DYCOMSrf02_aci.csh`. Each block lists the
master defaults commented out, so you can vary them without looking anything
up.

| block | line | namelist group | knobs |
|---|---|---|---|
| resolution table | ~104 | `ctl_nl` | `se_ne_x/y`, `se_lx/ly`, `se_tstep`, `nu_top`, `nu` |
| Nd -> SPA factor table | ~149 | `p3` | per-Nd `spa_ccn_to_nc_factor` |
| **SPA settings** | ~318 | `p3` (spa process supplies `nccn`) | `do_prescribed_ccn`, `spa_ccn_to_nc_factor`, `spa_ccn_to_nc_exponent` (`spa_data_file` under `spa`) |
| **P3 settings** | ~327 | `p3` | `autoconversion_*`, `accretion_*`, `set_cld_frac_{l,r}_to_one`, `extra_p3_diags` |
| **SHOC settings** | ~343 | `shoc` | `length_fac`, `c_diag_3rd_mom`, `lambda_*`, `coeff_kh/km`, `shoc_1p5tke`, `extra_shoc_diags` |
| **3D turbulence** | ~356 | `ctl_nl` (+ `shoc`) | `ctl_nl::do_3d_turbulence`, `coeff_kh_horiz`, `coeff_km_horiz`, `ctl_nl::horiz_turb_subcycle{,_q}` |

Run `./atmquery --listall p3` (or `shoc`, `spa`, `ctl_nl`) in a case
directory to see every option.

## 3D turbulence

`./atmchange ctl_nl::do_3d_turbulence=true` (E3SM PRs #8013, #8392, #8630;
docs in `components/eamxx/docs/user/shoc_homme_3d_turbulence.md`):

- SHOC computes `K_h = coeff_k*_horiz * sqrt(dx*dy) * sqrt(TKE)` (both
  coefficients default to 0.1) and passes it to HOMME, which applies horizontal
  turbulent diffusion to momentum, heat and tracers.
- HOMME passes horizontal velocity gradients back to SHOC, which uses the full
  3D strain in TKE shear production.
- Do not touch `homme::do_3d_turbulence_homme`. It is locked and mirrored from
  `ctl_nl`.
- HOMME clips the horizontal diffusivities to an explicit CFL limit (target 1.0).
  If the clip is active a lot at 156 m, subcycle with
  `ctl_nl::horiz_turb_subcycle` and `ctl_nl::horiz_turb_subcycle_q` rather than
  shortening the time step.
- Extra output (`scream_turb3d_horiz_avg_output_15min.yaml`):
  `eddy_diff_{heat,mom}_horiz`, `tke_shear_strain3d`. These fields only exist
  when the switch is on, so the script adds this stream only then.

## Output

| stream | freq | content |
|---|---|---|
| `scream_horiz_avg_output_15min.yaml` | 15 min avg | upstream profile set + `nccn`, number paths, P3 warm-rain rates, extra SHOC diags |
| `scream_aci_2d_inst_15min.yaml` | 15 min inst | column LWP, `LiqNumberPath`, rain, PBL height, OLR, LWCF, surface fluxes (Nd-LWP joint stats) |
| `scream_aci_3d_inst_2hour.yaml` | 2 h inst | trimmed 3D state (~0.5 GB per field per snapshot at 156 m) |
| `scream_turb3d_horiz_avg_output_15min.yaml` | 15 min avg | 3D-turbulence fields (turb3d=on only) |

The `PBLEntrainmentBudget*` fields in `DPxx_SCREAM_SCRIPTS/yaml_file_example`
on this branch are not on E3SM master, so they are not included here.

## Test runs (pm-gpu, 2026-10-26, E3SM master 0f3298812a)

Nd 100, 3D turbulence off unless noted. "SICE" runs used the stub-ice
executable with the patched `perturb`, and every run after the CICE ones used
the current `run_dpxx_scream_DYCOMSrf02_aci.csh`:

| run | GPUs | model time | init (s) | stepping (s) | notes |
|---|---|---|---|---|---|
| 40 km (600 km, ne 5), SICE | 4 | 6 h | 63 | 214 | executable built for 312 m, so the build is grid-independent; GPUs shared with another run |
| 20 km (300 km, ne 5), SICE | 4 | 6 h | 13 | 20 | |
| 10 km, SICE | 4 | 6 h | 12 | 21 | |
| 5 km, SICE | 4 | 6 h | 16 | 24 | |
| 2.5 km, CICE | 8 | 6 h | 43 | 44 | unpatched `perturb` |
| 2.5 km, SICE, Nd 20 / 50 / 200 | 8 | 6 h | 20-22 | 44 | |
| 1.25 km | 16 | 6 h | 70 | 133 | dyn_ratio 24, stable |
| 625 m, CICE | 16 | 1 h | 520 | 137 | unpatched `perturb` |
| 625 m, SICE | 16 | 1 h | 88 | 135 | patched `perturb` |
| 625 m, SICE, 3D turbulence on | 16 | 1 h | 86 | 147 | horizontal Kh up to ~30 m2/s, LWP within 0.5 g/m2 of off |
| 625 m, SICE, 3D turbulence on | 16 | 6 h | 89 | 816 | stable; no NaNs, LWP 131-140 g/m2, horizontal Kh 26-30 m2/s; ~1 % over 6 x the 1 h off cost |
| 2.5 km on a 600 km domain (ne 80), SICE | 4 | 1 h | 132 | 52 | 1600 elements per GPU fits |
| 1.25 km on a 600 km domain (ne 160), SICE | 16 | 1 h | 132 | 112 | 1600 elements per GPU fits |
| 312 m, SICE, 3D turbulence on | 16 | - | - | - | out of GPU memory in RRTMGP init: needs >= 32 GPUs |

**GPU memory (16 x A100 40 GB, 625 m config, 3D turbulence on, 128 levels).**
Peak `nvidia-smi` memory on one node, with equal elements on every rank:

| elements/GPU | domain at 625 m | peak GB | result | stepping s per model hour |
|---|---|---|---|---|
| 1,600 | 300 km (ne 160) | 25.6 | ok | 220 |
| 1,936 | 330 km (ne 176) | 28.5 | ok | |
| 2,304 | 360 km (ne 192) | 32.1 | ok, 78 % | |
| 2,500 | 375 km (ne 200) | 33.7 | ok, 82 % | 337 |
| 2,916 | 405 km (ne 216) | 37.6 | ok but 92 %, too tight | |
| 3,364 | 435 km (ne 232) | - | out of memory | |
| 3,844 | 465 km (ne 248) | - | out of memory | |

Memory is ~11 GB fixed plus ~9 MB per element. Stay at or below **~2,300
elements per GPU** for comfortable headroom (2,500 works). The cost per element
is the same between 1,600 and 2,500 per GPU, so packing denser cuts node count
without changing node-hours. At ne <= 192 per 16 GPUs, the largest domain is
576 x dx: 360 km at 625 m, 180 km at 312 m, 90 km at 156 m.

**Initialization bottleneck.** DP perturbs the initial `T_mid` below 900 hPa.
`scream::impl::perturb` (`components/eamxx/src/share/field/utils/perturb.cpp`)
does that one (column, level) at a time, with two subfield allocations and two
device kernels each. That costs ~9 min of init at 1024 elements per GPU. A fast
path that applies the same random draws on the host in one pass gives
bit-identical `T_mid` (checked at 40 km) and cuts init from 520 s to 88 s at
625 m. The patch is on the local E3SM branch `mahf708/eamxx/fast-col-perturb`
and is not upstream yet. Without it, budget ~9 extra minutes of init per run at
1024 elements per GPU.

## Open questions

- Is 6 h long enough? LWP adjustments to Nd develop over many hours. A 12 h
  RF02 forcing exists (`DYCOMSrf02_12hr_PMCnBLH_4scam.nc` in inputdata) if the
  6 h runs are still drifting.
- Is one realization per cell enough? The DP runs perturb T_mid with a fixed
  seed. The sub-km Nd-LWP signal may need 2-3 seeds
  (`generate_perturbation_random_seed=true`) to separate it from noise.
- At 40 and 20 km there are only 100 physics columns, so the column statistics
  are thin. A larger domain is cheap at that resolution if it matters.
