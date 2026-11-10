#!/usr/bin/env python3
"""
Process-level diagnostics for every finished 12 h run (hours 10-12).

  explore.py OUTDIR CASEDIR [CASEDIR ...]     -> OUTDIR/explore_<case>.npz
  (run on a CPU node; process many cases in parallel with multiprocessing)

Per run, from the 15-min domain-mean profiles (window mean), the 2-hourly 3D
snapshots at 10 and 12 h, and the 15-min column LWP / rain:
  profiles: z, thl, qt, cldfrac_liq, qc, qr, w2_sgs, tke_sgs, sgs_buoy_flux,
            w2_res, wthv_res, w3_res, rad_heat (K/s), autoconv, accret, evap
  scalars : zi, zb, cloud thickness, decoupling dqt/dthl, resolved fraction of
            BL w-variance, w skewness at 0.5 zi, cloud-top sedimentation flux,
            cloud-base rain flux, column autoconversion/accretion/evaporation,
            surface rain, LW radiative cooling of the BL, raining fraction,
            dominant LWP wavelength.
"""
import glob
import os
import sys
import numpy as np
import netCDF4
from multiprocessing import Pool

G, RD, CP, P0 = 9.80616, 287.04, 1004.64, 1.0e5
T_END = 12.0


def files(case, stream):
    name = os.path.basename(case)
    return sorted(glob.glob(f"{case}/run/{name}.{stream}.*.nc"))


def read(case, stream, names, tsel=None):
    """Concatenate a stream's segment files in time; return hours and arrays."""
    tt, out = [], {n: [] for n in names}
    for f in files(case, stream):
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            t = d["time"][:]
            if "time_bnds" in d.variables:
                t = d["time_bnds"][:, 1]
            tt.append(t)
            for n in names:
                out[n].append(d[n][:])
    t = np.concatenate(tt)
    t, iu = np.unique(t, return_index=True)
    res = {n: np.concatenate(out[n])[iu] for n in names}
    return t, res


def inversion_height(z, thl):
    bl = thl[z < 400].mean()
    ft = np.interp(1400.0, z, thl)
    target = bl + 0.5 * (ft - bl)
    k = np.where((thl[:-1] < target) & (thl[1:] >= target) & (z[:-1] < 1500))[0]
    if not k.size:
        return np.nan
    k = k[0]
    return z[k] + (target - thl[k]) * (z[k + 1] - z[k]) / (thl[k + 1] - thl[k])


def peak_wavelength(img, dx):
    a = np.nan_to_num(img - np.nanmean(img))
    ps = np.abs(np.fft.fft2(a)) ** 2
    f = np.fft.fftfreq(a.shape[0], dx)
    ky, kx = np.meshgrid(f, np.fft.fftfreq(a.shape[1], dx), indexing="ij")
    k = np.hypot(kx, ky)
    bins = f[1:a.shape[0] // 2]
    spec = np.array([ps[(k >= b - bins[0] / 2) & (k < b + bins[0] / 2)].mean() for b in bins])
    return 1.0 / bins[np.argmax(spec)], bins, spec


def one(case):
    name = os.path.basename(case)
    out = {}
    # ---- domain-mean profiles, hours 10-12 ----
    hv = ["z_mid_horiz_avg", "p_mid_horiz_avg", "T_mid_horiz_avg", "qv_horiz_avg", "qc_horiz_avg", "qr_horiz_avg",
          "nc_horiz_avg", "cldfrac_liq_horiz_avg", "LiqPotentialTemperature_horiz_avg", "w_variance_horiz_avg",
          "tke_horiz_avg", "sgs_buoy_flux_horiz_avg", "rrtmgp_T_mid_tend_horiz_avg", "qc2qr_autoconv_horiz_avg",
          "qc2qr_accret_horiz_avg", "qr2qv_evap_horiz_avg", "qc_sed_horiz_avg", "qr_sed_horiz_avg",
          "precip_liq_surf_mass_flux_horiz_avg", "wthl_sec_horiz_avg", "wqw_sec_horiz_avg"]
    t, h = read(case, "horiz_avg.AVERAGE", hv)
    hrs = np.round((t - (t[0] - 0.25 / 24)) * 24, 3)
    w = (hrs > T_END - 2) & (hrs <= T_END + 1e-6)
    m = {k.replace("_horiz_avg", ""): np.nanmean(v[w], axis=0).squeeze() for k, v in h.items()}
    z = m["z_mid"][::-1]                              # bottom -> top
    P = lambda k: m[k][::-1]
    rho = P("p_mid") / (RD * P("T_mid") * (1 + 0.608 * P("qv")))
    dz = np.abs(np.gradient(z))
    thl, qt = P("LiqPotentialTemperature"), P("qv") + P("qc") + P("qr")
    cf = P("cldfrac_liq")
    zi = inversion_height(z, thl)
    qcp = P("qc")
    kc = np.where((qcp >= 0.1 * qcp.max()) & (z < 1500))[0] if qcp.max() > 1e-6 else np.array([])
    zb = z[kc[0]] if kc.size else np.nan            # lowest level with qc >= 10 % of its max
    out.update(z=z, thl=thl, qt=qt, cf=cf, qc=P("qc"), qr=P("qr"), nc_rho=P("nc") * rho / 1e6,
               w2_sgs=P("w_variance"), tke_sgs=P("tke"), buoy_sgs=P("sgs_buoy_flux"),
               rad_heat=P("rrtmgp_T_mid_tend"), autoconv=P("qc2qr_autoconv"), accret=P("qc2qr_accret"),
               evap=P("qr2qv_evap"), wthl_sgs=P("wthl_sec"), wqw_sgs=P("wqw_sec"), rho=rho)
    bl = z < zi
    # decoupling (Jones et al. 2011): lowest vs highest quarter of the BL
    lo, hi = (z < 0.25 * zi), (z > 0.75 * zi) & (z < 0.95 * zi)
    out["dqt"] = (qt[lo].mean() - qt[hi].mean()) * 1e3          # g/kg
    out["dthl"] = thl[hi].mean() - thl[lo].mean()                 # K
    # NB: P3's qc_sed/qr_sed outputs are not usable (the C++ port never loads the
    # pre-sedimentation q into the tendency buffer, so they come out as ~q/dt).
    col = lambda x, sel: np.sum((rho * x * dz)[sel]) * 86400                       # mm/day
    out["autoconv_col"] = col(P("qc2qr_autoconv"), bl)
    out["accret_col"] = col(P("qc2qr_accret"), bl)
    out["evap_col"] = col(P("qr2qv_evap"), bl)
    out["precip_sfc"] = float(np.nanmean(h["precip_liq_surf_mass_flux_horiz_avg"][w])) * 86400e3    # m/s -> mm/day
    gross = out["autoconv_col"] + out["accret_col"]
    out["evap_frac"] = 1 - out["precip_sfc"] / gross if gross > 1e-3 else np.nan    # share of rain production lost
    out["lw_cool_bl"] = np.sum((rho * CP * P("rrtmgp_T_mid_tend") * dz)[z < zi + 150])            # W m-2
    out["w2_sgs_bl"] = np.mean(P("w_variance")[bl])
    out["tke_sgs_bl"] = np.mean(P("tke")[bl])
    out.update(zi=zi, zb=zb)
    # ---- resolved statistics from the 3D snapshots at 10 and 12 h ----
    f3 = files(case, "aci3d.INSTANT")
    w2r, wthv, w3r = [], [], []
    t0 = None
    for f in f3:
        with netCDF4.Dataset(f) as d:
            d.set_auto_mask(False)
            tv = d["time"][:]
            if t0 is None:
                t0 = tv[0]
            for k, tk in enumerate(tv):
                hr = (tk - t0) * 24
                if not (T_END - 2 - 0.01 <= hr <= T_END + 0.01):
                    continue
                om, T, p, qv_, qc_, qr_ = (d[n][k] for n in ("omega", "T_mid", "p_mid", "qv", "qc", "qr"))
                rho3 = p / (RD * T * (1 + 0.608 * qv_))
                ww = -om / (rho3 * G)
                thv = T * (P0 / p) ** (RD / CP) * (1 + 0.608 * qv_ - qc_ - qr_)
                wp = ww - ww.mean(axis=0)
                tp = thv - thv.mean(axis=0)
                w2r.append((wp ** 2).mean(axis=0)[::-1]); w3r.append((wp ** 3).mean(axis=0)[::-1])
                wthv.append((wp * tp).mean(axis=0)[::-1])
    if w2r:
        w2r, w3r, wthv = np.mean(w2r, 0), np.mean(w3r, 0), np.mean(wthv, 0)
        out.update(w2_res=w2r, w3_res=w3r, wthv_res=wthv)
        out["w2_res_bl"] = np.mean(w2r[bl])
        out["f_res"] = out["w2_res_bl"] / (out["w2_res_bl"] + out["w2_sgs_bl"])
        k5 = np.argmin(np.abs(z - 0.5 * zi))
        out["skew_w_mid"] = w3r[k5] / max(w2r[k5], 1e-12) ** 1.5
        out["skew_w_bl"] = np.mean(w3r[bl]) / max(np.mean(w2r[bl]), 1e-12) ** 1.5
    # ---- column fields: raining fraction, cell scale ----
    t2, c2 = read(case, "aci2d.INSTANT", ["LiqWaterPath", "precip_liq_surf_mass_flux"])
    with netCDF4.Dataset(files(case, "aci2d.INSTANT")[0]) as d:
        x, y = d["lon"][:] / 1e3, d["lat"][:] / 1e3
    h2 = (t2 - t2[0]) * 24
    w2 = (h2 > T_END - 2 - 1e-6) & (h2 <= T_END + 1e-6)
    out["rain_frac"] = float((c2["precip_liq_surf_mass_flux"][w2] * 86400e3 > 0.5).mean())   # > 0.5 mm/day
    lwp = c2["LiqWaterPath"][w2] * 1e3
    xs, ys = np.unique(x), np.unique(y)
    out["dx_phys"] = float(xs[1] - xs[0]) if xs.size > 1 else np.nan
    out["L"] = float(xs.size * out["dx_phys"]) if xs.size > 1 else np.nan
    if xs.size >= 16 and np.nanstd(lwp) > 2:
        ix, iy = np.searchsorted(xs, x), np.searchsorted(ys, y)
        lams, specs = [], []
        for t_ in range(lwp.shape[0]):
            img = np.full((ys.size, xs.size), np.nan); img[iy, ix] = lwp[t_]
            lam, kb, sp = peak_wavelength(img, out["dx_phys"]); lams.append(lam); specs.append(sp)
        out["lambda_peak"] = float(np.median(lams))
        out["spec_k"], out["spec"] = kb, np.mean(specs, 0)
    else:
        out["lambda_peak"] = np.nan
    np.savez(f"{OUT}/explore_{name}.npz", **{k: np.asarray(v) for k, v in out.items()})
    return name


def safe(case):
    try:
        return one(case)
    except Exception as e:
        return f"FAIL {os.path.basename(case)}: {e!r}"


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    cases = sys.argv[2:]
    with Pool(int(os.environ.get("NPROC", 32))) as p:
        for r in p.imap_unordered(safe, cases):
            print(r, flush=True)
