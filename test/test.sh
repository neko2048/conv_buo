
for k in 325 326 327 328 329
do
    echo "diurnal_prescribed $k 1" | python convectionCluster.py &
done
wait
