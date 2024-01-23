#!/usr/bin/env python
"""
Written by Li Lei,1-11-2024, in Berkley
This script is to combine all of the tsv files in this directory and make a gian raw cout file

"""
import sys
import pandas as pd
import os
import csv

if __name__ == '__main__':
    # Define the filenames for both files
    try:
        directory = sys.argv[1]
        file_A = sys.argv[2]
        file_B = sys.argv[3]
    except IndexError:
        sys.stderr.write(__doc__ + '\n')
        exit(1)	
# Directory containing the files
#directory = 'S'

# Path to file A
#file_a_path = os.path.join(directory, 'A.tsv')  # Adjust if file A has a different extension

# Read file A to get the list of file prefixes
with open(file_A, 'r') as file_a:
    next(file_a)
    file_prefixes = [line.strip().split('\t')[0] for line in file_a]

# Initialize a dictionary to hold the combined data
combined_data = {}

# Process each TSV file
for prefix in file_prefixes:
    file_path = os.path.join(directory, f'{prefix}.gene.expr.tsv')
    #print(file_path)
    # Read the file into a DataFrame
    #temp_df = pd.read_csv(file_path, sep='\t', header=None, names=['geneId', f'readCount_{prefix}'])
    with open(file_path, 'r') as file:
        for line in file:
            col = line.strip().split('\t')
            gene_id = col[0]
            count = col[1]
            if gene_id not in combined_data:
                combined_data[gene_id] = []
            combined_data[gene_id].append(count)
			
    print ("Merging file with prefix"+"\t"+ prefix)

# Write the combined data to a new file
with open(file_B, 'w') as combined_file:
    for gene_id, counts in combined_data.items():
        combined_file.write(f'{gene_id}\t{"\t".join(counts)}\n')