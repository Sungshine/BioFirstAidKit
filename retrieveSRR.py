__author__ = 'Sung Im'
#!/usr/bin/env python
import os
import sys
import csv
import subprocess

filePath = sys.argv[1]
edirectPath = sys.argv[2]

pulsenetList = []

with open(filePath, 'rb') as csvfile:

    readerObject = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in readerObject:

        pulsenetKey = ', '.join(row)    # remove the brackets and quotation from list elements
        pulsenetList.append(pulsenetKey)

for key in pulsenetList:

    esearch = subprocess.call([edirectPath+'esearch', '-db', 'biosample', '-query', key,])
    elink = subprocess.call([edirectPath+'elink', '-target', 'sra', '-db', 'sra',])
    efetch = subprocess.call([edirectPath+'efetch', '-format', 'xml',])
    xtract = subprocess.call([edirectPath+'xtract', '-pattern', 'IDENTIFIERS', '-element', 'PRIMARY_ID'])
    grep = subprocess.call(['grep', 'SRR'])

