#!/usr/bin/env python

""" Execute SPAdes de novo assembly program on a directory of sequence reads.

Output: directory containing the contig and scaffold files in FASTA format
Usage: module_SPAdes.py </path/to/inputfiles/> </path/to/output directory/>
"""


import os
import csv
import subprocess
from timeit import default_timer


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


def wranglePairedEnds(RawReadPaths):
    """ Match each paired in read sequence.

    """
    for file in RawReadPaths:
        newfile = ""
        if 'R1' in file:
            newfile = file.replace('R1', 'R*')
        elif 'R2' in file:
            newfile = file.replace('R2', 'R*')
        if not newfile in fileHash:
            fileHash[newfile] = [file]
        else:
            fileHash[newfile].append(file)
    return


def matchStrains(file):
    """ Generate hash from line-list csv file to match up BCW_ID with strain_ID

    """
    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        linelist = list(reader)
        for b in linelist:
            bcwID = b[1]
            strainID = b[2]
            if not bcwID in matchHash:
                matchHash[bcwID] = [strainID]


def moduleSpadesSE(inputfileOne):
    """ Invoke SPAdes for unpaired read sequences.

    """
    base = os.path.basename(inputfileOne)
    filename = os.path.splitext(base)[0]
    subprocess.call(['spades.py',
                     '--careful',
                     '-s',
                     inputfileOne,
                     '-o',
                     SPAdesOutDirectory + filename + '.spades',
                     ]
                    )


def moduleSpadesPE(inputfileOne, inputfileTwo):
    """ Invoke SPAdes for paired end read sequences.

    """
    base = os.path.basename(inputfileOne)
    filebase = os.path.splitext(base)[0]
    filename = filebase.split('-M')
    file = ''
    for key, value in matchHash.items():
        if filename[0] == value[0]:
             file = key
    subprocess.call(['spades.py',
                     '--careful',
                     '-1',
                     inputfileOne,
                     '-2',
                     inputfileTwo,
                     '-o',
                     SPAdesOutDirectory + file + '.spades',
                     ]
                    )


if __name__ == '__main__':

    start = default_timer()

    inputDirectory = '/home/sim/Projects/test/reads/'
    SPAdesOutDirectory = '/home/sim/Projects/test/assemblies/'
    RawReadPaths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

    fileHash = {}
    matchHash = {}
    wranglePairedEnds(RawReadPaths)
    matchStrains(file)

    for key in fileHash:

        currentValue = fileHash.get(key)
        sortedValue = sorted(currentValue)

        # call assemblers to execute single-end read
        if len(sortedValue) == 1:
            inputfileOne = sortedValue[0]
            moduleSpadesSE(inputfileOne)

        # execute paired-end reads
        if len(sortedValue) == 2:
            inputfileOne = sortedValue[0]
            inputfileTwo = sortedValue[1]
            moduleSpadesPE(inputfileOne, inputfileTwo)

    # print "The SPAdes assemblies took: "+`default_timer() - start`