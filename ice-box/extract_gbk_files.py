#!/usr/bin/env python

""" Extract genbank files from Prokka annotation output directories.

Copy to directory of choice.
"""


import os
import sys
import shutil


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


## usage: $python extract_gbk_files.py <input directory> <output directory>

input_dir = sys.argv[1]
output_dir = sys.argv[2]

directory_paths = [os.path.join(input_dir, fn) for fn in next(os.walk(input_dir))[1]]

for directory in directory_paths:
    if ".fasta" in directory:
        genbank_file = directory + '/' + os.path.basename(directory) + '.gbk'
        # print(genbank_file)
        fmt_file_name = os.path.basename(directory).split('.')[0]
        fmt_out = output_dir + "/{}.gbk".format(fmt_file_name)
        shutil.copy(genbank_file, fmt_out)