#!/usr/bin/env python3
"""
Per-run diagnostics for the sed x precip-suppression study.

Reuses aci-res-study/analysis/analyze_runs.py:analyze() (LWP, rain, cloud
cover, z_i, w_e, process rates, Nd), and adds from the aerocom stream:
LWP spatial SD (online variance, and offline from the 2D LWP), liquid
cloud-top fraction, cloud-top CDNC and r_eff (weighted sums divided by the
cloud-top liquid fraction, domain-weighted).

Usage:  python3 analyze_sedps.py RUNROOT OUTDIR
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "../../aci-res-study/analysis"))
from analyze_runs import RES_KM, analyze, open_stream  # noqa: E402

# averaging window: the last 2 h of the run (SEDPS_TEND=12 for the 12 h set)
T_END = float(os.environ.get("SEDPS_TEND", 6))
PAT = re.compile(r"sedps_(\w+?)_nd(\d+)_sed(0p5|1|2)_ps(on|off)(_t3don)?$")
SED = {"0p5": 0.5, "1": 1.0, "2": 2.0}


def find_runs(root):
    runs = {}
    for d in sorted(glob.glob(f"{root}/sedps_*")):
        m = PAT.match(os.path.basename(d))
        if not m or m.group(1) not in RES_KM:
            continue
        f = glob.glob(f"{d}/run/{os.path.basename(d)}.horiz_avg.AVERAGE.*.nc")
        if not f or open_stream(d, "horiz_avg.AVERAGE").sizes["time"] < 4 * T_END:
            continue
        runs[(m.group(1), int(m.group(2)), m.group(3), m.group(4), "on" if m.group(5) else "off")] = d
    return runs


def aerocom(case):
    name = os.path.basename(case)
    a = open_stream(case, "aerocom.INSTANT")
    l2 = open_stream(case, "aci2d.INSTANT")
    th = (a.time.values - a.time.values[0]) / np.timedelta64(1, "h")
    late = (th > T_END - 2) & (th <= T_END)
    cf = a.cf_top_liq.values
    out = {
        "LWP_sd_online": np.sqrt(np.clip(a.lwp_var.values.squeeze()[late], 0, None)).mean() * 1e3,
        "LWP_sd_offline": (l2.LiqWaterPath.values[late].std(axis=1)).mean() * 1e3,
        "cf_top_liq": cf[late].mean(),
        # domain cloud-top means: sum of weighted sums / sum of weights
        "cdnc_top_cm3": a.cdnc_top_liq.values[late].sum() / cf[late].sum() / 1e6,
        "reff_top_um": a.reff_top_liq.values[late].sum() / cf[late].sum(),
        "T_top": a.T_top.values[late].sum() / a.cf_top.values[late].sum(),
    }
    ts = xr.Dataset({"LWP_sd": ("t2", np.sqrt(np.clip(a.lwp_var.values.squeeze(), 0, None)) * 1e3)},
                    coords={"t2": th})
    return ts, out


def main():
    root, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rows, series = [], []
    key = lambda kv: (-RES_KM[kv[0][0]], kv[0][1], SED[kv[0][2]], kv[0][3], kv[0][4])
    for (res, nd, sed, ps, t3d), case in sorted(find_runs(root).items(), key=key):
        ts, s = analyze(case, T_END)
        ts2, s2 = aerocom(case)
        rows.append({"res": res, "dx_km": RES_KM[res], "Nd_target": nd, "sed": SED[sed],
                     "precsupp": ps, "turb3d": t3d, **s, **s2, "case": os.path.basename(case)})
        series.append(xr.merge([ts, ts2]).expand_dims(run=[os.path.basename(case)]))
        print(f"{res:7s} Nd{nd:<4d} sed={sed:3s} ps={ps:3s} t3d={t3d:3s} LWP={s['LWP']:6.1f} sd={s2['LWP_sd_online']:5.1f} "
              f"cc={s['cloud_cover']:.2f} P={s['precip']:5.2f} we={s['we_mm_s']:5.2f} "
              f"Nd={s['Nd_incloud']:5.0f} cdnc_top={s2['cdnc_top_cm3']:5.0f} reff={s2['reff_top_um']:5.1f}")
    pd.DataFrame(rows).to_csv(f"{out}/summary_h{T_END - 2:g}-{T_END:g}.csv", index=False)
    xr.concat(series, dim="run", join="outer").to_netcdf(f"{out}/timeseries.nc")


if __name__ == "__main__":
    main()
