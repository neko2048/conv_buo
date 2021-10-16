#!/bin/bash

# ============ control param ======================
case_name="diurnal_prescribed"
rmfig=true
cover_old=false
Tstart=320
steps=3
Ntask=3

# ============= setting to remove all figures  ====================
echo $rmfig | sh ./bash_package/remove.sh # remove.sh

# ========== subfolders check & mkdir ==========
sh ./bash_package/build_subfolder.sh

# ========= parallel compute ==============
Tend=$(($Tstart+$steps))
interval=$((($Tend-$Tstart) / $Ntask))
time_count=($(seq $Tstart $interval $Tend))

# ============ main ==================
echo "---------- start main program ----------"
for k in ${time_count[@]:0:Ntask}; do
    echo "$case_name $k $interval" | python tbuoyancy.py &
done
echo "$case_name $Tend 1" | python tbuoyancy.py
wait

# ============ collect figures ============
sh ./bash_package/collectfig.sh

# ============ move figure-contained folders to case folder ===========
echo $case_name $cover_old | sh ./bash_package/mvfig.sh
