#!/usr/bin/env python3
"""Figures for the sed x precip-suppression study.  Usage: plot_sedps.py OUTDIR"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

out = sys.argv[1]
df = pd.read_csv(f"{out}/summary_h4-6.csv")
res_order = [r for r in ["40km", "20km", "10km", "5km", "2p5km", "1p25km", "625m"] if r in set(df.res)]
lab = {"40km": "40 km", "20km": "20 km", "10km": "10 km", "5km": "5 km", "2p5km": "2.5 km", "1p25km": "1.25 km", "625m": "625 m"}
col = {0.5: "#1f77b4", 1.0: "#333333", 2.0: "#d62728"}
vars_ = [("LWP", "LWP (g m$^{-2}$)"), ("LWP_sd_online", "LWP spatial SD (g m$^{-2}$)"),
         ("we_mm_s", "$w_e$ (mm s$^{-1}$)"), ("precip", "surface precip (mm day$^{-1}$)"),
         ("cloud_cover", "cloud cover (LWP>10)")]
fig, axs = plt.subplots(len(vars_), len(res_order), figsize=(2.6 * len(res_order), 2.2 * len(vars_)),
                        sharex=True, sharey="row", squeeze=False)
for j, r in enumerate(res_order):
    for i, (v, vl) in enumerate(vars_):
        ax = axs[i, j]
        for sed in (0.5, 1.0, 2.0):
            for ps, ls, mk in (("on", "-", "o"), ("off", "--", "s")):
                d = df[(df.res == r) & (df.sed == sed) & (df.precsupp == ps)].sort_values("Nd_incloud")
                ax.plot(d.Nd_incloud, d[v], ls=ls, marker=mk, ms=3, color=col[sed], lw=1.2)
        ax.set_xscale("log")
        ax.set_xticks([20, 50, 100, 200])
        ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        if i == 0:
            ax.set_title(lab[r])
        if j == 0:
            ax.set_ylabel(vl)
        if i == len(vars_) - 1:
            ax.set_xlabel("in-cloud Nd (cm$^{-3}$)")
        ax.grid(alpha=0.3)
from matplotlib.lines import Line2D
h = [Line2D([], [], color=col[s], label=f"sed x{s:g}") for s in (0.5, 1.0, 2.0)]
h += [Line2D([], [], color="k", ls="-", marker="o", ms=3, label="precip supp. on"),
      Line2D([], [], color="k", ls="--", marker="s", ms=3, label="precip supp. off")]
fig.legend(handles=h, loc="upper center", ncol=5, frameon=False, bbox_to_anchor=(0.5, 1.0))
fig.suptitle("DP-EAMxx DYCOMS-II RF02, hours 4-6", y=1.025)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(f"{out}/fig_sedps_response.png", dpi=130, bbox_inches="tight")

# susceptibility S = dlnLWP/dlnNd (diagnosed Nd), low (20->50) and high (100->200) branches
rows = []
for (r, sed, ps), g in df.groupby(["res", "sed", "precsupp"]):
    g = g.set_index("Nd_target")
    s = lambda a, b: np.log(g.LWP[b] / g.LWP[a]) / np.log(g.Nd_incloud[b] / g.Nd_incloud[a])
    rows.append({"res": r, "sed": sed, "precsupp": ps, "S_low_20_50": s(20, 50), "S_high_100_200": s(100, 200)})
S = pd.DataFrame(rows)
S["res"] = pd.Categorical(S.res, res_order, ordered=True)
S.sort_values(["res", "precsupp", "sed"], ascending=[True, False, True]).round(2).to_csv(f"{out}/susceptibility.csv", index=False)
print(S.sort_values(["res", "precsupp", "sed"], ascending=[True, False, True]).round(2).to_string(index=False))
