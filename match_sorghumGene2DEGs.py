#!/usr/bin/env python
"""Written by Li Lei, 11-08-2023, in Berkley
This script is to extract the homeologous based onthe orthID from the output of the GENESPACE

"""
import sys
import os

# Define the filenames for both files
try:
    lookup_table_file = sys.argv[1]
    input_text_file = sys.argv[2]
    output_file = sys.argv[3]
except IndexError:
    sys.stderr.write(__doc__ + '\n')
    exit(1)


def create_lookup_table(file_path):
    lookup = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                # Assuming the second column in both cases holds the relevant gene ID
                gene_id = parts[1]
                orthologous_id = parts[0]
                lookup[gene_id] = orthologous_id
    return lookup

def match_genes(input_file, lookup_table, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) >= 1:
                gene_id = parts[0]
                orthologous_id = lookup_table.get(gene_id, 'Not Found')
                outfile.write(f"{orthologous_id}\t{line.strip()}\n")

# Create the lookup table
lookup_table = create_lookup_table(lookup_table_file)

# Match genes and write to output file
match_genes(input_text_file, lookup_table, output_file)