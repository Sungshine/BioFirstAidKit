#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" SPAdes wrapper for unpaired reads.
    Read correction is disabled.

"""


import os
import subprocess


indir = '/data/home/sim8/Projects/cims/amr'
outdir = '/data/home/sim8/Projects/cims/spades'

paths = [os.path.join(indir, fn) for fn in next(os.walk(indir))[2]]

for fp in paths:
    fname = os.path.basename(fp).split('.')[0]
    outpath = os.path.join(outdir, fname)
    subprocess.call(['spades.py', '--careful', '--only-assembler', '-s', fp, '-o', outpath,])
