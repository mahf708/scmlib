## Loaders for the DP-EAMxx DYCOMS-II RF02 sed x precip-suppression study.
##
##   source("/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/R/sedps.R")
##   runs <- sedps_runs()                      # one row per finished run
##   df.2d <- sedps_ddply(runs, load_sedps_2d)  # column-level, all runs
##
## Needs ncdf4, plyr, dplyr, magrittr.  Written in the plyr/dplyr/magrittr
## style of mltools; plotutils is not required.
##
## Case naming: sedps_<res>_nd<Nd>_sed<0p5|1|2>_ps<on|off>, under
## /pscratch/sd/m/mahf708/dp_screamxx_sedps/<case>/run/.  Streams (one file each):
##   <case>.horiz_avg.AVERAGE.nmins_x15.*   domain-mean profiles + scalars, 15-min means
##   <case>.aci2d.INSTANT.nmins_x15.*       per-column 2D fields, 15-min snapshots
##   <case>.aerocom.INSTANT.nmins_x15.*     per-column AeroCom cloud-top fields + LWP variance
##   <case>.aci3d.INSTANT.nhours_x2.*       trimmed 3D state, 2-hourly
## The AeroCom fields (cf_top*, T_top, p_top, reff_top_liq, cdnc_top_liq) are
## weighted SUMS over levels (E3SM PR #9017): divide by the matching cloud-top
## fraction to get the value at cloud top.  Values > 1e30 are fill (no cloud).

suppressPackageStartupMessages({
    library(magrittr)
    library(plyr)
    library(dplyr)
})

sedps.root <- "/pscratch/sd/m/mahf708/dp_screamxx_sedps"
sedps.analysis <- file.path(sedps.root, "analysis")

sedps.res.km <- c("40km" = 40, "20km" = 20, "10km" = 10, "5km" = 5, "2p5km" = 2.5,
                  "1p25km" = 1.25, "625m" = 0.625, "312m" = 0.3125, "156m" = 0.15625)
sedps.sed <- c("0p5" = 0.5, "1" = 1, "2" = 2)

#' Finished runs: res, dx.km, nd (target, cm-3), sed (factor), precsupp (on/off), case, dir
sedps_runs <- function(root = sedps.root) {
    dirs <- Sys.glob(file.path(root, "sedps_*"))
    m <- regmatches(basename(dirs),
                    regexec("^sedps_(.+?)_nd([0-9]+)_sed(0p5|1|2)_ps(on|off)$", basename(dirs)))
    ok <- lengths(m) == 5
    runs <- data.frame(res = sapply(m[ok], `[`, 2),
                       nd = as.integer(sapply(m[ok], `[`, 3)),
                       sed = sedps.sed[sapply(m[ok], `[`, 4)],
                       precsupp = sapply(m[ok], `[`, 5),
                       case = basename(dirs[ok]),
                       dir = dirs[ok],
                       stringsAsFactors = FALSE, row.names = NULL) %>%
        mutate(dx.km = unname(sedps.res.km[res]))
    ## keep only runs with a complete 6 h aerocom stream
    runs[sapply(runs$dir, function(d) {
        f <- sedps_file(d, "aerocom.INSTANT")
        if (is.na(f)) return(FALSE)
        nc <- ncdf4::nc_open(f); on.exit(ncdf4::nc_close(nc))
        nc$dim$time$len >= 25
    }), ] %>% arrange(desc(dx.km), nd, sed, desc(precsupp))
}

#' Path of one output stream of a run (the file starting at t0, not the rhist)
sedps_file <- function(dir, stream) {
    f <- Sys.glob(file.path(dir, "run", sprintf("%s.%s.*-00000.nc", basename(dir), stream)))
    if (length(f)) f[1] else NA_character_
}

#' Variables of an open nc into a long-by-dimension, wide-by-variable data.frame
#' (like plotutils::nc.to.df(nc, vars)); time becomes hours since the first record.
nc_df <- function(nc, vars) {
    dims <- sapply(nc$var[[vars[1]]]$dim, function(d) d$name)
    vals <- lapply(nc$var[[vars[1]]]$dim, function(d) if (d$name == "time") d$vals else seq_len(d$len))
    names(vals) <- dims
    if ("time" %in% dims) vals$time <- (vals$time - vals$time[1]) * 24  # days -> hours
    df <- expand.grid(vals, KEEP.OUT.ATTRS = FALSE)
    for (v in vars) {
        x <- as.vector(ncdf4::ncvar_get(nc, v, collapse_degen = FALSE))
        x[!is.na(x) & abs(x) > 1e30] <- NA
        df[[v]] <- x
    }
    df
}

#' Per-column 2D fields every 15 min (LWP etc. in g/m2, rain in mm/day), with
#' the AeroCom cloud-top fields turned into cloud-top values:
#'   cf.top.liq, cdnc.top (cm-3, in cloud), reff.top (um), T.top (K)
load_sedps_2d <- function(dir) {
    nc <- ncdf4::nc_open(sedps_file(dir, "aci2d.INSTANT")); on.exit(ncdf4::nc_close(nc))
    df <- nc_df(nc, c("LiqWaterPath", "LiqNumberPath", "RainWaterPath", "pbl_height",
                      "precip_liq_surf_mass_flux", "LongwaveCloudForcing"))
    na <- ncdf4::nc_open(sedps_file(dir, "aerocom.INSTANT"))
    da <- nc_df(na, c("cf_top", "cf_top_liq", "T_top", "reff_top_liq", "cdnc_top_liq"))
    ncdf4::nc_close(na)
    df %>%
        left_join(da, by = c("ncol", "time")) %>%
        transmute(time, ncol,
                  lwp = LiqWaterPath * 1e3,
                  lnp = LiqNumberPath,
                  rwp = RainWaterPath * 1e3,
                  prec = precip_liq_surf_mass_flux * 86400e3,
                  zpbl = pbl_height,
                  lwcf = LongwaveCloudForcing,
                  cf.top = cf_top,
                  cf.top.liq = cf_top_liq,
                  cdnc.top = ifelse(cf_top_liq > 0, cdnc_top_liq / cf_top_liq / 1e6, NA),
                  reff.top = ifelse(cf_top_liq > 0, reff_top_liq / cf_top_liq, NA),
                  T.top = ifelse(cf_top > 0, T_top / cf_top, NA))
}

#' Domain-mean scalars every 15 min: online LWP mean and spatial SD (g/m2)
load_sedps_lwp_sd <- function(dir) {
    nc <- ncdf4::nc_open(sedps_file(dir, "aerocom.INSTANT")); on.exit(ncdf4::nc_close(nc))
    nc_df(nc, c("lwp_mean", "lwp_var")) %>%
        transmute(time, lwp.mean = lwp_mean * 1e3, lwp.sd = sqrt(pmax(lwp_var, 0)) * 1e3)
}

#' Domain-mean profiles (15-min means; time = end of interval, hours).
#' vars: names without the _horiz_avg suffix, e.g. c("T_mid", "qc", "nc", "cldfrac_liq")
load_sedps_profiles <- function(dir, vars = c("z_mid", "p_mid", "T_mid", "qv", "qc", "nc",
                                              "cldfrac_liq", "LiqPotentialTemperature")) {
    nc <- ncdf4::nc_open(sedps_file(dir, "horiz_avg.AVERAGE")); on.exit(ncdf4::nc_close(nc))
    df <- nc_df(nc, paste0(vars, "_horiz_avg"))
    names(df) <- sub("_horiz_avg$", "", names(df))
    df %>% mutate(time = time + 0.25)
}

#' Apply fun(dir) to every run and bind the results, tagged with the run factors.
#' Use .parallel = TRUE after doParallel::registerDoParallel(n).
sedps_ddply <- function(runs, fun, ..., .parallel = FALSE) {
    plyr::ddply(runs, ~ case, function(r) {
        cbind(r[rep(1, 1), c("res", "dx.km", "nd", "sed", "precsupp", "case")], fun(r$dir, ...),
              row.names = NULL)
    }, .parallel = .parallel)
}

#' Hours 4-6 summary and 15-min time series already computed in Python
#' (one row per run / per run and time, run factors as columns)
read_sedps_summary <- function() read.csv(file.path(sedps.analysis, "summary_h4-6.csv"))
read_sedps_timeseries <- function() read.csv(file.path(sedps.analysis, "timeseries_15min.csv"))
