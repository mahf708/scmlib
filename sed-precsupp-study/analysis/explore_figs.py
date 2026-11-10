#!/usr/bin/env python3
"""
Figures from explore.py output.   explore_figs.py NPZDIR SUMMARY_CSV OUTDIR
X1 cell scale        X2 resolved vs SGS turbulence    X3 w skewness (Sc vs Cu)
X4 decoupling        X5 rain budget                   X6 mean profiles
X7 radiative driving X8 LWP spectra
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
from matplotlib.lines import Line2D

npzdir, summ, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
S = pd.read_csv(summ)
rows, prof = [], {}
for f in sorted(glob.glob(f"{npzdir}/explore_*.npz")):
    case = os.path.basename(f)[8:-4]
    d = np.load(f)
    rows.append({"case": case, **{k: float(d[k]) for k in d.files if d[k].ndim == 0}})
    prof[case] = {k: d[k] for k in d.files if d[k].ndim == 1}
E = pd.DataFrame(rows).merge(S, on="case", suffixes=("", "_s"))
E = E[E.turb3d == "off"]
E.round(4).to_csv(f"{out}/explore_scalars.csv", index=False)

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
ALLRES = ["40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m", "312m"]
RESC = dict(zip(ALLRES, ["#eda100", "#e87ba4", "#6250d6", "#1baf7a", "#2a78d6", "#e34948", "#008300", "#0b0b0b"]))
LAB = dict(zip(ALLRES, ["40 km", "20 km", "10 km", "5 km", "2.5 km", "1.25 km", "625 m", "312 m"]))
NDS = [20, 50, 100, 200, 500, 1000]
NDC = dict(zip(NDS, ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]))
KM = [r for r in ["5km", "2p5km", "1p25km", "625m", "312m"] if r in set(E.res)]
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "legend.frameon": False,
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
PSL = {"on": dict(ls="-", marker="o"), "off": dict(ls=(0, (4, 2)), marker="s")}


def ndaxis(ax):
    ax.set_xscale("log"); ax.set_xticks(NDS)
    ax.xaxis.set_major_formatter(mt.ScalarFormatter()); ax.xaxis.set_minor_locator(mt.NullLocator())


def dxaxis(ax, dxs):
    ax.set_xscale("log"); ax.invert_xaxis(); ax.set_xticks(dxs)
    ax.set_xticklabels([f"{x:g}" for x in dxs]); ax.xaxis.set_minor_locator(mt.NullLocator())


def nd_lines(ax, v, sed=1.0, res=KM, both=True):
    for r in res:
        for ps in (("on", "off") if both else ("on",)):
            d = E[(E.res == r) & (E.sed == sed) & (E.precsupp == ps)].sort_values("Nd_target")
            st = PSL[ps]
            ax.plot(d.Nd_incloud, d[v], ls=st["ls"], marker=st["marker"], ms=3.5, lw=1.5, color=RESC[r],
                    mfc=RESC[r] if ps == "on" else "white")
    ndaxis(ax)


def res_legend(fig, res, y=1.05, extra=True):
    h = [Line2D([], [], color=RESC[r], lw=2.5, label=LAB[r]) for r in res]
    if extra:
        h += [Line2D([], [], color=INK2, marker="o", label="suppression on"),
              Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="suppression off")]
    fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, y))


# ---- X1 cell scale ----
fig, axs = plt.subplots(1, 3, figsize=(13.5, 3.6))
dxs = sorted(E[E.res.isin(KM)].dx_km.unique(), reverse=True)
for nd in NDS:
    for ps in ("on", "off"):
        d = E[E.res.isin(KM) & (E.sed == 1) & (E.Nd_target == nd) & (E.precsupp == ps)].sort_values("dx_km", ascending=False)
        st = PSL[ps]
        kw = dict(ls=st["ls"], marker=st["marker"], ms=4, lw=1.4, color=NDC[nd], mfc=NDC[nd] if ps == "on" else "white")
        axs[0].plot(d.dx_km, d.lambda_peak, **kw)
        axs[1].plot(d.dx_km, d.lambda_peak / d.dx_phys, **kw)
        axs[2].plot(d.dx_km, d.lambda_peak * 1e3 / d.zi, **kw)
for ax, t in zip(axs, ["dominant LWP wavelength λ (km)", "λ / physics-grid spacing", "λ / inversion height (aspect ratio)"]):
    dxaxis(ax, dxs); ax.set_xlabel("Δx (km)"); ax.set_title(t, fontsize=9.5)
axs[0].set_yscale("log")
h = [Line2D([], [], color=NDC[n], lw=2.5, label=f"Nd {n}") for n in NDS]
h += [Line2D([], [], color=INK2, marker="o", label="supp. on"), Line2D([], [], color=INK2, ls=(0, (4, 2)), marker="s", mfc="white", label="supp. off")]
fig.legend(handles=h, loc="upper center", ncol=len(h), bbox_to_anchor=(0.5, 1.08))
fig.tight_layout(); fig.savefig(f"{out}/figX1_cell_scale.png", dpi=150, bbox_inches="tight")

# ---- X2 grey zone ----
fig, axs = plt.subplots(1, 3, figsize=(13.5, 3.6))
dxa = sorted(E.dx_km.unique(), reverse=True)
for nd in NDS:
    d = E[(E.sed == 1) & (E.Nd_target == nd) & (E.precsupp == "on")].sort_values("dx_km", ascending=False)
    axs[0].plot(d.dx_km, d.f_res, "-o", ms=4, lw=1.4, color=NDC[nd])
    axs[1].plot(d.dx_km, d.w2_sgs_bl, "-o", ms=4, lw=1.4, color=NDC[nd])
    axs[2].plot(d.dx_km, d.w2_res_bl, "-o", ms=4, lw=1.4, color=NDC[nd])
for ax, t in zip(axs, ["resolved share of BL w-variance", "SHOC (SGS) w-variance, BL mean (m² s⁻²)",
                       "resolved w-variance, BL mean (m² s⁻²)"]):
    dxaxis(ax, dxa); ax.set_xlabel("Δx (km)"); ax.set_title(t, fontsize=9.5)
fig.legend(handles=[Line2D([], [], color=NDC[n], lw=2.5, label=f"Nd {n}") for n in NDS], loc="upper center",
           ncol=6, bbox_to_anchor=(0.5, 1.07))
fig.tight_layout(); fig.savefig(f"{out}/figX2_grey_zone.png", dpi=150, bbox_inches="tight")

# ---- X3 skewness / regime ----
fig, axs = plt.subplots(1, 3, figsize=(13.5, 3.6), sharey=True)
for ax, sed in zip(axs, (0.5, 1.0, 2.0)):
    nd_lines(ax, "skew_w_bl", sed=sed)
    ax.axhline(0, color=INK2, lw=0.8); ax.set_title(f"sed ×{sed:g}"); ax.set_xlabel("in-cloud Nd (cm$^{-3}$)")
axs[0].set_ylabel("resolved w skewness, BL\n(> 0 cumulus-like, < 0 Sc-like)")
res_legend(fig, KM, 1.08)
fig.tight_layout(); fig.savefig(f"{out}/figX3_skewness.png", dpi=150, bbox_inches="tight")

# ---- X4 decoupling ----
fig, axs = plt.subplots(1, 3, figsize=(13.5, 3.6))
nd_lines(axs[0], "dqt", res=ALLRES); axs[0].set_title("Δq$_t$ (bottom − top quarter of BL, g kg$^{-1}$)", fontsize=9.5)
nd_lines(axs[1], "dthl", res=ALLRES); axs[1].set_title("Δθ$_l$ (top − bottom quarter, K)", fontsize=9.5)
for ax in axs[:2]:
    ax.set_xlabel("in-cloud Nd (cm$^{-3}$)")
for r in ALLRES:
    d = E[E.res == r]
    axs[2].scatter(d.dqt, d.LWP, s=12, color=RESC[r], alpha=0.8)
axs[2].set_xlabel("Δq$_t$ (g kg$^{-1}$)"); axs[2].set_ylabel("LWP (g m$^{-2}$)"); axs[2].set_title("LWP vs decoupling (all runs)", fontsize=9.5)
res_legend(fig, ALLRES, 1.08)
fig.tight_layout(); fig.savefig(f"{out}/figX4_decoupling.png", dpi=150, bbox_inches="tight")

# ---- X5 rain budget ----
E["rain_prod"] = E.autoconv_col + E.accret_col
fig, axs = plt.subplots(1, 4, figsize=(16, 3.6))
nd_lines(axs[0], "rain_prod", res=ALLRES, both=False); axs[0].set_yscale("log")
axs[0].set_title("rain production (autoconv + accretion, mm d$^{-1}$)", fontsize=9)
nd_lines(axs[1], "autoconv_col", res=ALLRES, both=False); axs[1].set_yscale("log")
axs[1].set_title("autoconversion (mm d$^{-1}$)", fontsize=9)
nd_lines(axs[2], "evap_frac", res=ALLRES, both=False); axs[2].set_title("share of rain production evaporated", fontsize=9)
nd_lines(axs[3], "rain_frac", res=ALLRES, both=False); axs[3].set_title("raining fraction (sfc > 0.5 mm d$^{-1}$)", fontsize=9)
for ax in axs:
    ax.set_xlabel("in-cloud Nd (cm$^{-3}$)")
res_legend(fig, ALLRES, 1.08, extra=False)
fig.suptitle("sed ×1, precipitation suppression on", y=1.16, fontsize=10, fontweight="bold")
fig.tight_layout(); fig.savefig(f"{out}/figX5_rain_budget.png", dpi=150, bbox_inches="tight")

# ---- X6 profiles ----
pv = [("thl", "θ$_l$ (K)", 1), ("qt", "q$_t$ (g kg$^{-1}$)", 1e3), ("cf", "liquid cloud fraction", 1),
      ("w2tot", "w variance, resolved + SGS (m² s⁻²)", 1), ("rad_heat", "LW heating (K h$^{-1}$)", 3600)]
fig, axs = plt.subplots(2, len(pv), figsize=(16, 7.2), sharey=True)
for i, nd in enumerate((20, 200)):
    for j, (v, vl, sc) in enumerate(pv):
        ax = axs[i, j]
        for r in ALLRES:
            c = f"sedps_{r}_nd{nd}_sed1_pson"
            if c not in prof:
                continue
            p = prof[c]
            x = p["w2_sgs"] + p.get("w2_res", 0 * p["w2_sgs"]) if v == "w2tot" else p[v]
            ax.plot(x * sc, p["z"], color=RESC[r], lw=1.5)
        ax.set_ylim(0, 1200)
        if i == 0:
            ax.set_title(vl, fontsize=9.5)
        if j == 0:
            ax.set_ylabel(f"Nd {nd}\nheight (m)")
axs[0, 0].set_xlim(287, 300); axs[1, 0].set_xlim(287, 300); axs[0, 1].set_xlim(4, 10); axs[1, 1].set_xlim(4, 10)
res_legend(fig, ALLRES, 1.03, extra=False)
fig.tight_layout(); fig.savefig(f"{out}/figX6_profiles.png", dpi=150, bbox_inches="tight")

# ---- X7 radiative driving ----
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
for r in ALLRES:
    d = E[E.res == r]
    axs[0].scatter(d.LWP, -d.lw_cool_bl, s=12, color=RESC[r])
    axs[1].scatter(-d.lw_cool_bl, d.we_mm_s, s=12, color=RESC[r])
axs[0].set_xlabel("LWP (g m$^{-2}$)"); axs[0].set_ylabel("BL LW cooling (W m$^{-2}$)")
axs[1].set_xlabel("BL LW cooling (W m$^{-2}$)"); axs[1].set_ylabel("$w_e$ (mm s$^{-1}$)")
res_legend(fig, ALLRES, 1.06, extra=False)
fig.tight_layout(); fig.savefig(f"{out}/figX7_radiation.png", dpi=150, bbox_inches="tight")

# ---- X8 spectra ----
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
for ax, nd in zip(axs, (20, 200)):
    for r in KM:
        c = f"sedps_{r}_nd{nd}_sed1_pson"
        if c not in prof or "spec" not in prof[c]:
            continue
        k, sp = prof[c]["spec_k"], prof[c]["spec"]
        ax.loglog(1 / k, k * sp / np.max(k * sp), color=RESC[r], lw=1.6)
    ax.invert_xaxis(); ax.set_xlabel("wavelength (km)"); ax.set_title(f"Nd {nd}, sed ×1, suppression on")
axs[0].set_ylabel("k·P(k), normalised")
res_legend(fig, KM, 1.08, extra=False)
fig.tight_layout(); fig.savefig(f"{out}/figX8_spectra.png", dpi=150, bbox_inches="tight")
print("ok", len(E))
