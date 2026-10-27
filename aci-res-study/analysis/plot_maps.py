#!/usr/bin/env python3
"""
LWP maps at the last 2D output time: rows = target Nd, columns = runs.

Usage:
  python plot_maps.py OUTPNG ND1,ND2 RUNDIR_PATTERN [RUNDIR_PATTERN ...]
  where each pattern contains {nd}, e.g. .../tt2_2p5km_nd{nd}_t3doff
"""
import glob
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import netCDF4  # noqa: E402
import numpy as np  # noqa: E402

# sequential one-hue ramp: clear sky light, thick cloud dark
CMAP = mcolors.LinearSegmentedColormap.from_list(
    "lwp", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])


def load(case):
    name = os.path.basename(case)
    f = glob.glob(f"{case}/run/{name}.aci2d.INSTANT*.nc")[0]
    with netCDF4.Dataset(f) as d:
        x, y = d["lon"][:] / 1e3, d["lat"][:] / 1e3
        lwp = d["LiqWaterPath"][-1, :] * 1e3
    xs, ys = np.unique(x), np.unique(y)
    img = np.full((ys.size, xs.size), np.nan)
    img[np.searchsorted(ys, y), np.searchsorted(xs, x)] = lwp
    return xs, ys, img


def main():
    out, nds, pats = sys.argv[1], sys.argv[2].split(","), sys.argv[3:]
    fig, axes = plt.subplots(len(nds), len(pats), figsize=(3.1 * len(pats), 3.0 * len(nds)),
                             squeeze=False, constrained_layout=True)
    for i, nd in enumerate(nds):
        for j, pat in enumerate(pats):
            ax = axes[i, j]
            case = pat.format(nd=nd)
            if not glob.glob(f"{case}/run/*.aci2d.INSTANT*.nc"):
                ax.set_axis_off()
                continue
            xs, ys, img = load(case)
            im = ax.imshow(img, origin="lower", extent=(xs[0], xs[-1], ys[0], ys[-1]),
                           cmap=CMAP, vmin=0, vmax=300, interpolation="nearest")
            cc = np.nanmean(img > 10)
            ax.set_title(f"{os.path.basename(case).split('_')[1]}, Nd {nd}: "
                         f"mean {np.nanmean(img):.0f} g/m², cover {cc:.2f}", fontsize=8)
            ax.set_xticks([])
            ax.set_yticks([])
    fig.colorbar(im, ax=axes, shrink=0.7, label="LWP at 6 h (g m$^{-2}$)")
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main()
