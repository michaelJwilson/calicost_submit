#!/bin/bash

# Launch a slurm job for each simulation ID,
# creating a job array across the required
# realizations in each case.
# simids=(
#     "numcnas1.2_cnasize1e7_ploidy2_random0"
#     "numcnas1.2_cnasize1e7_ploidy2_random1"
#     "numcnas3.3_cnasize5e7_ploidy2_random9"
#     "numcnas6.3_cnasize5e7_ploidy2_random6"
# )

# Define the base directory
base_dir="/scratch/network/mw9568/Calicost/bafonly_nomerge"

# Initialize an empty array to hold the SIMID values
simids=()

# Find all subdirectories and extract SIMID from the directory name
while IFS= read -r dir; do
    simid=$(basename "$dir")
    simids+=("$simid")
done < <(find "$base_dir" -mindepth 1 -maxdepth 1 -type d)

# Print the array elements
# echo "SIMIDs:  ${simid_array[@]}"

iterations=0

for simid in "${simids[@]}"; do
    job_id=$(sbatch --export=SIMID=$simid job.slurm | awk '{print $4}')
    
    echo "Submitted batch job $job_id for simid: $simid"
    
    # sbatch --export=SIMID=$simid job.slurm

    ((iterations++))

    if [ "$iterations" -ge 5 ]; then
        break
    fi
    
done
