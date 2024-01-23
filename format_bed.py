#!/usr/bin/env python
"""
Written by Li Lei, 11-09-2023, in Berkley
This script is to split the switch grass genome into K and N subgenomes

"""
import sys


def reformat_to_bed(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Splitting the line into columns assuming tab-delimited format
            cols = line.strip().split('\t')

            # Check if there are enough columns
            if len(cols) >= 5:
                chrom = cols[0]
                start = cols[2]
                end = cols[3]
                score = cols[4]

                # Check the condition on the 5th column
                if float(score) > 0:
                    bed_line = f"{chrom}\t{start}\t{end}\n"
                else:
                    bed_line = f"{chrom}\t{end}\t{start}\n"

                # Write the formatted line to the output file
                outfile.write(bed_line)

# Replace 'input.txt' and 'output.bed' with your actual file paths
if __name__ == '__main__':
    # Define the filenames for both files
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        sys.stderr.write(__doc__ + '\n')
        exit(1)	
    reformat_to_bed(input_file, output_file)