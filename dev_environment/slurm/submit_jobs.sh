#!/bin/bash

hpc_users="aandersson akowalska enovakova hkildong isidorov jjonsson mdupont mjanos mmustermann nnegidius pivanov ssvensson tyamada wdebruijn ycohen"
doe_users="jdoe akowalska cespanola hkildong isidorov mjanos mmustermann mrossi nnegidius onordmann tyamada"
opmodes='sleep stress timeout'

for ((node_count=1; node_count <= 2; node_count++)); do
    for user in $hpc_users; do
        for mode in $opmodes; do
                sudo -u $user -i -- sbatch -n $node_count --job-name=$user_$script_$node_count --export='ALL,MODE='$mode /usr/local/bin/example_job.sbatch
        done
    done
done

for ((node_count=1; node_count <= 2; node_count++)); do
    for user in $doe_users; do
        for mode in $opmodes; do
                sudo -u $user -i -- sbatch -n $node_count --job-name=$user_$script_$node_count --partition=doe --export='ALL,MODE='$mode /usr/local/bin/example_job.sbatch
        done
    done
done
