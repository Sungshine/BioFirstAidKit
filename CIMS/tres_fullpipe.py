#!/usr/bin/python3

""" Descriptive text goes here

"""


# import statements go here


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


class TaxRecord(object):
    """ Dictionary object to store taxa objects.

    """
    def __init__(self):
        self.taxonomy = {}


def parse_kraken_labels(handle):
    """ Parse the taxa labels from kraken-translate.

    """
    record = TaxRecord()
    for line in handle:
        contigId = line.rstrip().split('\t')[0]
        classification = line.rstrip().split('\t')[1].split(';')[-1]
        record.taxonomy[contigId] = classification
    return record


def parse_kraken_unclassified(handle):
    """

    """
    unclassifiedContigs = []
    for line in handle:
        if line.startswith('>'):
            contigId = line.split(' ')[0].lstrip('>')
            unclassifiedContigs.append(contigId)
    return unclassifiedContigs


if __name__ == "__main__":

    labels = open('/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.sequence.labels', 'r')
    unclassified = open('/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.fasta.unclassified', 'r')

    targetContigs = []
    otherContigs = []
    unclassed = parse_kraken_unclassified(unclassified)
    record = parse_kraken_labels(labels)

    for contig, classification in record.taxonomy.items():
        if 'Salmonella' in classification:
            targetContigs.append(contig)
        else:
            otherContigs.append(contig)






