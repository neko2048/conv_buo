#!/bin/bash

# ============ control param ======================
case_name="diurnal_prescribed"

rmfig=false
Tstart=325
steps=24
Ntask=4
# ============= setting to remove all figures  ====================
if $rmfig; then 
    find . -name '*.jpg' -delete && echo "File Cleared"
else
    echo "Skip Deleting Files"
fi

# ========== subfolders check & mkdir ==========
while read dirname others; do
    [ ! -d "./$dirname"] && mkdir "$dirname" || echo "$dirname exists"
done < subfolder_name.txt


#[ ! -d "./buoyancy" ] && mkdir buoyancy || echo "Buoyancy Exists"
#[ ! -d "./cloud" ] && mkdir cloud || echo "Cloud Exists"  
#[ ! -d "./srfrain" ] && mkdir srfrain || echo "Srfrain Exists"
#[ ! -d "./cwv" ] && mkdir cwv || echo "CWV Exists"
#[ ! -d "./coreshell" ] && mkdir coreshell || echo "Coreshell Exists"


# ========= parallel compute ==============
Tend=$(($Tstart+$steps))
interval=$((($Tend-$Tstart) / $Ntask))
time_count=($(seq $Tstart $interval $Tend))

# ============ main ==================
for k in ${time_count[@]:0:Ntask}; do
    echo "$case_name $k $interval" | python tbuoyancy.py &
done
echo "$case_name $Tend 1" | python tbuoyancy.py
wait

# ============ collect figures ============
while read dirname others; do
    mv "$dirname"*.jpg "$dirname"
done < subfolder_name.txt
#mv cloud*.jpg cloud
#mv buoyancy*.jpg buoyancy
#mv srfrain*.jpg srfrain
#mv cwv*.jpg cwv
#mv coreshell*jpg coreshell

# ============ move figure-contained folders to case folder ===========
mv ./"$dirname" ../$case_name
