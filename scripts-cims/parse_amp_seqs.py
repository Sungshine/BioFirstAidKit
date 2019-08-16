#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" You are piloting Salmonella AMR gene detection in Fluidigm reads.
    Jo gave you a multi-fasta file that contains the expected amplicon
    sequences for the Salmonella AMR genes. You wrote this script to separate
    each amplicon sequence into its own fasta file.

"""


import os


outdir = '/data/home/sim8/Projects/cims/amr_data'
fp = '/data/home/sim8/Projects/cims/predicted_amps.fasta'

with open(fp, 'r') as infile:

    header = ''
    sequence = ''

    reader = infile.readlines()
    for line in reader:
        if line.startswith('>'):
            header = line.strip().lstrip('>').replace('|', '_')
        else:
            sequence = line.strip()

        outfile = '{}.fa'.format(header)
        outpath = os.path.join(outdir, outfile)

        with open(outpath, 'w') as outhandle:
            outhandle.write('>{}\n'.format(str(header)))
            outhandle.write('{}\n'.format(str(sequence)))
