#!/bin/bash

# ============ control param ======================
case_name="diurnal_prescribed"
rmfig=false
cover_old=false
Tstart=320
steps=4
Ntask=4
# ============= setting to remove all figures  ====================
if $rmfig; then 
    find . -name '*.jpg' -delete && echo "---------- File Cleared ----------"
else
    echo "---------- Skip Deleting Files ----------"
fi

# ========== subfolders check & mkdir ==========
echo "---------- checking subfolders and build if not exist ----------"
while read dirname others; do
    if [ ! -d "./$dirname" ]; then
        mkdir "$dirname"
        echo "+ mkdir $dirname"
    else
        echo "* $dirname exists"
    fi 
done < subfolder_name.txt


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
echo "---------- collecting and sorting figures ----------"
while read dirname others; do
    PATTERN="./$dirname*.jpg"
    if ls $PATTERN 1> /dev/null 2>&1; then
        mv $dirname*.jpg $dirname
        echo "+ $dirname figures are sorted"
    else
        echo "- No $dirname figures generated"
    fi
done < subfolder_name.txt

# ============ move figure-contained folders to case folder ===========
echo "---------- moving subfolders to $case_name folders ----------"
dir2="/home/atmenu10246/figure_VVM/${case_name}"
now=$(date +%F%H%M)
dir3="/home/atmenu10246/figure_VVM/temp/$now"
while read dirname others; do
    dir1="/home/atmenu10246/figure_VVM/code/${dirname}"
    if $cover_old; then
        [ -d $dir2 ] && rm -fr $dir2 && echo "- delete $dirname @ $case_name"
        mv $dir1 $dir2
        echo "+ move ./$dirname to $case_name folder"
    else
        echo "* create temporary folder to save: $now/$dirname"
        [ ! -d $dir3 ] && mkdir $dir3
        echo "${dir2}" >> "readme.md"
        cp parallel.sh $dir3
        mv readme.md $dir3 
        mv $dir1 $dir3
    fi
done < subfolder_name.txt
