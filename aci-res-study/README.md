# ACI x resolution x 3D-turbulence study (DYCOMS-II RF02, DP-EAMxx)

How does the Nd-LWP relationship of drizzling stratocumulus change as DP-EAMxx
goes from 40 km to ~150 m, and does the new SHOC-HOMME 3D turbulence change
the sub-km answer?

| factor | levels |
|---|---|
| Nd (in-cloud, #/cm3) | 20, 50, 100, 200 |
| dx (dynamics) | 40, 20, 10, 5, 2.5, 1.25 km, 625, 312.5, 156.25 m |
| 3D turbulence | off everywhere; on *and* off at 625, 312.5, 156.25 m |
| domain | 240 km x 240 km, fixed |

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

## Domain and the integer-element constraint

Resolution follows the scmlib convention `dx = L / (3 * num_ne_x)` (unique
dynamics GLL points). `num_ne_x` must be an integer, and at L = 200 km,
dx = 40 km would need `num_ne_x = 1.67`. 240 km is the smallest domain that hits
40 km exactly (`num_ne_x = 2`) and lets every finer level be an exact halving
(`num_ne_x` = 2, 4, ..., 512).

At 40 km that is 6 dynamics points but only **4 physics (pg2) columns** per
direction. The physics grid is 1.5x coarser than the label:
`dx_phys = L / (2 * num_ne_x)`. SHOC's horizontal length scale (and so the 3D
turbulence diffusivities) uses the physics-grid spacing. If you want >= 5 physics
columns per direction at 40 km, use L = 360 km (`num_ne_x` = 3 ... 768). That
costs 2.25x more at every level.

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

| res | num_ne_x | dx_phys (km) | physics cols | model_dtime (s) | dyn_ratio | se_tstep (s) | se_tstep per km dx | nu_top (m2/s) | 6 h phys steps | rel. cost* | ranks (pm-gpu) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40km   | 2   | 60    | 16        | 100 | 12 | 8.333 | 0.21 | 1.2e5 | 216   | 4e-5   | 4 (1 node) |
| 20km   | 4   | 30    | 64        | 100 | 12 | 8.333 | 0.42 | 6e4   | 216   | 2e-4   | 4 (1 node) |
| 10km   | 8   | 15    | 256       | 100 | 12 | 8.333 | 0.83 | 3e4   | 216   | 6e-4   | 4 (1 node) |
| 5km    | 16  | 7.5   | 1,024     | 100 | 12 | 8.333 | 1.67 | 1.5e4 | 216   | 0.003  | 4 (1 node) |
| 2p5km  | 32  | 3.75  | 4,096     | 75  | 12 | 6.25  | 2.50 | 7500  | 288   | 0.014  | 8 (2 nodes) |
| 1p25km | 64  | 1.875 | 16,384    | 60  | 24 | 2.5   | 2.00 | 1667  | 360   | 0.14   | 16 (4 nodes) |
| 625m   | 128 | 0.94  | 65,536    | 30  | 24 | 1.25  | 2.00 | 833   | 720   | 1.1    | 32 (8 nodes) |
| 312m   | 256 | 0.47  | 262,144   | 15  | 24 | 0.625 | 2.00 | 417   | 1,440 | 8.7    | 64 (16 nodes) |
| 156m   | 512 | 0.23  | 1,048,576 | 6   | 24 | 0.25  | 1.60 | 208   | 3,600 | 87     | 256 (64 nodes) |

\* elements x dynamics steps, relative to the `inverted-v-res-study` 100 m run
(ne 50, dt 5 s, ratio 24, 6 h). Walltimes in the script are rough scalings of that.
Correct them after the first 625 m run.

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

## Where the settings are

All of these are in `run_dpxx_scream_DYCOMSrf02_aci.csh`. Each block lists the
master defaults commented out, so you can vary them without looking anything
up.

| block | line | namelist group | knobs |
|---|---|---|---|
| resolution table | ~103 | `ctl_nl` | `se_ne_x/y`, `se_lx/ly`, `se_tstep`, `nu_top`, `nu` |
| Nd -> SPA factor table | ~146 | `p3` | per-Nd `spa_ccn_to_nc_factor` |
| **SPA settings** | ~309 | `p3` (spa process supplies `nccn`) | `do_prescribed_ccn`, `spa_ccn_to_nc_factor`, `spa_ccn_to_nc_exponent` (`spa_data_file` under `spa`) |
| **P3 settings** | ~318 | `p3` | `autoconversion_*`, `accretion_*`, `set_cld_frac_{l,r}_to_one`, `extra_p3_diags` |
| **SHOC settings** | ~334 | `shoc` | `length_fac`, `c_diag_3rd_mom`, `lambda_*`, `coeff_kh/km`, `shoc_1p5tke`, `extra_shoc_diags` |
| **3D turbulence** | ~347 | `ctl_nl` (+ `shoc`) | `ctl_nl::do_3d_turbulence`, `coeff_kh_horiz`, `coeff_km_horiz`, `ctl_nl::horiz_turb_subcycle{,_q}` |

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

## Open questions

- Is 6 h long enough? LWP adjustments to Nd develop over many hours. A 12 h
  RF02 forcing exists (`DYCOMSrf02_12hr_PMCnBLH_4scam.nc` in inputdata) if the
  6 h runs are still drifting.
- Is one realization per cell enough? The DP runs perturb T_mid with a fixed
  seed. The sub-km Nd-LWP signal may need 2-3 seeds
  (`generate_perturbation_random_seed=true`) to separate it from noise.
- At 40 km there are only 16 physics columns, so the domain-mean spread is
  small by construction. Use L = 360 km if that matters.
