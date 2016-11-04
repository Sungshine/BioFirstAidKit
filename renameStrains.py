#!/usr/bin/python

""" Strain id matching script from ANI research.

"""


import os
import csv
import shutil


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


inputDirectory = '/home/sim/Projects/GA_assemblies/completeAssemblies'
outputDirectory = '/home/sim/Projects/GA_assemblies/finalAssemblies/'
folders = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[1]]

masterList = '/home/sim/Projects/GA_assemblies/strainlists/OH_MasterListFinal.csv'
with open(masterList, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    matchList = list(reader)

for folder in folders:
    base = os.path.basename(folder)
    filename = os.path.splitext(base)[0]        # i.e. BCW_4033
    filePath = os.path.join(inputDirectory, folder) + '/contigs.fasta'

    for item in matchList:
        buildString = item[3] + ' ' + item[4]
        newPath = outputDirectory + buildString + '.fasta'

        if filename == item[0]:
            # shutil.copy(filePath, newPath)
            print filename + ',' + buildString
