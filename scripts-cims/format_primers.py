#!/usr/bin/python3

""" Format primer sets for input to EMBOSS primersearch program.

    Input:  tab-delimited file containing:
            primer name, forward primer sequence, reverse primer sequence
"""


import os
import csv
import sys


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


def format_primers(handle):
    """ Format primer sets for input into primersearch program.

    Returns a list object containing one primer set per line.
    """
    record = []
    reader = csv.reader(handle, delimiter='\t')
    for line in reader:
        primer_set = '{}\t{}\t{}\n'.format(line[1], line[3], line[5])
        record.append(primer_set)
    return record


if __name__ == "__main__":

    input_file = sys.argv[1]
    output_file = os.path.basename(input_file) + '.format'

    # print the list of records out to a file
    with open(input_file, 'r') as summarytable, \
            open(output_file, 'wb') as formatted:
            primer_sets = format_primers(summarytable)
            for item in primer_sets:
                formatted.write(bytes(item, 'UTF-8'))