#!/bin/bash

read -r case_name cover_old
echo "---------- moving subfolders to $case_name folders ----------"
now=$(date +%F%H%M%s)
while read dirname others; do
    dir1="/home/atmenu10246/figure_VVM/code/${dirname}"
    if $cover_old; then
        dir2="/home/atmenu10246/figure_VVM/${case_name}"
        [ -d $dir2 ] && rm -fr $dir2/$dirname && echo "- delete $dirname @ $case_name"
        mv $dir1 $dir2
        echo "+ move ./$dirname to $case_name folder"
    else
        dir3="/home/atmenu10246/figure_VVM/temp/$now"
        echo "* create temporary folder to save: $now/$dirname"
        [ ! -d $dir3 ] && mkdir $dir3
        echo "${case_name}" >> "readme.md"
        cp *.sh $dir3
        mv readme.md $dir3 
        mv $dir1 $dir3
    fi
done < subfolder_name.txt
