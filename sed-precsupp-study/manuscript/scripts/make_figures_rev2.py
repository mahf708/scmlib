#!/usr/bin/env python3
"""Figures of the second revision. `module load python; python make_figures_rev2.py`"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import make_figures as mf
import make_figures_rev as mr
from make_figures import (R, T, DX, DXLAB, RESLAB, CDX, CSED, ND, CND, runs, off, label, dx_axis, save, W2)
from make_figures_rev import MDX, dx_handles

BT = pd.read_csv(f"{T}/rev2_branch.csv")
D3 = pd.read_csv(f"{T}/rev2_d3.csv")
DEC = pd.read_csv(f"{T}/rev2_decoup.csv").merge(off[["case", "dx_km", "Nd_target", "sed", "precsupp", "cdnc_top_cm3"]], on="case")
ETA = pd.read_csv(f"{T}/rev2_eta.csv")
TW = pd.read_csv(f"{T}/rev2_twins.csv")
TL = pd.read_csv(f"{T}/rev2_tiles.csv")
BRL = {"low": r"$S_{20\to50}$", "mid": r"$S_{50\to100}$", "high": r"$S_{100\to200}$", "vhigh": r"$S_{200\to1000}$"}
off3 = mr.off3


def ndtop_axis(ax, sparse=False):
    ax.set_xscale("log")
    t = [20, 100, 1000] if sparse else [20, 50, 100, 200, 500, 1000]
    ax.set_xticks(t); ax.set_xticklabels([str(v) for v in t]); ax.minorticks_off()
    ax.set_xlabel(r"cloud-top $N_d$ (cm$^{-3}$)")


def fig_meanstate():
    fig, axs = plt.subplots(2, 3, figsize=(W2, 4.8), constrained_layout=True)
    s = off3[(off3.sed == 1) & (off3.precsupp == "on")]
    d = D3[(D3.sed == 1) & (D3.precsupp == "on")]
    dc = DEC[(DEC.sed == 1) & (DEC.precsupp == "on")]
    e = ETA[(ETA.sed == 1) & (ETA.precsupp == "on")]
    for nd in (20, 200, 1000):
        g = s[s.Nd_target == nd].sort_values("dx_km", ascending=False)
        axs[0, 0].plot(g.dx_km, g.LWP, "o-", color=CND[nd], label=f"{nd}")
        axs[0, 1].plot(g.dx_km, g.zi, "o-", color=CND[nd]); axs[0, 1].plot(g.dx_km, g.zb, "s--", color=CND[nd], mfc="w")
        h = dc[dc.Nd_target == nd].sort_values("dx_km", ascending=False)
        axs[0, 2].plot(g.dx_km, g.we_812_mm_s, "o-", color=CND[nd])
        axs[1, 0].plot(h.dx_km, h.A_eff, "o-", color=CND[nd])
        ee = e[e.Nd_target == nd].sort_values("dx_km", ascending=False)
        axs[1, 0].plot(ee.dx_km, ee.eta_interface, "s:", color=CND[nd], mfc="w")
        k = d[d.Nd_target == nd].sort_values("dx_km", ascending=False)
        axs[1, 1].plot(g.dx_km, g.f_res, "o-", color=CND[nd])
        axs[1, 1].plot(k.dx_km[k.dx_km <= 10], k.frac_w_small[k.dx_km <= 10], "s:", color=CND[nd], mfc="w")
        k5 = k[k.dx_km <= 5]
        axs[1, 2].plot(k5.dx_km, k5.resid_frac50, "o-", color=CND[nd])
        axs[1, 2].plot(k5.dx_km, k5.sig_ztop / 50.0, "s:", color=CND[nd], mfc="w")
    axs[0, 0].set_ylabel("LWP (g m$^{-2}$)")
    axs[0, 0].legend(title=r"target $N_d$", fontsize=5.5, title_fontsize=6)
    axs[0, 1].set_ylabel(r"$z_i$ (solid), $z_b$ (dashed) (m)")
    axs[0, 2].axhspan(6.0, 7.6, color="0.85", lw=0); axs[0, 2].text(30, 6.2, "RF02 obs.", fontsize=6, color="0.4")
    axs[0, 2].set_ylabel(r"$w_e$, 8-12 h (mm s$^{-1}$)")
    axs[1, 0].set_ylabel(r"$A$ (solid), $\eta_{int}$ (dotted)")
    axs[1, 0].axhspan(0.53, 0.68, color="0.85", lw=0)
    axs[1, 1].set_ylabel("resolved share (solid),\nnear-grid share (dotted)")
    axs[1, 2].set_ylabel("implicit fraction (solid),\n" r"$\sigma(z_{top})/\Delta z$ (dotted)")
    for ax in axs.flat:
        dx_axis(ax, sub=ax is axs[1, 2])
    for ax, l in zip(axs.flat, "abcdef"):
        label(ax, f"({l})", x=-0.3)
    save(fig, "fig02_meanstate")


def fig_response():
    fig, axs = plt.subplots(2, 2, figsize=(W2, 5.0), constrained_layout=True)
    sub = off3[off3.sed == 1].sort_values("Nd_target")
    for dx in DX:
        for ps, ax in (("on", axs[0, 0]), ("off", axs[0, 1])):
            g = sub[(sub.dx_km == dx) & (sub.precsupp == ps)]
            ax.plot(g.cdnc_top_cm3, g.LWP, "-", marker=MDX[dx], ms=3.5, color=CDX[dx])
        g = sub[(sub.dx_km == dx) & (sub.precsupp == "on")]
        axs[1, 0].plot(g.cdnc_top_cm3, g.LWP / g.cc_max, "-", marker=MDX[dx], ms=3.5, color=CDX[dx])
        axs[1, 1].plot(g.cdnc_top_cm3, g.cc_max, "-", marker=MDX[dx], ms=3.5, color=CDX[dx])
    for ax in axs.flat:
        ndtop_axis(ax)
    axs[0, 0].set_title("autoconversion with $N_d$ dependence"); axs[0, 1].set_title(r"$N_d$-independent autoconversion")
    for ax in axs[0]:
        ax.set_ylabel("domain-mean LWP (g m$^{-2}$)"); ax.set_ylim(30, 360)
    axs[1, 0].set_ylabel(r"in-cloud LWP (g m$^{-2}$)"); axs[1, 1].set_ylabel("cloud cover (max. overlap)")
    fig.legend(handles=dx_handles(), loc="lower center", ncol=8, bbox_to_anchor=(0.5, -0.05), fontsize=6.5)
    for ax, l in zip(axs.flat, "abcd"):
        label(ax, f"({l})")
    save(fig, "fig03_response")


def fig_Scomp():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.7), constrained_layout=True)
    b = BT[(BT.turb3d == "off") & (BT.sed == 1) & (BT.precsupp == "on")]
    tl = TL[(TL.sed == 1) & (TL.ps == "on")]
    for ax, br in zip(axs, ("low", "mid", "high", "vhigh")):
        g = b[b.branch == br].set_index("dx_km").loc[DX]
        ax.plot(DX, g.S_top, "ko-", label="all-sky", ms=3.5)
        ax.plot(DX, g.S_ic_max, "o--", color="#0072B2", label="in-cloud", ms=3)
        ax.plot(DX, g.S_cf_max, "s:", color="#D55E00", label="cloud cover", ms=3)
        t = tl[tl.branch == br].set_index("dx_km")
        if len(t):
            ax.errorbar(t.index, t.S_top, yerr=[t.S_top - t.p05, t.p95 - t.S_top], fmt="none", ecolor="k", elinewidth=0.8, capsize=2)
        ax.axhline(0, color="0.5", lw=0.5)
        dx_axis(ax); ax.set_title(BRL[br])
    axs[0].set_ylabel(r"$S$ (cloud-top $N_d$)")
    axs[0].legend(fontsize=6)
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "fig04_Scomponents")


def fig_time():
    st = pd.read_csv(f"{T}/rev2_S_t.csv")
    pk = pd.read_csv(f"{T}/rev2_peak.csv")
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.6), constrained_layout=True)
    x = st[(st.sed == 1) & (st.ps == "on")]
    for k, br in enumerate(("high", "vhigh")):
        for dx in DX:
            g = x[(x.dx_km == dx) & (x.branch == br)].sort_values("t")
            axs[k].plot(g.t, g.S.rolling(8, min_periods=4, center=True).mean(), "-", color=CDX[dx], lw=1)
        axs[k].axhline(0, color="0.5", lw=0.5); axs[k].set_xlabel("time (h)"); axs[k].set_title(BRL[br], pad=8)
        axs[k].set_xticks([0, 4, 8, 12])
    axs[0].set_ylabel(r"$S$ (cloud-top $N_d$)")
    p = pk[(pk.sed == 1) & (pk.ps == "on")]
    for dx in DX:
        g = p[p.dx_km == dx].sort_values("t")
        axs[2].plot(g.t, g.Nd_peak.rolling(8, min_periods=4, center=True).median(), "-", color=CDX[dx])
    axs[2].set_yscale("log"); axs[2].set_ylabel(r"cloud-top $N_d$ of max. LWP (cm$^{-3}$)"); axs[2].set_xlabel("time (h)")
    axs[2].set_xticks([0, 4, 8, 12])
    ts = mf.pd.read_csv(f"{R}/analysis_report5/timeseries_15min.csv")
    for nd in ND:
        g = ts[(ts.res == "312m") & (ts.Nd_target == nd) & (ts.sed_factor == 1) & (ts.precip_suppression == "on") & (ts.turb3d == "off")].dropna(subset=["LWP_gm2"]).sort_values("time_h")
        g = g[g.time_h >= 4]
        L = g.LWP_gm2.rolling(4, center=True, min_periods=2).mean().values
        dL = np.gradient(L, g.time_h.values)
        axs[3].plot(L, dL, "-", color=CND[nd], lw=1, label=f"{nd}")
        axs[3].plot(L[-1], dL[-1], "o", color=CND[nd], ms=3)
    axs[3].axhline(0, color="0.5", lw=0.5)
    axs[3].set_xlabel("LWP (g m$^{-2}$)"); axs[3].set_ylabel(r"$d$LWP$/dt$ (g m$^{-2}$ h$^{-1}$)"); axs[3].set_title("312 m, 4-12 h")
    axs[3].legend(fontsize=5, title=r"target $N_d$", title_fontsize=5.5)
    fig.legend(handles=dx_handles(), loc="lower center", ncol=8, bbox_to_anchor=(0.4, -0.08), fontsize=6)
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.28)
    save(fig, "fig05_time")


def fig_regime():
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.7), constrained_layout=True)
    b = BT[(BT.turb3d == "off")]
    for ax, br in zip(axs, ("mid", "high", "vhigh")):
        for ps, mk in (("on", "o"), ("off", "s")):
            for dx in DX:
                g = b[(b.branch == br) & (b.precsupp == ps) & (b.dx_km == dx)]
                ax.scatter(np.clip(g.ratio_P_Fent, 1e-5, None), g.S_top, s=14, marker=mk, color=CDX[dx],
                           edgecolor="k" if ps == "on" else CDX[dx], lw=0.3, facecolor=CDX[dx] if ps == "on" else "w")
        g = b[(b.branch == br) & (b.precsupp == "on")]
        r = np.corrcoef(np.log(np.clip(g.ratio_P_Fent, 1e-5, None)), g.S_top)[0, 1]
        ax.text(0.04, 0.93, f"r = {r:.2f} (on)", transform=ax.transAxes, fontsize=6.5)
        ax.set_xscale("log"); ax.axhline(0, color="0.5", lw=0.5)
        ax.set_xlabel(r"$P_\mathrm{sfc}/F_\mathrm{ent,q}$ of the lower-$N_d$ run"); ax.set_title(BRL[br])
    axs[0].set_ylabel(r"$S$ (cloud-top $N_d$)")
    h = dx_handles() + [plt.Line2D([], [], ls="", marker="o", color="0.4", label="$N_d$-dep. autoconv."),
                         plt.Line2D([], [], ls="", marker="s", mfc="w", color="0.4", label="$N_d$-indep. autoconv.")]
    fig.legend(handles=h, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.13), fontsize=6)
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.22)
    save(fig, "fig06_regime")


def fig_entrain():
    sf = pd.read_csv(f"{T}/rev2_sedflux.csv")
    oo = pd.read_csv(f"{T}/rev2_onoff.csv")
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.7), constrained_layout=True)
    for dx in DX:
        g = sf[(sf.dx_km == dx) & (sf.precsupp == "on")]
        hi = g[g.Nd_target >= 200]; lo = g[g.Nd_target <= 50]
        axs[0].scatter(hi.dF, hi.dwe, s=14, color=CDX[dx], marker=MDX[dx], edgecolor="k", lw=0.3)
        axs[0].scatter(lo.dF, lo.dwe, s=14, color="w", marker=MDX[dx], edgecolor=CDX[dx], lw=0.8)
        o = oo[(oo.dx_km == dx) & (oo.sed == 1)].sort_values("Nd_target")
        axs[1].plot(o.Nd_target, o.d_we, "-", marker=MDX[dx], ms=3, color=CDX[dx])
    axs[0].axhline(0, color="0.5", lw=0.5)
    axs[0].set_xlabel(r"$\Delta F_\mathrm{sed}$ at cloud top, $s=2$ vs 0.5 (mm d$^{-1}$)")
    axs[0].set_ylabel(r"$\Delta w_e$ (mm s$^{-1}$)")
    axs[0].text(0.03, 0.04, "filled: target $N_d\\geq200$\nopen: target $N_d\\leq50$", transform=axs[0].transAxes, fontsize=5.5)
    axs[1].axhline(0, color="0.5", lw=0.5); mf.nd_axis(axs[1], sparse=True); axs[1].set_xlabel(r"target $N_d$ (cm$^{-3}$)")
    axs[1].set_ylabel(r"$w_e$(dep.) $-$ $w_e$(indep.) (mm s$^{-1}$)")
    e = ETA[(ETA.sed == 1) & (ETA.precsupp == "on") & (ETA.Nd_target == 200)].sort_values("dx_km", ascending=False)
    for col, lab, ls in (("eta_50", "+50 m", "-"), ("eta_100", "+100 m", "--"), ("eta_150", "+150 m", "-."), ("eta_interface", "interface (6.7 K)", ":")):
        axs[2].plot(e.dx_km, e[col], ls, marker="o", ms=3, color="k", label=lab)
    axs[2].plot(e.dx_km, e.eta_steady_ref, "-", color="#D55E00", label="steady reference")
    axs[2].axhspan(0.53, 0.68, color="0.85", lw=0); axs[2].text(30, 0.62, "obs. (interface)", fontsize=5.5, color="0.4")
    dx_axis(axs[2]); axs[2].set_ylabel(r"$\eta$ (target $N_d$ = 200)"); axs[2].legend(fontsize=5.5, loc="upper left")
    fig.legend(handles=dx_handles(), loc="lower center", ncol=8, bbox_to_anchor=(0.5, -0.08), fontsize=6)
    for ax, l in zip(axs, "abc"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "fig08_entrainment")


def fig_budget2():
    b2 = pd.read_csv(f"{T}/rev2_budget2.csv")
    sk = []
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.7), constrained_layout=True, sharey=True)
    terms = [("t_ent_zi", "entrainment ($z_i$)", "#E69F00"), ("t_ent_zb", "entrainment ($z_b$)", "#D55E00"),
             ("t_subs", "subsidence", "#CC79A7"), ("t_rad", "radiation", "#0072B2"), ("t_sfc", "surface fluxes", "#009E73"),
             ("t_precip", "precipitation", "#56B4E9")]
    x = b2[(b2.t_end == 12) & (b2.sed == 1) & (b2.precsupp == "on")]
    for ax, dx in zip(axs, (40.0, 5.0, 2.5, 0.3125)):
        g = x[x.dx_km == dx].sort_values("Nd_target")
        for k, lab, col in terms:
            ax.plot(g.Nd_target, g[k], "o-", color=col, label=lab, ms=2.5)
        ax.plot(g.Nd_target, g.dlnLWPic_pred, "k-", lw=1.6, label="sum (in-cloud LWP)")
        ax.plot(g.Nd_target, g.dlnLWPic_obs, "kx", ms=5, label="simulated in-cloud trend")
        ax.plot(g.Nd_target, g.dlncc_obs, "^", color="0.5", ms=4, label="simulated cloud-cover trend")
        dec = g[~g.coupled]
        ax.plot(dec.Nd_target, np.full(len(dec), -48), "|", color="r", ms=8, mew=1.5)
        ax.axhline(0, color="0.5", lw=0.5); mf.nd_axis(ax, sparse=True); ax.set_xlabel(r"target $N_d$ (cm$^{-3}$)")
        ax.set_title(DXLAB[dx])
    axs[0].set_ylabel(r"contribution (% h$^{-1}$)")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.16), fontsize=6)
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.12)
    save(fig, "fig09_budget")


def fig_decoup():
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.6), constrained_layout=True)
    d = DEC[DEC.sed == 1]
    B = pd.read_csv(f"{T}/ml_budget.csv")
    b = B[(B.t_end == 12) & (B.turb3d == "off") & (B.sed == 1)]
    for dx in DX:
        g = d[(d.dx_km == dx)]
        axs[0].scatter(g.dqt_J, g.dthl_J, s=10, color=CDX[dx], marker=MDX[dx], lw=0)
        g = d[(d.dx_km == dx) & (d.precsupp == "on")].sort_values("Nd_target")
        axs[1].plot(g.Nd_target, g.Bmin_below_zb_rel, "-", marker=MDX[dx], ms=3, color=CDX[dx])
        axs[3].plot(g.Nd_target, g.w2_cloud_over_sub, "-", marker=MDX[dx], ms=3, color=CDX[dx])
        h = b[(b.dx_km == dx) & (b.precsupp == "on")].sort_values("Nd_target")
        axs[2].plot(h.Nd_target, h.zb - h.lcl_ml, "-", marker=MDX[dx], ms=3, color=CDX[dx])
    axs[0].axvline(0.5, color="0.5", lw=0.5, ls="--"); axs[0].axhline(0.5, color="0.5", lw=0.5, ls="--")
    axs[0].set_xlabel(r"$\Delta q_t$ (g kg$^{-1}$)"); axs[0].set_ylabel(r"$\Delta\theta_l$ (K)")
    axs[1].set_ylabel("min. buoyancy flux below $z_b$ / surface")
    axs[2].set_ylabel(r"$z_b-z_\mathrm{LCL,ml}$ (m)"); axs[2].axhline(50, color="0.5", lw=0.5, ls="--")
    axs[3].set_ylabel(r"$\overline{w'^2}$ cloud layer / subcloud")
    for ax in axs[1:]:
        mf.nd_axis(ax, sparse=True); ax.set_xlabel(r"target $N_d$ (cm$^{-3}$)")
    fig.legend(handles=dx_handles(), loc="lower center", ncol=8, bbox_to_anchor=(0.5, -0.08), fontsize=6)
    for ax, l in zip(axs, "abcd"):
        label(ax, f"({l})", x=-0.3)
    save(fig, "fig10_decoupling")


def fig_sat():
    sat = pd.read_csv(f"{T}/rev2_sat.csv")
    fig, axs = plt.subplots(1, 2, figsize=(W2 * 0.7, 2.6), constrained_layout=True)
    b = BT[(BT.turb3d == "off") & (BT.sed == 1) & (BT.precsupp == "on")]
    x = sat[(sat.sed == 1) & (sat.ps == "on")]
    dxs = [5.0, 2.5, 1.25, 0.625, 0.3125]
    for kind, lab, mk in (("top_f2", "pooled, cloud-top $N_d$", "o"), ("ret_f2", "pooled, retrieval-like $N_d$", "s"),
                          ("ret_c4", "pooled, retrieval-like, 3.75 km", "^")):
        g = x[x.kind == kind].set_index("dx_km").reindex(dxs)
        axs[0].plot(dxs, g.slope_pooled, "-", marker=mk, ms=3.5, label=lab)
        if kind != "ret_c4":
            axs[1].plot(dxs, g.frac_var_within, "-", marker=mk, ms=3.5, label=lab)
    g = x[x.kind == "ret_f2"].set_index("dx_km").reindex(dxs)
    axs[0].plot(dxs, g.slope_between, "--", color="0.4", label="between runs, retrieval-like $N_d$")
    fitall = []
    for dx in dxs:
        o = off3[(off3.dx_km == dx) & (off3.sed == 1) & (off3.precsupp == "on")]
        fitall.append(np.polyfit(np.log(o.cdnc_top_cm3), np.log(o.LWP / o.cloud_cover), 1)[0])
    axs[0].plot(dxs, fitall, "k-", lw=1.5, label="causal (in-cloud LWP, all $N_d$)")
    axs[0].axhline(0, color="0.5", lw=0.5); dx_axis(axs[0], sub=True); dx_axis(axs[1], sub=True)
    axs[0].set_ylabel(r"$d\ln\mathrm{LWP}/d\ln N_d$"); axs[1].set_ylabel(r"within-scene share of $\ln N_d$ variance")
    axs[0].legend(fontsize=5, loc="upper right")
    for ax, l in zip(axs, "ab"):
        label(ax, f"({l})", x=-0.25)
    save(fig, "figA6_satellite")


REMAP = {"fig06_rain": "fig07_rain", "fig05_decomposition": "figA1_decomposition", "figA1_budget_check": "figA2_budget_check",
         "figA4_shocmix_nd": "figA3_shocmix_nd", "figA2_turb3d": "figA4_turb3d", "figA3_spectra_pdf": "figA5_spectra_pdf"}
_orig_save = mf.save


def _save(fig, name):
    _orig_save(fig, REMAP.get(name, name))


mf.save = _save
mr.save = _save
save = _save

if __name__ == "__main__":
    mr.fig_maps(); fig_meanstate(); fig_response(); fig_Scomp(); fig_time(); fig_regime()
    mf.fig_rain(); fig_entrain(); fig_budget2(); fig_decoup()
    mr.fig_decomp(); mr.fig_budget_check(); mr.fig_shocmix(); mf.fig_t3d(); mr.fig_spectra_pdf(); fig_sat()
