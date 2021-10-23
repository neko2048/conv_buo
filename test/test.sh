
for k in 325 326 327
do
    echo "diurnal_prescribed $k 1" | python convectAnalysis.py &
done
wait
