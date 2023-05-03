import os
import pandas as pd
import numpy as np

# The input directory containing the FASTA files to be merged
input_dir = "/home/jake/Downloads/HSP_Project/CDS/modified_headers"
# The output file where the merged FASTA file will be saved
output_file = "/home/jake/Downloads/HSP_Project/CDS/all_cds.fasta"
# A reference file
reference = "/home/jake/Downloads/HSP_Project/aligned_seq_matching_header_as_cds/modifed"

# Function to merge all the FASTA files in the input directory into one FASTA file
def merge_fasta_files(input_dir, output_file):
    # Change the current working directory to the input directory
    os.chdir(input_dir)
    # Create a list of all files in the input directory
    file_list = os.listdir(input_dir)
    # Open the output file in write mode
    with open(output_file, "w") as outfile:
        # Iterate over each file in the file list
        for file in file_list:
            # Open each file in read mode
            with open(file, "r") as infile:
                # Write the contents of each file into the output file
                outfile.write(infile.read())

# Call the function with the input directory and output file as arguments
merge_fasta_files(input_dir, output_file)
