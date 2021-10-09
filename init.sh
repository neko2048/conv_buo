#!bin/bash
echo "type the folder name:"
read fname

# initialize folder
echo "===== check needed folder ====="
fmain="./$fname"
fdata="/home/atmenu10246/VVM/DATA/$fname"


# checking dataset existence
[ ! -d "$fdata" ] && echo "no such folder" && exit 1

# checking local drawing folder existence
[ ! -d "$fmain" ] && mkdir "$fmain" && echo "mkdir $fmain" || echo "$fmain folder exists"


# folders for drawing variables
fthermody="./$fname/thermodynamic"
[ ! -d "$fthermody" ] && mkdir $fname/thermodynamic && echo "make $fthermody/" || echo "$fthermody folder exists"

fdiag="./$fname/diag"
[ ! -d "$fdiag" ] && mkdir $fname/diag && echo "make $fdiag/" || echo "$fdiag folder exists"

fdynamic="./$fname/dynamic"
[ ! -d "$fdynamic" ] && mkdir $fname/dynamic && echo "make $fdynamic/" || echo "$fdynamic folder exists"
# ============================
