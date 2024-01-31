from Bio import SeqIO

# Input FASTA file path
input_fasta_file = "ls_orchid.fasta"

# Output FASTA file path
output_fasta_file = "output.fasta"

# Read the first sequence from the input file
with open(input_fasta_file, "r") as input_file:
    records = list(SeqIO.parse(input_file, "fasta"))

# Get the first sequence
first_sequence = records[0]
print(f"len:{len(first_sequence)}")
seqs = (first_sequence for _ in range(1000))

# Write the first sequence to the output file 1000 times
with open(output_fasta_file, "w") as output_file:
    SeqIO.write(seqs, output_file, "fasta")

print(f"The first sequence has been written to {output_fasta_file} 1000 times.")
