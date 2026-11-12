#!/usr/bin/env python3
"""
Diagnostics from the 2-hourly 3D snapshots at 10 and 12 h (CPU compute node).

  rev2_3d.py OUTCSV CASEDIR [CASEDIR ...]

Per run (mean of the 10 h and 12 h snapshots):
  zi_snap            inversion height of the snapshot's domain-mean theta_l (midpoint method)
  wthl_res_min, wqt_res_at  resolved <w'thl'> (K m/s) minimum within zi-150..zi+50 m and <w'qt'> at that level
  z_fluxmin          height of that minimum
  inv_depth_mean     thickness of the domain-mean inversion: depth where dthl/dz > 20 % of its max (m)
  inv_depth_local    median over sampled columns of the same column-local thickness (m)
  sig_ztop           standard deviation of column cloud-top height (highest level with qc > 1e-5) (m)
  frac_qc_above      fraction of columns with qc > 1e-5 more than 50 m above zi
  enh_auto           <qc_ic^2.47>/<qc_ic>^2.47 over cloudy cells at the level of max mean qc
  Fsed_top_mmd       offline cloud-top droplet sedimentation flux (P3 gamma DSD, Stokes regime), mm/day,
                     domain mean, without the sedimentation factor
  Vsed_top           cloud-water-weighted mean mass-weighted fall speed at cloud top (m/s)
  frac_w_small       fraction of resolved w variance at 0.5 zi at wavelengths < 6 physics spacings
"""
import glob, os, sys
from multiprocessing import Pool
import netCDF4
import numpy as np
import pandas as pd

RD, CP, LV, G, P0, RHOW = 287.04, 1004.64, 2.501e6, 9.80616, 1.0e5, 1000.0


def inversion_height(z, thl):
    bl = thl[z < 400].mean()
    ft = np.interp(1400.0, z, thl)
    target = bl + 0.5 * (ft - bl)
    k = np.where((thl[:-1] < target) & (thl[1:] >= target) & (z[:-1] < 1500))[0]
    if not k.size:
        return np.nan
    k = k[0]
    return z[k] + (target - thl[k]) * (z[k + 1] - z[k]) / (thl[k + 1] - thl[k])


def depth_10_90(z, thl, zi):
    """Inversion thickness: depth over which d(theta_l)/dz exceeds 20 % of its maximum within zi +- 300 m."""
    sel = (z > zi - 300) & (z < zi + 300)
    zz, tt = z[sel], thl[sel]
    if zz.size < 4:
        return np.nan
    zc = 0.5 * (zz[1:] + zz[:-1])
    gr = np.diff(tt) / np.diff(zz)
    dz = np.diff(zz)
    m = gr.max()
    if m <= 0:
        return np.nan
    return float(dz[gr > 0.2 * m].sum())


def one(case):
    name = os.path.basename(case)
    fs = sorted(glob.glob(f"{case}/run/{name}.aci3d.INSTANT.*.nc"))
    with netCDF4.Dataset(sorted(glob.glob(f"{case}/run/{name}.aci2d.INSTANT.*.nc"))[0]) as d:
        x, y = np.asarray(d["lon"][:]), np.asarray(d["lat"][:])
    sed = float(name.split("_sed")[1].split("_")[0].replace("p", "."))
    res = []
    t0 = None
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
                g = lambda v: np.asarray(d[v][k], dtype=np.float64)[:, ::-1]     # (ncol, lev) bottom->top
                z, p, T, qv, qc, qr = g("z_mid"), g("p_mid"), g("T_mid"), g("qv"), g("qc"), g("qr")
                nc, cf, om = g("nc"), np.clip(g("cldfrac_liq"), 0, 1), g("omega")
                ex = (P0 / p) ** (RD / CP)
                thl = T * ex - LV / CP * ex * (qc + qr)
                qt = qv + qc + qr
                rho = p / (RD * T * (1 + 0.608 * qv))
                w = -om / (rho * G)
                zm = z.mean(0)
                thm = thl.mean(0)
                zi = inversion_height(zm, thm)
                out = {"zi_snap": zi}
                wp, tp, qp = w - w.mean(0), thl - thm, qt - qt.mean(0)
                fth, fqt = (wp * tp).mean(0), (wp * qp).mean(0)
                sel = (zm > zi - 150) & (zm < zi + 50)
                kk = np.where(sel)[0]
                kmin = kk[np.argmin(fth[kk])]
                out.update(wthl_res_min=fth[kmin], wqt_res_at=fqt[kmin], z_fluxmin=zm[kmin])
                out["inv_depth_mean"] = depth_10_90(zm, thm, zi)
                ii = np.linspace(0, z.shape[0] - 1, min(z.shape[0], 2048)).astype(int)
                out["inv_depth_local"] = float(np.nanmedian([depth_10_90(z[i], thl[i], zi) for i in ii]))
                cloudy = qc > 1e-5
                anyc = cloudy.any(1)
                ktop = np.where(anyc, z.shape[1] - 1 - np.argmax(cloudy[:, ::-1], axis=1), 0)
                icol = np.arange(z.shape[0])
                ztop = z[icol, ktop]
                out["sig_ztop"] = float(ztop[anyc].std()) if anyc.sum() > 2 else np.nan
                out["frac_qc_above"] = float((anyc & (ztop > zi + 50)).mean())
                kq = int(np.argmax(qc.mean(0)))
                c = cloudy[:, kq] & (cf[:, kq] > 0.01)
                if c.sum() > 0:
                    qic = qc[c, kq] / cf[c, kq]
                    out["enh_auto"] = float(np.mean(qic ** 2.47) / np.mean(qic) ** 2.47)
                else:
                    out["enh_auto"] = np.nan
                # offline cloud-top sedimentation flux (P3 cloud DSD, Stokes regime)
                qt_ = qc[icol, ktop]; nt_ = nc[icol, ktop]; ct_ = np.maximum(cf[icol, ktop], 1e-3)
                rt_ = rho[icol, ktop]; Tt_ = T[icol, ktop]
                ok = anyc & (qt_ > 1e-6) & (nt_ > 1e3)
                F = np.zeros(z.shape[0]); V = np.zeros(z.shape[0])
                if ok.any():
                    qic, nic = qt_[ok] / ct_[ok], nt_[ok] / ct_[ok]
                    mu = 0.0005714 * (nic * 1e-6 * rt_[ok]) + 0.2714
                    mu = np.clip(1.0 / mu ** 2 - 1.0, 2.0, 15.0)
                    lam = (np.pi * RHOW / 6.0 * nic * (mu + 3) * (mu + 2) * (mu + 1) / qic) ** (1.0 / 3.0)
                    lam = np.clip(lam, (mu + 1) * 2.5e4, (mu + 1) * 1e6)
                    visc = 1.496e-6 * Tt_[ok] ** 1.5 / (Tt_[ok] + 120.0) / rt_[ok]   # kinematic -> dynamic below
                    mu_air = visc * rt_[ok]
                    acn = G * RHOW / (18.0 * mu_air)
                    Vm = acn * (mu + 5) * (mu + 4) / lam ** 2
                    V[ok] = Vm
                    F[ok] = rt_[ok] * qt_[ok] * Vm
                out["Fsed_top_mmd"] = float(F.mean() * 86400)
                wq = qt_ * ok
                out["Vsed_top"] = float((V * wq).sum() / max(wq.sum(), 1e-30))
                # resolved w spectrum at 0.5 zi
                xs, ys = np.unique(x), np.unique(y)
                if xs.size >= 16:
                    k5 = int(np.argmin(np.abs(zm - 0.5 * zi)))
                    img = np.zeros((ys.size, xs.size))
                    img[np.searchsorted(ys, y), np.searchsorted(xs, x)] = wp[:, k5]
                    ps = np.abs(np.fft.fft2(img)) ** 2
                    dxp = xs[1] - xs[0]
                    fx = np.fft.fftfreq(xs.size, dxp)
                    kx, ky = np.meshgrid(fx, np.fft.fftfreq(ys.size, dxp))
                    kk_ = np.hypot(kx, ky)
                    small = kk_ > 1.0 / (6 * dxp)
                    out["frac_w_small"] = float(ps[small].sum() / ps[kk_ > 0].sum())
                else:
                    out["frac_w_small"] = np.nan
                res.append(out)
    df = pd.DataFrame(res)
    row = df.mean().to_dict()
    row["case"] = name
    return row


def safe(c):
    try:
        return one(c)
    except Exception as e:
        print("FAIL", c, repr(e), flush=True)
        return None


if __name__ == "__main__":
    with Pool(int(os.environ.get("NPROC", 16))) as p:
        rows = [r for r in p.map(safe, sys.argv[2:]) if r]
    pd.DataFrame(rows).to_csv(sys.argv[1], index=False)
    print(len(rows))
