
for k in 325
do
    echo "diurnal_prescribed $k 1" | python convectionCluster.py &
done
wait
