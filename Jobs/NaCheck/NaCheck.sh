#!/bin/bash
# The interpreter used to execute the script

#“#SBATCH” directives that convey submission options:

#SBATCH --job-name=NaCheck
#SBATCH --mail-user=aysola@umich.edu
#SBATCH --mail-type=END
#SBATCH --cpus-per-task=2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=8000m 
#SBATCH --time=10:00
#SBATCH --account=eecs498s009w21_class
#SBATCH --partition=standard

# python NaCheck.py

echo "wassup\n" > temp.txt
