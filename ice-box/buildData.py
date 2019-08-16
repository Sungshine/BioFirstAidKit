#!/usr/bin/env python

""" Given a list of strain ids, find matching file and copy to destination.

"""


import os
import shutil


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


# input file containing strain ids
isolates = open('/home/sim/Downloads/170_ANIb.txt', 'r')
# target directory
destinationDir = '/home/sim/Projects/ANI/aniBlastData/'

inputDirectory = '/mnt/monolith0ECOLI/2014-11-24_ecoli_cgp_annotations/cgp.gbk/'
paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

for line in isolates:
    identifier = line.rstrip()
    for file in paths:
        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]
        next = os.path.splitext(filename)[0]
        if identifier == next:
            print('moving file {} to {}'.format(file, destinationDir))
            shutil.copy(file, destinationDir)

## ghetto sanity checks
# found = Counter(arr)
# expected = Counter(existing)
# print(list((found - expected).elements()))