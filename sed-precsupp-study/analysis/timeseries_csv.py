#!/usr/bin/env python3
"""
One long CSV of 15-min time series for every sedps run, with the run's
characteristics as columns.  Usage: timeseries_csv.py RUNROOT OUTCSV

time_h is the end of each 15-min interval (instant fields are at time_h;
averaged fields are the average over (time_h-0.25, time_h]).

Nd columns:
  Nd_top_cm3        AeroCom liquid cloud-top in-cloud CDNC, domain mean
                    (sum of weighted sums / sum of cloud-top liquid fraction)
  Nd_layer_cm3      in-cloud Nd of the domain-mean profile, averaged over levels
                    with domain-mean cldfrac_liq > 0.5: <nc>*rho/<cldfrac_liq>
  Nd_med_3d_cm3     median in-cloud Nd over all cloudy grid cells (qc>1e-5), from
                    the 2-hourly 3D snapshots only (empty at other times)
"""
import glob
import os
import sys

import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_sedps import find_runs, SED  # noqa: E402
from analyze_runs import RES_KM, RD, G, inversion_height, open_stream  # noqa: E402


def one(case):
    name = os.path.basename(case)
    op = lambda s: open_stream(case, s)
    h, a2, ac, d3 = op("horiz_avg.AVERAGE"), op("aci2d.INSTANT"), op("aerocom.INSTANT"), op("aci3d.INSTANT")
    t0 = a2.time.values[0]
    hr = lambda t: np.round((t - t0) / np.timedelta64(1, "h"), 4)
    t_end = hr(h.time_bnds.values[:, 1])
    t_ins = hr(a2.time.values)

    p = h.p_mid_horiz_avg.values
    T = h.T_mid_horiz_avg.values
    qv = h.qv_horiz_avg.values
    rho = p / (RD * T * (1 + 0.608 * qv))
    cf = h.cldfrac_liq_horiz_avg.values
    m = cf > 0.5
    nd_layer = np.where(m, h.nc_horiz_avg.values * rho / np.where(m, cf, 1), np.nan)
    z = h.z_mid_horiz_avg.values
    thl = h.LiqPotentialTemperature_horiz_avg.values
    zi = [inversion_height(z[i][::-1], thl[i][::-1]) for i in range(len(t_end))]
    avg = pd.DataFrame({
        "time_h": t_end,
        "LWP_gm2": h.LiqWaterPath_horiz_avg.values.squeeze() * 1e3,
        "RWP_gm2": h.RainWaterPath_horiz_avg.values.squeeze() * 1e3,
        "precip_mmday": h.precip_liq_surf_mass_flux_horiz_avg.values.squeeze() * 86400e3,
        "zi_m": zi,
        "Nd_layer_cm3": np.nanmean(nd_layer, axis=1) / 1e6,
    })
    cft = ac.cf_top_liq.values
    lwp2d = a2.LiqWaterPath.values * 1e3
    ins = pd.DataFrame({
        "time_h": t_ins,
        "LWP_inst_gm2": ac.lwp_mean.values.squeeze() * 1e3,
        "LWP_sd_gm2": np.sqrt(np.clip(ac.lwp_var.values.squeeze(), 0, None)) * 1e3,
        "cloud_cover": (lwp2d > 10).mean(axis=1),
        "cf_top_liq": np.nanmean(np.where(cft > 1, np.nan, cft), axis=1),
        "Nd_top_cm3": [np.nan if np.nansum(np.where(c > 1, 0, c)) == 0 else
                       np.nansum(np.where(c > 1, 0, n)) / np.nansum(np.where(c > 1, 0, c)) / 1e6
                       for c, n in zip(cft, ac.cdnc_top_liq.values)],
        "reff_top_um": [np.nan if np.nansum(np.where(c > 1, 0, c)) == 0 else
                        np.nansum(np.where(c > 1, 0, r)) / np.nansum(np.where(c > 1, 0, c))
                        for c, r in zip(cft, ac.reff_top_liq.values)],
    })
    med = []
    for k in range(d3.sizes["time"]):
        s = d3.isel(time=k)
        r3 = s.p_mid / (RD * s.T_mid * (1 + 0.608 * s.qv))
        mm = (s.qc > 1e-5) & (s.cldfrac_liq > 0.01)
        nd = (s.nc / s.cldfrac_liq.where(mm) * r3 / 1e6).values
        med.append({"time_h": hr(d3.time.values[k]),
                    "Nd_med_3d_cm3": np.nanmedian(nd) if np.isfinite(nd).any() else np.nan})
    df = ins.merge(avg, on="time_h", how="outer").merge(pd.DataFrame(med), on="time_h", how="left")
    return df.sort_values("time_h")


def main():
    root, outcsv = sys.argv[1], sys.argv[2]
    frames = []
    for (res, nd, sed, ps, t3d), case in find_runs(root).items():
        df = one(case)
        df.insert(0, "case", os.path.basename(case))
        df.insert(1, "res", res)
        df.insert(2, "dx_km", RES_KM[res])
        df.insert(3, "Nd_target", nd)
        df.insert(4, "sed_factor", SED[sed])
        df.insert(5, "precip_suppression", ps)
        df.insert(6, "turb3d", t3d)
        frames.append(df)
        print(os.path.basename(case), len(df))
    out = pd.concat(frames)
    out = out.sort_values(["dx_km", "Nd_target", "sed_factor", "precip_suppression", "time_h"],
                          ascending=[False, True, True, False, True])
    out.round(4).to_csv(outcsv, index=False)
    print(outcsv, out.shape)


if __name__ == "__main__":
    main()
