#!/usr/bin/env python3
"""
Figures from analyze_runs.py output.

Usage:
  python plot_runs.py OUTDIR      # reads summary_h4-6.csv and timeseries.csv there
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# ordinal blue ramp (light -> dark = coarse -> fine), and an orange one for Nd
BLUE = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]
ORANGE = ["#f4b393", "#eb6834", "#c24f1e", "#8c3510"]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 2, "figure.dpi": 130,
})

# resolution groups: 5-40 km are horizontally homogeneous and identical within ~2 %
GROUPS = [("≥ 5 km", ["10km"]), ("2.5 km", ["2p5km"]), ("1.25 km", ["1p25km"]),
          ("625 m", ["625m"]), ("312 m", ["312m"]), ("156 m", ["156m"])]


def main():
    out = sys.argv[1]
    df = pd.read_csv(f"{out}/summary_h4-6.csv")
    ts = pd.read_csv(f"{out}/timeseries.csv")
    groups = [(lab, r) for lab, r in GROUPS if df.res.isin(r).any()]

    # 1. LWP vs in-cloud Nd, one line per resolution (3D turbulence on dashed)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    for (lab, rs), col in zip(groups, BLUE[-len(groups):] if len(groups) <= len(BLUE) else BLUE):
        for t3d, ls in (("off", "-"), ("on", "--")):
            s = df[df.res.isin(rs) & (df.turb3d == t3d)].sort_values("Nd_incloud")
            if s.empty:
                continue
            name = lab + (" 3D turb" if t3d == "on" else "")
            for ax, var in zip(axes, ("LWP", "we_mm_s", "precip")):
                ax.plot(s.Nd_incloud, s[var], ls, color=col, marker="o", ms=5, label=name)
    axes[0].set(xscale="log", yscale="log", xlabel="in-cloud Nd (cm$^{-3}$)", ylabel="LWP (g m$^{-2}$)",
                title="LWP, hours 4-6")
    axes[1].set(xscale="log", xlabel="in-cloud Nd (cm$^{-3}$)", ylabel="w$_e$ (mm s$^{-1}$)",
                title="entrainment rate, hours 2-6")
    axes[2].set(xscale="log", yscale="log", xlabel="in-cloud Nd (cm$^{-3}$)",
                ylabel="surface rain (mm day$^{-1}$)", title="surface rain, hours 4-6")
    for ax in axes:
        ax.set_xticks([20, 50, 100, 200])
        ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        if ax.get_yscale() == "log":
            ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
            ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axes[0].set_yticks([75, 100, 150, 200])
    axes[0].legend(frameon=False, fontsize=8, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(f"{out}/fig_nd_response.png")

    # 2. LWP time series per resolution, one line per Nd
    nds = sorted(df.Nd_target.unique())
    panels = [(lab, rs, t3d) for lab, rs in groups for t3d in ("off", "on")
              if (df.res.isin(rs) & (df.turb3d == t3d)).any()]
    fig, axes = plt.subplots(1, len(panels), figsize=(3.2 * len(panels), 3.4), sharey=True)
    for ax, (lab, rs, t3d) in zip(np.atleast_1d(axes), panels):
        for nd, col in zip(nds, ORANGE):
            q = ts[ts.run == f"{rs[0]}_nd{nd}_{t3d}"]
            if not q.empty:
                ax.plot(q.t, q.LWP, color=col)
                ax.annotate(f"{nd}", (q.t.values[-1], q.LWP.values[-1]), xytext=(3, 0),
                            textcoords="offset points", va="center", fontsize=8, color=MUTED)
        ax.set(title=lab + (", 3D turb" if t3d == "on" else ""), xlabel="hour")
    np.atleast_1d(axes)[0].set_ylabel("LWP (g m$^{-2}$), labels = target Nd")
    fig.tight_layout()
    fig.savefig(f"{out}/fig_lwp_timeseries.png")

    # 3. resolved vs subgrid w variance in the boundary layer, Nd 100
    s = df[(df.Nd_target == 100)].sort_values("dx_km")
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    for t3d, mk in (("off", "o"), ("on", "s")):
        q = s[s.turb3d == t3d]
        if q.empty:
            continue
        sfx = " (3D turb)" if t3d == "on" else ""
        ax.plot(q.dx_km, q.w2_sgs_bl, marker=mk, color="#2a78d6", ls="-" if t3d == "off" else "--",
                label="SHOC subgrid" + sfx)
        ax.plot(q.dx_km, q.w2_res_bl, marker=mk, color="#eb6834", ls="-" if t3d == "off" else "--",
                label="resolved" + sfx)
    ax.set(xscale="log", xlabel="dx (km)", ylabel="BL-mean w'$^2$ (m$^2$ s$^{-2}$)",
           title="who carries the turbulence, Nd 100")
    ax.invert_xaxis()
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{out}/fig_w2_partition.png")

    # 4. LWP susceptibility per resolution
    rows = []
    for lab, rs in groups:
        for t3d in ("off", "on"):
            q = df[df.res.isin(rs) & (df.turb3d == t3d)]
            if len(q) >= 3:
                x, y = np.log(q.Nd_incloud), np.log(q.LWP)
                lo, hi = q.Nd_incloud < 80, q.Nd_incloud > 80
                rows.append({"res": lab, "turb3d": t3d, "n": len(q),
                             "S_all": np.polyfit(x, y, 1)[0],
                             "S_low": np.polyfit(x[lo], y[lo], 1)[0] if lo.sum() >= 2 else np.nan,
                             "S_high": np.polyfit(x[hi], y[hi], 1)[0] if hi.sum() >= 2 else np.nan})
    pd.DataFrame(rows).to_csv(f"{out}/susceptibility.csv", index=False)
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
