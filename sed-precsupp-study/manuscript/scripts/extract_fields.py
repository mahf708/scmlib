#!/usr/bin/env python3
"""
Column-level statistics for the manuscript (run on a CPU compute node).

  extract_fields.py OUTDIR CASEDIR [CASEDIR ...]   -> OUTDIR/fields_<case>.npz

Per run, from the 15-min aci2d.INSTANT (column LWP, rain) and aerocom.INSTANT
(cloud-top liquid fraction, CDNC and r_eff weighted sums) streams:

  time series (every 15 min):
    t_h          hours since start
    cc           fraction of columns with LWP > 10 g m-2
    lwp_ic       mean LWP over those columns (g m-2)
    lwp_mean     domain-mean LWP (g m-2)
    nd_top_ic    mean cloud-top CDNC over columns with cf_top_liq > 0.5 (cm-3)
  hours 10-12 (instants in (10, 12]):
    lwp_hist     histogram of column LWP on log bins (lwp_edges)
    jh           joint histogram of (log10 Nd_top, log10 LWP) over columns with
                 cf_top_liq > 0.5 and LWP > 10 g m-2 (nd_edges x lwp_edges)
    jh_re        same for (log10 r_eff_top, log10 LWP)  (re_edges x lwp_edges)
    slope_scene  within-scene OLS slope d ln LWP / d ln Nd_top for those columns,
                 one per instant
    corr_scene   correlation of ln LWP and ln Nd_top, one per instant
  map: LWP at hour 12 on the physics grid (float32) for runs listed in MAPS.
"""
import glob
import os
import sys
from multiprocessing import Pool

import netCDF4
import numpy as np

LWP_EDGES = np.logspace(-1, 3.3, 87)          # 0.1 .. 2000 g m-2
ND_EDGES = np.logspace(0, 3.5, 71)            # 1 .. 3160 cm-3
RE_EDGES = np.logspace(0.3, 1.7, 57)          # 2 .. 50 um
MAPS = ("_nd20_sed1_pson", "_nd200_sed1_pson", "_nd1000_sed1_pson",
        "_nd20_sed1_psoff", "_nd200_sed1_psoff", "_nd1000_sed1_psoff")


def files(case, stream):
    name = os.path.basename(case)
    return sorted(glob.glob(f"{case}/run/{name}.{stream}.*.nc"))


def read_times(case, stream):
    """(hours, list of (file, index)) for every unique instant of a stream."""
    t0, seen, out = None, set(), []
    for f in files(case, stream):
        with netCDF4.Dataset(f) as d:
            tv = np.asarray(d["time"][:])
            if t0 is None:
                t0 = tv[0]
            for k, t in enumerate(tv):
                h = round(float((t - t0) * 24), 4)
                if h in seen:
                    continue
                seen.add(h)
                out.append((h, f, k))
    out.sort()
    return out


def one(case):
    name = os.path.basename(case)
    a2 = read_times(case, "aci2d.INSTANT")
    ac = {h: (f, k) for h, f, k in read_times(case, "aerocom.INSTANT")}
    with netCDF4.Dataset(a2[0][1]) as d:
        x, y = np.asarray(d["lon"][:]), np.asarray(d["lat"][:])
    out = {k: [] for k in ("t_h", "cc", "lwp_ic", "lwp_mean", "nd_top_ic", "slope_scene", "corr_scene")}
    lwp_hist = np.zeros(LWP_EDGES.size - 1)
    jh = np.zeros((ND_EDGES.size - 1, LWP_EDGES.size - 1))
    jh_re = np.zeros((RE_EDGES.size - 1, LWP_EDGES.size - 1))
    lwp12 = None
    for h, f, k in a2:
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            lwp = np.asarray(d["LiqWaterPath"][k], dtype=np.float64) * 1e3
        cl = lwp > 10.0
        out["t_h"].append(h)
        out["cc"].append(cl.mean())
        out["lwp_ic"].append(lwp[cl].mean() if cl.any() else np.nan)
        out["lwp_mean"].append(lwp.mean())
        nd_ic = np.nan
        if h in ac:
            fa, ka = ac[h]
            with netCDF4.Dataset(fa) as d:
                d.set_auto_mask(False)
                cf = np.asarray(d["cf_top_liq"][ka], dtype=np.float64)
                cd = np.asarray(d["cdnc_top_liq"][ka], dtype=np.float64)
                re = np.asarray(d["reff_top_liq"][ka], dtype=np.float64)
            ok = (cf > 0.5) & (cf <= 1.0)
            nd = np.where(ok, cd / np.where(ok, cf, 1), np.nan) / 1e6
            rr = np.where(ok, re / np.where(ok, cf, 1), np.nan)
            if ok.any():
                nd_ic = np.nanmean(nd)
            if 10.0 < h <= 12.0 + 1e-6:
                lwp_hist += np.histogram(np.clip(lwp, LWP_EDGES[0], None), LWP_EDGES)[0]
                sel = ok & cl & (nd > 0) & np.isfinite(nd) & (rr > 0)
                if sel.sum() > 20:
                    ln_n, ln_l = np.log(nd[sel]), np.log(lwp[sel])
                    jh += np.histogram2d(nd[sel], lwp[sel], [ND_EDGES, LWP_EDGES])[0]
                    jh_re += np.histogram2d(rr[sel], lwp[sel], [RE_EDGES, LWP_EDGES])[0]
                    if ln_n.std() > 1e-6:
                        out["slope_scene"].append(np.polyfit(ln_n, ln_l, 1)[0])
                        out["corr_scene"].append(np.corrcoef(ln_n, ln_l)[0, 1])
        out["nd_top_ic"].append(nd_ic)
        if abs(h - 12.0) < 1e-3 and any(name.endswith(m) for m in MAPS):
            lwp12 = lwp.astype(np.float32)
    res = {k: np.asarray(v) for k, v in out.items()}
    res.update(lwp_hist=lwp_hist, lwp_edges=LWP_EDGES, jh=jh, jh_re=jh_re, nd_edges=ND_EDGES,
               re_edges=RE_EDGES, ncol=x.size)
    if lwp12 is not None:
        res.update(lwp12=lwp12, x=x.astype(np.float32), y=y.astype(np.float32))
    np.savez(f"{OUT}/fields_{name}.npz", **res)
    return name


def safe(case):
    try:
        return one(case)
    except Exception as e:  # report and keep going
        return f"FAIL {os.path.basename(case)}: {e!r}"


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    with Pool(int(os.environ.get("NPROC", 32))) as p:
        for r in p.imap_unordered(safe, sys.argv[2:]):
            print(r, flush=True)
