#!/bin/csh -fe

#######################################################################
#######################################################################
#######  Script to run SCREAMv1 in doubly periodic (DP) mode (DP-EAMxx)
#######  DYCOMSrf02
#######  Drizzling marine stratocumulus
#######
#######  ACI x resolution x 3D-turbulence study (see README.md in this dir)
#######  Based on DPxx_SCREAM_SCRIPTS/run_dpxx_scream_DYCOMSrf02.csh
#######  (script author: P. Bogenschutz) and the sub-800m settings in
#######  inverted-v-res-study/.
#######
#######  Usage:
#######    ./run_dpxx_scream_DYCOMSrf02_aci.csh <res> <nd> <turb3d>
#######      res    : 40km 20km 10km 5km 2p5km 1p25km 625m 312m 156m
#######      nd     : 20 50 100 200   (target in-cloud droplet number, #/cm3)
#######      turb3d : on off          (SHOC-HOMME 3D turbulence)
#######  e.g.  ./run_dpxx_scream_DYCOMSrf02_aci.csh 625m 100 on
#######
#######  IMPORTANT:
#######    - turb3d=on needs E3SM master that includes PR #8630
#######      (bogensch/eamxx/3d_turbulence_finisher, merged 2026-09-04).
#######

  if ($#argv != 3) then
    echo "Usage: $0 <res> <nd> <turb3d>"
    echo "  res    : 40km 20km 10km 5km 2p5km 1p25km 625m 312m 156m"
    echo "  nd     : 20 50 100 200"
    echo "  turb3d : on off"
    exit 1
  endif
  set res = $argv[1]
  set nd = $argv[2]
  set turb3d = $argv[3]

#######################################################
#######  BEGIN USER DEFINED SETTINGS
####### NOTE: beyond this section you will need to configure your
#######  ouput yaml file(s).  Please do a search for "yamlpath" and you will
#######  be brought to the correct locations.
####### See the example yaml file in the DPxx_SCREAM_SCRIPTS/yaml_file_example
#######  of the scmlib repo to get you started.

  # Set the name of your case here
  setenv casename scream_dpxx_DYCOMSrf02_aci_${res}_nd${nd}_t3d${turb3d}

  # Set the case directory here
  setenv casedirectory $PSCRATCH/dp_screamxx_aci_res

  # Directory where code lives
  setenv code_dir $PSCRATCH/e3sm-repo

  # Code tag name (must be E3SM master at or after PR #8630, see above)
  setenv code_tag E3SM-master

  # Name of machine you are running on (i.e. pm-cpu, anvil, etc)
  setenv machine pm-gpu

  # Compiler (pm-cpu should use "gnu"; pm-gpu should use "gnugpu"; LC should use "intel";
  #   frontier should use "craygnu-mphipcc") more machine compiler defaults will be added
  #   as they are tested/validated.
  setenv compiler gnugpu

  # Name of project to run on, if submitting to queue
  setenv projectname e3sm

  # Path where output YAML files are located (i.e. where you specify your output streams)
  #  See example files in DPxx_SCREAM_SCRIPTS/yaml_file_example to get you started.
  # NOTE, you will likely need to edit the section of the script where the yaml files
  #  are appended to your case.  Do a search for "yamlpath" to find this location.
  setenv yamlpath $PSCRATCH/scmlib/aci-res-study/yaml_file_example

  ## SET DOMAIN SIZE AND DYNAMICS RESOLUTION:
  # To estimate dx (analogous for dy):
  # dx = domain_size_x / (num_ne_x * 3)
  # (there are 3x3 unique dynamics columns per element, hence the "3" factor)
  # The physics (pg2) grid is coarser: dx_phys = domain_size_x / (num_ne_x * 2)

  # The domain is fixed at 240 km for every resolution.  num_ne_x must be an
  #  integer, so 240 km (not 200 km) is the smallest domain that hits
  #  dx = 40 km exactly (num_ne_x = 2: 6 dynamics / 4 physics columns per
  #  direction) and lets every finer level be an exact halving.
  set domain_size_x = 240000
  set domain_size_y = 240000

  # Resolution-dependent settings.  Columns:
  #   num_ne_x  : elements per direction
  #   model_dtime : model/physics time step [s] (integer, divides 86400)
  #   dyn_ratio : model_dtime / se_tstep (must be a multiple of 6 =
  #               lcm(dt_remap_factor=2, dt_tracer_factor=6))
  #   nu_top_dyn: second order viscosity near model top [m2/s]
  #   num_procs : MPI ranks (1 per GPU on pm-gpu, <= num_ne_x**2)
  #   walltime  : rough estimate, scaled from the inverted-v-res-study ~100 m runs
  #
  # dx >= 5 km : model_dtime stays at the 3.33 km default (100 s) so the physics
  #              time step does not co-vary with dx; dynamics is far from its CFL.
  # 2.5-1.25 km: default rule of thumb (dt halves with dx) and dyn_ratio 12/24.
  # dx < 1 km  : the inverted-v-res-study fix for the sub-800 m CFL blow-ups:
  #              dyn_ratio = 24 instead of 12 (se_tstep = model_dtime/24, i.e.
  #              ~2 s of dynamics step per km of dx) and nu_top reduced in
  #              proportion to dx (1111 m2/s at ~800 m).
  switch ($res)
    case 40km:
      set num_ne_x = 2;   set model_dtime = 100; set dyn_ratio = 12; set nu_top_dyn = 1.2e5
      set num_procs = 4;   set walltime = '00:30:00'; setenv debug_queue true
      breaksw
    case 20km:
      set num_ne_x = 4;   set model_dtime = 100; set dyn_ratio = 12; set nu_top_dyn = 6.0e4
      set num_procs = 4;   set walltime = '00:30:00'; setenv debug_queue true
      breaksw
    case 10km:
      set num_ne_x = 8;   set model_dtime = 100; set dyn_ratio = 12; set nu_top_dyn = 3.0e4
      set num_procs = 4;   set walltime = '00:30:00'; setenv debug_queue true
      breaksw
    case 5km:
      set num_ne_x = 16;  set model_dtime = 100; set dyn_ratio = 12; set nu_top_dyn = 1.5e4
      set num_procs = 4;   set walltime = '00:30:00'; setenv debug_queue true
      breaksw
    case 2p5km:
      set num_ne_x = 32;  set model_dtime = 75;  set dyn_ratio = 12; set nu_top_dyn = 7500
      set num_procs = 8;   set walltime = '00:30:00'; setenv debug_queue true
      breaksw
    case 1p25km:
      set num_ne_x = 64;  set model_dtime = 60;  set dyn_ratio = 24; set nu_top_dyn = 1666.667
      set num_procs = 16;  set walltime = '00:30:00'; setenv debug_queue true
      breaksw
    case 625m:
      set num_ne_x = 128; set model_dtime = 30;  set dyn_ratio = 24; set nu_top_dyn = 833.333
      set num_procs = 32;  set walltime = '01:00:00'; setenv debug_queue false
      breaksw
    case 312m:
      set num_ne_x = 256; set model_dtime = 15;  set dyn_ratio = 24; set nu_top_dyn = 416.667
      set num_procs = 64;  set walltime = '03:00:00'; setenv debug_queue false
      breaksw
    case 156m:
      set num_ne_x = 512; set model_dtime = 6;   set dyn_ratio = 24; set nu_top_dyn = 208.333
      set num_procs = 256; set walltime = '06:00:00'; setenv debug_queue false
      breaksw
    default:
      echo "Unknown res '$res'"; exit 1
  endsw
  set num_ne_y = $num_ne_x
  set dyn_dtime = `echo $model_dtime $dyn_ratio | awk '{printf "%.13f", $1/$2}'`

  ## SPA SETTINGS (target droplet number)
  # P3 activates SPA CCN as  nc = max(nc, factor * (CCN3 * cld_frac_l)^exponent).
  # With exponent = 1 the in-cloud Nd is factor * CCN3 * rho, independent of
  # the (resolution-dependent) liquid cloud fraction.  The factors below come
  # from compute_spa_factors.py: SPA CCN3 over the IOP cloud layer
  # (926-967 hPa) at the DYCOMS site is 9.2e7 #/kg, i.e. ~106 #/cm3 at
  # factor 1.  (The default 2000, 0.55 gives ~55 #/cm3 here.)
  set spa_exponent = 1.0
  switch ($nd)
    case 20:
      set spa_factor = 0.1882; breaksw
    case 50:
      set spa_factor = 0.4706; breaksw
    case 100:
      set spa_factor = 0.9412; breaksw
    case 200:
      set spa_factor = 1.8824; breaksw
    default:
      echo "Unknown nd '$nd'"; exit 1
  endsw

  if ($turb3d != on && $turb3d != off) then
    echo "turb3d must be on or off"; exit 1
  endif

####### END (mandatory) USER DEFINED SETTINGS, but see above about output
###########################################################################
###########################################################################
###########################################################################

# Case specific information kept here
  set lat = 31.5 # latitude
  set lon = 238.500 # longitude
  set do_iop_srf_prop = true # Use surface fluxes in IOP file?
  set do_iop_nudge_tq = true # Relax T&Q to observations?
  set do_iop_nudge_uv = false # Relax U&V to observations?
  set do_iop_nudge_coriolis = false # Nudge to geostrophic winds?
  set do_iop_subsidence = true # compute LS vertical transport?
  set startdate = 1999-07-11 # Start date in IOP file
  set start_in_sec = 0 # start time in seconds in IOP file
  set stop_option = nhours
  set stop_n = 6
  set iop_file = DYCOMSrf02_iopfile_4scam.nc #IOP file name
  set do_turnoff_swrad = true # Turn off SW calculation (if false, keep false)
# End Case specific stuff here

  # Location of IOP file
  set iop_path = atm/cam/scam/iop

  set PROJECT=$projectname
  set E3SMROOT=${code_dir}/${code_tag}

  cd $E3SMROOT/cime/scripts

  set compset=FIOP-SCREAMv1-DP

  # Note that in DP-SCREAM the grid is set ONLY to initialize
  #  the model from these files
  set grid=ne30pg2_ne30pg2

  set CASEID=$casename

  set CASEDIR=${casedirectory}/$CASEID

  set run_root_dir = $CASEDIR
  set temp_case_scripts_dir = $run_root_dir/case_scripts

  set case_scripts_dir = $run_root_dir/case_scripts
  set case_build_dir   = $run_root_dir/build
  set case_run_dir     = $run_root_dir/run

# Create new case
  ./create_newcase -case $casename --script-root $temp_case_scripts_dir -mach $machine -project $PROJECT -compset $compset -res $grid --compiler $compiler --driver mct
  cd $temp_case_scripts_dir

  ./xmlchange JOB_WALLCLOCK_TIME=$walltime

 ./xmlchange SCREAM_CMAKE_OPTIONS="`./xmlquery -value SCREAM_CMAKE_OPTIONS | sed 's/SCREAM_NUM_VERTICAL_LEV [0-9][0-9]*/SCREAM_NUM_VERTICAL_LEV 128/'`"

# Define executable and run directories
  ./xmlchange --id EXEROOT --val "${case_build_dir}"
  ./xmlchange --id RUNDIR --val "${case_run_dir}"

# Set to debug, only on certain machines
  if ($debug_queue == 'true') then
    if ($machine =~ 'pm*') then
      ./xmlchange --id JOB_QUEUE --val 'debug'
    endif

    if ($machine == 'quartz' || $machine == 'syrah' || $machine == 'ruby') then
      ./xmlchange --id JOB_QUEUE --val 'pdebug'
    endif
  endif

# need to use single thread
  set npes = $num_procs
  foreach component ( ATM LND ICE OCN CPL GLC ROF WAV )
    ./xmlchange  NTASKS_$component=$npes,NTHRDS_$component=1,ROOTPE_$component=0
  end

# Compute maximum allowable number for processes (number of elements)
  set dyn_pes_nxny = `expr $num_ne_x \* $num_ne_y`

  set ELM_CONFIG_OPTS="-phys elm"
  ./xmlchange ELM_CONFIG_OPTS="$ELM_CONFIG_OPTS"

# Modify the run start and duration parameters for the desired case
  ./xmlchange RUN_STARTDATE="$startdate",START_TOD="$start_in_sec",STOP_OPTION="$stop_option",STOP_N="$stop_n"

# Compute number of columns needed for component model initialization
  set comp_mods_nx = `expr $num_ne_x \* $num_ne_y \* 4`

# Modify the latitude and longitude for the particular case
  ./xmlchange PTS_MULTCOLS_MODE="TRUE",PTS_MODE="TRUE",PTS_LAT="$lat",PTS_LON="$lon"
  ./xmlchange MASK_GRID="USGS",PTS_NX="${comp_mods_nx}",PTS_NY=1
  ./xmlchange ICE_NX="${comp_mods_nx}",ICE_NY=1
  ./xmlchange CALENDAR="GREGORIAN"


# Set model timesteps

  @ ncpl = 86400 / $model_dtime
  ./xmlchange ATM_NCPL=$ncpl
  ./xmlchange ELM_NAMELIST_OPTS="dtime=$model_dtime"

  ./case.setup

# Get local input data directory path
  set input_data_dir = `./xmlquery DIN_LOC_ROOT -value`


# Set relevant namelist modifications
  ./atmchange se_ne_x=$num_ne_x
  ./atmchange se_ne_y=$num_ne_y
  ./atmchange se_lx=$domain_size_x
  ./atmchange se_ly=$domain_size_y
  ./atmchange dt_remap_factor=2
  ./atmchange cubed_sphere_map=2
  ./atmchange target_latitude=$lat
  ./atmchange target_longitude=$lon
  ./atmchange iop_file=$input_data_dir/$iop_path/$iop_file
  ./atmchange nu=0.216784
  ./atmchange nu_top=$nu_top_dyn
  ./atmchange se_ftype=2
  ./atmchange se_tstep=$dyn_dtime
  ./atmchange rad_frequency=3
  ./atmchange iop_srf_prop=$do_iop_srf_prop
  ./atmchange iop_dosubsidence=$do_iop_subsidence
  ./atmchange iop_coriolis=$do_iop_nudge_coriolis
  ./atmchange iop_nudge_uv=$do_iop_nudge_uv
  ./atmchange iop_nudge_tq=$do_iop_nudge_tq
  ./atmchange iop_nudge_tq_low=650
  ./atmchange iop_nudge_tq_high=0
  ./atmchange iop_nudge_tscale=3600

# Set default physics process ordering (NOTE: if you add/remove a process or change ordering,
# all DPxx runs NEED to have "iop_forcing" process in the list somewhere).
  ./atmchange physics::atm_procs_list=iop_forcing,mac_aero_mic,rrtmgp
  # SHOC and P3 run once per model_dtime (no subcycling), so the physics
  #  time step is exactly the model_dtime in the table above
  ./atmchange physics::mac_aero_mic::number_of_subcycles=1

#######################################################
####### SPA settings  (namelist group: p3, process: spa)
#######  spa supplies CCN3 ("nccn", #/kg) from the climatology file
#######  `./atmquery spa_data_file`; p3 turns it into droplet number.
#######  ./atmquery --listall p3   to see all P3 options
  ./atmchange do_prescribed_ccn=true
  ./atmchange spa_ccn_to_nc_factor=$spa_factor
  ./atmchange spa_ccn_to_nc_exponent=$spa_exponent

#######################################################
####### P3 settings  (namelist group: p3)
#######  Left at master defaults; listed here so they are easy to vary.
#######  The ones that matter most for ACI are the warm-rain terms.
#  ./atmchange autoconversion_prefactor=1350.0
#  ./atmchange autoconversion_qc_exponent=2.47
#  ./atmchange autoconversion_nc_exponent=1.79
#  ./atmchange autoconversion_radius=25.0e-6
#  ./atmchange accretion_prefactor=67.0
#  ./atmchange accretion_qc_exponent=1.15
#  ./atmchange accretion_qr_exponent=1.15
#  ./atmchange set_cld_frac_l_to_one=false
  ./atmchange set_cld_frac_r_to_one=true
  # process rates (qc2qr_autoconv, qc2qr_accret, qr2qv_evap, ...)
  ./atmchange extra_p3_diags=true

#######################################################
####### SHOC settings  (namelist group: shoc)
#######  Left at master defaults; listed here so they are easy to vary.
#######  ./atmquery --listall shoc   to see all SHOC options
#  ./atmchange length_fac=0.5
#  ./atmchange c_diag_3rd_mom=7.0
#  ./atmchange lambda_low=0.001
#  ./atmchange lambda_high=0.08
#  ./atmchange coeff_kh=0.1
#  ./atmchange coeff_km=0.1
#  ./atmchange shoc_1p5tke=false
  ./atmchange extra_shoc_diags=true

#######################################################
####### 3D turbulence (SHOC <-> HOMME)
#######  Switch: ctl_nl::do_3d_turbulence (HOMME control namelist).  Do NOT
#######  set homme::do_3d_turbulence_homme, it is locked and mirrored from
#######  the ctl_nl value.  When on, SHOC hands horizontal eddy
#######  diffusivities (coeff_k*_horiz * sqrt(dx*dy) * sqrt(TKE)) to HOMME and
#######  HOMME hands horizontal velocity gradients back for 3D shear
#######  production.  HOMME clips the horizontal diffusivities to an explicit
#######  CFL limit; if the clip is active a lot, subcycle with
#######  ctl_nl::horiz_turb_subcycle / horiz_turb_subcycle_q.
#######  See components/eamxx/docs/user/shoc_homme_3d_turbulence.md
  if ($turb3d == on) then
    ./atmchange ctl_nl::do_3d_turbulence=true
#    ./atmchange coeff_kh_horiz=0.1
#    ./atmchange coeff_km_horiz=0.1
#    ./atmchange ctl_nl::horiz_turb_subcycle=1
#    ./atmchange ctl_nl::horiz_turb_subcycle_q=1
  else
    ./atmchange ctl_nl::do_3d_turbulence=false
  endif

# Allow for the computation of tendencies for output purposes
  ./atmchange physics::mac_aero_mic::shoc::compute_tendencies=T_mid,qv
  ./atmchange physics::mac_aero_mic::p3::compute_tendencies=T_mid,qv
  ./atmchange physics::rrtmgp::compute_tendencies=T_mid
  ./atmchange homme::compute_tendencies=T_mid,qv
  ./atmchange physics::iop_forcing::compute_tendencies=T_mid,qv

 # configure yaml output
 # See the example yaml files in the DPxx_SCREAM_SCRIPTS/yaml_file_example
 # Note that you can have as many output streams (yaml files) as you want!
cp ${yamlpath}/scream_horiz_avg_output_15min.yaml .
cp ${yamlpath}/scream_aci_2d_inst_15min.yaml .
cp ${yamlpath}/scream_aci_3d_inst_2hour.yaml .
./atmchange output_yaml_files="./scream_horiz_avg_output_15min.yaml"
./atmchange output_yaml_files+="./scream_aci_2d_inst_15min.yaml"
./atmchange output_yaml_files+="./scream_aci_3d_inst_2hour.yaml"
# the 3D-turbulence fields only exist when do_3d_turbulence=true
if ($turb3d == on) then
  cp ${yamlpath}/scream_turb3d_horiz_avg_output_15min.yaml .
  ./atmchange output_yaml_files+="./scream_turb3d_horiz_avg_output_15min.yaml"
endif

# avoid the monthly cice file from writing as this
#   appears to be currently broken for SCM
cat <<EOF >> user_nl_cice
  histfreq='y','x','x','x','x'
EOF

# Turn on UofA surface flux scheme
cat <<EOF>> user_nl_cpl
  ocn_surface_flux_scheme = 2
EOF

if ($do_turnoff_swrad == 'true') then
  set solar_angle = 180 # turns off incoming solar radiation
else
  set solar_angle = -1 # Interactive SW radiation
endif

# Note that this call will be disabled for RCE
cat <<EOF>> user_nl_cpl
  constant_zenith_deg = $solar_angle
EOF

  ./case.setup

# Write restart files at the end of model simulation
  ./xmlchange PIO_TYPENAME="pnetcdf"

# Build the case
  ./case.build

# Submit the case
  ./case.submit

  exit
