#!/usr/bin/env python3
"""
Column-level statistics over hours 10-12 for the revision (CPU compute node).

  rev2_cols.py OUTDIR CASEDIR [CASEDIR ...]  -> OUTDIR/cols_<case>.npz

Per run, for the 8 instants in (10, 12]:
  tiles        domain split into 4x4 square tiles (60 km for the 240 km domain); tile-mean LWP (8, 16)
  cc_tiles     tile cloud cover (LWP > 10 g m-2) (8, 16)
  Sufficient statistics (n, sx, sy, sxx, syy, sxy) of x = ln Nd, y = ln LWP for:
    top_f1   cloud-top Nd, filter cf_top > 0.5 and LWP > 10 g m-2 (filter used in the first version)
    top_f2   cloud-top Nd, satellite-like filter cf_top > 0.9, LWP > 20 g m-2, r_e < 15 um, tau > 3
    ret_f2   retrieval-like adiabatic Nd from column LWP and cloud-top r_e, same filter
    top_c4 / ret_c4  as *_f2 after averaging to 3.75 km blocks (dx <= 1.25 km only)
  Also mean of ln Nd_ret and ln Nd_top under f2 for the between-run analysis.
Adiabatic retrieval (Grosvenor et al., 2018): tau = 9 LWP / (5 rho_w r_e),
  Nd = sqrt(5)/(2 pi k) * sqrt(f_ad c_w tau / (Q rho_w r_e^5)), k = 0.8, Q = 2, f_ad = 1, c_w = 2e-6 kg m-4.
"""
import glob, os, sys
from multiprocessing import Pool
import netCDF4
import numpy as np

RHOW, K, Q, FAD, CW = 1000.0, 0.8, 2.0, 1.0, 2.0e-6


def times(case, stream):
    t0, seen, out = None, set(), []
    for f in sorted(glob.glob(f"{case}/run/{os.path.basename(case)}.{stream}.*.nc")):
        with netCDF4.Dataset(f) as d:
            tv = np.asarray(d["time"][:])
            if t0 is None:
                t0 = tv[0]
            for k, t in enumerate(tv):
                h = round(float((t - t0) * 24), 4)
                if 10 < h <= 12.0001 and h not in seen:
                    seen.add(h); out.append((h, f, k))
    return sorted(out)


def stats(x, y):
    return np.array([x.size, x.sum(), y.sum(), (x * x).sum(), (y * y).sum(), (x * y).sum()])


def retrieve(lwp_gm2, re_um):
    lwp, re = lwp_gm2 * 1e-3, re_um * 1e-6
    tau = 9 * lwp / (5 * RHOW * re)
    nd = np.sqrt(5) / (2 * np.pi * K) * np.sqrt(FAD * CW * tau / (Q * RHOW * re ** 5))
    return tau, nd / 1e6


def one(case):
    name = os.path.basename(case)
    a2 = times(case, "aci2d.INSTANT")
    ac = {h: (f, k) for h, f, k in times(case, "aerocom.INSTANT")}
    with netCDF4.Dataset(a2[0][1]) as d:
        x, y = np.asarray(d["lon"][:]), np.asarray(d["lat"][:])
    xs, ys = np.unique(x), np.unique(y)
    ix, iy = np.searchsorted(xs, x), np.searchsorted(ys, y)
    n = xs.size
    tile = (iy * 4 // n) * 4 + (ix * 4 // n)
    dxkm = (xs[1] - xs[0]) / 1e3 if n > 1 else 60.0
    blk = int(round(3.75 / dxkm)) if dxkm < 3.0 else 0
    acc = {k: np.zeros(6) for k in ("top_f1", "top_f2", "ret_f2", "top_c4", "ret_c4")}
    tiles, cct, mean_ret, mean_top, mean_lnl = [], [], [], [], []
    for h, f, k in a2:
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            lwp = np.asarray(d["LiqWaterPath"][k], dtype=np.float64) * 1e3
        tiles.append(np.bincount(tile, lwp, 16) / np.bincount(tile, None, 16))
        cct.append(np.bincount(tile, (lwp > 10).astype(float), 16) / np.bincount(tile, None, 16))
        if h not in ac:
            continue
        fa, ka = ac[h]
        with netCDF4.Dataset(fa) as d:
            d.set_auto_mask(False)
            cf = np.asarray(d["cf_top_liq"][ka], dtype=np.float64)
            cd = np.asarray(d["cdnc_top_liq"][ka], dtype=np.float64)
            re = np.asarray(d["reff_top_liq"][ka], dtype=np.float64)
        okc = (cf > 0.01) & (cf <= 1.0)
        ndt = np.where(okc, cd / np.where(okc, cf, 1), np.nan) / 1e6
        ret = np.where(okc, re / np.where(okc, cf, 1), np.nan)
        f1 = (cf > 0.5) & (cf <= 1) & (lwp > 10) & (ndt > 0)
        acc["top_f1"] += stats(np.log(ndt[f1]), np.log(lwp[f1]))
        tau, ndr = retrieve(lwp, np.where(ret > 0, ret, np.nan))
        f2 = (cf > 0.9) & (cf <= 1) & (lwp > 20) & (ret > 0) & (ret < 15) & (tau > 3) & (ndt > 0) & (ndr > 0)
        if f2.sum() > 0:
            acc["top_f2"] += stats(np.log(ndt[f2]), np.log(lwp[f2]))
            acc["ret_f2"] += stats(np.log(ndr[f2]), np.log(lwp[f2]))
            mean_ret.append(np.log(ndr[f2]).mean()); mean_top.append(np.log(ndt[f2]).mean()); mean_lnl.append(np.log(lwp[f2]).mean())
        if blk > 1:
            G = np.full((ys.size, xs.size), np.nan)
            def grid(v):
                g = G.copy(); g[iy, ix] = v
                m = n // blk * blk
                return g[:m, :m].reshape(m // blk, blk, m // blk, blk)
            lg, cg = grid(lwp), grid(np.where(okc, cf, 0))
            ng, rg = grid(np.where(okc, cd, 0)), grid(np.where(okc, re, 0))
            lb = lg.mean((1, 3)); cfb = cg.mean((1, 3))
            cldfrac_cols = (grid((lwp > 10).astype(float))).mean((1, 3))
            ndb = ng.sum((1, 3)) / np.maximum(cg.sum((1, 3)), 1e-9) / 1e6
            reb = rg.sum((1, 3)) / np.maximum(cg.sum((1, 3)), 1e-9)
            taub, ndrb = retrieve(lb, np.where(reb > 0, reb, np.nan))
            fb = (cldfrac_cols > 0.9) & (cfb > 0.9) & (lb > 20) & (reb > 0) & (reb < 15) & (taub > 3) & (ndb > 0) & (ndrb > 0)
            if fb.sum() > 0:
                acc["top_c4"] += stats(np.log(ndb[fb]), np.log(lb[fb]))
                acc["ret_c4"] += stats(np.log(ndrb[fb]), np.log(lb[fb]))
    np.savez(f"{OUT}/cols_{name}.npz", tiles=np.array(tiles), cc_tiles=np.array(cct),
             mean_lnret=np.nanmean(mean_ret) if mean_ret else np.nan, mean_lntop=np.nanmean(mean_top) if mean_top else np.nan,
             mean_lnlwp_f2=np.nanmean(mean_lnl) if mean_lnl else np.nan, **acc)
    return name


def safe(c):
    try:
        return one(c)
    except Exception as e:
        return f"FAIL {c} {e!r}"


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    with Pool(int(os.environ.get("NPROC", 32))) as p:
        for r in p.imap_unordered(safe, sys.argv[2:]):
            print(r, flush=True)
