#!/usr/bin/python3

""" Unpack and parse output from Kraken-translate.

"""


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


labels = open('/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.sequence.labels')

otherContigs = {}
targetContigs = {}
unclassifiedContigs = []

for line in labels:
    contigId = line.rstrip().split('\t')[0]
    classify = line.rstrip().split('\t')[1].split(';')[-1]
    if "Salmonella" in line:
        targetContigs[contigId] = classify
    elif "Salmonella" not in line:
        otherContigs[contigId] = classify

labels.close()
unclassHandle = open('/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.fasta.unclassified')

for line in unclassHandle:
    if line.startswith('>'):
        contigId = line.split(' ')[0].lstrip('>')
        unclassifiedContigs.append(contigId)

unclassHandle.close()