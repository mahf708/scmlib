#!/usr/bin/env python3
"""
Cloud cover that includes SHOC's subgrid liquid cloud fraction, from the 2-hourly 3D
snapshots (run on a CPU compute node).  For each column, the maximum-overlap cloud cover
is max_k(cldfrac_liq); the random-overlap value is 1 - prod_k(1 - cldfrac_liq).  Domain
means at 10 and 12 h are averaged.  Also the fraction of columns with LWP-independent
cloud (max cf > 0.5) for comparison with the LWP > 10 g m-2 definition.

  cloudcover_3d.py OUTCSV CASEDIR [CASEDIR ...]
"""
import glob, os, sys
from multiprocessing import Pool
import netCDF4
import numpy as np
import pandas as pd


def one(case):
    name = os.path.basename(case)
    fs = sorted(glob.glob(f"{case}/run/{name}.aci3d.INSTANT.*.nc"))
    t0, vals = None, {"cc_max": [], "cc_rand": [], "cc_cf05": []}
    for f in fs:
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            tv = np.asarray(d["time"][:])
            if t0 is None:
                t0 = tv[0]
            for k, t in enumerate(tv):
                h = (t - t0) * 24
                if not (9.99 <= h <= 12.01):
                    continue
                cf = np.clip(np.asarray(d["cldfrac_liq"][k], dtype=np.float32), 0, 1)   # (ncol, lev)
                cmax = cf.max(axis=1)
                vals["cc_max"].append(cmax.mean())
                vals["cc_rand"].append((1 - np.prod(1 - cf, axis=1)).mean())
                vals["cc_cf05"].append((cmax > 0.5).mean())
    return {"case": name, **{k: float(np.mean(v)) if v else np.nan for k, v in vals.items()}}


if __name__ == "__main__":
    with Pool(int(os.environ.get("NPROC", 16))) as p:
        rows = p.map(one, sys.argv[2:])
    pd.DataFrame(rows).to_csv(sys.argv[1], index=False)
    print(len(rows))
