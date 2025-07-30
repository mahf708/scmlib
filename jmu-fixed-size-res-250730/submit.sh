#!/bin/bash

module load python

# cd to the directory where the script is located
cd "$(dirname "$0")"

# submit run_dpxx_scream_DYCOMSrf02_a1_1_0ps_copy.csh 
for i in {100,50,25,20,10,5,2}
do
    echo "Submitting run_dpxx_scream_DYCOMSrf02_a1_1_0ps_copy.csh with argument $i"
    ./run_dpxx_scream_DYCOMSrf02_a1_1_0ps_copy.csh $i &
    # sleep for 100 seconds to avoid overloading the system
    sleep 100
done
