#!/usr/bin/env python3
"""
Revision-2 analyses that use the CPU-node products (rev2_3d.py, rev2_cols.py, profiles_ts2.py).

Outputs (manuscript/tables/):
  rev2_d3.csv        3D-snapshot diagnostics merged with run settings, plus the inversion flux budget
                     (resolved + SHOC turbulent theta_l flux at the flux minimum vs the implied
                     entrainment flux -w_e*Dtheta_l; residual = implicit mixing)
  rev2_sedflux.csv   change in w_e against change in the offline cloud-top sedimentation flux (s=2 vs 0.5)
  rev2_tiles.csv     spatial block-bootstrap (4x4 tiles of 60 km) 90 % intervals of S at hours 10-12
  rev2_sat.csv       pooled composites per (dx, s, suppression): within-scene, pooled and between-run slopes
                     of ln LWP on ln Nd (cloud-top and retrieval-like), ln Nd variance partition
  rev2_eta.csv       eta for jump offsets of 50/100/150 m and for the specified interface jump (6.7 K);
                     observational reference
  rev2_ft.csv        free-tropospheric drift and inversion wind shear (6 h and 12 h)
  rev2_budget2.csv   budget for in-cloud LWP with cloud-layer LCL sensitivities, plus a cloud-fraction term,
                     with a coupling flag
"""
import glob
import numpy as np
import pandas as pd

R = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h"
T = f"{R}/manuscript/tables"
RD, CP, LV, G, P0 = 287.04, 1004.64, 2.501e6, 9.80616, 1e5
runs = pd.read_csv(f"{T}/runs.csv")
off = runs[runs.turb3d == "off"]
dec = pd.read_csv(f"{T}/rev2_decoup.csv")


def d3():
    d = pd.concat([pd.read_csv(f"{R}/manuscript/rev2/d3_a.csv"), pd.read_csv(f"{R}/manuscript/rev2/d3_b.csv")])
    d = d.merge(off[["case", "res", "dx_km", "Nd_target", "sed", "precsupp", "we_812_mm_s", "dthl_inv", "zi", "Nd_incloud",
                     "cdnc_top_cm3"]], on="case")
    sgs, impl50 = [], []
    ml2 = pd.read_csv(f"{T}/ml_timeseries2.csv")
    for _, r in d.iterrows():
        e = np.load(f"{R}/explore/npz/explore_{r.case}.npz")
        z = e["z"]
        zint = np.r_[0.0, 0.5 * (z[1:] + z[:-1]), z[-1] + 0.5 * (z[-1] - z[-2])]
        sgs.append(np.interp(r.z_fluxmin, zint, e["wthl_sgs"]))
        m = ml2[(ml2.case == r.case) & (ml2.time_h > 10) & (ml2.time_h <= 12.001)]
        impl50.append(-(r.we_812_mm_s * 1e-3) * (m.thl_zi50 - m.thl_ml).mean())
    d["wthl_sgs_at"] = sgs
    d["wthl_turb"] = d.wthl_res_min + d.wthl_sgs_at
    d["F_impl50"] = impl50
    d["F_impl100"] = -(d.we_812_mm_s * 1e-3) * d.dthl_inv
    d["resid_frac50"] = 1 - d.wthl_turb / d.F_impl50
    d["res_frac_of_turb"] = d.wthl_res_min / d.wthl_turb
    d.to_csv(f"{T}/rev2_d3.csv", index=False)
    rows = []
    for (dx, nd, ps), g in d.groupby(["dx_km", "Nd_target", "precsupp"]):
        g = g.set_index("sed")
        if {0.5, 2.0} <= set(g.index):
            F05, F2 = 0.5 * g.Fsed_top_mmd[0.5], 2.0 * g.Fsed_top_mmd[2.0]
            rows.append({"dx_km": dx, "Nd_target": nd, "precsupp": ps, "Fsed_s05": F05, "Fsed_s2": F2, "dF": F2 - F05,
                         "dwe": g.we_812_mm_s[2.0] - g.we_812_mm_s[0.5], "Vsed_s1": g.Vsed_top.get(1.0, np.nan),
                         "Fsed_s1": g.Fsed_top_mmd.get(1.0, np.nan)})
    pd.DataFrame(rows).to_csv(f"{T}/rev2_sedflux.csv", index=False)
    return d


def tiles(nboot=2000):
    rng = np.random.default_rng(2)
    BR = {"low": (20, 50), "high": (100, 200), "vhigh": (200, 1000)}
    rows = []
    for (dx, sed, ps), g in off[off.dx_km <= 5].groupby(["dx_km", "sed", "precsupp"]):
        g = g.set_index("Nd_target")
        tl = {nd: np.load(f"{R}/manuscript/rev2/cols/cols_{c}.npz")["tiles"].mean(0) for nd, c in g.case.items()}
        for b, (a, c) in BR.items():
            dn = np.log(g.cdnc_top_cm3[c] / g.cdnc_top_cm3[a])
            ia = rng.integers(0, 16, (nboot, 16)); ic = rng.integers(0, 16, (nboot, 16))
            sb = np.log(tl[c][ic].mean(1) / tl[a][ia].mean(1)) / dn
            s0 = np.log(tl[c].mean() / tl[a].mean()) / dn
            rows.append({"dx_km": dx, "sed": sed, "ps": ps, "branch": b, "S_top": s0, "p05": np.percentile(sb, 5),
                         "p95": np.percentile(sb, 95), "sd": sb.std()})
    pd.DataFrame(rows).to_csv(f"{T}/rev2_tiles.csv", index=False)


def slope(st):
    n, sx, sy, sxx, syy, sxy = st
    vx = sxx / n - (sx / n) ** 2
    vy = syy / n - (sy / n) ** 2
    cxy = sxy / n - sx * sy / n ** 2
    return cxy / vx if vx > 0 else np.nan, cxy / np.sqrt(vx * vy) if vx > 0 and vy > 0 else np.nan, vx


def sat():
    rows = []
    for (dx, sed, ps), g in off[off.dx_km <= 5].groupby(["dx_km", "sed", "precsupp"]):
        for kind in ("top_f1", "top_f2", "ret_f2", "top_c4", "ret_c4"):
            stats, within, means = [], [], []
            for _, r in g.iterrows():
                d = np.load(f"{R}/manuscript/rev2/cols/cols_{r.case}.npz")
                st = d[kind]
                if st[0] < 30:
                    continue
                # equal weight per run: normalise sums to unit count
                stn = st / st[0]
                stats.append(stn)
                b, rr, vx = slope(st)
                within.append((b, rr, vx))
                means.append((st[1] / st[0], st[2] / st[0]))
            if len(stats) < 4:
                continue
            pooled = np.sum(stats, 0)
            bp, rp, vxp = slope(pooled)
            mx, my = np.array(means).T
            bb = np.polyfit(mx, my, 1)[0]
            vw = np.mean([w[2] for w in within])
            rows.append({"dx_km": dx, "sed": sed, "ps": ps, "kind": kind, "n_runs": len(stats),
                         "slope_pooled": bp, "r_pooled": rp, "slope_between": bb,
                         "slope_within_min": np.nanmin([w[0] for w in within]), "slope_within_max": np.nanmax([w[0] for w in within]),
                         "r_within_min": np.nanmin([w[1] for w in within]), "r_within_max": np.nanmax([w[1] for w in within]),
                         "sd_lnNd_within_max": np.sqrt(np.nanmax([w[2] for w in within])),
                         "frac_var_within": vw / vxp, "mean_lnNd": mx.tolist().__repr__()})
    pd.DataFrame(rows).to_csv(f"{T}/rev2_sat.csv", index=False)


def eta_ft():
    ml2 = pd.read_csv(f"{T}/ml_timeseries2.csv")
    w = ml2[(ml2.time_h > 10) & (ml2.time_h <= 12.001)].groupby("case").mean(numeric_only=True)
    x = off.set_index("case").join(w, rsuffix="_ts")
    rho, we = x.rho_zi, x.we_812_mm_s * 1e-3
    out = pd.DataFrame({"dx_km": x.dx_km, "Nd_target": x.Nd_target, "sed": x.sed, "precsupp": x.precsupp,
                        "F_rad": x.F_rad_ts if "F_rad_ts" in x else x.F_rad})
    for lab, col in (("50", "thl_zi50"), ("100", None), ("150", "thl_zi150")):
        dth = x.dthl_inv if col is None else x[col] - x.thl_ml_ts if "thl_ml_ts" in x else x[col] - x.thl_ml
        out[f"dthl_{lab}"] = dth
        out[f"eta_{lab}"] = rho * CP * we * dth / out.F_rad
    out["eta_interface"] = rho * CP * we * 6.7 / out.F_rad
    out["eta_steady_ref"] = 1 - (16.0 + x.P_sfc_Wm2) / out.F_rad
    out.reset_index().to_csv(f"{T}/rev2_eta.csv", index=False)
    rows = []
    for case, g in ml2.groupby("case"):
        if "t3don" in case:
            continue
        g = g.set_index("time_h")
        def at(t, c):
            return g[c].iloc[np.argmin(np.abs(g.index.values - t))]
        rows.append({"case": case, "thl_2km_0": at(0.25, "thl_2km"), "thl_2km_12": at(12, "thl_2km"),
                     "thl_ft300_6": at(6, "thl_ft300"), "thl_ft300_12": at(12, "thl_ft300"),
                     "qt_2km_0": at(0.25, "qt_2km"), "qt_2km_12": at(12, "qt_2km"),
                     "dU_inv_6": at(6, "dU_inv"), "dU_inv_12": at(12, "dU_inv"),
                     "U_ml_0": np.hypot(at(0.25, "u_ml"), at(0.25, "v_ml")), "U_ml_12": np.hypot(at(12, "u_ml"), at(12, "v_ml")),
                     "heat_ft_rad_12": at(12, "heat_ft_rad_Kday"), "dthl_inv12": at(12, "dthl_inv"),
                     "jump50_12": at(12, "thl_zi50") - at(12, "thl_ml")})
    pd.DataFrame(rows).merge(off[["case", "dx_km", "Nd_target", "sed", "precsupp"]], on="case").to_csv(f"{T}/rev2_ft.csv", index=False)


def qsat(Tk, p):
    es = 611.2 * np.exp(17.67 * (Tk - 273.15) / (Tk - 29.65))
    return 0.622 * es / (p - 0.378 * es)


def lcl(thl, qt, ps=101780.0):
    z = np.arange(0.0, 2500.0, 1.0)
    p = ps * np.exp(-G * z / (RD * 287.0))
    k = np.where(qsat(thl * (p / P0) ** (RD / CP), p) <= qt)[0]
    return float(z[k[0]]) if k.size else np.nan


def budget2():
    """In-cloud LWP budget with cloud-layer LCL sensitivities and an explicit cloud-fraction term."""
    ml2 = pd.read_csv(f"{T}/ml_timeseries2.csv")
    B = pd.read_csv(f"{T}/ml_budget.csv")
    coupled = dec.set_index("case")
    rows = []
    for _, b in B[(B.turb3d == "off")].iterrows():
        f = np.load(f"{R}/manuscript/fields/fields_{b.case}.npz")
        th, cc, lic = f["t_h"], f["cc"], f["lwp_ic"]
        w = (th > b.t_end - 2 + 1e-6) & (th <= b.t_end + 1e-6)
        if w.sum() < 6:
            continue
        tt = th[w] * 3600
        dlnlic = np.polyfit(tt, np.log(lic[w]), 1)[0] * 3600 * 100
        dlncc = np.polyfit(tt, np.log(np.maximum(cc[w], 1e-3)), 1)[0] * 3600 * 100
        g = ml2[(ml2.case == b.case) & (ml2.time_h > b.t_end - 2 + 1e-6) & (ml2.time_h <= b.t_end + 1e-6)]
        thc, qtc = g.thl_cl.mean(), g.qt_cl.mean() * 1e-3
        a = (lcl(thc + 0.05, qtc) - lcl(thc - 0.05, qtc)) / 0.1
        bq = (lcl(thc, qtc + 5e-5) - lcl(thc, qtc - 5e-5)) / 1e-4
        zi, h = b.zi, b.h
        we, ws = b.we_mm_s * 1e-3, b.w_subs_mm_s * 1e-3
        rho = b.rho
        th_ent, q_ent = we * b.dthl_inv / zi, we * b.dqt_inv * 1e-3 / zi
        th_rad = -b.F_rad / (rho * CP * zi)
        th_sfc, q_sfc = b.SHF / (rho * CP * zi), b.LHF / (rho * LV * zi)
        th_pr, q_pr = b.P_sfc / (rho * CP * zi), -b.P_sfc / (rho * LV * zi)
        fac = 2.0 / h * 3600 * 100            # % per hour per (m/s)
        terms = {"ent_zi": fac * we, "ent_zb": fac * (-a * th_ent - bq * q_ent), "subs": fac * ws,
                 "rad": fac * (-a * th_rad), "sfc": fac * (-a * th_sfc - bq * q_sfc), "precip": fac * (-a * th_pr - bq * q_pr)}
        c = coupled.loc[b.case] if b.case in coupled.index else None
        rows.append({"case": b.case, "t_end": b.t_end, "dx_km": b.dx_km, "Nd_target": b.Nd_target, "sed": b.sed,
                     "precsupp": b.precsupp, "dlnLWPic_obs": dlnlic, "dlncc_obs": dlncc,
                     "dlnLWP_obs": 100 * b.dlwp_dt_obs / b.LWP, **{f"t_{k}": v for k, v in terms.items()},
                     "dlnLWPic_pred": sum(terms.values()), "dzb_dthl_cl": a,
                     "zb_minus_lcl_ml": b.zb - b.lcl_ml,
                     "coupled": bool(c is not None and (not c.jones_decoupled) and (b.zb - b.lcl_ml) < 50 and c.Bmin_below_zb_rel > 0.2)})
    pd.DataFrame(rows).to_csv(f"{T}/rev2_budget2.csv", index=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "budget":
        budget2()
    else:
        d3(); tiles(); sat(); eta_ft(); budget2()
    print("done")
