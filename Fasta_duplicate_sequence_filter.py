import os
import sys
from Bio import SeqIO
from tqdm import tqdm

# Get the input and output directories from the command-line arguments
input_dir = sys.argv[1]
output_dir = sys.argv[2]
log_file = os.path.join(output_dir, "log_file.txt")

# Check if the output directory exists
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Check if the log file exists, if it does, delete it, if not create it
# This is done to prevent the log file from getting too large
if os.path.exists(log_file):
    os.remove(log_file)
else:
    open(log_file, "w").close()

# Define the function to process each input file
def process_file(input_file):
    # Define the output file path
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    # Parse the input fasta file
    records = list(SeqIO.parse(input_file, "fasta"))
    # Create a dictionary to store the unique sequences and their frequency count
    unique_seqs = {}
    # Open the log file for writing
    with open(log_file, "a") as log_file_output:
        # Loop through the records
        for record in records:
            # Log the sequence being compared
            log_file_output.write(f"Comparing sequence: {record.id}\n")
            # Check if the sequence is already in the dictionary
            if str(record.seq) in unique_seqs:
                # If it is, decrement its frequency count and skip writing the record to the output file
                unique_seqs[str(record.seq)] -= 1
                log_file_output.write(f"Duplicate found! Decremented frequency count for {record.id}\n")
            else:
                # If it isn't, add it to the dictionary with a frequency count of 1
                unique_seqs[str(record.seq)] = 1
                SeqIO.write(record, output_file, "fasta")
                log_file_output.write(f"No match found for {record.id}, adding to dictionary with frequency count of 1\n")
            log_file_output.write("\n")
    # Process the dictionary to write the output file
    with open(output_file, "w") as output_file_handle:
        for record in records:
            if unique_seqs[str(record.seq)] == 1:
                SeqIO.write(record, output_file_handle, "fasta")

# Get a list of input files
input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".fasta") or f.endswith(".fa")]

# Process each input file with a tqdm progress bar
for input_file in tqdm(input_files, desc="Processing files"):
    process_file(input_file)

# Print the statistics regarding the number of sequences removed
with open(log_file, "r") as log_handle:
    log = log_handle.read()
    print(f"Number of sequences removed: {log.count('Deleting')}")
    print(f"Number of sequences kept: {log.count('Keeping')}")
    print(f"Number of sequences added to dictionary: {log.count('adding to dictionary')}")
    print(f"Number of sequences compared: {log.count('Comparing sequence')}")
    print(f"Number of sequences with no match: {log.count('No match found')}")
    print(f"Number of sequences with a match: {log.count('Match found!')}")