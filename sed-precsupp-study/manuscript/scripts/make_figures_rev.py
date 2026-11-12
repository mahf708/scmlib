#!/usr/bin/env python3
"""
Revised manuscript figures. Re-uses the unchanged figure functions of make_figures.py and
replaces those revised after review. `module load python; python make_figures_rev.py`
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import make_figures as mf
from make_figures import (R, T, DX, DXLAB, RESLAB, CDX, CSED, ND, CND, BR, runs, S, D, B, off,
                          label, dx_axis, nd_axis, save, W2)

MDX = {40.0: "^", 20.0: "s", 10.0: "D", 5.0: "o", 2.5: "o", 1.25: "o", 0.625: "o", 0.3125: "o"}
cc3 = pd.read_csv(f"{T}/cloudcover_3d.csv")
runs3 = runs.merge(cc3, on="case", how="left")
off3 = runs3[runs3.turb3d == "off"]


def dx_handles(dxs=DX):
    return [plt.Line2D([], [], color=CDX[d], marker=MDX[d], ms=4, label=DXLAB[d]) for d in dxs]


def fig_maps():
    cols = [5.0, 2.5, 1.25, 0.625, 0.3125]
    inv = {v: k for k, v in RESLAB.items()}
    fig, axs = plt.subplots(3, 5, figsize=(W2, 4.5), constrained_layout=True)
    for i, nd in enumerate([20, 200, 1000]):
        for j, dx in enumerate(cols):
            ax = axs[i, j]
            d = np.load(f"{R}/manuscript/fields/fields_sedps_{inv[dx]}_nd{nd}_sed1_pson.npz")
            x, y, v = d["x"] / 1e3, d["y"] / 1e3, d["lwp12"]
            xs, ys = np.unique(x), np.unique(y)
            img = np.full((ys.size, xs.size), np.nan)
            img[np.searchsorted(ys, y), np.searchsorted(xs, x)] = v
            h = (xs[1] - xs[0]) / 2
            im = ax.imshow(img, origin="lower", extent=[xs[0] - h, xs[-1] + h, ys[0] - h, ys[-1] + h],
                           cmap="cividis", vmin=0, vmax=300, interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([])
            if i == 0:
                ax.set_title(DXLAB[dx])
            if j == 0:
                ax.set_ylabel(f"target $N_d$ = {nd} cm$^{{-3}}$")
    fig.colorbar(im, ax=axs, shrink=0.6, label="LWP at 12 h (g m$^{-2}$)", extend="max")
    save(fig, "fig01_maps")


def fig_response():
    fig, axs = plt.subplots(2, 2, figsize=(W2, 5.2), constrained_layout=True)
    sub = off[off.sed == 1].sort_values("Nd_target")
    for dx in DX:
        mk = MDX[dx]
        for ps, ax in (("on", axs[0, 0]), ("off", axs[0, 1])):
            g = sub[(sub.dx_km == dx) & (sub.precsupp == ps)]
            ax.plot(g.Nd_incloud, g.LWP, "-", marker=mk, ms=4, color=CDX[dx])
            if ps == "on":
                k = g.LWP.idxmax()
                ax.plot(g.Nd_incloud[k], g.LWP[k], "*", ms=10, color=CDX[dx], mec="k", mew=0.5)
        for ps, ls, a in (("on", "-", 1.0), ("off", "--", 0.6)):
            g = sub[(sub.dx_km == dx) & (sub.precsupp == ps)]
            axs[1, 0].plot(g.Nd_incloud, g.we_812_mm_s, ls, marker=mk, ms=3 if ps == "on" else 2, color=CDX[dx], alpha=a)
            axs[1, 1].plot(g.Nd_incloud, np.clip(g.precip, 1e-4, None), ls, marker=mk, ms=3 if ps == "on" else 2, color=CDX[dx], alpha=a)
    for ax in axs.flat:
        nd_axis(ax)
    axs[0, 0].set_title("precipitation suppression on (KK2000)")
    axs[0, 1].set_title(r"precipitation suppression off ($N_d$ exponent 0)")
    for ax in axs[0]:
        ax.set_ylabel("LWP (g m$^{-2}$)")
        ax.set_ylim(30, 360)
    axs[1, 0].set_ylabel(r"$w_e$, 8-12 h (mm s$^{-1}$)")
    axs[1, 1].set_ylabel("surface precipitation (mm d$^{-1}$)")
    axs[1, 1].set_yscale("log")
    axs[1, 1].set_ylim(1e-4, 3)
    h = dx_handles() + [plt.Line2D([], [], color="k", ls="-", label="suppression on"),
                         plt.Line2D([], [], color="k", ls="--", alpha=0.6, label="suppression off")]
    fig.legend(handles=h, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.07), fontsize=6.5)
    for ax, l in zip(axs.flat, "abcd"):
        label(ax, f"({l})")
    save(fig, "fig02_response")


def fig_susc():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.7), constrained_layout=True)
    s = S[S.turb3d == "off"]
    for ax, (b, lab) in zip(axs, BR.items()):
        for sed in (0.5, 1.0, 2.0):
            for ps, ls, mk in (("on", "-", "o"), ("off", "--", "s")):
                g = s[(s.sed == sed) & (s.precsupp == ps)].sort_values("dx_km", ascending=False)
                ax.errorbar(g.dx_km * (1.06 if sed == 2 else 0.94 if sed == 0.5 else 1), g[f"S_{b}"], yerr=g[f"S_{b}_sd"],
                            color=CSED[sed], ls=ls, marker=mk, ms=3, capsize=1.5, elinewidth=0.6,
                            mfc=CSED[sed] if ps == "on" else "w")
        ax.axhline(0, color="0.5", lw=0.5)
        dx_axis(ax)
        ax.set_title(lab)
        if b == "low":
            ax.set_ylabel(r"$S = d\ln \mathrm{LWP}/d\ln N_d$")
    h = [plt.Line2D([], [], color=CSED[s_], marker="o", label=f"sedimentation factor {s_:g}") for s_ in (0.5, 1, 2)]
    h += [plt.Line2D([], [], color="k", ls="-", marker="o", label="suppression on"),
          plt.Line2D([], [], color="k", ls="--", marker="s", mfc="w", label="suppression off")]
    fig.legend(handles=h, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.1))
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.2)
    save(fig, "fig03_susceptibility")


def fig_decomp():
    """S_on(s=1) = a_off + (a_on - a_off) + b_off + (b_on - b_off), from linear fits in s."""
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.9), constrained_layout=True)
    d = D[(D.turb3d == "off") & (D.sed == 1)].set_index(["branch", "dx_km"])
    comps = [("ps0", "precipitation suppression\n(at $s\\to0$)", "#0072B2"),
             ("sed", "sedimentation\n(suppression off)", "#D55E00"),
             ("int", "interaction", "#CC79A7"),
             ("res", "residual", "#999999")]
    x = np.arange(len(DX))
    for ax, (b, lab) in zip(axs, BR.items()):
        g = d.loc[b].loc[DX]
        vals = {"ps0": g.S_on_sed0 - g.S_resid, "sed": g.dS_dsed_off, "int": g.dS_dsed_on - g.dS_dsed_off, "res": g.S_resid}
        for k, (c, cl, col) in enumerate(comps):
            ax.bar(x + (k - 1.5) * 0.2, vals[c], width=0.19, color=col, label=cl, edgecolor="w", lw=0.3)
        ax.plot(x, g.S_on, "k_", ms=10, mew=1.5, label=r"total $S_{on}$")
        ax.axhline(0, color="0.3", lw=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels([DXLAB[v] for v in DX], rotation=45, ha="right")
        ax.set_title(lab)
        label(ax, f"({'abc'[list(BR).index(b)]})", x=-0.2)
    axs[0].set_ylabel("contribution to $S$ ($s=1$)")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.12), fontsize=6.5)
    save(fig, "fig05_decomposition")


def fig_entrain():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.7), constrained_layout=True)
    w = pd.read_csv(f"{T}/dwe_sed.csv")
    for dx in DX:
        g = w[(w.dx_km == dx) & (w.precsupp == "on")].sort_values("Nd_target")
        axs[0].plot(g.Nd_incloud, g.dwe_sed, "-", marker=MDX[dx], ms=3, color=CDX[dx])
    nd_axis(axs[0], sparse=True)
    axs[0].axhline(0, color="0.5", lw=0.5)
    axs[0].set_ylabel(r"$w_e(s=2)-w_e(s=0.5)$ (mm s$^{-1}$)")
    sub = off[(off.sed == 1) & (off.precsupp == "on")]
    for dx in DX:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[1].plot(g.Nd_incloud, g.eta_ent, "-", marker=MDX[dx], ms=3, color=CDX[dx])
        axs[2].plot(g.Nd_incloud, g.F_ent_moist, "-", marker=MDX[dx], ms=3, color=CDX[dx])
    nd_axis(axs[1], sparse=True); nd_axis(axs[2], sparse=True)
    axs[1].axhline(1, color="0.5", lw=0.5, ls=":")
    axs[1].set_ylabel(r"$\eta=\rho c_p w_e\Delta\theta_l / F_\mathrm{rad}$")
    axs[2].axhline(93, color="0.5", lw=0.5, ls=":")
    axs[2].text(250, 86, "prescribed LHF", fontsize=6, color="0.4")
    axs[2].set_ylabel(r"$-\rho L_v w_e \Delta q_t$ (W m$^{-2}$)")
    fig.legend(handles=dx_handles(), loc="lower center", ncol=8, bbox_to_anchor=(0.5, -0.08), fontsize=6.5)
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.3)
    save(fig, "fig07_entrainment")


TERMS = [("ent", "entrainment", "#D55E00"), ("subs", "subsidence", "#CC79A7"), ("rad", "radiative cooling", "#0072B2"),
         ("sfc", "surface fluxes", "#009E73"), ("precip", "precipitation", "#56B4E9")]


def fig_budget():
    sk = pd.read_csv(f"{T}/budget_skill.csv").set_index("dx_km")
    fig, axs = plt.subplots(2, 3, figsize=(W2, 4.6), constrained_layout=True, sharey=True)
    b = B[(B.turb3d == "off") & (B.t_end == 12) & (B.sed == 1) & (B.precsupp == "on")]
    for ax, res in zip(axs.flat, ("40km", "5km", "2p5km", "1p25km", "625m", "312m")):
        g = b[b.res == res].sort_values("Nd_target")
        nd = runs.set_index("case").loc[g.case, "Nd_incloud"].values
        for k, lab, col in TERMS:
            ax.plot(nd, 100 * g[f"dlwp_{k}"] / g.LWP, "o-", color=col, label=lab, ms=2.5)
        tot = 100 * g.dlwp_dt_pred / g.LWP
        err = 100 * sk.loc[RESLAB[res], "rmse_raw"] / g.LWP
        ax.fill_between(nd, tot - err, tot + err, color="k", alpha=0.12, lw=0)
        ax.plot(nd, tot, "k-", lw=1.6, label="sum (budget)")
        ax.plot(nd, 100 * g.dlwp_dt_obs / g.LWP, "kx", ms=5, label="simulated trend")
        ax.axhline(0, color="0.5", lw=0.5)
        nd_axis(ax, sparse=True)
        ax.set_title(DXLAB[RESLAB[res]])
    for ax in axs[:, 0]:
        ax.set_ylabel(r"contribution to $d\ln\mathrm{LWP}/dt$ (% h$^{-1}$)")
    h, l = axs[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=7, bbox_to_anchor=(0.5, -0.05), fontsize=6.5)
    for ax, l in zip(axs.flat, "abcdef"):
        label(ax, f"({l})", x=-0.12)
    save(fig, "fig08_budget")


def fig_structure():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.6), constrained_layout=True)
    sub = off[(off.sed == 1) & (off.precsupp == "on")]
    for nd in (20, 200, 1000):
        g = sub[sub.Nd_target == nd].sort_values("dx_km", ascending=False)
        axs[0].plot(g.dx_km, g.f_res, "o-", color=CND[nd], label=f"{nd}")
        g = g[g.dx_km <= 5]
        axs[3].plot(g.dx_km, g.lambda_peak / (g.zi / 1e3), "o-", color=CND[nd], label=f"{nd}")
    axs[0].set_ylabel("resolved share of BL $w$ variance")
    axs[0].legend(title=r"target $N_d$", fontsize=5.5, title_fontsize=6, loc="upper left")
    dx_axis(axs[0]); dx_axis(axs[3], sub=True)
    axs[3].set_ylabel(r"LWP spectral peak $\lambda/z_i$")
    for dx in DX[3:]:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[1].plot(g.Nd_incloud, g.skew_w_bl, "o-", color=CDX[dx], ms=3)
        axs[2].plot(g.Nd_incloud, g.dqt, "o-", color=CDX[dx], ms=3)
    for dx in DX[:3]:
        g = sub[sub.dx_km == dx].sort_values("Nd_target")
        axs[2].plot(g.Nd_incloud, g.dqt, ":", marker=MDX[dx], color=CDX[dx], ms=2)
    axs[1].axhline(0, color="0.5", lw=0.5)
    nd_axis(axs[1], sparse=True); nd_axis(axs[2], sparse=True)
    axs[1].set_ylabel("resolved $w$ skewness (BL)")
    axs[2].set_ylabel(r"decoupling $\Delta q_t$ (g kg$^{-1}$)")
    fig.legend(handles=dx_handles(), loc="lower center", ncol=8, bbox_to_anchor=(0.5, -0.08), fontsize=6.5)
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.3)
    save(fig, "fig09_structure")


def fig_conv():
    """Bulk quantities against dx at fixed diagnosed in-cloud Nd (interpolated in ln Nd)."""
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.6), constrained_layout=True)
    sub = off3[(off3.sed == 1) & (off3.precsupp == "on") & (off3.dx_km <= 5)]
    targets = [30, 50, 100, 200, 500]
    cols = {n: c for n, c in zip(targets, plt.cm.magma(np.linspace(0.12, 0.78, 5)))}
    for nd in targets:
        for ax, v in zip(axs, ("LWP", "cc_max", "we_812_mm_s", "h_cloud")):
            xs, ys = [], []
            for dx in DX[3:]:
                g = sub[sub.dx_km == dx].sort_values("Nd_incloud")
                val = np.interp(np.log(nd), np.log(g.Nd_incloud), g[v], left=np.nan, right=np.nan)
                xs.append(dx); ys.append(val)
            ax.plot(xs, ys, "o-", color=cols[nd], label=f"{nd}")
    for ax, yl in zip(axs, ("LWP (g m$^{-2}$)", "cloud cover (max. overlap)", r"$w_e$, 8-12 h (mm s$^{-1}$)",
                            r"cloud thickness $z_i-z_b$ (m)")):
        dx_axis(ax, sub=True)
        ax.set_ylabel(yl)
    axs[0].legend(title=r"in-cloud $N_d$ (cm$^{-3}$)", fontsize=5.5, title_fontsize=6, ncol=2, loc="lower left")
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.3)
    save(fig, "fig10_convergence")


def fig_sat():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.7), constrained_layout=True)
    s = S[S.turb3d == "off"]
    ax = axs[0]
    for b, mk in zip(BR, ("o", "s", "^")):
        for dx in DX:
            g = s[s.dx_km == dx]
            ax.scatter(g[f"S_{b}"], g[f"S_{b}_top"], s=8, marker=mk, color=CDX[dx], lw=0)
    ax.plot([-0.2, 1.05], [-0.2, 1.05], color="0.5", lw=0.5)
    ax.set_xlabel(r"$S$ with in-cloud layer $N_d$")
    ax.set_ylabel(r"$S$ with cloud-top $N_d$")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker=m, color="k", label=BR[b]) for b, m in zip(BR, "os^")], loc="upper left")
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
    sc = pd.read_csv(f"{T}/scene_se.csv")
    sc = sc[(sc.sed == 1) & (sc.precsupp == "on")]
    for dx in DX[3:]:
        g = sc[sc.dx_km == dx].sort_values("Nd_target")
        ax.errorbar(g.Nd_incloud, g.slope, yerr=g.se, fmt="o-", ms=3, capsize=1.5, elinewidth=0.6, color=CDX[dx], label=DXLAB[dx])
    ax.axhline(0, color="0.5", lw=0.5)
    nd_axis(ax, sparse=True)
    ax.set_ylabel(r"within-scene $d\ln\mathrm{LWP}/d\ln N_{d,top}$")
    ax.legend(fontsize=5.5, loc="lower right")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "fig11_cloudtop")


def fig_budget_check():
    b = B[B.turb3d == "off"].copy()
    key = ["dx_km", "sed", "precsupp", "t_end"]
    for v in ("pred", "obs"):
        b[f"a_{v}"] = b[f"dlwp_dt_{v}"] - b.groupby(key)[f"dlwp_dt_{v}"].transform("mean")
    fig, axs = plt.subplots(2, 3, figsize=(W2, 4.6), constrained_layout=True)
    for ax, dx in zip(axs.flat, (40.0, 5.0, 2.5, 1.25, 0.625, 0.3125)):
        g = b[b.dx_km == dx]
        sc = ax.scatter(g.a_obs, g.a_pred, s=5, c=g.t_end, cmap="viridis", vmin=4, vmax=12, lw=0)
        lim = np.nanpercentile(np.abs(np.r_[g.a_obs, g.a_pred]), 99)
        ax.plot([-lim, lim], [-lim, lim], color="0.4", lw=0.5)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        r_raw = np.corrcoef(g.dlwp_dt_obs, g.dlwp_dt_pred)[0, 1]
        r_an = np.corrcoef(g.a_obs, g.a_pred)[0, 1]
        ax.text(0.04, 0.96, f"r (raw) = {r_raw:.2f}\nr ($N_d$ anomaly) = {r_an:.2f}", transform=ax.transAxes, fontsize=6, va="top")
        ax.set_title(DXLAB[dx])
        ax.set_xlabel(r"simulated $N_d$ anomaly (g m$^{-2}$ h$^{-1}$)")
        ax.set_ylabel(r"budget $N_d$ anomaly (g m$^{-2}$ h$^{-1}$)")
    fig.colorbar(sc, ax=axs, shrink=0.5, label="end of 2-h window (h)")
    for ax, l in zip(axs.flat, "abcdef"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "figA1_budget_check")


def fig_spectra_pdf():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.5), constrained_layout=True)
    inv = {v: k for k, v in RESLAB.items()}
    for dx in DX[3:]:
        e = np.load(f"{R}/explore/npz/explore_sedps_{inv[dx]}_nd200_sed1_pson.npz")
        k, sp = e["spec_k"], e["spec"]
        y = k * sp
        axs[0].plot(1 / k, y / y.max(), color=CDX[dx], label=DXLAB[dx])
    axs[0].set_xscale("log")
    axs[0].set_xlabel("wavelength (km)")
    axs[0].set_ylabel(r"normalised $k\,P(k)$ of LWP")
    for ax, nd in zip(axs[1:], (20, 1000)):
        for dx in DX[3:]:
            f = np.load(f"{R}/manuscript/fields/fields_sedps_{inv[dx]}_nd{nd}_sed1_pson.npz")
            e, hst = f["lwp_edges"], f["lwp_hist"]
            c = np.sqrt(e[1:] * e[:-1])
            ax.plot(c, hst / hst.sum() / np.diff(np.log10(e)), color=CDX[dx], label=DXLAB[dx])
        ax.set_xscale("log"); ax.set_xlim(1, 2000)
        ax.set_ylim(0, 1.4 if nd == 20 else 2.4)
        ax.set_xlabel("column LWP (g m$^{-2}$)")
        ax.set_ylabel(r"PDF per $\log_{10}$ LWP")
    for ax in axs:
        ax.legend(fontsize=5.5, loc="upper left")
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "figA3_spectra_pdf")


def fig_shocmix():
    m = pd.read_csv(f"{T}/shocmix.csv")
    fig, axs = plt.subplots(1, 2, figsize=(W2 * 0.75, 2.8), constrained_layout=True)
    for dx in DX:
        g = m[m.dx_km == dx]
        g = g[g.z_zi < 1.2]
        axs[0].plot(g.shoc_mix, g.z_zi, "-", color=CDX[dx], label=DXLAB[dx])
        if dx <= 1.25:
            axs[0].axvline(dx * 1000, color=CDX[dx], ls=":", lw=0.8)
        axs[1].plot(g.nd_incloud_cm3, g.z, "-", color=CDX[dx], label=DXLAB[dx])
    g = m[m.dx_km == 40.0]
    axs[1].plot(g.nd_floor_cm3, g.z, "k--", lw=1, label="activation floor")
    axs[0].set_xlabel("SHOC mixing length (m)"); axs[0].set_ylabel(r"$z/z_i$")
    axs[0].set_xlim(0, 1700)
    axs[1].set_xlabel(r"in-cloud $N_d$ (cm$^{-3}$)"); axs[1].set_ylabel("height (m)")
    axs[1].set_ylim(0, 1200); axs[1].set_xlim(0, 600)
    axs[1].legend(fontsize=5.5, loc="upper right")
    for ax, l in zip(axs, "ab"):
        label(ax, f"({l})", x=-0.2)
    save(fig, "figA4_shocmix_nd")


if __name__ == "__main__":
    fig_maps(); fig_response(); fig_susc(); mf.fig_time(); fig_decomp(); mf.fig_rain(); fig_entrain(); fig_budget()
    fig_structure(); fig_conv(); fig_sat(); fig_budget_check(); mf.fig_t3d(); fig_spectra_pdf(); fig_shocmix()
