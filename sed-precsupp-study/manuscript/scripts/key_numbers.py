#!/usr/bin/env python3
"""Print every number quoted in the manuscript text, from the tables (-> tables/key_numbers.txt)."""
import numpy as np
import pandas as pd

T = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/tables"
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
r = pd.read_csv(f"{T}/runs.csv")
S = pd.read_csv(f"{T}/susceptibility.csv")
D = pd.read_csv(f"{T}/decomposition.csv")
ST = pd.read_csv(f"{T}/s_time.csv")
B = pd.read_csv(f"{T}/ml_budget.csv")
C = pd.read_csv(f"{T}/convergence.csv")
off = r[r.turb3d == "off"]
o1 = off[off.sed == 1]
P = lambda df, v, idx=("precsupp", "Nd_target"): df.pivot_table(index=list(idx), columns="dx_km", values=v).sort_index(axis=1, ascending=False)

print("runs:", len(r), "t3d off:", len(off), "t3d on:", (r.turb3d == "on").sum(),
      "t3d on at 312m:", ((r.turb3d == "on") & (r.res == "312m")).sum())
print("\n== LWP (sed 1)\n", P(o1, "LWP").round(0))
print("\n== Nd_incloud / target (all t3d-off runs): by dx min/max\n",
      (off.Nd_incloud / off.Nd_target).groupby(off.dx_km).agg(["min", "max", "mean"]).round(2))
print("\n== cdnc_top / Nd_incloud by dx\n", (off.cdnc_top_cm3 / off.Nd_incloud).groupby(off.dx_km).agg(["min", "max"]).round(2))
print("\n== ps gain LWP(on)-LWP(off), sed 1\n", (P(o1[o1.precsupp == 'on'], 'LWP', ('Nd_target',)) - P(o1[o1.precsupp == 'off'], 'LWP', ('Nd_target',))).round(0))
s = S[S.turb3d == "off"]
for b in ("low", "high", "vhigh"):
    print(f"\n== S_{b}\n", s.pivot_table(index=["precsupp", "sed"], columns="dx_km", values=f"S_{b}").sort_index(axis=1, ascending=False).round(3))
    print(f"   temporal sd (max over configs) by dx:\n", s.groupby("dx_km")[f"S_{b}_sd"].max().round(3).to_dict())
    print("   max |S_top - S| :", np.nanmax(np.abs(s[f"S_{b}_top"] - s[f"S_{b}"])).round(3))
    print("   cloud-cover part (sed1 on):", s[(s.sed == 1) & (s.precsupp == 'on')].set_index('dx_km')[f"S_{b}_cc"].round(3).to_dict())
print("\n== Nd target at LWP max\n", s.pivot_table(index=["precsupp", "sed"], columns="dx_km", values="Nd_target_at_max").sort_index(axis=1, ascending=False))
d = D[(D.turb3d == "off") & (D.sed == 1)]
print("\n== decomposition (sed 1)\n", d[["branch", "dx_km", "S_on", "S_off", "S_ps", "S_sed", "S_resid", "dS_dsed_off", "dS_dsed_on", "fit_rms_off"]].round(3).to_string())
st = ST[(ST.sed == 1)]
for b in ("low", "high", "vhigh"):
    print(f"\n== S_{b}(t)\n", st.pivot_table(index=["precsupp", "dx_km"], columns="t_end", values=f"S_{b}").round(3))
for v in ("we_812_mm_s", "eta_ent", "F_ent_moist", "F_ent_heat", "F_rad", "dthl_inv", "dqt_inv_gkg", "P_sfc_Wm2",
          "autoconv_col", "accret_col", "evap_frac", "h_cloud", "zi", "zb", "cloud_cover", "f_res", "w2_sgs_bl",
          "w2_res_bl", "skew_w_bl", "dqt", "dthl", "lambda_peak", "rain_frac", "slope_scene", "corr_scene", "thl_ml"):
    print(f"\n== {v} (sed 1)\n", P(o1, v).round(3))
print("\n== lambda/zi\n", (P(o1, "lambda_peak") / (P(o1, "zi") / 1e3)).round(1))
b12 = B[(B.turb3d == "off") & (B.t_end == 12) & (B.sed == 1)]
for k in ("ent", "subs", "rad", "sfc", "precip"):
    b12 = b12.assign(**{f"rel_{k}": 100 * b12[f"dlwp_{k}"] / b12.LWP})
b12 = b12.assign(rel_pred=100 * b12.dlwp_dt_pred / b12.LWP, rel_obs=100 * b12.dlwp_dt_obs / b12.LWP)
print("\n== relative LWP budget (%/h), sed1, 10-12 h\n",
      b12[["res", "precsupp", "Nd_target", "rel_ent", "rel_subs", "rel_rad", "rel_sfc", "rel_precip", "rel_pred", "rel_obs", "dlwp_dt_obs"]]
      .sort_values(["precsupp", "Nd_target"]).round(1).to_string())
bb = B[B.turb3d == "off"]
for v in ("dthl_dt", "dqt_dt", "dlwp_dt", "dzb_dt"):
    x, y = bb[f"{v}_obs"], bb[f"{v}_pred"]
    print(f"budget closure {v}: n={len(x)} r={np.corrcoef(x, y)[0, 1]:.2f} bias={np.mean(y - x):.3f} rmse={np.sqrt(np.mean((y - x) ** 2)):.3f} sd_obs={x.std():.3f}")
print("dzb/dthl, dzb/dqt range:", bb.dzb_dthl.min(), bb.dzb_dthl.max(), bb.dzb_dqt_gkg.min(), bb.dzb_dqt_gkg.max())
print("\n== LWP trend 10-12 h (g m-2 h-1), sed 1\n", P(b12, "dlwp_dt_obs").round(1))
print("   |trend| max at dx<=2.5 km (all t3d off):", B[(B.t_end == 12) & (B.turb3d == 'off') & (B.dx_km <= 2.5)].dlwp_dt_obs.abs().max().round(1))
c = C[(C.sed == 1)]
print("\n== convergence (sed 1)\n", c[["precsupp", "Nd_target", "var", "rel_1.25_0.625", "rel_0.625_0.3125", "ratio_finest"]].round(3).to_string())
# 3D turbulence
on = r[r.turb3d == "on"]
rows = []
for _, x in on.iterrows():
    y = off[(off.res == x.res) & (off.Nd_target == x.Nd_target) & (off.sed == x.sed) & (off.precsupp == x.precsupp)].iloc[0]
    rows.append({"res": x.res, "dLWP": x.LWP - y.LWP, "dcc": x.cloud_cover - y.cloud_cover, "dwe": x.we_812_mm_s - y.we_812_mm_s,
                 "rel_dLWP": (x.LWP - y.LWP) / y.LWP})
t3 = pd.DataFrame(rows)
print("\n== 3D turbulence on-off\n", t3.groupby("res").agg(["min", "max", "count"]).round(4))
