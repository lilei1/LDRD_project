#!/usr/bin/env python
"""Written by Li Lei, 11-09-2023, in Berkley
This script is to split the switch grass genome into K and N subgenomes

"""
import sys

def split_genome(input_file, subgenome1_file, subgenome2_file):
    with open(input_file, 'r') as genome, \
         open(subgenome1_file, 'w') as subgenome1, \
         open(subgenome2_file, 'w') as subgenome2:

        current_chromosome = None
        current_sequence = []

        for line in genome:
            if line.startswith('>'):
                # If the line is a header line (starts with '>'), it's a new chromosome
                if current_chromosome:
                    # Write the sequence to the appropriate subgenome file
                    if current_chromosome.endswith('K'):
                        subgenome1.write(f">{current_chromosome}\n")
                        subgenome1.write("".join(current_sequence) + "\n")
                    elif current_chromosome.endswith('N'):
                        subgenome2.write(f">{current_chromosome}\n")
                        subgenome2.write("".join(current_sequence) + "\n")

                # Reset the current chromosome and sequence
                current_chromosome = line.strip().split()[0][1:]
                current_sequence = []
            else:
                # Accumulate the sequence lines
                current_sequence.append(line.strip())

        # Write the last chromosome's sequence
        if current_chromosome:
            if current_chromosome.endswith('K'):
                subgenome1.write(f">{current_chromosome}\n")
                subgenome1.write("".join(current_sequence) + "\n")
            elif current_chromosome.endswith('N'):
                subgenome2.write(f">{current_chromosome}\n")
                subgenome2.write("".join(current_sequence) + "\n")

if __name__ == '__main__':
    # Define the filenames for both files
    try:
        genome_file = sys.argv[1]
        subgenome1_file = sys.argv[2]
        subgenome2_file = sys.argv[3]
    except IndexError:
        sys.stderr.write(__doc__ + '\n')
        exit(1)
    split_genome(genome_file, subgenome1_file, subgenome2_file)