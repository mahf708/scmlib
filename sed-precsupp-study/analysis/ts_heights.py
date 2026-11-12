#!/usr/bin/env python3
"""
15-min cloud-top / cloud-base heights for every 12 h run.
  ts_heights.py OUTCSV CASEDIR [CASEDIR ...]
Columns: case, time_h, z_top_aerocom_m (AeroCom liquid-or-ice cloud-top pressure
seen from above, cloud-fraction weighted over the domain, mapped to height with
the domain-mean p-z profile), z_top_qc_m / z_base_qc_m (highest / lowest level
where domain-mean qc >= 10 % of its column maximum, from the 15-min means).
"""
import glob, os, sys
import numpy as np, netCDF4, pandas as pd
from multiprocessing import Pool


def files(case, stream):
    n = os.path.basename(case)
    return sorted(glob.glob(f"{case}/run/{n}.{stream}.*.nc"))


def cat(case, stream, names):
    tt, out = [], {k: [] for k in names}
    for f in files(case, stream):
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            tt.append(d["time"][:])
            for k in names:
                out[k].append(d[k][:])
    t = np.concatenate(tt); t, iu = np.unique(t, return_index=True)
    return t, {k: np.concatenate(v)[iu] for k, v in out.items()}


def one(case):
    try:
        t, h = cat(case, "horiz_avg.AVERAGE", ["z_mid_horiz_avg", "p_mid_horiz_avg", "qc_horiz_avg"])
        th = (t - t[0]) * 24 + 0.25 if len(t) else t
        rows = {}
        for i in range(len(t)):
            z = h["z_mid_horiz_avg"][i].squeeze(); qc = h["qc_horiz_avg"][i].squeeze()
            k = np.where((qc >= 0.1 * qc.max()) & (z < 2000))[0] if qc.max() > 1e-7 else np.array([])
            rows[round(th[i], 3)] = {"z_top_qc_m": z[k].max() if k.size else np.nan,
                                     "z_base_qc_m": z[k].min() if k.size else np.nan}
        # AeroCom cloud-top pressure (weighted sum) / cloud-top fraction -> p_top -> z via mean profile
        ta, a = cat(case, "aerocom.INSTANT", ["p_top", "cf_top"])
        tha = (ta - ta[0]) * 24
        pz_t = (t - t[0]) * 24 + 0.125     # mid-time of the 15-min means
        for i in range(len(ta)):
            pt, cf = a["p_top"][i], a["cf_top"][i]
            ok = (cf > 0) & (cf <= 1) & (pt < 1e30)
            if not ok.any():
                continue
            ptop = pt[ok].sum() / cf[ok].sum()
            j = int(np.argmin(np.abs(pz_t - tha[i])))
            p = h["p_mid_horiz_avg"][j].squeeze(); z = h["z_mid_horiz_avg"][j].squeeze()
            o = np.argsort(p)
            key = round(tha[i], 3)
            rows.setdefault(key, {"z_top_qc_m": np.nan, "z_base_qc_m": np.nan})
            rows[key]["z_top_aerocom_m"] = float(np.interp(ptop, p[o], z[o]))
        df = pd.DataFrame.from_dict(rows, orient="index").rename_axis("time_h").reset_index()
        df.insert(0, "case", os.path.basename(case))
        return df
    except Exception as e:
        print("FAIL", case, repr(e), flush=True)
        return None


if __name__ == "__main__":
    out, cases = sys.argv[1], sys.argv[2:]
    with Pool(int(os.environ.get("NPROC", 32))) as p:
        dfs = [d for d in p.map(one, cases) if d is not None]
    pd.concat(dfs).sort_values(["case", "time_h"]).round(2).to_csv(out, index=False)
    print("wrote", out, len(dfs), "runs")
