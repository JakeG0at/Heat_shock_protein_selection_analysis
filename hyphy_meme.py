#!/usr/bin/env python3

import os
import subprocess
import argparse

def submit_sbatch_job(fasta_file, tree_file):
    subprocess.run(["sbatch", "hyphy_meme.srun", fasta_file, tree_file])

def main(directory):
    fasta_files = [f for f in os.listdir(directory) if f.endswith(".fasta")]

    for fasta_file in fasta_files:
        tree_file = fasta_file.replace(".fasta", ".contree")

        fasta_path = os.path.join(directory, fasta_file)
        tree_path = os.path.join(directory, tree_file)

        if os.path.exists(tree_path):
            print(f"Submitting sbatch job for {fasta_file} and {tree_file}...")
            submit_sbatch_job(fasta_path, tree_path)
        else:
            print(f"There is no tree file for {fasta_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit sbatch jobs for fasta and tree files.")
    parser.add_argument("directory", help="Path to the directory containing fasta and tree files.")
    args = parser.parse_args()
    main(args.directory)

