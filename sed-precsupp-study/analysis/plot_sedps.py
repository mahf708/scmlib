#!/usr/bin/env python3
"""
Figures for the sed x precip-suppression study.
  plot_sedps.py OUTDIR    (reads summary_h4-6.csv and timeseries_15min.csv)

Encoding (all figures): sed factor = one blue ramp, light (x0.5) -> dark (x2);
precip suppression on = solid line + filled circle, off = dashed + open square.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
from matplotlib.lines import Line2D

out = sys.argv[1]
df = pd.read_csv(f"{out}/summary_h4-6.csv")
ts = pd.read_csv(f"{out}/timeseries_15min.csv")

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SEDC = {0.5: "#86b6ef", 1.0: "#2a78d6", 2.0: "#104281"}       # blue ramp 250/450/650
PS = {"on": dict(ls="-", marker="o", mfc=None), "off": dict(ls=(0, (4, 2)), marker="s", mfc="white")}
RES = [r for r in ["40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m"] if r in set(df.res)]
LAB = {"40km": "40 km", "20km": "20 km", "10km": "10 km", "5km": "5 km", "2p5km": "2.5 km",
       "1p25km": "1.25 km", "625m": "625 m"}
DOM = {"40km": 600, "20km": 300}

plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.titlesize": 10, "axes.titleweight": "bold", "legend.frameon": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})


def line(ax, x, y, sed, ps, **kw):
    st = PS[ps]
    c = SEDC[sed]
    ax.plot(x, y, color=c, lw=1.6, ls=st["ls"], marker=st["marker"], ms=4.5,
            mfc=c if st["mfc"] is None else st["mfc"], mec=c, mew=1.2, **kw)


def legend(fig, y=1.0):
    h = [Line2D([], [], color=SEDC[s], lw=2.5, label=f"cloud sed ×{s:g}") for s in (0.5, 1.0, 2.0)]
    h += [Line2D([], [], color=INK2, lw=1.4, marker="o", ms=4.5, label="precip suppression on"),
          Line2D([], [], color=INK2, lw=1.4, ls=(0, (4, 2)), marker="s", mfc="white", ms=4.5,
                 label="precip suppression off (KK Nd-exponent 0)")]
    fig.legend(handles=h, loc="upper center", ncol=5, bbox_to_anchor=(0.5, y), fontsize=9,
               handlelength=2.6, columnspacing=1.6)


def ndaxis(ax):
    ax.set_xscale("log")
    ax.set_xticks([20, 50, 100, 200])
    ax.xaxis.set_major_formatter(mt.ScalarFormatter())
    ax.xaxis.set_minor_locator(mt.NullLocator())
    ax.set_xlim(16, 290)


# ---------- Fig 1: response to Nd, small multiples (rows = quantity, cols = dx) ----------
rows = [("LWP", "LWP\n(g m$^{-2}$)"),
        ("LWP_sd_online", "LWP spatial SD\n(g m$^{-2}$)"),
        ("cloud_cover", "cloud cover\n(LWP > 10 g m$^{-2}$)"),
        ("we_mm_s", "entrainment $w_e$\n(mm s$^{-1}$)"),
        ("precip", "surface precip\n(mm day$^{-1}$)"),
        ("reff_top_um", "liquid cloud-top\n$r_\\mathrm{eff}$ (µm)")]
fig, axs = plt.subplots(len(rows), len(RES), figsize=(2.35 * len(RES) + 0.8, 1.75 * len(rows) + 0.9),
                        sharex=True, sharey="row", squeeze=False)
for j, r in enumerate(RES):
    for i, (v, vl) in enumerate(rows):
        ax = axs[i, j]
        for sed in (0.5, 1.0, 2.0):
            for ps in ("on", "off"):
                d = df[(df.res == r) & (df.sed == sed) & (df.precsupp == ps)].sort_values("Nd_incloud")
                line(ax, d.Nd_incloud, d[v], sed, ps)
        ndaxis(ax)
        if i == 0:
            ax.set_title(f"Δx = {LAB[r]}\n({DOM.get(r, 240)} km domain)", fontsize=9.5)
        if j == 0:
            ax.set_ylabel(vl, fontsize=9)
        if i == len(rows) - 1:
            ax.set_xlabel("in-cloud Nd (cm$^{-3}$)")
axs[2, 0].set_ylim(0.6, 1.02)
legend(fig, 1.0)
fig.suptitle("DP-EAMxx DYCOMS-II RF02: response to droplet number, hours 4–6 mean",
             y=1.035, fontsize=12, fontweight="bold", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.975), h_pad=0.6, w_pad=0.4)
fig.savefig(f"{out}/fig1_response.png", dpi=150, bbox_inches="tight")

# ---------- Fig 2: susceptibility vs resolution ----------
rows_s = []
for (r, sed, ps), g in df.groupby(["res", "sed", "precsupp"]):
    g = g.set_index("Nd_target")
    s = lambda a, b: np.log(g.LWP[b] / g.LWP[a]) / np.log(g.Nd_incloud[b] / g.Nd_incloud[a])
    rows_s.append({"res": r, "dx_km": g.dx_km.iloc[0], "sed": sed, "precsupp": ps,
                   "S_low_20_50": s(20, 50), "S_high_100_200": s(100, 200)})
S = pd.DataFrame(rows_s).sort_values(["dx_km", "precsupp", "sed"], ascending=[False, False, True])
S.round(3).to_csv(f"{out}/susceptibility.csv", index=False)
fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.6), sharey=True)
for ax, col, ttl in zip(axs, ["S_low_20_50", "S_high_100_200"],
                        ["low-Nd branch (Nd 20 → 50)", "high-Nd branch (Nd 100 → 200)"]):
    for sed in (0.5, 1.0, 2.0):
        for ps in ("on", "off"):
            d = S[(S.sed == sed) & (S.precsupp == ps)].sort_values("dx_km", ascending=False)
            line(ax, d.dx_km, d[col], sed, ps)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xticks(sorted(S.dx_km.unique()))
    ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.xaxis.set_minor_locator(mt.NullLocator())
    ax.set_xlabel("Δx (km)")
    ax.set_title(ttl)
axs[0].set_ylabel("$S = d\\ln \\mathrm{LWP} / d\\ln N_d$")
legend(fig, 1.08)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(f"{out}/fig2_susceptibility.png", dpi=150, bbox_inches="tight")

# ---------- Fig 3: time series, coarse vs km-scale, low vs high Nd ----------
cases = [(RES[0], 20), (RES[0], 200), ("2p5km", 20), ("2p5km", 200)]
if "1p25km" in RES:
    cases = [(RES[0], 20), (RES[0], 200), ("1p25km", 20), ("1p25km", 200)]
trows = [("LWP_gm2", "LWP (g m$^{-2}$)"), ("LWP_sd_gm2", "LWP spatial SD\n(g m$^{-2}$)"),
         ("Nd_layer_cm3", "in-cloud Nd\n(cm$^{-3}$)"), ("precip_mmday", "surface precip\n(mm day$^{-1}$)")]
fig, axs = plt.subplots(len(trows), len(cases), figsize=(11, 7.6), sharex=True, sharey="row")
for j, (r, nd) in enumerate(cases):
    for i, (v, vl) in enumerate(trows):
        ax = axs[i, j]
        for sed in (0.5, 1.0, 2.0):
            for ps in ("on", "off"):
                d = ts[(ts.res == r) & (ts.Nd_target == nd) & (ts.sed_factor == sed) &
                       (ts.precip_suppression == ps)].dropna(subset=[v]).sort_values("time_h")
                st = PS[ps]
                ax.plot(d.time_h, d[v], color=SEDC[sed], lw=1.5, ls=st["ls"])
        ax.axvspan(4, 6, color=GRID, alpha=0.5, lw=0, zorder=0)
        ax.set_xticks([0, 2, 4, 6])
        ax.set_xlim(0, 6)
        if i == 0:
            ax.set_title(f"Δx = {LAB[r]}, Nd target {nd}")
        if j == 0:
            ax.set_ylabel(vl, fontsize=9)
        if i == len(trows) - 1:
            ax.set_xlabel("hour")
axs[2, 0].set_yscale("log")
axs[2, 0].set_yticks([20, 50, 100, 200])
axs[2, 0].yaxis.set_major_formatter(mt.ScalarFormatter())
axs[2, 0].yaxis.set_minor_locator(mt.NullLocator())
legend(fig, 1.02)
fig.text(0.99, 0.005, "shaded: hours 4–6 averaging window", ha="right", fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.01, 1, 0.96))
fig.savefig(f"{out}/fig3_timeseries.png", dpi=150, bbox_inches="tight")
print("ok")
