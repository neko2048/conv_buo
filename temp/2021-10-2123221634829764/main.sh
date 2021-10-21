#!/bin/bash

# ============ control param ======================
case_name="diurnal_prescribed"
current_dir=`pwd`
rmfig=true
cover_old=false
Tstart=320
steps=30
Ntask=3

# ============= setting to remove all figures  ====================
echo $rmfig | sh $current_dir/bash_fns/remove.sh # remove.sh

# ========== subfolders check & mkdir ==========
sh $current_dir/bash_fns/build_subfolder.sh

# ========= parallel compute ==============
Tend=$(($Tstart+$steps))
interval=$((($Tend-$Tstart) / $Ntask))
time_count=($(seq $Tstart $interval $Tend))

# ============ main ==================
echo "---------- start main program ----------"
for k in ${time_count[@]:0:Ntask}; do
    echo "$case_name $k $interval" | python main.py &
done
echo "$case_name $Tend 1" | python main.py
wait

# ============ collect figures ============
sh $current_dir/bash_fns/collectfig.sh

# ============ move figure-contained folders to case folder ===========
echo $case_name $cover_old | sh $current_dir/bash_fns/mvfig.sh
