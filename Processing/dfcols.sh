#!/bin/bash

#SBATCH --job-name=adddbcols
#SBATCH --mail-user=gmudel@umich.edu
#SBATCH --mail-type=END
#SBATCH --cpus-per-task=2
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=8000m 
#SBATCH --time=20:00
#SBATCH --account=eecs498s009w21_class
#SBATCH --partition=standard

python3 add_dataframe_cols.py
