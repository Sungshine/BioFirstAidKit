#!/usr/bin/env python

""" Parse each metrics file of a SPAdes assemblies.

Output: csv formatted file containing desired metric numbers
"""


import os
import csv


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


def file2dict(resultFile, filename):
    """ Parses each result file from a SPAdes assembly.

    Returns desired metrics in csv format.
    """
    with open(resultFile, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        resultData = list(reader)

        for item in resultData:
            sauceList.append(item[1])

        noContigs = sauceList[5]
        largestContig = sauceList[6]
        totalLength = sauceList[7]
        gc = sauceList[8]
        nFifty = sauceList[9]
    f.close()

    # open the output csv file handle
    with open('/home/sim/Projects/GA_assemblies/QuastLog.csv', 'a') as csvout:
        fieldnames = ['strainID', '#contigs', 'largestContig', 'totalLength', 'GC%', 'N50']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerow({'strainID': filename,
                         '#contigs': noContigs,
                         'largestContig': largestContig,
                         'totalLength': totalLength,
                         'GC%': gc,
                         'N50': nFifty})
        del sauceList[:]
    csvout.close()


inputDirectory = '/home/sim/Projects/GA_assemblies/completeAssemblies'
folders = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[1]]
sauceList = []

for f in next(os.walk(inputDirectory))[1]:

    base = os.path.basename(f)
    filename = os.path.splitext(base)[0]
    filePath = os.path.join(inputDirectory, f) + '/report.tsv'
    file2dict(filePath, filename)