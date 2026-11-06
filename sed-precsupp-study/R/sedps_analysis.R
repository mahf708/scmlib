## Example analysis for the sed x precip-suppression study, knitr-chunked like
## mltools/vignettes.  Run on Perlmutter (login node is fine):
##   Rscript /pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/R/sedps_analysis.R [outdir]
## Needs ncdf4, plyr, dplyr, magrittr, tidyr, ggplot2.

## @knitr sedps-setup
source(file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))),
                 "sedps.R"))
suppressPackageStartupMessages({ library(tidyr); library(ggplot2) })
args <- commandArgs(TRUE)
outdir <- if (length(args)) args[1] else file.path(sedps.analysis, "R")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

res.levels <- c("40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m")
res.labels <- c("40 km", "20 km", "10 km", "5 km", "2.5 km", "1.25 km", "625 m")
sed.colors <- c("0.5" = "#86b6ef", "1" = "#2a78d6", "2" = "#104281")
theme_set(theme_bw(base_size = 9) + theme(panel.grid.minor = element_blank(),
                                          strip.background = element_rect(fill = "grey95")))
scales_sedps <- list(scale_color_manual("cloud sed factor", values = sed.colors),
                     scale_linetype_manual("precip suppression", values = c(on = "solid", off = "22")),
                     scale_shape_manual("precip suppression", values = c(on = 16, off = 0)))

## @knitr sedps-summary
df.sum <- read_sedps_summary() %>%
    mutate(res = factor(res, res.levels, res.labels), sed = factor(sed), precsupp = factor(precsupp, c("on", "off")))

df.sum %>%
    select(res, Nd_incloud, sed, precsupp, LWP, LWP_sd_online, cloud_cover, we_mm_s, precip, reff_top_um) %>%
    gather(var, val, -res, -Nd_incloud, -sed, -precsupp) %>%
    mutate(var = factor(var, c("LWP", "LWP_sd_online", "cloud_cover", "we_mm_s", "precip", "reff_top_um"),
                        c("LWP~(g~m^-2)", "sigma[LWP]~(g~m^-2)", "cloud~cover", "w[e]~(mm~s^-1)",
                          "precip~(mm~d^-1)", "r[eff*','*top]~(mu*m)"))) %>%
    ggplot(aes(Nd_incloud, val, col = sed, lty = precsupp, shape = precsupp)) +
    geom_line() + geom_point(size = 1.5) +
    scale_x_log10(breaks = c(20, 50, 100, 200)) + scales_sedps +
    facet_grid(var ~ res, scales = "free_y", labeller = labeller(var = label_parsed)) +
    labs(x = expression(paste("in-cloud ", N[d], " (cm"^-3, ")")), y = NULL,
         title = "DP-EAMxx RF02, hours 4-6 mean")
ggsave(file.path(outdir, "sedps_response.pdf"), width = 11, height = 9)

## @knitr sedps-timeseries
df.ts <- read_sedps_timeseries() %>%
    mutate(res = factor(res, res.levels, res.labels), sed = factor(sed_factor),
           precsupp = factor(precip_suppression, c("on", "off")))
df.ts %>%
    filter(Nd_target %in% c(20, 200)) %>%
    select(res, Nd_target, sed, precsupp, time_h, LWP_inst_gm2, LWP_sd_gm2, Nd_layer_cm3) %>%
    gather(var, val, LWP_inst_gm2, LWP_sd_gm2, Nd_layer_cm3) %>%
    ggplot(aes(time_h, val, col = sed, lty = precsupp)) +
    geom_line() + scales_sedps[1:2] +
    facet_grid(var ~ res + Nd_target, scales = "free_y") +
    labs(x = "hour", y = NULL)
ggsave(file.path(outdir, "sedps_timeseries.pdf"), width = 14, height = 6)

## @knitr sedps-columns
## Column-level Nd-LWP joint distribution at hours 4-6 (km-scale runs only;
## at >= 10 km all columns are nearly identical).  cdnc.top is the in-cloud
## liquid cloud-top CDNC; require a mostly-liquid-capped, cloudy (LWP > 10 g/m2) column.
runs <- sedps_runs() %>% filter(dx.km <= 2.5, nd %in% c(20, 200), sed == 1)
df.col <- sedps_ddply(runs, load_sedps_2d) %>%
    filter(time > 4, cf.top.liq > 0.5, lwp > 10) %>%
    mutate(res = factor(res, res.levels, res.labels), precsupp = factor(precsupp, c("on", "off")))
saveRDS(df.col, file.path(outdir, "sedps_columns_h4-6_sed1.rds"))
df.col %>%
    ggplot(aes(cdnc.top, lwp)) +
    geom_bin2d(bins = 40) +
    scale_x_log10(breaks = c(10, 20, 50, 100, 200, 400)) +
    scale_y_log10(breaks = c(10, 20, 50, 100, 200, 500)) +
    scale_fill_viridis_c(trans = "log10") +
    facet_grid(precsupp ~ res + nd, labeller = label_both) +
    labs(x = expression(paste("cloud-top ", N[d], " (cm"^-3, ")")), y = expression(LWP~(g~m^-2)))
ggsave(file.path(outdir, "sedps_columns.pdf"), width = 10, height = 5)
cat("wrote", outdir, "\n")
