#!bin/bash

#echo "---------- checking subfolders and build if not exist ----------"
while read dirname others; do
    if [ ! -d "./$dirname" ]; then
        mkdir "$dirname"
        echo "+ mkdir $dirname"
    else
        echo "* $dirname exists"
    fi 
done < subfolder_name.txt
