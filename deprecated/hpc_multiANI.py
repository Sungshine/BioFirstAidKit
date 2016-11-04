#!/usr/bin/env python2.7

""" Execute ani.rb on a directory of fasta files.

Usage: python hpc_multiANI.py </path/to/ani.rb> </path/to/data/files>
"""


import os
import sys
import subprocess


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


aniPath = sys.argv[1]           #point to absolute path of ani.rb script
inputDirectory = sys.argv[2]    #point to directory path of data set

outputFile = open('aniBlastResults.txt', 'a')
# store file paths in list
paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]
# initialize 2D array
aniMatrix = [[[] for i in range(len(paths))] for j in range(len(paths))]

for i in range(len(paths)):
    for j in range(i+1, len(paths)):
        aniCall = subprocess.check_output([aniPath, '-q', '-1', paths[i], '-2', paths[j]])
        aniScores = aniCall.rstrip().split()
        queryBase = os.path.basename(paths[i])
        queryStrain = os.path.splitext(queryBase)[0]
        subjectBase = os.path.basename(paths[j])
        subjectStrain = os.path.splitext(subjectBase)[0]
        outputFile.write(`queryStrain` + ' vs. ' + `subjectStrain` + ': ' + aniScores[24] + '\n')
outputFile.close()