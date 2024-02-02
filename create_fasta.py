from Bio import SeqIO
import random

# Input FASTA file path
input_fasta_file = "ls_orchid.fasta"

# Output FASTA file path
output_fasta_file = "output-10k-diff.fasta"

# Read the first sequence from the input file
with open(input_fasta_file, "r") as input_file:
    records = list(SeqIO.parse(input_file, "fasta"))

n= 10**4
seqs = (random.choice(records) for _ in range(n))

# Write the first sequence to the output file 1000 times
with open(output_fasta_file, "w") as output_file:
    SeqIO.write(seqs, output_file, "fasta")

print(f"The first sequence has been written to {output_fasta_file} {n} times.")
