#!/usr/bin/env python
"""Written by Li Lei, 11-08-2023, in Berkley
This script is to synthesize the raw counts data from maize for Bliss to call DEGs

"""
import sys
import csv

# Define the filenames for files A, B, C, and D
try:
    N_sub = sys.argv[1]
    lookup_file = sys.argv[2]
    inter_file = sys.argv[3]
    #single_cp_rawcount = sys.argv[4]
except IndexError:
    sys.stderr.write(__doc__ + '\n')
    exit(1)

# Create a dictionary to store the key-value lookup from file C
key_value_lookup = {}

with open(N_sub, 'r') as file_a:
    next(file_a)
    for line_a in file_a:
        data_a = line_a.strip().split('\t')
        key = data_a[0]
        #print(key)
        key_value_lookup[key] =  data_a[1:]
        #print (key,key_value_lookup[key])    
        # Iterate through the lines in file A and file B simultaneously

# Read the key-value pairs from file C and store them in the dictionary
with open(lookup_file, 'r') as file_b:
    with open(inter_file, 'w', newline='') as file_c:
        csv_writer = csv.writer(file_c)
        for line_b in file_b:
            #print (line_b)
            data_b = line_b.strip().split(',')
        # Check if the key exists in the lookup from file C
            key = data_b[1]
            #print(key,key_value_lookup.get(key, 'Not Found'))
            #print (data_b[0],data_b[1])
            if key in key_value_lookup:
                # Combine the key, value, and corresponding columns from files A and B
                #print(key)
                output_data = [key,data_b[1]]
                output_data.extend(key_value_lookup[key])
                csv_writer.writerow(output_data)
            #else:
                #print(key)
            #print(output_data)

#print(f"File c has been generated as '{inter_file}'.")