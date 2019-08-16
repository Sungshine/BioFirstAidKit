#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" You are piloting Salmonella AMR gene detection in Fluidigm reads.
    Jo gave you a multi-fasta file that contains the expected amplicon
    sequences for the Salmonella AMR genes. You wrote this script to separate
    the amplicon sequences for each AMR gene into its own fasta file.

"""


import os


# amps = raw_input('Enter file path: ')
outdir = '/data/home/sim8/Projects/cims/tmp'
fp = '/data/home/sim8/Projects/cims/predicted_amps.fasta'

# d = { gene: [ [header, sequence], [header, sequence], ... ] }
d = {}

with open(fp, 'r') as infile:

    header = ''
    gene_name = ''
    sequence = ''

    reader = infile.readlines()
    for line in reader:
        if line.startswith('>'):
            header = line.strip()
            gene_name = line.strip().split('|')[1]
        else:
            sequence = line.strip()

            if gene_name not in d.keys():
                d[gene_name] = [[header, sequence]]
            else:
                d[gene_name].append([header, sequence])

# Write amplicons to file
for gn in d.keys():
    outfile = '{}.fa'.format(gn)
    outpath = os.path.join(outdir, outfile)

    with open(outpath, 'w') as outhandle:
        for i in range(0, len(d[gn])):
            outhandle.write('{}\n'.format(str(d[gn][i][0])))
            outhandle.write('{}\n'.format(str(d[gn][i][1])))
