import os

input_file = "/scratch/jlamb/all_cds.fasta"
output_dir = "/scratch/jlamb/cds_orthogroups/"
reference_dir = "/scratch/jlamb/salmo_hsp_orthogroups/aligned_heatshock_proteins/renamed"

# read in the input file and return a dictionary mapping headers to sequences
def read_fasta(input_file):
    seq_dict = {}
    with open(input_file, "r") as f:
        header = ""
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    seq_dict[header] = seq
                header = line
                seq = ""
            else:
                seq += line
        seq_dict[header] = seq
    return seq_dict

# process a reference file against the input file and write the output to a file
def process_reference(reference_file):
    output_file = os.path.join(output_dir, os.path.basename(reference_file))
    with open(os.path.join(reference_dir, reference_file), "r") as ref, open(output_file, "w") as out:
        headers = set()
        # for each line in the reference file
        for line in ref:
            line = line.strip()
            # if the line starts with a >, add the header to the set of headers
            if line.startswith(">"):
                headers.add(line)
        # for each header in the set
        for header in headers:
            # find the matching sequence in the input fasta file
            for input_header, seq in input_dict.items():
                if header == input_header:
                    # write the header and sequence to the output file
                    out.write(header + "\n")
                    out.write(seq + "\n")
                    break

if __name__ == "__main__":
    # create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # read in the input fasta file
    input_dict = read_fasta(input_file)
    # process each reference file in the reference directory
    for reference_file in os.listdir(reference_dir):
        process_reference(reference_file)

