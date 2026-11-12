#!/usr/bin/env python3
"""
15-min mixed-layer time series from the domain-mean profiles (horiz_avg.AVERAGE),
for the mixed-layer LWP budget (run on a CPU compute node).

  profiles_ts.py OUTCSV CASEDIR [CASEDIR ...]

Columns: case, time_h (end of the 15-min interval), zi (theta_l midpoint, m),
zb (lowest level with cldfrac_liq >= 0.5 of its max, m), thl_ml and qt_ml (means over
0.1-0.8 z_i; K, g/kg), dthl_inv and dqt_inv (value 100 m above z_i minus the mixed-layer
mean), rho_zi, p_zb (Pa), F_rad (radiative cooling of the layer below z_i+150 m, W m-2),
P_sfc (surface rain, W m-2), LWP (g m-2), SHF and LHF (surface fluxes, W m-2).
"""
import glob
import os
import sys
from multiprocessing import Pool

import netCDF4
import numpy as np
import pandas as pd

RD, CP, LV = 287.04, 1004.64, 2.501e6
VARS = ["z_mid", "p_mid", "T_mid", "qv", "qc", "qr", "cldfrac_liq", "LiqPotentialTemperature",
        "rrtmgp_T_mid_tend", "precip_liq_surf_mass_flux", "LiqWaterPath", "surf_sens_flux",
        "surface_upward_latent_heat_flux"]


def inversion_height(z, thl):
    bl = thl[z < 400].mean()
    ft = np.interp(1400.0, z, thl)
    target = bl + 0.5 * (ft - bl)
    k = np.where((thl[:-1] < target) & (thl[1:] >= target) & (z[:-1] < 1500))[0]
    if not k.size:
        return np.nan
    k = k[0]
    return z[k] + (target - thl[k]) * (z[k + 1] - z[k]) / (thl[k + 1] - thl[k])


def one(case):
    name = os.path.basename(case)
    fs = sorted(glob.glob(f"{case}/run/{name}.horiz_avg.AVERAGE.*.nc"))
    tt, data = [], {v: [] for v in VARS}
    for f in fs:
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            tt.append(np.asarray(d["time_bnds"][:, 1]))
            for v in VARS:
                data[v].append(np.asarray(d[v + "_horiz_avg"][:]))
    t = np.concatenate(tt)
    t, iu = np.unique(t, return_index=True)
    data = {v: np.concatenate(x)[iu] for v, x in data.items()}
    hrs = np.round((t - t[0]) * 24 + 0.25, 3)
    rows = []
    for i, h in enumerate(hrs):
        P = lambda v: np.squeeze(data[v][i])[::-1] if np.ndim(np.squeeze(data[v][i])) else float(np.squeeze(data[v][i]))
        z, p, T, qv = P("z_mid"), P("p_mid"), P("T_mid"), P("qv")
        thl, cf = P("LiqPotentialTemperature"), P("cldfrac_liq")
        qt = qv + P("qc") + P("qr")
        rho = p / (RD * T * (1 + 0.608 * qv))
        dz = np.abs(np.gradient(z))
        zi = inversion_height(z, thl)
        k = np.where(cf >= 0.5 * cf.max())[0]
        zb = z[k[0]] if (k.size and cf.max() > 0.05) else np.nan
        ml = (z > 0.1 * zi) & (z < 0.8 * zi)
        rows.append({
            "case": name, "time_h": h, "zi": zi, "zb": zb,
            "thl_ml": thl[ml].mean(), "qt_ml": qt[ml].mean() * 1e3,
            "dthl_inv": np.interp(zi + 100, z, thl) - thl[ml].mean(),
            "dqt_inv": (np.interp(zi + 100, z, qt) - qt[ml].mean()) * 1e3,
            "rho_zi": np.interp(zi, z, rho), "p_zb": np.interp(zb, z, p) if np.isfinite(zb) else np.nan,
            "F_rad": -np.sum((rho * CP * P("rrtmgp_T_mid_tend") * dz)[z < zi + 150]),
            "P_sfc": P("precip_liq_surf_mass_flux") * 1000 * LV,
            "LWP": P("LiqWaterPath") * 1e3,
            "SHF": P("surf_sens_flux"), "LHF": P("surface_upward_latent_heat_flux"),
        })
    return pd.DataFrame(rows)


def safe(case):
    try:
        return one(case)
    except Exception as e:
        print("FAIL", case, repr(e), flush=True)
        return None


if __name__ == "__main__":
    out = sys.argv[1]
    with Pool(int(os.environ.get("NPROC", 32))) as p:
        frames = [f for f in p.map(safe, sys.argv[2:]) if f is not None]
    pd.concat(frames).round(5).to_csv(out, index=False)
    print(out, len(frames), "runs")
