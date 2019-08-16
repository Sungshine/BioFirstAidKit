#!/usr/bin/env python

""" Use BioPython Seq.IO to convert files from genbank to fasta format.

"""


import os
import sys
import subprocess
from Bio import SeqIO


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


inputDirectory = '/mnt/ecoli/2014-11-24_ecoli_cgp_annotations/cgp.gbk/'
paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

for file in paths:

    keyname = os.path.splitext(os.path.basename(file))[0]

    input_handle = open(file, 'rU')
    output_handle = open('/home/sim/Projects/ANI/ANI.fasta/%s.fasta' % (keyname,), 'w')

    sequences = SeqIO.parse(input_handle, 'genbank')
    count = SeqIO.write(sequences, output_handle, 'fasta')

    input_handle.close()
    output_handle.close()
    print('Conversion of ' + keyname + ' to fasta format has completed.')
