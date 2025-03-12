#!/bin/bash
#
# Array of Slurm accounts or QoS to simulate different users
accounts=("yamada_lab" "sidorov_lab" "doe_grads")

# Loop over each account and submit an sbatch job under that account
for account in "${accounts[@]}"; do
    sbatch --account="$account" --partition="compute" <<EOF
#!/bin/bash
#SBATCH --job-name=test_job_$account
#SBATCH --output=test_job_$account.out
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100M

echo "Running job as $account"
sleep 30  # Small but notable compute load
EOF

    echo "Submitted job for account: $account"
done
