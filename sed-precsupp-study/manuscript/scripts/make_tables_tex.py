#!/usr/bin/env python3
"""LaTeX table bodies generated from the CSV tables (-> manuscript/tables/*.tex)."""
import pandas as pd

T = "/pscratch/sd/m/mahf708/dp_screamxx_sedps_12h/manuscript/tables"
OUT = "/pscratch/sd/m/mahf708/scmlib/sed-precsupp-study/manuscript/tables"
import os
os.makedirs(OUT, exist_ok=True)
DX = [40.0, 20.0, 10.0, 5.0, 2.5, 1.25, 0.625, 0.3125]
LAB = {40.0: "40\\,km", 20.0: "20\\,km", 10.0: "10\\,km", 5.0: "5\\,km", 2.5: "2.5\\,km", 1.25: "1.25\\,km",
       0.625: "625\\,m", 0.3125: "312\\,m"}
r = pd.read_csv(f"{T}/runs.csv")
o = r[(r.turb3d == "off") & (r.sed == 1)]

# LWP table: rows dx x suppression, columns Nd target; bold = maximum with suppression on
lines = []
for dx in DX:
    for ps in ("on", "off"):
        g = o[(o.dx_km == dx) & (o.precsupp == ps)].set_index("Nd_target").sort_index()
        vals = []
        for nd, v in g.LWP.items():
            s = f"{v:.0f}"
            if ps == "on" and nd == g.LWP.idxmax():
                s = f"\\textbf{{{s}}}"
            vals.append(s)
        nd_in = g.Nd_incloud
        lines.append(f"{LAB[dx] if ps == 'on' else ''} & {ps} & " + " & ".join(vals) + " \\\\")
    if dx != DX[-1]:
        lines.append("\\noalign{\\vskip 2pt}")
open(f"{OUT}/tab_lwp.tex", "w").write("\n".join(lines) + "\n\\bottomhline\n")

# S table (sed 1): rows dx, columns branch x suppression, with temporal sd
S = pd.read_csv(f"{T}/susceptibility.csv")
s = S[(S.turb3d == "off") & (S.sed == 1)]
lines = []
for dx in DX:
    row = [LAB[dx]]
    for b in ("low", "high", "vhigh"):
        for ps in ("on", "off"):
            x = s[(s.dx_km == dx) & (s.precsupp == ps)].iloc[0]
            sd = x[f'S_{b}_sd']; row.append(f"${x[f'S_{b}']:.2f}$\\,(" + (f"{sd:.2f}" if sd >= 0.005 else "$<$0.01") + ")")
    nd_max = s[(s.dx_km == dx) & (s.precsupp == "on")].iloc[0].Nd_target_at_max
    row.append(f"{nd_max:.0f}")
    lines.append(" & ".join(row) + " \\\\")
open(f"{OUT}/tab_S.tex", "w").write("\n".join(lines) + "\n\\bottomhline\n")

# observation comparison (hours 4-6, target Nd 50, s = 1)
oc = pd.read_csv(f"{T}/obs_comparison.csv")
lines = []
for ps in ("on", "off"):
    for dx in DX:
        x = oc[(oc.dx_km == dx) & (oc.precsupp == ps)].iloc[0]
        lines.append(f"{LAB[dx]} & {ps} & {x.LWP_4_6:.0f} & {x.we_4_6_mm_s:.1f} & {x.P_sfc_4_6_mm_d:.2f} & {x.evap_frac_4_6:.2f} & {x.zb_4_6:.0f} & {x.zi_6h:.0f} \\\\")
    if ps == "on":
        lines.append("\\noalign{\\vskip 2pt}")
open(f"{OUT}/tab_obs.tex", "w").write("\n".join(lines) + "\n\\middlehline\n")
# budget skill by grid spacing
bs = pd.read_csv(f"{T}/budget_skill.csv")
lines = []
for _, x in bs.iterrows():
    lines.append(f"{LAB[x.dx_km]} & {x.r_raw:.2f} & {x.rmse_raw:.1f} & {x.sd_obs:.1f} & {x.r_anom_all:.2f} & {x.r_anom_10_12:.2f} & {x.rmse_anom_10_12:.1f} & {x.sd_anom_10_12:.1f} \\\\")
open(f"{OUT}/tab_skill.tex", "w").write("\n".join(lines) + "\n\\bottomhline\n")
print(open(f"{OUT}/tab_lwp.tex").read())
print(open(f"{OUT}/tab_S.tex").read())
