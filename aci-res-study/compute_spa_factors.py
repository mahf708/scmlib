#!/usr/bin/env python3
"""
Compute the P3 SPA activation settings that give a target in-cloud droplet
number (Nd) for the DYCOMS-II RF02 DP-EAMxx case.

P3 (components/eamxx/src/physics/p3/impl/p3_main_impl_part1.hpp) applies,
in every cloudy cell, before any other microphysics:

    nc = max(nc, spa_ccn_to_nc_factor * (CCN3 * cld_frac_l) ** spa_ccn_to_nc_exponent)

with CCN3 (SPA "nccn") in #/kg and nc the grid-mean droplet number in #/kg.
With exponent = 1 the in-cloud number is factor * CCN3, so for a target
in-cloud Nd [#/cm3]:

    factor = Nd * 1e6 / (rho_cloud * CCN3_cloud)

where CCN3_cloud is SPA's CCN3 averaged over the IOP cloud layer, at the
SPA column nearest the IOP site, interpolated to the start date.

Usage:
    python3 compute_spa_factors.py [--nd 20 50 100 200]
"""
import argparse

import numpy as np
import xarray as xr

INPUTDATA = "/global/cfs/cdirs/e3sm/inputdata"
SPA_FILE = f"{INPUTDATA}/atm/scream/init/spa_from_v3LRamip_CMIP6_2010_clim_ne30pg2_c20260928.nc"
IOP_FILE = f"{INPUTDATA}/atm/cam/scam/iop/DYCOMSrf02_iopfile_4scam.nc"
LAT, LON = 31.5, 238.5  # DYCOMSrf02 run script
MONTH, DAY = 7, 11      # startdate 1999-07-11


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nd", type=float, nargs="+", default=[20, 50, 100, 200],
                        help="target in-cloud Nd [#/cm3]")
    parser.add_argument("--spa-file", default=SPA_FILE)
    parser.add_argument("--iop-file", default=IOP_FILE)
    args = parser.parse_args()

    # Cloud layer and air density from the IOP initial profile
    iop = xr.open_dataset(args.iop_file, decode_times=False)
    p = iop["lev"].values
    T = iop["T"].isel(time=0).squeeze().values
    q = iop["q"].isel(time=0).squeeze().values
    ql = iop["CLDLIQ"].isel(time=0).squeeze().values
    cloudy = ql > 1e-6
    p_top, p_bot = p[cloudy].min(), p[cloudy].max()
    rho = (p / (287.04 * T * (1 + 0.608 * q)))[cloudy].mean()

    # SPA CCN3 at the nearest column, linearly interpolated between the
    # monthly values (stored mid-month) to the start date
    spa = xr.open_dataset(args.spa_file)
    icol = int(np.argmin((spa["lat"].values - LAT) ** 2 + (spa["lon"].values - LON) ** 2))
    col = spa.isel(ncol=icol)
    w_next = (DAY + 30 - 15) / 30.0 if DAY < 15 else (DAY - 15) / 30.0
    m0 = MONTH - 2 if DAY < 15 else MONTH - 1  # 0-based index of the earlier month
    m1 = (m0 + 1) % 12
    ccn = (1 - w_next) * col["CCN3"].values[m0] + w_next * col["CCN3"].values[m1]
    ps = (1 - w_next) * col["PS"].values[m0] + w_next * col["PS"].values[m1]
    p0 = float(spa["P0"]) if "P0" in spa else 1.0e5
    p_spa = spa["hyam"].values * p0 + spa["hybm"].values * ps
    in_layer = (p_spa >= p_top) & (p_spa <= p_bot)
    ccn_cloud = ccn[in_layer].mean()

    print(f"SPA column {icol}: lat={float(col['lat']):.2f} lon={float(col['lon']):.2f}")
    print(f"IOP cloud layer: {p_top/100:.0f}-{p_bot/100:.0f} hPa, rho = {rho:.3f} kg/m3")
    print(f"SPA CCN3 in cloud layer: {ccn_cloud:.3e} #/kg "
          f"(range {ccn[in_layer].min():.2e}-{ccn[in_layer].max():.2e})")
    nd_default = 2000.0 * ccn_cloud ** 0.55 * rho / 1e6
    print(f"Nd with the default SPA settings (2000, 0.55): {nd_default:.0f} #/cm3")
    nd_raw = ccn_cloud * rho / 1e6
    print(f"Nd with (factor=1, exponent=1), i.e. raw SPA CCN3: {nd_raw:.0f} #/cm3\n")
    print("  Nd [#/cm3]   spa_ccn_to_nc_factor (exponent = 1)")
    for nd in args.nd:
        print(f"  {nd:10g}   {nd * 1e6 / (rho * ccn_cloud):.4f}")


if __name__ == "__main__":
    main()
