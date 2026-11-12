## Time series of LWP, in-cloud Nd, cloud fraction, inversion height and cloud-top/base height, coloured by target Nd and
## faceted by precipitation suppression x sedimentation factor, one page per
## grid spacing (12 h runs, 3D turbulence off).  As requested by J. Muelmenstaedt:
##   ggplot(aes(x = time, col = target_cdnc)) + geom_line() + facet_grid(precsupp ~ sed_factor)
## Usage: Rscript timeseries_facets.R [timeseries_15min.csv] [outdir]
suppressPackageStartupMessages({ library(dplyr); library(tidyr); library(ggplot2) })
args <- commandArgs(TRUE)
csv <- if (length(args) >= 1) args[1] else "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/analysis_report5/timeseries_15min.csv"
out <- if (length(args) >= 2) args[2] else "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/analysis_report5/ts_ggplot"
dir.create(out, showWarnings = FALSE, recursive = TRUE)

res.levels <- c("40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m", "312m")
res.labels <- c("40 km", "20 km", "10 km", "5 km", "2.5 km", "1.25 km", "625 m", "312 m")
heights.csv <- file.path(dirname(csv), "heights", "heights_15min.csv")
df <- read.csv(csv)
if (file.exists(heights.csv)) {   # cloud-top/base heights from ts_heights.py
    hgt <- read.csv(heights.csv)
    df <- left_join(df, hgt, by = c("case", "time_h"))
}
df <- df %>%
    filter(turb3d == "off") %>%
    mutate(res = factor(res, res.levels, res.labels),
           target_cdnc = factor(Nd_target),
           precsupp = factor(paste("precip suppression", precip_suppression),
                             paste("precip suppression", c("on", "off"))),
           sed_factor = factor(paste0("sed x", sed_factor), c("sed x0.5", "sed x1", "sed x2")))
long <- df %>%
    transmute(res, time = time_h, target_cdnc, precsupp, sed_factor,
              `LWP (g m-2)` = LWP_inst_gm2,
              `in-cloud Nd (cm-3)` = Nd_layer_cm3,
              `cloud fraction (LWP > 10 g m-2)` = cloud_cover,
              `inversion height (m)` = zi_m,
              `cloud-top height (m)` = if ("z_top_aerocom_m" %in% names(df)) z_top_aerocom_m else NA_real_,
              `cloud-base height (m)` = if ("z_base_qc_m" %in% names(df)) z_base_qc_m else NA_real_) %>%
    pivot_longer(-c(res, time, target_cdnc, precsupp, sed_factor), names_to = "var", values_to = "val") %>%
    filter(is.finite(val))
cdnc.cols <- c("20" = "#fde725", "50" = "#7ad151", "100" = "#22a884", "200" = "#2a788e",
               "500" = "#414487", "1000" = "#440154")      # viridis, light = low Nd
theme_set(theme_bw(base_size = 10) + theme(panel.grid.minor = element_blank(),
                                           strip.background = element_rect(fill = "grey95"),
                                           legend.position = "bottom"))

pdf(file.path(out, "timeseries_by_res.pdf"), width = 9, height = 6.5)
for (v in unique(long$var)) {
    for (r in levels(droplevels(long$res))) {
        d <- filter(long, var == v, res == r)
        p <- ggplot(d, aes(x = time, y = val, col = target_cdnc)) +
            geom_line(linewidth = 0.6) +
            scale_colour_manual("target Nd (cm-3)", values = cdnc.cols) +
            scale_x_continuous(breaks = seq(0, 12, 2)) +
            facet_grid(precsupp ~ sed_factor) +
            labs(x = "time (h)", y = v, title = paste0(v, ", dx = ", r))
        if (grepl("Nd", v)) p <- p + scale_y_log10()
        print(p)
        ggsave(file.path(out, sprintf("ts_%s_%s.png", gsub("[^A-Za-z]+", "", sub(" .*", "", v)), gsub(" |\\.", "", r))),
               p, width = 9, height = 6.5, dpi = 120)
    }
}
dev.off()

## one overview page per variable with all resolutions (facet rows = res, sed x1 only)
for (v in unique(long$var)) {
    d <- filter(long, var == v, sed_factor == "sed x1")
    p <- ggplot(d, aes(x = time, y = val, col = target_cdnc)) + geom_line(linewidth = 0.5) +
        scale_colour_manual("target Nd (cm-3)", values = cdnc.cols) +
        scale_x_continuous(breaks = seq(0, 12, 4)) +
        facet_grid(precsupp ~ res) + labs(x = "time (h)", y = v, title = paste0(v, ", sed x1, all grid spacings"))
    if (grepl("Nd", v)) p <- p + scale_y_log10()
    ggsave(file.path(out, sprintf("overview_%s_sed1.png", gsub("[^A-Za-z]+", "", sub(" .*", "", v)))), p,
           width = 15, height = 5, dpi = 120)
}
cat("wrote", out, "\n")
