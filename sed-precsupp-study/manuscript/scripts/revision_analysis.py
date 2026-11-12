#!/usr/bin/env python3
"""
Additional diagnostics for the revised manuscript (login node; light work).

Outputs in manuscript/tables/:
  obs_comparison.csv  hours 4-6 (the last 2 h of the 6 h RF02 protocol) at target Nd 50
  budget_skill.csv    mixed-layer budget skill by grid spacing, raw and for Nd anomalies
  matched_nd.csv      LWP interpolated (in ln Nd) to fixed diagnosed in-cloud Nd
  shocmix.csv         domain-mean SHOC mixing length, CCN floor and in-cloud Nd profiles (h 10-12)
  dwe_sed.csv         w_e(s=2) - w_e(s=0.5) at fixed (dx, Nd, suppression)
  nd_stability.csv    drift of the diagnosed in-cloud Nd between 6 h and 12 h
  sfcflux_feedback.csv bulk estimate of surface-flux changes if fluxes were interactive
  deposition.csv      estimate of cloud-droplet deposition at the surface (lowest model level)
  scene_se.csv        within-scene slope mean and standard error over instants (dx <= 5 km)
  interaction.csv     dS/ds with suppression on and off and their difference (interaction)
"""
import glob
import os

import netCDF4
import numpy as np
import pandas as pd

R = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h"
T = f"{R}/manuscript/tables"
IOP = "/global/cfs/cdirs/e3sm/inputdata/atm/cam/scam/iop/DYCOMSrf02_iopfile_4scam.nc"
G, RD, CP, LV, P0, RHOW = 9.80616, 287.04, 1004.64, 2.501e6, 1.0e5, 1000.0
runs = pd.read_csv(f"{T}/runs.csv")
off = runs[runs.turb3d == "off"]
ml = pd.read_csv(f"{T}/ml_timeseries.csv")
B = pd.read_csv(f"{T}/ml_budget.csv")
D = pd.read_csv(f"{T}/decomposition.csv")
ts = pd.read_csv(f"{R}/analysis_report5/timeseries_15min.csv")
with netCDF4.Dataset(IOP) as d:
    _p = np.asarray(d["lev"][:]).ravel()
    _w = -np.asarray(d["omega"][0]).ravel() / (_p / (RD * np.asarray(d["T"][0]).ravel()) * G)
    TG = float(np.asarray(d["Tg"][:]).ravel()[0])
    PS = float(np.asarray(d["Ps"][:]).ravel()[0])


def horiz(case, names, t0, t1):
    """Window mean (t0, t1] of domain-mean profiles, bottom -> top."""
    fs = sorted(glob.glob(f"{R}/{case}/run/{case}.horiz_avg.AVERAGE.*.nc"))
    acc, tt = {n: [] for n in names}, []
    for f in fs:
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            tb = np.asarray(d["time_bnds"][:, 1])
            tt.append(tb)
            for n in names:
                acc[n].append(np.asarray(d[n + "_horiz_avg"][:]))
    t = np.concatenate(tt)
    t, iu = np.unique(t, return_index=True)
    h = (t - t[0]) * 24 + 0.25
    w = (h > t0 + 1e-6) & (h <= t1 + 1e-6)
    out = {}
    for n, v in acc.items():
        a = np.asarray(np.concatenate(v)[iu][w].mean(0)).squeeze()
        out[n] = a[::-1] if a.ndim >= 1 and a.size > 1 else float(a)
    return out


def obs_comparison():
    rows = []
    for _, r in off[(off.Nd_target == 50) & (off.sed == 1)].iterrows():
        g = ml[ml.case == r.case].sort_values("time_h")
        w = g[(g.time_h > 4) & (g.time_h <= 6 + 1e-6)]
        dzi = np.polyfit(w.time_h * 3600, w.zi, 1)[0]
        ws = float(np.interp(PS * np.exp(-G * w.zi.mean() / (RD * 287.0)), _p, _w))
        hv = horiz(r.case, ["z_mid", "p_mid", "qc2qr_autoconv", "qc2qr_accret", "precip_liq_surf_mass_flux"], 4, 6)
        dp = np.abs(np.gradient(hv["p_mid"]))
        prod = np.sum((hv["qc2qr_autoconv"] + hv["qc2qr_accret"]) * dp) / G * 86400
        psfc = float(hv["precip_liq_surf_mass_flux"]) * 86400e3
        rows.append({"res": r.res, "dx_km": r.dx_km, "precsupp": r.precsupp, "Nd_incloud_h10_12": r.Nd_incloud,
                     "zi_6h": g[(g.time_h > 5.75) & (g.time_h <= 6 + 1e-6)].zi.mean(), "zb_4_6": w.zb.mean(),
                     "LWP_4_6": w.LWP.mean(), "we_4_6_mm_s": (dzi - ws) * 1e3, "P_sfc_4_6_mm_d": psfc,
                     "rain_prod_4_6_mm_d": prod, "evap_frac_4_6": 1 - psfc / prod if prod > 1e-3 else np.nan})
    pd.DataFrame(rows).sort_values(["precsupp", "dx_km"], ascending=[False, False]).to_csv(f"{T}/obs_comparison.csv", index=False)


def budget_skill():
    rows = []
    b = B[B.turb3d == "off"].copy()
    key = ["dx_km", "sed", "precsupp", "t_end"]
    for v in ("pred", "obs"):
        b[f"anom_{v}"] = b[f"dlwp_dt_{v}"] - b.groupby(key)[f"dlwp_dt_{v}"].transform("mean")
    for dx, g in b.groupby("dx_km"):
        g12 = g[g.t_end == 12]
        rr = lambda x, y: np.corrcoef(x, y)[0, 1]
        rows.append({"dx_km": dx, "n": len(g),
                     "r_raw": rr(g.dlwp_dt_pred, g.dlwp_dt_obs),
                     "rmse_raw": np.sqrt(np.mean((g.dlwp_dt_pred - g.dlwp_dt_obs) ** 2)), "sd_obs": g.dlwp_dt_obs.std(),
                     "r_anom_all": rr(g.anom_pred, g.anom_obs),
                     "rmse_anom_all": np.sqrt(np.mean((g.anom_pred - g.anom_obs) ** 2)), "sd_anom_all": g.anom_obs.std(),
                     "r_anom_10_12": rr(g12.anom_pred, g12.anom_obs), "sd_anom_10_12": g12.anom_obs.std(),
                     "rmse_anom_10_12": np.sqrt(np.mean((g12.anom_pred - g12.anom_obs) ** 2))})
    pd.DataFrame(rows).sort_values("dx_km", ascending=False).to_csv(f"{T}/budget_skill.csv", index=False)


def matched_nd():
    rows = []
    for (dx, sed, ps), g in off.groupby(["dx_km", "sed", "precsupp"]):
        g = g.sort_values("Nd_incloud")
        x, y = np.log(g.Nd_incloud.values), np.log(g.LWP.values)
        for nd in (30, 50, 100, 200, 500, 800):
            v = np.exp(np.interp(np.log(nd), x, y, left=np.nan, right=np.nan))
            rows.append({"dx_km": dx, "sed": sed, "precsupp": ps, "Nd_ic": nd, "LWP": v})
    m = pd.DataFrame(rows)
    m.to_csv(f"{T}/matched_nd.csv", index=False)
    return m


def shocmix():
    rows = []
    for res in ("40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m", "312m"):
        case = f"sedps_{res}_nd200_sed1_pson"
        hv = horiz(case, ["z_mid", "p_mid", "T_mid", "qv", "shoc_mix", "nccn", "nc", "cldfrac_liq"], 10, 12)
        rho = hv["p_mid"] / (RD * hv["T_mid"] * (1 + 0.608 * hv["qv"]))
        zi = runs[runs.case == case].zi.iloc[0]
        cf = hv["cldfrac_liq"]
        for k in range(len(hv["z_mid"])):
            if hv["z_mid"][k] > 1500:
                break
            rows.append({"res": res, "dx_km": runs[runs.case == case].dx_km.iloc[0], "z": hv["z_mid"][k], "z_zi": hv["z_mid"][k] / zi,
                         "shoc_mix": hv["shoc_mix"][k], "nd_floor_cm3": 1.8824 * hv["nccn"][k] * rho[k] / 1e6,
                         "nd_incloud_cm3": hv["nc"][k] * rho[k] / cf[k] / 1e6 if cf[k] > 0.2 else np.nan, "cf": cf[k]})
    pd.DataFrame(rows).to_csv(f"{T}/shocmix.csv", index=False)


def dwe_sed():
    rows = []
    for (dx, nd, ps), g in off.groupby(["dx_km", "Nd_target", "precsupp"]):
        g = g.set_index("sed")
        rows.append({"dx_km": dx, "Nd_target": nd, "precsupp": ps, "Nd_incloud": g.Nd_incloud[1.0],
                     "dwe_sed": g.we_812_mm_s[2.0] - g.we_812_mm_s[0.5], "dLWP_sed": g.LWP[2.0] - g.LWP[0.5],
                     "dP_sed": g.precip[2.0] - g.precip[0.5]})
    pd.DataFrame(rows).to_csv(f"{T}/dwe_sed.csv", index=False)


def nd_stability():
    rows = []
    t3 = ts.dropna(subset=["Nd_med_3d_cm3"])
    for case, g in t3[t3.turb3d == "off"].groupby("case"):
        g = g.set_index("time_h")
        n6 = g.Nd_med_3d_cm3.get(6.0, np.nan)
        n12 = g.Nd_med_3d_cm3.get(12.0, np.nan)
        rows.append({"case": case, "dx_km": g.dx_km.iloc[0], "Nd_target": g.Nd_target.iloc[0], "ratio_12_6": n12 / n6})
    pd.DataFrame(rows).to_csv(f"{T}/nd_stability.csv", index=False)


def qsat(T_, p):
    es = 611.2 * np.exp(17.67 * (T_ - 273.15) / (T_ - 29.65))
    return 0.622 * es / (p - 0.378 * es)


def sfcflux_feedback():
    """Bulk-aerodynamic scaling, LHF ~ qs(Tg) - q_ml and SHF ~ Tg - T_air, calibrated to the
    prescribed 93 and 16 W m-2 with the initial mixed layer (theta_l = 288.3 K, q_t = 9.45 g/kg)."""
    p_s = PS
    ex = (p_s / P0) ** (RD / CP)
    qs0 = qsat(TG, p_s)
    dq0, dT0 = qs0 - 9.45e-3, TG - 288.3 * ex
    rows = []
    for _, r in off[(off.sed == 1)].iterrows():
        dq, dT = qs0 - r.qt_ml_gkg * 1e-3, TG - r.thl_ml * ex
        rows.append({"case": r.case, "dx_km": r.dx_km, "Nd_target": r.Nd_target, "precsupp": r.precsupp,
                     "LHF_est": 93 * dq / dq0, "SHF_est": 16 * dT / dT0, "thl_ml": r.thl_ml, "qt_ml": r.qt_ml_gkg})
    out = pd.DataFrame(rows)
    out.attrs["dq0"] = dq0
    out.to_csv(f"{T}/sfcflux_feedback.csv", index=False)
    print("initial qs(Tg) - q =", round(dq0 * 1e3, 2), "g/kg; Tg - T_air =", round(dT0, 2), "K")


def deposition():
    """Cloud-droplet flux at the lowest model level: s * rho * qc * v, with v the Stokes speed of the
    mean-volume radius (lower bound for the P3 mass-weighted speed of a gamma distribution)."""
    rows = []
    for _, r in off.iterrows():
        f = f"{R}/explore/npz/explore_{r.case}.npz"
        d = np.load(f)
        qc, rho, ncr = float(d["qc"][0]), float(d["rho"][0]), float(d["nc_rho"][0]) * 1e6   # m-3
        rv = (3 * qc * rho / (4 * np.pi * RHOW * ncr)) ** (1 / 3) if (qc > 1e-8 and ncr > 1e3) else 0.0
        v = 1.19e8 * rv ** 2
        dep = r.sed * rho * qc * v * 86400   # mm/day
        rows.append({"case": r.case, "dx_km": r.dx_km, "Nd_target": r.Nd_target, "sed": r.sed, "precsupp": r.precsupp,
                     "qc_lowest_gkg": qc * 1e3, "rv_um": rv * 1e6, "dep_mm_d": dep, "precip_mm_d": r.precip,
                     "dep_frac": dep / r.precip if r.precip > 1e-4 else np.nan})
    pd.DataFrame(rows).to_csv(f"{T}/deposition.csv", index=False)


def scene_se():
    rows = []
    for _, r in off[off.dx_km <= 5].iterrows():
        d = np.load(f"{R}/manuscript/fields/fields_{r.case}.npz")
        s = d["slope_scene"]
        rows.append({"case": r.case, "dx_km": r.dx_km, "Nd_target": r.Nd_target, "sed": r.sed, "precsupp": r.precsupp,
                     "Nd_incloud": r.Nd_incloud, "slope": s.mean(), "se": s.std(ddof=1) / np.sqrt(s.size) if s.size > 1 else np.nan,
                     "corr": d["corr_scene"].mean(), "n": s.size, "LWP_sd": r.LWP_sd_offline})
    pd.DataFrame(rows).to_csv(f"{T}/scene_se.csv", index=False)


def interaction():
    d = D[(D.turb3d == "off") & (D.sed == 1)].copy()
    d["interaction"] = d.dS_dsed_on - d.dS_dsed_off
    d[["branch", "dx_km", "S_on", "S_off", "S_ps", "S_sed", "S_resid", "dS_dsed_on", "dS_dsed_off", "interaction"]] \
        .to_csv(f"{T}/interaction.csv", index=False)


if __name__ == "__main__":
    obs_comparison(); budget_skill(); matched_nd(); shocmix(); dwe_sed(); nd_stability()
    sfcflux_feedback(); deposition(); scene_se(); interaction()
    print("done")
