#!/usr/bin/env python

""" Extract contig files from SPAdes assembly directories.

Copy to directory of choice
"""


import os
import sys
import shutil


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


## usage: $python extract_contig_files.py <input directory> <output directory>

input_dir = sys.argv[1]
output_dir = sys.argv[2]

directory_paths = [os.path.join(input_dir, fn) for fn in next(os.walk(input_dir))[1]]

for directory in directory_paths:
    if ".spades" in directory:
        contig_file = directory + "/contigs.fasta"
        fmt_file_name = os.path.basename(directory).split("-M")[0]
        fmt_out = output_dir + "/{}.contigs.fasta".format(fmt_file_name)

        shutil.copy(contig_file, fmt_out)