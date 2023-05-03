import os
import sys

# Set the directory path where your input FASTA files are located
seq_dir = sys.argv[1]

# Set the directory path where you want the output aligned FASTA files to be written
out_dir = sys.argv[2]

# Set the path to the MACSE JAR file
macse_jar = "/scratch/jlamb/Bio_tools/macse_v2.06.jar"

# Set any additional MACSE options you want to use
macse_opts = "-prog alignSequences -out_NT"

# Create the output directory if it doesn't already exist
os.makedirs(out_dir, exist_ok=True)

# Loop through each file in the directory
for file in os.listdir(seq_dir):
    if file.endswith(".fixed"):
        input_file = os.path.join(seq_dir, file)
        output_file = os.path.join(out_dir, "aligned_" + file)

        # Load the Java module and run the MACSE command
        macse_cmd = f"module load java/1.8.202 && java -jar {macse_jar} {macse_opts} {output_file} -seq {input_file}"

        sbatch_cmd = f"sbatch --qos main --partition main --job-name=MACSE --mem=20G -n 1 -N 1 -c 4 --wrap='{macse_cmd}'"

        print(sbatch_cmd)
        os.system(sbatch_cmd)

