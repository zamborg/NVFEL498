#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=Velocity
#SBATCH --mail-user=aysola@umich.edu
#SBATCH --mail-type=END
#SBATCH --cpus-per-task=10
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=8000m 
#SBATCH --time=3:00:00
#SBATCH --account=eecs498s009w21_class
#SBATCH --partition=standard

python velocity.py
