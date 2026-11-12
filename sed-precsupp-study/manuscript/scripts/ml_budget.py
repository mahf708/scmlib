#!/usr/bin/env python3
"""
Mixed-layer (bulk) budget of the domain-mean boundary layer and of LWP, in the
spirit of Lilly (1968) and van der Dussen et al. (2014), evaluated for every run
over 2-h windows from the 15-min mixed-layer time series (profiles_ts.py).

For a well-mixed layer of depth z_i with conserved variables theta_l and q_t:

  d theta_l/dt = [ H/(rho c_p) + w_e Dtheta_l - F_rad/(rho c_p) + P/(rho c_p) ] / z_i
  d q_t/dt     = [ E/(rho L)   + w_e Dq_t                 - P/(rho L)   ] / z_i
  d z_i/dt     = w_e + w_s(z_i)
  d z_b/dt     = (dz_b/dtheta_l) d theta_l/dt + (dz_b/dq_t) d q_t/dt       (LCL of mixed-layer air)
  d LWP/dt     = 2 LWP (d z_i/dt - d z_b/dt) / h,   h = z_i - z_b           (LWP ~ h^2)

H, E: prescribed surface sensible and latent heat fluxes; F_rad: radiative cooling of the
layer below z_i + 150 m; P: surface rain rate (W m-2); D: jumps between the mixed layer and
100 m above z_i; w_e = dz_i/dt - w_s(z_i) from a linear fit over the window.
Each term of d LWP/dt is reported separately (entrainment, subsidence, radiation, surface
fluxes, precipitation) along with the observed tendencies of every variable.

Output: manuscript/tables/ml_budget.csv
"""
import numpy as np
import pandas as pd
import netCDF4

R = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/tables"
IOP = "/global/cfs/cdirs/e3sm/inputdata/atm/cam/scam/iop/DYCOMSrf02_iopfile_4scam.nc"
G, RD, RV, CP, LV, P0 = 9.80616, 287.04, 461.5, 1004.64, 2.501e6, 1.0e5
PS = 101780.0
KAPPA = RD / CP

with netCDF4.Dataset(IOP) as d:
    _p = np.asarray(d["lev"][:]).ravel()
    _w = -np.asarray(d["omega"][0]).ravel() / (_p / (RD * np.asarray(d["T"][0]).ravel()) * G)


def w_subs(p):
    return float(np.interp(p, _p, _w))


def qsat(T, p):
    es = 611.2 * np.exp(17.67 * (T - 273.15) / (T - 29.65))     # Bolton (1980)
    return 0.622 * es / (p - 0.378 * es)


def p_of_z(z, Tm=287.0):
    return PS * np.exp(-G * z / (RD * Tm))


def lcl(thl, qt):
    """Height (m) where unsaturated mixed-layer air (theta = theta_l) saturates."""
    z = np.arange(0.0, 2500.0, 1.0)
    p = p_of_z(z)
    T = thl * (p / P0) ** KAPPA
    k = np.where(qsat(T, p) <= qt)[0]
    return float(z[k[0]]) if k.size else np.nan


def dzb_sens(thl, qt):
    d1, d2 = 0.05, 0.05e-3
    a = (lcl(thl + d1, qt) - lcl(thl - d1, qt)) / (2 * d1)          # m K-1
    b = (lcl(thl, qt + d2) - lcl(thl, qt - d2)) / (2 * d2)          # m (kg/kg)-1
    return a, b


def slope(t, y):
    ok = np.isfinite(y)
    return np.polyfit(t[ok], y[ok], 1)[0] if ok.sum() > 3 else np.nan


def main():
    ts = pd.read_csv(f"{R}/ml_timeseries.csv")
    runs = pd.read_csv(f"{R}/runs.csv")[["case", "res", "dx_km", "Nd_target", "sed", "precsupp", "turb3d"]]
    rows = []
    for case, g in ts.groupby("case"):
        g = g.sort_values("time_h")
        for te in (4, 6, 8, 10, 12):
            w = g[(g.time_h > te - 2 - 1e-6) & (g.time_h <= te + 1e-6)]
            if len(w) < 6:
                continue
            th = w.time_h.values * 3600.0
            m = w.mean(numeric_only=True)
            zi, zb, h = m.zi, m.zb, m.zi - m.zb
            rho = m.rho_zi
            thl, qt = m.thl_ml, m.qt_ml * 1e-3
            a, b = dzb_sens(thl, qt)
            p_zi = p_of_z(zi)
            ws = w_subs(p_zi)
            dzi = slope(th, w.zi.values)
            we = dzi - ws
            dthl_inv, dqt_inv = m.dthl_inv, m.dqt_inv * 1e-3
            # mixed-layer tendencies by process (K s-1 and kg kg-1 s-1)
            th_ent, q_ent = we * dthl_inv / zi, we * dqt_inv / zi
            th_rad = -m.F_rad / (rho * CP * zi)
            th_sfc, q_sfc = m.SHF / (rho * CP * zi), m.LHF / (rho * LV * zi)
            th_pr, q_pr = m.P_sfc / (rho * CP * zi), -m.P_sfc / (rho * LV * zi)
            fac = 2.0 * m.LWP / h * 3600.0                               # (g m-2 h-1) per (m s-1)
            terms = {
                "ent": fac * (we - a * th_ent - b * q_ent),
                "subs": fac * ws,
                "rad": fac * (-a * th_rad),
                "sfc": fac * (-a * th_sfc - b * q_sfc),
                "precip": fac * (-a * th_pr - b * q_pr),
            }
            row = {"case": case, "t_end": te, "zi": zi, "zb": zb, "h": h, "LWP": m.LWP, "rho": rho,
                   "thl_ml": thl, "qt_ml": qt * 1e3, "dzb_dthl": a, "dzb_dqt_gkg": b * 1e-3,
                   "w_subs_mm_s": ws * 1e3, "we_mm_s": we * 1e3, "dthl_inv": dthl_inv, "dqt_inv": dqt_inv * 1e3,
                   "F_rad": m.F_rad, "P_sfc": m.P_sfc, "SHF": m.SHF, "LHF": m.LHF,
                   "F_ent_heat": rho * CP * we * dthl_inv, "F_ent_moist": -rho * LV * we * dqt_inv,
                   "lcl_ml": lcl(thl, qt),
                   # predicted vs observed tendencies
                   "dthl_dt_pred": (th_ent + th_rad + th_sfc + th_pr) * 3600, "dthl_dt_obs": slope(th, w.thl_ml.values) * 3600,
                   "dqt_dt_pred": (q_ent + q_sfc + q_pr) * 3600e3, "dqt_dt_obs": slope(th, w.qt_ml.values) * 3600,
                   "dzb_dt_obs": slope(th, w.zb.values) * 3600, "dzi_dt_obs": dzi * 3600,
                   "dlwp_dt_obs": slope(th, w.LWP.values) * 3600}
            row["dzb_dt_pred"] = (a * (th_ent + th_rad + th_sfc + th_pr) + b * (q_ent + q_sfc + q_pr)) * 3600
            row.update({f"dlwp_{k}": v for k, v in terms.items()})
            row["dlwp_dt_pred"] = sum(terms.values())
            row["dlwp_dt_geom"] = 2 * m.LWP / h * (row["dzi_dt_obs"] - row["dzb_dt_obs"])   # LWP ~ h^2 with observed z_i, z_b
            rows.append(row)
    out = pd.DataFrame(rows).merge(runs, on="case")
    out.to_csv(f"{R}/ml_budget.csv", index=False)
    print(out.shape)


if __name__ == "__main__":
    main()
