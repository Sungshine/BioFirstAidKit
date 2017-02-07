#!/usr/bin/env python2.7

""" Build custom MLST scheme for Stx database from CGE.

"""


import os
import csv
import errno
import argparse
import itertools


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


stx1_list = []
stx2_list = []

stx1_fsa = '/Users/sim/Projects/stx/stx_data/underscored/stx1_fmt.fa'
stx2_fsa = '/Users/sim/Projects/stx/stx_data/underscored/stx2_noY_fmt.fa'

with open(stx1_fsa, 'rb') as stx1in:
    for line in stx1in:
        if line.startswith('>'):
            stx1_list.append(line.rstrip().split('_')[1])

with open(stx2_fsa, 'rb') as stx2in:
    for line in stx2in:
        if line.startswith('>'):
            stx2_list.append(line.rstrip().split('_')[1])

combined_list = []
combined_list.append(stx1_list)
combined_list.append(stx2_list)

combinations = list(itertools.product(*combined_list))

for i in combinations:
    print('{}\t{}'.format(i[0], i[1]))


