#!/usr/bin/python3

""" Descriptive text goes here

"""


# import statements go here


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


class TaxRecord(object):
    """ Dictionary object to store taxonomy objects.

    """
    def __init__(self):
        self.taxonomy = {}


class Taxonomy(object):
    """ Store information from a single taxonomy classification.

    """
    def __init__(self):
        self.contig = ''
        self.superkingdom = ''
        self.kingdom = ''
        self.phylum = ''
        self.classic = ''
        self.order = ''
        self.family = ''
        self.genus = ''
        self.species = ''


def parse_kraken_labels(handle):
    record = TaxRecord()
    for line in handle:
        contigId = line.rstrip().split('\t')[0]
        classify = line.rstrip().split('\t')[1].split(';')[-1]
        taxonomy = Taxonomy()
        record.taxonomy[contigId] = []
        if 'Salmonella' in line:
            targetContigs[contigId] = classify
        else:
            otherContigs[contigId] = classify
    return record


def parse_kraken_unclassified(handle):
    unclassifedContigs = []
    for line in handle:
        if line.startswith('>'):
            contigId = line.split(' ')[0].lstrip('>')
            unclassifedContigs.append(contigId)
    return unclassifedContigs


if __name__ == "__main__":
    # otherContigs = {}
    # targetContigs = {}
    labels = open('/Users/sungshine/Downloads/2013RAN-169-M947-14-049-Loopy_contigs4.sequence.labels')

