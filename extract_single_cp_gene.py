#!/usr/bin/env python
"""Written by Li Lei, 11-08-2023, in Berkley
This script is to extract the homeologous based onthe orthID from the output of the GENESPACE

"""
import sys

# Define the filenames for both files
try:
    orthID = sys.argv[1]
    homeoGene = sys.argv[2]
    out = sys.argv[3]
except IndexError:
    sys.stderr.write(__doc__ + '\n')
    exit(1)

# Create a set to store the names from file B
names_set = set()

# Read the names from file B and store them in the set
with open(orthID, 'r') as file_b:
    for line in file_b:
        names_set.add(line.strip())

# Open file A for reading
with open(homeoGene, 'r') as file_a:
    # Open a new file to write the matching lines
    with open(out, 'w') as matching_file:
        # Iterate through the lines in file A
        for line in file_a:
            # Split the line into words (assuming names are separated by spaces)
            words = line.strip().split()
            # Check if any word in the line is in the names set
            if any(word in names_set for word in words):
                # If a name is found in the line, write the line to the output file
                matching_file.write(line)

print("Matching lines have been extracted to output")
