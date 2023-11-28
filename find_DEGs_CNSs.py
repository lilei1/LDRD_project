#!/usr/bin/env python
"""Written by Li Lei, 11-08-2023, in Berkley
This script is to extract the homeologous based onthe orthID from the output of the GENESPACE

"""
import sys
import os

# Define the filenames for both files
try:
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    output_file = sys.argv[3]
except IndexError:
    sys.stderr.write(__doc__ + '\n')
    exit(1)

def read_gene_ids(file_path):
    gene_ids = set()
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            gene_id = columns[0]
            gene_ids.add(gene_id)
    return gene_ids

def filter_file_a(file_a_path, gene_ids, output_file_path):
    """ Go through file A and write lines containing gene IDs to the output file. """
    with open(file_a_path, 'r') as file_a, open(output_file_path, 'w') as output_file:
        for line in file_a:
            # Check if any gene ID is in the line
            if any(gene_id in line for gene_id in gene_ids):
                output_file.write(line)

# Read gene IDs from file B
gene_ids = read_gene_ids(file_b)

# Filter file A based on gene IDs and write to output file
filter_file_a(file_a, gene_ids, output_file)