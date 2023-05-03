#!/bin/bash
#SBATCH --qos mrmckain
#SBATCH --partition ultrahigh
#SBATCH --job-name=Orthofinder
#SBATCH --mem=60G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jlamb@crimson.ua.edu
#SBATCH -n 1 #tasks
#SBATCH -N 1 #nodes
#SBATCH -c 32 #number of cores per task
#SBATCH -o Orthofinder_Fish.o
module load bio/orthofinder/2.3.14

# Runs the orthofinder pipeline script
ulimit -Sn 10000
ulimit -Hn 10000
orthofinder -f /scratch/jlamb/Orthofind_w_outgroup/primary_transcripts -t 32

