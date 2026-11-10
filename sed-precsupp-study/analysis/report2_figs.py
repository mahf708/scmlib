#!/usr/bin/env python3
"""
Extra figures for the consolidated report (12 h set, 40 km - 312 m).
  report2_figs.py OUTDIR RUNROOT      (reads OUTDIR/summary_h10-12.csv)
H1  Nd response with all resolutions on shared axes (sed x1)
H2  resolution dependence at fixed Nd (sed x1)
H3  LWP maps at hour 12 (sed x1, suppression on), Nd x resolution
"""
import glob
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import netCDF4

out, root = sys.argv[1], sys.argv[2]
df = pd.read_csv(f"{out}/summary_h10-12.csv")
df = df[df.turb3d == "off"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
ALLRES = ["40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m", "312m"]
RESC = dict(zip(ALLRES, ["#eda100", "#e87ba4", "#6250d6", "#1baf7a", "#2a78d6", "#e34948", "#008300", "#0b0b0b"]))
LAB = dict(zip(ALLRES, ["40 km", "20 km", "10 km", "5 km", "2.5 km", "1.25 km", "625 m", "312 m"]))
RES = [r for r in ALLRES if r in set(df.res)]
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "legend.frameon": False,
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2})


def ndaxis(ax):
    ax.set_xscale("log")
    ax.set_xticks([20, 50, 100, 200, 500, 1000])
    ax.xaxis.set_major_formatter(mt.ScalarFormatter())
    ax.xaxis.set_minor_locator(mt.NullLocator())


# ---- H1 ----
vv = [("LWP", "LWP (g m$^{-2}$)"), ("cloud_cover", "cloud cover"), ("we_mm_s", "$w_e$ (mm s$^{-1}$)"),
      ("LWP_sd_online", "LWP spatial SD (g m$^{-2}$)")]
fig, axs = plt.subplots(2, 4, figsize=(15, 6.6), sharex=True)
for i, ps in enumerate(("on", "off")):
    for j, (v, vl) in enumerate(vv):
        ax = axs[i, j]
        for r in RES:
            d = df[(df.res == r) & (df.sed == 1) & (df.precsupp == ps)].sort_values("Nd_incloud")
            ax.plot(d.Nd_incloud, d[v], "-o", ms=3.5, lw=1.6, color=RESC[r],
                    zorder=3 if r in ("625m", "312m") else 2)
        ndaxis(ax)
        ax.set_title(f"{vl}, suppression {ps}", fontsize=9.5)
        if i == 1:
            ax.set_xlabel("in-cloud Nd (cm$^{-3}$)")
h = [Line2D([], [], color=RESC[r], lw=2.5, label=LAB[r]) for r in RES]
fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, 1.05))
fig.tight_layout()
fig.savefig(f"{out}/figH1_nd_response_by_res.png", dpi=150, bbox_inches="tight")

# ---- H2 ----
km = df[df.dx_km <= 5]
nds = [n for n in (20, 50, 100, 200, 500, 1000) if n in set(km[km.res == RES[-1]].Nd_target)]
NDC = dict(zip([20, 50, 100, 200, 500, 1000], ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]))
dxs = sorted(km.dx_km.unique(), reverse=True)
fig, axs = plt.subplots(1, 4, figsize=(15, 3.4))
for ax, (v, vl) in zip(axs, vv):
    for nd in nds:
        for ps, ls, mk in (("on", "-", "o"), ("off", (0, (4, 2)), "s")):
            d = km[(km.sed == 1) & (km.Nd_target == nd) & (km.precsupp == ps)].sort_values("dx_km", ascending=False)
            ax.plot(d.dx_km, d[v], ls=ls, marker=mk, ms=4, lw=1.5, color=NDC[nd],
                    mfc=NDC[nd] if ps == "on" else "white")
    ax.set_xscale("log"); ax.invert_xaxis()
    ax.set_xticks(dxs); ax.set_xticklabels([f"{x:g}" for x in dxs])
    ax.xaxis.set_minor_locator(mt.NullLocator())
    ax.set_xlabel("Δx (km)"); ax.set_title(vl, fontsize=9.5)
h = [Line2D([], [], color=NDC[n], lw=2.5, label=f"Nd {n}") for n in nds]
h += [Line2D([], [], color=INK2, marker="o", label="suppression on"),
      Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, 1.1))
fig.tight_layout()
fig.savefig(f"{out}/figH2_convergence.png", dpi=150, bbox_inches="tight")

# ---- H3 ----
CMAP = mcolors.LinearSegmentedColormap.from_list(
    "lwp", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
MR = [r for r in ("2p5km", "1p25km", "625m", "312m") if r in RES]
MN = [n for n in (20, 200, 1000) if n in nds] or [n for n in (20, 100, 500) if n in nds]


def lastmap(case):
    fl = sorted(glob.glob(f"{root}/{case}/run/{case}.aci2d.INSTANT.*.nc"))
    with netCDF4.Dataset(fl[-1]) as d:
        x, y = d["lon"][:] / 1e3, d["lat"][:] / 1e3
        lwp = d["LiqWaterPath"][-1, :] * 1e3
    xs, ys = np.unique(x), np.unique(y)
    img = np.full((ys.size, xs.size), np.nan)
    img[np.searchsorted(ys, y), np.searchsorted(xs, x)] = lwp
    return xs, ys, img


fig, axs = plt.subplots(len(MN), len(MR), figsize=(3.1 * len(MR), 3.15 * len(MN)), constrained_layout=True,
                        squeeze=False)
for i, nd in enumerate(MN):
    for j, r in enumerate(MR):
        ax = axs[i, j]
        xs, ys, img = lastmap(f"sedps_{r}_nd{nd}_sed1_pson")
        im = ax.imshow(img, origin="lower", extent=(xs[0], xs[-1], ys[0], ys[-1]), cmap=CMAP,
                       vmin=0, vmax=300, interpolation="nearest")
        ax.set_title(f"{LAB[r]}, Nd {nd}: {np.nanmean(img):.0f} g/m², cover {np.nanmean(img > 10):.2f}", fontsize=8)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
fig.colorbar(im, ax=axs, shrink=0.6, label="LWP at hour 12 (g m$^{-2}$)")
fig.savefig(f"{out}/figH3_lwp_maps.png", dpi=130)
print("ok")
