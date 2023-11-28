#!/usr/bin/env python
"""Written by Li Lei, 11-08-2023, in Berkley
This script is to extract the homeologous based onthe orthID from the output of the GENESPACE

"""
import sys
import os
from Bio import SeqIO

# Directory containing your FASTA files
fasta_dir = 'path_to_your_directory_with_fasta_files'
output_file = 'genes_output.txt'
# Define the filenames for both files
try:
    fasta_dir = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    sys.stderr.write(__doc__ + '\n')
    exit(1)

# Function to extract and categorize gene names from a FASTA file
def process_fasta(fasta_file):
    gene_names = {'Sobic': '', 'K': '', 'N': ''}
    with open(fasta_file, 'r') as file:
        for seq_record in SeqIO.parse(file, 'fasta'):
            gene_name = seq_record.id  # Assuming the gene name is the sequence ID
            if gene_name.startswith("Sobic"):
                gene_names['Sobic'] = gene_name
            elif "K" in gene_name:
                gene_names['K'] = gene_name
            elif "N" in gene_name:
                gene_names['N'] = gene_name
    return gene_names

# Process all FASTA files and write results to the output file
with open(output_file, 'w') as outfile:
    for filename in os.listdir(fasta_dir):
        if filename.endswith('.fa') or filename.endswith('.fasta'):
            file_path = os.path.join(fasta_dir, filename)
            genes = process_fasta(file_path)
            outfile.write(f"{genes['Sobic']}\t{genes['K']}\t{genes['N']}\n")

print(f"Gene names have been extracted and saved to {output_file}")