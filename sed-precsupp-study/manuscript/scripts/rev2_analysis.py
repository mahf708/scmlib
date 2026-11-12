#!/usr/bin/env python3
"""
Revision-2 analyses that use only the per-run tables, time series and npz reductions (login node).

Outputs (manuscript/tables/rev2_*.csv):
  rev2_branch.csv     one row per (dx, s, suppression, branch): S with layer, cloud-top and target Nd;
                      in-cloud and cloud-fraction parts (two cover definitions); d ln tau/d ln Nd;
                      offline albedo split; precipitation susceptibility; base-state predictors of the
                      lower-Nd run (rain/entrainment-drying ratio, LWP, h, z_b, P_sfc, eta)
  rev2_regime.csv     regressions of S on the base-state regime and on log dx
  rev2_twins.csv      3D-turbulence on/off differences of S (perturbed-twin noise)
  rev2_S_t.csv        S at every 15-min output time from cloud-top Nd (raw, unsmoothed)
  rev2_peak.csv       LWP maximum location (cloud-top Nd) against time
  rev2_relax.csv      exponential relaxation fits of LWP(t), 6-12 h, per run
  rev2_Seq.csv        steady-state S from the fits, paired moving-block bootstrap
  rev2_onoff.csv      on-minus-off LWP budget terms (rain-sink and entrainment parts), hours 10-12
  rev2_decoup.csv     multi-metric decoupling per run
  rev2_eff.csv        entrainment efficiencies (w*-based A; eta with several jump definitions)
  rev2_S55.csv        local S at cloud-top Nd = 55 cm-3 and the Nd above which |S| < 0.1
"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

R = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h"
T = f"{R}/manuscript/tables"
G, CP, LV, RD = 9.80616, 1004.64, 2.501e6, 287.04
BR = {"low": (20, 50), "mid": (50, 100), "high": (100, 200), "vhigh": (200, 1000)}
runs = pd.read_csv(f"{T}/runs.csv")
cc3 = pd.read_csv(f"{T}/cloudcover_3d.csv")
runs = runs.merge(cc3, on="case", how="left")
off = runs[runs.turb3d == "off"].copy()
B = pd.read_csv(f"{T}/ml_budget.csv")
ts = pd.read_csv(f"{R}/analysis_report5/timeseries_15min.csv")
ts = ts[(ts.time_h > 0)]


def tau_of(lwp_ic, nd):
    """Optical depth for adiabatic cloud: 0.07 LWP_ic^(5/6) Nd^(1/3) (LWP in g m-2, Nd in cm-3)."""
    return 0.07 * lwp_ic ** (5 / 6) * nd ** (1 / 3)


def alb(tau):
    return tau / (tau + 13.3)


def branch_table():
    rows = []
    for (dx, sed, ps, t3d), g in runs.groupby(["dx_km", "sed", "precsupp", "turb3d"]):
        g = g.set_index("Nd_target")
        for b, (a, c) in BR.items():
            if a not in g.index or c not in g.index:
                continue
            A, C = g.loc[a], g.loc[c]
            dl = np.log(C.LWP / A.LWP)
            dn_l, dn_t, dn_g = np.log(C.Nd_incloud / A.Nd_incloud), np.log(C.cdnc_top_cm3 / A.cdnc_top_cm3), np.log(c / a)
            ic_a, ic_c = A.LWP / A.cc_max, C.LWP / C.cc_max
            ict_a, ict_c = A.LWP / A.cloud_cover, C.LWP / C.cloud_cover
            r = {"dx_km": dx, "sed": sed, "precsupp": ps, "turb3d": t3d, "branch": b,
                 "S_layer": dl / dn_l, "S_top": dl / dn_t, "S_target": dl / dn_g,
                 "S_ic_max": np.log(ic_c / ic_a) / dn_t, "S_cf_max": np.log(C.cc_max / A.cc_max) / dn_t,
                 "S_ic_thr": np.log(ict_c / ict_a) / dn_t, "S_cf_thr": np.log(C.cloud_cover / A.cloud_cover) / dn_t,
                 "S_R": -np.log(max(C.precip, 1e-6) / max(A.precip, 1e-6)) / dn_t,
                 # base state of the lower-Nd run
                 "ratio_P_Fent": A.P_sfc_Wm2 / A.F_ent_moist, "LWP_base": A.LWP, "h_base": A.h_cloud, "zb_base": A.zb,
                 "Psfc_base": A.precip, "eta_base": A.eta_ent, "zi_base": A.zi, "rainfrac_base": A.rain_frac}
            r["dlntau_dlnNd"] = 1 / 3 + 5 / 6 * r["S_ic_max"]
            # offline albedo split (scene albedo = cc * A(tau)), sequential: Twomey, LWP_ic, CF
            ta = tau_of(ic_a, A.cdnc_top_cm3)
            tw = tau_of(ic_a, C.cdnc_top_cm3)
            tl = tau_of(ic_c, C.cdnc_top_cm3)
            twomey = A.cc_max * (alb(tw) - alb(ta))
            lwp_t = A.cc_max * (alb(tl) - alb(tw))
            cf_t = (C.cc_max - A.cc_max) * alb(tl)
            r.update(alb_twomey=twomey, alb_lwp=lwp_t, alb_cf=cf_t, alb_total=twomey + lwp_t + cf_t,
                     adj_over_twomey=(lwp_t + cf_t) / twomey)
            rows.append(r)
    return pd.DataFrame(rows)


def regime(bt):
    out = []
    d = bt[(bt.turb3d == "off")].copy()
    d["lnratio"] = np.log(np.clip(d.ratio_P_Fent, 1e-5, None))
    d["lndx"] = np.log(d.dx_km)
    for b in BR:
        for ps in ("on", "off", "both"):
            x = d[(d.branch == b) & ((d.precsupp == ps) | (ps == "both"))].dropna(subset=["S_top", "lnratio"])
            for pred in ("lnratio", "LWP_base", "h_base", "zb_base"):
                X1 = np.c_[np.ones(len(x)), x[pred]]
                c1, res1 = np.linalg.lstsq(X1, x.S_top, rcond=None)[:2]
                X2 = np.c_[X1, x.lndx]
                c2 = np.linalg.lstsq(X2, x.S_top, rcond=None)[0]
                r1 = 1 - np.sum((x.S_top - X1 @ c1) ** 2) / np.sum((x.S_top - x.S_top.mean()) ** 2)
                r2 = 1 - np.sum((x.S_top - X2 @ c2) ** 2) / np.sum((x.S_top - x.S_top.mean()) ** 2)
                Xd = np.c_[np.ones(len(x)), x.lndx]
                cd = np.linalg.lstsq(Xd, x.S_top, rcond=None)[0]
                rd = 1 - np.sum((x.S_top - Xd @ cd) ** 2) / np.sum((x.S_top - x.S_top.mean()) ** 2)
                out.append({"branch": b, "ps": ps, "pred": pred, "n": len(x), "r": np.corrcoef(x[pred], x.S_top)[0, 1],
                            "R2_state": r1, "R2_state_dx": r2, "R2_dx_only": rd, "slope": c1[1], "coef_lndx": c2[2]})
    return pd.DataFrame(out)


def twins():
    on = runs[runs.turb3d == "on"]
    rows = []
    bt = branch_table()
    for (dx, sed, ps), g in on.groupby(["dx_km", "sed", "precsupp"]):
        a = bt[(bt.dx_km == dx) & (bt.sed == sed) & (bt.precsupp == ps)]
        for b in BR:
            x_on = a[(a.turb3d == "on") & (a.branch == b)]
            x_off = a[(a.turb3d == "off") & (a.branch == b)]
            if len(x_on) and len(x_off):
                rows.append({"dx_km": dx, "sed": sed, "precsupp": ps, "branch": b,
                             "dS_top": x_on.S_top.iloc[0] - x_off.S_top.iloc[0],
                             "dlnLWP": np.nan})
    tw = pd.DataFrame(rows)
    pairs = []
    for _, r in on.iterrows():
        o = off[(off.res == r.res) & (off.Nd_target == r.Nd_target) & (off.sed == r.sed) & (off.precsupp == r.precsupp)].iloc[0]
        pairs.append(np.log(r.LWP / o.LWP))
    return tw, np.array(pairs)


def S_t():
    rows, peaks = [], []
    t = ts[ts.turb3d == "off"].dropna(subset=["LWP_gm2", "Nd_top_cm3"])
    for (res, dx, sed, ps), g in t.groupby(["res", "dx_km", "sed_factor", "precip_suppression"]):
        piv_l = g.pivot_table(index="time_h", columns="Nd_target", values="LWP_gm2")
        piv_n = g.pivot_table(index="time_h", columns="Nd_target", values="Nd_top_cm3")
        for b, (a, c) in BR.items():
            if a in piv_l and c in piv_l:
                s = np.log(piv_l[c] / piv_l[a]) / np.log(piv_n[c] / piv_n[a])
                for tt, v in s.items():
                    rows.append({"res": res, "dx_km": dx, "sed": sed, "ps": ps, "branch": b, "t": tt, "S": v})
        for tt in piv_l.index:
            L, N = piv_l.loc[tt].values, piv_n.loc[tt].values
            if np.any(~np.isfinite(L)) or np.any(~np.isfinite(N)):
                continue
            k = int(np.argmax(L))
            if 0 < k < len(L) - 1:
                x, y = np.log(N[k - 1:k + 2]), np.log(L[k - 1:k + 2])
                cc = np.polyfit(x, y, 2)
                xp = -cc[1] / (2 * cc[0]) if cc[0] < 0 else x[1]
                peaks.append({"res": res, "dx_km": dx, "sed": sed, "ps": ps, "t": tt, "Nd_peak": np.exp(xp), "edge": False,
                              "target_peak": [20, 50, 100, 200, 500, 1000][k]})
            else:
                peaks.append({"res": res, "dx_km": dx, "sed": sed, "ps": ps, "t": tt, "Nd_peak": N[k], "edge": True,
                              "target_peak": [20, 50, 100, 200, 500, 1000][k]})
    return pd.DataFrame(rows), pd.DataFrame(peaks)


def relax_model(t, Leq, L0, tau):
    return Leq + (L0 - Leq) * np.exp(-(t - 6.0) / tau)


def relax():
    rows, series = [], {}
    t = ts[ts.turb3d == "off"].dropna(subset=["LWP_gm2"])
    for case, g in t.groupby("case"):
        g = g[(g.time_h >= 6) & (g.time_h <= 12 + 1e-6)].sort_values("time_h")
        tt, L = g.time_h.values, g.LWP_gm2.values
        series[case] = (tt, L)
        try:
            p, _ = curve_fit(relax_model, tt, L, p0=[L[-1], L[0], 6.0], bounds=([0, 0, 0.5], [2000, 2000, 200]), maxfev=20000)
            res = L - relax_model(tt, *p)
            rows.append({"case": case, "Leq": p[0], "tau_h": p[2], "L12": L[-1], "rmse": np.sqrt(np.mean(res ** 2)),
                         "constrained": bool(p[2] < 24)})
        except Exception:
            rows.append({"case": case, "Leq": np.nan, "tau_h": np.nan, "L12": L[-1], "rmse": np.nan, "constrained": False})
    return pd.DataFrame(rows), series


def steady_S(rel, series, nboot=400):
    rng = np.random.default_rng(1)
    rel = rel.set_index("case")
    rows = []
    for (dx, sed, ps), g in off.groupby(["dx_km", "sed", "precsupp"]):
        g = g.set_index("Nd_target")
        for b, (a, c) in BR.items():
            ca, cc_ = g.case[a], g.case[c]
            ra, rc = rel.loc[ca], rel.loc[cc_]
            if not (ra.constrained and rc.constrained):
                rows.append({"dx_km": dx, "sed": sed, "ps": ps, "branch": b, "S_eq": np.nan, "p05": np.nan, "p95": np.nan,
                             "constrained": False})
                continue
            dn = np.log(g.cdnc_top_cm3[c] / g.cdnc_top_cm3[a])
            seq = np.log(rc.Leq / ra.Leq) / dn
            ta, La = series[ca]; tc, Lc = series[cc_]
            fa = relax_model(ta, ra.Leq, *(_p0(ta, La, ra)))
            fc = relax_model(tc, rc.Leq, *(_p0(tc, Lc, rc)))
            resa, resc = La - fa, Lc - fc
            n, blk = len(ta), 4
            boots = []
            for _ in range(nboot):
                idx = np.concatenate([np.arange(s0, s0 + blk) for s0 in rng.integers(0, n - blk + 1, n // blk + 1)])[:n]
                try:
                    pa, _ = curve_fit(relax_model, ta, fa + resa[idx], p0=[ra.Leq, La[0], ra.tau_h], bounds=([0, 0, 0.5], [2000, 2000, 200]), maxfev=5000)
                    pc, _ = curve_fit(relax_model, tc, fc + resc[idx], p0=[rc.Leq, Lc[0], rc.tau_h], bounds=([0, 0, 0.5], [2000, 2000, 200]), maxfev=5000)
                    boots.append(np.log(pc[0] / pa[0]) / dn)
                except Exception:
                    pass
            boots = np.array(boots)
            rows.append({"dx_km": dx, "sed": sed, "ps": ps, "branch": b, "S_eq": seq,
                         "p05": np.nanpercentile(boots, 5) if boots.size > 50 else np.nan,
                         "p95": np.nanpercentile(boots, 95) if boots.size > 50 else np.nan, "constrained": True,
                         "tau_a": ra.tau_h, "tau_c": rc.tau_h})
    return pd.DataFrame(rows)


def _p0(t, L, r):
    p, _ = curve_fit(relax_model, t, L, p0=[r.Leq, L[0], r.tau_h], bounds=([0, 0, 0.5], [2000, 2000, 200]), maxfev=20000)
    return p[1], p[2]


def onoff():
    b = B[(B.turb3d == "off") & (B.t_end == 12)]
    rows = []
    for (dx, nd, sed), g in b.groupby(["dx_km", "Nd_target", "sed"]):
        g = g.set_index("precsupp")
        if not {"on", "off"} <= set(g.index):
            continue
        on, of = g.loc["on"], g.loc["off"]
        rows.append({"dx_km": dx, "Nd_target": nd, "sed": sed,
                     "d_ent": 100 * (on.dlwp_ent / on.LWP - of.dlwp_ent / of.LWP),
                     "d_precip": 100 * (on.dlwp_precip / on.LWP - of.dlwp_precip / of.LWP),
                     "d_rad": 100 * (on.dlwp_rad / on.LWP - of.dlwp_rad / of.LWP),
                     "d_sum": 100 * (on.dlwp_dt_pred / on.LWP - of.dlwp_dt_pred / of.LWP),
                     "d_we": on.we_mm_s - of.we_mm_s, "P_on": on.P_sfc, "P_off": of.P_sfc})
    return pd.DataFrame(rows)


def lcl(thl, qt, ps=101780.0):
    z = np.arange(0.0, 2500.0, 2.0)
    p = ps * np.exp(-G * z / (RD * 287.0))
    Tz = thl * (p / 1e5) ** (RD / CP)
    es = 611.2 * np.exp(17.67 * (Tz - 273.15) / (Tz - 29.65))
    qs = 0.622 * es / (p - 0.378 * es)
    k = np.where(qs <= qt)[0]
    return z[k[0]] if k.size else np.nan


def decoup_eff():
    rows = []
    for _, r in off.iterrows():
        d = np.load(f"{R}/explore/npz/explore_{r.case}.npz")
        z, thl, qt, rho = d["z"], d["thl"], d["qt"], d["rho"]
        zi = float(d["zi"])
        # inversion base: lowest level within zi-300..zi where dthl/dz exceeds 20 % of its max
        sel = np.where((z > zi - 300) & (z < zi + 300))[0]
        gr = np.diff(thl[sel]) / np.diff(z[sel])
        kb = sel[np.where(gr > 0.2 * gr.max())[0][0]]
        zib = z[kb]
        lo, hi = z < 0.25 * zib, (z > 0.75 * zib) & (z < zib)
        dqt = (qt[lo].mean() - qt[hi].mean()) * 1e3
        dthl = thl[hi].mean() - thl[lo].mean()
        zb = float(r.zb)
        lcl_sfc = lcl(thl[:3].mean(), qt[:3].mean())
        B = d["buoy_sgs"] + (d["wthv_res"] if "wthv_res" in d.files else 0)
        Bs = B[0]
        below = (z < zb) & (z > 50)
        bmin = B[below].min() / Bs if below.any() else np.nan
        dz = np.gradient(z)
        neg = -np.sum(np.minimum(B[z < zib], 0) * dz[z < zib]); pos = np.sum(np.maximum(B[z < zib], 0) * dz[z < zib])
        w2 = d["w2_sgs"] + (d["w2_res"] if "w2_res" in d.files else 0)
        wcl = w2[(z > zb) & (z < zib)].mean(); wsc = w2[z < zb].mean()
        # efficiency
        th0 = thl[z < zib].mean()
        Bint = np.sum(B[z < zi] * dz[z < zi])
        wstar3 = 2.5 * G / th0 * Bint
        we = r.we_812_mm_s * 1e-3
        dthv = r.dthl_inv + 0.608 * th0 * r.dqt_inv_gkg * 1e-3
        A_eff = we * zi * G / th0 * dthv / wstar3 if wstar3 > 0 else np.nan
        rows.append({"case": r.case, "zib": zib, "dqt_J": dqt, "dthl_J": dthl,
                     "jones_decoupled": bool(dqt > 0.5 and dthl > 0.5), "zb_minus_lcl_sfc": zb - lcl_sfc,
                     "Bmin_below_zb_rel": bmin, "Bneg_over_pos": neg / pos if pos > 0 else np.nan,
                     "w2_cloud_over_sub": wcl / wsc if wsc > 0 else np.nan, "wstar": np.cbrt(max(wstar3, 0)),
                     "A_eff": A_eff, "Bint": Bint})
    return pd.DataFrame(rows)


def S55():
    rows = []
    for (dx, sed, ps), g in off.groupby(["dx_km", "sed", "precsupp"]):
        g = g.sort_values("cdnc_top_cm3")
        x, y = np.log(g.cdnc_top_cm3.values), np.log(g.LWP.values)
        c = np.polyfit(x[:3], y[:3], 2)
        s55 = 2 * c[0] * np.log(55) + c[1]
        sl = np.diff(y) / np.diff(x)
        xm = np.exp(0.5 * (x[1:] + x[:-1]))
        k = np.where(np.abs(sl) < 0.1)[0]
        rows.append({"dx_km": dx, "sed": sed, "ps": ps, "S55": s55, "Nd_top_S_below_0p1": xm[k[0]] if k.size else np.nan,
                     "S_fit_all": np.polyfit(x, y, 1)[0]})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    bt = branch_table(); bt.to_csv(f"{T}/rev2_branch.csv", index=False)
    regime(bt).to_csv(f"{T}/rev2_regime.csv", index=False)
    tw, pairs = twins(); tw.to_csv(f"{T}/rev2_twins.csv", index=False)
    print("twin pairs:", len(pairs), "RMS dlnLWP", np.sqrt(np.mean(pairs ** 2)).round(4), "mean", pairs.mean().round(4))
    st, pk = S_t(); st.to_csv(f"{T}/rev2_S_t.csv", index=False); pk.to_csv(f"{T}/rev2_peak.csv", index=False)
    rel, series = relax(); rel.to_csv(f"{T}/rev2_relax.csv", index=False)
    steady_S(rel, series).to_csv(f"{T}/rev2_Seq.csv", index=False)
    onoff().to_csv(f"{T}/rev2_onoff.csv", index=False)
    decoup_eff().to_csv(f"{T}/rev2_decoup.csv", index=False)
    S55().to_csv(f"{T}/rev2_S55.csv", index=False)
    print("done")
