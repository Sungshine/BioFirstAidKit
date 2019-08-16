#!/usr/bin/env python

""" Execute QUAST quality program on a directory of genome assemblies.

"""


import os
import subprocess


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


inputDirectory = '/home/sim/Projects/vibrio/assemblies/'
folders = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[1]]

for folder in folders:
    filePath = folder + '/contigs.fasta'
    subprocess.call(['/opt/quast-2.3/quast.py', '-o', folder, filePath])