#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Extract contig files from SPAdes output directories.
    Specify copy location.

"""


import os
import sys
import shutil


## usage: $python extract_contig_files.py <input directory> <output directory>

indir = '/data/home/sim8/Projects/cims/spades'
outdir = '/data/home/sim8/Projects/cims/assemblies'

dir_paths = [os.path.join(indir, fn) for fn in next(os.walk(indir))[2]]

for dir in dir_paths:
    contig_file = dir + "/contigs.fasta"
    fname = os.path.basename(dir)
    outpath = os.path.join(outdir, '{}.contigs.fa'.format(fname))

    shutil.copy(contig_file, outpath)
