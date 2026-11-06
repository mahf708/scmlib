# R tools for the sed x precip-suppression study

`sedps.R` holds the loaders. They are written in the plyr/dplyr/magrittr style of `mltools` and need only
`ncdf4`, `plyr`, `dplyr` and `magrittr`.

```r
source("/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/R/sedps.R")
runs  <- sedps_runs()                        # res, dx.km, nd, sed, precsupp, case, dir (finished runs)
df.2d <- sedps_ddply(runs, load_sedps_2d)    # per column, 15-min: lwp, lnp, rwp, prec, zpbl, cdnc.top, reff.top, ...
df.sd <- sedps_ddply(runs, load_sedps_lwp_sd)        # domain LWP mean and spatial SD (online), 15-min
df.pr <- sedps_ddply(runs, load_sedps_profiles)      # domain-mean profiles, 15-min means
df.sum <- read_sedps_summary()               # hour 4-6 summary (one row per run)
df.ts  <- read_sedps_timeseries()            # 15-min time series (one row per run x time)
```

`sedps_analysis.R` is a knitr-chunked example (`## @knitr` labels). It draws the Nd response, the time series and
the column-level Nd-LWP joint histograms at km scale with ggplot2, and saves the column data frame as RDS:

```bash
Rscript /pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/R/sedps_analysis.R  /path/to/outdir
```

Notes:

- `time` is in hours since the start. For the `horiz_avg` stream, it is the end of each 15-min averaging interval.
- The AeroCom outputs are weighted sums over levels. The loaders divide by the cloud-top fraction, so `cdnc.top`
  (in-cloud, cm-3), `reff.top` (um) and `T.top` (K) are the values at cloud top.
- Tested with R 4.4 (conda-forge) on a Perlmutter login node. A ready environment is at
  `/pscratch/sd/m/mahf708/r_env` (`/pscratch/sd/m/mahf708/r_env/bin/Rscript`).
