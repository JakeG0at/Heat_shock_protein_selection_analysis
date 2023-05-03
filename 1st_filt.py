import os
import glob
import argparse
from Bio import SeqIO
import statistics

# create an argparse object to handle command line arguments
parser = argparse.ArgumentParser(description='Process fasta files.')
parser.add_argument('directory', metavar='dir', type=str,
                    help='path to directory containing fasta files')

# parse the command line arguments
args = parser.parse_args()

# get the directory path from the command line arguments
directory = args.directory

for file in glob.glob(os.path.join(directory, "*.fa")):
    # read in the fasta file
    sequences = SeqIO.parse(file, "fasta")
    # create empty list to store sequence lengths
    seq_lengths = []
    # loop over each sequence in the fasta file
    for seq in sequences:
        # calculate the length of the sequence
        length = len(seq.seq)
        # append the length to the list of sequence lengths
        seq_lengths.append(length)
    # calculate the mean and standard deviation of the sequence lengths
    mean_length = statistics.mean(seq_lengths)
    std_dev = statistics.stdev(seq_lengths)
    # create empty list to store sequences within 1 standard deviation of the mean
    in_range_seqs = []
    # loop over each sequence in the fasta file again
    sequences = SeqIO.parse(file, "fasta")
    for seq in sequences:
        # calculate the length of the sequence
        length = len(seq.seq)
        # check if the length is within 1 standard deviation of the mean
        if length >= mean_length - std_dev and length <= mean_length + std_dev:
            # if it is, append the sequence to the list of sequences within 1 standard deviation of the mean
            in_range_seqs.append(seq)
    # create a new file name with the "1std_" prefix
    new_file_name = "1std_" + os.path.basename(file)
    # write the sequences within 1 standard deviation of the mean to the new file
    with open(os.path.join(directory, new_file_name), "w") as out_file:
        SeqIO.write(in_range_seqs, out_file, "fasta")

