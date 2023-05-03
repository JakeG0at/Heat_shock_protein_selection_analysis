import os
input_file = "/home/jake/Downloads/HSP_Project/CDS/all_cds.fasta"
output_dir = "/home/jake/Downloads/HSP_Project/CDS/cds_orthogroups"
reference = "/scratch/jlamb/salmo_hsp_orthogroups/aligned_heatshock_proteins/renamed"

# read in the input file and return a generator that yields one header-sequence pair at a time
def read_fasta(input_file):
    with open(input_file, "r") as f:
        header = ""
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    yield header, seq
                header = line
                seq = ""
            else:
                seq += line
        yield header, seq

# for each file in the reference directory
for file in os.listdir(reference):
    output_file = os.path.join(output_dir, file)
    with open(output_file, "w") as f:
        headers = set()
        # read in the file
        with open(os.path.join(reference, file), "r") as ref:
            # for each line in the reference file
            for line in ref:
                line = line.strip()
                # if the line starts with a >, add the header to the set of headers
                if line.startswith(">"):
                    headers.add(line)
        # for each header in the set
        for header in headers:
            # find the matching sequence in the input fasta file
            for input_header, seq in read_fasta(input_file):
                if header == input_header:
                    # write the header and sequence to the output file
                    f.write(header + "\n")
                    f.write(seq + "\n")
                    break
