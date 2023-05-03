import os

input_dir = "/scratch/jlamb/salmo_hsp_orthogroups/aligned_heatshock_proteins"
output_dir = "/scratch/jlamb/salmo_hsp_orthogroups/aligned_heatshock_proteins/renamed"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(".fasta") or filename.endswith(".fa"):
        with open(os.path.join(input_dir, filename), "r") as infile:
            with open(os.path.join(output_dir, filename), "w") as outfile:
                for line in infile:
                    if line.startswith(">"):
                        line_parts = line.strip().split("_")
                        new_header = ">{}".format("_".join(line_parts[2:]))
                        outfile.write(new_header + "\n")
                    else:
                        outfile.write(line)
