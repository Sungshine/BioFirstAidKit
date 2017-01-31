#!/usr/bin/env python2.7

""" Parse stx.fsa into stx1.fsa & stx2.fsa.

"""


import os
import sys


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


dir_path = os.getcwd()
file_path = sys.argv[1]
filein = open(file_path, 'r')

for line in filein:
    if line.startswith('>stx1'):
        if line.startswith('>'):
            fmt_file_id = line.strip('>').rstrip()
            out_file = 'stx1.fsa'
            # open outfile handle
            out = open(dir_path + '/{}'.format(out_file), 'wa')
            # write header
            out.write(line)
        else:
            if line != '':
                out.write(line)
            else:
                out.close()
    elif line.startswith('>stx2'):
        if line.startswith('>'):
            fmt_file_id = line.strip('>').rstrip()
            out_file = 'stx2.fsa'
            out = open(dir_path + '/{}'.format(out_file), 'wa')
            out.write(line)
        else:
            if line != '':
                out.write(line)
            else:
                out.close()
