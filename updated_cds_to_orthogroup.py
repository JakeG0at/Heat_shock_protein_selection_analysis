import os
import multiprocessing
import itertools

input_file = "/home/jake/Downloads/HSP_Project/CDS/all_cds.fasta"
output_dir = "/home/jake/Downloads/HSP_Project/CDS/cds_orthogroups"
reference = "/home/jake/Downloads/HSP_Project/aligned_seq_matching_header_as_cds/modifed"

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


# process a chunk of files
def process_chunk(files):
    for file in files:
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


if __name__ == "__main__":
    # get the list of files in the reference directory
    files = os.listdir(reference)
    # set the number of workers
    num_workers = multiprocessing.cpu_count()
    # split the files into chunks
    chunks = list(itertools.chunked(files, num_workers))
    # create a process for each chunk
    processes = []
    for chunk in chunks:
        p = multiprocessing.Process(target=process_chunk, args=(chunk,))
        p.start()
        processes.append(p)
    # wait for all processes to finish
    for p in processes:
        p.join()
    print("Done!")
