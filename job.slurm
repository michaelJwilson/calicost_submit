#!/bin/bash
#SBATCH --job-name=calicost
#SBATCH --output=jobs/%A/slurm-%A.%a.out # job id:  %A, array id: %a 
#SBATCH --error=jobs/%A/slurm-%A.%a.err
#SBATCH --nodes=1            
#SBATCH --ntasks=1       
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G 
#SBATCH --time=02:00:00
#SBATCH --qos=short
#SBATCH --array=0-4 # job array with index values 0, 1, 2, 3, 4

#
#
# runs on adroit.
#
# see:  https://researchcomputing.princeton.edu/support/knowledge-base/slurm
# 
module purge
module load anaconda3/2024.6

conda activate calicost_env

# NB sbatch --export=SIMID=$simid with a default if not provided.
SIMID=${SIMID:-"numcnas1.2_cnasize1e7_ploidy2_random0"}

echo "(SLURM_ARRAY_JOB_ID, SIMID, SLURM_ARRAY_TASK_ID) == ($SLURM_ARRAY_JOB_ID, $SIMID, $SLURM_ARRAY_TASK_ID) @ " $(hostname)

python /home/mw9568/repos/CalicoST/src/calicost/calicost_main.py -c "/scratch/network/mw9568/Calicost/bafonly/"$SIMID"/configfile"$SLURM_ARRAY_TASK_ID
