#!/bin/bash

# ============ control param ======================
rmfig=false
Tstart=325
steps=24
Ntask=4

if $rmfig; then 
    find . -name '*.jpg' -delete && echo "File Cleared"
else
    echo "Skip Deleting Files"
fi

# subfolders
[ ! -d "./buoyancy" ] && mkdir buoyancy || echo "Buoyancy Exists"
[ ! -d "./cloud" ] && mkdir cloud || echo "Cloud Exists"  
[ ! -d "./srfrain" ] && mkdir srfrain || echo "Srfrain Exists"
[ ! -d "./cwv" ] && mkdir cwv || echo "CWV Exists"
[ ! -d "./coreshell" ] && mkdir coreshell || echo "Coreshell Exists"
# ====================================
Tend=$(($Tstart+$steps))
interval=$((($Tend-$Tstart) / $Ntask))
time_count=($(seq $Tstart $interval $Tend))

# ============ main ==================
for k in ${time_count[@]:0:Ntask}; do
    echo "diurnal_prescribed $k $interval" | python tbuoyancy.py &
done
echo "diurnal_prescribed $Tend 1" | python tbuoyancy.py
wait


mv cloud*.jpg cloud
mv buoyancy*.jpg buoyancy
mv srfrain*.jpg srfrain
mv cwv*.jpg cwv
mv coreshell*jpg coreshell
