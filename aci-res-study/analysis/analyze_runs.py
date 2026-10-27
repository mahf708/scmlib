#!/usr/bin/env python3
"""
Per-run diagnostics and Nd/resolution summaries for the ACI study.

For each run (res, Nd, turb3d) found under RUNROOT this computes, from the
15-min horizontal-average stream, the 15-min column 2D stream and the 2-hourly
3D snapshots:

  LWP, RWP, surface rain, cloud cover (LWP > 10 g/m2), inversion height z_i
  (theta_l midway between the boundary layer and the free troposphere), cloud
  base, entrainment rate w_e = dz_i/dt - w_subs(z_i), column autoconversion and
  accretion, SHOC (subgrid) and resolved w variance, and in-cloud Nd.

Averages over hours 4-6 go to a CSV; time series go to a .nc file.

Usage:
  python3 analyze_runs.py RUNROOT OUTDIR
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd
import xarray as xr

G, RD = 9.80616, 287.04
IOP_FILE = "/global/cfs/cdirs/e3sm/inputdata/atm/cam/scam/iop/DYCOMSrf02_iopfile_4scam.nc"
RES_KM = {"40km": 40, "20km": 20, "10km": 10, "5km": 5, "2p5km": 2.5,
          "1p25km": 1.25, "625m": 0.625, "312m": 0.3125, "156m": 0.15625}


def find_runs(root):
    """Map (res, nd, turb3d) -> case dir. Prefer the newest naming (tt2_)."""
    runs = {}
    pats = [r"tt_aci_(\w+?)_nd(\d+)_t3d(on|off)(_sice)?$",
            r"tt2_(\w+?)_nd(\d+)_t3d(on|off)$"]
    for d in sorted(glob.glob(f"{root}/tt*")):
        name = os.path.basename(d)
        for pat in pats:
            m = re.match(pat, name)
            if m and m.group(1) in RES_KM:
                key = (m.group(1), int(m.group(2)), m.group(3))
                files = glob.glob(f"{d}/run/{name}.horiz_avg.AVERAGE*.nc")
                if not files:
                    continue
                h = xr.open_dataset(files[0])
                if h.sizes["time"] < 24:  # only full 6 h runs
                    continue
                if key not in runs or name.startswith("tt2_"):
                    runs[key] = d
    return runs


def inversion_height(z, thl):
    """Height where theta_l crosses the midpoint of the inversion jump."""
    bl = thl[z < 400].mean()
    ft = np.interp(1400.0, z, thl)
    target = bl + 0.5 * (ft - bl)
    k = np.where((thl[:-1] < target) & (thl[1:] >= target) & (z[:-1] < 1500))[0]
    if not k.size:
        return np.nan
    k = k[0]
    return z[k] + (target - thl[k]) * (z[k + 1] - z[k]) / (thl[k + 1] - thl[k])


def column_integral(rate, p):
    """Mass-weighted column integral of a (kg/kg)/s rate -> mm/day."""
    dp = np.abs(np.gradient(p, axis=-1))
    return (rate * dp).sum(axis=-1) / G * 86400.0


def analyze(case):
    name = os.path.basename(case)
    h = xr.open_dataset(glob.glob(f"{case}/run/{name}.horiz_avg.AVERAGE*.nc")[0])
    a = xr.open_dataset(glob.glob(f"{case}/run/{name}.aci2d.INSTANT*.nc")[0])
    d3 = xr.open_dataset(glob.glob(f"{case}/run/{name}.aci3d.INSTANT*.nc")[0])

    t = (h.time_bnds.values.astype("datetime64[s]").astype(float).mean(axis=1)
         - h.time_bnds.values[0, 0].astype("datetime64[s]").astype(float)) / 3600.0
    z = h.z_mid_horiz_avg.values
    p = h.p_mid_horiz_avg.values
    T = h.T_mid_horiz_avg.values
    # The large-scale subsidence is applied as an IOP forcing tendency, so the
    # model's domain-mean omega does not contain it: take it from the IOP file.
    iop = xr.open_dataset(IOP_FILE, decode_times=False)
    p_iop = iop.lev.values
    w_iop = -iop.omega.isel(time=0).squeeze().values / (p_iop / (RD * iop["T"].isel(time=0).squeeze().values) * G)

    zi = np.array([inversion_height(z[i][::-1], h.LiqPotentialTemperature_horiz_avg.values[i][::-1])
                   for i in range(len(t))])
    p_zi = np.array([np.interp(zi[i], z[i][::-1], p[i][::-1]) for i in range(len(t))])
    w_zi = np.interp(p_zi, p_iop, w_iop)
    cf = h.cldfrac_liq_horiz_avg.values
    zb = []
    for i in range(len(t)):
        zz, cc = z[i][::-1], cf[i][::-1]
        k = np.where(cc >= 0.5 * cc.max())[0]
        zb.append(zz[k[0]] if k.size and cc.max() > 0.05 else np.nan)
    zb = np.array(zb)

    # subgrid (SHOC) w variance averaged over the boundary layer
    w2_sgs = np.array([h.w_variance_horiz_avg.values[i][(z[i] < zi[i])].mean() for i in range(len(t))])

    ts = xr.Dataset(
        {
            "LWP": ("t", h.LiqWaterPath_horiz_avg.values.squeeze() * 1e3),
            "RWP": ("t", h.RainWaterPath_horiz_avg.values.squeeze() * 1e3),
            "precip": ("t", h.precip_liq_surf_mass_flux_horiz_avg.values.squeeze() * 86400e3),
            "zi": ("t", zi),
            "zb": ("t", zb),
            "w_subs_zi": ("t", w_zi),
            "autoconv": ("t", column_integral(h.qc2qr_autoconv_horiz_avg.values, p)),
            "accret": ("t", column_integral(h.qc2qr_accret_horiz_avg.values, p)),
            "w2_sgs_bl": ("t", w2_sgs),
            "tke_max": ("t", h.tke_horiz_avg.values.max(axis=1)),
        },
        coords={"t": t},
    )

    lwp2d = a.LiqWaterPath.values * 1e3
    ts_cc = (lwp2d > 10.0).mean(axis=1)
    t2d = (a.time.values - a.time.values[0]).astype("timedelta64[s]").astype(float) / 3600.0

    # in-cloud Nd and resolved w variance from the 3D snapshots
    nd_med, w2_res = {}, {}
    for k in range(1, d3.sizes["time"]):
        s = d3.isel(time=k)
        hr = round(float((d3.time.values[k] - d3.time.values[0]) / np.timedelta64(1, "h")))
        r3 = s.p_mid / (RD * s.T_mid * (1 + 0.608 * s.qv))
        m = (s.qc > 1e-5) & (s.cldfrac_liq > 0.01)
        nd = (s.nc / s.cldfrac_liq.where(m) * r3 / 1e6).values
        nd_med[hr] = np.nanmedian(nd)
        w = (-s.omega / (r3 * G)).values  # (ncol, lev)
        zz = s.z_mid.values.mean(axis=0)
        zi_hr = float(np.interp(hr, t, zi))
        w2_res[hr] = w.var(axis=0)[zz < zi_hr].mean()

    late = (t > 4.0) & (t <= 6.0)
    fit = np.polyfit(t[(t >= 2.0)], zi[(t >= 2.0)], 1)
    summary = {
        "LWP": ts.LWP.values[late].mean(),
        "RWP": ts.RWP.values[late].mean(),
        "precip": ts.precip.values[late].mean(),
        "cloud_cover": ts_cc[(t2d > 4.0) & (t2d <= 6.0)].mean(),
        "zi": zi[late].mean(),
        "zb": np.nanmean(zb[late]),
        "dzi_dt_mm_s": fit[0] / 3.6,
        "w_subs_mm_s": w_zi[t >= 2.0].mean() * 1e3,
        "autoconv": ts.autoconv.values[late].mean(),
        "accret": ts.accret.values[late].mean(),
        "w2_sgs_bl": w2_sgs[late].mean(),
        "w2_res_bl": np.mean([w2_res[k] for k in (4, 6) if k in w2_res]),
        "Nd_incloud": np.mean([nd_med[k] for k in (4, 6) if k in nd_med]),
    }
    summary["we_mm_s"] = summary["dzi_dt_mm_s"] - summary["w_subs_mm_s"]
    return ts, summary


def main():
    root, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rows, series = [], []
    for (res, nd, t3d), case in sorted(find_runs(root).items(), key=lambda kv: (-RES_KM[kv[0][0]], kv[0][1], kv[0][2])):
        ts, s = analyze(case)
        rows.append({"res": res, "dx_km": RES_KM[res], "Nd_target": nd, "turb3d": t3d, **s,
                     "case": os.path.basename(case)})
        series.append(ts.expand_dims(run=[f"{res}_nd{nd}_{t3d}"]))
        print(f"{res:7s} Nd{nd:<4d} t3d={t3d:3s} LWP={s['LWP']:6.1f} cc={s['cloud_cover']:.2f} "
              f"P={s['precip']:5.2f} we={s['we_mm_s']:5.2f} zi={s['zi']:5.0f} Nd={s['Nd_incloud']:5.0f}")
    df = pd.DataFrame(rows)
    df.to_csv(f"{out}/summary_h4-6.csv", index=False)
    ts_all = xr.concat(series, dim="run", join="outer")
    ts_all.to_netcdf(f"{out}/timeseries.nc")
    ts_all.to_dataframe().reset_index().to_csv(f"{out}/timeseries.csv", index=False)


if __name__ == "__main__":
    main()
