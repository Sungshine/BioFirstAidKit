#!/usr/bin/env python2.7

""" Given a list of PNUSA Ids return the SRR Id associated, assuming the SRR Id exists.

Required: NCBI eUtils executables are required in your system $PATH.
Usage: python retrieveSRR.py [path to csv file containing PNUSA Ids]
"""


import sys
import subprocess


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


filePath = sys.argv[0]

# Test case with pre-loaded list of PNUSA Ids.
# pulsenet_ids = ['PNUSAL000100', 'PNUSAL000101',]

pulsenet_ids = []

# with open(filePath, 'rb') as csvfile:
#
#     readerObject = csv.reader(csvfile, delimiter=' ', quotechar='|')
#
#     for row in readerObject:
#
#         pulsenetKey = ', '.join(row)    # remove the brackets and quotation from list elements
#         pulsenetList.append(pulsenetKey)

for key in pulsenet_ids:

    esearch = subprocess.Popen(('esearch', '-db', 'biosample', '-query', key,),
                               stdout=subprocess.PIPE,
                               )

    elink = subprocess.Popen(('elink', '-target', 'sra', '-db', 'sra',),
                             stdin=esearch.stdout,
                             stdout=subprocess.PIPE,
                             )
    esearch.stdout.close()

    efetch = subprocess.Popen(('efetch', '-format', 'xml'),
                              stdin=elink.stdout,
                              stdout=subprocess.PIPE,
                              )
    elink.stdout.close()

    xtract = subprocess.Popen(('xtract', '-pattern', 'IDENTIFIERS', '-element', 'PRIMARY_ID'),
                              stdin=efetch.stdout,
                              stdout=subprocess.PIPE,
                              )
    efetch.stdout.close()

    sauce = subprocess.Popen(('grep', 'SRR'),
                             stdin=xtract.stdout)
    xtract.stdout.close()

## TODO need to figure out how to put output into a csv format - maybe use "communicate"
## TODO need to figure out error handling for ID's that return nothing