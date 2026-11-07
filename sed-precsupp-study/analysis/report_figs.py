#!/usr/bin/env python3
"""
Mechanism figures for the technical report.  Usage: report_figs.py OUTDIR [RUNROOT]
Reads summary_h4-6.csv and timeseries_15min.csv in OUTDIR; RUNROOT (for the
column-level joint histograms) defaults to /pscratch/sd/m/mahf708/dp_screamxx_sedps.
"""
import glob
import os
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
from matplotlib.lines import Line2D

out = sys.argv[1]
root = sys.argv[2] if len(sys.argv) > 2 else "/pscratch/sd/m/mahf708/dp_screamxx_sedps"
T_END = float(os.environ.get("SEDPS_TEND", 6))
WIN = f"{T_END - 2:g}–{T_END:g}"
df = pd.read_csv(f"{out}/summary_h{T_END - 2:g}-{T_END:g}.csv")
ts = pd.read_csv(f"{out}/timeseries_15min.csv")

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SEDC = {0.5: "#86b6ef", 1.0: "#2a78d6", 2.0: "#104281"}
# resolution as an ordered magnitude: one aqua->blue sequential-ish ramp is hard to read
# with 6 levels, so use the categorical palette in fixed order (identity, not rank)
RES = [r for r in ["40km", "20km", "10km", "5km", "2p5km", "1p25km"] if r in set(df.res)]
RESC = dict(zip(["40km", "20km", "10km", "5km", "2p5km", "1p25km"],
                ["#eda100", "#e87ba4", "#6250d6", "#1baf7a", "#2a78d6", "#e34948"]))
LAB = {"40km": "40 km", "20km": "20 km", "10km": "10 km", "5km": "5 km", "2p5km": "2.5 km", "1p25km": "1.25 km"}
NDT = sorted(df.Nd_target.unique())
plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.titlesize": 10, "axes.titleweight": "bold", "legend.frameon": False,
})


def ndaxis(ax):
    ax.set_xscale("log")
    t = [n for n in [20, 50, 100, 200, 500, 1000] if n <= max(NDT) * 1.3]
    ax.set_xticks(t)
    ax.xaxis.set_major_formatter(mt.ScalarFormatter())
    ax.xaxis.set_minor_locator(mt.NullLocator())


def pivot(v):
    return df.pivot_table(index=["res", "Nd_target", "sed"], columns="precsupp", values=v)


# ---------- R1: pathway decomposition ----------
# precip-suppression pathway: LWP(on) - LWP(off), same sed
# sedimentation pathway: LWP(sed 2) - LWP(sed 0.5), same suppression
p = pivot("LWP").reset_index()
p["d_ps"] = p["on"] - p["off"]
q = df.pivot_table(index=["res", "Nd_target", "precsupp"], columns="sed", values="LWP").reset_index()
q["d_sed"] = q[2.0] - q[0.5]
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
for r in RES:
    d = p[(p.res == r) & (p.sed == 1.0)].sort_values("Nd_target")
    axs[0].plot(d.Nd_target, d.d_ps, "-o", color=RESC[r], ms=4, lw=1.6, label=LAB[r])
    for ps, ls, mk in (("on", "-", "o"), ("off", (0, (4, 2)), "s")):
        d = q[(q.res == r) & (q.precsupp == ps)].sort_values("Nd_target")
        axs[1].plot(d.Nd_target, d.d_sed, ls=ls, marker=mk, color=RESC[r], ms=4, lw=1.4,
                    mfc=RESC[r] if ps == "on" else "white")
for ax in axs:
    ax.axhline(0, color=INK2, lw=0.8)
    ndaxis(ax)
    ax.set_xlabel("Nd target (cm$^{-3}$)")
axs[0].set_ylabel("ΔLWP (g m$^{-2}$)")
axs[0].set_title("precip-suppression pathway\nLWP(suppression on) − LWP(off), sed ×1")
axs[1].set_title("sedimentation pathway\nLWP(sed ×2) − LWP(sed ×0.5)")
h = [Line2D([], [], color=RESC[r], lw=2, label=LAB[r]) for r in RES]
h += [Line2D([], [], color=INK2, marker="o", label="suppression on"),
      Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, 1.07))
fig.tight_layout()
fig.savefig(f"{out}/figR1_pathways.png", dpi=150, bbox_inches="tight")

# ---------- R2: entrainment vs cloud-top sedimentation proxy ----------
# Stokes: v_sed ~ sed_factor * r^2; use cloud-top r_eff (um) -> proxy in units of (sed x 10 um)^2
df["vsed_proxy"] = df.sed * (df.reff_top_um / 10.0) ** 2
fig, axs = plt.subplots(1, 2, figsize=(10, 3.9), sharey=True)
for ax, sel, ttl in ((axs[0], df.dx_km >= 5, "Δx ≥ 5 km (single-column-like)"),
                     (axs[1], df.dx_km <= 2.5, "Δx ≤ 2.5 km (resolved cells)")):
    for r in [r for r in RES if r in set(df[sel].res)]:
        for ps, mk in (("on", "o"), ("off", "s")):
            d = df[(df.res == r) & (df.precsupp == ps)]
            ax.scatter(d.vsed_proxy, d.we_mm_s, s=22, marker=mk, color=RESC[r] if ps == "on" else "white",
                       edgecolor=RESC[r], lw=1.1, zorder=3)
    ax.set_xscale("log")
    ax.set_xticks([0.2, 0.5, 1, 2, 5])
    ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.xaxis.set_minor_locator(mt.NullLocator())
    ax.set_xlabel("cloud-top fall-speed proxy:  sed × ($r_\\mathrm{eff,top}$ / 10 µm)$^2$")
    ax.set_title(ttl)
axs[0].set_ylabel("entrainment $w_e$ (mm s$^{-1}$)")
h = [Line2D([], [], color=RESC[r], marker="o", lw=0, label=LAB[r]) for r in RES]
h += [Line2D([], [], color=INK2, marker="o", lw=0, label="suppression on"),
      Line2D([], [], color=INK2, marker="s", mfc="white", lw=0, label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, 1.07))
fig.tight_layout()
fig.savefig(f"{out}/figR2_we_vs_vsed.png", dpi=150, bbox_inches="tight")

# ---------- R3: steadiness: LWP trend over hours 4-6 ----------
rows = []
for (case, r, nd, sed, ps), g in ts.groupby(["case", "res", "Nd_target", "sed_factor", "precip_suppression"]):
    g = g[(g.time_h > T_END - 2) & (g.time_h <= T_END)].dropna(subset=["LWP_gm2"])
    slope = np.polyfit(g.time_h, g.LWP_gm2, 1)[0]
    rows.append({"res": r, "Nd_target": nd, "sed": sed, "precsupp": ps, "dLWPdt": slope,
                 "rel": slope * 2 / g.LWP_gm2.mean()})
T = pd.DataFrame(rows)
T.round(3).to_csv(f"{out}/lwp_trend_h{T_END - 2:g}-{T_END:g}.csv", index=False)
fig, axs = plt.subplots(1, len(RES), figsize=(2.3 * len(RES), 3.0), sharey=True, sharex=True)
for ax, r in zip(axs, RES):
    for sed in (0.5, 1.0, 2.0):
        for ps, ls, mk in (("on", "-", "o"), ("off", (0, (4, 2)), "s")):
            d = T[(T.res == r) & (T.sed == sed) & (T.precsupp == ps)].sort_values("Nd_target")
            ax.plot(d.Nd_target, d.dLWPdt, ls=ls, marker=mk, ms=3.5, color=SEDC[sed], lw=1.3,
                    mfc=SEDC[sed] if ps == "on" else "white")
    ax.axhspan(-5, 5, color=GRID, alpha=0.6, lw=0, zorder=0)
    ax.axhline(0, color=INK2, lw=0.8)
    ndaxis(ax)
    ax.set_title(LAB[r])
    ax.set_xlabel("Nd target")
axs[0].set_ylabel(f"dLWP/dt, hours {WIN}\n(g m$^{{-2}}$ h$^{{-1}}$)")
h = [Line2D([], [], color=SEDC[s], lw=2.5, label=f"sed ×{s:g}") for s in (0.5, 1.0, 2.0)]
h += [Line2D([], [], color=INK2, marker="o", label="suppression on"),
      Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.1))
fig.tight_layout()
fig.savefig(f"{out}/figR3_lwp_trend.png", dpi=150, bbox_inches="tight")

# ---------- R4: column LWP distributions at km scale ----------
# Prescribed CCN keeps Nd nearly uniform within a domain, so the column-level
# information is in the LWP distribution (deck break-up, thinning), not Nd-LWP.
import netCDF4  # noqa: E402
NDC = {20: "#86b6ef", 100: "#2a78d6", 1000: "#0d366b"}
fine = [r for r in ("2p5km", "1p25km") if r in RES]
bins = np.logspace(0, np.log10(800), 50)
mid = np.sqrt(bins[1:] * bins[:-1])
fig, axs = plt.subplots(len(fine), 3, figsize=(11, 3.1 * len(fine)), sharex=True, sharey=True, squeeze=False)
for i, r in enumerate(fine):
    for j, sed in enumerate(("0p5", "1", "2")):
        ax = axs[i, j]
        for nd in [n for n in (20, 100, 1000) if n in NDT]:
            for ps, ls in (("on", "-"), ("off", (0, (4, 2)))):
                case = f"sedps_{r}_nd{nd}_sed{sed}_ps{ps}"
                fl = sorted(glob.glob(f"{root}/{case}/run/{case}.aci2d.INSTANT.*.nc"))
                if not fl:
                    continue
                lw, tt = [], []
                for fn in fl:   # restart segments write one file each
                    l = netCDF4.Dataset(fn); l.set_auto_mask(False)
                    tt.append(l["time"][:]); lw.append(l["LiqWaterPath"][:])
                tt, lw = np.concatenate(tt), np.concatenate(lw)
                tt, iu = np.unique(tt, return_index=True)
                lw = lw[iu]
                lwp = lw[(tt - tt[0]) * 24 > T_END - 2].ravel() * 1e3
                h, _ = np.histogram(lwp, bins=bins)   # columns below 1 g/m2 (clear) drop out,
                ax.plot(mid, h / lwp.size / np.diff(np.log10(bins)),   # so the area is the cloudy fraction
                        color=NDC.get(nd, INK), ls=ls, lw=1.5)
        ax.set_xscale("log")
        ax.axvline(10, color=INK2, lw=0.7, ls=":")
        ax.set_title(f"{LAB[r]}, sed ×{sed.replace('0p5', '0.5')}")
        if i == len(fine) - 1:
            ax.set_xlabel(f"column LWP (g m$^{{-2}}$), hours {WIN}")
        if j == 0:
            ax.set_ylabel("fraction of columns\nper decade of LWP")
h = [Line2D([], [], color=NDC[n], lw=2.5, label=f"Nd {n}") for n in NDC if n in NDT]
h += [Line2D([], [], color=INK2, label="suppression on"),
      Line2D([], [], color=INK2, ls=(0, (4, 2)), label="suppression off")]
fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, 1.04))
fig.tight_layout()
fig.savefig(f"{out}/figR4_lwp_pdf.png", dpi=150, bbox_inches="tight")
print("ok")
