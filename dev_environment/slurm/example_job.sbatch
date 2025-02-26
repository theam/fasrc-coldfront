#!/bin/bash
##SBATCH --job-name=test_job
##SBATCH --output=test_job.out
##SBATCH --time=00:05:00
##SBATCH --ntasks=1
##SBATCH --cpus-per-task=1
##SBATCH --mem=100M
num1=$RANDOM
num2=$RANDOM
for i in {1..num2}; do result=$((i * num1)); done
echo "The product is: $result"
