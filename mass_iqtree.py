import os
import pandas as pd

# set the path to the directory containing the sequence files
seq_dir = '/scratch/jlamb/aligned_heatshock_proteins/'

# set the path to the output directory for the aligned sequences
out_dir = '/scratch/jlamb/iqtree_heatshock_protein_sequences'

hsps = pd.read_csv('/scratch/jlamb/hsps_w_outgroup.csv')

# set the path to the IQ-TREE executable
iqtree_exe = '/scratch/jlamb/Bio_tools/iqtree-2.2.0-Linux/bin/iqtree2'

# set the IQ-TREE command options
iqtree_opts = '-bb 1000 -nt 16 -m MFP+MERGE'

# loop through the sequence files in the input directory
for seq_file in os.listdir(seq_dir):
    # check if the file is a FASTA file
    if seq_file.endswith('.fasta') or seq_file.endswith('.fa'):
        # construct the input and output file paths
        input_file = os.path.join(seq_dir, seq_file)
        basename = os.path.basename(seq_file)
        name = os.path.splitext(basename)[0]  # get the filename without the extension
        output_file = os.path.join(out_dir, 'unique_aligned_' + name + '.fasta')
        outgroup = hsps.loc[hsps['Orthogroup'] == name, 'Outgroup'].values[0]

        # construct the IQ-TREE command
        iqtree_cmd = f'{iqtree_exe} -s {input_file} {iqtree_opts} -o {outgroup} -pre unique_{name}'

        # construct the sbatch command
        sbatch_cmd = f'sbatch --qos highmem --partition highmem --job-name=IQ-TREE --mem=20G -n 1 -N 1 -c 16 --wrap="{iqtree_cmd}"'

        # print the command for debugging purposes
        print(sbatch_cmd)

	# execute the command
        os.system(sbatch_cmd)
