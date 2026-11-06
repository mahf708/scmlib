# Cloud sedimentation x precip suppression x Nd x resolution (DYCOMS-II RF02, DP-EAMxx)

This study extends `aci-res-study/`. It keeps the same case, domains, time steps and SPA Nd
factors, and fixes 3D turbulence off. It adds two P3 factors. One-page plan: `plan.pdf`
(source in `plan/`). EAMxx only.

| factor | levels |
|---|---|
| dx | 40, 20, 10, 5, 2.5, 1.25 km (625 m and below on hold) |
| Nd target (cm-3) | 20, 50, 100, 200 |
| `p3::cloud_sedimentation_factor` | 0.5, 1, 2 |
| precip suppression | on (KK2000 default); off (`autoconversion_nc_exponent=0`, `autoconversion_prefactor=0.8119`) |

That is 6 x 4 x 3 x 2 = 144 runs, each 6 h.

**Code.** E3SM branch `mahf708/eamxx/p3-cloud-sed-factor`. It has three parts:
- E3SM PR #9017 (the `aerocom(..)` expression operator);
- the `perturb` speed-up `66951b3838`;
- a new P3 runtime option, `cloud_sedimentation_factor` (default 1). It scales the mass- and number-weighted cloud
  droplet fall speeds in `cloud_sedimentation`, the counterpart of MG2's `cld_sed`, which scales `acn`.

**Precip suppression off.** P3 autoconversion is `1350 qc^2.47 (Nd/cm-3)^-1.79`. With
the exponent at 0, the prefactor `1350 * 63^-1.79 = 0.8119` gives the default rate at
Nd = 63 cm-3, the geometric mean of the sweep. (1.04 would match at 55 cm-3, the default SPA Nd here.)

## Files

| file | what |
|---|---|
| `run_dpxx_scream_DYCOMSrf02_sedps.csh <res> <nd> <sed> <ps>` | create one case. It builds unless `SEDPS_EXEROOT` is set, and submits only if `SEDPS_SUBMIT` is set |
| `create_cases.sh [res ...]` | create the matrix on one build. Writes `$PSCRATCH/dp_screamxx_sedps/lists/<res>.txt` |
| `run_packed.sh <list>` | inside an allocation, run the listed cases (`case.submit --no-batch`), packed onto its nodes. Finished cases are skipped |
| `yaml_file_example/scream_aerocom_15min.yaml` | AeroCom cloud-top fields (#9017) and the online LWP spatial variance |

The remaining yaml files are the ACI-study streams.

```bash
# e.g. 8 debug nodes for the 40 and 20 km cases
cat $PSCRATCH/dp_screamxx_sedps/lists/{40km,20km}.txt > l.txt
sbatch -A e3sm_g -C gpu -q debug -N 8 --gpus-per-node=4 -t 30 run_packed.sh l.txt
```
