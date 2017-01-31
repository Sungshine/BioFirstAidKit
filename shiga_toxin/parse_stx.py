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

out1 = open(dir_path+'/stx1.fsa', 'wa')
out2 = open(dir_path+'/stx2.fsa', 'wa')

for line in filein:

    if line.startswith('>stx1'):
        out1.write(line)
        continue
    if line != '':
        out1.write(line)
    if line == '':
        continue
    if line.startswith('>stx2'):
        out2.write(line)
        continue
    if line != '':
        out2.write(line)
    if line == '':
        continue

out1.close()
out2.close()
