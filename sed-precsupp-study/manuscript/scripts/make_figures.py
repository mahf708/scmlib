#!/usr/bin/env python3
"""
All manuscript figures (PDF, vector) from the tables built by build_tables.py and
ml_budget.py and the per-run npz files.  Light work: run on a login node with
`module load python; python make_figures.py`.
"""
import glob
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm

R = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h"
T = f"{R}/manuscript/tables"
FIG = "/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/figures"
os.makedirs(FIG, exist_ok=True)

mpl.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.5, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "lines.linewidth": 1.2, "lines.markersize": 3.5,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "savefig.dpi": 300, "pdf.fonttype": 42, "axes.grid": False, "mathtext.default": "regular",
})
W2 = 7.0   # full width (in)

DX = [40.0, 20.0, 10.0, 5.0, 2.5, 1.25, 0.625, 0.3125]
DXLAB = {40.0: "40 km", 20.0: "20 km", 10.0: "10 km", 5.0: "5 km", 2.5: "2.5 km", 1.25: "1.25 km",
         0.625: "625 m", 0.3125: "312 m"}
RESLAB = {"40km": 40.0, "20km": 20.0, "10km": 10.0, "5km": 5.0, "2p5km": 2.5, "1p25km": 1.25,
          "625m": 0.625, "312m": 0.3125}
CDX = {d: c for d, c in zip(DX, plt.cm.viridis(np.linspace(0.92, 0.0, 8)))}
CSED = {0.5: "#56B4E9", 1.0: "#0072B2", 2.0: "#D55E00"}
ND = [20, 50, 100, 200, 500, 1000]
CND = {n: c for n, c in zip(ND, plt.cm.magma(np.linspace(0.12, 0.78, 6)))}
BR = {"low": r"$S_{20\to50}$", "high": r"$S_{100\to200}$", "vhigh": r"$S_{200\to1000}$"}

runs = pd.read_csv(f"{T}/runs.csv")
S = pd.read_csv(f"{T}/susceptibility.csv")
D = pd.read_csv(f"{T}/decomposition.csv")
ST = pd.read_csv(f"{T}/s_time.csv")
B = pd.read_csv(f"{T}/ml_budget.csv")
off = runs[runs.turb3d == "off"]


def label(ax, s, x=-0.14, y=1.04):
    ax.text(x, y, s, transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom")


def dx_axis(ax, sub=False):
    ax.set_xscale("log")
    ticks = [d for d in DX if (d <= 5 or not sub)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([DXLAB[d].replace(" ", "\n") if False else DXLAB[d] for d in ticks], rotation=45, ha="right")
    ax.minorticks_off()
    ax.invert_xaxis()
    ax.set_xlabel(r"grid spacing $\Delta x$")


def nd_axis(ax, sparse=False):
    ax.set_xscale("log")
    t = [20, 100, 1000] if sparse else [20, 50, 100, 200, 500, 1000]
    ax.set_xticks(t)
    ax.set_xticklabels([str(v) for v in t])
    ax.minorticks_off()
    ax.set_xlabel(r"in-cloud $N_d$ (cm$^{-3}$)")


def dx_legend(ax, dxs=DX, **kw):
    h = [plt.Line2D([], [], color=CDX[d], marker="o", label=DXLAB[d]) for d in dxs]
    ax.legend(handles=h, **kw)


def save(fig, name):
    fig.savefig(f"{FIG}/{name}.pdf", bbox_inches="tight")
    fig.savefig(f"{FIG}/{name}.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(name)


# ------------------------------------------------------------------ Fig 1: LWP maps
def fig_maps():
    cols = [5.0, 2.5, 1.25, 0.625, 0.3125]
    inv = {v: k for k, v in RESLAB.items()}
    fig, axs = plt.subplots(3, 5, figsize=(W2, 4.5), constrained_layout=True)
    for i, nd in enumerate([20, 200, 1000]):
        for j, dx in enumerate(cols):
            ax = axs[i, j]
            f = f"{R}/manuscript/fields/fields_sedps_{inv[dx]}_nd{nd}_sed1_pson.npz"
            d = np.load(f)
            x, y, v = d["x"] / 1e3, d["y"] / 1e3, d["lwp12"]
            xs, ys = np.unique(x), np.unique(y)
            img = np.full((ys.size, xs.size), np.nan)
            img[np.searchsorted(ys, y), np.searchsorted(xs, x)] = v
            dxp = xs[1] - xs[0]
            im = ax.imshow(img, origin="lower", extent=[xs[0] - dxp / 2, xs[-1] + dxp / 2, ys[0] - dxp / 2, ys[-1] + dxp / 2],
                           cmap="bone", vmin=0, vmax=400, interpolation="nearest")
            ax.set_xticks([0, 120, 240] if False else [])
            ax.set_yticks([])
            m = runs[(runs.res == inv[dx]) & (runs.Nd_target == nd) & (runs.sed == 1) & (runs.precsupp == "on") & (runs.turb3d == "off")].iloc[0]
            ax.text(0.03, 0.03, f"{m.LWP:.0f} g m$^{{-2}}$, cc {m.cloud_cover:.2f}", transform=ax.transAxes, color="w", fontsize=6,
                    bbox=dict(facecolor="k", alpha=0.5, lw=0, pad=1))
            if i == 0:
                ax.set_title(DXLAB[dx])
            if j == 0:
                ax.set_ylabel(f"$N_d$ target {nd} cm$^{{-3}}$")
            label(ax, f"({'abcdefghijklmno'[i * 5 + j]})", x=0.0, y=1.01) if False else None
    cb = fig.colorbar(im, ax=axs, shrink=0.6, label="LWP (g m$^{-2}$)", extend="max")
    save(fig, "fig01_maps")


# ------------------------------------------------------------------ Fig 2: response
def fig_response():
    fig, axs = plt.subplots(2, 2, figsize=(W2, 5.0), constrained_layout=True)
    sub = off[off.sed == 1].sort_values("Nd_target")
    for dx in DX:
        for ps, ax in (("on", axs[0, 0]), ("off", axs[0, 1])):
            g = sub[(sub.dx_km == dx) & (sub.precsupp == ps)]
            ax.plot(g.Nd_incloud, g.LWP, "o-", color=CDX[dx])
            if ps == "on":
                k = g.LWP.idxmax()
                ax.plot(g.Nd_incloud[k], g.LWP[k], "*", ms=9, color=CDX[dx], mec="k", mew=0.5)
        g = sub[(sub.dx_km == dx) & (sub.precsupp == "on")]
        axs[1, 0].plot(g.Nd_incloud, g.we_812_mm_s, "o-", color=CDX[dx])
        axs[1, 1].plot(g.Nd_incloud, g.precip, "o-", color=CDX[dx])
        g = sub[(sub.dx_km == dx) & (sub.precsupp == "off")]
        axs[1, 0].plot(g.Nd_incloud, g.we_812_mm_s, "o--", color=CDX[dx], alpha=0.5, ms=2)
        axs[1, 1].plot(g.Nd_incloud, g.precip, "o--", color=CDX[dx], alpha=0.5, ms=2)
    for ax in axs.flat:
        nd_axis(ax)
    axs[0, 0].set_title("precipitation suppression on (KK2000)")
    axs[0, 1].set_title(r"precipitation suppression off ($N_d$ exponent 0)")
    for ax in axs[0]:
        ax.set_ylabel("LWP (g m$^{-2}$)")
        ax.set_ylim(30, 360)
    axs[1, 0].set_ylabel(r"entrainment rate $w_e$ (mm s$^{-1}$)")
    axs[1, 1].set_ylabel("surface precipitation (mm d$^{-1}$)")
    axs[1, 1].set_yscale("log")
    axs[1, 1].set_ylim(1e-3, 3)
    h = [plt.Line2D([], [], color="k", ls="-", label="suppression on"),
         plt.Line2D([], [], color="k", ls="--", alpha=0.5, label="suppression off")]
    axs[1, 0].legend(handles=h, loc="lower right")
    dx_legend(axs[0, 1], ncol=2, loc="upper right")
    for ax, l in zip(axs.flat, "abcd"):
        label(ax, f"({l})")
    save(fig, "fig02_response")


# ------------------------------------------------------------------ Fig 3: susceptibility
def fig_susc():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.7), constrained_layout=True, sharey=False)
    s = S[S.turb3d == "off"]
    for ax, (b, lab) in zip(axs, BR.items()):
        for sed in (0.5, 1.0, 2.0):
            for ps, ls, mk in (("on", "-", "o"), ("off", "--", "s")):
                g = s[(s.sed == sed) & (s.precsupp == ps)].sort_values("dx_km", ascending=False)
                ax.errorbar(g.dx_km * (1.04 if sed == 2 else 0.96 if sed == 0.5 else 1), g[f"S_{b}"], yerr=g[f"S_{b}_sd"],
                            color=CSED[sed], ls=ls, marker=mk, ms=3, capsize=1.5, elinewidth=0.6,
                            mfc=CSED[sed] if ps == "on" else "w")
        ax.axhline(0, color="0.5", lw=0.5)
        dx_axis(ax)
        ax.set_title(f"{lab}")
        ax.set_ylabel(r"$S = d\ln \mathrm{LWP}/d\ln N_d$" if b == "low" else "")
    h = [plt.Line2D([], [], color=CSED[s_], marker="o", label=f"sed. factor {s_:g}") for s_ in (0.5, 1, 2)]
    h += [plt.Line2D([], [], color="k", ls="-", marker="o", label="suppression on"),
          plt.Line2D([], [], color="k", ls="--", marker="s", mfc="w", label="suppression off")]
    fig.legend(handles=h, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.08))
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.2)
    save(fig, "fig03_susceptibility")


# ------------------------------------------------------------------ Fig 4: time evolution
def fig_time():
    fig = plt.figure(figsize=(W2, 4.6), constrained_layout=True)
    gs = fig.add_gridspec(2, 3)
    st = ST[(ST.sed == 1) & (ST.precsupp == "on")]
    for i, (b, lab) in enumerate(BR.items()):
        ax = fig.add_subplot(gs[0, i])
        for dx in DX:
            g = st[st.dx_km == dx].sort_values("t_end")
            ax.plot(g.t_end - 1, g[f"S_{b}"], "o-", color=CDX[dx])
        ax.axhline(0, color="0.5", lw=0.5)
        ax.set_xticks([3, 5, 7, 9, 11])
        ax.set_xlabel("window centre (h)")
        ax.set_title(lab + ", suppression on, sed. 1")
        if i == 0:
            ax.set_ylabel("S (2-h windows)")
        label(ax, f"({'abc'[i]})", x=-0.2)
    dx_legend(fig.axes[0], ncol=2, loc="lower right", fontsize=5.5)
    ts = pd.read_csv(f"{R}/analysis_report5/timeseries_15min.csv")
    for k, (res, ps) in enumerate((("40km", "on"), ("312m", "on"), ("312m", "off"))):
        ax = fig.add_subplot(gs[1, k])
        for nd in ND:
            g = ts[(ts.res == res) & (ts.Nd_target == nd) & (ts.sed_factor == 1) & (ts.precip_suppression == ps)
                   & (ts.turb3d == "off")].dropna(subset=["LWP_gm2"]).sort_values("time_h")
            ax.plot(g.time_h, g.LWP_gm2, color=CND[nd], label=f"{nd}")
        ax.axvspan(10, 12, color="0.9", lw=0)
        ax.set_xlabel("time (h)")
        ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
        ax.set_title(f"{DXLAB[RESLAB[res]]}, suppression {ps}, sed. 1")
        ax.set_ylim(0, 360)
        if k == 0:
            ax.set_ylabel("LWP (g m$^{-2}$)")
            ax.legend(title=r"$N_d$ target (cm$^{-3}$)", ncol=2, loc="upper left", fontsize=5.5, title_fontsize=6)
        label(ax, f"({'def'[k]})", x=-0.2)
    save(fig, "fig04_time")


# ------------------------------------------------------------------ Fig 5: decomposition
def fig_decomp():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.8), constrained_layout=True)
    d = D[(D.turb3d == "off") & (D.sed == 1)]
    comps = [("S_ps", "precip. suppression\n" r"$S_{on}-S_{off}$", "#0072B2"),
             ("S_sed", "sedimentation\n" r"$b\,s$ ($s=1$)", "#D55E00"),
             ("S_resid", "residual\n" r"$a$ ($S_{off}$ at $s\to0$)", "#999999")]
    x = np.arange(len(DX))
    for ax, (b, lab) in zip(axs, BR.items()):
        g = d[d.branch == b].set_index("dx_km").loc[DX]
        for k, (c, cl, col) in enumerate(comps):
            ax.bar(x + (k - 1) * 0.26, g[c], width=0.24, color=col, label=cl, edgecolor="w", lw=0.3)
        ax.plot(x, g.S_on, "k_", ms=10, mew=1.5, label=r"total $S_{on}$")
        ax.axhline(0, color="0.3", lw=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels([DXLAB[v] for v in DX], rotation=45, ha="right")
        ax.set_title(lab)
        label(ax, f"({'abc'[list(BR).index(b)]})", x=-0.2)
    axs[0].set_ylabel("contribution to S")
    axs[2].legend(loc="upper right", fontsize=5.5)
    save(fig, "fig05_decomposition")


# ------------------------------------------------------------------ Fig 6: entrainment
def fig_entrain():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.6), constrained_layout=True)
    ax = axs[0]
    for dx in DX:
        g = off[off.dx_km == dx]
        ax.scatter(g.sed * (g.reff_top_um / 10) ** 2, g.we_812_mm_s, s=6, color=CDX[dx], lw=0)
    ax.set_xscale("log")
    ax.set_xticks([0.1, 0.3, 1, 3]); ax.set_xticklabels(["0.1", "0.3", "1", "3"]); ax.minorticks_off()
    ax.set_xlabel(r"fall-speed proxy  $s\,(r_{e,top}/10\,\mu$m$)^2$")
    ax.set_ylabel(r"$w_e$ (mm s$^{-1}$)")
    dx_legend(ax, ncol=2, fontsize=5, loc="upper right", handletextpad=0.2, columnspacing=0.5)
    sub = off[(off.sed == 1) & (off.precsupp == "on")]
    for dx in DX:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[1].plot(g.Nd_incloud, g.eta_ent, "o-", color=CDX[dx])
        axs[2].plot(g.Nd_incloud, g.F_ent_moist, "o-", color=CDX[dx])
    nd_axis(axs[1]); nd_axis(axs[2])
    axs[1].axhline(1, color="0.5", lw=0.5, ls=":")
    axs[1].set_ylabel(r"$\eta=\rho c_p w_e\Delta\theta_l / F_{rad}$")
    axs[2].axhline(93, color="0.5", lw=0.5, ls=":")
    axs[2].text(25, 95, "surface LHF", fontsize=6, color="0.4")
    axs[2].set_ylabel(r"entrainment drying $-\rho L_v w_e \Delta q_t$ (W m$^{-2}$)")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.22)
    save(fig, "fig07_entrainment")


# ------------------------------------------------------------------ Fig 7: LWP budget
TERMS = [("ent", "entrainment", "#D55E00"), ("subs", "subsidence", "#CC79A7"), ("rad", "radiative cooling", "#0072B2"),
         ("sfc", "surface fluxes", "#009E73"), ("precip", "precipitation", "#56B4E9")]


def fig_budget():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.6), constrained_layout=True, sharey=True)
    b = B[(B.turb3d == "off") & (B.t_end == 12) & (B.sed == 1) & (B.precsupp == "on")]
    for ax, res in zip(axs, ("40km", "2p5km", "625m", "312m")):
        g = b[b.res == res].sort_values("Nd_target")
        nd = runs.set_index("case").loc[g.case, "Nd_incloud"].values
        for k, lab, col in TERMS:
            ax.plot(nd, 100 * g[f"dlwp_{k}"] / g.LWP, "o-", color=col, label=lab, ms=2.5)
        ax.plot(nd, 100 * g.dlwp_dt_pred / g.LWP, "k-", lw=1.8, label="sum (budget)")
        ax.plot(nd, 100 * g.dlwp_dt_obs / g.LWP, "kx", ms=5, label="observed trend")
        ax.axhline(0, color="0.5", lw=0.5)
        nd_axis(ax, sparse=True)
        ax.set_title(DXLAB[RESLAB[res]])
    axs[0].set_ylabel(r"$d\ln\mathrm{LWP}/dt$ contribution (% h$^{-1}$)")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=7, bbox_to_anchor=(0.5, -0.1), fontsize=6)
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.12)
    save(fig, "fig08_budget")


# ------------------------------------------------------------------ Fig 8: rain
def fig_rain():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.4), constrained_layout=True)
    sub = off[(off.sed == 1) & (off.precsupp == "on")]
    for dx in DX:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[0].plot(g.Nd_incloud, g.autoconv_col + g.accret_col, "o-", color=CDX[dx])
        axs[1].plot(g.Nd_incloud, g.evap_frac, "o-", color=CDX[dx])
        axs[2].plot(g.Nd_incloud, g.P_sfc_Wm2 / g.F_ent_moist, "o-", color=CDX[dx])
        axs[3].plot(g.Nd_incloud, g.h_cloud, "o-", color=CDX[dx])
    for ax in axs:
        nd_axis(ax, sparse=True)
    axs[0].set_yscale("log"); axs[0].set_ylim(1e-3, 3)
    axs[0].set_ylabel("rain production (mm d$^{-1}$)")
    axs[1].set_ylabel("fraction evaporated below cloud")
    axs[2].set_yscale("log"); axs[2].set_ylim(1e-5, 1.5)
    axs[2].set_ylabel("surface rain / entrainment drying")
    axs[3].set_ylabel(r"cloud thickness $z_i-z_b$ (m)")
    dx_legend(axs[3], ncol=2, fontsize=5, loc="upper right")
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "fig06_rain")


# ------------------------------------------------------------------ Fig 9: structure
def fig_structure():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.5), constrained_layout=True)
    sub = off[(off.sed == 1) & (off.precsupp == "on")]
    for nd in (20, 200, 1000):
        g = sub[sub.Nd_target == nd].sort_values("dx_km", ascending=False)
        axs[0].plot(g.dx_km, g.f_res, "o-", color=CND[nd], label=f"{nd}")
        g = g[g.dx_km <= 5]
        axs[3].plot(g.dx_km, g.lambda_peak / (g.zi / 1e3), "o-", color=CND[nd], label=f"{nd}")
    axs[3].annotate("domain-limited", (5, 52), (2.2, 48), fontsize=6, arrowprops=dict(arrowstyle="->", lw=0.5))
    axs[0].set_ylabel("resolved share of BL $w$ variance")
    axs[0].legend(title=r"$N_d$ target", fontsize=5.5, title_fontsize=6, loc="upper left")
    dx_axis(axs[0]); dx_axis(axs[3], sub=True)
    axs[3].set_ylabel(r"LWP cell scale $\lambda/z_i$")
    for dx in DX[3:]:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[1].plot(g.Nd_incloud, g.skew_w_bl, "o-", color=CDX[dx])
        axs[2].plot(g.Nd_incloud, g.dqt, "o-", color=CDX[dx])
    for dx in DX[:3]:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[2].plot(g.Nd_incloud, g.dqt, "o:", color=CDX[dx], ms=2)
    axs[1].axhline(0, color="0.5", lw=0.5)
    nd_axis(axs[1], sparse=True); nd_axis(axs[2], sparse=True)
    axs[1].set_ylabel("resolved $w$ skewness (BL)")
    axs[2].set_ylabel(r"decoupling $\Delta q_t$ (g kg$^{-1}$)")
    dx_legend(axs[1], dxs=DX[3:], fontsize=5.5, loc="upper right")
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "fig09_structure")


# ------------------------------------------------------------------ Fig 10: convergence
def fig_conv():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.5), constrained_layout=True)
    sub = off[(off.sed == 1) & (off.precsupp == "on") & (off.dx_km <= 5)]
    for nd in ND:
        g = sub[sub.Nd_target == nd].sort_values("dx_km", ascending=False)
        for ax, v in zip(axs, ("LWP", "cloud_cover", "we_812_mm_s", "h_cloud")):
            ax.plot(g.dx_km, g[v], "o-", color=CND[nd], label=f"{nd}")
    for ax, yl in zip(axs, ("LWP (g m$^{-2}$)", "cloud cover (LWP > 10 g m$^{-2}$)", r"$w_e$ (mm s$^{-1}$, 8-12 h)",
                            r"cloud thickness $z_i-z_b$ (m)")):
        dx_axis(ax, sub=True)
        ax.set_ylabel(yl)
    axs[0].legend(title=r"$N_d$ target", fontsize=5.5, title_fontsize=6, ncol=2, loc="lower left")
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "fig10_convergence")


# ------------------------------------------------------------------ Fig 11: cloud-top / satellite view
def fig_sat():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.6), constrained_layout=True)
    s = S[S.turb3d == "off"]
    ax = axs[0]
    for b, mk in zip(BR, ("o", "s", "^")):
        for dx in DX:
            g = s[s.dx_km == dx]
            ax.scatter(g[f"S_{b}"], g[f"S_{b}_top"], s=8, marker=mk, color=CDX[dx], lw=0)
    ax.plot([-0.2, 1.05], [-0.2, 1.05], color="0.5", lw=0.5)
    ax.set_xlabel(r"$S$ with in-cloud layer $N_d$")
    ax.set_ylabel(r"$S$ with cloud-top $N_d$ (AeroCom)")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker=m, color="k", label=BR[b]) for b, m in zip(BR, "os^")],
              loc="upper left")
    ax = axs[1]
    for res, nd, ls in (("2p5km", 20, "--"), ("2p5km", 200, "-"), ("312m", 20, "--"), ("312m", 200, "-")):
        d = np.load(f"{R}/manuscript/fields/fields_sedps_{res}_nd{nd}_sed1_pson.npz")
        jh, ne, le = d["jh"], d["nd_edges"], d["lwp_edges"]
        nc, lc = np.log(np.sqrt(ne[1:] * ne[:-1])), np.sqrt(le[1:] * le[:-1])
        cnt = jh.sum(0)
        mean_ln = (jh * nc[:, None]).sum(0) / np.where(cnt > 0, cnt, 1)
        ok = cnt > 0.003 * cnt.sum()
        ref = (jh * nc[:, None]).sum() / jh.sum()
        ax.plot(lc[ok], np.exp(mean_ln[ok] - ref), ls, color=CDX[RESLAB[res]], label=f"{DXLAB[RESLAB[res]]}, target {nd}")
    ax.set_xscale("log")
    ax.axhline(1, color="0.5", lw=0.5)
    ax.set_xlabel("column LWP (g m$^{-2}$)")
    ax.set_ylabel(r"mean cloud-top $N_d$ / scene mean")
    ax.legend(fontsize=5.5, loc="lower right")
    ax = axs[2]
    sub = off[(off.sed == 1) & (off.precsupp == "on")]
    for dx in DX:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        ax.plot(g.Nd_incloud, g.slope_scene, "o-", color=CDX[dx])
    ax.axhline(0, color="0.5", lw=0.5)
    nd_axis(ax)
    ax.set_ylabel(r"within-scene $d\ln\mathrm{LWP}/d\ln N_{d,top}$")
    dx_legend(ax, ncol=2, fontsize=5, loc="lower right")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.22)
    save(fig, "fig11_cloudtop")


# ------------------------------------------------------------------ Appendix figures
def fig_budget_check():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.4), constrained_layout=True)
    b = B[(B.turb3d == "off")]
    for ax, v, lab in zip(axs, ("dthl_dt", "dqt_dt", "dlwp_dt"),
                          (r"$d\theta_l/dt$ (K h$^{-1}$)", r"$dq_t/dt$ (g kg$^{-1}$ h$^{-1}$)", r"$d\mathrm{LWP}/dt$ (g m$^{-2}$ h$^{-1}$)")):
        for dx in DX:
            g = b[b.dx_km == dx]
            ax.scatter(g[f"{v}_obs"], g[f"{v}_pred"], s=4, color=CDX[dx], lw=0, alpha=0.8)
        lim = np.nanpercentile(np.abs(np.r_[b[f"{v}_obs"], b[f"{v}_pred"]]), 99.5)
        ax.plot([-lim, lim], [-lim, lim], color="0.4", lw=0.5)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        r = np.corrcoef(b[f"{v}_obs"], b[f"{v}_pred"])[0, 1]
        ax.text(0.05, 0.9, f"r = {r:.2f}", transform=ax.transAxes, fontsize=7)
        ax.set_xlabel("simulated " + lab)
        ax.set_ylabel("mixed-layer budget " + lab)
    dx_legend(axs[2], ncol=2, fontsize=5, loc="lower right")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "figA1_budget_check")


def fig_t3d():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.3), constrained_layout=True)
    on = runs[runs.turb3d == "on"]
    for _, r in on.iterrows():
        o = runs[(runs.res == r.res) & (runs.Nd_target == r.Nd_target) & (runs.sed == r.sed) & (runs.precsupp == r.precsupp)
                 & (runs.turb3d == "off")].iloc[0]
        dx = RESLAB[r.res]
        for ax, v in zip(axs, ("LWP", "cloud_cover", "we_812_mm_s")):
            ax.scatter(r.Nd_incloud * (1.05 if r.precsupp == "on" else 0.95), r[v] - o[v], s=9,
                       marker="o" if r.precsupp == "on" else "s", color=CSED[r.sed] if dx == 0.3125 else "w",
                       edgecolor=CSED[r.sed], lw=0.7)
    for ax, yl in zip(axs, (r"$\Delta$LWP (g m$^{-2}$)", r"$\Delta$cloud cover", r"$\Delta w_e$ (mm s$^{-1}$, 8-12 h)")):
        nd_axis(ax); ax.axhline(0, color="0.5", lw=0.5); ax.set_ylabel(yl)
    h = [plt.Line2D([], [], ls="", marker="o", color=CSED[s_], label=f"sed. {s_:g}") for s_ in (0.5, 1, 2)]
    h += [plt.Line2D([], [], ls="", marker="o", mfc="w", mec="k", label="625 m"),
          plt.Line2D([], [], ls="", marker="o", color="k", label="312 m"),
          plt.Line2D([], [], ls="", marker="o", color="0.5", label="supp. on"),
          plt.Line2D([], [], ls="", marker="s", color="0.5", label="supp. off")]
    axs[0].legend(handles=h, fontsize=5.5, ncol=3, loc="lower left")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "figA2_turb3d")


def fig_spectra_pdf():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.4), constrained_layout=True)
    inv = {v: k for k, v in RESLAB.items()}
    for dx in DX[3:]:
        e = np.load(f"{R}/explore/npz/explore_sedps_{inv[dx]}_nd200_sed1_pson.npz")
        k, sp = e["spec_k"], e["spec"]
        y = k * sp
        axs[0].plot(1 / k, y / y.max(), color=CDX[dx], label=DXLAB[dx])
    axs[0].set_xscale("log")
    axs[0].set_xlabel("wavelength (km)")
    axs[0].set_ylabel(r"normalised $k\,P(k)$ of LWP")
    axs[0].set_title(r"$N_d$ target 200, sed. 1, supp. on")
    axs[0].legend(fontsize=5.5)
    for ax, nd in zip(axs[1:], (20, 1000)):
        for dx in DX[3:]:
            f = np.load(f"{R}/manuscript/fields/fields_sedps_{inv[dx]}_nd{nd}_sed1_pson.npz")
            e, hst = f["lwp_edges"], f["lwp_hist"]
            c = np.sqrt(e[1:] * e[:-1])
            pdf = hst / hst.sum() / np.diff(np.log10(e))
            ax.plot(c, pdf, color=CDX[dx])
        ax.set_xscale("log")
        ax.set_xlim(1, 2000)
        ax.set_ylim(0, 1.4 if nd == 20 else 2.4)
        ax.set_xlabel("column LWP (g m$^{-2}$)")
        ax.set_ylabel(r"PDF per $\log_{10}$ LWP")
        ax.set_title(fr"$N_d$ target {nd}, hours 10-12")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.22)
    save(fig, "figA3_spectra_pdf")


if __name__ == "__main__":
    fig_maps(); fig_response(); fig_susc(); fig_time(); fig_decomp(); fig_entrain(); fig_budget()
    fig_rain(); fig_structure(); fig_conv(); fig_sat(); fig_budget_check(); fig_t3d(); fig_spectra_pdf()
