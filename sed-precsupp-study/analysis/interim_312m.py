#!/usr/bin/env python3
"""
Interim 312 m figures: 312 m next to 2.5 km / 1.25 km / 625 m for the runs
312 m has finished.  Usage: interim_312m.py OUT_DIR SUMMARY_12H SUMMARY_312M RUNROOT
"""
import glob
import os
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

out, s12, s312, root = sys.argv[1:5]
df = pd.concat([pd.read_csv(s12), pd.read_csv(s312)])
df = df[(df.turb3d == "off") & df.dx_km.le(2.5)]
done = pd.read_csv(s312)[["Nd_target", "sed", "precsupp"]].drop_duplicates()
df = df.merge(done, on=["Nd_target", "sed", "precsupp"])         # same cells at every dx
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
NDC = {20: "#86b6ef", 50: "#2a78d6", 100: "#0d366b"}
SEDC = {0.5: "#86b6ef", 1.0: "#2a78d6", 2.0: "#104281"}
RESL = {2.5: "2.5 km", 1.25: "1.25 km", 0.625: "625 m", 0.3125: "312 m"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "legend.frameon": False,
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2})


def dxaxis(ax):
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xticks(list(RESL))
    ax.set_xticklabels(list(RESL.values()))
    ax.xaxis.set_minor_locator(mt.NullLocator())


# ---- I1: convergence with resolution (sed x1) ----
vv = [("LWP", "LWP (g m$^{-2}$)"), ("cloud_cover", "cloud cover"), ("we_mm_s", "$w_e$ (mm s$^{-1}$)"),
      ("LWP_sd_online", "LWP spatial SD (g m$^{-2}$)"), ("precip", "surface precip (mm day$^{-1}$)")]
fig, axs = plt.subplots(1, len(vv), figsize=(15, 3.3))
for ax, (v, vl) in zip(axs, vv):
    for nd in NDC:
        for ps, ls, mk in (("on", "-", "o"), ("off", (0, (4, 2)), "s")):
            d = df[(df.sed == 1) & (df.Nd_target == nd) & (df.precsupp == ps)].sort_values("dx_km", ascending=False)
            ax.plot(d.dx_km, d[v], ls=ls, marker=mk, ms=4.5, lw=1.6, color=NDC[nd],
                    mfc=NDC[nd] if ps == "on" else "white")
    dxaxis(ax)
    ax.set_title(vl, fontsize=9.5)
    ax.set_xlabel("Δx")
h = [Line2D([], [], color=NDC[n], lw=2.5, label=f"Nd {n}") for n in NDC]
h += [Line2D([], [], color=INK2, marker="o", label="suppression on"),
      Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.1))
fig.suptitle("Resolution dependence, sed ×1, hours 10–12", y=1.18, fontweight="bold")
fig.tight_layout()
fig.savefig(f"{out}/figI1_convergence.png", dpi=150, bbox_inches="tight")

# ---- I2: low-Nd susceptibility vs resolution, all sed ----
rows = []
for (dx, sed, ps), g in df.groupby(["dx_km", "sed", "precsupp"]):
    g = g.set_index("Nd_target")
    if {20, 50, 100} <= set(g.index):
        s = lambda a, b: np.log(g.LWP[b] / g.LWP[a]) / np.log(g.Nd_incloud[b] / g.Nd_incloud[a])
        rows.append({"dx_km": dx, "sed": sed, "precsupp": ps, "S_20_50": s(20, 50), "S_50_100": s(50, 100)})
S = pd.DataFrame(rows)
S.round(3).to_csv(f"{out}/susceptibility_lowNd.csv", index=False)
fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.5), sharey=True)
for ax, col, ttl in zip(axs, ["S_20_50", "S_50_100"], ["Nd 20 → 50", "Nd 50 → 100"]):
    for sed in SEDC:
        for ps, ls, mk in (("on", "-", "o"), ("off", (0, (4, 2)), "s")):
            d = S[(S.sed == sed) & (S.precsupp == ps)].sort_values("dx_km", ascending=False)
            ax.plot(d.dx_km, d[col], ls=ls, marker=mk, ms=4.5, lw=1.6, color=SEDC[sed],
                    mfc=SEDC[sed] if ps == "on" else "white")
    ax.axhline(0, color=INK2, lw=0.8)
    dxaxis(ax)
    ax.set_title(ttl)
    ax.set_xlabel("Δx")
axs[0].set_ylabel("$S = d\\ln\\mathrm{LWP}/d\\ln N_d$")
h = [Line2D([], [], color=SEDC[s], lw=2.5, label=f"sed ×{s:g}") for s in SEDC]
h += [Line2D([], [], color=INK2, marker="o", label="suppression on"),
      Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.08))
fig.tight_layout()
fig.savefig(f"{out}/figI2_susceptibility_lowNd.png", dpi=150, bbox_inches="tight")

# ---- I3: LWP maps at 12 h ----
CMAP = mcolors.LinearSegmentedColormap.from_list(
    "lwp", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
RES = [("2p5km", "2.5 km"), ("1p25km", "1.25 km"), ("625m", "625 m"), ("312m", "312 m")]


def lastmap(case):
    fl = sorted(glob.glob(f"{root}/{case}/run/{case}.aci2d.INSTANT.*.nc"))
    with netCDF4.Dataset(fl[-1]) as d:
        x, y = d["lon"][:] / 1e3, d["lat"][:] / 1e3
        lwp = d["LiqWaterPath"][-1, :] * 1e3
    xs, ys = np.unique(x), np.unique(y)
    img = np.full((ys.size, xs.size), np.nan)
    img[np.searchsorted(ys, y), np.searchsorted(xs, x)] = lwp
    return xs, ys, img


for ps in ("on", "off"):
    fig, axs = plt.subplots(3, 4, figsize=(12.5, 9.6), constrained_layout=True)
    for i, nd in enumerate((20, 50, 100)):
        for j, (r, rl) in enumerate(RES):
            ax = axs[i, j]
            case = f"sedps_{r}_nd{nd}_sed1_ps{ps}"
            try:
                xs, ys, img = lastmap(case)
            except Exception:
                ax.set_axis_off(); continue
            im = ax.imshow(img, origin="lower", extent=(xs[0], xs[-1], ys[0], ys[-1]), cmap=CMAP,
                           vmin=0, vmax=300, interpolation="nearest")
            ax.set_title(f"{rl}, Nd {nd}: mean {np.nanmean(img):.0f} g/m², cover {np.nanmean(img > 10):.2f}",
                         fontsize=8.5)
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    fig.colorbar(im, ax=axs, shrink=0.6, label="LWP at 12 h (g m$^{-2}$)")
    fig.suptitle(f"LWP at hour 12, 240 km domain, sed ×1, precip suppression {ps}", fontweight="bold")
    fig.savefig(f"{out}/figI3_lwp_maps_ps{ps}.png", dpi=130)

# ---- I4: LWP and cloud cover time series, 312 m vs coarser ----
def series(case):
    fl = sorted(glob.glob(f"{root}/{case}/run/{case}.aci2d.INSTANT.*.nc"))
    tt, lw = [], []
    for f in fl:
        with netCDF4.Dataset(f) as d:
            tt.append(d["time"][:]); lw.append(d["LiqWaterPath"][:] * 1e3)
    tt, lw = np.concatenate(tt), np.concatenate(lw)
    tt, iu = np.unique(tt, return_index=True)
    lw = lw[iu]
    return (tt - tt[0]) * 24, lw.mean(axis=1), (lw > 10).mean(axis=1)


RC = {"2p5km": "#2a78d6", "1p25km": "#e34948", "625m": "#008300", "312m": "#0b0b0b"}
fig, axs = plt.subplots(2, 3, figsize=(13, 6.2), sharex=True)
for j, nd in enumerate((20, 50, 100)):
    for r, rl in RES:
        for ps, ls in (("on", "-"), ("off", (0, (4, 2)))):
            case = f"sedps_{r}_nd{nd}_sed1_ps{ps}"
            try:
                t, m, cc = series(case)
            except Exception:
                continue
            axs[0, j].plot(t, m, color=RC[r], ls=ls, lw=1.5)
            axs[1, j].plot(t, cc, color=RC[r], ls=ls, lw=1.5)
    axs[0, j].set_title(f"Nd {nd}, sed ×1")
    axs[1, j].set_xlabel("hour")
    for ax in axs[:, j]:
        ax.axvspan(10, 12, color=GRID, alpha=0.6, lw=0, zorder=0)
        ax.set_xlim(0, 12); ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
axs[0, 0].set_ylabel("LWP (g m$^{-2}$)"); axs[1, 0].set_ylabel("cloud cover (LWP > 10)")
h = [Line2D([], [], color=RC[r], lw=2.5, label=rl) for r, rl in RES]
h += [Line2D([], [], color=INK2, label="suppression on"), Line2D([], [], color=INK2, ls=(0, (4, 2)), label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=6, bbox_to_anchor=(0.5, 1.04))
fig.tight_layout()
fig.savefig(f"{out}/figI4_timeseries.png", dpi=150, bbox_inches="tight")
print("ok")
