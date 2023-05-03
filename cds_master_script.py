#This script is the master CDS script. 
#Order of operations:
#1. Downloads the CDS data for each species and store it in a folder called CDS
#2. Concat all the CDS files into one file
#3. 


##########################################################################################
import os
import sys
import subprocess
from tqdm import tqdm

cds_dir = "/home/jake/Downloads/HSP_Project/CDS"
modified_headers_dir = "/home/jake/Downloads/HSP_Project/CDS/modified_headers"

# Make a new directory to save the modified files if it doesn't already exist
if not os.path.exists(modified_headers_dir):
    os.makedirs(modified_headers_dir)

# Loop over all files in the directory
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

merged_cds_file = "/home/jake/Downloads/HSP_Project/CDS/all_cds.fasta"
aligned_seq_dir = "/home/jake/Downloads/HSP_Project/aligned_seq_matching_header_as_cds/modifed"

# merge all the fasta files in the input directory into one fasta file
def merge_fasta_files(input_dir, output_file):
    os.chdir(input_dir)
    file_list = os.listdir(input_dir)
    with open(output_file, "w") as outfile:
        for file_name in tqdm(file_list, desc="Merging files"):
            with open(file_name, "r") as infile:
                outfile.write(infile.read())

merge_fasta_files(modified_headers_dir, merged_cds_file)

input_file = "/home/jake/Downloads/HSP_Project/CDS/all_cds.fasta"
cds_orthogroups_dir = "/home/jake/Downloads/HSP_Project/CDS/cds_orthogroups"

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
                seq += line
        yield header, seq

# for each file in the aligned_seq_dir
aligned_seq_files = os.listdir(aligned_seq_dir)
for file_name in tqdm(aligned_seq_files, desc="Processing aligned sequences"):
    output_file = os.path.join(cds_orthogroups_dir, file_name)
    with open(output_file, "w") as orthogroup_file:
        headers = set()
        # read in the file
        with open(os.path.join(aligned_seq_dir, file_name), "r") as ref_file:
            # for each line in the reference file
            for line in ref_file:
                line = line.strip()
                # if the line starts with a >, add the header to the set of headers
  # if the line starts with a >, add the header to the set of headers
                if line.startswith(">"):
                    headers.add(line)
        # for each header in the set
        for header in tqdm(headers, desc=f"Processing headers for {file_name}"):
            # find the matching sequence in the input fasta file
            for input_header, seq in read_fasta(input_file):
                if header == input_header:
                    # write the header and sequence to the output file
                    orthogroup_file.write(header + "\n")
                    orthogroup_file.write(seq + "\n")
                    break