#!/usr/bin/env python

"""
Written by Li Lei,1-29-2024, in Berkley
This script is to extract the interval based on the paralogous genes
python3 extract_20kb_paralogous_seq.py /global/u2/l/llei2019/plantbox/LDRD/maize/maize_V4_genome/annotation/Zmays_493_RefGen_V4.gene.gff3 /global/u2/l/llei2019/plantbox/LDRD/maize/maiz1_para.txt 20000

"""
import sys
import os

if __name__ == '__main__':
    # Define the filenames for both files
    try:
        gff_file = sys.argv[1]
        geneid_file = sys.argv[2]
        interval = sys.argv[3]
    except IndexError:
        sys.stderr.write(__doc__ + '\n')
        exit(1) 

#read gff file and save the content in a dict
gene_coords = {}
with open(gff_file, 'r') as file_a:
    for line in file_a:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        if parts[2] == 'gene':
            attributes = parts[8]               
            gene = next((attr.split('=')[1] for attr in attributes.split(';') if attr.startswith('ID=')), None)
            gene_id = gene.split('.')[0]
            gene_coords[gene_id] = (parts[0], int(parts[3]), int(parts[4]),parts[6])
            #print (gene_id)

#read the gene_id file
with open(geneid_file, 'r') as file_b:
    for line in file_b:
        geneID = line.strip().split('\t')[0]
        #print (geneID)
        if geneID in gene_coords:
    # Calculate intervals
            upstream_interval = ""
            downstream_interval = ""
            chromosome, start, end, strand = gene_coords[geneID]
            if strand == '+':
                upstream_interval = max(1, start - int(interval))
                downstream_interval = end + int(interval)
            else:
                upstream_interval = max(1, end - int(interval))
                downstream_interval = start + int(interval)
            print(chromosome,(start), str(end), strand,geneID,sep='\t')
        else:
            print(geneID)
			 