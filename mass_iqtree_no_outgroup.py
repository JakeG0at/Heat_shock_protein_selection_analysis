import os
import argparse

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Process sequence files with IQ-TREE")
parser.add_argument("input_dir", help="The directory containing the sequence files")
parser.add_argument("output_dir", help="The directory for the output files")
args = parser.parse_args()

# Set the paths to the input and output directories
seq_dir = args.input_dir
out_dir = args.output_dir

# Create the output directory if it doesn't exist
os.makedirs(out_dir, exist_ok=True)

# Set the path to the IQ-TREE executable
iqtree_exe = '/scratch/jlamb/Bio_tools/iqtree-2.2.0-Linux/bin/iqtree2'

# Set the IQ-TREE command options
iqtree_opts = '-bb 1000 -nt 16 -m MFP+MERGE'

# Loop through the sequence files in the input directory
for seq_file in os.listdir(seq_dir):
    # Check if the file ends with correct .ext file
    if seq_file.endswith('.fixed'):
        # Construct the input and output file paths
        input_file = os.path.join(seq_dir, seq_file)
        basename = os.path.basename(seq_file)
        name = os.path.splitext(basename)[0]  # Get the filename without the extension
        output_file = os.path.join(out_dir, 'unique_aligned_' + name + '.fasta')

        # Construct the IQ-TREE command
        iqtree_cmd = f'{iqtree_exe} -s {input_file} {iqtree_opts} -pre {output_file}'

        # Construct the sbatch command
        sbatch_cmd = f'sbatch --qos main --partition main --job-name=IQ-TREE --mem=16G --nodes=1 --ntasks-per-node=16 --wrap="{iqtree_cmd}"'

        # Print the command for debugging purposes
        print(sbatch_cmd)

        # Execute the command
        os.system(sbatch_cmd)

