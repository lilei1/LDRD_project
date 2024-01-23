#!/usr/bin/env python
"""
Written by Li Lei,1-11-2024, in Berkley
This script is to check if all of the downloaded gene expression files are in the directory

"""
import sys
import os

# Function to check file existence based on ID
def check_file_existence(id, dir_path):
    # Check for any file that starts with the ID and a dot
    for file in os.listdir(dir_path):
        if file.startswith(id + '.'):
            return True
    return False

if __name__ == '__main__':
    # Define the filenames for both files
    try:
        directory_path = sys.argv[1]
        lookup_file_path = sys.argv[2]

    except IndexError:
        sys.stderr.write(__doc__ + '\n')
        exit(1)		
# Read the look-up file
with open(lookup_file_path, 'r') as file:
    for line in file:
        id = line.split('\t')[0]  # Assuming the ID is the first element
        exists = check_file_existence(id, directory_path)
        print(f"File with ID '{id}': {'Exists' if exists else 'Does Not Exist'}")
