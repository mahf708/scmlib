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
            row.append(f"${x[f'S_{b}']:.3f}$\\,({x[f'S_{b}_sd']:.3f})")
    nd_max = s[(s.dx_km == dx) & (s.precsupp == "on")].iloc[0].Nd_target_at_max
    row.append(f"{nd_max:.0f}")
    lines.append(" & ".join(row) + " \\\\")
open(f"{OUT}/tab_S.tex", "w").write("\n".join(lines) + "\n\\bottomhline\n")
print(open(f"{OUT}/tab_lwp.tex").read())
print(open(f"{OUT}/tab_S.tex").read())
