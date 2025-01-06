#!/bin/bash

# Launch a slurm job for each simulation ID,
# creating a job array across the required
# realizations in each case.
simids=(
    "numcnas1.2_cnasize1e7_ploidy2_random0"
    "numcnas3.3_cnasize5e7_ploidy2_random9"
    "numcnas6.3_cnasize5e7_ploidy2_random6"
)

for simid in "${simids[@]}"; do
    echo "Submitting job for simid: $simid"
    
    sbatch --export=SIMID=$simid job.slurm
done
