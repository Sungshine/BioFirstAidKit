#!/usr/bin/python3

""" BLAST fasta files against the O and H serotype finder database.

Acknowledgement:    DTU - Center for Genomic Epidemiology
                    http://www.genomicepidemiology.org/
"""


import os
import subprocess


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


def oBlast(queryFile, outFilePathO):
    print ('blast O...')
    subprocess.call(['blastn',
                     '-query',
                     queryFile,
                     '-db',
                     O_blastDB,
                     '-outfmt',
                     '10',
                     '-out',
                     outFilePathO
                     ]
                    )


def hBlast(queryFile, outFilePathH):
    print ('blast H...')
    subprocess.call(['blastn',
                     '-query',
                     queryFile,
                     '-db',
                     H_blastDB,
                     '-outfmt',
                     '10',
                     '-out',
                     outFilePathH
                     ]
                    )

## uncomment the lines below for testing environment
# inputDirectory = '/home/sim/Projects/gaTest'
# outputDirectory = '/home/sim/Projects/gaTest/results/'

## uncomment the lines below for production environment
inputDirectory = '/home/sim/Projects/GA_assemblies/finalAssemblies'
outputDirectory = '/home/sim/Projects/SerotypeFinder/results/'

O_blastDB = '/home/sim/Projects/SerotypeFinder/O_type.fsa'
H_blastDB = '/home/sim/Projects/SerotypeFinder/H_type.fsa'

folders = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

for f in folders:
    base = os.path.basename(f)
    filename = os.path.splitext(base)[0]
    outFilePathO = outputDirectory + filename + '.resultO'
    outFilePathH = outputDirectory + filename + '.resultH'

    # blast in both O_type and H_type database
    if '_O' in filename and '_H' in filename:
        print(filename)
        oBlast(f, outFilePathO)
        hBlast(f, outFilePathH)

    # blast in O_type database
    elif '_H' not in filename:
        print(filename)
        oBlast(f, outFilePathO)

    # blast in H_type database
    elif '_O' not in filename:
        print(filename)
        hBlast(f, outFilePathH)