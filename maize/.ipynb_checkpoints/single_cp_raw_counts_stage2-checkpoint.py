#!/usr/bin/env python
"""Written by Li Lei, 11-08-2023, in Berkley
This script is to synthesize the raw counts data for Bliss to call DEGs
N_sub is fo all the couts datasets; inter_file is the counts with the raw count and their paralogous 
"""
import sys
import csv

# Define the filenames for files A, B, C, and D
try:
    N_sub = sys.argv[1]
    inter_file = sys.argv[2]
    single_cp_rawcount = sys.argv[3]
except IndexError:
    sys.stderr.write(__doc__ + '\n')
    exit(1)

# Create a dictionary to store the key-value lookup from file C
key_value_lookup = {}

with open(N_sub, 'r') as file_a:
    # Open a new file D for writing
    next(file_a)
    for line_a in file_a:
        data_a = line_a.strip().split('\t')
        key = data_a[0]
        key_value_lookup[key] =  data_a[1:]
        #print (key,key_value_lookup)    
        # Iterate through the lines in file A and file B simultaneously

# Read the key-value pairs from file C and store them in the dictionary
with open(inter_file, 'r') as file_b:
    with open(single_cp_rawcount, 'w', newline='') as file_c:
        csv_writer = csv.writer(file_c)
        for line_b in file_b:
        #print (line_b)
            data_b = line_b.strip().split(',')
        # Check if the key exists in the lookup from file C
            key = data_b[1]
        #print (data_b[0],data_b[1])
            if key in key_value_lookup:
                # Combine the key, value, and corresponding columns from files A and B
                output_data = [data_b[0],key]
                for col_a, col_b in zip(data_b[2:],key_value_lookup[key]):
                    output_data.extend([col_a,col_b])
                csv_writer.writerow(output_data)
            else:
                 output_data = [data_b[0],key,"None"]
            #print(output_data)

print(f"File C has been generated as '{single_cp_rawcount}'.")