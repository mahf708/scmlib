#!/usr/bin/env python3
"""
Dominant horizontal wavelength of the LWP field (peak of the radially
averaged power spectrum) at each 2D output time after 3 h.

Usage:
  python cell_scale.py RUNDIR [RUNDIR ...]
"""
import glob
import os
import sys

import netCDF4
import numpy as np


def peak_wavelength(img, dx_km):
    a = img - np.nanmean(img)
    a = np.nan_to_num(a)
    ps = np.abs(np.fft.fft2(a)) ** 2
    ky, kx = np.meshgrid(np.fft.fftfreq(a.shape[0], dx_km), np.fft.fftfreq(a.shape[1], dx_km), indexing="ij")
    k = np.hypot(kx, ky)
    bins = np.fft.fftfreq(a.shape[0], dx_km)[1:a.shape[0] // 2]
    spec = np.array([ps[(k >= b - bins[0] / 2) & (k < b + bins[0] / 2)].mean() for b in bins])
    return 1.0 / bins[np.argmax(spec)]


for case in sys.argv[1:]:
    name = os.path.basename(case)
    with netCDF4.Dataset(glob.glob(f"{case}/run/{name}.aci2d.INSTANT*.nc")[0]) as d:
        x, y = d["lon"][:] / 1e3, d["lat"][:] / 1e3
        lwp = d["LiqWaterPath"][:] * 1e3
    xs, ys = np.unique(x), np.unique(y)
    dx = xs[1] - xs[0]
    ix, iy = np.searchsorted(xs, x), np.searchsorted(ys, y)
    lams = []
    for t in range(12, lwp.shape[0]):  # 3 h onwards
        img = np.full((ys.size, xs.size), np.nan)
        img[iy, ix] = lwp[t]
        lams.append(peak_wavelength(img, dx))
    print(f"{name:32s} dx_phys={dx:6.3f} km  peak wavelength {np.median(lams):6.1f} km "
          f"({np.median(lams) / dx:4.1f} dx_phys)")
