#!/usr/bin/env python3
"""
Build every table used in the manuscript from the per-run products.

Inputs (all under /pscratch/sd/m/mahf708/dp_screamxx_sedps_12h):
  analysis_report5/summary_h10-12.csv, analysis_report5/timeseries_15min.csv
  manuscript/newruns/<case>/{summary_h10-12.csv,timeseries_15min.csv}   (runs finished later)
  explore/npz/explore_<case>.npz      (explore.py: profiles and process scalars, hours 10-12)
  manuscript/fields/fields_<case>.npz (extract_fields.py: column statistics)
  IOP file (large-scale subsidence)

Outputs (manuscript/tables/):
  runs.csv            one row per run: summary + explore scalars + derived quantities
  susceptibility.csv  S on three Nd branches for every (dx, sed, ps, t3d) with
                      temporal-sampling spread (S at each 15-min instant in hours 10-12)
  decomposition.csv   factorial decomposition of S into precipitation-suppression,
                      sedimentation and residual contributions
  s_time.csv          S on each branch for 2-h windows ending at 4, 6, 8, 10, 12 h
  convergence.csv     relative change per halving of dx and an observed-order test
  scene.csv           within-scene (spatial) ln LWP - ln Nd_top slopes
Usage:  python3 build_tables.py
"""
import glob
import os

import netCDF4
import numpy as np
import pandas as pd

R = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h"
A5 = f"{R}/analysis_report5"
OUT = f"{R}/manuscript/tables"
IOP = "/global/cfs/cdirs/e3sm/inputdata/atm/cam/scam/iop/DYCOMSrf02_iopfile_4scam.nc"
G, RD, CP, LV = 9.80616, 287.04, 1004.64, 2.501e6
PS = 101780.0
LHF, SHF = 93.0, 16.0                  # prescribed IOP surface fluxes (W m-2)
BRANCHES = {"low": (20, 50), "high": (100, 200), "vhigh": (200, 1000)}
os.makedirs(OUT, exist_ok=True)


def load_summary():
    s = pd.read_csv(f"{A5}/summary_h10-12.csv")
    t = pd.read_csv(f"{A5}/timeseries_15min.csv")
    for d in sorted(glob.glob(f"{R}/manuscript/newruns/sedps_*")):
        f1, f2 = f"{d}/summary_h10-12.csv", f"{d}/timeseries_15min.csv"
        if os.path.exists(f1) and os.path.exists(f2):
            s = pd.concat([s[s.case != os.path.basename(d)], pd.read_csv(f1)])
            t = pd.concat([t[t.case != os.path.basename(d)], pd.read_csv(f2)])
    return s.reset_index(drop=True), t.reset_index(drop=True)


def subsidence():
    """w_subs(p) (m/s, negative downward) from the IOP omega and T profiles."""
    with netCDF4.Dataset(IOP) as d:
        p = np.asarray(d["lev"][:]).ravel()
        om = np.asarray(d["omega"][0]).ravel()
        T = np.asarray(d["T"][0]).ravel()
    w = -om / (p / (RD * T) * G)
    return lambda pp: np.interp(pp, p, w)


def interp(z, f, z0):
    return float(np.interp(z0, z, f))


def explore_row(case, wsub, zi_series):
    f = f"{R}/explore/npz/explore_{case}.npz"
    if not os.path.exists(f):
        return {}
    d = np.load(f)
    z, rho, thl, qt = d["z"], d["rho"], d["thl"], d["qt"]
    zi = float(d["zi"])
    out = {k: float(d[k]) for k in ("dqt", "dthl", "autoconv_col", "accret_col", "evap_col", "precip_sfc",
                                     "evap_frac", "lw_cool_bl", "w2_sgs_bl", "tke_sgs_bl", "rain_frac",
                                     "dx_phys", "lambda_peak") if k in d.files}
    for k in ("w2_res_bl", "f_res", "skew_w_mid", "skew_w_bl"):
        out[k] = float(d[k]) if k in d.files else np.nan
    out["zi_prof"], out["zb_prof"] = zi, float(d["zb"])
    # hydrostatic pressure from the mean density profile -> subsidence at z_i
    dz = np.diff(np.concatenate([[0.0], z]))
    p = PS - np.cumsum(rho * G * dz)
    # entrainment rate: linear fit of z_i(t) minus subsidence at z_i
    th, zt = zi_series
    sel = (th >= 10 - 1e-6) & (th <= 12 + 1e-6) & np.isfinite(zt)
    dzdt = np.polyfit(th[sel], zt[sel], 1)[0] / 3600.0 if sel.sum() > 3 else np.nan
    zim = float(np.nanmean(zt[sel]))
    ws = float(wsub(interp(z, p, zim)))
    out["dzi_dt_1012_mm_s"] = dzdt * 1e3
    out["w_subs_1012_mm_s"] = ws * 1e3
    out["we_1012_mm_s"] = (dzdt - ws) * 1e3
    # 4-h fit (8-12 h): less sensitive to the 50 m level spacing at the inversion; used for w_e below
    s4 = (th >= 8 - 1e-6) & (th <= 12 + 1e-6) & np.isfinite(zt)
    out["we_812_mm_s"] = (np.polyfit(th[s4], zt[s4], 1)[0] / 3600.0 - ws) * 1e3
    # inversion jumps: mixed layer (0.1-0.8 z_i) to 100 m above z_i
    ml = (z > 0.1 * zi) & (z < 0.8 * zi)
    thl_ml, qt_ml = thl[ml].mean(), qt[ml].mean()
    out["thl_ml"], out["qt_ml_gkg"] = thl_ml, qt_ml * 1e3
    out["dthl_inv"] = interp(z, thl, zi + 100) - thl_ml
    out["dqt_inv_gkg"] = (interp(z, qt, zi + 100) - qt_ml) * 1e3
    rho_i = interp(z, rho, zi)
    we = out["we_812_mm_s"] * 1e-3
    out["F_ent_heat"] = rho_i * CP * we * out["dthl_inv"]                 # W m-2, warming of the BL
    out["F_ent_moist"] = -rho_i * LV * we * out["dqt_inv_gkg"] * 1e-3     # W m-2, drying of the BL
    out["F_rad"] = -out["lw_cool_bl"]                                     # W m-2, BL radiative cooling
    out["eta_ent"] = out["F_ent_heat"] / out["F_rad"]
    out["P_sfc_Wm2"] = out["precip_sfc"] * LV / 86400.0                  # mm/day -> W m-2
    out["P_gross_Wm2"] = (out["autoconv_col"] + out["accret_col"]) * LV / 86400.0
    # cloud layer from the mean profile
    cf = d["cf"]
    k = np.where(cf > 0.5 * cf.max())[0]
    out["h_cloud_prof"] = float(z[k[-1]] - z[k[0]]) if k.size else np.nan
    return out


def fields_row(case):
    f = f"{R}/manuscript/fields/fields_{case}.npz"
    if not os.path.exists(f):
        return {}
    d = np.load(f)
    th = d["t_h"]
    w = (th > 10 - 1e-6) & (th <= 12 + 1e-6)
    w8 = (th > 10 + 1e-6) & (th <= 12 + 1e-6)
    out = {"cc_f": float(np.nanmean(d["cc"][w8])), "lwp_ic": float(np.nanmean(d["lwp_ic"][w8])),
           "nd_top_ic": float(np.nanmean(d["nd_top_ic"][w8]))}
    if d["slope_scene"].size:
        out["slope_scene"] = float(np.mean(d["slope_scene"]))
        out["slope_scene_sd"] = float(np.std(d["slope_scene"]))
        out["corr_scene"] = float(np.mean(d["corr_scene"]))
    return out


def runs_table(s, t):
    wsub = subsidence()
    rows = []
    for _, r in s.iterrows():
        tt = t[t.case == r.case].sort_values("time_h")
        ts = tt.dropna(subset=["zi_m"])
        row = r.to_dict()
        row.update(explore_row(r.case, wsub, (ts.time_h.values, ts.zi_m.values)))
        row.update(fields_row(r.case))
        rows.append(row)
    df = pd.DataFrame(rows)
    df["h_cloud"] = df.zi - df.zb
    return df


# ---------------------------------------------------------------- susceptibility
def lwp_instants(t, case):
    """15-min-averaged LWP for the 8 intervals ending in (10, 12] h."""
    tt = t[(t.case == case)].dropna(subset=["LWP_gm2"])
    tt = tt[(tt.time_h > 10 + 1e-6) & (tt.time_h <= 12 + 1e-6)].sort_values("time_h")
    return tt.LWP_gm2.values


def susceptibility(df, t):
    rows = []
    for (res, dx, sed, ps, t3d), g in df.groupby(["res", "dx_km", "sed", "precsupp", "turb3d"]):
        g = g.set_index("Nd_target")
        row = {"res": res, "dx_km": dx, "sed": sed, "precsupp": ps, "turb3d": t3d}
        for b, (a, c) in BRANCHES.items():
            if a not in g.index or c not in g.index:
                row[f"S_{b}"] = np.nan
                continue
            dln_n = np.log(g.Nd_incloud[c] / g.Nd_incloud[a])
            row[f"S_{b}"] = np.log(g.LWP[c] / g.LWP[a]) / dln_n
            la, lc = lwp_instants(t, g.case[a]), lwp_instants(t, g.case[c])
            n = min(la.size, lc.size)
            si = np.log(lc[:n] / la[:n]) / dln_n
            row[f"S_{b}_sd"] = si.std(ddof=1) if n > 2 else np.nan
            row[f"S_{b}_min"], row[f"S_{b}_max"] = (si.min(), si.max()) if n else (np.nan, np.nan)
            # same with cloud-top (retrieval-like) Nd instead of the layer Nd
            row[f"S_{b}_top"] = np.log(g.LWP[c] / g.LWP[a]) / np.log(g.cdnc_top_cm3[c] / g.cdnc_top_cm3[a])
            # cloud-cover and in-cloud LWP parts (d ln LWP = d ln cc + d ln LWP_ic, approx.)
            if "cc_f" in g and np.isfinite(g.cc_f[a]) and np.isfinite(g.cc_f[c]):
                row[f"S_{b}_cc"] = np.log(g.cc_f[c] / g.cc_f[a]) / dln_n
                row[f"S_{b}_ic"] = np.log(g.lwp_ic[c] / g.lwp_ic[a]) / dln_n
        # Nd of maximum LWP (from the discrete Nd levels)
        row["Nd_target_at_max"] = int(g.LWP.idxmax())
        rows.append(row)
    return pd.DataFrame(rows)


def decomposition(S):
    """S(on, s) = [S(on, s) - S(off, s)] + b*s + a, where S(off, s) = a + b*s is fit over s = 0.5, 1, 2."""
    rows = []
    for (res, dx, t3d), g in S.groupby(["res", "dx_km", "turb3d"]):
        for b in BRANCHES:
            on = g[g.precsupp == "on"].set_index("sed")[f"S_{b}"]
            off = g[g.precsupp == "off"].set_index("sed")[f"S_{b}"]
            if len(on) < 3 or len(off) < 3 or on.isna().any() or off.isna().any():
                continue
            ss = np.array([0.5, 1.0, 2.0])
            bb, aa = np.polyfit(ss, off.loc[ss].values, 1)
            resid = off.loc[ss].values - (aa + bb * ss)
            bon, aon = np.polyfit(ss, on.loc[ss].values, 1)
            for s_ in ss:
                rows.append({"res": res, "dx_km": dx, "turb3d": t3d, "branch": b, "sed": s_,
                             "S_on": on[s_], "S_off": off[s_], "S_ps": on[s_] - off[s_],
                             "S_sed": bb * s_, "S_resid": aa, "fit_rms_off": np.sqrt(np.mean(resid ** 2)),
                             "dS_dsed_off": bb, "dS_dsed_on": bon, "S_on_sed0": aon})
    return pd.DataFrame(rows)


def s_time(df, t):
    """S for 2-h windows; Nd from the 3D snapshots at the window ends."""
    rows = []
    for (res, dx, sed, ps, t3d), g in df.groupby(["res", "dx_km", "sed", "precsupp", "turb3d"]):
        g = g.set_index("Nd_target")
        for te in (4, 6, 8, 10, 12):
            row = {"res": res, "dx_km": dx, "sed": sed, "precsupp": ps, "turb3d": t3d, "t_end": te}
            vals = {}
            for nd, case in g.case.items():
                tt = t[t.case == case]
                lw = tt[(tt.time_h > te - 2 + 1e-6) & (tt.time_h <= te + 1e-6)].LWP_gm2.mean()
                n3 = tt.dropna(subset=["Nd_med_3d_cm3"])
                n3 = n3[(n3.time_h >= te - 2 - 1e-6) & (n3.time_h <= te + 1e-6)].Nd_med_3d_cm3.mean()
                vals[nd] = (lw, n3)
                row[f"LWP_{nd}"] = lw
            for b, (a, c) in BRANCHES.items():
                if a in vals and c in vals:
                    row[f"S_{b}"] = np.log(vals[c][0] / vals[a][0]) / np.log(vals[c][1] / vals[a][1])
            rows.append(row)
    return pd.DataFrame(rows)


def convergence(df):
    """Relative change per halving of dx and an observed order from the three finest grids."""
    rows = []
    sub = df[(df.turb3d == "off")]
    order = [5.0, 2.5, 1.25, 0.625, 0.3125]
    for (nd, sed, ps), g in sub.groupby(["Nd_target", "sed", "precsupp"]):
        g = g.set_index("dx_km")
        for var in ("LWP", "cloud_cover", "we_812_mm_s", "zi", "zb", "h_cloud", "lambda_peak", "Nd_incloud"):
            if not all(d in g.index for d in order):
                continue
            v = [g[var][d] for d in order]
            row = {"Nd_target": nd, "sed": sed, "precsupp": ps, "var": var}
            for d, x in zip(order, v):
                row[f"v_{d:g}"] = x
            for d1, d2, x1, x2 in zip(order[:-1], order[1:], v[:-1], v[1:]):
                row[f"rel_{d1:g}_{d2:g}"] = (x2 - x1) / x1
            e1, e2 = v[2] - v[3], v[3] - v[4]          # 1.25->0.625, 0.625->0.3125
            row["ratio_finest"] = e2 / e1 if e1 != 0 else np.nan
            row["p_obs"] = np.log2(e1 / e2) if (e1 * e2 > 0 and abs(e2) < abs(e1)) else np.nan
            rows.append(row)
    return pd.DataFrame(rows)


def main():
    s, t = load_summary()
    df = runs_table(s, t)
    df.to_csv(f"{OUT}/runs.csv", index=False)
    S = susceptibility(df, t)
    S.to_csv(f"{OUT}/susceptibility.csv", index=False)
    decomposition(S).to_csv(f"{OUT}/decomposition.csv", index=False)
    s_time(df[df.turb3d == "off"], t).to_csv(f"{OUT}/s_time.csv", index=False)
    convergence(df).to_csv(f"{OUT}/convergence.csv", index=False)
    print(len(df), "runs;", (df.turb3d == "on").sum(), "with 3D turbulence;", S.shape, "S rows")


if __name__ == "__main__":
    main()
