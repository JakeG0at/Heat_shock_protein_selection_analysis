# This script is the master CDS script. 

import os
import sys
import subprocess
from tqdm import tqdm

# Set the paths to the input and output directories
cds_dir = "/home/jake/Downloads/HSP_Project/CDS"
modified_headers_dir = "/home/jake/Downloads/HSP_Project/CDS/modified_headers"
merged_cds_file = "/home/jake/Downloads/HSP_Project/CDS/all_cds.fasta"
aligned_seq_dir = "/home/jake/Downloads/HSP_Project/aligned_seq_matching_header_as_cds/modifed"
cds_orthogroups_dir = "/home/jake/Downloads/HSP_Project/CDS/cds_orthogroups"

# Make a new directory to save the modified files if it doesn't already exist
if not os.path.exists(modified_headers_dir):
    os.makedirs(modified_headers_dir)

# Loop over all files in the CDS directory
file_list = os.listdir(cds_dir)
for file_name in tqdm(file_list, desc="Modifying headers"):
    # Skip over files that aren't fasta files
    if not file_name.endswith(".fa"):
        continue
    # Open the file for reading
    with open(os.path.join(cds_dir, file_name), "r") as input_file:
        # Open a new file for writing
        with open(os.path.join(modified_headers_dir, file_name), "w") as output_file:
            # Loop over all lines in the file
            for line in input_file:
                # If the line starts with a >, change the header
                if line.startswith(">"):
                    fields = line.split(" ")
                    for field in fields:
                        if field.startswith("gene:"):
                            output_file.write(">" + field.split(":")[1] + "\n")
                            break
                else:
                    output_file.write(line)

# merge all the fasta files in the input directory into one fasta file
def merge_fasta_files(input_dir, output_file):
    os.chdir(input_dir)
    file_list = os.listdir(input_dir)
    with open(output_file, "w") as outfile:
        for file_name in tqdm(file_list, desc="Merging files"):
            with open(file_name, "r") as infile:
                outfile.write(infile.read())

# Call the function to merge the modified CDS files
merge_fasta_files(modified_headers_dir, merged_cds_file)

# read in the input file and return a generator that yields one header-sequence pair at a time
def read_fasta(input_file):
    with open(input_file, "r") as file:
        header = ""
        seq = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    yield header, seq
                header = line
                seq = ""
            else:
                seq
