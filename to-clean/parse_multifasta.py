#!/usr/bin/env python2.7

""" Parse multifasta file into individual fasta files.

"""


import os
import sys


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


dir_path = os.getcwd()
file_path = sys.argv[1]
filein = open(file_path, 'r')

for line in filein:
    if line.startswith('>'):
        fmt_file_id = line.strip('>').replace(':', '-').rstrip()
        out_file = '{}.fa'.format(fmt_file_id)
        # open outfile handle
        out = open(dir_path + '/{}'.format(out_file), 'wa')
        # write header
        out.write(line)
    else:
        if line != '':
            out.write(line)
        else:
            out.close()
