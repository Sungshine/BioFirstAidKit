#!/usr/bin/env python

""" Basic k-mer counting.

"""


import sys


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


def find_kmers(string, k):
    kmers = []
    n = len(string)
    for i in range(0, n-k+1):
        kmers.append(string[i:i+k])
    return kmers


if __name__ == '__main__':

    inputFile = sys.argv[1]
    find_kmers(inputFile, 11)

    fastq = open(inputFile, 'r')
    line = fastq.readline()