#!/usr/bin/env python

""" Given a list of ids search and move file to target directory.

"""


import os
import csv
import shutil


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


file = '/home/sim/PycharmProjects/genomics/OH_MasterList.csv'
outdir = '/home/sim/Projects/GA_assemblies/new/'

with open(file, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    arr = list(reader)

    for item in arr:
        bcwID = item[0]
        outpath = '/home/sim/Projects/GA_assemblies/' + bcwID + '.spades'
        if os.path.exists(outpath):
            shutil.move(outpath, outdir)