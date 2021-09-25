#!bin/bash
echo 'type the folder name:'
read fname

# initialize folder
echo 'check needed folder'

fthermody="./$fname/thermodynamic"
if [ ! -d "$fthermody" ]; then
    mkdir $fname/thermodynamic
    echo "make $fthermody/"
else
    echo "$fthermody folder exists"
fi

fdiag="./$fname/diag"
if [ ! -d "$fdiag" ]; then
    mkdir $fname/diag
    echo "make $fdiag/"
else
    echo "$fdiag folder exists"
fi

fdynamic="./$fname/dynamic"
if [ ! -d "$fdynamic" ]; then
    mkdir $fname/dynamic
    echo "make $fdynamic/"
else
    echo "$fdynamic folder exists"
fi
