import os
import sys

seq_dir = sys.argv[1]

out_dir = sys.argv[2]

mafft_exe = "/scratch/jlamb/Bio_tools/mafft"

mafft_opts = "--auto"
 

# Create output directory if it doesn't exist
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for file in os.listdir(seq_dir):

    if file.endswith(".fasta") or file.endswith(".pep") or file.endswith(".filtered"):

        input_file = os.path.join(seq_dir, file)

        output_file = os.path.join(out_dir, file)

        mafft_cmd = f'{mafft_exe} {mafft_opts} {input_file} > {output_file}'

        sbatch_cmd = f'sbatch --qos main --partition main --job-name=Mafft --mem=20G -n 1 -N 1 -c 16 --wrap="{mafft_cmd}"'

        print(sbatch_cmd)

        os.system(sbatch_cmd)
