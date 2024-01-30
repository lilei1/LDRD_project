#!/usr/bin/env python

"""
Written by Li Lei,1-30-2024, in Berkley
This script is to sort the gff3 file
python3 extract_20kb_paralogous_seq.py /global/u2/l/llei2019/plantbox/LDRD/maize/maize_V4_genome/annotation/Zmays_493_RefGen_V4.gene.gff3 /global/u2/l/llei2019/plantbox/LDRD/maize/maiz1_para.txt 20000

"""
import sys
import os

if __name__ == '__main__':
    # Define the filenames for both files
    try:
        gff_file = sys.argv[1]
        sorted_file = sys.argv[2]
    except IndexError:
        sys.stderr.write(__doc__ + '\n')
        exit(1) 		
		
def sort_gff3(file_path,out_file):
    with open(file_path, 'r') as file:
        lines = [line for line in file if not line.startswith('#')]
        sorted_lines = sorted(lines, key=lambda x: (x.split('\t')[0], int(x.split('\t')[3])))

    with open(sorted_file, 'w') as outfile:
        outfile.writelines(sorted_lines)


# Replace 'path_to_gff3_file.gff3' with your GFF3 file path
sort_gff3(gff_file,sorted_file)