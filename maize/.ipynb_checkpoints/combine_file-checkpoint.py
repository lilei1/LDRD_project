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
with open(file_A, 'r') as file:
    next(file)
    file_prefixes = [line.strip().split('\t')[0] for line in file]

# Initialize an empty DataFrame for the combined data
combined_df = pd.DataFrame()

# Process each TSV file
for prefix in file_prefixes:
    file_path = os.path.join(directory, f'{prefix}.gene.expr.tsv')
    #print(file_path)
    # Read the file into a DataFrame
    #temp_df = pd.read_csv(file_path, sep='\t', header=None, names=['geneId', f'readCount_{prefix}'])
    temp_df = pd.read_csv(file_path, sep='\t', usecols=[0,1], header=0, quoting=csv.QUOTE_NONE, encoding='utf-8')
    #print(temp_df)
    if combined_df.empty:
        # For the first file, set the DataFrame
        combined_df = temp_df.set_index('geneId')
    else:
        # For subsequent files, merge based on GeneID
        temp_df.set_index('geneId', inplace=True)
        combined_df = combined_df.join(temp_df, how='outer',rsuffix='_other')
        #combined_df = combined_df.join(temp_df, how='outer',lsuffix='_caller', rsuffix='_other')
        #combined_df = combined_df.set_index('geneId').join(temp_df.set_index('geneId'))
# Reset the index to get GeneID as the first column
    print ("Merging file with prefix"+"\t"+ prefix)
combined_df.reset_index(inplace=True)

# Save the combined DataFrame to a new file
combined_df.to_csv(file_B, sep='\t', index=False, header=False)