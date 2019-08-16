#!/usr/bin/python

""" Mass SPAdes de novo assemblies for first Vibrio MiSeq runs.

"""


import os
import sys
import subprocess


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


def wranglePairedEnds(paths):
    """ Match each paired in read sequence.

    """
    for file in paths:
        newfile = ''
        if "R1" in file:
            newfile = file.replace('R1', 'R*')
        elif "R2" in file:
            newfile = file.replace('R2', 'R*')
        if not newfile in fileHash:
            fileHash[newfile] = [file]
        else:
            fileHash[newfile].append(file)
    return


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
                     outputDirectory + filename + '.spades',
                     ]
                    )


def moduleSpadesPE(inputfileOne, inputfileTwo):
    """ Invoke SPAdes for paired end read sequences.

    """
    base = os.path.basename(inputfileOne)
    filename = os.path.splitext(base)[0]
    subprocess.call(['spades.py',
                     '--careful',
                     '-1',
                     inputfileOne,
                     '-2',
                     inputfileTwo,
                     '-o',
                     outputDirectory + filename + '.spades',
                     ]
                    )


if __name__ == '__main__':

    inputDirectory = '/home/sim/Projects/test/reads/'       #point to directory of trimmed (prinseq) files.
    outputDirectory = '/home/sim/Projects/test/assemblies/' #point to output directory where SPAdes assemblies will be stored.

    fileHash = {}
    paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

    wranglePairedEnds(paths)    #generates hash of paired-end files

    inputfileOne = ''
    inputfileTwo = ''

    for key in fileHash:

        hashValues = fileHash.get(key)
        sortedValues = sorted(hashValues)   #sorts the file-path(s)-values in hash

        if len(sortedValues) == 1:          #if key in hash has one value, invoke SPAdes for single-end read
            inputfileOne = sortedValues[0]

            moduleSpadesSE(inputfileOne)

        if len(sortedValues) == 2:          #if key in hash has two values, invoke SPAdes for paired-end reads
            inputfileOne = sortedValues[0]
            inputfileTwo = sortedValues[1]

            moduleSpadesPE(inputfileOne, inputfileTwo)
